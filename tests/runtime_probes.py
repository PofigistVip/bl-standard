"""Build Z8 from source with JDK 8 and test BL -> Java -> execution.

Run: python tests/runtime_probes.py --z8-root PATH --jdk8 JDK_PATH
All generated sources, Java classes and resources are stored in a temporary directory.
The dependency cache must contain the dependencies of this Z8 revision.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

DEFAULT_VALUE = 'public class Value { virtual public int value(){return 1;} }'
# label, Value.bl, SpecProbe.bl, expected stage, expected value/message
CASES = [
    ('arithmetic precedence', None, 'public class SpecProbe {public int f(){return 1+2*3;}}', 'run', '7'),
    ('default local int', None, 'public class SpecProbe {public int f(){int a;return a;}}', 'run', '0'),
    ('final reassignment', None, 'public class SpecProbe {public int f(){final int a=1;a=2;return a;}}', 'run', '2'),
    ('null return', None, 'public class SpecProbe {public int f(){return null;}}', 'run', '<null>'),
    ('null makes overload ambiguous', None, 'public class SpecProbe {int pick(int x){return 1;}int pick(string x){return 2;}public int f(){return pick(null);}}', 'bl-error', 'ambiguous'),
    ('null logical and fails Java', None, 'public class SpecProbe {public bool f(){return null && true;}}', 'javac-error', 'bad operand types'),
    ('array alias', None, 'public class SpecProbe {public int f(){int[] a={1};int[] b=a;b.set(0,9);return a[0];}}', 'run', '9'),
    ('array indexed assignment', None, 'public class SpecProbe {public int f(){int[] a={1};a[0]=9;return a[0];}}', 'javac-error', 'unexpected type'),
    ('array compound assignment', None, 'public class SpecProbe {int n=0;int idx(){n+=1;return 0;}public int f(){int[] a={1};a[idx()]+=4;return n;}}', 'javac-error', 'unexpected type'),
    ('map indexed assignment', None, 'public class SpecProbe {public int f(){int[int] a={(1,9)};a[1]=5;return a[1];}}', 'javac-error', 'unexpected type'),
    ('argument order', None, 'public class SpecProbe {int n=0;int mark(int d){n=n*10+d;return d;}int combine(int a,int b){return n;}public int f(){return combine(mark(1),mark(2));}}', 'run', '12'),
    ('binary operand order', None, 'public class SpecProbe {int n=0;int mark(int d){n=n*10+d;return d;}public int f(){int x=mark(1)+mark(2);return n;}}', 'run', '12'),
    ('compound receiver evaluated twice', 'public class Value {public int field=0;}', 'public class SpecProbe {Value v;int n=0;Value fetch(){n+=1;return v;}public int f(){fetch().field+=1;return n;}}', 'run', '2'),
    ('simple receiver evaluated once', 'public class Value {public int field=0;}', 'public class SpecProbe {Value v;int n=0;Value fetch(){n+=1;return v;}public int f(){fetch().field=1;return n;}}', 'run', '1'),
    ('map initializer order', None, 'public class SpecProbe {int n=0;int mark(int d){n=n*10+d;return d;}public int f(){int[int] m={(mark(1),mark(2)),(mark(3),mark(4))};return n;}}', 'run', '1324'),
    ('short circuit and', None, 'public class SpecProbe {int n=0;bool mark(){n+=1;return true;}public int f(){bool x=false && mark();return n;}}', 'run', '0'),
    ('short circuit or', None, 'public class SpecProbe {int n=0;bool mark(){n+=1;return true;}public int f(){bool x=true || mark();return n;}}', 'run', '0'),
    ('sql bool evaluates right operand', None, 'public class SpecProbe {int n=0;sql_bool mark(){n+=1;return true;}public int f(){sql_bool x=false;sql_bool y=x && mark();return n;}}', 'run', '1'),
    ('priority operator reference return', 'public class Value {public int n=0;public operator(){n+=1;return this;}}', 'public class SpecProbe {public int f(){Value x;Value y=(x);return x.n;}}', 'javac-error', 'cannot find symbol'),
    ('elvis nonnull', None, 'public class SpecProbe {int n=0;string mark(){n+=1;return "r";}public int f(){string x="l";string s=x ?: mark();return n;}}', 'run', '0'),
    ('elvis null', None, 'public class SpecProbe {int n=0;string mark(){n+=1;return "r";}public int f(){string x=null;string s=x ?: mark();return n;}}', 'run', '1'),
    ('scalar assignment', None, 'public class SpecProbe {public int f(){int a=1;int b=a;b+=1;return a;}}', 'run', '1'),
    ('parameter reassignment', None, 'public class SpecProbe {void change(int a){a=9;}public int f(){int x=1;change(x);return x;}}', 'run', '1'),
    ('map alias', None, 'public class SpecProbe {public int f(){int[int] a={(1,2)};int[int] b=a;b.add(1,9);return a[1];}}', 'run', '9'),
    ('exact overload', None, 'public class SpecProbe {int pick(int x){return 1;}int pick(decimal x){return 2;}public int f(){return pick(1);}}', 'run', '1'),
    ('foreach', None, 'public class SpecProbe {public int f(){int n=0;int[] a={1,2,3};for(int x : a){n+=x;}return n;}}', 'run', '6'),
    ('exception catch', None, 'public class SpecProbe {public int f(){try {int x=1/0;}catch(exception e){return 7;}return 0;}}', 'run', '7'),
    ('finally', None, 'public class SpecProbe {int n=0;int g(){try{return 7;}finally{n=9;}}public int f(){int x=g();return x*10+n;}}', 'run', '79'),
    ('integer overflow', None, 'public class SpecProbe {public int f(){int x=0x7fffffffffffffff;return x+1;}}', 'run', '-9223372036854775808'),
    ('virtual override', 'public class Value {virtual public int f(){return 1;}}', 'public class SpecProbe extends Value {public int f(){return 2;}}', 'run', '2'),
    ('non-virtual override', 'public class Value {public int f(){return 1;}}', 'public class SpecProbe extends Value {public int f(){return 2;}}', 'bl-error', 'is not virtual'),
    ('inherited initialization', 'public class Value {public int x=2;public int y=x+3;}', 'public class SpecProbe extends Value {public int f(){return y;}}', 'run', '5'),
    ('closure captured value', None, 'public class SpecProbe {public int f(){int x=3;Value v=class {public int value(){return x;}};x=9;return v.value();}}', 'run', '3'),
    ('nested container', None, 'public class SpecProbe {int n=7;Value v=class {public int value(){return container.n;}};public int f(){return v.value();}}', 'run', '7'),
    ('closure shared array', None, 'public class SpecProbe {public int f(){int[] x={3};Value v=class {public int value(){return x[0];}};x.set(0,9);return v.value();}}', 'run', '9'),
    ('covariant mutable array', None, 'public class SpecProbe {public int f(){Child[] c={};Value[] v=c;v.add(new Value);Child first=c[0];return 1;}}', 'run-error', 'ClassCastException'),
    ('overload base distance ignored', 'import org.zenframework.z8.lang.Object;public class Value extends Object {}', 'import org.zenframework.z8.lang.Object;public class SpecProbe {int pick(Object x){return 1;}int pick(Value x){return 2;}public int f(){Child x;return pick(x);}}', 'bl-error', 'ambiguous'),
]

RUNNER = '''public class Runner {
  public static void main(String[] args) throws Exception {
    java.lang.reflect.Field f=org.zenframework.z8.server.config.ServerConfig.class.getDeclaredField("language");
    f.setAccessible(true); f.set(null,"ru");
    p.SpecProbe o=new p.SpecProbe.CLASS<p.SpecProbe>(null).get();
    Object v=o.z8_f();
    System.out.println("RESULT="+(v==null?"<null>":v.toString()));
  }
}'''


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          text=True, encoding='utf-8', errors='replace', timeout=180)


def checked(command: list[str], cwd: Path, label: str) -> None:
    result = run(command, cwd)
    if result.returncode:
        raise SystemExit(f'{label} failed:\n{result.stdout}')


def argfile(path: Path, arguments: list[str]) -> None:
    # Arguments use forward slashes so quoted Windows paths do not lose backslashes.
    path.write_text('\n'.join('"' + arg.replace('\\', '/') + '"' for arg in arguments), encoding='utf-8')


def manifest_jar(path: Path, jars: list[Path]) -> None:
    logical = 'Class-Path: ' + ' '.join(p.resolve().as_uri() for p in jars)
    lines = [logical[:70]]
    logical = logical[70:]
    while logical:
        lines.append(' ' + logical[:69])
        logical = logical[69:]
    manifest = 'Manifest-Version: 1.0\r\n' + '\r\n'.join(lines) + '\r\n\r\n'
    with zipfile.ZipFile(path, 'w') as jar:
        jar.writestr('META-INF/MANIFEST.MF', manifest)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--z8-root', type=Path, required=True)
    p.add_argument('--jdk8', type=Path, required=True)
    p.add_argument('--case', action='append', help='Run only the named case; may be repeated')
    p.add_argument('--dependency-cache', type=Path, default=Path.home()/'.gradle/caches/modules-2/files-2.1')
    a = p.parse_args()
    root = a.z8_root.resolve()
    javac = a.jdk8 / 'bin' / ('javac.exe' if os.name == 'nt' else 'javac')
    java = a.jdk8 / 'bin' / ('java.exe' if os.name == 'nt' else 'java')
    boot_src = root/'org.zenframework.z8.boot/src/main/java'
    server_src = root/'org.zenframework.z8.server/src/main/java'
    compiler_src = root/'org.zenframework.z8.compiler/src/main/java'
    library = root/'org.zenframework.z8.lang/src/bl'
    if not all(p.exists() for p in (javac, java, boot_src, server_src, compiler_src, library, a.dependency_cache)):
        raise SystemExit('JDK, Z8 source or dependency cache not found')
    version = run([str(javac), '-version'], root)
    if '1.8.' not in version.stdout:
        raise SystemExit(f'JDK 8 required, got: {version.stdout}')
    jars = sorted((x for x in a.dependency_cache.rglob('*.jar') if not any(y in x.name for y in ('-sources.jar', '-javadoc.jar', '-tests.jar'))),
                  key=lambda x: (0 if '3.4-cert' in x.parts else 1, x.as_posix()))
    if not jars:
        raise SystemExit('No cached dependency jars found')
    with tempfile.TemporaryDirectory(prefix='bl-runtime-probes-') as temp:
        work = Path(temp)
        boot, server, compiler, generated = (work/x for x in ('boot', 'server', 'compiler', 'generated'))
        for directory in (boot, server, compiler, generated): directory.mkdir()
        project = work/'project'; (project/'src').mkdir(parents=True)
        shutil.copytree(library, project/'src/bl')
        sources = project/'src/bl/p'; sources.mkdir()
        depjar = work/'deps.jar'; manifest_jar(depjar, jars)
        checked([str(javac), '-encoding', 'UTF-8', '-source', '8', '-target', '8', '-d', str(boot),
                 *map(str, sorted(boot_src.rglob('*.java')))], work, 'boot build')
        argsfile = work/'server.args'
        argfile(argsfile, ['-Xbootclasspath/p:' + str(boot), '-encoding', 'UTF-8', '-source', '8', '-target', '8',
                          '-cp', os.pathsep.join(map(str, jars)), '-d', str(server), *map(str, sorted(server_src.rglob('*.java')))])
        checked([str(javac), '@' + str(argsfile)], work, 'server build')
        compiler_jars = [x for x in jars if 'org.zenframework.z8.dependencies.eclipse' in x.parts and '3.4-cert' in x.parts]
        if not compiler_jars: raise SystemExit('Z8 Eclipse 3.4-cert dependency jars not found')
        checked([str(javac), '-encoding', 'UTF-8', '-source', '8', '-target', '8', '-cp', os.pathsep.join(map(str, compiler_jars)),
                 '-d', str(compiler), *map(str, sorted(compiler_src.rglob('*.java')))], work, 'BL compiler build')
        print('PASS: boot, server and BL compiler rebuilt from source', flush=True)
        runner = work/'Runner.java'; runner.write_text(RUNNER, encoding='utf-8')
        bcp = os.pathsep.join(map(str, [compiler, depjar]))
        rcp = os.pathsep.join(map(str, [generated, server, depjar]))
        bl_command = [str(java), '-cp', bcp, 'org.zenframework.z8.compiler.cmd.Main', str(project),
                      '-projectName:verify', '-sources:src/bl', '-output:' + str(generated)]
        selected = [case for case in CASES if not a.case or case[0] in a.case]
        if a.case and len(selected) != len(set(a.case)):
            raise SystemExit('Unknown --case name')
        for name, value, source, stage, expected in selected:
            (sources/'Value.bl').write_text(value or DEFAULT_VALUE, encoding='utf-8')
            (sources/'Child.bl').write_text('public class Child extends Value {}', encoding='utf-8')
            (sources/'SpecProbe.bl').write_text(source, encoding='utf-8')
            result = run(bl_command, work)
            if stage == 'bl-error':
                if result.returncode == 0 or expected not in result.stdout:
                    raise SystemExit(f'FAIL {name}: expected BL error {expected!r}:\n{result.stdout}')
            else:
                if result.returncode or 'Error(s) 0' not in result.stdout:
                    raise SystemExit(f'FAIL {name}: BL compilation:\n{result.stdout}')
                result = run([str(javac), '-encoding', 'UTF-8', '-cp', rcp, '-d', str(generated),
                              str(generated/'p/Value.java'), str(generated/'p/Child.java'), str(generated/'p/SpecProbe.java'), str(runner)], work)
                if stage == 'javac-error':
                    if result.returncode == 0 or expected not in result.stdout:
                        raise SystemExit(f'FAIL {name}: expected javac error {expected!r}:\n{result.stdout}')
                else:
                    if result.returncode:
                        raise SystemExit(f'FAIL {name}: generated Java:\n{result.stdout}')
                    result = run([str(java), '-cp', rcp, 'Runner'], work)
                    if stage == 'run-error':
                        if not result.returncode or expected not in result.stdout:
                            raise SystemExit(f'FAIL {name}: expected runtime error {expected!r}:\n{result.stdout}')
                    elif result.returncode or ('RESULT=' + expected) not in result.stdout.splitlines():
                        raise SystemExit(f'FAIL {name}: execution:\n{result.stdout}')
            print('PASS:', name, flush=True)
        print(f'PASS: {len(selected)} BL-to-Java/runtime probes', flush=True)


if __name__ == '__main__':
    main()
