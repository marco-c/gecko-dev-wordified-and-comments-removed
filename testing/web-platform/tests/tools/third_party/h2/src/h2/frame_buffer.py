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
frame_buffer
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
A
data
structure
that
provides
a
way
to
iterate
over
a
byte
buffer
in
terms
of
frames
.
"
"
"
from
hyperframe
.
exceptions
import
InvalidFrameError
InvalidDataError
from
hyperframe
.
frame
import
(
    
Frame
HeadersFrame
ContinuationFrame
PushPromiseFrame
)
from
.
exceptions
import
(
    
ProtocolError
FrameTooLargeError
FrameDataMissingError
)
CONTINUATION_BACKLOG
=
64
class
FrameBuffer
:
    
"
"
"
    
This
is
a
data
structure
that
expects
to
act
as
a
buffer
for
HTTP
/
2
data
    
that
allows
iteraton
in
terms
of
H2
frames
.
    
"
"
"
    
def
__init__
(
self
server
=
False
)
:
        
self
.
data
=
b
'
'
        
self
.
max_frame_size
=
0
        
self
.
_preamble
=
b
'
PRI
*
HTTP
/
2
.
0
\
r
\
n
\
r
\
nSM
\
r
\
n
\
r
\
n
'
if
server
else
b
'
'
        
self
.
_preamble_len
=
len
(
self
.
_preamble
)
        
self
.
_headers_buffer
=
[
]
    
def
add_data
(
self
data
)
:
        
"
"
"
        
Add
more
data
to
the
frame
buffer
.
        
:
param
data
:
A
bytestring
containing
the
byte
buffer
.
        
"
"
"
        
if
self
.
_preamble_len
:
            
data_len
=
len
(
data
)
            
of_which_preamble
=
min
(
self
.
_preamble_len
data_len
)
            
if
self
.
_preamble
[
:
of_which_preamble
]
!
=
data
[
:
of_which_preamble
]
:
                
raise
ProtocolError
(
"
Invalid
HTTP
/
2
preamble
.
"
)
            
data
=
data
[
of_which_preamble
:
]
            
self
.
_preamble_len
-
=
of_which_preamble
            
self
.
_preamble
=
self
.
_preamble
[
of_which_preamble
:
]
        
self
.
data
+
=
data
    
def
_validate_frame_length
(
self
length
)
:
        
"
"
"
        
Confirm
that
the
frame
is
an
appropriate
length
.
        
"
"
"
        
if
length
>
self
.
max_frame_size
:
            
raise
FrameTooLargeError
(
                
"
Received
overlong
frame
:
length
%
d
max
%
d
"
%
                
(
length
self
.
max_frame_size
)
            
)
    
def
_update_header_buffer
(
self
f
)
:
        
"
"
"
        
Updates
the
internal
header
buffer
.
Returns
a
frame
that
should
replace
        
the
current
one
.
May
throw
exceptions
if
this
frame
is
invalid
.
        
"
"
"
        
if
self
.
_headers_buffer
:
            
stream_id
=
self
.
_headers_buffer
[
0
]
.
stream_id
            
valid_frame
=
(
                
f
is
not
None
and
                
isinstance
(
f
ContinuationFrame
)
and
                
f
.
stream_id
=
=
stream_id
            
)
            
if
not
valid_frame
:
                
raise
ProtocolError
(
"
Invalid
frame
during
header
block
.
"
)
            
self
.
_headers_buffer
.
append
(
f
)
            
if
len
(
self
.
_headers_buffer
)
>
CONTINUATION_BACKLOG
:
                
raise
ProtocolError
(
"
Too
many
continuation
frames
received
.
"
)
            
if
'
END_HEADERS
'
in
f
.
flags
:
                
f
=
self
.
_headers_buffer
[
0
]
                
f
.
flags
.
add
(
'
END_HEADERS
'
)
                
f
.
data
=
b
'
'
.
join
(
x
.
data
for
x
in
self
.
_headers_buffer
)
                
self
.
_headers_buffer
=
[
]
            
else
:
                
f
=
None
        
elif
(
isinstance
(
f
(
HeadersFrame
PushPromiseFrame
)
)
and
                
'
END_HEADERS
'
not
in
f
.
flags
)
:
            
self
.
_headers_buffer
.
append
(
f
)
            
f
=
None
        
return
f
    
def
__iter__
(
self
)
:
        
return
self
    
def
__next__
(
self
)
:
        
if
len
(
self
.
data
)
<
9
:
            
raise
StopIteration
(
)
        
try
:
            
f
length
=
Frame
.
parse_frame_header
(
self
.
data
[
:
9
]
)
        
except
(
InvalidDataError
InvalidFrameError
)
as
e
:
            
raise
ProtocolError
(
                
"
Received
frame
with
invalid
header
:
%
s
"
%
str
(
e
)
            
)
        
if
len
(
self
.
data
)
<
length
+
9
:
            
raise
StopIteration
(
)
        
self
.
_validate_frame_length
(
length
)
        
try
:
            
f
.
parse_body
(
memoryview
(
self
.
data
[
9
:
9
+
length
]
)
)
        
except
InvalidDataError
:
            
raise
ProtocolError
(
"
Received
frame
with
non
-
compliant
data
"
)
        
except
InvalidFrameError
:
            
raise
FrameDataMissingError
(
"
Frame
data
missing
or
invalid
"
)
        
self
.
data
=
self
.
data
[
9
+
length
:
]
        
f
=
self
.
_update_header_buffer
(
f
)
        
return
f
if
f
is
not
None
else
self
.
__next__
(
)
