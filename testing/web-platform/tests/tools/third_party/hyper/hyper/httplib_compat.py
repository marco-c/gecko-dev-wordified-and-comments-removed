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
hyper
/
httplib_compat
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
This
file
defines
the
publicly
-
accessible
API
for
hyper
.
This
API
also
constitutes
the
abstraction
layer
between
HTTP
/
1
.
1
and
HTTP
/
2
.
This
API
doesn
'
t
currently
work
and
is
a
lower
priority
than
the
HTTP
/
2
stack
at
this
time
.
"
"
"
import
socket
try
:
    
import
http
.
client
as
httplib
except
ImportError
:
    
import
httplib
from
.
compat
import
ssl
from
.
http20
.
tls
import
wrap_socket
try
:
    
support_20
=
ssl
.
HAS_NPN
except
AttributeError
:
    
support_20
=
False
HTTPConnection
=
httplib
.
HTTPConnection
HTTPSConnection
=
httplib
.
HTTPSConnection
if
support_20
:
    
class
HTTPSConnection
(
object
)
:
        
"
"
"
        
An
object
representing
a
single
HTTPS
connection
whether
HTTP
/
1
.
1
or
        
HTTP
/
2
.
        
More
specifically
this
object
represents
an
abstraction
over
the
        
distinction
.
This
object
encapsulates
a
connection
object
for
one
of
        
the
specific
types
of
connection
and
delegates
most
of
the
work
to
        
that
object
.
        
"
"
"
        
def
__init__
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
_original_args
=
args
            
self
.
_original_kwargs
=
kwargs
            
self
.
_sock
=
None
            
self
.
_conn
=
None
            
self
.
_call_queue
=
[
]
        
def
__getattr__
(
self
name
)
:
            
delay_methods
=
[
"
set_tunnel
"
"
set_debuglevel
"
]
            
if
self
.
_conn
is
None
and
name
in
delay_methods
:
                
def
capture
(
obj
*
args
*
*
kwargs
)
:
                    
self
.
_call_queue
.
append
(
(
name
args
kwargs
)
)
                
return
capture
            
elif
self
.
_conn
is
None
:
                
self
.
_delayed_connect
(
)
            
return
getattr
(
self
.
_conn
name
)
        
def
_delayed_connect
(
self
)
:
            
"
"
"
            
Called
when
we
need
to
work
out
what
kind
of
HTTPS
connection
we
'
re
            
actually
going
to
use
.
            
"
"
"
            
tempconn
=
httplib
.
HTTPConnection
(
*
self
.
_original_args
                                              
*
*
self
.
_original_kwargs
)
            
host
=
tempconn
.
host
            
port
=
tempconn
.
port
            
timeout
=
tempconn
.
timeout
            
source_address
=
tempconn
.
source_address
            
sock
=
socket
.
create_connection
(
                
(
host
port
)
                
timeout
                
source_address
            
)
            
sock
=
wrap_socket
(
sock
host
)
            
tempconn
.
sock
=
sock
            
self
.
_sock
=
sock
            
self
.
_conn
=
tempconn
            
return
