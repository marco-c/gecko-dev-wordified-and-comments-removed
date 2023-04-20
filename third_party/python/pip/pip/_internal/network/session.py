"
"
"
PipSession
and
supporting
code
containing
all
pip
-
specific
network
request
configuration
and
behavior
.
"
"
"
import
email
.
utils
import
io
import
ipaddress
import
json
import
logging
import
mimetypes
import
os
import
platform
import
shutil
import
subprocess
import
sys
import
urllib
.
parse
import
warnings
from
typing
import
(
    
TYPE_CHECKING
    
Any
    
Dict
    
Generator
    
List
    
Mapping
    
Optional
    
Sequence
    
Tuple
    
Union
)
from
pip
.
_vendor
import
requests
urllib3
from
pip
.
_vendor
.
cachecontrol
import
CacheControlAdapter
as
_BaseCacheControlAdapter
from
pip
.
_vendor
.
requests
.
adapters
import
DEFAULT_POOLBLOCK
BaseAdapter
from
pip
.
_vendor
.
requests
.
adapters
import
HTTPAdapter
as
_BaseHTTPAdapter
from
pip
.
_vendor
.
requests
.
models
import
PreparedRequest
Response
from
pip
.
_vendor
.
requests
.
structures
import
CaseInsensitiveDict
from
pip
.
_vendor
.
urllib3
.
connectionpool
import
ConnectionPool
from
pip
.
_vendor
.
urllib3
.
exceptions
import
InsecureRequestWarning
from
pip
import
__version__
from
pip
.
_internal
.
metadata
import
get_default_environment
from
pip
.
_internal
.
models
.
link
import
Link
from
pip
.
_internal
.
network
.
auth
import
MultiDomainBasicAuth
from
pip
.
_internal
.
network
.
cache
import
SafeFileCache
from
pip
.
_internal
.
utils
.
compat
import
has_tls
from
pip
.
_internal
.
utils
.
glibc
import
libc_ver
from
pip
.
_internal
.
utils
.
misc
import
build_url_from_netloc
parse_netloc
from
pip
.
_internal
.
utils
.
urls
import
url_to_path
if
TYPE_CHECKING
:
    
from
ssl
import
SSLContext
    
from
pip
.
_vendor
.
urllib3
.
poolmanager
import
PoolManager
logger
=
logging
.
getLogger
(
__name__
)
SecureOrigin
=
Tuple
[
str
str
Optional
[
Union
[
int
str
]
]
]
warnings
.
filterwarnings
(
"
ignore
"
category
=
InsecureRequestWarning
)
SECURE_ORIGINS
:
List
[
SecureOrigin
]
=
[
    
(
"
https
"
"
*
"
"
*
"
)
    
(
"
*
"
"
localhost
"
"
*
"
)
    
(
"
*
"
"
127
.
0
.
0
.
0
/
8
"
"
*
"
)
    
(
"
*
"
"
:
:
1
/
128
"
"
*
"
)
    
(
"
file
"
"
*
"
None
)
    
(
"
ssh
"
"
*
"
"
*
"
)
]
CI_ENVIRONMENT_VARIABLES
=
(
    
"
BUILD_BUILDID
"
    
"
BUILD_ID
"
    
"
CI
"
    
"
PIP_IS_CI
"
)
def
looks_like_ci
(
)
-
>
bool
:
    
"
"
"
    
Return
whether
it
looks
like
pip
is
running
under
CI
.
    
"
"
"
    
return
any
(
name
in
os
.
environ
for
name
in
CI_ENVIRONMENT_VARIABLES
)
def
user_agent
(
)
-
>
str
:
    
"
"
"
    
Return
a
string
representing
the
user
agent
.
    
"
"
"
    
data
:
Dict
[
str
Any
]
=
{
        
"
installer
"
:
{
"
name
"
:
"
pip
"
"
version
"
:
__version__
}
        
"
python
"
:
platform
.
python_version
(
)
        
"
implementation
"
:
{
            
"
name
"
:
platform
.
python_implementation
(
)
        
}
    
}
    
