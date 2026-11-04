# 8. Грамматика реализации

Источник: `C/grammar/Grammar.y`, `C/java/org/zenframework/z8/compiler/parser/grammar/Parser.java`, `grammar/lexer/Lexer.java`. Это автоматически извлечённая справочная грамматика из исходного yacc-файла на зафиксированной ревизии, с удалёнными Java-действиями и очевидными альтернативами диагностики/восстановления. Она не является автономным парсером и не заменяет семантические проверки. Автоматическое удаление действий и ветвей ошибок может изменить разрешение конфликтов или поведение восстановления; при сомнении авторитетны исходный `Grammar.y`, его действия и фактический сгенерированный parser. Извлечённые строки проверяются скриптом `tests/check_docs.py`. `tests/check_parser.py` дополнительно сравнивает 288 продукций с массивами длин и групп левых частей `Grammar.java` и сравнивает 202 семантических действия. Переходы LR-автомата, разрешение конфликтов и сами символы правых частей из таблиц такой проверкой не доказываются; повторная генерация parser не выполнялась. Исходная грамматика находится в проекте Z8, распространяемом вместе с `LICENSE` LGPL-3.0.

## 8.1 Обозначения

Использована нотация yacc: имя правила на отдельной строке, `:` начинает альтернативы, `|` отделяет их, `;` завершает правило. Пустая альтернатива означает пустую последовательность. Имена в нижнем/смешанном регистре — нетерминалы; имена токенов перечислены ниже. `{ ... }` в этой секции являются только частью исходных действий и удалены; литеральные скобки обозначаются токенами. Начальный символ — `program`. Неиспользуемые lexer-токены и Yacc-приоритеты не включены; конкретные конфликты определяются исходной грамматикой и сгенерированными таблицами.

## 8.2 Соответствие токенов

| Токен | Написание |
|---|---|
| `Identifier` | идентификатор |
| `Constant` | числовой, строковый, булев, date, datespan, guid или binary литерал |
| `LBrace`, `RBrace` | `(`, `)` |
| `LBracket`, `RBracket` | `[`, `]` |
| `LCBrace`, `RCBrace` | `{`, `}` |
| `Colon`, `Semicolon`, `Comma`, `Dot` | `:`, `;`, `,`, `.` |
| `Question`, `Elvis` | `?`, `?:` |
| `Assign`, `AddAssign`, `SubAssign`, `MulAssign`, `DivAssign`, `ModAssign`, `BitwiseAndAssign`, `BitwiseOrAssign`, `BitwiseXorAssign` | `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `&=`, `\|=`, `^=` |
| `Not`, `BitwiseNot`, `Mul`, `Div`, `Mod`, `Plus`, `Minus` | `!`, `~`, `*`, `/`, `%`, `+`, `-` |
| `Equ`, `NotEqu`, `Less`, `More`, `LessEqu`, `MoreEqu` | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| `BitwiseAnd`, `BitwiseOr`, `BitwiseXor`, `And`, `Or` | `&`, `\|`, `^`, `&&`, `\|\|` |
| `Operator`, `InstanceOf` | `operator`, `instanceof` |
| остальные токены с заглавной буквы | ключевое слово, полученное переводом имени токена в нижний регистр, например `Class` → `class`, `This` → `this` |

Семантика и допустимые символы лексем приведены в [лексическом разделе](02-lexical.md). `null` — `Null`, а не `Constant`. Термин `LBrace` в исходниках означает круглую скобку, а не фигурную.

## 8.3 Продукции

```yacc


program
	:
	| import
	| classes
	| import classes
	;

classes
	: classEnum
	| classes classEnum
	;

classEnum
	: class
	| enum
	;

import
	: importList
	;

importList
	: importElement
	| importList importElement
	;

importElement
	: Import qualifiedName Semicolon
	;

attribute
	: LBracket Identifier RBracket
	| LBracket Identifier Constant RBracket
	| LBracket Identifier expression RBracket
	;

access
	: Public
	| Private
	| Protected
	| Static
	| Auto
	| Virtual
	;

modifier
	: access
	| attribute
	;

modifiers
	: modifier
	| modifiers modifier
	;

qualifiedName
	: Identifier
	| qualifiedName Dot Identifier
	;

enumKeyword
	: Enum
	;

enumName
	: Identifier
	;

simpleEnumHeader
	: enumKeyword enumName
	;

enumHeader
	: simpleEnumHeader
	| modifiers simpleEnumHeader
	;

enum
	: enumHeader enumBody
	;

enumBodyLCBrace
	: LCBrace
	;

enumIdentifier
	: Identifier
	;

