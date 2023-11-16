#
-
*
-
coding
:
utf
-
8
-
*
-
"
"
"
h2
/
errors
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
Global
error
code
registry
containing
the
established
HTTP
/
2
error
codes
.
The
current
registry
is
available
at
:
https
:
/
/
tools
.
ietf
.
org
/
html
/
rfc7540
#
section
-
11
.
4
"
"
"
import
enum
class
ErrorCodes
(
enum
.
IntEnum
)
:
    
"
"
"
    
All
known
HTTP
/
2
error
codes
.
    
.
.
versionadded
:
:
2
.
5
.
0
    
"
"
"
    
NO_ERROR
=
0x0
    
PROTOCOL_ERROR
=
0x1
    
INTERNAL_ERROR
=
0x2
    
FLOW_CONTROL_ERROR
=
0x3
    
SETTINGS_TIMEOUT
=
0x4
    
STREAM_CLOSED
=
0x5
    
FRAME_SIZE_ERROR
=
0x6
    
REFUSED_STREAM
=
0x7
    
CANCEL
=
0x8
    
COMPRESSION_ERROR
=
0x9
    
CONNECT_ERROR
=
0xa
    
ENHANCE_YOUR_CALM
=
0xb
    
INADEQUATE_SECURITY
=
0xc
    
HTTP_1_1_REQUIRED
=
0xd
def
_error_code_from_int
(
code
)
:
    
"
"
"
    
Given
an
integer
error
code
returns
either
one
of
:
class
:
ErrorCodes
    
<
h2
.
errors
.
ErrorCodes
>
or
if
not
present
in
the
known
set
of
codes
    
returns
the
integer
directly
.
    
"
"
"
    
try
:
        
return
ErrorCodes
(
code
)
    
except
ValueError
:
        
return
code
__all__
=
[
'
ErrorCodes
'
]