if
data
[
"
implementation
"
]
[
"
name
"
]
=
=
"
CPython
"
:
        
data
[
"
implementation
"
]
[
"
version
"
]
=
platform
.
python_version
(
)
    
elif
data
[
"
implementation
"
]
[
"
name
"
]
=
=
"
PyPy
"
:
        
pypy_version_info
=
sys
.
pypy_version_info
        
if
pypy_version_info
.
releaselevel
=
=
"
final
"
:
            
pypy_version_info
=
pypy_version_info
[
:
3
]
        
data
[
"
implementation
"
]
[
"
version
"
]
=
"
.
"
.
join
(
            
[
str
(
x
)
for
x
in
pypy_version_info
]
        
)
    
elif
data
[
"
implementation
"
]
[
"
name
"
]
=
=
"
Jython
"
:
        
data
[
"
implementation
"
]
[
"
version
"
]
=
platform
.
python_version
(
)
    
elif
data
[
"
implementation
"
]
[
"
name
"
]
=
=
"
IronPython
"
:
        
data
[
"
implementation
"
]
[
"
version
"
]
=
platform
.
python_version
(
)
    
if
sys
.
platform
.
startswith
(
"
linux
"
)
:
        
from
pip
.
_vendor
import
distro
        
linux_distribution
=
distro
.
name
(
)
distro
.
version
(
)
distro
.
codename
(
)
        
distro_infos
:
Dict
[
str
Any
]
=
dict
(
            
filter
(
                
lambda
x
:
x
[
1
]
                
zip
(
[
"
name
"
"
version
"
"
id
"
]
linux_distribution
)
            
)
        
)
        
libc
=
dict
(
            
filter
(
                
lambda
x
:
x
[
1
]
                
zip
(
[
"
lib
"
"
version
"
]
libc_ver
(
)
)
            
)
        
)
        
if
libc
:
            
distro_infos
[
"
libc
"
]
=
libc
        
if
distro_infos
:
            
data
[
"
distro
"
]
=
distro_infos
    
if
sys
.
platform
.
startswith
(
"
darwin
"
)
and
platform
.
mac_ver
(
)
[
0
]
:
        
data
[
"
distro
"
]
=
{
"
name
"
:
"
macOS
"
"
version
"
:
platform
.
mac_ver
(
)
[
0
]
}
    
if
platform
.
system
(
)
:
        
data
.
setdefault
(
"
system
"
{
}
)
[
"
name
"
]
=
platform
.
system
(
)
    
if
platform
.
release
(
)
:
        
data
.
setdefault
(
"
system
"
{
}
)
[
"
release
"
]
=
platform
.
release
(
)
    
if
platform
.
machine
(
)
:
        
data
[
"
cpu
"
]
=
platform
.
machine
(
)
    
if
has_tls
(
)
:
        
import
_ssl
as
ssl
        
data
[
"
openssl_version
"
]
=
ssl
.
OPENSSL_VERSION
    
setuptools_dist
=
get_default_environment
(
)
.
get_distribution
(
"
setuptools
"
)
    
if
setuptools_dist
is
not
None
:
        
data
[
"
setuptools_version
"
]
=
str
(
setuptools_dist
.
version
)
    
if
shutil
.
which
(
"
rustc
"
)
is
not
None
:
        
try
:
            
rustc_output
=
subprocess
.
check_output
(
                
[
"
rustc
"
"
-
-
version
"
]
stderr
=
subprocess
.
STDOUT
timeout
=
0
.
5
            
)
        
except
Exception
:
            
pass
        
else
:
            
if
rustc_output
.
startswith
(
b
"
rustc
"
)
:
                
data
[
"
rustc_version
"
]
=
rustc_output
.
split
(
b
"
"
)
[
1
]
.
decode
(
)
    
