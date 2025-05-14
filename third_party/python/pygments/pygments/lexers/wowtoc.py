"
"
"
    
pygments
.
lexers
.
wowtoc
    
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
    
Lexer
for
World
of
Warcraft
TOC
files
    
TOC
files
describe
game
addons
.
    
:
copyright
:
Copyright
2006
-
2025
by
the
Pygments
team
see
AUTHORS
.
    
:
license
:
BSD
see
LICENSE
for
details
.
"
"
"
import
re
from
pygments
.
lexer
import
RegexLexer
bygroups
from
pygments
.
token
import
Comment
Name
Text
Punctuation
String
Keyword
__all__
=
[
"
WoWTocLexer
"
]
def
_create_tag_line_pattern
(
inner_pattern
ignore_case
=
False
)
:
    
return
(
(
r
"
(
?
i
)
"
if
ignore_case
else
r
"
"
)
        
+
r
"
^
(
#
#
)
(
*
)
"
        
+
inner_pattern
        
+
r
"
(
*
)
(
:
)
(
*
)
(
.
*
?
)
(
*
)
"
)
def
_create_tag_line_token
(
inner_pattern
inner_token
ignore_case
=
False
)
:
    
return
(
        
_create_tag_line_pattern
(
inner_pattern
ignore_case
=
ignore_case
)
        
bygroups
(
            
Keyword
.
Declaration
            
Text
.
Whitespace
            
inner_token
            
Text
.
Whitespace
            
Punctuation
            
Text
.
Whitespace
            
String
            
Text
.
Whitespace
        
)
    
)
class
WoWTocLexer
(
RegexLexer
)
:
    
"
"
"
    
Lexer
for
World
of
Warcraft
TOC
files
.
    
"
"
"
    
name
=
"
World
of
Warcraft
TOC
"
    
aliases
=
[
"
wowtoc
"
]
    
filenames
=
[
"
*
.
toc
"
]
    
url
=
'
https
:
/
/
wowpedia
.
fandom
.
com
/
wiki
/
TOC_format
'
    
version_added
=
'
2
.
14
'
    
tokens
=
{
        
"
root
"
:
[
            
_create_tag_line_token
(
                
r
"
(
(
?
:
[
nN
]
[
oO
]
[
tT
]
[
eE
]
[
sS
]
|
[
tT
]
[
iI
]
[
tT
]
[
lL
]
[
eE
]
)
-
(
?
:
ptBR
|
zhCN
|
"
                
r
"
enCN
|
frFR
|
deDE
|
itIT
|
esMX
|
ptPT
|
koKR
|
ruRU
|
esES
|
zhTW
|
enTW
|
enGB
|
enUS
)
)
"
                
Name
.
Builtin
            
)
            
_create_tag_line_token
(
                
r
"
(
Interface
|
Title
|
Notes
|
RequiredDeps
|
Dep
[
^
:
]
*
|
OptionalDeps
|
"
                
r
"
LoadOnDemand
|
LoadWith
|
LoadManagers
|
SavedVariablesPerCharacter
|
"
                
r
"
SavedVariables
|
DefaultState
|
Secure
|
Author
|
Version
)
"
                
Name
.
Builtin
                
ignore_case
=
True
            
)
            
_create_tag_line_token
(
                
r
"
(
X
-
[
^
:
]
*
)
"
                
Name
.
Variable
                
ignore_case
=
True
            
)
            
_create_tag_line_token
(
                
r
"
(
[
^
:
]
*
)
"
                
Name
.
Other
            
)
            
(
r
"
^
#
.
*
"
Comment
)
            
(
r
"
^
.
+
"
Name
)
        
]
    
}
    
def
analyse_text
(
text
)
:
        
result
=
0
        
interface_pattern
=
_create_tag_line_pattern
(
r
"
(
Interface
)
"
ignore_case
=
True
)
        
match
=
re
.
search
(
interface_pattern
text
)
        
if
match
and
re
.
match
(
r
"
(
\
d
+
)
(
\
d
{
2
}
)
(
\
d
{
2
}
)
"
match
.
group
(
7
)
)
:
            
result
+
=
0
.
8
        
casefolded
=
text
.
casefold
(
)
        
if
"
.
lua
"
in
casefolded
:
            
result
+
=
0
.
1
        
if
"
.
xml
"
in
casefolded
:
            
result
+
=
0
.
05
        
return
result
