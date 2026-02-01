"
"
"
    
pygments
.
styles
.
paraiso_light
    
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
~
~
~
~
~
~
~
    
Para
so
(
Light
)
by
Jan
T
.
Sott
    
Pygments
template
by
Jan
T
.
Sott
(
https
:
/
/
github
.
com
/
idleberg
)
    
Created
with
Base16
Builder
by
Chris
Kempson
    
(
https
:
/
/
github
.
com
/
chriskempson
/
base16
-
builder
)
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
from
pygments
.
style
import
Style
from
pygments
.
token
import
Keyword
Name
Comment
String
Error
Text
\
    
Number
Operator
Generic
Whitespace
Punctuation
Other
Literal
__all__
=
[
'
ParaisoLightStyle
'
]
BACKGROUND
=
"
#
e7e9db
"
CURRENT_LINE
=
"
#
b9b6b0
"
SELECTION
=
"
#
a39e9b
"
FOREGROUND
=
"
#
2f1e2e
"
COMMENT
=
"
#
8d8687
"
RED
=
"
#
ef6155
"
ORANGE
=
"
#
f99b15
"
YELLOW
=
"
#
fec418
"
GREEN
=
"
#
48b685
"
AQUA
=
"
#
5bc4bf
"
BLUE
=
"
#
06b6ef
"
PURPLE
=
"
#
815ba4
"
class
ParaisoLightStyle
(
Style
)
:
    
name
=
'
paraiso
-
light
'
    
background_color
=
BACKGROUND
    
highlight_color
=
SELECTION
    
styles
=
{
        
Text
:
FOREGROUND
        
Whitespace
:
"
"
        
Error
:
RED
        
Other
:
"
"
        
Comment
:
COMMENT
        
Comment
.
Multiline
:
"
"
        
Comment
.
Preproc
:
"
"
        
Comment
.
Single
:
"
"
        
Comment
.
Special
:
"
"
        
Keyword
:
PURPLE
        
Keyword
.
Constant
:
"
"
        
Keyword
.
Declaration
:
"
"
        
Keyword
.
Namespace
:
AQUA
        
Keyword
.
Pseudo
:
"
"
        
Keyword
.
Reserved
:
"
"
        
Keyword
.
Type
:
YELLOW
        
Operator
:
AQUA
        
Operator
.
Word
:
"
"
        
Punctuation
:
FOREGROUND
        
Name
:
FOREGROUND
        
Name
.
Attribute
:
BLUE
        
Name
.
Builtin
:
"
"
        
Name
.
Builtin
.
Pseudo
:
"
"
        
Name
.
Class
:
YELLOW
        
Name
.
Constant
:
RED
        
Name
.
Decorator
:
AQUA
        
Name
.
Entity
:
"
"
        
Name
.
Exception
:
RED
        
Name
.
Function
:
BLUE
        
Name
.
Property
:
"
"
        
Name
.
Label
:
"
"
        
Name
.
Namespace
:
YELLOW
        
Name
.
Other
:
BLUE
        
Name
.
Tag
:
AQUA
        
Name
.
Variable
:
RED
        
Name
.
Variable
.
Class
:
"
"
        
Name
.
Variable
.
Global
:
"
"
        
Name
.
Variable
.
Instance
:
"
"
        
Number
:
ORANGE
        
Number
.
Float
:
"
"
        
Number
.
Hex
:
"
"
        
Number
.
Integer
:
"
"
        
Number
.
Integer
.
Long
:
"
"
        
Number
.
Oct
:
"
"
        
Literal
:
ORANGE
        
Literal
.
Date
:
GREEN
        
String
:
GREEN
        
String
.
Backtick
:
"
"
        
String
.
Char
:
FOREGROUND
        
String
.
Doc
:
COMMENT
        
String
.
Double
:
"
"
        
String
.
Escape
:
ORANGE
        
String
.
Heredoc
:
"
"
        
String
.
Interpol
:
ORANGE
        
String
.
Other
:
"
"
        
String
.
Regex
:
"
"
        
String
.
Single
:
"
"
        
String
.
Symbol
:
"
"
        
Generic
:
"
"
        
Generic
.
Deleted
:
RED
        
Generic
.
Emph
:
"
italic
"
        
Generic
.
Error
:
"
"
        
Generic
.
Heading
:
"
bold
"
+
FOREGROUND
        
Generic
.
Inserted
:
GREEN
        
Generic
.
Output
:
"
"
        
Generic
.
Prompt
:
"
bold
"
+
COMMENT
        
Generic
.
Strong
:
"
bold
"
        
Generic
.
EmphStrong
:
"
bold
italic
"
        
Generic
.
Subheading
:
"
bold
"
+
AQUA
        
Generic
.
Traceback
:
"
"
    
}
