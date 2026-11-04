"""Compare the checked-in Yacc source with the generated parser's rules and actions.

This is not a comparison of LR action/goto tables or a regeneration of Grammar.java.
"""
from pathlib import Path
import argparse
import re

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--z8-root', required=True, type=Path)
args = parser.parse_args()
base = args.z8_root / 'org.zenframework.z8.compiler/src/main'
yacc = (base / 'grammar/Grammar.y').read_text(encoding='utf-8').split('%%')[1]
java = (base / 'java/org/zenframework/z8/compiler/parser/grammar/Grammar.java').read_text(encoding='utf-8')
rules = []
name = None
for line in yacc.splitlines():
    line = line.strip()
    if re.fullmatch(r'[A-Za-z][A-Za-z0-9]*', line):
        name = line
    elif line.startswith((':', '|')):
        rhs, *action = line[1:].split('{', 1)
        rules.append((name, rhs.split(), action[0].rsplit('}', 1)[0].strip() if action else None))


def array(name: str) -> list[int]:
    match = re.search(r'int ' + name + r'\[\] = \{(.*?)\};', java, re.S)
    if match is None:
        raise SystemExit(f'Missing {name} array')
    return [int(value) for value in re.findall(r'-?\d+', match.group(1))]


lhs, lengths = array('yyr1'), array('yyr2')
if len(lhs) - 1 != len(rules) or len(lengths) - 1 != len(rules):
    raise SystemExit('Rule count does not match parser tables')
ids: dict[str, int] = {}
for number, (name, rhs, _) in enumerate(rules, 1):
    if len(rhs) != lengths[number]:
        raise SystemExit(f'Rule {number} ({name}) has a different right-hand length')
    if name in ids and ids[name] != lhs[number]:
        raise SystemExit(f'Rule {number} ({name}) has a different left-hand symbol')
    ids[name] = lhs[number]
if len(set(ids.values())) != len(ids):
    raise SystemExit('Two nonterminal names map to the same generated left-hand symbol')

actions = {int(number): action.strip() for number, action in re.findall(
    r'case (\d+):\s*\{\s*(.*?)\s*\}\s*break;', java, re.S)}
expected = set()
for number, (name, rhs, action) in enumerate(rules, 1):
    if action is None:
        continue
    expected.add(number)
    transformed = re.sub(r'\$(\d+)', lambda m: 's[s1 - ' + str(len(rhs) - int(m.group(1))) + ']', action)
    compact = lambda s: re.sub(r'\s+', '', s)
    if number not in actions or compact(transformed) != compact(actions[number]):
        raise SystemExit(f'Action {number} ({name}) differs from Grammar.y')
if set(actions) != expected:
    raise SystemExit('Parser has unexpected generated actions')
print(f'PASS: {len(rules)} productions, left-hand groups, lengths and {len(actions)} actions; LR tables not regenerated')
