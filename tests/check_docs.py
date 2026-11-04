"""Check Markdown links, extracted grammar, keyword inventories, and BL file index."""
from __future__ import annotations
import argparse
from pathlib import Path
import re
from urllib.parse import unquote

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--z8-root', required=True, type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
compiler = args.z8_root / 'org.zenframework.z8.compiler/src/main'
bl = args.z8_root / 'org.zenframework.z8.lang/src/bl'
errors: list[str] = []
for path in root.glob('*.md'):
    source = path.read_text(encoding='utf-8-sig')
    for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', source):
        target = unquote(target.split('#', 1)[0])
        if target and '://' not in target and not (path.parent / target).exists():
            errors.append(f'{path.name}: missing link {target}')

grammar = (compiler / 'grammar/Grammar.y').read_text(encoding='utf-8').split('%%')[1]
lines = []
for line in grammar.splitlines():
    if '/*' in line or '*/' in line:
        continue
    if re.search(r'\b(error\(|onMissingSemicolon\(|onStatement1\(|onStatement2\()', line):
        continue
    lines.append(re.sub(r'\s*\{\s*parser\.[^}]*\}', '', line).rstrip())
while lines and not lines[-1].strip():
    lines.pop()
expected = re.sub(r'(?m)^([A-Za-z][A-Za-z0-9]*)\n\s*\|', r'\1\n\t:', '\n'.join(lines))
document = (root / '08-grammar.md').read_text(encoding='utf-8')
actual = document.split('```yacc\n', 1)[1].split('\n```', 1)[0]
if expected != actual:
    errors.append('08-grammar.md: extracted productions differ from Grammar.y')

lexer = (compiler / 'java/org/zenframework/z8/compiler/parser/grammar/lexer/Lexer.java').read_text(encoding='utf-8')
lexical = (root / '02-lexical.md').read_text(encoding='utf-8')
for group, pattern in [('keyword', r'keywords\.put\("(\w+)"'), ('reserved', r'reserved\.add\("(\w+)"')]:
    for name in re.findall(pattern, lexer):
        if f'`{name}`' not in lexical:
            errors.append(f'02-lexical.md: {group} {name} missing')

catalog = (root / '11-library-catalog.md').read_text(encoding='utf-8').split('## 11.2', 1)[1]
listed = set(re.findall(r'^- `([^`]+\.bl)`$', catalog, re.M))
found = {p.relative_to(bl).as_posix() for p in bl.rglob('*.bl')}
if listed != found:
    errors.append(f'11-library-catalog.md: {len(found-listed)} omitted, {len(listed-found)} obsolete file paths')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: local links, source grammar, lexer keywords/reserved names and {len(found)} BL file paths')
