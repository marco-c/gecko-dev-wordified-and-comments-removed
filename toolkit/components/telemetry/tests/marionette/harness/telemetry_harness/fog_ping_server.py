import
json
import
zlib
import
wptserve
.
logger
from
marionette_harness
.
runner
import
httpd
from
mozlog
import
get_default_logger
from
six
.
moves
.
urllib
import
parse
as
urlparse
class
FOGPingServer
(
object
)
:
    
"
"
"
HTTP
server
for
receiving
Firefox
on
Glean
pings
.
"
"
"
    
def
__init__
(
self
server_root
url
)
:
        
self
.
_logger
=
get_default_logger
(
component
=
"
fog_ping_server
"
)
        
try
:
            
wptserve
.
logger
.
set_logger
(
self
.
_logger
)
        
except
Exception
:
            
pass
        
self
.
pings
=
[
]
        
httpd
.
handlers
.
handler
        
def
pings_handler
(
request
response
)
:
            
"
"
"
Handler
for
HTTP
requests
to
the
ping
server
.
"
"
"
            
request_data
=
request
.
body
            
if
request
.
headers
.
get
(
"
Content
-
Encoding
"
)
=
=
b
"
gzip
"
:
                
request_data
=
zlib
.
decompress
(
request_data
zlib
.
MAX_WBITS
|
16
)
            
request_url
=
request
.
route_match
.
copy
(
)
            
self
.
pings
.
append
(
                
{
                    
"
request_url
"
:
request_url
                    
"
payload
"
:
json
.
loads
(
request_data
)
                    
"
debug_tag
"
:
request
.
headers
.
get
(
"
X
-
Debug
-
ID
"
)
                
}
            
)
            
self
.
_logger
.
info
(
                
"
pings_handler
received
'
{
}
'
ping
"
.
format
(
request_url
[
"
doc_type
"
]
)
            
)
            
status_code
=
200
            
content
=
"
OK
"
            
headers
=
[
                
(
"
Content
-
Type
"
"
text
/
plain
"
)
                
(
"
Content
-
Length
"
len
(
content
)
)
            
]
            
return
(
status_code
headers
content
)
        
self
.
_httpd
=
httpd
.
FixtureServer
(
server_root
url
=
url
)
        
self
.
_httpd
.
router
.
register
(
            
"
POST
"
            
"
/
submit
/
{
application_id
}
/
{
doc_type
}
/
{
glean_schema_version
}
/
{
document_id
}
"
            
pings_handler
        
)
    
property
    
def
url
(
self
)
:
        
"
"
"
Return
the
URL
for
the
running
HTTP
FixtureServer
.
"
"
"
        
return
self
.
_httpd
.
get_url
(
"
/
"
)
    
property
    
def
port
(
self
)
:
        
"
"
"
Return
the
port
for
the
running
HTTP
FixtureServer
.
"
"
"
        
parse_result
=
urlparse
.
urlparse
(
self
.
url
)
        
return
parse_result
.
port
    
def
start
(
self
)
:
        
"
"
"
Start
the
HTTP
FixtureServer
.
"
"
"
        
return
self
.
_httpd
.
start
(
)
    
def
stop
(
self
)
:
        
"
"
"
Stop
the
HTTP
FixtureServer
.
"
"
"
        
return
self
.
_httpd
.
stop
(
)
