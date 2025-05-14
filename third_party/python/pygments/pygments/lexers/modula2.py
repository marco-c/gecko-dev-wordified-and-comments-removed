"
"
"
    
pygments
.
lexers
.
modula2
    
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
    
Multi
-
Dialect
Lexer
for
Modula
-
2
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
include
from
pygments
.
util
import
get_bool_opt
get_list_opt
from
pygments
.
token
import
Text
Comment
Operator
Keyword
Name
\
    
String
Number
Punctuation
Error
__all__
=
[
'
Modula2Lexer
'
]
class
Modula2Lexer
(
RegexLexer
)
:
    
"
"
"
    
For
Modula
-
2
source
code
.
    
The
Modula
-
2
lexer
supports
several
dialects
.
By
default
it
operates
in
    
fallback
mode
recognising
the
*
combined
*
literals
punctuation
symbols
    
and
operators
of
all
supported
dialects
and
the
*
combined
*
reserved
words
    
and
builtins
of
PIM
Modula
-
2
ISO
Modula
-
2
and
Modula
-
2
R10
while
not
    
differentiating
between
library
defined
identifiers
.
    
To
select
a
specific
dialect
a
dialect
option
may
be
passed
    
or
a
dialect
tag
may
be
embedded
into
a
source
file
.
    
Dialect
Options
:
    
m2pim
        
Select
PIM
Modula
-
2
dialect
.
    
m2iso
        
Select
ISO
Modula
-
2
dialect
.
    
m2r10
        
Select
Modula
-
2
R10
dialect
.
    
objm2
        
Select
Objective
Modula
-
2
dialect
.
    
The
PIM
and
ISO
dialect
options
may
be
qualified
with
a
language
extension
.
    
Language
Extensions
:
    
+
aglet
        
Select
Aglet
Modula
-
2
extensions
available
with
m2iso
.
    
+
gm2
        
Select
GNU
Modula
-
2
extensions
available
with
m2pim
.
    
+
p1
        
Select
p1
Modula
-
2
extensions
available
with
m2iso
.
    
+
xds
        
Select
XDS
Modula
-
2
extensions
available
with
m2iso
.
    
Passing
a
Dialect
Option
via
Unix
Commandline
Interface
    
Dialect
options
may
be
passed
to
the
lexer
using
the
dialect
key
.
    
Only
one
such
option
should
be
passed
.
If
multiple
dialect
options
are
    
passed
the
first
valid
option
is
used
any
subsequent
options
are
ignored
.
    
Examples
:
    
pygmentize
-
O
full
dialect
=
m2iso
-
f
html
-
o
/
path
/
to
/
output
/
path
/
to
/
input
        
Use
ISO
dialect
to
render
input
to
HTML
output
    
pygmentize
-
O
full
dialect
=
m2iso
+
p1
-
f
rtf
-
o
/
path
/
to
/
output
/
path
/
to
/
input
        
Use
ISO
dialect
with
p1
extensions
to
render
input
to
RTF
output
    
Embedding
a
Dialect
Option
within
a
source
file
    
A
dialect
option
may
be
embedded
in
a
source
file
in
form
of
a
dialect
    
tag
a
specially
formatted
comment
that
specifies
a
dialect
option
.
    
Dialect
Tag
EBNF
:
:
       
dialectTag
:
           
OpeningCommentDelim
Prefix
dialectOption
ClosingCommentDelim
;
       
dialectOption
:
           
'
m2pim
'
|
'
m2iso
'
|
'
m2r10
'
|
'
objm2
'
|
           
'
m2iso
+
aglet
'
|
'
m2pim
+
gm2
'
|
'
m2iso
+
p1
'
|
'
m2iso
+
xds
'
;
       
Prefix
:
'
!
'
;
       
OpeningCommentDelim
:
'
(
*
'
;
       
ClosingCommentDelim
:
'
*
)
'
;
    
No
whitespace
is
permitted
between
the
tokens
of
a
dialect
tag
.
    
In
the
event
that
a
source
file
contains
multiple
dialect
tags
the
first
    
tag
that
contains
a
valid
dialect
option
will
be
used
and
any
subsequent
    
dialect
tags
will
be
ignored
.
Ideally
a
dialect
tag
should
be
placed
    
at
the
beginning
of
a
source
file
.
    
An
embedded
dialect
tag
overrides
a
dialect
option
set
via
command
line
.
    
Examples
:
    
(
*
!
m2r10
*
)
DEFINITION
MODULE
Foobar
;
.
.
.
        
Use
Modula2
R10
dialect
to
render
this
source
file
.
    
(
*
!
m2pim
+
gm2
*
)
DEFINITION
MODULE
Bazbam
;
.
.
.
        
Use
PIM
dialect
with
GNU
extensions
to
render
this
source
file
.
    
Algol
Publication
Mode
:
    
In
Algol
publication
mode
source
text
is
rendered
for
publication
of
    
algorithms
in
scientific
papers
and
academic
texts
following
the
format
    
of
the
Revised
Algol
-
60
Language
Report
.
It
is
activated
by
passing
    
one
of
two
corresponding
styles
as
an
option
:
    
algol
        
render
reserved
words
lowercase
underline
boldface
        
and
builtins
lowercase
boldface
italic
    
algol_nu
        
render
reserved
words
lowercase
boldface
(
no
underlining
)
        
and
builtins
lowercase
boldface
italic
    
The
lexer
automatically
performs
the
required
lowercase
conversion
when
    
this
mode
is
activated
.
    
Example
:
    
pygmentize
-
O
full
style
=
algol
-
f
latex
-
o
/
path
/
to
/
output
/
path
/
to
/
input
        
Render
input
file
in
Algol
publication
mode
to
LaTeX
output
.
    
Rendering
Mode
of
First
Class
ADT
Identifiers
:
    
The
rendering
of
standard
library
first
class
ADT
identifiers
is
controlled
    
by
option
flag
"
treat_stdlib_adts_as_builtins
"
.
    
When
this
option
is
turned
on
standard
library
ADT
identifiers
are
rendered
    
as
builtins
.
When
it
is
turned
off
they
are
rendered
as
ordinary
library
    
identifiers
.
    
treat_stdlib_adts_as_builtins
(
default
:
On
)
    
The
option
is
useful
for
dialects
that
support
ADTs
as
first
class
objects
    
and
provide
ADTs
in
the
standard
library
that
would
otherwise
be
built
-
in
.
    
At
present
only
Modula
-
2
R10
supports
library
ADTs
as
first
class
objects
    
