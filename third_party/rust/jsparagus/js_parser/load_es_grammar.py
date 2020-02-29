"
"
"
Functions
for
loading
the
ECMAScript
lexical
and
syntactic
grammars
.
"
"
"
from
jsparagus
.
ordered
import
OrderedSet
OrderedFrozenSet
from
jsparagus
import
gen
from
.
lexer
import
ECMASCRIPT_FULL_KEYWORDS
ECMASCRIPT_CONDITIONAL_KEYWORDS
from
.
parse_esgrammar
import
parse_esgrammar
ECMASCRIPT_LEXICAL_SYNTHETIC_TERMINALS
=
{
    
'
SourceCharacter
'
:
OrderedFrozenSet
(
[
]
)
}
ECMASCRIPT_LEXICAL_GOAL_NTS
=
[
    
'
WhiteSpace
'
    
'
InputElementDiv
'
    
'
InputElementRegExp
'
]
def
load_lexical_grammar
(
filename
)
:
    
"
"
"
Load
the
ECMAScript
lexical
grammar
.
"
"
"
    
with
open
(
filename
)
as
f
:
        
grammar_text
=
f
.
read
(
)
    
g
=
parse_esgrammar
(
        
grammar_text
        
filename
=
filename
        
goals
=
ECMASCRIPT_LEXICAL_GOAL_NTS
        
synthetic_terminals
=
ECMASCRIPT_LEXICAL_SYNTHETIC_TERMINALS
        
terminal_names
=
ECMASCRIPT_LEXICAL_SYNTHETIC_TERMINALS
.
keys
(
)
)
    
return
gen
.
expand_parameterized_nonterminals
(
g
)
ECMASCRIPT_SYNTACTIC_GOAL_NTS
=
[
    
'
Script
'
    
'
Module
'
]
ECMASCRIPT_SYNTHETIC_TERMINALS
=
{
    
'
IdentifierName
'
:
OrderedSet
(
[
        
'
Name
'
        
'
BooleanLiteral
'
        
'
NullLiteral
'
        
'
NameWithEscape
'
        
*
ECMASCRIPT_FULL_KEYWORDS
        
*
ECMASCRIPT_CONDITIONAL_KEYWORDS
    
]
)
-
OrderedSet
(
[
'
true
'
'
false
'
'
null
'
]
)
    
'
Identifier
'
:
OrderedSet
(
[
        
'
Name
'
        
'
NameWithEscape
'
        
*
ECMASCRIPT_CONDITIONAL_KEYWORDS
    
]
)
}
ECMASCRIPT_TOKEN_NAMES
=
[
    
'
BooleanLiteral
'
    
'
IdentifierName
'
    
'
PrivateIdentifier
'
    
'
NoSubstitutionTemplate
'
    
'
NullLiteral
'
    
'
NumericLiteral
'
    
'
BigIntLiteral
'
    
'
RegularExpressionLiteral
'
    
'
StringLiteral
'
    
'
TemplateHead
'
    
'
TemplateMiddle
'
    
'
TemplateTail
'
]
TERMINAL_NAMES_FOR_SYNTACTIC_GRAMMAR
=
ECMASCRIPT_TOKEN_NAMES
+
[
    
'
Identifier
'
    
'
Name
'
]
def
load_syntactic_grammar
(
filename
)
:
    
"
"
"
Load
the
ECMAScript
syntactic
grammar
.
"
"
"
    
with
open
(
filename
)
as
f
:
        
grammar_text
=
f
.
read
(
)
    
g
=
parse_esgrammar
(
        
grammar_text
        
filename
=
filename
        
goals
=
ECMASCRIPT_SYNTACTIC_GOAL_NTS
        
synthetic_terminals
=
ECMASCRIPT_SYNTHETIC_TERMINALS
        
terminal_names
=
TERMINAL_NAMES_FOR_SYNTACTIC_GRAMMAR
)
    
return
g
