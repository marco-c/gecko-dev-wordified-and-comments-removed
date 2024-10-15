from
__future__
import
annotations
from
collections
import
namedtuple
from
dataclasses
import
dataclass
from
typing
import
TYPE_CHECKING
Any
Literal
from
.
.
_compat
import
DATACLASS_KWARGS
from
.
.
common
.
utils
import
isMdAsciiPunct
isPunctChar
isWhiteSpace
from
.
.
ruler
import
StateBase
from
.
.
token
import
Token
from
.
.
utils
import
EnvType
if
TYPE_CHECKING
:
    
from
markdown_it
import
MarkdownIt
dataclass
(
*
*
DATACLASS_KWARGS
)
class
Delimiter
:
    
marker
:
int
    
length
:
int
    
token
:
int
    
end
:
int
    
open
:
bool
    
close
:
bool
    
level
:
bool
|
None
=
None
Scanned
=
namedtuple
(
"
Scanned
"
[
"
can_open
"
"
can_close
"
"
length
"
]
)
class
StateInline
(
StateBase
)
:
    
def
__init__
(
        
self
src
:
str
md
:
MarkdownIt
env
:
EnvType
outTokens
:
list
[
Token
]
    
)
-
>
None
:
        
self
.
src
=
src
        
self
.
env
=
env
        
self
.
md
=
md
        
self
.
tokens
=
outTokens
        
self
.
tokens_meta
:
list
[
dict
[
str
Any
]
|
None
]
=
[
None
]
*
len
(
outTokens
)
        
self
.
pos
=
0
        
self
.
posMax
=
len
(
self
.
src
)
        
self
.
level
=
0
        
self
.
pending
=
"
"
        
self
.
pendingLevel
=
0
        
self
.
cache
:
dict
[
int
int
]
=
{
}
        
self
.
delimiters
:
list
[
Delimiter
]
=
[
]
        
self
.
_prev_delimiters
:
list
[
list
[
Delimiter
]
]
=
[
]
        
self
.
backticks
:
dict
[
int
int
]
=
{
}
        
self
.
backticksScanned
=
False
        
self
.
linkLevel
=
0
    
def
__repr__
(
self
)
-
>
str
:
        
return
(
            
f
"
{
self
.
__class__
.
__name__
}
"
            
f
"
(
pos
=
[
{
self
.
pos
}
of
{
self
.
posMax
}
]
token
=
{
len
(
self
.
tokens
)
}
)
"
        
)
    
def
pushPending
(
self
)
-
>
Token
:
        
token
=
Token
(
"
text
"
"
"
0
)
        
token
.
content
=
self
.
pending
        
token
.
level
=
self
.
pendingLevel
        
self
.
tokens
.
append
(
token
)
        
self
.
pending
=
"
"
        
return
token
    
def
push
(
self
ttype
:
str
tag
:
str
nesting
:
Literal
[
-
1
0
1
]
)
-
>
Token
:
        
"
"
"
Push
new
token
to
"
stream
"
.
        
If
pending
text
exists
-
flush
it
as
text
token
        
"
"
"
        
if
self
.
pending
:
            
self
.
pushPending
(
)
        
token
=
Token
(
ttype
tag
nesting
)
        
token_meta
=
None
        
if
nesting
<
0
:
            
self
.
level
-
=
1
            
self
.
delimiters
=
self
.
_prev_delimiters
.
pop
(
)
        
token
.
level
=
self
.
level
        
if
nesting
>
0
:
            
self
.
level
+
=
1
            
self
.
_prev_delimiters
.
append
(
self
.
delimiters
)
            
self
.
delimiters
=
[
]
            
token_meta
=
{
"
delimiters
"
:
self
.
delimiters
}
        
self
.
pendingLevel
=
self
.
level
        
self
.
tokens
.
append
(
token
)
        
self
.
tokens_meta
.
append
(
token_meta
)
        
return
token
    
def
scanDelims
(
self
start
:
int
canSplitWord
:
bool
)
-
>
Scanned
:
        
"
"
"
        
Scan
a
sequence
of
emphasis
-
like
markers
and
determine
whether
        
it
can
start
an
emphasis
sequence
or
end
an
emphasis
sequence
.
         
-
start
-
position
to
scan
from
(
it
should
point
at
a
valid
marker
)
;
         
-
canSplitWord
-
determine
if
these
markers
can
be
found
inside
a
word
        
"
"
"
        
pos
=
start
        
maximum
=
self
.
posMax
        
marker
=
self
.
src
[
start
]
        
lastChar
=
self
.
src
[
start
-
1
]
if
start
>
0
else
"
"
        
while
pos
<
maximum
and
self
.
src
[
pos
]
=
=
marker
:
            
pos
+
=
1
        
count
=
pos
-
start
        
nextChar
=
self
.
src
[
pos
]
if
pos
<
maximum
else
"
"
        
isLastPunctChar
=
isMdAsciiPunct
(
ord
(
lastChar
)
)
or
isPunctChar
(
lastChar
)
        
isNextPunctChar
=
isMdAsciiPunct
(
ord
(
nextChar
)
)
or
isPunctChar
(
nextChar
)
        
isLastWhiteSpace
=
isWhiteSpace
(
ord
(
lastChar
)
)
        
isNextWhiteSpace
=
isWhiteSpace
(
ord
(
nextChar
)
)
        
left_flanking
=
not
(
            
isNextWhiteSpace
            
or
(
isNextPunctChar
and
not
(
isLastWhiteSpace
or
isLastPunctChar
)
)
        
)
        
right_flanking
=
not
(
            
isLastWhiteSpace
            
or
(
isLastPunctChar
and
not
(
isNextWhiteSpace
or
isNextPunctChar
)
)
        
)
        
if
not
canSplitWord
:
            
can_open
=
left_flanking
and
(
(
not
right_flanking
)
or
isLastPunctChar
)
            
can_close
=
right_flanking
and
(
(
not
left_flanking
)
or
isNextPunctChar
)
        
else
:
            
can_open
=
left_flanking
            
can_close
=
right_flanking
        
return
Scanned
(
can_open
can_close
count
)