and
therefore
no
ADT
identifiers
are
defined
for
any
other
dialects
.
    
Example
:
    
pygmentize
-
O
full
dialect
=
m2r10
treat_stdlib_adts_as_builtins
=
Off
.
.
.
        
Render
standard
library
ADTs
as
ordinary
library
types
.
    
.
.
versionchanged
:
:
2
.
1
       
Added
multi
-
dialect
support
.
    
"
"
"
    
name
=
'
Modula
-
2
'
    
url
=
'
http
:
/
/
www
.
modula2
.
org
/
'
    
aliases
=
[
'
modula2
'
'
m2
'
]
    
filenames
=
[
'
*
.
def
'
'
*
.
mod
'
]
    
mimetypes
=
[
'
text
/
x
-
modula2
'
]
    
version_added
=
'
1
.
3
'
    
flags
=
re
.
MULTILINE
|
re
.
DOTALL
    
tokens
=
{
        
'
whitespace
'
:
[
            
(
r
'
\
n
+
'
Text
)
            
(
r
'
\
s
+
'
Text
)
        
]
        
'
dialecttags
'
:
[
            
(
r
'
\
(
\
*
!
m2pim
\
*
\
)
'
Comment
.
Special
)
            
(
r
'
\
(
\
*
!
m2iso
\
*
\
)
'
Comment
.
Special
)
            
(
r
'
\
(
\
*
!
m2r10
\
*
\
)
'
Comment
.
Special
)
            
(
r
'
\
(
\
*
!
objm2
\
*
\
)
'
Comment
.
Special
)
            
(
r
'
\
(
\
*
!
m2iso
\
+
aglet
\
*
\
)
'
Comment
.
Special
)
            
(
r
'
\
(
\
*
!
m2pim
\
+
gm2
\
*
\
)
'
Comment
.
Special
)
            
(
r
'
\
(
\
*
!
m2iso
\
+
p1
\
*
\
)
'
Comment
.
Special
)
            
(
r
'
\
(
\
*
!
m2iso
\
+
xds
\
*
\
)
'
Comment
.
Special
)
        
]
        
'
identifiers
'
:
[
            
(
r
'
(
[
a
-
zA
-
Z_
]
[
\
w
]
*
)
'
Name
)
        
]
        
'
prefixed_number_literals
'
:
[
            
(
r
'
0b
[
01
]
+
(
\
'
[
01
]
+
)
*
'
Number
.
Bin
)
            
(
r
'
0
[
ux
]
[
0
-
9A
-
F
]
+
(
\
'
[
0
-
9A
-
F
]
+
)
*
'
Number
.
Hex
)
        
]
        
'
plain_number_literals
'
:
[
            
(
r
'
[
0
-
9
]
+
(
\
'
[
0
-
9
]
+
)
*
'
             
r
'
\
.
[
0
-
9
]
+
(
\
'
[
0
-
9
]
+
)
*
'
             
r
'
[
eE
]
[
+
-
]
?
[
0
-
9
]
+
(
\
'
[
0
-
9
]
+
)
*
'
             
Number
.
Float
)
            
(
r
'
[
0
-
9
]
+
(
\
'
[
0
-
9
]
+
)
*
'
             
r
'
\
.
[
0
-
9
]
+
(
\
'
[
0
-
9
]
+
)
*
'
             
Number
.
Float
)
            
(
r
'
[
0
-
9
]
+
(
\
'
[
0
-
9
]
+
)
*
'
Number
.
Integer
)
        
]
        
'
suffixed_number_literals
'
:
[
            
(
r
'
[
0
-
7
]
+
B
'
Number
.
Oct
)
            
(
r
'
[
0
-
7
]
+
C
'
Number
.
Oct
)
            
(
r
'
[
0
-
9A
-
F
]
+
H
'
Number
.
Hex
)
        
]
        
'
string_literals
'
:
[
            
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
[
^
\
\
]
|
[
^
"
\
\
]
)
*
"
'
String
.
Double
)
            
(
r
"
'
(
\
\
\
\
|
\
\
[
^
\
\
]
|
[
^
'
\
\
]
)
*
'
"
String
.
Single
)
        
]
        
'
digraph_operators
'
:
[
            
(
r
'
\
*
\
.
'
Operator
)
            
(
r
'
\
+
>
'
Operator
)
            
(
r
'
<
>
'
Operator
)
            
(
r
'
<
=
'
Operator
)
            
(
r
'
>
=
'
Operator
)
            
(
r
'
=
=
'
Operator
)
            
(
r
'
:
:
'
Operator
)
            
(
r
'
:
=
'
Operator
)
            
(
r
'
\
+
\
+
'
Operator
)
            
(
r
'
-
-
'
Operator
)
        
]
        
'
unigraph_operators
'
:
[
            
(
r
'
[
+
-
]
'
Operator
)
            
(
r
'
[
*
/
]
'
Operator
)
            
(
r
'
\
\
'
Operator
)
            
(
r
'
[
=
#
<
>
]
'
Operator
)
            
(
r
'
\
^
'
Operator
)
            
(
r
'
'
Operator
)
            
(
r
'
&
'
Operator
)
            
(
r
'
~
'
Operator
)
            
(
r
'
'
Operator
)
        
]
        
'
digraph_punctuation
'
:
[
            
(
r
'
\
.
\
.
'
Punctuation
)
            
(
r
'
<
<
'
Punctuation
)
            
(
r
'
>
>
'
Punctuation
)
            
(
r
'
-
>
'
Punctuation
)
            
(
r
'
\
|
#
'
Punctuation
)
            
(
r
'
#
#
'
Punctuation
)
            
(
r
'
\
|
\
*
'
Punctuation
)
        
]
        
'
unigraph_punctuation
'
:
[
            
(
r
'
[
(
)
\
[
\
]
{
}
.
:
;
|
]
'
Punctuation
)
            
(
r
'
!
'
Punctuation
)
            
(
r
'
\
?
'
Punctuation
)
        
]
        
'
comments
'
:
[
            
(
r
'
^
/
/
.
*
?
\
n
'
Comment
.
Single
)
            
(
r
'
\
(
\
*
(
[
^
]
.
*
?
)
\
*
\
)
'
Comment
.
Multiline
)
            
(
r
'
/
\
*
(
.
*
?
)
\
*
/
'
Comment
.
Multiline
)
        
]
        
'
pragmas
'
:
[
            
(
r
'
<
\
*
.
*
?
\
*
>
'
Comment
.
Preproc
)
            
(
r
'
\
(
\
*
\
.
*
?
\
*
\
)
'
Comment
.
Preproc
)
        
]
        