data
[
"
ci
"
]
=
True
if
looks_like_ci
(
)
else
None
    
user_data
=
os
.
environ
.
get
(
"
PIP_USER_AGENT_USER_DATA
"
)
    
if
user_data
is
not
None
:
        
data
[
"
user_data
"
]
=
user_data
    
return
"
{
data
[
installer
]
[
name
]
}
/
{
data
[
installer
]
[
version
]
}
{
json
}
"
.
format
(
        
data
=
data
        
json
=
json
.
dumps
(
data
separators
=
(
"
"
"
:
"
)
sort_keys
=
True
)
    
)
class
LocalFSAdapter
(
BaseAdapter
)
:
    
def
send
(
        
self
        
request
:
PreparedRequest
        
stream
:
bool
=
False
        
timeout
:
Optional
[
Union
[
float
Tuple
[
float
float
]
]
]
=
None
        
verify
:
Union
[
bool
str
]
=
True
        
cert
:
Optional
[
Union
[
str
Tuple
[
str
str
]
]
]
=
None
        
proxies
:
Optional
[
Mapping
[
str
str
]
]
=
None
    
)
-
>
Response
:
        
pathname
=
url_to_path
(
request
.
url
)
        
resp
=
Response
(
)
        
resp
.
status_code
=
200
        
resp
.
url
=
request
.
url
        
try
:
            
stats
=
os
.
stat
(
pathname
)
        
except
OSError
as
exc
:
            
resp
.
status_code
=
404
            
resp
.
reason
=
type
(
exc
)
.
__name__
            
resp
.
raw
=
io
.
BytesIO
(
f
"
{
resp
.
reason
}
:
{
exc
}
"
.
encode
(
"
utf8
"
)
)
        
else
:
            
modified
=
email
.
utils
.
formatdate
(
stats
.
st_mtime
usegmt
=
True
)
            
content_type
=
mimetypes
.
guess_type
(
pathname
)
[
0
]
or
"
text
/
plain
"
            
resp
.
headers
=
CaseInsensitiveDict
(
                
{
                    
"
Content
-
Type
"
:
content_type
                    
"
Content
-
Length
"
:
stats
.
st_size
                    
"
Last
-
Modified
"
:
modified
                
}
            
)
            
resp
.
raw
=
open
(
pathname
"
rb
"
)
            
resp
.
close
=
resp
.
raw
.
close
        
return
resp
    
def
close
(
self
)
-
>
None
:
        
pass
class
_SSLContextAdapterMixin
:
    
"
"
"
Mixin
to
add
the
ssl_context
constructor
argument
to
HTTP
adapters
.
    
The
additional
argument
is
forwarded
directly
to
the
pool
manager
.
This
allows
us
    
to
dynamically
decide
what
SSL
store
to
use
at
runtime
which
is
used
to
implement
    
the
optional
truststore
backend
.
    
"
"
"
    
def
__init__
(
        
self
        
*
        
ssl_context
:
Optional
[
"
SSLContext
"
]
=
None
        
*
*
kwargs
:
Any
    
)
-
>
None
:
        
self
.
_ssl_context
=
ssl_context
        
super
(
)
.
__init__
(
*
*
kwargs
)
    
def
init_poolmanager
(
        
self
        
connections
:
int
        
maxsize
:
int
        
block
:
bool
=
DEFAULT_POOLBLOCK
        
*
*
pool_kwargs
:
Any
    
)
-
>
"
PoolManager
"
:
        
if
self
.
_ssl_context
is
not
None
:
            
pool_kwargs
.
setdefault
(
"
ssl_context
"
self
.
_ssl_context
)
        
return
super
(
)
.
init_poolmanager
(
            
connections
=
connections
            
maxsize
=
maxsize
            
block
=
block
            
*
*
pool_kwargs
        
)
class
HTTPAdapter
(
_SSLContextAdapterMixin
_BaseHTTPAdapter
)
:
    
