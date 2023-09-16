from
__future__
import
annotations
import
enum
import
logging
import
uuid
from
typing
import
Generator
List
Optional
Type
Union
from
.
exceptions
import
(
    
ConnectionClosed
    
ConnectionClosedError
    
ConnectionClosedOK
    
InvalidState
    
PayloadTooBig
    
ProtocolError
)
from
.
extensions
import
Extension
from
.
frames
import
(
    
OK_CLOSE_CODES
    
OP_BINARY
    
OP_CLOSE
    
OP_CONT
    
OP_PING
    
OP_PONG
    
OP_TEXT
    
Close
    
Frame
)
from
.
http11
import
Request
Response
from
.
streams
import
StreamReader
from
.
typing
import
LoggerLike
Origin
Subprotocol
__all__
=
[
    
"
Connection
"
    
"
Side
"
    
"
State
"
    
"
SEND_EOF
"
]
Event
=
Union
[
Request
Response
Frame
]
"
"
"
Events
that
:
meth
:
~
Connection
.
events_received
may
return
.
"
"
"
class
Side
(
enum
.
IntEnum
)
:
    
"
"
"
A
WebSocket
connection
is
either
a
server
or
a
client
.
"
"
"
    
SERVER
CLIENT
=
range
(
2
)
SERVER
=
Side
.
SERVER
CLIENT
=
Side
.
CLIENT
class
State
(
enum
.
IntEnum
)
:
    
"
"
"
A
WebSocket
connection
is
in
one
of
these
four
states
.
"
"
"
    
CONNECTING
OPEN
CLOSING
CLOSED
=
range
(
4
)
CONNECTING
=
State
.
CONNECTING
OPEN
=
State
.
OPEN
CLOSING
=
State
.
CLOSING
CLOSED
=
State
.
CLOSED
SEND_EOF
=
b
"
"
"
"
"
Sentinel
signaling
that
the
TCP
connection
must
be
half
-
closed
.
"
"
"
class
Connection
:
    
"
"
"
    
Sans
-
I
/
O
implementation
of
a
WebSocket
connection
.
    
Args
:
        
side
:
:
attr
:
~
Side
.
CLIENT
or
:
attr
:
~
Side
.
SERVER
.
        
state
:
initial
state
of
the
WebSocket
connection
.
        
max_size
:
maximum
size
of
incoming
messages
in
bytes
;
            
:
obj
:
None
to
disable
the
limit
.
        
logger
:
logger
for
this
connection
;
depending
on
side
            
defaults
to
logging
.
getLogger
(
"
websockets
.
client
"
)
            
or
logging
.
getLogger
(
"
websockets
.
server
"
)
;
            
see
the
:
doc
:
logging
guide
<
.
.
/
topics
/
logging
>
for
details
.
    
"
"
"
    
def
__init__
(
        
self
        
side
:
Side
        
state
:
State
=
OPEN
        
max_size
:
Optional
[
int
]
=
2
*
*
20
        
logger
:
Optional
[
LoggerLike
]
=
None
    
)
-
>
None
:
        
self
.
id
:
uuid
.
UUID
=
uuid
.
uuid4
(
)
        
"
"
"
Unique
identifier
of
the
connection
.
Useful
in
logs
.
"
"
"
        
if
logger
is
None
:
            
logger
=
logging
.
getLogger
(
f
"
websockets
.
{
side
.
name
.
lower
(
)
}
"
)
        
self
.
logger
:
LoggerLike
=
logger
        
"
"
"
Logger
for
this
connection
.
"
"
"
        
self
.
debug
=
logger
.
isEnabledFor
(
logging
.
DEBUG
)
        
self
.
side
=
side
        
self
.
state
=
state
        
self
.
max_size
=
max_size
        
self
.
cur_size
:
Optional
[
int
]
=
None
        
self
.
expect_continuation_frame
=
False
        
self
.
origin
:
Optional
[
Origin
]
=
None
        
self
.
extensions
:
List
[
Extension
]
=
[
]
        
