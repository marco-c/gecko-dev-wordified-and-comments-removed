"
"
"
Common
functions
and
exceptions
used
by
WebSocket
opening
handshake
processors
.
"
"
"
from
__future__
import
absolute_import
from
mod_pywebsocket
import
common
from
mod_pywebsocket
import
http_header_util
from
mod_pywebsocket
.
extensions
import
get_extension_processor
from
mod_pywebsocket
.
stream
import
StreamOptions
from
mod_pywebsocket
.
stream
import
Stream
from
mod_pywebsocket
import
util
from
six
.
moves
import
map
from
six
.
moves
import
range
_VERSION_LATEST
=
common
.
VERSION_HYBI_LATEST
_VERSION_LATEST_STRING
=
str
(
_VERSION_LATEST
)
_SUPPORTED_VERSIONS
=
[
    
_VERSION_LATEST
]
class
AbortedByUserException
(
Exception
)
:
    
"
"
"
Exception
for
aborting
a
connection
intentionally
.
    
If
this
exception
is
raised
in
do_extra_handshake
handler
the
connection
    
will
be
abandoned
.
No
other
WebSocket
or
HTTP
(
S
)
handler
will
be
invoked
.
    
If
this
exception
is
raised
in
transfer_data_handler
the
connection
will
    
be
closed
without
closing
handshake
.
No
other
WebSocket
or
HTTP
(
S
)
handler
    
will
be
invoked
.
    
"
"
"
    
pass
class
HandshakeException
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
an
error
occurred
while
processing
    
WebSocket
initial
handshake
.
    
"
"
"
    
def
__init__
(
self
name
status
=
None
)
:
        
super
(
HandshakeException
self
)
.
__init__
(
name
)
        
self
.
status
=
status
class
VersionException
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
version
of
client
request
does
not
    
match
with
version
the
server
supports
.
    
"
"
"
    
def
__init__
(
self
name
supported_versions
=
'
'
)
:
        
"
"
"
Construct
an
instance
.
        
Args
:
            
supported_version
:
a
str
object
to
show
supported
hybi
versions
.
                               
(
e
.
g
.
'
13
'
)
        
"
"
"
        
super
(
VersionException
self
)
.
__init__
(
name
)
        
self
.
supported_versions
=
supported_versions
def
get_default_port
(
is_secure
)
:
    
if
is_secure
:
        
return
common
.
DEFAULT_WEB_SOCKET_SECURE_PORT
    
else
:
        
return
common
.
DEFAULT_WEB_SOCKET_PORT
def
validate_subprotocol
(
subprotocol
)
:
    
"
"
"
Validate
a
value
in
the
Sec
-
WebSocket
-
Protocol
field
.
    
See
the
Section
4
.
1
.
4
.
2
.
2
.
and
4
.
3
.
of
RFC
6455
.
    
"
"
"
    
if
not
subprotocol
:
        
raise
HandshakeException
(
'
Invalid
subprotocol
name
:
empty
'
)
    
state
=
http_header_util
.
ParsingState
(
subprotocol
)
    
token
=
http_header_util
.
consume_token
(
state
)
    
rest
=
http_header_util
.
peek
(
state
)
    
if
rest
is
not
None
:
        
raise
HandshakeException
(
'
Invalid
non
-
token
string
in
subprotocol
'
                                 
'
name
:
%
r
'
%
rest
)
def
parse_host_header
(
request
)
:
    
fields
=
request
.
headers_in
[
common
.
HOST_HEADER
]
.
split
(
'
:
'
1
)
    
if
len
(
fields
)
=
=
1
:
        
return
fields
[
0
]
get_default_port
(
request
.
is_https
(
)
)
    
try
:
        
return
fields
[
0
]
int
(
fields
[
1
]
)
    
except
ValueError
as
e
:
        
raise
HandshakeException
(
'
Invalid
port
number
format
:
%
r
'
%
e
)
def
get_mandatory_header
(
request
key
)
:
    
value
=
request
.
headers_in
.
get
(
key
)
    
if
value
is
None
:
        
raise
HandshakeException
(
'
Header
%
s
is
not
defined
'
%
key
)
    
return
value
def
validate_mandatory_header
(
request
key
expected_value
fail_status
=
None
)
:
    
value
=
get_mandatory_header
(
request
key
)
    
if
value
.
lower
(
)
!
=
expected_value
.
lower
(
)
:
        
raise
HandshakeException
(
            
'
Expected
%
r
for
header
%
s
but
found
%
r
(
case
-
insensitive
)
'
%
            
(
expected_value
key
value
)
            
status
=
fail_status
)
def
parse_token_list
(
data
)
:
    
"
"
"
Parses
a
header
value
which
follows
1
#
token
and
returns
parsed
elements
    
as
a
list
of
strings
.
    
Leading
LWSes
must
be
trimmed
.
    
"
"
"
    