'
root
'
:
[
            
include
(
'
whitespace
'
)
            
include
(
'
dialecttags
'
)
            
include
(
'
pragmas
'
)
            
include
(
'
comments
'
)
            
include
(
'
identifiers
'
)
            
include
(
'
suffixed_number_literals
'
)
            
include
(
'
prefixed_number_literals
'
)
            
include
(
'
plain_number_literals
'
)
            
include
(
'
string_literals
'
)
            
include
(
'
digraph_punctuation
'
)
            
include
(
'
digraph_operators
'
)
            
include
(
'
unigraph_punctuation
'
)
            
include
(
'
unigraph_operators
'
)
        
]
    
}
    
common_reserved_words
=
(
        
'
AND
'
'
ARRAY
'
'
BEGIN
'
'
BY
'
'
CASE
'
'
CONST
'
'
DEFINITION
'
'
DIV
'
        
'
DO
'
'
ELSE
'
'
ELSIF
'
'
END
'
'
EXIT
'
'
FOR
'
'
FROM
'
'
IF
'
        
'
IMPLEMENTATION
'
'
IMPORT
'
'
IN
'
'
LOOP
'
'
MOD
'
'
MODULE
'
'
NOT
'
        
'
OF
'
'
OR
'
'
POINTER
'
'
PROCEDURE
'
'
RECORD
'
'
REPEAT
'
'
RETURN
'
        
'
SET
'
'
THEN
'
'
TO
'
'
TYPE
'
'
UNTIL
'
'
VAR
'
'
WHILE
'
    
)
    
common_builtins
=
(
        
'
ABS
'
'
BOOLEAN
'
'
CARDINAL
'
'
CHAR
'
'
CHR
'
'
FALSE
'
'
INTEGER
'
        
'
LONGINT
'
'
LONGREAL
'
'
MAX
'
'
MIN
'
'
NIL
'
'
ODD
'
'
ORD
'
'
REAL
'
        
'
TRUE
'
    
)
    
common_pseudo_builtins
=
(
        
'
ADDRESS
'
'
BYTE
'
'
WORD
'
'
ADR
'
    
)
    
pim_lexemes_to_reject
=
(
        
'
!
'
'
'
'
'
'
'
'
%
'
'
?
'
'
\
\
'
'
=
=
'
'
+
+
'
'
-
-
'
'
:
:
'
'
*
.
'
        
'
+
>
'
'
-
>
'
'
<
<
'
'
>
>
'
'
|
#
'
'
#
#
'
    
)
    
pim_additional_reserved_words
=
(
        
'
EXPORT
'
'
QUALIFIED
'
'
WITH
'
    
)
    
pim_additional_builtins
=
(
        
'
BITSET
'
'
CAP
'
'
DEC
'
'
DISPOSE
'
'
EXCL
'
'
FLOAT
'
'
HALT
'
'
HIGH
'
        
'
INC
'
'
INCL
'
'
NEW
'
'
NIL
'
'
PROC
'
'
SIZE
'
'
TRUNC
'
'
VAL
'
    
)
    
pim_additional_pseudo_builtins
=
(
        
'
SYSTEM
'
'
PROCESS
'
'
TSIZE
'
'
NEWPROCESS
'
'
TRANSFER
'
    
)
    
iso_lexemes_to_reject
=
(
        
'
'
'
'
'
%
'
'
?
'
'
\
\
'
'
=
=
'
'
+
+
'
'
-
-
'
'
:
:
'
'
*
.
'
'
+
>
'
'
-
>
'
        
'
<
<
'
'
>
>
'
'
|
#
'
'
#
#
'
    
)
    
iso_additional_reserved_words
=
(
        
'
EXCEPT
'
'
EXPORT
'
'
FINALLY
'
'
FORWARD
'
'
PACKEDSET
'
'
QUALIFIED
'
        
'
REM
'
'
RETRY
'
'
WITH
'
        
'
ABSTRACT
'
'
AS
'
'
CLASS
'
'
GUARD
'
'
INHERIT
'
'
OVERRIDE
'
'
READONLY
'
        
'
REVEAL
'
'
TRACED
'
'
UNSAFEGUARDED
'
    
)
    
iso_additional_builtins
=
(
        
'
BITSET
'
'
CAP
'
'
CMPLX
'
'
COMPLEX
'
'
DEC
'
'
DISPOSE
'
'
EXCL
'
'
FLOAT
'
        
'
HALT
'
'
HIGH
'
'
IM
'
'
INC
'
'
INCL
'
'
INT
'
'
INTERRUPTIBLE
'
'
LENGTH
'
        
'
LFLOAT
'
'
LONGCOMPLEX
'
'
NEW
'
'
PROC
'
'
PROTECTION
'
'
RE
'
'
SIZE
'
        
'
TRUNC
'
'
UNINTERRUBTIBLE
'
'
VAL
'
        
'
CREATE
'
'
DESTROY
'
'
EMPTY
'
'
ISMEMBER
'
'
SELF
'
    
)
    
iso_additional_pseudo_builtins
=
(
        
'
SYSTEM
'
'
BITSPERLOC
'
'
LOCSPERBYTE
'
'
LOCSPERWORD
'
'
LOC
'
        
'
ADDADR
'
'
SUBADR
'
'
DIFADR
'
'
MAKEADR
'
'
ADR
'
        
'
ROTATE
'
'
SHIFT
'
'
CAST
'
'
TSIZE
'
        
'
COROUTINES
'
'
ATTACH
'
'
COROUTINE
'
'
CURRENT
'
'
DETACH
'
'
HANDLER
'
        
'
INTERRUPTSOURCE
'
'
IOTRANSFER
'
'
IsATTACHED
'
'
LISTEN
'
        
'
NEWCOROUTINE
'
'
PROT
'
'
TRANSFER
'
        
'
EXCEPTIONS
'
'
AllocateSource
'
'
CurrentNumber
'
'
ExceptionNumber
'
        
'
ExceptionSource
'
'
GetMessage
'
'
IsCurrentSource
'
        
'
IsExceptionalExecution
'
'
RAISE
'
        
'
TERMINATION
'
'
IsTerminating
'
'
HasHalted
'
        
'
M2EXCEPTION
'
'
M2Exceptions
'
'
M2Exception
'
'
IsM2Exception
'
        
'
indexException
'
'
rangeException
'
'
caseSelectException
'
        
'
invalidLocation
'
'
functionException
'
'
wholeValueException
'
        
'
wholeDivException
'
'
realValueException
'
'
realDivException
'
        
'
complexValueException
'
'
complexDivException
'
'
protException
'
        
'
sysException
'
'
coException
'
'
exException
'
    
)
    
