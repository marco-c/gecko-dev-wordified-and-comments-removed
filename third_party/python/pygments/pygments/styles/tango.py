"
"
"
    
pygments
.
styles
.
tango
    
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
    
The
Crunchy
default
Style
inspired
from
the
color
palette
from
    
the
Tango
Icon
Theme
Guidelines
.
    
http
:
/
/
tango
.
freedesktop
.
org
/
Tango_Icon_Theme_Guidelines
    
Butter
:
#
fce94f
#
edd400
#
c4a000
    
Orange
:
#
fcaf3e
#
f57900
#
ce5c00
    
Chocolate
:
#
e9b96e
#
c17d11
#
8f5902
    
Chameleon
:
#
8ae234
#
73d216
#
4e9a06
    
Sky
Blue
:
#
729fcf
#
3465a4
#
204a87
    
Plum
:
#
ad7fa8
#
75507b
#
5c35cc
    
Scarlet
Red
:
#
ef2929
#
cc0000
#
a40000
    
Aluminium
:
#
eeeeec
#
d3d7cf
#
babdb6
                
#
888a85
#
555753
#
2e3436
    
Not
all
of
the
above
colors
are
used
;
other
colors
added
:
        
very
light
grey
:
#
f8f8f8
(
for
background
)
    
This
style
can
be
used
as
a
template
as
it
includes
all
the
known
    
Token
types
unlike
most
(
if
not
all
)
of
the
styles
included
in
the
    
Pygments
distribution
.
    
However
since
Crunchy
is
intended
to
be
used
by
beginners
we
have
strived
    
to
create
a
style
that
gloss
over
subtle
distinctions
between
different
    
categories
.
    
Taking
Python
for
example
comments
(
Comment
.
*
)
and
docstrings
(
String
.
Doc
)
    
have
been
chosen
to
have
the
same
style
.
Similarly
keywords
(
Keyword
.
*
)
    
and
Operator
.
Word
(
and
or
in
)
have
been
assigned
the
same
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
Punctuation
Other
Literal
__all__
=
[
'
TangoStyle
'
]
class
TangoStyle
(
Style
)
:
    
"
"
"
    
The
Crunchy
default
Style
inspired
from
the
color
palette
from
    
the
Tango
Icon
Theme
Guidelines
.
    
"
"
"
    
name
=
'
tango
'
    
background_color
=
"
#
f8f8f8
"
    
styles
=
{
        
Whitespace
:
"
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
Multiline
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
italic
#
8f5902
"
        
Comment
.
Single
:
"
italic
#
8f5902
"
        
Comment
.
Special
:
"
italic
#
8f5902
"
        
Keyword
:
"
bold
#
204a87
"
        
Keyword
.
Constant
:
"
bold
#
204a87
"
        
Keyword
.
Declaration
:
"
bold
#
204a87
"
        
Keyword
.
Namespace
:
"
bold
#
204a87
"
        
Keyword
.
Pseudo
:
"
bold
#
204a87
"
        
Keyword
.
Reserved
:
"
bold
#
204a87
"
        
Keyword
.
Type
:
"
bold
#
204a87
"
        
Operator
:
"
bold
#
ce5c00
"
        
Operator
.
Word
:
"
bold
#
204a87
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
204a87
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
bold
#
5c35cc
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
204a87
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
bold
#
0000cf
"
        
Number
.
Float
:
"
bold
#
0000cf
"
        
Number
.
Hex
:
"
bold
#
0000cf
"
        
Number
.
Integer
:
"
bold
#
0000cf
"
        
Number
.
Integer
.
Long
:
"
bold
#
0000cf
"
        
Number
.
Oct
:
"
bold
#
0000cf
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
italic
#
000000
"
        
Generic
.
Prompt
:
"
#
8f5902
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
EmphStrong
:
"
bold
italic
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
