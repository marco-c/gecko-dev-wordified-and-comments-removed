from
__future__
import
absolute_import
import
cgi
import
email
.
utils
import
getpass
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
re
import
shutil
import
sys
import
tempfile
try
:
    
import
ssl
    
HAS_TLS
=
True
except
ImportError
:
    
HAS_TLS
=
False
from
pip9
.
_vendor
.
six
.
moves
.
urllib
import
parse
as
urllib_parse
from
pip9
.
_vendor
.
six
.
moves
.
urllib
import
request
as
urllib_request
import
pip9
from
pip9
.
exceptions
import
InstallationError
HashMismatch
from
pip9
.
models
import
PyPI
from
pip9
.
utils
import
(
splitext
rmtree
format_size
display_path
                       
backup_dir
ask_path_exists
unpack_file
                       
ARCHIVE_EXTENSIONS
consume
call_subprocess
)
from
pip9
.
utils
.
encoding
import
auto_decode
from
pip9
.
utils
.
filesystem
import
check_path_owner
from
pip9
.
utils
.
logging
import
indent_log
from
pip9
.
utils
.
setuptools_build
import
SETUPTOOLS_SHIM
from
pip9
.
utils
.
glibc
import
libc_ver
from
pip9
.
utils
.
ui
import
DownloadProgressBar
DownloadProgressSpinner
from
pip9
.
locations
import
write_delete_marker_file
from
pip9
.
vcs
import
vcs
from
pip9
.
_vendor
import
requests
six
from
pip9
.
_vendor
.
requests
.
adapters
import
BaseAdapter
HTTPAdapter
from
pip9
.
_vendor
.
requests
.
auth
import
AuthBase
HTTPBasicAuth
from
pip9
.
_vendor
.
requests
.
models
import
CONTENT_CHUNK_SIZE
Response
from
pip9
.
_vendor
.
requests
.
utils
import
get_netrc_auth
from
pip9
.
_vendor
.
requests
.
structures
import
CaseInsensitiveDict
from
pip9
.
_vendor
import
urllib3
from
pip9
.
_vendor
.
cachecontrol
import
CacheControlAdapter
from
pip9
.
_vendor
.
cachecontrol
.
caches
import
FileCache
from
pip9
.
_vendor
.
lockfile
import
LockError
from
pip9
.
_vendor
.
six
.
moves
import
xmlrpc_client
__all__
=
[
'
get_file_content
'
           
'
is_url
'
'
url_to_path
'
'
path_to_url
'
           
'
is_archive_file
'
'
unpack_vcs_link
'
           
'
unpack_file_url
'
'
is_vcs_url
'
'
is_file_url
'
           
'
unpack_http_url
'
'
unpack_url
'
]
logger
=
logging
.
getLogger
(
__name__
)
def
user_agent
(
)
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
pip9
.
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
'
CPython
'
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
'
PyPy
'
:
        
if
sys
.
pypy_version_info
.
releaselevel
=
=
'
final
'
:
            
pypy_version_info
=
sys
.
pypy_version_info
[
:
3
]
        
else
:
            
pypy_version_info
=
sys
.
pypy_version_info
        
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
'
Jython
'
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
'
IronPython
'
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
pip9
.
_vendor
import
distro
        
distro_infos
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
distro
.
linux_distribution
(
)
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
HAS_TLS
and
sys
.
version_info
[
:
2
]
>
(
2
6
)
:
        
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
MultiDomainBasicAuth
(
AuthBase
)
:
    
def
__init__
(
self
prompting
=
True
)
:
        
self
.
prompting
=
prompting
        
self
.
passwords
=
{
}
    
def
__call__
(
self
req
)
:
        
parsed
=
urllib_parse
.
urlparse
(
req
.
url
)
        
netloc
=
parsed
.
netloc
.
rsplit
(
"
"
1
)
[
-
1
]
        
req
.
url
=
urllib_parse
.
urlunparse
(
parsed
[
:
1
]
+
(
netloc
)
+
parsed
[
2
:
]
)
        