m2r10_lexemes_to_reject
=
(
        
'
!
'
'
'
'
'
'
'
'
%
'
'
&
'
'
<
>
'
    
)
    
m2r10_additional_reserved_words
=
(
        
'
ALIAS
'
'
ARGLIST
'
'
BLUEPRINT
'
'
COPY
'
'
GENLIB
'
'
INDETERMINATE
'
        
'
NEW
'
'
NONE
'
'
OPAQUE
'
'
REFERENTIAL
'
'
RELEASE
'
'
RETAIN
'
        
'
ASM
'
'
REG
'
    
)
    
m2r10_additional_builtins
=
(
        
'
CARDINAL
'
'
COUNT
'
'
EMPTY
'
'
EXISTS
'
'
INSERT
'
'
LENGTH
'
'
LONGCARD
'
        
'
OCTET
'
'
PTR
'
'
PRED
'
'
READ
'
'
READNEW
'
'
REMOVE
'
'
RETRIEVE
'
'
SORT
'
        
'
STORE
'
'
SUBSET
'
'
SUCC
'
'
TLIMIT
'
'
TMAX
'
'
TMIN
'
'
TRUE
'
'
TSIZE
'
        
'
UNICHAR
'
'
WRITE
'
'
WRITEF
'
    
)
    
m2r10_additional_pseudo_builtins
=
(
        
'
TPROPERTIES
'
'
PROPERTY
'
'
LITERAL
'
'
TPROPERTY
'
'
TLITERAL
'
        
'
TBUILTIN
'
'
TDYN
'
'
TREFC
'
'
TNIL
'
'
TBASE
'
'
TPRECISION
'
        
'
TMAXEXP
'
'
TMINEXP
'
        
'
CONVERSION
'
'
TSXFSIZE
'
'
SXF
'
'
VAL
'
        
'
UNSAFE
'
'
CAST
'
'
INTRINSIC
'
'
AVAIL
'
'
ADD
'
'
SUB
'
'
ADDC
'
'
SUBC
'
        
'
FETCHADD
'
'
FETCHSUB
'
'
SHL
'
'
SHR
'
'
ASHR
'
'
ROTL
'
'
ROTR
'
'
ROTLC
'
        
'
ROTRC
'
'
BWNOT
'
'
BWAND
'
'
BWOR
'
'
BWXOR
'
'
BWNAND
'
'
BWNOR
'
        
'
SETBIT
'
'
TESTBIT
'
'
LSBIT
'
'
MSBIT
'
'
CSBITS
'
'
BAIL
'
'
HALT
'
        
'
TODO
'
'
FFI
'
'
ADDR
'
'
VARGLIST
'
'
VARGC
'
        
'
ATOMIC
'
'
INTRINSIC
'
'
AVAIL
'
'
SWAP
'
'
CAS
'
'
INC
'
'
DEC
'
'
BWAND
'
        
'
BWNAND
'
'
BWOR
'
'
BWXOR
'
        
'
COMPILER
'
'
DEBUG
'
'
MODNAME
'
'
PROCNAME
'
'
LINENUM
'
'
DEFAULT
'
        
'
HASH
'
        
'
ASSEMBLER
'
'
REGISTER
'
'
SETREG
'
'
GETREG
'
'
CODE
'
    
)
    
objm2_lexemes_to_reject
=
(
        
'
!
'
'
'
'
%
'
'
&
'
'
<
>
'
    
)
    
objm2_additional_reserved_words
=
(
        
'
BYCOPY
'
'
BYREF
'
'
CLASS
'
'
CONTINUE
'
'
CRITICAL
'
'
INOUT
'
'
METHOD
'
        
'
ON
'
'
OPTIONAL
'
'
OUT
'
'
PRIVATE
'
'
PROTECTED
'
'
PROTOCOL
'
'
PUBLIC
'
        
'
SUPER
'
'
TRY
'
    
)
    
objm2_additional_builtins
=
(
        
'
OBJECT
'
'
NO
'
'
YES
'
    
)
    
objm2_additional_pseudo_builtins
=
(
    
)
    
aglet_additional_reserved_words
=
(
    
)
    
aglet_additional_builtins
=
(
        
'
BITSET8
'
'
BITSET16
'
'
BITSET32
'
'
CARDINAL8
'
'
CARDINAL16
'
        
'
CARDINAL32
'
'
INTEGER8
'
'
INTEGER16
'
'
INTEGER32
'
    
)
    
aglet_additional_pseudo_builtins
=
(
    
)
    
gm2_additional_reserved_words
=
(
        
'
ASM
'
'
__ATTRIBUTE__
'
'
__BUILTIN__
'
'
__COLUMN__
'
'
__DATE__
'
        
'
__FILE__
'
'
__FUNCTION__
'
'
__LINE__
'
'
__MODULE__
'
'
VOLATILE
'
    
)
    
gm2_additional_builtins
=
(
        
'
BITSET8
'
'
BITSET16
'
'
BITSET32
'
'
CARDINAL8
'
'
CARDINAL16
'
        
'
CARDINAL32
'
'
CARDINAL64
'
'
COMPLEX32
'
'
COMPLEX64
'
'
COMPLEX96
'
        
'
COMPLEX128
'
'
INTEGER8
'
'
INTEGER16
'
'
INTEGER32
'
'
INTEGER64
'
        
'
REAL8
'
'
REAL16
'
'
REAL32
'
'
REAL96
'
'
REAL128
'
'
THROW
'
    
)
    
gm2_additional_pseudo_builtins
=
(
    
)
    
p1_additional_reserved_words
=
(
    
)
    
p1_additional_builtins
=
(
    
)
    
p1_additional_pseudo_builtins
=
(
        
'
BCD
'
    
)
    
xds_additional_reserved_words
=
(
        
'
SEQ
'
    
)
    
xds_additional_builtins
=
(
        
'
ASH
'
'
ASSERT
'
'
DIFFADR_TYPE
'
'
ENTIER
'
'
INDEX
'
'
LEN
'
        
'
LONGCARD
'
'
SHORTCARD
'
'
SHORTINT
'
    
)
    
xds_additional_pseudo_builtins
=
(
        
'
PROCESS
'
'
NEWPROCESS
'
'
BOOL8
'
'
BOOL16
'
'
BOOL32
'
'
CARD8
'
        
'
CARD16
'
'
CARD32
'
'
INT8
'
'
INT16
'
'
INT32
'
'
REF
'
'
MOVE
'
        
'
FILL
'
'
GET
'
'
PUT
'
'
CC
'
'
int
'
'
unsigned
'
'
size_t
'
'
void
'
        
'
COMPILER
'
'
OPTION
'
'
EQUATION
'
    
)
    