self
.
subprotocol
:
Optional
[
Subprotocol
]
=
None
        
self
.
close_rcvd
:
Optional
[
Close
]
=
None
        
self
.
close_sent
:
Optional
[
Close
]
=
None
        
self
.
close_rcvd_then_sent
:
Optional
[
bool
]
=
None
        
self
.
handshake_exc
:
Optional
[
Exception
]
=
None
        
"
"
"
        
Exception
to
raise
if
the
opening
handshake
failed
.
        
:
obj
:
None
if
the
opening
handshake
succeeded
.
        
"
"
"
        
self
.
eof_sent
=
False
        
self
.
reader
=
StreamReader
(
)
        
self
.
events
:
List
[
Event
]
=
[
]
        
self
.
writes
:
List
[
bytes
]
=
[
]
        
self
.
parser
=
self
.
parse
(
)
        
next
(
self
.
parser
)
        
self
.
parser_exc
:
Optional
[
Exception
]
=
None
    
property
    
def
state
(
self
)
-
>
State
:
        
"
"
"
        
WebSocket
connection
state
.
        
Defined
in
4
.
1
4
.
2
7
.
1
.
3
and
7
.
1
.
4
of
:
rfc
:
6455
.
        
"
"
"
        
return
self
.
_state
    
state
.
setter
    
def
state
(
self
state
:
State
)
-
>
None
:
        
if
self
.
debug
:
            
self
.
logger
.
debug
(
"
=
connection
is
%
s
"
state
.
name
)
        
self
.
_state
=
state
    
property
    
def
close_code
(
self
)
-
>
Optional
[
int
]
:
        
"
"
"
        
WebSocket
close
code
_
.
        
.
.
_WebSocket
close
code
:
            
https
:
/
/
www
.
rfc
-
editor
.
org
/
rfc
/
rfc6455
.
html
#
section
-
7
.
1
.
5
        
:
obj
:
None
if
the
connection
isn
'
t
closed
yet
.
        
"
"
"
        
if
self
.
state
is
not
CLOSED
:
            
return
None
        
elif
self
.
close_rcvd
is
None
:
            
return
1006
        
else
:
            
return
self
.
close_rcvd
.
code
    
property
    
def
close_reason
(
self
)
-
>
Optional
[
str
]
:
        
"
"
"
        
WebSocket
close
reason
_
.
        
.
.
_WebSocket
close
reason
:
            
https
:
/
/
www
.
rfc
-
editor
.
org
/
rfc
/
rfc6455
.
html
#
section
-
7
.
1
.
6
        
:
obj
:
None
if
the
connection
isn
'
t
closed
yet
.
        
"
"
"
        
if
self
.
state
is
not
CLOSED
:
            
return
None
        
elif
self
.
close_rcvd
is
None
:
            
return
"
"
        
else
:
            
return
self
.
close_rcvd
.
reason
    
property
    
def
close_exc
(
self
)
-
>
ConnectionClosed
:
        
"
"
"
        
Exception
to
raise
when
trying
to
interact
with
a
closed
connection
.
        
Don
'
t
raise
this
exception
while
the
connection
:
attr
:
state
        
is
:
attr
:
~
websockets
.
connection
.
State
.
CLOSING
;
wait
until
        
it
'
s
:
attr
:
~
websockets
.
connection
.
State
.
CLOSED
.
        
Indeed
the
exception
includes
the
close
code
and
reason
which
are
        
known
only
once
the
connection
is
closed
.
        
Raises
:
            
AssertionError
:
if
the
connection
isn
'
t
closed
yet
.
        
"
"
"
        
assert
self
.
state
is
CLOSED
"
connection
isn
'
t
closed
yet
"
        
exc_type
:
Type
[
ConnectionClosed
]
        
if
(
            
self
.
close_rcvd
is
not
None
            
and
self
.
close_sent
is
not
None
            
and
self
.
close_rcvd
.
code
in
OK_CLOSE_CODES
            
and
self
.
close_sent
.
code
in
OK_CLOSE_CODES
        
)
:
            