username
password
=
self
.
passwords
.
get
(
netloc
(
None
None
)
)
        
if
username
is
None
:
            
username
password
=
self
.
parse_credentials
(
parsed
.
netloc
)
        
if
username
is
None
and
password
is
None
:
            
netrc_auth
=
get_netrc_auth
(
req
.
url
)
            
username
password
=
netrc_auth
if
netrc_auth
else
(
None
None
)
        
if
username
or
password
:
            
self
.
passwords
[
netloc
]
=
(
username
password
)
            
req
=
HTTPBasicAuth
(
username
or
"
"
password
or
"
"
)
(
req
)
        
req
.
register_hook
(
"
response
"
self
.
handle_401
)
        
return
req
    
def
handle_401
(
self
resp
*
*
kwargs
)
:
        
if
resp
.
status_code
!
=
401
:
            
return
resp
        
if
not
self
.
prompting
:
            
return
resp
        
parsed
=
urllib_parse
.
urlparse
(
resp
.
url
)
        
username
=
six
.
moves
.
input
(
"
User
for
%
s
:
"
%
parsed
.
netloc
)
        
password
=
getpass
.
getpass
(
"
Password
:
"
)
        
if
username
or
password
:
            
self
.
passwords
[
parsed
.
netloc
]
=
(
username
password
)
        
resp
.
content
        
resp
.
raw
.
release_conn
(
)
        
req
=
HTTPBasicAuth
(
username
or
"
"
password
or
"
"
)
(
resp
.
request
)
        
new_resp
=
resp
.
connection
.
send
(
req
*
*
kwargs
)
        
new_resp
.
history
.
append
(
resp
)
        
return
new_resp
    
def
parse_credentials
(
self
netloc
)
:
        
if
"
"
in
netloc
:
            
userinfo
=
netloc
.
rsplit
(
"
"
1
)
[
0
]
            
if
"
:
"
in
userinfo
:
                
return
userinfo
.
split
(
"
:
"
1
)
            
return
userinfo
None
        
return
None
None
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
stream
=
None
timeout
=
None
verify
=
None
cert
=
None
             
proxies
=
None
)
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
raw
=
exc
        
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
:
        
pass
class
SafeFileCache
(
FileCache
)
:
    
"
"
"
    
A
file
based
cache
which
is
safe
to
use
even
when
the
target
directory
may
    
not
be
accessible
or
writable
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
        
super
(
SafeFileCache
self
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
        
if
not
check_path_owner
(
self
.
directory
)
:
            
logger
.
warning
(
                
"
The
directory
'
%
s
'
or
its
parent
directory
is
not
owned
by
"
                
"
the
current
user
and
the
cache
has
been
disabled
.
Please
"
                
"
check
the
permissions
and
owner
of
that
directory
.
If
"
                
"
executing
pip
with
sudo
you
may
want
sudo
'
s
-
H
flag
.
"
                
self
.
directory
            
)
            
self
.
directory
=
None
    
def
get
(
self
*
args
*
*
kwargs
)
:
        
if
self
.
directory
is
None
:
            
return
        
try
:
            
return
super
(
SafeFileCache
self
)
.
get
(
*
args
*
*
kwargs
)
        
except
(
LockError
OSError
IOError
)
:
            
pass
    
def
set
(
self
*
args
*
*
kwargs
)
:
        
if
self
.
directory
is
None
:
            
return
        
try
:
            
return
super
(
SafeFileCache
self
)
.
set
(
*
args
*
*
kwargs
)
        
except
(
LockError
OSError
IOError
)
:
            
pass
    
def
delete
(
self
*
args
*
*
kwargs
)
:
        
if
self
.
directory
is
None
:
            
return
        
try
:
            
return
super
(
SafeFileCache
self
)
.
delete
(
*
args
*
*
kwargs
)
        
except
(
LockError
OSError
IOError
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
url
verify
cert
)
:
        
conn
.
cert_reqs
=
'
CERT_NONE
'
        
conn
.
ca_certs
=
None
class
PipSession
(
requests
.
Session
)
:
    
timeout
=
None
    
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
        
retries
=
kwargs
.
pop
(
"
retries
"
0
)
        
cache
=
kwargs
.
pop
(
"
cache
"
None
)
        
insecure_hosts
=
kwargs
.
pop
(
"
insecure_hosts
"
[
]
)
        
super
(
PipSession
self
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
503
]
            
backoff_factor
=
0
.
25
        
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
use_dir_lock
=
True
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
)
        