pim_stdlib_module_identifiers
=
(
        
'
Terminal
'
'
FileSystem
'
'
InOut
'
'
RealInOut
'
'
MathLib0
'
'
Storage
'
    
)
    
pim_stdlib_type_identifiers
=
(
        
'
Flag
'
'
FlagSet
'
'
Response
'
'
Command
'
'
Lock
'
'
Permission
'
        
'
MediumType
'
'
File
'
'
FileProc
'
'
DirectoryProc
'
'
FileCommand
'
        
'
DirectoryCommand
'
    
)
    
pim_stdlib_proc_identifiers
=
(
        
'
Read
'
'
BusyRead
'
'
ReadAgain
'
'
Write
'
'
WriteString
'
'
WriteLn
'
        
'
Create
'
'
Lookup
'
'
Close
'
'
Delete
'
'
Rename
'
'
SetRead
'
'
SetWrite
'
        
'
SetModify
'
'
SetOpen
'
'
Doio
'
'
SetPos
'
'
GetPos
'
'
Length
'
'
Reset
'
        
'
Again
'
'
ReadWord
'
'
WriteWord
'
'
ReadChar
'
'
WriteChar
'
        
'
CreateMedium
'
'
DeleteMedium
'
'
AssignName
'
'
DeassignName
'
        
'
ReadMedium
'
'
LookupMedium
'
'
OpenInput
'
'
OpenOutput
'
'
CloseInput
'
        
'
CloseOutput
'
'
ReadString
'
'
ReadInt
'
'
ReadCard
'
'
ReadWrd
'
        
'
WriteInt
'
'
WriteCard
'
'
WriteOct
'
'
WriteHex
'
'
WriteWrd
'
        
'
ReadReal
'
'
WriteReal
'
'
WriteFixPt
'
'
WriteRealOct
'
'
sqrt
'
'
exp
'
        
'
ln
'
'
sin
'
'
cos
'
'
arctan
'
'
entier
'
'
ALLOCATE
'
'
DEALLOCATE
'
    
)
    
pim_stdlib_var_identifiers
=
(
        
'
Done
'
'
termCH
'
'
in
'
'
out
'
    
)
    
pim_stdlib_const_identifiers
=
(
        
'
EOL
'
    
)
    
iso_stdlib_module_identifiers
=
(
    
)
    
iso_stdlib_type_identifiers
=
(
    
)
    
iso_stdlib_proc_identifiers
=
(
    
)
    
iso_stdlib_var_identifiers
=
(
    
)
    
iso_stdlib_const_identifiers
=
(
    
)
    
m2r10_stdlib_adt_identifiers
=
(
        
'
BCD
'
'
LONGBCD
'
'
BITSET
'
'
SHORTBITSET
'
'
LONGBITSET
'
        
'
LONGLONGBITSET
'
'
COMPLEX
'
'
LONGCOMPLEX
'
'
SHORTCARD
'
'
LONGLONGCARD
'
        
'
SHORTINT
'
'
LONGLONGINT
'
'
POSINT
'
'
SHORTPOSINT
'
'
LONGPOSINT
'
        
'
LONGLONGPOSINT
'
'
BITSET8
'
'
BITSET16
'
'
BITSET32
'
'
BITSET64
'
        
'
BITSET128
'
'
BS8
'
'
BS16
'
'
BS32
'
'
BS64
'
'
BS128
'
'
CARDINAL8
'
        
'
CARDINAL16
'
'
CARDINAL32
'
'
CARDINAL64
'
'
CARDINAL128
'
'
CARD8
'
        
'
CARD16
'
'
CARD32
'
'
CARD64
'
'
CARD128
'
'
INTEGER8
'
'
INTEGER16
'
        
'
INTEGER32
'
'
INTEGER64
'
'
INTEGER128
'
'
INT8
'
'
INT16
'
'
INT32
'
        
'
INT64
'
'
INT128
'
'
STRING
'
'
UNISTRING
'
    
)
    
m2r10_stdlib_blueprint_identifiers
=
(
        
'
ProtoRoot
'
'
ProtoComputational
'
'
ProtoNumeric
'
'
ProtoScalar
'
        
'
ProtoNonScalar
'
'
ProtoCardinal
'
'
ProtoInteger
'
'
ProtoReal
'
        
'
ProtoComplex
'
'
ProtoVector
'
'
ProtoTuple
'
'
ProtoCompArray
'
        
'
ProtoCollection
'
'
ProtoStaticArray
'
'
ProtoStaticSet
'
        
'
ProtoStaticString
'
'
ProtoArray
'
'
ProtoString
'
'
ProtoSet
'
        
'
ProtoMultiSet
'
'
ProtoDictionary
'
'
ProtoMultiDict
'
'
ProtoExtension
'
        
'
ProtoIO
'
'
ProtoCardMath
'
'
ProtoIntMath
'
'
ProtoRealMath
'
    
)
    
m2r10_stdlib_module_identifiers
=
(
        
'
ASCII
'
'
BooleanIO
'
'
CharIO
'
'
UnicharIO
'
'
OctetIO
'
        
'
CardinalIO
'
'
LongCardIO
'
'
IntegerIO
'
'
LongIntIO
'
'
RealIO
'
        
'
LongRealIO
'
'
BCDIO
'
'
LongBCDIO
'
'
CardMath
'
'
LongCardMath
'
        
'
IntMath
'
'
LongIntMath
'
'
RealMath
'
'
LongRealMath
'
'
BCDMath
'
        
'
LongBCDMath
'
'
FileIO
'
'
FileSystem
'
'
Storage
'
'
IOSupport
'
    
)
    
m2r10_stdlib_type_identifiers
=
(
        
'
File
'
'
Status
'
    
)
    
m2r10_stdlib_proc_identifiers
=
(
        
'
ALLOCATE
'
'
DEALLOCATE
'
'
SIZE
'
    
)
    
m2r10_stdlib_var_identifiers
=
(
        
'
stdIn
'
'
stdOut
'
'
stdErr
'
    
)
    
m2r10_stdlib_const_identifiers
=
(
        
'
pi
'
'
tau
'
    
)
    
dialects
=
(
        
'
unknown
'
        
'
m2pim
'
'
m2iso
'
'
m2r10
'
'
objm2
'
        
'
m2iso
+
aglet
'
'
m2pim
+
gm2
'
'
m2iso
+
p1
'
'
m2iso
+
xds
'
    
)
    