enumMembers
	: enumIdentifier
	| enumMembers Comma enumIdentifier
	| enumMembers Comma
	;

enumBodyLeft
	: enumBodyLCBrace
	| enumBodyLCBrace enumMembers
	;

enumBody
	: enumBodyLeft RCBrace
	;

classKeyword
	: Class
	| Final Class
	;

className
	: Identifier
	;

extendsKeyword
	: Extends
	;

baseName
	: qualifiedName
	;

simpleClassHeader
	: classKeyword className
	;

extendedClassHeader
	: simpleClassHeader
	| simpleClassHeader extendsKeyword baseName
	;

classHeader
	: extendedClassHeader
	| modifiers extendedClassHeader
	;

class
	: classHeader classBody
	;

nonameClass
	: classKeyword classBody
	;

classBodyLCBrace
	: LCBrace
	;

classBodyLeft
	: classBodyLCBrace
	| classBodyLCBrace classMembers
	;

classBody
	: classBodyLeft RCBrace
	;

variableDeclaratorInit1
	: variableDeclaratorInit
	| modifiers variableDeclaratorInit
	;

qualifiedNameInit1
	: qualifiedNameInit
	| modifiers qualifiedNameInit
	;

method1
	: method
	| modifiers method
	;

records1
	: records
	| modifiers records
	;

classMember
	: classMember1
	;

classMember1
	: variableDeclaratorInit1 Semicolon
	| qualifiedNameInit1 Semicolon
	| method1
	| records1
	;

classMembers
	: classMember
	| classMembers classMember
	;

recordsKeyword
	: Records
	;

records
	: recordsKeyword recordsBody
	;

recordsLCBrace
	: LCBrace
	;

recordsBodyLeft
	: recordsLCBrace
	| recordsLCBrace recordsList
	;

recordsBody
	: recordsBodyLeft RCBrace
	;

recordName
	: Identifier
	;

simpleRecord
	: recordName Assign Constant
	;

record1
	: simpleRecord
	| modifiers simpleRecord
	;

record
	: record1 Semicolon
	;

recordsList
	: record
	| recordsList record
	;

simpleType
	: qualifiedName
	;

arrayType
	: qualifiedName indices
	;

type
	: simpleType
	| arrayType
	;

variableDeclarator
	: variableDeclarator1
	;

variableDeclarator1
	: type Identifier
	| Final type Identifier
	;

variableDeclaratorInit
	: variableDeclarator
	| variableDeclarator Assign initializer
	;

qualifiedNameInit
	: qualifiedName
	| qualifiedName Assign initializer
	| qualifiedName AddAssign initializer
	;

methodHeader
	: type Identifier parameters
	| Operator parameters
	| Operator Identifier parameters
	| type Operator Not parameters
	| type Operator Mul parameters
	| type Operator Div parameters
	| type Operator Mod parameters
	| type Operator Plus parameters
	| type Operator Minus parameters

	| type Operator Equ parameters
	| type Operator NotEqu parameters
	| type Operator Less parameters
	| type Operator More parameters
	| type Operator LessEqu parameters
	| type Operator MoreEqu parameters

	| type Operator BitwiseNot parameters
	| type Operator BitwiseAnd parameters
	| type Operator BitwiseOr parameters
	| type Operator BitwiseXor parameters

	| type Operator And parameters
	| type Operator Or parameters
	| type Operator Assign parameters
	;

method
	: methodHeader compound
	| methodHeader Semicolon
	;

parameter
	: variableDeclarator
	;

parametersList
	: parameter
	| parametersList Comma parameter
	;

parametersLeft
	: LBrace
	;

parameters
	: parametersLeft RBrace
	| parametersLeft parametersList RBrace
	;

initializer
	: nonameClass
	| expression
	| arrayInitializer
	;

arrayInitializerLeft
	: LCBrace
	;

arrayInitializer
	: arrayInitializerLeft RCBrace
	| arrayInitializerLeft arrayInitializers RCBrace
	| arrayInitializerLeft arrayInitializers Comma RCBrace
	;

arrayInitializers
	: arrayInitializersElement
	| arrayInitializers Comma arrayInitializersElement
	;

arrayInitializersElement
	: mapElement
	| expression
	| arrayInitializer
	;

mapElement
	: LBrace expression Comma expression RBrace
	| LBrace expression Comma arrayInitializer RBrace
	;

compoundLeft
	: LCBrace
	;

compound
	: compoundLeft RCBrace
	| compoundLeft statements RCBrace
	;

statements
	: statement
	| statements statement
	;