exc_type
=
ConnectionClosedOK
        
else
:
            
exc_type
=
ConnectionClosedError
        
exc
:
ConnectionClosed
=
exc_type
(
            
self
.
close_rcvd
            
self
.
close_sent
            
self
.
close_rcvd_then_sent
        
)
        
exc
.
__cause__
=
self
.
parser_exc
        
return
exc
    
def
receive_data
(
self
data
:
bytes
)
-
>
None
:
        
"
"
"
        
Receive
data
from
the
network
.
        
After
calling
this
method
:
        
-
You
must
call
:
meth
:
data_to_send
and
send
this
data
to
the
network
.
        
-
You
should
call
:
meth
:
events_received
and
process
resulting
events
.
        
Raises
:
            
EOFError
:
if
:
meth
:
receive_eof
was
called
earlier
.
        
"
"
"
        
self
.
reader
.
feed_data
(
data
)
        
next
(
self
.
parser
)
    
def
receive_eof
(
self
)
-
>
None
:
        
"
"
"
        
Receive
the
end
of
the
data
stream
from
the
network
.
        
After
calling
this
method
:
        
-
You
must
call
:
meth
:
data_to_send
and
send
this
data
to
the
network
.
        
-
You
aren
'
t
expected
to
call
:
meth
:
events_received
;
it
won
'
t
return
          
any
new
events
.
        
Raises
:
            
EOFError
:
if
:
meth
:
receive_eof
was
called
earlier
.
        
"
"
"
        
self
.
reader
.
feed_eof
(
)
        
next
(
self
.
parser
)
    
def
send_continuation
(
self
data
:
bytes
fin
:
bool
)
-
>
None
:
        
"
"
"
        
Send
a
Continuation
frame
_
.
        
.
.
_Continuation
frame
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
html
/
rfc6455
#
section
-
5
.
6
        
Parameters
:
            
data
:
payload
containing
the
same
kind
of
data
                
as
the
initial
frame
.
            
fin
:
FIN
bit
;
set
it
to
:
obj
:
True
if
this
is
the
last
frame
                
of
a
fragmented
message
and
to
:
obj
:
False
otherwise
.
        
Raises
:
            
ProtocolError
:
if
a
fragmented
message
isn
'
t
in
progress
.
        
"
"
"
        
if
not
self
.
expect_continuation_frame
:
            
raise
ProtocolError
(
"
unexpected
continuation
frame
"
)
        
self
.
expect_continuation_frame
=
not
fin
        
self
.
send_frame
(
Frame
(
OP_CONT
data
fin
)
)
    
def
send_text
(
self
data
:
bytes
fin
:
bool
=
True
)
-
>
None
:
        
"
"
"
        
Send
a
Text
frame
_
.
        
.
.
_Text
frame
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
html
/
rfc6455
#
section
-
5
.
6
        
Parameters
:
            
data
:
payload
containing
text
encoded
with
UTF
-
8
.
            
fin
:
FIN
bit
;
set
it
to
:
obj
:
False
if
this
is
the
first
frame
of
                
a
fragmented
message
.
        
Raises
:
            
ProtocolError
:
if
a
fragmented
message
is
in
progress
.
        
"
"
"
        
if
self
.
expect_continuation_frame
:
            
raise
ProtocolError
(
"
expected
a
continuation
frame
"
)
        
self
.
expect_continuation_frame
=
not
fin
        
self
.
send_frame
(
Frame
(
OP_TEXT
data
fin
)
)
    
def
send_binary
(
self
data
:
bytes
fin
:
bool
=
True
)
-
>
None
:
        
"
"
"
        
Send
a
Binary
frame
_
.
        
.
.
_Binary
frame
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
html
/
rfc6455
#
section
-
5
.
6
        
Parameters
:
            
data
:
payload
containing
arbitrary
binary
data
.
            
fin
:
FIN
bit
;
set
it
to
:
obj
:
False
if
this
is
the
first
frame
of
                
a
fragmented
message
.
        