pass
class
CacheControlAdapter
(
_SSLContextAdapterMixin
_BaseCacheControlAdapter
)
:
    
pass
class
InsecureHTTPAdapter
(
HTTPAdapter
)
:
    
def
cert_verify
(
        
self
        
conn
:
ConnectionPool
        
url
:
str
        
verify
:
Union
[
bool
str
]
        
cert
:
Optional
[
Union
[
str
Tuple
[
str
str
]
]
]
    
)
-
>
None
:
        
super
(
)
.
cert_verify
(
conn
=
conn
url
=
url
verify
=
False
cert
=
cert
)
class
InsecureCacheControlAdapter
(
CacheControlAdapter
)
:
    
def
cert_verify
(
        
self
        
conn
:
ConnectionPool
        
url
:
str
        
verify
:
Union
[
bool
str
]
        
cert
:
Optional
[
Union
[
str
Tuple
[
str
str
]
]
]
    
)
-
>
None
:
        
super
(
)
.
cert_verify
(
conn
=
conn
url
=
url
verify
=
False
cert
=
cert
)
class
PipSession
(
requests
.
Session
)
:
    
timeout
:
Optional
[
int
]
=
None
    
def
__init__
(
        
self
        
*
args
:
Any
        
retries
:
int
=
0
        
cache
:
Optional
[
str
]
=
None
        
trusted_hosts
:
Sequence
[
str
]
=
(
)
        
index_urls
:
Optional
[
List
[
str
]
]
=
None
        
ssl_context
:
Optional
[
"
SSLContext
"
]
=
None
        
*
*
kwargs
:
Any
    
)
-
>
None
:
        
"
"
"
        
:
param
trusted_hosts
:
Domains
not
to
emit
warnings
for
when
not
using
            
HTTPS
.
        
"
"
"
        
super
(
)
.
__init__
(
*
args
*
*
kwargs
)
        
self
.
pip_trusted_origins
:
List
[
Tuple
[
str
Optional
[
int
]
]
]
=
[
]
        
self
.
headers
[
"
User
-
Agent
"
]
=
user_agent
(
)
        
self
.
auth
=
MultiDomainBasicAuth
(
index_urls
=
index_urls
)
        
retries
=
urllib3
.
Retry
(
            
total
=
retries
            
status_forcelist
=
[
500
503
520
527
]
            
backoff_factor
=
0
.
25
        
)
        
insecure_adapter
=
InsecureHTTPAdapter
(
max_retries
=
retries
)
        
if
cache
:
            
secure_adapter
=
CacheControlAdapter
(
                
cache
=
SafeFileCache
(
cache
)
                
max_retries
=
retries
                
ssl_context
=
ssl_context
            
)
            
self
.
_trusted_host_adapter
=
InsecureCacheControlAdapter
(
                
cache
=
SafeFileCache
(
cache
)
                
max_retries
=
retries
            
)
        
else
:
            
secure_adapter
=
HTTPAdapter
(
max_retries
=
retries
ssl_context
=
ssl_context
)
            
self
.
_trusted_host_adapter
=
insecure_adapter
        
self
.
mount
(
"
https
:
/
/
"
secure_adapter
)
        
self
.
mount
(
"
http
:
/
/
"
insecure_adapter
)
        
self
.
mount
(
"
file
:
/
/
"
LocalFSAdapter
(
)
)
        
for
host
in
trusted_hosts
:
            
self
.
add_trusted_host
(
host
suppress_logging
=
True
)
    
def
update_index_urls
(
self
new_index_urls
:
List
[
str
]
)
-
>
None
:
        
"
"
"
        
:
param
new_index_urls
:
New
index
urls
to
update
the
authentication
            
handler
with
.
        
"
"
"
        
self
.
auth
.
index_urls
=
new_index_urls
    
def
add_trusted_host
(
        
self
host
:
str
source
:
Optional
[
str
]
=
None
suppress_logging
:
bool
=
False
    
)
-
>
None
:
        