lexemes_to_reject_db
=
{
        
'
unknown
'
:
(
        
)
        
'
m2pim
'
:
(
            
pim_lexemes_to_reject
        
)
        
'
m2iso
'
:
(
            
iso_lexemes_to_reject
        
)
        
'
m2r10
'
:
(
            
m2r10_lexemes_to_reject
        
)
        
'
objm2
'
:
(
            
objm2_lexemes_to_reject
        
)
        
'
m2iso
+
aglet
'
:
(
            
iso_lexemes_to_reject
        
)
        
'
m2pim
+
gm2
'
:
(
            
pim_lexemes_to_reject
        
)
        
'
m2iso
+
p1
'
:
(
            
iso_lexemes_to_reject
        
)
        
'
m2iso
+
xds
'
:
(
            
iso_lexemes_to_reject
        
)
    
}
    
reserved_words_db
=
{
        
'
unknown
'
:
(
            
common_reserved_words
            
pim_additional_reserved_words
            
iso_additional_reserved_words
            
m2r10_additional_reserved_words
        
)
        
'
m2pim
'
:
(
            
common_reserved_words
            
pim_additional_reserved_words
        
)
        
'
m2iso
'
:
(
            
common_reserved_words
            
iso_additional_reserved_words
        
)
        
'
m2r10
'
:
(
            
common_reserved_words
            
m2r10_additional_reserved_words
        
)
        
'
objm2
'
:
(
            
common_reserved_words
            
m2r10_additional_reserved_words
            
objm2_additional_reserved_words
        
)
        
'
m2iso
+
aglet
'
:
(
            
common_reserved_words
            
iso_additional_reserved_words
            
aglet_additional_reserved_words
        
)
        
'
m2pim
+
gm2
'
:
(
            
common_reserved_words
            
pim_additional_reserved_words
            
gm2_additional_reserved_words
        
)
        
'
m2iso
+
p1
'
:
(
            
common_reserved_words
            
iso_additional_reserved_words
            
p1_additional_reserved_words
        
)
        
'
m2iso
+
xds
'
:
(
            
common_reserved_words
            
iso_additional_reserved_words
            
xds_additional_reserved_words
        
)
    
}
    
builtins_db
=
{
        
'
unknown
'
:
(
            
common_builtins
            
pim_additional_builtins
            
iso_additional_builtins
            
m2r10_additional_builtins
        
)
        
'
m2pim
'
:
(
            
common_builtins
            
pim_additional_builtins
        
)
        
'
m2iso
'
:
(
            
common_builtins
            
iso_additional_builtins
        
)
        
'
m2r10
'
:
(
            
common_builtins
            
m2r10_additional_builtins
        
)
        
'
objm2
'
:
(
            
common_builtins
            
m2r10_additional_builtins
            
objm2_additional_builtins
        
)
        
'
m2iso
+
aglet
'
:
(
            
common_builtins
            
iso_additional_builtins
            
aglet_additional_builtins
        
)
        
'
m2pim
+
gm2
'
:
(
            
common_builtins
            
pim_additional_builtins
            
gm2_additional_builtins
        
)
        
'
m2iso
+
p1
'
:
(
            
common_builtins
            
iso_additional_builtins
            
p1_additional_builtins
        
)
        
'
m2iso
+
xds
'
:
(
            
common_builtins
            
iso_additional_builtins
            
xds_additional_builtins
        
)
    
}
    
pseudo_builtins_db
=
{
        
'
unknown
'
:
(
            
common_pseudo_builtins
            
pim_additional_pseudo_builtins
            
iso_additional_pseudo_builtins
            
m2r10_additional_pseudo_builtins
        
)
        
'
m2pim
'
:
(
            
common_pseudo_builtins
            
pim_additional_pseudo_builtins
        
)
        
'
m2iso
'
:
(
            
common_pseudo_builtins
            
iso_additional_pseudo_builtins
        
)
        
'
m2r10
'
:
(
            
common_pseudo_builtins
            
m2r10_additional_pseudo_builtins
        
)
        
'
objm2
'
:
(
            
common_pseudo_builtins
            
m2r10_additional_pseudo_builtins
            
objm2_additional_pseudo_builtins
        
)
        
'
m2iso
+
aglet
'
:
(
            
common_pseudo_builtins
            
iso_additional_pseudo_builtins
            
aglet_additional_pseudo_builtins
        
)
        
'
m2pim
+
gm2
'
:
(
            
common_pseudo_builtins
            
pim_additional_pseudo_builtins
            
gm2_additional_pseudo_builtins
        
)
        
'
m2iso
+
p1
'
:
(
            
common_pseudo_builtins
            
iso_additional_pseudo_builtins
            
p1_additional_pseudo_builtins
        
)
        
'
m2iso
+
xds
'
:
(
            
common_pseudo_builtins
            
iso_additional_pseudo_builtins
            
xds_additional_pseudo_builtins
        
)
    
}
    
stdlib_adts_db
=
{
        
'
unknown
'
:
(
        
)
        
'
m2pim
'
:
(
        
)
        
'
m2iso
'
:
(
        
)
        
'
m2r10
'
:
(
            
m2r10_stdlib_adt_identifiers
        
)
        
'
objm2
'
:
(
            
m2r10_stdlib_adt_identifiers
        
)
        
'
m2iso
+
aglet
'
:
(
        
)
        
'
m2pim
+
gm2
'
:
(
        
)
        
'
m2iso
+
p1
'
:
(
        
)
        
'
m2iso
+
xds
'
:
(
        
)
    
}
    
stdlib_modules_db
=
{
        
'
unknown
'
:
(
        
)
        
'
m2pim
'
:
(
            
pim_stdlib_module_identifiers
        
)
        
'
m2iso
'
:
(
            
iso_stdlib_module_identifiers
        
)
        
'
m2r10
'
:
(
            
m2r10_stdlib_blueprint_identifiers
            
m2r10_stdlib_module_identifiers
            
m2r10_stdlib_adt_identifiers
        
)
        
'
objm2
'
:
(
            
m2r10_stdlib_blueprint_identifiers
            
m2r10_stdlib_module_identifiers
        
)
        
'
m2iso
+
aglet
'
:
(
            
iso_stdlib_module_identifiers
        
)
        
'
m2pim
+
gm2
'
:
(
            
pim_stdlib_module_identifiers
        
)
        
'
m2iso
+
p1
'
:
(
            
iso_stdlib_module_identifiers
        
)
        
'
m2iso
+
xds
'
:
(
            
iso_stdlib_module_identifiers
        
)
    
}
    
