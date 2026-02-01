"
"
"
    
pygments
.
lexers
.
cddl
    
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
the
Concise
data
definition
language
(
CDDL
)
a
notational
    
convention
to
express
CBOR
and
JSON
data
structures
.
    
More
information
:
    
https
:
/
/
datatracker
.
ietf
.
org
/
doc
/
rfc8610
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
lexer
import
RegexLexer
bygroups
include
words
from
pygments
.
token
import
Comment
Error
Keyword
Name
Number
Operator
\
    
Punctuation
String
Whitespace
__all__
=
[
'
CddlLexer
'
]
class
CddlLexer
(
RegexLexer
)
:
    
"
"
"
    
Lexer
for
CDDL
definitions
.
    
"
"
"
    
name
=
"
CDDL
"
    
url
=
'
https
:
/
/
datatracker
.
ietf
.
org
/
doc
/
rfc8610
/
'
    
aliases
=
[
"
cddl
"
]
    
filenames
=
[
"
*
.
cddl
"
]
    
mimetypes
=
[
"
text
/
x
-
cddl
"
]
    
version_added
=
'
2
.
8
'
    
_prelude_types
=
[
        
"
any
"
        
"
b64legacy
"
        
"
b64url
"
        
"
bigfloat
"
        
"
bigint
"
        
"
bignint
"
        
"
biguint
"
        
"
bool
"
        
"
bstr
"
        
"
bytes
"
        
"
cbor
-
any
"
        
"
decfrac
"
        
"
eb16
"
        
"
eb64legacy
"
        
"
eb64url
"
        
"
encoded
-
cbor
"
        
"
false
"
        
"
float
"
        
"
float16
"
        
"
float16
-
32
"
        
"
float32
"
        
"
float32
-
64
"
        
"
float64
"
        
"
int
"
        
"
integer
"
        
"
mime
-
message
"
        
"
nil
"
        
"
nint
"
        
"
null
"
        
"
number
"
        
"
regexp
"
        
"
tdate
"
        
"
text
"
        
"
time
"
        
"
true
"
        
"
tstr
"
        
"
uint
"
        
"
undefined
"
        
"
unsigned
"
        
"
uri
"
    
]
    
_controls
=
[
        
"
.
and
"
        
"
.
bits
"
        
"
.
cbor
"
        
"
.
cborseq
"
        
"
.
default
"
        
"
.
eq
"
        
"
.
ge
"
        
"
.
gt
"
        
"
.
le
"
        
"
.
lt
"
        
"
.
ne
"
        
"
.
regexp
"
        
"
.
size
"
        
"
.
within
"
    
]
    
_re_id
=
(
        
r
"
[
A
-
Z_a
-
z
]
"
        
r
"
(
?
:
[
\
-
\
.
]
+
(
?
=
[
0
-
9A
-
Z_a
-
z
]
)
|
[
0
-
9A
-
Z_a
-
z
]
)
*
"
    
)
    
_re_uint
=
r
"
(
?
:
0b
[
01
]
+
|
0x
[
0
-
9a
-
fA
-
F
]
+
|
[
1
-
9
]
\
d
*
|
0
(
?
!
\
d
)
)
"
    
_re_int
=
r
"
-
?
"
+
_re_uint
    
tokens
=
{
        
"
commentsandwhitespace
"
:
[
(
r
"
\
s
+
"
Whitespace
)
(
r
"
;
.
+
"
Comment
.
Single
)
]
        
"
root
"
:
[
            
include
(
"
commentsandwhitespace
"
)
            
(
rf
"
#
(
\
d
\
.
{
_re_uint
}
)
?
"
Keyword
.
Type
)
            
(
                
rf
"
(
{
_re_uint
}
)
?
(
\
*
)
(
{
_re_uint
}
)
?
"
                
bygroups
(
Number
Operator
Number
)
            
)
            
(
r
"
\
?
|
\
+
"
Operator
)
            
(
r
"
\
^
"
Operator
)
            
(
r
"
(
\
.
\
.
\
.
|
\
.
\
.
)
"
Operator
)
            
(
words
(
_controls
suffix
=
r
"
\
b
"
)
Operator
.
Word
)
            
(
rf
"
&
(
?
=
\
s
*
(
{
_re_id
}
|
\
(
)
)
"
Operator
)
            
(
rf
"
~
(
?
=
\
s
*
{
_re_id
}
)
"
Operator
)
            
(
r
"
/
/
|
/
(
?
!
/
)
"
Operator
)
            
(
r
"
=
>
|
/
=
=
|
/
=
|
=
"
Operator
)
            
(
r
"
[
\
[
\
]
{
}
\
(
\
)
<
>
:
]
"
Punctuation
)
            
(
r
"
(
b64
)
(
'
)
"
bygroups
(
String
.
Affix
String
.
Single
)
"
bstrb64url
"
)
            
(
r
"
(
h
)
(
'
)
"
bygroups
(
String
.
Affix
String
.
Single
)
"
bstrh
"
)
            
(
r
"
'
"
String
.
Single
"
bstr
"
)
            
(
rf
"
(
{
_re_id
}
)
(
\
s
*
)
(
:
)
"
             
bygroups
(
String
Whitespace
Punctuation
)
)
            
(
words
(
_prelude_types
prefix
=
r
"
(
?
!
[
\
-
_
]
)
\
b
"
suffix
=
r
"
\
b
(
?
!
[
\
-
_
]
)
"
)
             
Name
.
Builtin
)
            
(
_re_id
Name
.
Class
)
            
(
r
"
0b
[
01
]
+
"
Number
.
Bin
)
            
(
r
"
0o
[
0
-
7
]
+
"
Number
.
Oct
)
            
(
r
"
0x
[
0
-
9a
-
fA
-
F
]
+
(
\
.
[
0
-
9a
-
fA
-
F
]
+
)
?
p
[
+
-
]
?
\
d
+
"
Number
.
Hex
)
            
(
r
"
0x
[
0
-
9a
-
fA
-
F
]
+
"
Number
.
Hex
)
            
(
rf
"
{
_re_int
}
(
?
=
(
\
.
\
d
|
e
[
+
-
]
?
\
d
)
)
(
?
:
\
.
\
d
+
)
?
(
?
:
e
[
+
-
]
?
\
d
+
)
?
"
             
Number
.
Float
)
            
(
_re_int
Number
.
Integer
)
            
(
r
'
"
(
\
\
\
\
|
\
\
"
|
[
^
"
]
)
*
"
'
String
.
Double
)
        
]
        
"
bstrb64url
"
:
[
            
(
r
"
'
"
String
.
Single
"
#
pop
"
)
            
include
(
"
commentsandwhitespace
"
)
            
(
r
"
\
\
.
"
String
.
Escape
)
            
(
r
"
[
0
-
9a
-
zA
-
Z
\
-
_
=
]
+
"
String
.
Single
)
            
(
r
"
.
"
Error
)
        
]
        
"
bstrh
"
:
[
            
(
r
"
'
"
String
.
Single
"
#
pop
"
)
            
include
(
"
commentsandwhitespace
"
)
            
(
r
"
\
\
.
"
String
.
Escape
)
            
(
r
"
[
0
-
9a
-
fA
-
F
]
+
"
String
.
Single
)
            
(
r
"
.
"
Error
)
        
]
        
"
bstr
"
:
[
            
(
r
"
'
"
String
.
Single
"
#
pop
"
)
            
(
r
"
\
\
.
"
String
.
Escape
)
            
(
r
"
[
^
'
\
\
]
+
"
String
.
Single
)
        
]
    
}
