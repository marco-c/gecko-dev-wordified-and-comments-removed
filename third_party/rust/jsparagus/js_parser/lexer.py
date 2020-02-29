"
"
"
Vague
approximation
of
an
ECMAScript
lexer
.
A
parser
has
two
levels
:
the
*
lexer
*
scans
bytes
to
produce
tokens
.
The
*
parser
*
consumes
tokens
and
produces
ASTs
.
In
a
traditional
design
the
parser
drives
the
process
.
It
*
pulls
*
one
token
at
a
time
from
the
lexer
.
However
for
a
parser
that
can
accept
arbitrary
slabs
of
data
scan
them
then
keep
going
it
makes
more
sense
for
the
user
to
feed
those
slabs
to
the
lexer
which
then
*
pushes
*
tokens
to
the
parser
.
So
that
'
s
what
we
do
.
Usage
:
    
from
js_parser
.
lexer
import
JSLexer
    
from
js_parser
.
parser
import
JSParser
    
lexer
=
JSLexer
(
JSParser
(
)
)
    
lexer
.
write
(
some_source_text
)
    
lexer
.
write
(
some_more_source_text
)
    
ast
=
lexer
.
close
(
)
"
"
"
import
re
import
jsparagus
.
lexer
def
_get_punctuators
(
)
:
    
punctuators
=
'
'
'
        