"
"
"
        
:
param
host
:
It
is
okay
to
provide
a
host
that
has
previously
been
            
added
.
        
:
param
source
:
An
optional
source
string
for
logging
where
the
host
            
string
came
from
.
        
"
"
"
        
if
not
suppress_logging
:
            
msg
=
f
"
adding
trusted
host
:
{
host
!
r
}
"
            
if
source
is
not
None
:
                
msg
+
=
f
"
(
from
{
source
}
)
"
            
logger
.
info
(
msg
)
        
host_port
=
parse_netloc
(
host
)
        
if
host_port
not
in
self
.
pip_trusted_origins
:
            
self
.
pip_trusted_origins
.
append
(
host_port
)
        
self
.
mount
(
            
build_url_from_netloc
(
host
scheme
=
"
http
"
)
+
"
/
"
self
.
_trusted_host_adapter
        
)
        
self
.
mount
(
build_url_from_netloc
(
host
)
+
"
/
"
self
.
_trusted_host_adapter
)
        
if
not
host_port
[
1
]
:
            
self
.
mount
(
                
build_url_from_netloc
(
host
scheme
=
"
http
"
)
+
"
:
"
                
self
.
_trusted_host_adapter
            
)
            
self
.
mount
(
build_url_from_netloc
(
host
)
+
"
:
"
self
.
_trusted_host_adapter
)
    
def
iter_secure_origins
(
self
)
-
>
Generator
[
SecureOrigin
None
None
]
:
        
yield
from
SECURE_ORIGINS
        
for
host
port
in
self
.
pip_trusted_origins
:
            
yield
(
"
*
"
host
"
*
"
if
port
is
None
else
port
)
    
def
is_secure_origin
(
self
location
:
Link
)
-
>
bool
:
        
parsed
=
urllib
.
parse
.
urlparse
(
str
(
location
)
)
        
origin_protocol
origin_host
origin_port
=
(
            
parsed
.
scheme
            
parsed
.
hostname
            
parsed
.
port
        
)
        
origin_protocol
=
origin_protocol
.
rsplit
(
"
+
"
1
)
[
-
1
]
        
for
secure_origin
in
self
.
iter_secure_origins
(
)
:
            
secure_protocol
secure_host
secure_port
=
secure_origin
            
if
origin_protocol
!
=
secure_protocol
and
secure_protocol
!
=
"
*
"
:
                
continue
            
try
:
                
addr
=
ipaddress
.
ip_address
(
origin_host
or
"
"
)
                
network
=
ipaddress
.
ip_network
(
secure_host
)
            
except
ValueError
:
                
if
(
                    
origin_host
                    
and
origin_host
.
lower
(
)
!
=
secure_host
.
lower
(
)
                    
and
secure_host
!
=
"
*
"
                
)
:
                    
continue
            
else
:
                
if
addr
not
in
network
:
                    
continue
            
if
(
                
origin_port
!
=
secure_port
                
and
secure_port
!
=
"
*
"
                
and
secure_port
is
not
None
            
)
:
                
continue
            
return
True
        
logger
.
warning
(
            
"
The
repository
located
at
%
s
is
not
a
trusted
or
secure
host
and
"
            
"
is
being
ignored
.
If
this
repository
is
available
via
HTTPS
we
"
            
"
recommend
you
use
HTTPS
instead
otherwise
you
may
silence
"
            
"
this
warning
and
allow
it
anyway
with
'
-
-
trusted
-
host
%
s
'
.
"
            
origin_host
            
origin_host
        
)
        
return
False
    
def
request
(
self
method
:
str
url
:
str
*
args
:
Any
*
*
kwargs
:
Any
)
-
>
Response
:
        
kwargs
.
setdefault
(
"
timeout
"
self
.
timeout
)
        
kwargs
.
setdefault
(
"
proxies
"
self
.
proxies
)
        
return
super
(
)
.
request
(
method
url
*
args
*
*
kwargs
)
