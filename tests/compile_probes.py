"""Compile a small BL conformance sample against a freshly compiled Z8 compiler.

Run: python tests/compile_probes.py --z8-root PATH [--eclipse-cache PATH]
This tests the BL compiler stage, not compilation or execution of generated Java.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

CASES = [
    ("method and integer addition", 'public class SpecProbe { public int sum(int a, int b) { return a + b; } }', None),
    ("array initializer and index", 'public class SpecProbe { public int test() { int[] a = {1, 2}; return a[0]; } }', None),
    ("map initializer and index", 'public class SpecProbe { public string test() { string[int] a = {(1, "v")}; return a[1]; } }', None),
    ("for with condition and step", 'public class SpecProbe { public int test() { int s = 0; for (int i = 0; i < 3; i += 1) { s += i; } return s; } }', None),
    ("nested block comments", '/* outer /* inner */ tail */ public class SpecProbe { public bool test() { return true && false; } }', None),
    ("date in year 1000", "public class SpecProbe { public date test() { return '01/01/1000'; } }", None),
    ("elvis expression", 'public class SpecProbe { public string test(string s) { return s ?: "x"; } }', None),
    ("new without parentheses", 'public class SpecProbe { public SpecProbe test() { return new SpecProbe; } }', None),
    ("for without condition or step", 'public class SpecProbe { public void test() { for (;;) { break; } } }', 'Syntax error'),
    ("decimal exponent without sign", 'public class SpecProbe { public decimal test() { return 1.0e2; } }', 'expected exponent sign'),
    ("guid record", "public class SpecProbe { records { X = '00000000-0000-0000-0000-000000000001'; } }", None),
    ("integer record rejected", 'public class SpecProbe { records { X = 1; } }', 'use guid'),
    ("break outside loop rejected", 'public class SpecProbe { public void f() { break; } }', 'cannot be used outside of a loop'),
    ("value from void rejected", 'public class SpecProbe { public void f() { return 1; } }', 'Void methods cannot return a value'),
    ("bodyless non-native rejected", 'public class SpecProbe { public void f(); }', 'requires a body'),
    ("final local reassignment accepted", 'public class SpecProbe { public int f() { final int x = 1; x = 2; return x; } }', None),
    ("final field reassignment accepted", 'public class SpecProbe { public final int x = 1; public void f() { x = 2; } }', None),
    ("qualified map key rejected", 'public class SpecProbe { public void f() { string[org.zenframework.z8.lang.int] x; } }', 'identifier expected'),
    ("repeated enum comma accepted", 'public enum SpecProbe { One,, Two }', None),
    ("boolean condition", 'public class SpecProbe { public int f(bool c) { if (c) return 1; else return 2; } }', None),
    ("integer condition rejected", 'public class SpecProbe { public int f() { if (1) return 1; else return 2; } }', 'cannot convert from int to bool'),
    ("datespan literal", "public class SpecProbe { public datespan f() { return '1 12:30:20'; } }", None),
    ("guid literal", "public class SpecProbe { public guid f() { return '00000000-0000-0000-0000-000000000001'; } }", None),
    ("binary literal", "public class SpecProbe { public binary f() { return '1, 0xFF'; } }", None),
    ("chained assignment rejected", 'public class SpecProbe { public void f() { int a; int b; int c; a = b = c; } }', 'Syntax error'),
    ("null return in int method accepted", 'public class SpecProbe { public int f() { return null; } }', None),
    ("empty array initializer", 'public class SpecProbe { public int f() { int[] x = {}; return x[0]; } }', None),
    ("decimal literal Java generation", 'public class SpecProbe { public decimal f() { return 0.12345678901234567890; } }', None),
    ("time-only literal Java generation", "public class SpecProbe { public date f() { return '12:34:56'; } }", None),
    ('public field', 'public class SpecProbe {public int x;}', None),
    ('default field', 'public class SpecProbe {int x;}', None),
    ('private field', 'public class SpecProbe {private int x;}', None),
    ('protected field', 'public class SpecProbe {protected int x;}', None),
    ('virtual field', 'public class SpecProbe {virtual int x;}', 'Modifier is illegal'),
    ('auto primary array', 'public class SpecProbe {auto int[] x;}', 'auto cannot be applied'),
    ('auto reference array', 'public class SpecProbe {auto Value[] x;}', None),
    ('auto map', 'public class SpecProbe {auto Value[int] x;}', 'one-dimensional array'),
    ('auto multidimensional', 'public class SpecProbe {auto Value[][] x;}', 'one-dimensional array'),
    ('static int', 'public class SpecProbe {static int x;}', None),
    ('static int array', 'public class SpecProbe {static int[] x;}', None),
    ('static reference', 'public class SpecProbe {static Value x;}', 'static cannot be used for a reference'),
    ('static reference array', 'public class SpecProbe {static Value[] x;}', 'static cannot be used for a reference'),
    ('duplicate static', 'public class SpecProbe {static static int x;}', 'Syntax error'),
    ('conflicting access', 'public class SpecProbe {public private int x;}', 'Syntax error'),
    ('duplicate attributes', 'public class SpecProbe {[name "A"] [name "B"] Value x;}', 'declared more then once'),
    ('static virtual method', 'public class SpecProbe {virtual static int f(){return 1;}}', 'Modifier is illegal'),
    ('auto method', 'public class SpecProbe {auto int f(){return 1;}}', 'Modifier is illegal'),
    ('virtual method', 'public class SpecProbe {virtual int f(){return 1;}}', None),
    ('nested local redefinition', 'public class SpecProbe {public int f(){int x=1;{int x=2;} return x;}}', 'redefinition'),
    ('local shadows field', 'public class SpecProbe {int x=1;public int f(){int x=2;return x;}}', None),
    ('parameter redefinition', 'public class SpecProbe {public int f(int x){int x=2;return x;}}', 'redefinition'),
    ('duplicate field', 'public class SpecProbe {int x;int x;}', 'Duplicate field'),
    ('attribute on primary', 'public class SpecProbe {[foo] int x;}', 'Attributes can only be applied'),
    ('attribute on reference', 'public class SpecProbe {[foo] Value x;}', None),
    ('static record', "public class SpecProbe {records {static X='00000000-0000-0000-0000-000000000001';}}", 'Modifier is illegal'),
    ('instance field in static method', 'public class SpecProbe {int x;static public int f(){return x;}}', 'Cannot make a static reference'),
    ('this in static method', 'public class SpecProbe {static public SpecProbe f(){return this;}}', 'cannot use this in a static context'),
    ('final method', 'public class SpecProbe {final int f(){return 1;}}', 'Syntax error'),
]


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          text=True, encoding="utf-8", errors="replace", timeout=120)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--z8-root', type=Path, required=True)
    parser.add_argument('--eclipse-cache', type=Path, default=Path.home() / '.gradle/caches/modules-2/files-2.1/org.zenframework.z8.dependencies.eclipse')
    args = parser.parse_args()
    source = args.z8_root / 'org.zenframework.z8.compiler/src/main/java'
    library = args.z8_root / 'org.zenframework.z8.lang/src/bl'
    jars = sorted(p for p in args.eclipse_cache.rglob('*.jar') if '3.4-cert' in p.parts and not p.name.endswith('-sources.jar'))
    if not source.is_dir() or not library.is_dir() or not jars:
        raise SystemExit('Compiler source, BL library or cached Eclipse 3.4-cert dependencies not found.')
    with tempfile.TemporaryDirectory(prefix='bl-spec-probes-') as tmp:
        tmp = Path(tmp)
        classes, project, output = tmp / 'classes', tmp / 'project', tmp / 'output'
        classes.mkdir(); (project / 'src').mkdir(parents=True); output.mkdir()
        shutil.copytree(library, project / 'src/bl')
        files = sorted(source.rglob('*.java'))
        build = run(['javac', '-encoding', 'UTF-8', '-source', '8', '-target', '8', '-cp', os.pathsep.join(map(str, jars)), '-d', str(classes), *map(str, files)])
        if build.returncode:
            raise SystemExit('Compiler build failed:\n' + build.stdout)
        classpath = os.pathsep.join([str(classes), *map(str, jars)])
        lexer_source = Path(__file__).with_name('LexerProbes.java')
        lexer_build = run(['javac', '-encoding', 'UTF-8', '-source', '8', '-target', '8', '-cp', classpath, '-d', str(classes), str(lexer_source)])
        if lexer_build.returncode:
            raise SystemExit('Lexer probe build failed:\n' + lexer_build.stdout)
        lexer_result = run(['java', '-cp', classpath, 'LexerProbes'])
        if lexer_result.returncode or 'PASS:' not in lexer_result.stdout:
            raise SystemExit('Lexer probes failed:\n' + lexer_result.stdout)
        print(lexer_result.stdout.strip(), flush=True)
        command = ['java', '-cp', classpath, 'org.zenframework.z8.compiler.cmd.Main', str(project), '-projectName:verify', '-sources:src/bl', '-output:' + str(output)]
        probe = project / 'src/bl/SpecProbe.bl'
        (project / 'src/bl/Value.bl').write_text('public class Value { public int field; virtual public int get(){return 0;} }', encoding='utf-8')
        for name, code, error in CASES:
            probe.write_text(code, encoding='utf-8')
            result = run(command)
            passed = (result.returncode == 0 and 'Error(s) 0' in result.stdout) if error is None else (result.returncode != 0 and error in result.stdout)
            if not passed:
                raise SystemExit(f'FAIL {name}:\n{result.stdout}')
            if name == 'decimal literal Java generation':
                generated = (output / 'SpecProbe.java').read_text(encoding='utf-8')
                if 'new decimal(0.12345678901234567890)' not in generated:
                    raise SystemExit('FAIL: decimal literal was not emitted as the expected unquoted Java argument')
            if name == 'time-only literal Java generation':
                import re
                generated = (output / 'SpecProbe.java').read_text(encoding='utf-8')
                if not re.search(r'new date\(-?\d+L\)', generated):
                    raise SystemExit('FAIL: time-only literal was not emitted as milliseconds')
            print('PASS', name, flush=True)
        access_checks = 0
        for access in ('', 'public', 'protected', 'private'):
            for kind in ('field', 'method'):
                for relation in ('unrelated', 'subclass'):
                    field = access + ' int field=4;'
                    method = access + ' int method(){return 4;}'
                    (project / 'src/bl/Value.bl').write_text('public class Value {' + field + method + '}', encoding='utf-8')
                    member = 'field' if kind == 'field' else 'method()'
                    source = ('public class SpecProbe {public int f(){Value x;return x.' + member + ';}}'
                              if relation == 'unrelated' else
                              'public class SpecProbe extends Value {public int f(){return ' + member + ';}}')
                    probe.write_text(source, encoding='utf-8')
                    result = run(command)
                    allowed = access in ('', 'public') or (access == 'protected' and relation == 'subclass')
                    passed = (result.returncode == 0 and 'Error(s) 0' in result.stdout) if allowed else (result.returncode != 0 and 'not visible' in result.stdout)
                    name = f"{access or 'default'} {kind} from {relation}"
                    if not passed:
                        raise SystemExit(f'FAIL {name}:\n{result.stdout}')
                    access_checks += 1
                    print('PASS', name, flush=True)
        # The parser accepts type modifiers syntactically; check whether a type in
        # a different package can actually be referenced and what Java is emitted.
        probe.unlink()
        (project / 'src/bl/Value.bl').unlink()
        package_p = project / 'src/bl/p'; package_p.mkdir()
        package_q = project / 'src/bl/q'; package_q.mkdir()
        (package_q / 'SpecProbe.bl').write_text('import p.Value;public class SpecProbe {public int f(){Value v;return v.field;}}', encoding='utf-8')
        for modifier in ('private', 'protected', 'public', 'static', 'auto', 'virtual'):
            (package_p / 'Value.bl').write_text(modifier + ' class Value {public int field=7;}', encoding='utf-8')
            result = run(command)
            if result.returncode or 'Error(s) 0' not in result.stdout:
                raise SystemExit(f'FAIL {modifier} type across packages:\n{result.stdout}')
            generated = (output / 'p/Value.java').read_text(encoding='utf-8')
            if 'public class Value extends OBJECT' not in generated:
                raise SystemExit(f'FAIL {modifier} type Java declaration differs:\n{generated}')
            access_checks += 1
            print('PASS', modifier, 'type across packages', flush=True)
        print(f'{len(CASES) + access_checks} BL compiler probes passed; generated Java was not compiled or executed.')


if __name__ == '__main__':
    main()