{
(
)
[
]
.
.
.
.
;
<
>
<
=
>
=
=
=
!
=
=
=
=
!
=
=
+
-
*
%
*
*
+
+
-
-
        
<
<
>
>
>
>
>
&
|
^
!
~
&
&
|
|
?
:
=
+
=
-
=
*
=
%
=
        
*
*
=
>
<
<
=
>
>
=
>
>
>
=
&
=
|
=
^
=
=
>
    
'
'
'
.
split
(
)
    
return
'
|
'
.
join
(
        
re
.
escape
(
token
)
        
for
token
in
sorted
(
punctuators
key
=
len
reverse
=
True
)
)
TOKEN_RE
=
re
.
compile
(
r
'
'
'
(
?
x
)
  
(
?
:
      
#
WhiteSpace
      
[
\
\
t
\
v
\
r
\
n
\
u00a0
\
u2028
\
u2029
\
ufeff
]
      
#
SingleLineComment
    
|
/
/
[
^
\
r
\
n
\
u2028
\
u2029
]
*
(
?
=
[
\
r
\
n
\
u2028
\
u2029
]
|
\
Z
)
      
#
MultiLineComment
    
|
/
\
*
(
?
:
[
^
*
]
|
\
*
+
[
^
/
]
)
*
\
*
+
/
  
)
*
  
(
      
#
Incomplete
MultiLineComment
      
/
\
*
(
?
:
[
^
*
]
|
\
*
+
[
^
/
]
)
*
\
*
*
    
|
#
Incomplete
SingleLineComment
      
/
/
[
^
\
r
\
n
\
u2028
\
u2029
]
*
    
|
#
IdentifierName
      
(
?
:
[
_A
-
Za
-
z
]
|
\
\
u
[
0
-
9A
-
Fa
-
f
]
{
4
}
|
\
\
u
\
{
[
0
-
9A
-
Fa
-
f
]
+
\
}
)
      
(
?
:
[
_0
-
9A
-
Za
-
z
]
|
\
\
u
[
0
-
9A
-
Fa
-
f
]
{
4
}
|
\
\
u
\
{
[
0
-
9A
-
Fa
-
f
]
+
\
}
)
*
    
|
#
NumericLiteral
      
[
0
-
9
]
[
0
-
9A
-
Za
-
z
]
*
(
?
:
\
.
[
0
-
9A
-
Za
-
z
]
*
)
?
    
|
\
.
[
0
-
9
]
[
0
-
9A
-
Za
-
z
]
*
    
|
#
Punctuator
      
<
INSERT_PUNCTUATORS
>
    
|
#
The
slash
special
case
      
/
    
|
#
The
curly
brace
special
case
      
}
    
|
#
StringLiteral
      
'
        
#
SingleStringCharacters
        
(
?
:
            
#
SourceCharacter
but
not
one
of
'
or
\
\
or
LineTerminator
            
#
but
also
allow
LINE
SEPARATOR
or
PARAGRAPH
SEPARATOR
            
[
^
'
\
\
\
r
\
n
]
          
|
\
\
[
^
0
-
9xu
\
r
\
n
\
u2028
\
u2029
]
#
CharacterEscapeSequence
          
|
\
\
x
[
0
-
9A
-
Fa
-
f
]
{
2
}
#
HexEscapeSequence
          
|
\
\
u
[
0
-
9A
-
Fa
-
f
]
{
4
}
#
UnicodeEscapeSequence
          
|
\
\
u
\
{
[
0
-
9A
-
Fa
-
f
]
+
\
}
          
|
\
\
\
r
\
n
?
#
LineContinuation
          
|
\
\
[
\
n
\
u2028
\
u2029
]
        
)
*
      
'
    
|
"
        
#
DoubleStringCharacters
        
(
?
:
            
#
SourceCharacter
but
not
one
of
"
or
\
\
or
LineTerminator
            
#
but
also
allow
LINE
SEPARATOR
or
PARAGRAPH
SEPARATOR
            
[
^
"
\
\
\
r
\
n
]
          
|
\
\
[
^
0
-
9xu
\
r
\
n
\
u2028
\
u2029
]
#
CharacterEscapeSequence
          
|
\
\
x
[
0
-
9A
-
Fa
-
f
]
{
2
}
#
HexEscapeSequence
          
|
\
\
u
[
0
-
9A
-
Fa
-
f
]
{
4
}
#
UnicodeEscapeSequence
          
|
\
\
u
\
{
[
0
-
9A
-
Fa
-
f
]
+
\
}
          
|
\
\
\
r
\
n
?
#
LineContinuation
          
|
\
\
[
\
n
\
u2028
\
u2029
]
        
)
*
      
"
    
|
#
Template
      
(
?
:
[
^
\
\
]
|
\
\
.
)
*
(
?
:
\
{
|
)
    
|
#
illegal
character
or
end
of
input
(
this
branch
matches
no
characters
)
  
)
'
'
'
.
replace
(
"
<
INSERT_PUNCTUATORS
>
"
_get_punctuators
(
)
)
)
DIV_RE
=
re
.
compile
(
r
'
(
/
=
?
)
'
)
REGEXP_RE
=
re
.
compile
(
r
'
'
'
(
?
x
)
(
    
/
    
(
?
:
        
#
RegularExpressionFirstChar
-
implemented
using
        
#
RegularExpressionChars
on
the
theory
that
we
have
already
        
#
ruled
out
the
possibility
of
a
comment
.
        
#
RegularExpressionChars
        
(
?
:
            
#
RegularExpressionNonTerminator
but
not
one
of
\
\
or
/
or
[
            
[
^
/
\
\
\
[
\
r
\
n
\
u2028
\
u2029
]
          
|
#
RegularExpressionBackslashSequence
            
\
\
[
^
\
r
\
n
\
u2028
\
u2029
]
          
|
#
RegularExpressionClass
            
\
[
                
#
RegularExpressionClassChars
                
(
?
:
                    
#
RegularExpressionNonTerminator
but
not
one
of
]
or
\
\
                    
[
^
]
\
\
\
r
\
n
\
u2028
\
u2029
]
                  
|
#
RegularExpressionBackslashSequence
                    
\
\
[
^
\
r
\
n
\
u2028
\
u2029
]
                
)
*
            
\
]
        
)
+
    
)
    
/
    
(
?
:
\
w
*
)
)
'
'
'
)
ECMASCRIPT_FULL_KEYWORDS
=
[
    
'
await
'
    
'
break
'
    
'
case
'
    
'
catch
'
    
'
class
'
    
'
const
'
    
'
continue
'
    
'
debugger
'
    
'
default
'
    
'
delete
'
    
'
do
'
    
'
else
'
    
'
enum
'
    
'
export
'
    
'
extends
'
    
'
finally
'
    
'
for
'
    
'
function
'
    
'
if
'
    
'
import
'
    
'
in
'
    
'
instanceof
'
    
'
new
'
    
'
null
'
    
'
return
'
    
'
super
'
    
'
switch
'
    
'
this
'
    
'
throw
'
    
'
true
'
    
'
false
'
    
'
try
'
    
'
typeof
'
    
'
var
'
    
'
void
'
    
'
while
'
    
'
with
'
    
'
yield
'
]
ECMASCRIPT_CONDITIONAL_KEYWORDS
=
[
    
'
let
'
    
'
static
'
    
'
implements
'
    
'
interface
'
    
'
package
'
    
'
private
'
    
'
protected
'
    
'
public
'
    
'
as
'
    
'
async
'
    
'
from
'
    
'
get
'
    
'
of
'
    
'
set
'
    
'
target
'
]
ALL_KEYWORDS
=
set
(
ECMASCRIPT_FULL_KEYWORDS
+
ECMASCRIPT_CONDITIONAL_KEYWORDS
)
class
JSLexer
(
jsparagus
.
lexer
.
FlatStringLexer
)
:
    
"
"
"
Vague
approximation
of
an
ECMAScript
lexer
.
"
"
"
    
def
__init__
(
self
parser
filename
=
None
)
:
        
super
(
)
.
__init__
(
parser
filename
)
    
def
_match
(
self
closing
)
:
        
match
=
TOKEN_RE
.
match
(
self
.
src
self
.
point
)
        
assert
match
is
not
None
        
if
match
.
end
(
)
=
=
len
(
self
.
src
)
and
not
closing
:
            
return
None
        
token
=
match
.
group
(
1
)
        
if
token
=
=
'
'
:
            
if
match
.
end
(
)
=
=
len
(
self
.
src
)
:
                
assert
closing
                
self
.
point
=
match
.
end
(
)
                
return
None
            
else
:
                
c
=
self
.
src
[
match
.
end
(
)
]
                
self
.
throw
(
"
unexpected
character
:
{
!
r
}
"
.
format
(
c
)
)
        
c
=
token
[
0
]
        
t
=
None
        
if
c
.
isdigit
(
)
or
c
=
=
'
.
'
and
token
!
=
'
.
'
:
            
t
=
'
NumericLiteral
'
        
elif
c
.
isalpha
(
)
or
c
in
'
_
'
:
            
if
token
in
ALL_KEYWORDS
:
                
if
token
=
=
'
null
'
:
                    
t
=
'
NullLiteral
'
                
elif
token
in
(
'
true
'
'
false
'
)
:
                    
t
=
'
BooleanLiteral
'
                
else
:
                    
t
=
token
            
else
:
                
t
=
'
Name
'
        
elif
c
=
=
'
/
'
:
            
if
token
.
startswith
(
(
'
/
*
'
'
/
/
'
)
)
:
                
assert
match
.
end
(
)
=
=
len
(
self
.
src
)
                
assert
closing
                
self
.
point
=
len
(
self
.
src
)
                
self
.
throw
(
"
incomplete
comment
at
end
of
source
"
)
            
point
=
match
.
start
(
1
)
            
if
self
.
parser
.
can_accept_terminal
(
'
RegularExpressionLiteral
'
)
:
                
match
=
REGEXP_RE
.
match
(
self
.
src
point
)
                
if
match
is
None
:
                    
if
closing
:
                        
self
.
throw
(
"
unterminated
regexp
literal
"
)
                    
else
:
                        
return
None
                
token
=
'
RegularExpressionLiteral
'
            
else
:
                
match
=
DIV_RE
.
match
(
self
.
src
point
)
                
token
=
match
.
group
(
1
)
            
if
not
closing
and
match
.
end
(
)
=
=
len
(
self
.
src
)
:
                
return
None
            
t
=
token
        
elif
c
=
=
'
'
:
            
if
token
.
endswith
(
'
'
)
:
                
t
=
'
NoSubstitutionTemplate
'
            
else
:
                
t
=
'
TemplateHead
'
        
elif
c
=
=
'
"
'
or
c
=
=
"
'
"
:
            
t
=
'
StringLiteral
'
        
elif
c
=
=
'
}
'
:
            
t
=
token
        
elif
c
in
'
{
(
)
[
]
;
~
?
:
.
<
>
=
!
+
-
*
%
&
|
^
'
:
            
t
=
token
        
else
:
            
assert
False
        
self
.
_current_match
=
match
        
self
.
previous_token_end
=
self
.
point
        
self
.
current_token_start
=
match
.
start
(
1
)
        
self
.
point
=
match
.
end
(
)
        
return
t
    
def
take
(
self
)
:
        
return
self
.
_current_match
.
group
(
1
)
    
def
saw_line_terminator
(
self
)
:
        
"
"
"
True
if
there
'
s
a
LineTerminator
before
the
current
token
.
"
"
"
        
i
=
self
.
previous_token_end
        
j
=
self
.
current_token_start
        
ws_between
=
self
.
src
[
i
:
j
]
        
return
any
(
c
in
ws_between
for
c
in
'
\
r
\
n
\
u2028
\
u2029
'
)
    
def
can_close
(
self
)
:
        
match
=
TOKEN_RE
.
match
(
self
.
src
)
        
return
match
.
group
(
1
)
=
=
'
'
and
self
.
parser
.
can_close
(
)