state
=
http_header_util
.
ParsingState
(
data
)
    
token_list
=
[
]
    
while
True
:
        
token
=
http_header_util
.
consume_token
(
state
)
        
if
token
is
not
None
:
            
token_list
.
append
(
token
)
        
http_header_util
.
consume_lwses
(
state
)
        
if
http_header_util
.
peek
(
state
)
is
None
:
            
break
        
if
not
http_header_util
.
consume_string
(
state
'
'
)
:
            
raise
HandshakeException
(
'
Expected
a
comma
but
found
%
r
'
%
                                     
http_header_util
.
peek
(
state
)
)
        
http_header_util
.
consume_lwses
(
state
)
    
if
len
(
token_list
)
=
=
0
:
        
raise
HandshakeException
(
'
No
valid
token
found
'
)
    
return
token_list
class
HandshakerBase
(
object
)
:
    
def
__init__
(
self
request
dispatcher
)
:
        
self
.
_logger
=
util
.
get_class_logger
(
self
)
        
self
.
_request
=
request
        
self
.
_dispatcher
=
dispatcher
    
"
"
"
subclasses
must
implement
the
five
following
methods
"
"
"
    
def
_protocol_rfc
(
self
)
:
        
"
"
"
Return
the
name
of
the
RFC
that
the
handshake
class
is
implementing
.
        
"
"
"
        
raise
AssertionError
(
"
subclasses
should
implement
this
method
"
)
    
def
_transform_header
(
self
header
)
:
        
"
"
"
        
:
param
header
:
header
name
        
transform
the
header
name
if
needed
.
For
example
HTTP
/
2
subclass
will
        
return
the
name
of
the
header
in
lower
case
.
        
"
"
"
        
raise
AssertionError
(
"
subclasses
should
implement
this
method
"
)
    
def
_validate_request
(
self
)
:
        
"
"
"
validate
that
all
the
mandatory
fields
are
set
"
"
"
        
raise
AssertionError
(
"
subclasses
should
implement
this
method
"
)
    
def
_set_accept
(
self
)
:
        
"
"
"
Computes
accept
value
based
on
Sec
-
WebSocket
-
Accept
if
needed
.
"
"
"
        
raise
AssertionError
(
"
subclasses
should
implement
this
method
"
)
    
def
_send_handshake
(
self
)
:
        
"
"
"
Prepare
and
send
the
response
after
it
has
been
parsed
and
processed
.
        
"
"
"
        
raise
AssertionError
(
"
subclasses
should
implement
this
method
"
)
    
def
do_handshake
(
self
)
:
        
self
.
_request
.
ws_close_code
=
None
        
self
.
_request
.
ws_close_reason
=
None
        
self
.
_validate_request
(
)
        
self
.
_request
.
ws_resource
=
self
.
_request
.
uri
        
self
.
_request
.
ws_version
=
self
.
_check_version
(
)
        
try
:
            
self
.
_get_origin
(
)
            
self
.
_set_protocol
(
)
            
self
.
_parse_extensions
(
)
            
self
.
_set_accept
(
)
            
self
.
_logger
.
debug
(
'
Protocol
version
is
'
+
self
.
_protocol_rfc
(
)
)
            
self
.
_request
.
ws_extension_processors
=
self
.
_get_extension_processors_requested
(
            
)
            
self
.
_request
.
extra_headers
=
[
]
            
self
.
_dispatcher
.
do_extra_handshake
(
self
.
_request
)
            
stream_options
=
StreamOptions
(
)
            
self
.
_process_extensions
(
stream_options
)
            
self
.
_request
.
ws_stream
=
Stream
(
self
.
_request
stream_options
)
            
if
self
.
_request
.
ws_requested_protocols
is
not
None
:
                
if
self
.
_request
.
ws_protocol
is
None
:
                    
raise
HandshakeException
(
                        
'
do_extra_handshake
must
choose
one
subprotocol
from
'
                        
'
ws_requested_protocols
and
set
it
to
ws_protocol
'
)
                
validate_subprotocol
(
self
.
_request
.
ws_protocol
)
                
self
.
_logger
.
debug
(
'
Subprotocol
accepted
:
%
r
'
                                   
self
.
_request
.
ws_protocol
)
            
else
:
                
if
self
.
_request
.
ws_protocol
is
not
None
:
                    
raise
HandshakeException
(
                        
'
ws_protocol
must
be
None
when
the
client
didn
\
'
t
'
                        
'
request
any
subprotocol
'
)
            
self
.
_send_handshake
(
)
        
except
HandshakeException
as
e
:
            
if
not
e
.
status
:
                
e
.
status
=
common
.
HTTP_STATUS_BAD_REQUEST
            
raise
e
    
def
_check_version
(
self
)
:
        
sec_websocket_version_header
=
self
.
_transform_header
(
            
common
.
SEC_WEBSOCKET_VERSION_HEADER
)
        