stdlib_types_db
=
{
        
'
unknown
'
:
(
        
)
        
'
m2pim
'
:
(
            
pim_stdlib_type_identifiers
        
)
        
'
m2iso
'
:
(
            
iso_stdlib_type_identifiers
        
)
        
'
m2r10
'
:
(
            
m2r10_stdlib_type_identifiers
        
)
        
'
objm2
'
:
(
            
m2r10_stdlib_type_identifiers
        
)
        
'
m2iso
+
aglet
'
:
(
            
iso_stdlib_type_identifiers
        
)
        
'
m2pim
+
gm2
'
:
(
            
pim_stdlib_type_identifiers
        
)
        
'
m2iso
+
p1
'
:
(
            
iso_stdlib_type_identifiers
        
)
        
'
m2iso
+
xds
'
:
(
            
iso_stdlib_type_identifiers
        
)
    
}
    
stdlib_procedures_db
=
{
        
'
unknown
'
:
(
        
)
        
'
m2pim
'
:
(
            
pim_stdlib_proc_identifiers
        
)
        
'
m2iso
'
:
(
            
iso_stdlib_proc_identifiers
        
)
        
'
m2r10
'
:
(
            
m2r10_stdlib_proc_identifiers
        
)
        
'
objm2
'
:
(
            
m2r10_stdlib_proc_identifiers
        
)
        
'
m2iso
+
aglet
'
:
(
            
iso_stdlib_proc_identifiers
        
)
        
'
m2pim
+
gm2
'
:
(
            
pim_stdlib_proc_identifiers
        
)
        
'
m2iso
+
p1
'
:
(
            
iso_stdlib_proc_identifiers
        
)
        
'
m2iso
+
xds
'
:
(
            
iso_stdlib_proc_identifiers
        
)
    
}
    
stdlib_variables_db
=
{
        
'
unknown
'
:
(
        
)
        
'
m2pim
'
:
(
            
pim_stdlib_var_identifiers
        
)
        
'
m2iso
'
:
(
            
iso_stdlib_var_identifiers
        
)
        
'
m2r10
'
:
(
            
m2r10_stdlib_var_identifiers
        
)
        
'
objm2
'
:
(
            
m2r10_stdlib_var_identifiers
        
)
        
'
m2iso
+
aglet
'
:
(
            
iso_stdlib_var_identifiers
        
)
        
'
m2pim
+
gm2
'
:
(
            
pim_stdlib_var_identifiers
        
)
        
'
m2iso
+
p1
'
:
(
            
iso_stdlib_var_identifiers
        
)
        
'
m2iso
+
xds
'
:
(
            
iso_stdlib_var_identifiers
        
)
    
}
    
stdlib_constants_db
=
{
        
'
unknown
'
:
(
        
)
        
'
m2pim
'
:
(
            
pim_stdlib_const_identifiers
        
)
        
'
m2iso
'
:
(
            
iso_stdlib_const_identifiers
        
)
        
'
m2r10
'
:
(
            
m2r10_stdlib_const_identifiers
        
)
        
'
objm2
'
:
(
            
m2r10_stdlib_const_identifiers
        
)
        
'
m2iso
+
aglet
'
:
(
            
iso_stdlib_const_identifiers
        
)
        
'
m2pim
+
gm2
'
:
(
            
pim_stdlib_const_identifiers
        
)
        
'
m2iso
+
p1
'
:
(
            
iso_stdlib_const_identifiers
        
)
        
'
m2iso
+
xds
'
:
(
            
iso_stdlib_const_identifiers
        
)
    
}
    
def
__init__
(
self
*
*
options
)
:
        
dialects
=
get_list_opt
(
options
'
dialect
'
[
]
)
        
for
dialect_option
in
dialects
:
            
if
dialect_option
in
self
.
dialects
[
1
:
-
1
]
:
                
self
.
set_dialect
(
dialect_option
)
                
break
        
else
:
            
self
.
set_dialect
(
'
unknown
'
)
        
self
.
dialect_set_by_tag
=
False
        
styles
=
get_list_opt
(
options
'
style
'
[
]
)
        
if
'
algol
'
in
styles
or
'
algol_nu
'
in
styles
:
            
self
.
algol_publication_mode
=
True
        
else
:
            
self
.
algol_publication_mode
=
False
        
self
.
treat_stdlib_adts_as_builtins
=
get_bool_opt
(
            
options
'
treat_stdlib_adts_as_builtins
'
True
)
        
RegexLexer
.
__init__
(
self
*
*
options
)
    
def
set_dialect
(
self
dialect_id
)
:
        
if
dialect_id
not
in
self
.
dialects
:
            
dialect
=
'
unknown
'
        
else
:
            
dialect
=
dialect_id
        
lexemes_to_reject_set
=
set
(
)
        
for
list
in
self
.
lexemes_to_reject_db
[
dialect
]
:
            
lexemes_to_reject_set
.
update
(
set
(
list
)
)
        
reswords_set
=
set
(
)
        
for
list
in
self
.
reserved_words_db
[
dialect
]
:
            
reswords_set
.
update
(
set
(
list
)
)
        
builtins_set
=
set
(
)
        
for
list
in
self
.
builtins_db
[
dialect
]
:
            
builtins_set
.
update
(
set
(
list
)
.
difference
(
reswords_set
)
)
        
pseudo_builtins_set
=
set
(
)
        
for
list
in
self
.
pseudo_builtins_db
[
dialect
]
:
            
pseudo_builtins_set
.
update
(
set
(
list
)
.
difference
(
reswords_set
)
)
        
adts_set
=
set
(
)
        
for
list
in
self
.
stdlib_adts_db
[
dialect
]
:
            
adts_set
.
update
(
set
(
list
)
.
difference
(
reswords_set
)
)
        
modules_set
=
set
(
)
        
for
list
in
self
.
stdlib_modules_db
[
dialect
]
:
            
modules_set
.
update
(
set
(
list
)
.
difference
(
builtins_set
)
)
        
types_set
=
set
(
)
        
for
list
in
self
.
stdlib_types_db
[
dialect
]
:
            
types_set
.
update
(
set
(
list
)
.
difference
(
builtins_set
)
)
        
procedures_set
=
set
(
)
        
for
list
in
self
.
stdlib_procedures_db
[
dialect
]
:
            
procedures_set
.
update
(
set
(
list
)
.
difference
(
builtins_set
)
)
        
variables_set
=
set
(
)
        
