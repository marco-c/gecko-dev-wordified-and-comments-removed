"
"
"
    
pygments
.
styles
.
monokai
    
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
    
Mimic
the
Monokai
color
scheme
.
Based
on
tango
.
py
.
    
http
:
/
/
www
.
monokai
.
nl
/
blog
/
2006
/
07
/
15
/
textmate
-
color
-
theme
/
    
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
Token
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
MonokaiStyle
'
]
class
MonokaiStyle
(
Style
)
:
    
"
"
"
    
This
style
mimics
the
Monokai
color
scheme
.
    
"
"
"
    
name
=
'
monokai
'
    
background_color
=
"
#
272822
"
    
highlight_color
=
"
#
49483e
"
    
styles
=
{
        
Token
:
"
#
f8f8f2
"
        
Whitespace
:
"
"
        
Error
:
"
#
ed007e
bg
:
#
1e0010
"
        
Other
:
"
"
        
Comment
:
"
#
959077
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
66d9ef
"
        
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
"
#
ff4689
"
        
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
"
"
        
Operator
:
"
#
ff4689
"
        
Operator
.
Word
:
"
"
        
Punctuation
:
"
#
f8f8f2
"
        
Name
:
"
#
f8f8f2
"
        
Name
.
Attribute
:
"
#
a6e22e
"
        
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
"
#
a6e22e
"
        
Name
.
Constant
:
"
#
66d9ef
"
        
Name
.
Decorator
:
"
#
a6e22e
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
#
a6e22e
"
        
Name
.
Function
:
"
#
a6e22e
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
a6e22e
"
        
Name
.
Tag
:
"
#
ff4689
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
ae81ff
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
        
Literal
:
"
#
ae81ff
"
        
Literal
.
Date
:
"
#
e6db74
"
        
String
:
"
#
e6db74
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
#
ae81ff
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
#
ff4689
"
        
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
"
        
Generic
.
Inserted
:
"
#
a6e22e
"
        
Generic
.
Output
:
"
#
66d9ef
"
        
Generic
.
Prompt
:
"
bold
#
ff4689
"
        
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
#
959077
"
        
Generic
.
Traceback
:
"
"
    
}
