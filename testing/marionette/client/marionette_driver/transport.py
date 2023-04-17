from
__future__
import
absolute_import
import
json
import
socket
import
sys
import
time
from
threading
import
Lock
import
six
class
SocketTimeout
(
object
)
:
    
def
__init__
(
self
socket_ctx
timeout
)
:
        
self
.
socket_ctx
=
socket_ctx
        
self
.
timeout
=
timeout
        
self
.
old_timeout
=
None
    
def
__enter__
(
self
)
:
        
self
.
old_timeout
=
self
.
socket_ctx
.
socket_timeout
        
self
.
socket_ctx
.
socket_timeout
=
self
.
timeout
    
def
__exit__
(
self
*
args
*
*
kwargs
)
:
        
self
.
socket_ctx
.
socket_timeout
=
self
.
old_timeout
class
Message
(
object
)
:
    
def
__init__
(
self
msgid
)
:
        
self
.
id
=
msgid
    
def
__eq__
(
self
other
)
:
        
return
self
.
id
=
=
other
.
id
    
def
__ne__
(
self
other
)
:
        
return
not
self
.
__eq__
(
other
)
    
def
__hash__
(
self
)
:
        
return
hash
(
self
.
id
)
class
Command
(
Message
)
:
    
TYPE
=
0
    
def
__init__
(
self
msgid
name
params
)
:
        
Message
.
__init__
(
self
msgid
)
        
self
.
name
=
name
        
self
.
params
=
params
    
def
__str__
(
self
)
:
        
return
"
<
Command
id
=
{
0
}
name
=
{
1
}
params
=
{
2
}
>
"
.
format
(
            
self
.
id
self
.
name
self
.
params
        
)
    
def
to_msg
(
self
)
:
        
msg
=
[
Command
.
TYPE
self
.
id
self
.
name
self
.
params
]
        
return
json
.
dumps
(
msg
)
    
staticmethod
    
def
from_msg
(
data
)
:
        
assert
data
[
0
]
=
=
Command
.
TYPE
        
cmd
=
Command
(
data
[
1
]
data
[
2
]
data
[
3
]
)
        
return
cmd
class
Response
(
Message
)
:
    
TYPE
=
1
    
def
__init__
(
self
msgid
error
result
)
:
        
Message
.
__init__
(
self
msgid
)
        
self
.
error
=
error
        
self
.
result
=
result
    
def
__str__
(
self
)
:
        
return
"
<
Response
id
=
{
0
}
error
=
{
1
}
result
=
{
2
}
>
"
.
format
(
            
self
.
id
self
.
error
self
.
result
        
)
    
def
to_msg
(
self
)
:
        
msg
=
[
Response
.
TYPE
self
.
id
self
.
error
self
.
result
]
        
return
json
.
dumps
(
msg
)
    
staticmethod
    
def
from_msg
(
data
)
:
        
assert
data
[
0
]
=
=
Response
.
TYPE
        
return
Response
(
data
[
1
]
data
[
2
]
data
[
3
]
)
class
SocketContext
(
object
)
:
    
"
"
"
Object
that
guards
access
to
a
socket
via
a
lock
.
    
The
socket
must
be
accessed
using
this
object
as
a
context
manager
;
    
access
to
the
socket
outside
of
a
context
will
bypass
the
lock
.
"
"
"
    
def
__init__
(
self
host
port
timeout
)
:
        
self
.
lock
=
Lock
(
)
        
self
.
_sock
=
socket
.
socket
(
socket
.
AF_INET
socket
.
SOCK_STREAM
)
        
self
.
_sock
.
settimeout
(
timeout
)
        
self
.
_sock
.
connect
(
(
host
port
)
)
    
property
    
def
socket_timeout
(
self
)
:
        
return
self
.
_sock
.
gettimeout
(
)
    
socket_timeout
.
setter
    
def
socket_timeout
(
self
value
)
:
        
self
.
_sock
.
settimeout
(
value
)
    
def
__enter__
(
self
)
:
        
self
.
lock
.
acquire
(
)
        
return
self
.
_sock
    
def
__exit__
(
self
*
args
*
*
kwargs
)
:
        
self
.
lock
.
release
(
)
class
TcpTransport
(
object
)
:
    
"
"
"
Socket
client
that
communciates
with
Marionette
via
TCP
.
    
It
speaks
the
protocol
of
the
remote
debugger
in
Gecko
in
which
    
messages
are
always
preceded
by
the
message
length
and
a
colon
e
.
g
.
:
        
7
:
MESSAGE
    
On
top
of
this
protocol
it
uses
a
Marionette
message
format
that
    
depending
on
the
protocol
level
offered
by
the
remote
server
varies
.
    
Supported
protocol
levels
are
min_protocol_level
and
above
.
    
"
"
"
    
max_packet_length
=
4096
    
min_protocol_level
=
3
    
def
__init__
(
self
host
port
socket_timeout
=
60
.
0
)
:
        
