from
__future__
import
annotations
import
typing
from
.
url
import
Url
if
typing
.
TYPE_CHECKING
:
    
from
.
.
connection
import
ProxyConfig
def
connection_requires_http_tunnel
(
    
proxy_url
:
Url
|
None
=
None
    
proxy_config
:
ProxyConfig
|
None
=
None
    
destination_scheme
:
str
|
None
=
None
)
-
>
bool
:
    
"
"
"
    
Returns
True
if
the
connection
requires
an
HTTP
CONNECT
through
the
proxy
.
    
:
param
URL
proxy_url
:
        
URL
of
the
proxy
.
    
:
param
ProxyConfig
proxy_config
:
        
Proxy
configuration
from
poolmanager
.
py
    
:
param
str
destination_scheme
:
        
The
scheme
of
the
destination
.
(
i
.
e
https
http
etc
)
    
"
"
"
    
if
proxy_url
is
None
:
        
return
False
    
if
destination_scheme
=
=
"
http
"
:
        
return
False
    
if
(
        
proxy_url
.
scheme
=
=
"
https
"
        
and
proxy_config
        
and
proxy_config
.
use_forwarding_for_https
    
)
:
        
return
False
    
return
True