for
list
in
self
.
stdlib_variables_db
[
dialect
]
:
            
variables_set
.
update
(
set
(
list
)
.
difference
(
builtins_set
)
)
        
constants_set
=
set
(
)
        
for
list
in
self
.
stdlib_constants_db
[
dialect
]
:
            
constants_set
.
update
(
set
(
list
)
.
difference
(
builtins_set
)
)
        
self
.
dialect
=
dialect
        
self
.
lexemes_to_reject
=
lexemes_to_reject_set
        
self
.
reserved_words
=
reswords_set
        
self
.
builtins
=
builtins_set
        
self
.
pseudo_builtins
=
pseudo_builtins_set
        
self
.
adts
=
adts_set
        
self
.
modules
=
modules_set
        
self
.
types
=
types_set
        
self
.
procedures
=
procedures_set
        
self
.
variables
=
variables_set
        
self
.
constants
=
constants_set
    
def
get_dialect_from_dialect_tag
(
self
dialect_tag
)
:
        
left_tag_delim
=
'
(
*
!
'
        
right_tag_delim
=
'
*
)
'
        
left_tag_delim_len
=
len
(
left_tag_delim
)
        
right_tag_delim_len
=
len
(
right_tag_delim
)
        
indicator_start
=
left_tag_delim_len
        
indicator_end
=
-
(
right_tag_delim_len
)
        
if
len
(
dialect_tag
)
>
(
left_tag_delim_len
+
right_tag_delim_len
)
\
           
and
dialect_tag
.
startswith
(
left_tag_delim
)
\
           
and
dialect_tag
.
endswith
(
right_tag_delim
)
:
            
indicator
=
dialect_tag
[
indicator_start
:
indicator_end
]
            
for
index
in
range
(
1
len
(
self
.
dialects
)
)
:
                
if
indicator
=
=
self
.
dialects
[
index
]
:
                    
return
indicator
            
else
:
                
return
'
unknown
'
        
else
:
            
return
'
unknown
'
    
def
get_tokens_unprocessed
(
self
text
)
:
        
for
index
token
value
in
RegexLexer
.
get_tokens_unprocessed
(
self
text
)
:
            
if
not
self
.
dialect_set_by_tag
and
token
=
=
Comment
.
Special
:
                
indicated_dialect
=
self
.
get_dialect_from_dialect_tag
(
value
)
                
if
indicated_dialect
!
=
'
unknown
'
:
                    
self
.
set_dialect
(
indicated_dialect
)
                    
self
.
dialect_set_by_tag
=
True
            
if
token
is
Name
:
                
if
value
in
self
.
reserved_words
:
                    
token
=
Keyword
.
Reserved
                    
if
self
.
algol_publication_mode
:
                        
value
=
value
.
lower
(
)
                
elif
value
in
self
.
builtins
:
                    
token
=
Name
.
Builtin
                    
if
self
.
algol_publication_mode
:
                        
value
=
value
.
lower
(
)
                
elif
value
in
self
.
pseudo_builtins
:
                    
token
=
Name
.
Builtin
.
Pseudo
                    
if
self
.
algol_publication_mode
:
                        
value
=
value
.
lower
(
)
                
elif
value
in
self
.
adts
:
                    
if
not
self
.
treat_stdlib_adts_as_builtins
:
                        
token
=
Name
.
Namespace
                    
else
:
                        
token
=
Name
.
Builtin
.
Pseudo
                        
if
self
.
algol_publication_mode
:
                            
value
=
value
.
lower
(
)
                
elif
value
in
self
.
modules
:
                    
token
=
Name
.
Namespace
                
elif
value
in
self
.
types
:
                    
token
=
Name
.
Class
                
elif
value
in
self
.
procedures
:
                    
token
=
Name
.
Function
                
elif
value
in
self
.
variables
:
                    
token
=
Name
.
Variable
                
elif
value
in
self
.
constants
:
                    
token
=
Name
.
Constant
            
elif
token
in
Number
:
                
if
self
.
dialect
not
in
(
'
unknown
'
'
m2r10
'
'
objm2
'
)
:
                    
if
"
'
"
in
value
or
value
[
0
:
2
]
in
(
'
0b
'
'
0x
'
'
0u
'
)
:
                        
token
=
Error
                
elif
self
.
dialect
in
(
'
m2r10
'
'
objm2
'
)
:
                    
if
token
is
Number
.
Oct
:
                        
token
=
Error
                    
elif
token
is
Number
.
Hex
and
'
H
'
in
value
:
                        
token
=
Error
                    
elif
token
is
Number
.
Float
and
'
E
'
in
value
:
                        
token
=
Error
            
elif
token
in
Comment
:
                
if
token
is
Comment
.
Single
:
                    
if
self
.
dialect
not
in
(
'
unknown
'
'
m2r10
'
'
objm2
'
)
:
                        
token
=
Error
                
if
token
is
Comment
.
Preproc
:
                    
if
value
.
startswith
(
'
<
*
'
)
and
\
                       
self
.
dialect
.
startswith
(
'
m2pim
'
)
:
                        
token
=
Error
                    
elif
value
.
startswith
(
'
(
*
'
)
and
\
                            
self
.
dialect
!
=
'
unknown
'
and
\
                            
not
self
.
dialect
.
startswith
(
'
m2pim
'
)
:
                        
token
=
Comment
.
Multiline
            
else
:
                
if
value
in
self
.
lexemes_to_reject
:
                    
token
=
Error
                
if
self
.
algol_publication_mode
:
                    
if
value
=
=
'
#
'
:
                        
value
=
'
'
                    
elif
value
=
=
'
<
=
'
:
                        
value
=
'
'
                    
elif
value
=
=
'
>
=
'
:
                        
value
=
'
'
                    
elif
value
=
=
'
=
=
'
:
                        
value
=
'
'
                    
elif
value
=
=
'
*
.
'
:
                        
value
=
'
'
            
yield
index
token
value
    
def
analyse_text
(
text
)
:
        
"
"
"
It
'
s
Pascal
-
like
but
does
not
use
FUNCTION
-
-
uses
PROCEDURE
        
instead
.
"
"
"
        
if
not
(
'
(
*
'
in
text
and
'
*
)
'
in
text
and
'
:
=
'
in
text
)
:
            
return
        
result
=
0
        
if
re
.
search
(
r
'
\
bPROCEDURE
\
b
'
text
)
:
            
result
+
=
0
.
6
        
if
re
.
search
(
r
'
\
bFUNCTION
\
b
'
text
)
:
            
result
=
0
.
0
        
return
result