Raises
:
            
ProtocolError
:
if
a
fragmented
message
is
in
progress
.
        
"
"
"
        
if
self
.
expect_continuation_frame
:
            
raise
ProtocolError
(
"
expected
a
continuation
frame
"
)
        
self
.
expect_continuation_frame
=
not
fin
        
self
.
send_frame
(
Frame
(
OP_BINARY
data
fin
)
)
    
def
send_close
(
self
code
:
Optional
[
int
]
=
None
reason
:
str
=
"
"
)
-
>
None
:
        
"
"
"
        
Send
a
Close
frame
_
.
        
.
.
_Close
frame
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
html
/
rfc6455
#
section
-
5
.
5
.
1
        
Parameters
:
            
code
:
close
code
.
            
reason
:
close
reason
.
        
Raises
:
            
ProtocolError
:
if
a
fragmented
message
is
being
sent
if
the
code
                
isn
'
t
valid
or
if
a
reason
is
provided
without
a
code
        
"
"
"
        
if
self
.
expect_continuation_frame
:
            
raise
ProtocolError
(
"
expected
a
continuation
frame
"
)
        
if
code
is
None
:
            
if
reason
!
=
"
"
:
                
raise
ProtocolError
(
"
cannot
send
a
reason
without
a
code
"
)
            
close
=
Close
(
1005
"
"
)
            
data
=
b
"
"
        
else
:
            
close
=
Close
(
code
reason
)
            
data
=
close
.
serialize
(
)
        
self
.
send_frame
(
Frame
(
OP_CLOSE
data
)
)
        
self
.
close_sent
=
close
        
self
.
state
=
CLOSING
    
def
send_ping
(
self
data
:
bytes
)
-
>
None
:
        
"
"
"
        
Send
a
Ping
frame
_
.
        
.
.
_Ping
frame
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
html
/
rfc6455
#
section
-
5
.
5
.
2
        
Parameters
:
            
data
:
payload
containing
arbitrary
binary
data
.
        
"
"
"
        
self
.
send_frame
(
Frame
(
OP_PING
data
)
)
    
def
send_pong
(
self
data
:
bytes
)
-
>
None
:
        
"
"
"
        
Send
a
Pong
frame
_
.
        
.
.
_Pong
frame
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
html
/
rfc6455
#
section
-
5
.
5
.
3
        
Parameters
:
            
data
:
payload
containing
arbitrary
binary
data
.
        
"
"
"
        
self
.
send_frame
(
Frame
(
OP_PONG
data
)
)
    
def
fail
(
self
code
:
int
reason
:
str
=
"
"
)
-
>
None
:
        
"
"
"
        
Fail
the
WebSocket
connection
_
.
        
.
.
_Fail
the
WebSocket
connection
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
html
/
rfc6455
#
section
-
7
.
1
.
7
        
Parameters
:
            
code
:
close
code
            
reason
:
close
reason
        
Raises
:
            
ProtocolError
:
if
the
code
isn
'
t
valid
.
        
"
"
"
        
if
self
.
state
is
OPEN
:
            
if
code
!
=
1006
:
                
close
=
Close
(
code
reason
)
                
data
=
close
.
serialize
(
)
                
self
.
send_frame
(
Frame
(
OP_CLOSE
data
)
)
                
self
.
close_sent
=
close
                
self
.
state
=
CLOSING
        
if
self
.
side
is
SERVER
and
not
self
.
eof_sent
:
            
self
.
send_eof
(
)
        
self
.
parser
=
self
.
discard
(
)
        
next
(
self
.
parser
)
    
def
events_received
(
self
)
-
>
List
[
Event
]
:
        
"
"
"
        
Fetch
events
generated
from
data
received
from
the
network
.
        
Call
this
method
immediately
after
any
of
the
receive_
*
(
)
methods
.
        
Process
resulting
events
likely
by
passing
them
to
the
application
.
        
Returns
:
            
List
[
Event
]
:
Events
read
from
the
connection
.
        
"
"
"
        