insecure_adapter
=
InsecureHTTPAdapter
(
max_retries
=
retries
)
        
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
insecure_hosts
:
            
self
.
mount
(
"
https
:
/
/
{
0
}
/
"
.
format
(
host
)
insecure_adapter
)
    
def
request
(
self
method
url
*
args
*
*
kwargs
)
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
        
return
super
(
PipSession
self
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
def
get_file_content
(
url
comes_from
=
None
session
=
None
)
:
    
"
"
"
Gets
the
content
of
a
file
;
it
may
be
a
filename
file
:
URL
or
    
http
:
URL
.
Returns
(
location
content
)
.
Content
is
unicode
.
"
"
"
    
if
session
is
None
:
        
raise
TypeError
(
            
"
get_file_content
(
)
missing
1
required
keyword
argument
:
'
session
'
"
        
)
    
match
=
_scheme_re
.
search
(
url
)
    
if
match
:
        
scheme
=
match
.
group
(
1
)
.
lower
(
)
        
if
(
scheme
=
=
'
file
'
and
comes_from
and
                
comes_from
.
startswith
(
'
http
'
)
)
:
            
raise
InstallationError
(
                
'
Requirements
file
%
s
references
URL
%
s
which
is
local
'
                
%
(
comes_from
url
)
)
        
if
scheme
=
=
'
file
'
:
            
path
=
url
.
split
(
'
:
'
1
)
[
1
]
            
path
=
path
.
replace
(
'
\
\
'
'
/
'
)
            
match
=
_url_slash_drive_re
.
match
(
path
)
            
if
match
:
                
path
=
match
.
group
(
1
)
+
'
:
'
+
path
.
split
(
'
|
'
1
)
[
1
]
            
path
=
urllib_parse
.
unquote
(
path
)
            
if
path
.
startswith
(
'
/
'
)
:
                
path
=
'
/
'
+
path
.
lstrip
(
'
/
'
)
            
url
=
path
        
else
:
            
resp
=
session
.
get
(
url
)
            
resp
.
raise_for_status
(
)
            
return
resp
.
url
resp
.
text
    
try
:
        
with
open
(
url
'
rb
'
)
as
f
:
            
content
=
auto_decode
(
f
.
read
(
)
)
    
except
IOError
as
exc
:
        
raise
InstallationError
(
            
'
Could
not
open
requirements
file
:
%
s
'
%
str
(
exc
)
        
)
    
return
url
content
_scheme_re
=
re
.
compile
(
r
'
^
(
http
|
https
|
file
)
:
'
re
.
I
)
_url_slash_drive_re
=
re
.
compile
(
r
'
/
*
(
[
a
-
z
]
)
\
|
'
re
.
I
)
def
is_url
(
name
)
:
    
"
"
"
Returns
true
if
the
name
looks
like
a
URL
"
"
"
    
if
'
:
'
not
in
name
:
        
return
False
    
scheme
=
name
.
split
(
'
:
'
1
)
[
0
]
.
lower
(
)
    
return
scheme
in
[
'
http
'
'
https
'
'
file
'
'
ftp
'
]
+
vcs
.
all_schemes
def
url_to_path
(
url
)
:
    
"
"
"
    
Convert
a
file
:
URL
to
a
path
.
    
"
"
"
    
assert
url
.
startswith
(
'
file
:
'
)
(
        
"
You
can
only
turn
file
:
urls
into
filenames
(
not
%
r
)
"
%
url
)
    
_
netloc
path
_
_
=
urllib_parse
.
urlsplit
(
url
)
    
if
netloc
:
        
netloc
=
'
\
\
\
\
'
+
netloc
    
path
=
urllib_request
.
url2pathname
(
netloc
+
path
)
    
return
path
def
path_to_url
(
path
)
:
    
"
"
"
    
Convert
a
path
to
a
file
:
URL
.
The
path
will
be
made
absolute
and
have
    
quoted
path
parts
.
    
"
"
"
    
path
=
os
.
path
.
normpath
(
os
.
path
.
abspath
(
path
)
)
    
url
=
urllib_parse
.
urljoin
(
'
file
:
'
urllib_request
.
pathname2url
(
path
)
)
    
return
url
def
is_archive_file
(
name
)
:
    
"
"
"
Return
True
if
name
is
a
considered
as
an
archive
file
.
"
"
"
    
ext
=
splitext
(
name
)
[
1
]
.
lower
(
)
    
if
ext
in
ARCHIVE_EXTENSIONS
:
        
return
True
    
return
False
def
unpack_vcs_link
(
link
location
)
:
    
vcs_backend
=
_get_used_vcs_backend
(
link
)
    
vcs_backend
.
unpack
(
location
)
def
_get_used_vcs_backend
(
link
)
:
    
for
backend
in
vcs
.
backends
:
        
if
link
.
scheme
in
backend
.
schemes
:
            
vcs_backend
=
backend
(
link
.
url
)
            
return
vcs_backend
def
is_vcs_url
(
link
)
:
    
return
bool
(
_get_used_vcs_backend
(
link
)
)
def
is_file_url
(
link
)
:
    
return
link
.
url
.
lower
(
)
.
startswith
(
'
file
:
'
)
def
is_dir_url
(
link
)
:
    
"
"
"
Return
whether
a
file
:
/
/
Link
points
to
a
directory
.
    
link
must
not
have
any
other
scheme
but
file
:
/
/
.
Call
is_file_url
(
)
    
first
.
    
"
"
"
    
link_path
=
url_to_path
(
link
.
url_without_fragment
)
    
return
os
.
path
.
isdir
(
link_path
)
def
_progress_indicator
(
iterable
*
args
*
*
kwargs
)
:
    
return
iterable
def
_download_url
(
resp
link
content_file
hashes
)
:
    
try
:
        
total_length
=
int
(
resp
.
headers
[
'
content
-
length
'
]
)
    
except
(
ValueError
KeyError
TypeError
)
:
        
total_length
=
0
    
cached_resp
=
getattr
(
resp
"
from_cache
"
False
)
    
if
logger
.
getEffectiveLevel
(
)
>
logging
.
INFO
:
        
show_progress
=
False
    
elif
cached_resp
:
        
show_progress
=
False
    
elif
total_length
>
(
40
*
1000
)
:
        
show_progress
=
True
    
elif
not
total_length
:
        
show_progress
=
True
    
else
:
        
show_progress
=
False
    
show_url
=
link
.
show_url
    
def
resp_read
(
chunk_size
)
:
        
try
:
            
for
chunk
in
resp
.
raw
.
stream
(
                    
chunk_size
                    
decode_content
=
False
)
:
                
yield
chunk
        
except
AttributeError
:
            
while
True
:
                
chunk
=
resp
.
raw
.
read
(
chunk_size
)
                
if
not
chunk
:
                    
break
                
yield
chunk
    
def
written_chunks
(
chunks
)
:
        
for
chunk
in
chunks
:
            
content_file
.
write
(
chunk
)
            
yield
chunk
    
progress_indicator
=
_progress_indicator
    
if
link
.
netloc
=
=
PyPI
.
netloc
:
        
url
=
show_url
    
else
:
        
url
=
link
.
url_without_fragment
    
if
show_progress
:
        
if
total_length
:
            
logger
.
info
(
"
Downloading
%
s
(
%
s
)
"
url
format_size
(
total_length
)
)
            
progress_indicator
=
DownloadProgressBar
(
max
=
total_length
)
.
iter
        
else
:
            
logger
.
info
(
"
Downloading
%
s
"
url
)
            
progress_indicator
=
DownloadProgressSpinner
(
)
.
iter
    
elif
cached_resp
:
        
logger
.
info
(
"
Using
cached
%
s
"
url
)
    
else
:
        
logger
.
info
(
"
Downloading
%
s
"
url
)
    
logger
.
debug
(
'
Downloading
from
URL
%
s
'
link
)
    
downloaded_chunks
=
written_chunks
(
        
progress_indicator
(
            
resp_read
(
CONTENT_CHUNK_SIZE
)
            
CONTENT_CHUNK_SIZE
        
)
    
)
    
if
hashes
:
        
hashes
.
check_against_chunks
(
downloaded_chunks
)
    
else
:
        
consume
(
downloaded_chunks
)
def
_copy_file
(
filename
location
link
)
:
    
copy
=
True
    
download_location
=
os
.
path
.
join
(
location
link
.
filename
)
    
if
os
.
path
.
exists
(
download_location
)
:
        
response
=
ask_path_exists
(
            
'
The
file
%
s
exists
.
(
i
)
gnore
(
w
)
ipe
(
b
)
ackup
(
a
)
abort
'
%
            
display_path
(
download_location
)
(
'
i
'
'
w
'
'
b
'
'
a
'
)
)
        
if
response
=
=
'
i
'
:
            
copy
=
False
        
elif
response
=
=
'
w
'
:
            
logger
.
warning
(
'
Deleting
%
s
'
display_path
(
download_location
)
)
            
os
.
remove
(
download_location
)
        
elif
response
=
=
'
b
'
:
            
dest_file
=
backup_dir
(
download_location
)
            
logger
.
warning
(
                
'
Backing
up
%
s
to
%
s
'
                
display_path
(
download_location
)
                
display_path
(
dest_file
)
            
)
            
shutil
.
move
(
download_location
dest_file
)
        
elif
response
=
=
'
a
'
:
            
sys
.
exit
(
-
1
)
    
if
copy
:
        
shutil
.
copy
(
filename
download_location
)
        
logger
.
info
(
'
Saved
%
s
'
display_path
(
download_location
)
)
def
unpack_http_url
(
link
location
download_dir
=
None
                    
session
=
None
hashes
=
None
)
:
    
if
session
is
None
:
        
raise
TypeError
(
            
"
unpack_http_url
(
)
missing
1
required
keyword
argument
:
'
session
'
"
        
)
    
temp_dir
=
tempfile
.
mkdtemp
(
'
-
unpack
'
'
pip
-
'
)
    
already_downloaded_path
=
None
    
if
download_dir
:
        
already_downloaded_path
=
_check_download_dir
(
link
                                                      
download_dir
                                                      
hashes
)
    
if
already_downloaded_path
:
        
from_path
=
already_downloaded_path
        
content_type
=
mimetypes
.
guess_type
(
from_path
)
[
0
]
    
else
:
        
from_path
content_type
=
_download_http_url
(
link
                                                     
session
                                                     
temp_dir
                                                     
hashes
)
    
unpack_file
(
from_path
location
content_type
link
)
    
if
download_dir
and
not
already_downloaded_path
:
        
_copy_file
(
from_path
download_dir
link
)
    
if
not
already_downloaded_path
:
        
os
.
unlink
(
from_path
)
    
rmtree
(
temp_dir
)
def
unpack_file_url
(
link
location
download_dir
=
None
hashes
=
None
)
:
    
"
"
"
Unpack
link
into
location
.
    
If
download_dir
is
provided
and
link
points
to
a
file
make
a
copy
    
of
the
link
file
inside
download_dir
.
    
"
"
"
    
link_path
=
url_to_path
(
link
.
url_without_fragment
)
    
if
is_dir_url
(
link
)
:
        
if
os
.
path
.
isdir
(
location
)
:
            
rmtree
(
location
)
        
shutil
.
copytree
(
link_path
location
symlinks
=
True
)
        
if
download_dir
:
            
logger
.
info
(
'
Link
is
a
directory
ignoring
download_dir
'
)
        
return
    
if
hashes
:
        
hashes
.
check_against_path
(
link_path
)
    
already_downloaded_path
=
None
    
if
download_dir
:
        
already_downloaded_path
=
_check_download_dir
(
link
                                                      
download_dir
                                                      
hashes
)
    
if
already_downloaded_path
:
        
from_path
=
already_downloaded_path
    
else
:
        
from_path
=
link_path
    
content_type
=
mimetypes
.
guess_type
(
from_path
)
[
0
]
    
unpack_file
(
from_path
location
content_type
link
)
    
if
download_dir
and
not
already_downloaded_path
:
        
_copy_file
(
from_path
download_dir
link
)
def
_copy_dist_from_dir
(
link_path
location
)
:
    
"
"
"
Copy
distribution
files
in
link_path
to
location
.
    
Invoked
when
user
requests
to
install
a
local
directory
.
E
.
g
.
:
        
pip
install
.
        
pip
install
~
/
dev
/
git
-
repos
/
python
-
prompt
-
toolkit
    
"
"
"
    
if
os
.
path
.
isdir
(
location
)
:
        
rmtree
(
location
)
    
setup_py
=
'
setup
.
py
'
    
sdist_args
=
[
sys
.
executable
]
    
sdist_args
.
append
(
'
-
c
'
)
    
sdist_args
.
append
(
SETUPTOOLS_SHIM
%
setup_py
)
    
sdist_args
.
append
(
'
sdist
'
)
    
sdist_args
+
=
[
'
-
-
dist
-
dir
'
location
]
    
logger
.
info
(
'
Running
setup
.
py
sdist
for
%
s
'
link_path
)
    
with
indent_log
(
)
:
        
call_subprocess
(
sdist_args
cwd
=
link_path
show_stdout
=
False
)
    
sdist
=
os
.
path
.
join
(
location
os
.
listdir
(
location
)
[
0
]
)
    
logger
.
info
(
'
Unpacking
sdist
%
s
into
%
s
'
sdist
location
)
    
unpack_file
(
sdist
location
content_type
=
None
link
=
None
)
class
PipXmlrpcTransport
(
xmlrpc_client
.
Transport
)
:
    
"
"
"
Provide
a
xmlrpclib
.
Transport
implementation
via
a
PipSession
    
object
.
    
"
"
"
    
def
__init__
(
self
index_url
session
use_datetime
=
False
)
:
        
xmlrpc_client
.
Transport
.
__init__
(
self
use_datetime
)
        
index_parts
=
urllib_parse
.
urlparse
(
index_url
)
        
self
.
_scheme
=
index_parts
.
scheme
        
self
.
_session
=
session
    
def
request
(
self
host
handler
request_body
verbose
=
False
)
:
        
parts
=
(
self
.
_scheme
host
handler
None
None
None
)
        
url
=
urllib_parse
.
urlunparse
(
parts
)
        
try
:
            
headers
=
{
'
Content
-
Type
'
:
'
text
/
xml
'
}
            
response
=
self
.
_session
.
post
(
url
data
=
request_body
                                          
headers
=
headers
stream
=
True
)
            
response
.
raise_for_status
(
)
            
self
.
verbose
=
verbose
            
return
self
.
parse_response
(
response
.
raw
)
        
except
requests
.
HTTPError
as
exc
:
            
logger
.
critical
(
                
"
HTTP
error
%
s
while
getting
%
s
"
                
exc
.
response
.
status_code
url
            
)
            
raise
def
unpack_url
(
link
location
download_dir
=
None
               
only_download
=
False
session
=
None
hashes
=
None
)
:
    
"
"
"
Unpack
link
.
       
If
link
is
a
VCS
link
:
         
if
only_download
export
into
download_dir
and
ignore
location
          
else
unpack
into
location
       
for
other
types
of
link
:
         
-
unpack
into
location
         
-
if
download_dir
copy
the
file
into
download_dir
         
-
if
only_download
mark
location
for
deletion
    
:
param
hashes
:
A
Hashes
object
one
of
whose
embedded
hashes
must
match
        
or
HashMismatch
will
be
raised
.
If
the
Hashes
is
empty
no
matches
are
        
required
and
unhashable
types
of
requirements
(
like
VCS
ones
which
        
would
ordinarily
raise
HashUnsupported
)
are
allowed
.
    
"
"
"
    
if
is_vcs_url
(
link
)
:
        
unpack_vcs_link
(
link
location
)
    
elif
is_file_url
(
link
)
:
        
unpack_file_url
(
link
location
download_dir
hashes
=
hashes
)
    
else
:
        
if
session
is
None
:
            
session
=
PipSession
(
)
        
unpack_http_url
(
            
link
            
location
            
download_dir
            
session
            
hashes
=
hashes
        
)
    
if
only_download
:
        
write_delete_marker_file
(
location
)
def
_download_http_url
(
link
session
temp_dir
hashes
)
:
    
"
"
"
Download
link
url
into
temp_dir
using
provided
session
"
"
"
    
target_url
=
link
.
url
.
split
(
'
#
'
1
)
[
0
]
    
try
:
        
resp
=
session
.
get
(
            
target_url
            
headers
=
{
"
Accept
-
Encoding
"
:
"
identity
"
}
            
stream
=
True
        
)
        
resp
.
raise_for_status
(
)
    
except
requests
.
HTTPError
as
exc
:
        
logger
.
critical
(
            
"
HTTP
error
%
s
while
getting
%
s
"
exc
.
response
.
status_code
link
        
)
        
raise
    
content_type
=
resp
.
headers
.
get
(
'
content
-
type
'
'
'
)
    
filename
=
link
.
filename
    
content_disposition
=
resp
.
headers
.
get
(
'
content
-
disposition
'
)
    
if
content_disposition
:
        
type
params
=
cgi
.
parse_header
(
content_disposition
)
        
filename
=
params
.
get
(
'
filename
'
)
or
filename
    
ext
=
splitext
(
filename
)
[
1
]
    
if
not
ext
:
        
ext
=
mimetypes
.
guess_extension
(
content_type
)
        
if
ext
:
            
filename
+
=
ext
    
if
not
ext
and
link
.
url
!
=
resp
.
url
:
        
ext
=
os
.
path
.
splitext
(
resp
.
url
)
[
1
]
        
if
ext
:
            
filename
+
=
ext
    
file_path
=
os
.
path
.
join
(
temp_dir
filename
)
    
with
open
(
file_path
'
wb
'
)
as
content_file
:
        
_download_url
(
resp
link
content_file
hashes
)
    
return
file_path
content_type
def
_check_download_dir
(
link
download_dir
hashes
)
:
    
"
"
"
Check
download_dir
for
previously
downloaded
file
with
correct
hash
        
If
a
correct
file
is
found
return
its
path
else
None
    
"
"
"
    
download_path
=
os
.
path
.
join
(
download_dir
link
.
filename
)
    
if
os
.
path
.
exists
(
download_path
)
:
        
logger
.
info
(
'
File
was
already
downloaded
%
s
'
download_path
)
        
if
hashes
:
            
try
:
                
hashes
.
check_against_path
(
download_path
)
            
except
HashMismatch
:
                
logger
.
warning
(
                    
'
Previously
-
downloaded
file
%
s
has
bad
hash
.
'
                    
'
Re
-
downloading
.
'
                    
download_path
                
)
                
os
.
unlink
(
download_path
)
                
return
None
        
return
download_path
    
return
None
