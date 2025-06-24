from
__future__
import
absolute_import
import
socket
from
sentry_sdk
import
Hub
from
sentry_sdk
.
_types
import
MYPY
from
sentry_sdk
.
consts
import
OP
from
sentry_sdk
.
integrations
import
Integration
if
MYPY
:
    
from
socket
import
AddressFamily
SocketKind
    
from
typing
import
Tuple
Optional
Union
List
__all__
=
[
"
SocketIntegration
"
]
class
SocketIntegration
(
Integration
)
:
    
identifier
=
"
socket
"
    
staticmethod
    
def
setup_once
(
)
:
        
"
"
"
        
patches
two
of
the
most
used
functions
of
socket
:
create_connection
and
getaddrinfo
(
dns
resolver
)
        
"
"
"
        
_patch_create_connection
(
)
        
_patch_getaddrinfo
(
)
def
_get_span_description
(
host
port
)
:
    
try
:
        
host
=
host
.
decode
(
)
    
except
(
UnicodeDecodeError
AttributeError
)
:
        
pass
    
description
=
"
%
s
:
%
s
"
%
(
host
port
)
    
return
description
def
_patch_create_connection
(
)
:
    
real_create_connection
=
socket
.
create_connection
    
def
create_connection
(
        
address
        
timeout
=
socket
.
_GLOBAL_DEFAULT_TIMEOUT
        
source_address
=
None
    
)
:
        
hub
=
Hub
.
current
        
if
hub
.
get_integration
(
SocketIntegration
)
is
None
:
            
return
real_create_connection
(
                
address
=
address
timeout
=
timeout
source_address
=
source_address
            
)
        
with
hub
.
start_span
(
            
op
=
OP
.
SOCKET_CONNECTION
            
description
=
_get_span_description
(
address
[
0
]
address
[
1
]
)
        
)
as
span
:
            
span
.
set_data
(
"
address
"
address
)
            
span
.
set_data
(
"
timeout
"
timeout
)
            
span
.
set_data
(
"
source_address
"
source_address
)
            
return
real_create_connection
(
                
address
=
address
timeout
=
timeout
source_address
=
source_address
            
)
    
socket
.
create_connection
=
create_connection
def
_patch_getaddrinfo
(
)
:
    
real_getaddrinfo
=
socket
.
getaddrinfo
    
def
getaddrinfo
(
host
port
family
=
0
type
=
0
proto
=
0
flags
=
0
)
:
        
hub
=
Hub
.
current
        
if
hub
.
get_integration
(
SocketIntegration
)
is
None
:
            
return
real_getaddrinfo
(
host
port
family
type
proto
flags
)
        
with
hub
.
start_span
(
            
op
=
OP
.
SOCKET_DNS
description
=
_get_span_description
(
host
port
)
        
)
as
span
:
            
span
.
set_data
(
"
host
"
host
)
            
span
.
set_data
(
"
port
"
port
)
            
return
real_getaddrinfo
(
host
port
family
type
proto
flags
)
    
socket
.
getaddrinfo
=
getaddrinfo
