"
"
"
    
pygments
.
styles
.
arduino
    
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
    
Arduino
Syntax
highlighting
style
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
\
    
Number
Operator
Generic
Whitespace
__all__
=
[
'
ArduinoStyle
'
]
class
ArduinoStyle
(
Style
)
:
    
"
"
"
    
The
Arduino
language
style
.
This
style
is
designed
to
highlight
the
    
Arduino
source
code
so
expect
the
best
results
with
it
.
    
"
"
"
    
name
=
'
arduino
'
    
background_color
=
"
#
ffffff
"
    
styles
=
{
        
Whitespace
:
"
"
        
Error
:
"
#
a61717
"
        
Comment
:
"
#
95a5a6
"
        
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
#
728E00
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
"
#
728E00
"
        
Keyword
.
Constant
:
"
#
00979D
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
"
"
        
Keyword
.
Pseudo
:
"
#
00979D
"
        
Keyword
.
Reserved
:
"
#
00979D
"
        
Keyword
.
Type
:
"
#
00979D
"
        
Operator
:
"
#
728E00
"
        
Operator
.
Word
:
"
"
        
Name
:
"
#
434f54
"
        
Name
.
Attribute
:
"
"
        
Name
.
Builtin
:
"
#
728E00
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
"
"
        
Name
.
Constant
:
"
"
        
Name
.
Decorator
:
"
"
        
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
"
"
        
Name
.
Function
:
"
#
D35400
"
        
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
"
"
        
Name
.
Other
:
"
#
728E00
"
        
Name
.
Tag
:
"
"
        
Name
.
Variable
:
"
"
        
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
"
#
8A7B52
"
        
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
        
String
:
"
#
7F8C8D
"
        
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
"
"
        
String
.
Doc
:
"
"
        
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
"
"
        
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
"
"
        
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
"
"
        
Generic
.
Emph
:
"
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
"
        
Generic
.
Inserted
:
"
"
        
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
"
        
Generic
.
Strong
:
"
"
        
Generic
.
Subheading
:
"
"
        
Generic
.
Traceback
:
"
"
    
}
