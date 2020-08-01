"
"
"
Stream
Exceptions
.
"
"
"
class
ConnectionTerminatedException
(
Exception
)
:
    
"
"
"
This
exception
will
be
raised
when
a
connection
is
terminated
    
unexpectedly
.
    
"
"
"
    
pass
class
InvalidFrameException
(
ConnectionTerminatedException
)
:
    
"
"
"
This
exception
will
be
raised
when
we
received
an
invalid
frame
we
    
cannot
parse
.
    
"
"
"
    
pass
class
BadOperationException
(
Exception
)
:
    
"
"
"
This
exception
will
be
raised
when
send_message
(
)
is
called
on
    
server
-
terminated
connection
or
receive_message
(
)
is
called
on
    
client
-
terminated
connection
.
    
"
"
"
    
pass
class
UnsupportedFrameException
(
Exception
)
:
    
"
"
"
This
exception
will
be
raised
when
we
receive
a
frame
with
flag
opcode
    
we
cannot
handle
.
Handlers
can
just
catch
and
ignore
this
exception
and
    
call
receive_message
(
)
again
to
continue
processing
the
next
frame
.
    
"
"
"
    
pass
class
InvalidUTF8Exception
(
Exception
)
:
    
"
"
"
This
exception
will
be
raised
when
we
receive
a
text
frame
which
    
contains
invalid
UTF
-
8
strings
.
    
"
"
"
    
pass
