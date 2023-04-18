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
contrib
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
Contains
a
few
utilities
for
use
with
other
HTTP
libraries
.
"
"
"
try
:
    
from
requests
.
adapters
import
HTTPAdapter
    
from
requests
.
models
import
Response
    
from
requests
.
structures
import
CaseInsensitiveDict
    
from
requests
.
utils
import
get_encoding_from_headers
    
from
requests
.
cookies
import
extract_cookies_to_jar
except
ImportError
:
    
HTTPAdapter
=
object
from
hyper
.
common
.
connection
import
HTTPConnection
from
hyper
.
compat
import
urlparse
from
hyper
.
tls
import
init_context
class
HTTP20Adapter
(
HTTPAdapter
)
:
    
"
"
"
    
A
Requests
Transport
Adapter
that
uses
hyper
to
send
requests
over
    
HTTP
/
2
.
This
implements
some
degree
of
connection
pooling
to
maximise
the
    
HTTP
/
2
gain
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
connections
=
{
}
    
def
get_connection
(
self
host
port
scheme
cert
=
None
)
:
        
"
"
"
        
Gets
an
appropriate
HTTP
/
2
connection
object
based
on
        
host
/
port
/
scheme
/
cert
tuples
.
        
"
"
"
        
secure
=
(
scheme
=
=
'
https
'
)
        
if
port
is
None
:
            
port
=
80
if
not
secure
else
443
        
ssl_context
=
None
        
if
cert
is
not
None
:
            
ssl_context
=
init_context
(
cert
=
cert
)
        
try
:
            
conn
=
self
.
connections
[
(
host
port
scheme
cert
)
]
        
except
KeyError
:
            
conn
=
HTTPConnection
(
                
host
                
port
                
secure
=
secure
                
ssl_context
=
ssl_context
)
            
self
.
connections
[
(
host
port
scheme
cert
)
]
=
conn
        
return
conn
    
def
send
(
self
request
stream
=
False
cert
=
None
*
*
kwargs
)
:
        
"
"
"
        
Sends
a
HTTP
message
to
the
server
.
        
"
"
"
        
parsed
=
urlparse
(
request
.
url
)
        
conn
=
self
.
get_connection
(
            
parsed
.
hostname
            
parsed
.
port
            
parsed
.
scheme
            
cert
=
cert
)
        
selector
=
parsed
.
path
        
selector
+
=
'
?
'
+
parsed
.
query
if
parsed
.
query
else
'
'
        
selector
+
=
'
#
'
+
parsed
.
fragment
if
parsed
.
fragment
else
'
'
        
conn
.
request
(
            
request
.
method
            
selector
            
request
.
body
            
request
.
headers
        
)
        
resp
=
conn
.
get_response
(
)
        
r
=
self
.
build_response
(
request
resp
)
        
if
not
stream
:
            
r
.
content
        
return
r
    
def
build_response
(
self
request
resp
)
:
        
"
"
"
        
Builds
a
Requests
'
response
object
.
This
emulates
most
of
the
logic
of
        
the
standard
fuction
but
deals
with
the
lack
of
the
.
headers
        
property
on
the
HTTP20Response
object
.
        
Additionally
this
function
builds
in
a
number
of
features
that
are
        
purely
for
HTTPie
.
This
is
to
allow
maximum
compatibility
with
what
        
urllib3
does
so
that
HTTPie
doesn
'
t
fall
over
when
it
uses
us
.
        
"
"
"
        
response
=
Response
(
)
        
response
.
status_code
=
resp
.
status
        
response
.
headers
=
CaseInsensitiveDict
(
resp
.
headers
.
iter_raw
(
)
)
        
response
.
raw
=
resp
        
response
.
reason
=
resp
.
reason
        
response
.
encoding
=
get_encoding_from_headers
(
response
.
headers
)
        
extract_cookies_to_jar
(
response
.
cookies
request
response
)
        
response
.
url
=
request
.
url
        
response
.
request
=
request
        
response
.
connection
=
self
        
resp
.
release_conn
=
lambda
:
None
        
class
FakeOriginalResponse
(
object
)
:
            
def
__init__
(
self
headers
)
:
                
self
.
_headers
=
headers
            
def
get_all
(
self
name
default
=
None
)
:
                
values
=
[
]
                
for
n
v
in
self
.
_headers
:
                    
if
n
=
=
name
.
lower
(
)
:
                        
values
.
append
(
v
)
                
if
not
values
:
                    
return
default
                
return
values
            
def
getheaders
(
self
name
)
:
                
return
self
.
get_all
(
name
[
]
)
        
response
.
raw
.
_original_response
=
orig
=
FakeOriginalResponse
(
None
)
        
orig
.
version
=
20
        
orig
.
status
=
resp
.
status
        
orig
.
reason
=
resp
.
reason
        
orig
.
msg
=
FakeOriginalResponse
(
resp
.
headers
.
iter_raw
(
)
)
        
return
response
