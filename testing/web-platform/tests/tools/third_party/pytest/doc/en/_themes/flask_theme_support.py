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
(
    
Keyword
    
Name
    
Comment
    
String
    
Error
    
Number
    
Operator
    
Generic
    
Whitespace
    
Punctuation
    
Other
    
Literal
)
class
FlaskyStyle
(
Style
)
:
    
background_color
=
"
#
f8f8f8
"
    
default_style
=
"
"
    
styles
=
{
        
Whitespace
:
"
underline
#
f8f8f8
"
        
Error
:
"
#
a40000
border
:
#
ef2929
"
        
Other
:
"
#
000000
"
        
Comment
:
"
italic
#
8f5902
"
        
Comment
.
Preproc
:
"
noitalic
"
        
Keyword
:
"
bold
#
004461
"
        
Keyword
.
Constant
:
"
bold
#
004461
"
        
Keyword
.
Declaration
:
"
bold
#
004461
"
        
Keyword
.
Namespace
:
"
bold
#
004461
"
        
Keyword
.
Pseudo
:
"
bold
#
004461
"
        
Keyword
.
Reserved
:
"
bold
#
004461
"
        
Keyword
.
Type
:
"
bold
#
004461
"
        
Operator
:
"
#
582800
"
        
Operator
.
Word
:
"
bold
#
004461
"
        
Punctuation
:
"
bold
#
000000
"
        
Name
:
"
#
000000
"
        
Name
.
Attribute
:
"
#
c4a000
"
        
Name
.
Builtin
:
"
#
004461
"
        
Name
.
Builtin
.
Pseudo
:
"
#
3465a4
"
        
Name
.
Class
:
"
#
000000
"
        
Name
.
Constant
:
"
#
000000
"
        
Name
.
Decorator
:
"
#
888
"
        
Name
.
Entity
:
"
#
ce5c00
"
        
Name
.
Exception
:
"
bold
#
cc0000
"
        
Name
.
Function
:
"
#
000000
"
        
Name
.
Property
:
"
#
000000
"
        
Name
.
Label
:
"
#
f57900
"
        
Name
.
Namespace
:
"
#
000000
"
        
Name
.
Other
:
"
#
000000
"
        
Name
.
Tag
:
"
bold
#
004461
"
        
Name
.
Variable
:
"
#
000000
"
        
Name
.
Variable
.
Class
:
"
#
000000
"
        
Name
.
Variable
.
Global
:
"
#
000000
"
        
Name
.
Variable
.
Instance
:
"
#
000000
"
        
Number
:
"
#
990000
"
        
Literal
:
"
#
000000
"
        
Literal
.
Date
:
"
#
000000
"
        
String
:
"
#
4e9a06
"
        
String
.
Backtick
:
"
#
4e9a06
"
        
String
.
Char
:
"
#
4e9a06
"
        
String
.
Doc
:
"
italic
#
8f5902
"
        
String
.
Double
:
"
#
4e9a06
"
        
String
.
Escape
:
"
#
4e9a06
"
        
String
.
Heredoc
:
"
#
4e9a06
"
        
String
.
Interpol
:
"
#
4e9a06
"
        
String
.
Other
:
"
#
4e9a06
"
        
String
.
Regex
:
"
#
4e9a06
"
        
String
.
Single
:
"
#
4e9a06
"
        
String
.
Symbol
:
"
#
4e9a06
"
        
Generic
:
"
#
000000
"
        
Generic
.
Deleted
:
"
#
a40000
"
        
Generic
.
Emph
:
"
italic
#
000000
"
        
Generic
.
Error
:
"
#
ef2929
"
        
Generic
.
Heading
:
"
bold
#
000080
"
        
Generic
.
Inserted
:
"
#
00A000
"
        
Generic
.
Output
:
"
#
888
"
        
Generic
.
Prompt
:
"
#
745334
"
        
Generic
.
Strong
:
"
bold
#
000000
"
        
Generic
.
Subheading
:
"
bold
#
800080
"
        
Generic
.
Traceback
:
"
bold
#
a40000
"
    
}