events
self
.
events
=
self
.
events
[
]
        
return
events
    
def
data_to_send
(
self
)
-
>
List
[
bytes
]
:
        
"
"
"
        
Obtain
data
to
send
to
the
network
.
        
Call
this
method
immediately
after
any
of
the
receive_
*
(
)
        
send_
*
(
)
or
:
meth
:
fail
methods
.
        
Write
resulting
data
to
the
connection
.
        
The
empty
bytestring
:
data
:
~
websockets
.
connection
.
SEND_EOF
signals
        
the
end
of
the
data
stream
.
When
you
receive
it
half
-
close
the
TCP
        
connection
.
        
Returns
:
            
List
[
bytes
]
:
Data
to
write
to
the
connection
.
        
"
"
"
        
writes
self
.
writes
=
self
.
writes
[
]
        
return
writes
    
def
close_expected
(
self
)
-
>
bool
:
        
"
"
"
        
Tell
if
the
TCP
connection
is
expected
to
close
soon
.
        
Call
this
method
immediately
after
any
of
the
receive_
*
(
)
or
        
:
meth
:
fail
methods
.
        
If
it
returns
:
obj
:
True
schedule
closing
the
TCP
connection
after
a
        
short
timeout
if
the
other
side
hasn
'
t
already
closed
it
.
        
Returns
:
            
bool
:
Whether
the
TCP
connection
is
expected
to
close
soon
.
        
"
"
"
        
return
self
.
state
is
CLOSING
or
self
.
handshake_exc
is
not
None
    
def
parse
(
self
)
-
>
Generator
[
None
None
None
]
:
        
"
"
"
        
Parse
incoming
data
into
frames
.
        
:
meth
:
receive_data
and
:
meth
:
receive_eof
run
this
generator
        
coroutine
until
it
needs
more
data
or
reaches
EOF
.
        
"
"
"
        
try
:
            
while
True
:
                
if
(
yield
from
self
.
reader
.
at_eof
(
)
)
:
                    
if
self
.
debug
:
                        
self
.
logger
.
debug
(
"
<
EOF
"
)
                    
raise
EOFError
(
"
unexpected
end
of
stream
"
)
                
if
self
.
max_size
is
None
:
                    
max_size
=
None
                
elif
self
.
cur_size
is
None
:
                    
max_size
=
self
.
max_size
                
else
:
                    
max_size
=
self
.
max_size
-
self
.
cur_size
                
frame
=
yield
from
Frame
.
parse
(
                    
self
.
reader
.
read_exact
                    
mask
=
self
.
side
is
SERVER
                    
max_size
=
max_size
                    
extensions
=
self
.
extensions
                
)
                
if
self
.
debug
:
                    
self
.
logger
.
debug
(
"
<
%
s
"
frame
)
                
self
.
recv_frame
(
frame
)
        
except
ProtocolError
as
exc
:
            
self
.
fail
(
1002
str
(
exc
)
)
            
self
.
parser_exc
=
exc
        
except
EOFError
as
exc
:
            
self
.
fail
(
1006
str
(
exc
)
)
            
self
.
parser_exc
=
exc
        
except
UnicodeDecodeError
as
exc
:
            
self
.
fail
(
1007
f
"
{
exc
.
reason
}
at
position
{
exc
.
start
}
"
)
            
self
.
parser_exc
=
exc
        
except
PayloadTooBig
as
exc
:
            
self
.
fail
(
1009
str
(
exc
)
)
            
self
.
parser_exc
=
exc
        
except
Exception
as
exc
:
            
self
.
logger
.
error
(
"
parser
failed
"
exc_info
=
True
)
            
self
.
fail
(
1011
)
            
self
.
parser_exc
=
exc
        
yield
        
raise
AssertionError
(
"
parse
(
)
shouldn
'
t
step
after
error
"
)
    
def
discard
(
self
)
-
>
Generator
[
None
None
None
]
:
        
"
"
"
        
Discard
incoming
data
.
        
This
coroutine
replaces
:
meth
:
parse
:
        