declaratorStatement
	: variableDeclaratorInit
	;

statement
	: tryCatchFinally
	| throw
	| assignment Semicolon
	| declaratorStatement Semicolon

	| compound
	| selection
	| iteration
	| jump


	;

throw
	: Throw expression Semicolon
	;

try
	: Try compound
	;

catch
	: Catch LBrace variableDeclarator RBrace compound
	;

finally
	: Finally compound
	;

tryCatch
	: try catch
	| tryCatch catch
	;

tryCatchFinally
	: tryCatch
	| try finally
	| tryCatch finally
	;

selection
	: If bracedExpression statement
	| If bracedExpression statement Else statement
	;

whileLoop
	: While bracedExpression statement
	;

doWhileLoop
	: Do statement While bracedExpression Semicolon
	;

forInit
	: variableDeclaratorInit
	| assignment
	;

forEachInit
	: variableDeclarator
	;

forStatement
	: For LBrace Semicolon expression Semicolon assignment RBrace statement
	| For LBrace forInit Semicolon expression Semicolon assignment RBrace statement
	| For LBrace forEachInit Colon expression RBrace statement
	;

iteration
	: whileLoop
	| doWhileLoop
	| forStatement
	;

jump
	: Return Semicolon
	| Return expression Semicolon
	| Return arrayInitializer Semicolon
	| Break Semicolon
	| Continue Semicolon
	;

assignment
	: expression
	| postfix Assign expression
	| postfix Assign arrayInitializer
	| postfix AddAssign expression
	| postfix SubAssign expression
	| postfix MulAssign expression
	| postfix DivAssign expression
	| postfix ModAssign expression
	| postfix BitwiseAndAssign expression
	| postfix BitwiseOrAssign expression
	| postfix BitwiseXorAssign expression
	;

expression
	: ternaryExpression
	| ternaryExpression InstanceOf simpleType
	;

ternaryExpression
	: logicalOr
	| logicalOr Question expression Colon ternaryExpression
	| logicalOr Elvis expression
	| logicalOr Elvis arrayInitializer
	;

logicalOr
	: logicalAnd
	| logicalOr Or logicalAnd
	;

logicalAnd
	: bitwiseOr
	| logicalAnd And bitwiseOr
	;

bitwiseOr
	: bitwiseXor
	| bitwiseOr BitwiseOr bitwiseXor
	;

bitwiseXor
	: bitwiseAnd
	| bitwiseXor BitwiseXor bitwiseAnd
	;

bitwiseAnd
	: equality
	| bitwiseAnd BitwiseAnd equality
	;

equality
	: relational
	| relational Equ relational
	| relational NotEqu relational
	;

relational
	: additive
	| Null
	| additive Less additive
	| additive More additive
	| additive LessEqu additive
	| additive MoreEqu additive
	;

additive
	: multiplicative
	| additive Plus multiplicative
	| additive Minus multiplicative
	;

multiplicative
	: unary
	| multiplicative Mul unary
	| multiplicative Div unary
	| multiplicative Mod unary
	;

unary
	: postfix
	| Plus unary
	| Minus unary
	| Not unary
	| BitwiseNot unary
	;

typeCast
	: bracedExpression postfix
	| arrayType arrayInitializer
	;

new
	: New Identifier
	;

container
	: Container
	| container Dot Container
	;

bracedExpression
	: LBrace expression RBrace
	| new
	;

prefix
	: This
	| Super
	| Constant
	| bracedExpression
	| simpleType
	| arrayType
	| methodCall
	| typeCast
	;

indexExpression
	: LBracket RBracket
	| LBracket expression RBracket
	;

indices
	: indexExpression
	| indices indexExpression
	;

postfix
	: prefix
	| container
	| container Dot qualifiedName
	| container Dot methodCall
	| postfix indices
	| postfix Dot qualifiedName
	| postfix Dot methodCall
	;

methodCall
	: qualifiedName expressions
	;

expressionsLeft
	: LBrace
	;

expressions
	: expressionsLeft RBrace
	| expressionsLeft expressionsList RBrace
	;

expressionsList
	: expression
	| arrayInitializer
	| expressionsList Comma expression
	| expressionsList Comma arrayInitializer
	;
```

Продукции вместе с семантическими действиями могут отвергать или трактовать вход иначе, чем чистая КС-грамматика. В частности, `indices` используется и для типа, и для выражения; применение `final`, атрибутов, отсутствия тела метода и литералов `records` дополнительно проверяется компилятором. Пустой файл или несколько деклараций грамматически представлены в `program`, но это не означает поддержку произвольного количества независимых единиц компиляции в файле.