version
=
get_mandatory_header
(
self
.
_request
                                       
sec_websocket_version_header
)
        
if
version
=
=
_VERSION_LATEST_STRING
:
            
return
_VERSION_LATEST
        
if
version
.
find
(
'
'
)
>
=
0
:
            
raise
HandshakeException
(
                
'
Multiple
versions
(
%
r
)
are
not
allowed
for
header
%
s
'
%
                
(
version
sec_websocket_version_header
)
                
status
=
common
.
HTTP_STATUS_BAD_REQUEST
)
        
raise
VersionException
(
'
Unsupported
version
%
r
for
header
%
s
'
%
                               
(
version
sec_websocket_version_header
)
                               
supported_versions
=
'
'
.
join
(
                                   
map
(
str
_SUPPORTED_VERSIONS
)
)
)
    
def
_get_origin
(
self
)
:
        
origin_header
=
self
.
_transform_header
(
common
.
ORIGIN_HEADER
)
        
origin
=
self
.
_request
.
headers_in
.
get
(
origin_header
)
        
if
origin
is
None
:
            
self
.
_logger
.
debug
(
'
Client
request
does
not
have
origin
header
'
)
        
self
.
_request
.
ws_origin
=
origin
    
def
_set_protocol
(
self
)
:
        
self
.
_request
.
ws_protocol
=
None
        
self
.
_request
.
sts
=
None
        
sec_websocket_protocol_header
=
self
.
_transform_header
(
            
common
.
SEC_WEBSOCKET_PROTOCOL_HEADER
)
        
protocol_header
=
self
.
_request
.
headers_in
.
get
(
            
sec_websocket_protocol_header
)
        
if
protocol_header
is
None
:
            
self
.
_request
.
ws_requested_protocols
=
None
            
return
        
self
.
_request
.
ws_requested_protocols
=
parse_token_list
(
            
protocol_header
)
        
self
.
_logger
.
debug
(
'
Subprotocols
requested
:
%
r
'
                           
self
.
_request
.
ws_requested_protocols
)
    
def
_parse_extensions
(
self
)
:
        
sec_websocket_extensions_header
=
self
.
_transform_header
(
            
common
.
SEC_WEBSOCKET_EXTENSIONS_HEADER
)
        
extensions_header
=
self
.
_request
.
headers_in
.
get
(
            
sec_websocket_extensions_header
)
        
if
not
extensions_header
:
            
self
.
_request
.
ws_requested_extensions
=
None
            
return
        
try
:
            
self
.
_request
.
ws_requested_extensions
=
common
.
parse_extensions
(
                
extensions_header
)
        
except
common
.
ExtensionParsingException
as
e
:
            
raise
HandshakeException
(
                
'
Failed
to
parse
sec
-
websocket
-
extensions
header
:
%
r
'
%
e
)
        
self
.
_logger
.
debug
(
            
'
Extensions
requested
:
%
r
'
            
list
(
                
map
(
common
.
ExtensionParameter
.
name
                    
self
.
_request
.
ws_requested_extensions
)
)
)
    
def
_get_extension_processors_requested
(
self
)
:
        
processors
=
[
]
        
if
self
.
_request
.
ws_requested_extensions
is
not
None
:
            
for
extension_request
in
self
.
_request
.
ws_requested_extensions
:
                
processor
=
get_extension_processor
(
extension_request
)
                
if
processor
is
not
None
:
                    
processors
.
append
(
processor
)
        
return
processors
    
def
_process_extensions
(
self
stream_options
)
:
        
processors
=
[
            
processor
for
processor
in
self
.
_request
.
ws_extension_processors
            
if
processor
is
not
None
        
]
        
for
processor
in
reversed
(
processors
)
:
            
if
processor
.
is_active
(
)
:
                
processor
.
check_consistency_with_other_processors
(
processors
)
        
processors
=
[
            
processor
for
processor
in
processors
if
processor
.
is_active
(
)
        
]
        
accepted_extensions
=
[
]
        
for
index
processor
in
enumerate
(
processors
)
:
            
if
not
processor
.
is_active
(
)
:
                
continue
            
extension_response
=
processor
.
get_extension_response
(
)
            
if
extension_response
is
None
:
                
continue
            
accepted_extensions
.
append
(
extension_response
)
            
processor
.
setup_stream_options
(
stream_options
)
            
for
j
in
range
(
index
+
1
len
(
processors
)
)
:
                
processors
[
j
]
.
set_active
(
False
)
        
if
len
(
accepted_extensions
)
>
0
:
            
self
.
_request
.
ws_extensions
=
accepted_extensions
            
self
.
_logger
.
debug
(
                
'
Extensions
accepted
:
%
r
'
                
list
(
map
(
common
.
ExtensionParameter
.
name
accepted_extensions
)
)
)
        
else
:
            
self
.
_request
.
ws_extensions
=
None