"
"
"
If
socket_timeout
is
0
or
0
.
0
non
-
blocking
socket
mode
        
will
be
used
.
Setting
it
to
1
or
None
disables
timeouts
on
        
socket
operations
altogether
.
        
"
"
"
        
self
.
_socket_context
=
None
        
self
.
host
=
host
        
self
.
port
=
port
        
self
.
_socket_timeout
=
socket_timeout
        
self
.
protocol
=
self
.
min_protocol_level
        
self
.
application_type
=
None
        
self
.
last_id
=
0
        
self
.
expected_response
=
None
    
property
    
def
socket_timeout
(
self
)
:
        
return
self
.
_socket_timeout
    
socket_timeout
.
setter
    
def
socket_timeout
(
self
value
)
:
        
self
.
_socket_timeout
=
value
        
if
self
.
_socket_context
is
not
None
:
            
self
.
_socket_context
.
socket_timeout
=
value
    
def
_unmarshal
(
self
packet
)
:
        
"
"
"
Convert
data
from
bytes
to
a
Message
subtype
        
Message
format
is
[
type
msg_id
body1
body2
]
where
body1
and
body2
depend
        
on
the
message
type
.
        
:
param
packet
:
Bytes
received
over
the
wire
representing
a
complete
message
.
        
"
"
"
        
msg
=
None
        
data
=
json
.
loads
(
packet
)
        
msg_type
=
data
[
0
]
        
if
msg_type
=
=
Command
.
TYPE
:
            
msg
=
Command
.
from_msg
(
data
)
        
elif
msg_type
=
=
Response
.
TYPE
:
            
msg
=
Response
.
from_msg
(
data
)
        
else
:
            
raise
ValueError
(
"
Invalid
message
body
{
!
r
}
"
.
format
(
packet
)
)
        
return
msg
    
def
receive
(
self
unmarshal
=
True
)
:
        
"
"
"
Wait
for
the
next
complete
response
from
the
remote
.
        
Packet
format
is
length
-
prefixed
JSON
:
          
packet
=
digit
+
"
:
"
body
          
digit
=
"
0
"
-
"
9
"
          
body
=
JSON
text
        
:
param
unmarshal
:
Default
is
to
deserialise
the
packet
and
            
return
a
Message
type
.
Setting
this
to
false
will
return
            
the
raw
packet
.
        
"
"
"
        
with
self
.
_socket_context
as
sock
:
            
recv_bytes
=
4
            
length_prefix
=
b
"
"
            
body_length
=
-
1
            
body_received
=
0
            
body_parts
=
[
]
            
now
=
time
.
time
(
)
            
timeout_time
=
(
                
now
+
self
.
socket_timeout
if
self
.
socket_timeout
is
not
None
else
None
            
)
            
while
recv_bytes
>
0
:
                
if
timeout_time
is
not
None
and
time
.
time
(
)
>
timeout_time
:
                    
raise
socket
.
timeout
(
                        
"
Connection
timed
out
after
{
}
s
"
.
format
(
self
.
socket_timeout
)
                    
)
                
try
:
                    
chunk
=
sock
.
recv
(
recv_bytes
)
                
except
OSError
:
                    
continue
                
if
not
chunk
:
                    
raise
socket
.
error
(
"
No
data
received
over
socket
"
)
                
body_part
=
None
                
if
body_length
>
0
:
                    
body_part
=
chunk
                
else
:
                    
parts
=
chunk
.
split
(
b
"
:
"
1
)
                    
length_prefix
+
=
parts
[
0
]
                    
if
len
(
length_prefix
)
>
10
:
                        
raise
ValueError
(
                            
"
Invalid
message
length
:
{
!
r
}
"
.
format
(
length_prefix
)
                        
)
                    
if
len
(
parts
)
=
=
2
:
                        
err
=
None
                        
try
:
                            
body_length
=
int
(
length_prefix
)
                        
except
ValueError
:
                            
err
=
"
expected
an
integer
"
                        
else
:
                            
if
body_length
<
=
0
:
                                
err
=
"
expected
a
positive
integer
"
                            
elif
body_length
>
2
*
*
32
-
1
:
                                
err
=
"
expected
a
32
bit
integer
"
                        
if
err
is
not
None
:
                            
raise
ValueError
(
                                
"
Invalid
message
length
:
{
}
got
{
!
r
}
"
.
format
(
                                    
err
length_prefix
                                
)
                            
)
                        
body_part
=
parts
[
1
]
                
if
body_part
is
not
None
:
                    
body_received
+
=
len
(
body_part
)
                    
body_parts
.
append
(
body_part
)
                    
recv_bytes
=
body_length
-
body_received
            
body
=
b
"
"
.
join
(
body_parts
)
            
if
unmarshal
:
                
msg
=
self
.
_unmarshal
(
body
)
                
self
.
last_id
=
msg
.
id
                
if
isinstance
(
msg
Response
)
and
msg
!
=
self
.
expected_response
:
                    