-
after
receiving
a
close
frame
during
a
normal
closure
(
1
.
4
)
;
        
-
after
sending
a
close
frame
during
an
abnormal
closure
(
7
.
1
.
7
)
.
        
"
"
"
        
assert
(
self
.
side
is
SERVER
)
=
=
(
self
.
eof_sent
)
        
while
not
(
yield
from
self
.
reader
.
at_eof
(
)
)
:
            
self
.
reader
.
discard
(
)
        
if
self
.
debug
:
            
self
.
logger
.
debug
(
"
<
EOF
"
)
        
if
self
.
side
is
CLIENT
:
            
self
.
send_eof
(
)
        
self
.
state
=
CLOSED
        
yield
        
raise
AssertionError
(
"
discard
(
)
shouldn
'
t
step
after
EOF
"
)
    
def
recv_frame
(
self
frame
:
Frame
)
-
>
None
:
        
"
"
"
        
Process
an
incoming
frame
.
        
"
"
"
        
if
frame
.
opcode
is
OP_TEXT
or
frame
.
opcode
is
OP_BINARY
:
            
if
self
.
cur_size
is
not
None
:
                
raise
ProtocolError
(
"
expected
a
continuation
frame
"
)
            
if
frame
.
fin
:
                
self
.
cur_size
=
None
            
else
:
                
self
.
cur_size
=
len
(
frame
.
data
)
        
elif
frame
.
opcode
is
OP_CONT
:
            
if
self
.
cur_size
is
None
:
                
raise
ProtocolError
(
"
unexpected
continuation
frame
"
)
            
if
frame
.
fin
:
                
self
.
cur_size
=
None
            
else
:
                
self
.
cur_size
+
=
len
(
frame
.
data
)
        
elif
frame
.
opcode
is
OP_PING
:
            
pong_frame
=
Frame
(
OP_PONG
frame
.
data
)
            
self
.
send_frame
(
pong_frame
)
        
elif
frame
.
opcode
is
OP_PONG
:
            
pass
        
elif
frame
.
opcode
is
OP_CLOSE
:
            
self
.
close_rcvd
=
Close
.
parse
(
frame
.
data
)
            
if
self
.
state
is
CLOSING
:
                
assert
self
.
close_sent
is
not
None
                
self
.
close_rcvd_then_sent
=
False
            
if
self
.
cur_size
is
not
None
:
                
raise
ProtocolError
(
"
incomplete
fragmented
message
"
)
            
if
self
.
state
is
OPEN
:
                
self
.
send_frame
(
Frame
(
OP_CLOSE
frame
.
data
)
)
                
self
.
close_sent
=
self
.
close_rcvd
                
self
.
close_rcvd_then_sent
=
True
                
self
.
state
=
CLOSING
            
if
self
.
side
is
SERVER
:
                
self
.
send_eof
(
)
            
self
.
parser
=
self
.
discard
(
)
            
next
(
self
.
parser
)
        
else
:
            
raise
AssertionError
(
f
"
unexpected
opcode
:
{
frame
.
opcode
:
02x
}
"
)
        
self
.
events
.
append
(
frame
)
    
def
send_frame
(
self
frame
:
Frame
)
-
>
None
:
        
if
self
.
state
is
not
OPEN
:
            
raise
InvalidState
(
                
f
"
cannot
write
to
a
WebSocket
in
the
{
self
.
state
.
name
}
state
"
            
)
        
if
self
.
debug
:
            
self
.
logger
.
debug
(
"
>
%
s
"
frame
)
        
self
.
writes
.
append
(
            
frame
.
serialize
(
mask
=
self
.
side
is
CLIENT
extensions
=
self
.
extensions
)
        
)
    
def
send_eof
(
self
)
-
>
None
:
        
assert
not
self
.
eof_sent
        
self
.
eof_sent
=
True
        
if
self
.
debug
:
            
self
.
logger
.
debug
(
"
>
EOF
"
)
        
self
.
writes
.
append
(
SEND_EOF
)