return
self
.
receive
(
unmarshal
)
                
return
msg
            
return
body
    
def
connect
(
self
)
:
        
"
"
"
Connect
to
the
server
and
process
the
hello
message
we
expect
        
to
receive
in
response
.
        
Returns
a
tuple
of
the
protocol
level
and
the
application
type
.
        
"
"
"
        
try
:
            
self
.
_socket_context
=
SocketContext
(
                
self
.
host
self
.
port
self
.
_socket_timeout
            
)
        
except
Exception
:
            
self
.
_socket_context
=
None
            
raise
        
try
:
            
with
SocketTimeout
(
self
.
_socket_context
60
.
0
)
:
                
raw
=
self
.
receive
(
unmarshal
=
False
)
        
except
socket
.
timeout
:
            
exc_cls
exc
tb
=
sys
.
exc_info
(
)
            
msg
=
"
Connection
attempt
failed
because
no
data
has
been
received
over
the
socket
:
{
}
"
            
six
.
reraise
(
exc_cls
exc_cls
(
msg
.
format
(
exc
)
)
tb
)
        
hello
=
json
.
loads
(
raw
)
        
application_type
=
hello
.
get
(
"
applicationType
"
)
        
protocol
=
hello
.
get
(
"
marionetteProtocol
"
)
        
if
application_type
!
=
"
gecko
"
:
            
raise
ValueError
(
                
"
Application
type
'
{
}
'
is
not
supported
"
.
format
(
application_type
)
            
)
        
if
not
isinstance
(
protocol
int
)
or
protocol
<
self
.
min_protocol_level
:
            
msg
=
"
Earliest
supported
protocol
level
is
'
{
}
'
but
got
'
{
}
'
"
            
raise
ValueError
(
msg
.
format
(
self
.
min_protocol_level
protocol
)
)
        
self
.
application_type
=
application_type
        
self
.
protocol
=
protocol
        
return
(
self
.
protocol
self
.
application_type
)
    
def
send
(
self
obj
)
:
        
"
"
"
Send
message
to
the
remote
server
.
Allowed
input
is
a
        
Message
instance
or
a
JSON
serialisable
object
.
        
"
"
"
        
if
not
self
.
_socket_context
:
            
self
.
connect
(
)
        
if
isinstance
(
obj
Message
)
:
            
data
=
obj
.
to_msg
(
)
            
if
isinstance
(
obj
Command
)
:
                
self
.
expected_response
=
obj
        
else
:
            
data
=
json
.
dumps
(
obj
)
        
data
=
six
.
ensure_binary
(
data
)
        
payload
=
six
.
ensure_binary
(
str
(
len
(
data
)
)
)
+
b
"
:
"
+
data
        
with
self
.
_socket_context
as
sock
:
            
totalsent
=
0
            
while
totalsent
<
len
(
payload
)
:
                
sent
=
sock
.
send
(
payload
[
totalsent
:
]
)
                
if
sent
=
=
0
:
                    
raise
IOError
(
                        
"
Socket
error
after
sending
{
0
}
of
{
1
}
bytes
"
.
format
(
                            
totalsent
len
(
payload
)
                        
)
                    
)
                
else
:
                    
totalsent
+
=
sent
    
def
respond
(
self
obj
)
:
        
"
"
"
Send
a
response
to
a
command
.
This
can
be
an
arbitrary
JSON
        
serialisable
object
or
an
Exception
.
        
"
"
"
        
res
err
=
None
None
        
if
isinstance
(
obj
Exception
)
:
            
err
=
obj
        
else
:
            
res
=
obj
        
msg
=
Response
(
self
.
last_id
err
res
)
        
self
.
send
(
msg
)
        
return
self
.
receive
(
)
    
def
request
(
self
name
params
)
:
        
"
"
"
Sends
a
message
to
the
remote
server
and
waits
for
a
response
        
to
come
back
.
        
"
"
"
        
self
.
last_id
=
self
.
last_id
+
1
        
cmd
=
Command
(
self
.
last_id
name
params
)
        
self
.
send
(
cmd
)
        
return
self
.
receive
(
)
    
def
close
(
self
)
:
        
"
"
"
Close
the
socket
.
        
First
forces
the
socket
to
not
send
data
anymore
and
then
explicitly
        
close
it
to
free
up
its
resources
.
        
See
:
https
:
/
/
docs
.
python
.
org
/
2
/
howto
/
sockets
.
html
#
disconnecting
        
"
"
"
        
if
self
.
_socket_context
:
            
with
self
.
_socket_context
as
sock
:
                
try
:
                    
sock
.
shutdown
(
socket
.
SHUT_RDWR
)
                
except
IOError
as
exc
:
                    
if
exc
.
errno
not
in
(
57
107
)
:
                        
raise
                
if
sock
:
                    
sock
.
close
(
)
                    
self
.
_socket_context
=
None
    
def
__del__
(
self
)
:
        
self
.
close
(
)
