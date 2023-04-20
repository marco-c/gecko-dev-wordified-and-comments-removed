"
"
"
Network
Authentication
Helpers
Contains
interface
(
MultiDomainBasicAuth
)
and
associated
glue
code
for
providing
credentials
in
the
context
of
network
requests
.
"
"
"
import
os
import
shutil
import
subprocess
import
urllib
.
parse
from
abc
import
ABC
abstractmethod
from
typing
import
Any
Dict
List
NamedTuple
Optional
Tuple
from
pip
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
pip
.
_vendor
.
requests
.
models
import
Request
Response
from
pip
.
_vendor
.
requests
.
utils
import
get_netrc_auth
from
pip
.
_internal
.
utils
.
logging
import
getLogger
from
pip
.
_internal
.
utils
.
misc
import
(
    
ask
    
ask_input
    
ask_password
    
remove_auth_from_url
    
split_auth_netloc_from_url
)
from
pip
.
_internal
.
vcs
.
versioncontrol
import
AuthInfo
logger
=
getLogger
(
__name__
)
KEYRING_DISABLED
=
False
class
Credentials
(
NamedTuple
)
:
    
url
:
str
    
username
:
str
    
password
:
str
class
KeyRingBaseProvider
(
ABC
)
:
    
"
"
"
Keyring
base
provider
interface
"
"
"
    
abstractmethod
    
def
get_auth_info
(
self
url
:
str
username
:
Optional
[
str
]
)
-
>
Optional
[
AuthInfo
]
:
        
.
.
.
    
abstractmethod
    
def
save_auth_info
(
self
url
:
str
username
:
str
password
:
str
)
-
>
None
:
        
.
.
.
class
KeyRingNullProvider
(
KeyRingBaseProvider
)
:
    
"
"
"
Keyring
null
provider
"
"
"
    
def
get_auth_info
(
self
url
:
str
username
:
Optional
[
str
]
)
-
>
Optional
[
AuthInfo
]
:
        
return
None
    
def
save_auth_info
(
self
url
:
str
username
:
str
password
:
str
)
-
>
None
:
        
return
None
class
KeyRingPythonProvider
(
KeyRingBaseProvider
)
:
    
"
"
"
Keyring
interface
which
uses
locally
imported
keyring
"
"
"
    
def
__init__
(
self
)
-
>
None
:
        
import
keyring
        
self
.
keyring
=
keyring
    
def
get_auth_info
(
self
url
:
str
username
:
Optional
[
str
]
)
-
>
Optional
[
AuthInfo
]
:
        
if
hasattr
(
self
.
keyring
"
get_credential
"
)
:
            
logger
.
debug
(
"
Getting
credentials
from
keyring
for
%
s
"
url
)
            
cred
=
self
.
keyring
.
get_credential
(
url
username
)
            
if
cred
is
not
None
:
                
return
cred
.
username
cred
.
password
            
return
None
        
if
username
is
not
None
:
            
logger
.
debug
(
"
Getting
password
from
keyring
for
%
s
"
url
)
            
password
=
self
.
keyring
.
get_password
(
url
username
)
            
if
password
:
                
return
username
password
        
return
None
    
def
save_auth_info
(
self
url
:
str
username
:
str
password
:
str
)
-
>
None
:
        
self
.
keyring
.
set_password
(
url
username
password
)
class
KeyRingCliProvider
(
KeyRingBaseProvider
)
:
    
"
"
"
Provider
which
uses
keyring
cli
    
Instead
of
calling
the
keyring
package
installed
alongside
pip
    
we
call
keyring
on
the
command
line
which
will
enable
pip
to
    
use
which
ever
installation
of
keyring
is
available
first
in
    
PATH
.
    
"
"
"
    
def
__init__
(
self
cmd
:
str
)
-
>
None
:
        
self
.
keyring
=
cmd
    
def
get_auth_info
(
self
url
:
str
username
:
Optional
[
str
]
)
-
>
Optional
[
AuthInfo
]
:
        
if
username
is
not
None
:
            
password
=
self
.
_get_password
(
url
username
)
            
if
password
is
not
None
:
                
return
username
password
        
return
None
    
def
save_auth_info
(
self
url
:
str
username
:
str
password
:
str
)
-
>
None
:
        
return
self
.
_set_password
(
url
username
password
)
    
def
_get_password
(
self
service_name
:
str
username
:
str
)
-
>
Optional
[
str
]
:
        
"
"
"
Mirror
the
implementation
of
keyring
.
get_password
using
cli
"
"
"
        
if
self
.
keyring
is
None
:
            
return
None
        
cmd
=
[
self
.
keyring
"
get
"
service_name
username
]
        
env
=
os
.
environ
.
copy
(
)
        
env
[
"
PYTHONIOENCODING
"
]
=
"
utf
-
8
"
        
res
=
subprocess
.
run
(
            
cmd
            
stdin
=
subprocess
.
DEVNULL
            
capture_output
=
True
            
env
=
env
        
)
        
if
res
.
returncode
:
            
return
None
        
return
res
.
stdout
.
decode
(
"
utf
-
8
"
)
.
strip
(
os
.
linesep
)
    
def
_set_password
(
self
service_name
:
str
username
:
str
password
:
str
)
-
>
None
:
        
"
"
"
Mirror
the
implementation
of
keyring
.
set_password
using
cli
"
"
"
        
if
self
.
keyring
is
None
:
            
return
None
        
cmd
=
[
self
.
keyring
"
set
"
service_name
username
]
        
input_
=
(
password
+
os
.
linesep
)
.
encode
(
"
utf
-
8
"
)
        
env
=
os
.
environ
.
copy
(
)
        
env
[
"
PYTHONIOENCODING
"
]
=
"
utf
-
8
"
        
res
=
subprocess
.
run
(
cmd
input
=
input_
env
=
env
)
        
res
.
check_returncode
(
)
        
return
None
def
get_keyring_provider
(
)
-
>
KeyRingBaseProvider
:
    
if
not
KEYRING_DISABLED
:
        
try
:
            
return
KeyRingPythonProvider
(
)
        
except
ImportError
:
            
pass
        
except
Exception
as
exc
:
            
logger
.
warning
(
                
"
Installed
copy
of
keyring
fails
with
exception
%
s
"
                
"
trying
to
find
a
keyring
executable
as
a
fallback
"
                
str
(
exc
)
            
)
        
cli
=
shutil
.
which
(
"
keyring
"
)
        
if
cli
:
            
return
KeyRingCliProvider
(
cli
)
    
return
KeyRingNullProvider
(
)
def
get_keyring_auth
(
url
:
Optional
[
str
]
username
:
Optional
[
str
]
)
-
>
Optional
[
AuthInfo
]
:
    
"
"
"
Return
the
tuple
auth
for
a
given
url
from
keyring
.
"
"
"
    
if
not
url
:
        
return
None
    
keyring
=
get_keyring_provider
(
)
    
try
:
        
return
keyring
.
get_auth_info
(
url
username
)
    
except
Exception
as
exc
:
        
logger
.
warning
(
            
"
Keyring
is
skipped
due
to
an
exception
:
%
s
"
            
str
(
exc
)
        
)
        
global
KEYRING_DISABLED
        
KEYRING_DISABLED
=
True
        
return
None
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
:
bool
=
True
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
    
)
-
>
None
:
        
self
.
prompting
=
prompting
        
self
.
index_urls
=
index_urls
        
self
.
passwords
:
Dict
[
str
AuthInfo
]
=
{
}
        
self
.
_credentials_to_save
:
Optional
[
Credentials
]
=
None
    
def
_get_index_url
(
self
url
:
str
)
-
>
Optional
[
str
]
:
        
"
"
"
Return
the
original
index
URL
matching
the
requested
URL
.
        
Cached
or
dynamically
generated
credentials
may
work
against
        
the
original
index
URL
rather
than
just
the
netloc
.
        
The
provided
url
should
have
had
its
username
and
password
        
removed
already
.
If
the
original
index
url
had
credentials
then
        
they
will
be
included
in
the
return
value
.
        
Returns
None
if
no
matching
index
was
found
or
if
-
-
no
-
index
        
was
specified
by
the
user
.
        
"
"
"
        
if
not
url
or
not
self
.
index_urls
:
            
return
None
        
for
u
in
self
.
index_urls
:
            
prefix
=
remove_auth_from_url
(
u
)
.
rstrip
(
"
/
"
)
+
"
/
"
            
if
url
.
startswith
(
prefix
)
:
                
return
u
        
return
None
    
def
_get_new_credentials
(
        
self
        
original_url
:
str
        
allow_netrc
:
bool
=
True
        
allow_keyring
:
bool
=
False
    
)
-
>
AuthInfo
:
        
"
"
"
Find
and
return
credentials
for
the
specified
URL
.
"
"
"
        
url
netloc
url_user_password
=
split_auth_netloc_from_url
(
            
original_url
        
)
        
username
password
=
url_user_password
        
if
username
is
not
None
and
password
is
not
None
:
            
logger
.
debug
(
"
Found
credentials
in
url
for
%
s
"
netloc
)
            
return
url_user_password
        
index_url
=
self
.
_get_index_url
(
url
)
        
if
index_url
:
            
index_info
=
split_auth_netloc_from_url
(
index_url
)
            
if
index_info
:
                
index_url
_
index_url_user_password
=
index_info
                
logger
.
debug
(
"
Found
index
url
%
s
"
index_url
)
        
if
index_url
and
index_url_user_password
[
0
]
is
not
None
:
            
username
password
=
index_url_user_password
            
if
username
is
not
None
and
password
is
not
None
:
                
logger
.
debug
(
"
Found
credentials
in
index
url
for
%
s
"
netloc
)
                
return
index_url_user_password
        
if
allow_netrc
:
            
netrc_auth
=
get_netrc_auth
(
original_url
)
            
if
netrc_auth
:
                
logger
.
debug
(
"
Found
credentials
in
netrc
for
%
s
"
netloc
)
                
return
netrc_auth
        
if
allow_keyring
:
            
kr_auth
=
(
                
get_keyring_auth
(
index_url
username
)
or
                
get_keyring_auth
(
netloc
username
)
            
)
            
if
kr_auth
:
                
logger
.
debug
(
"
Found
credentials
in
keyring
for
%
s
"
netloc
)
                
return
kr_auth
        
return
username
password
    
def
_get_url_and_credentials
(
        
self
original_url
:
str
    
)
-
>
Tuple
[
str
Optional
[
str
]
Optional
[
str
]
]
:
        
"
"
"
Return
the
credentials
to
use
for
the
provided
URL
.
        
If
allowed
netrc
and
keyring
may
be
used
to
obtain
the
        
correct
credentials
.
        
Returns
(
url_without_credentials
username
password
)
.
Note
        
that
even
if
the
original
URL
contains
credentials
this
        
function
may
return
a
different
username
and
password
.
        
"
"
"
        
url
netloc
_
=
split_auth_netloc_from_url
(
original_url
)
        
username
password
=
self
.
_get_new_credentials
(
original_url
)
        
if
(
username
is
None
or
password
is
None
)
and
netloc
in
self
.
passwords
:
            
un
pw
=
self
.
passwords
[
netloc
]
            
if
username
is
None
or
username
=
=
un
:
                
username
password
=
un
pw
        
if
username
is
not
None
or
password
is
not
None
:
            
username
=
username
or
"
"
            
password
=
password
or
"
"
            
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
        
assert
(
            
(
username
is
not
None
and
password
is
not
None
)
            
or
(
username
is
None
and
password
is
None
)
        
)
f
"
Could
not
load
credentials
from
url
:
{
original_url
}
"
        
return
url
username
password
    
def
__call__
(
self
req
:
Request
)
-
>
Request
:
        
url
username
password
=
self
.
_get_url_and_credentials
(
req
.
url
)
        
req
.
url
=
url
        
if
username
is
not
None
and
password
is
not
None
:
            
req
=
HTTPBasicAuth
(
username
password
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
_prompt_for_password
(
        
self
netloc
:
str
    
)
-
>
Tuple
[
Optional
[
str
]
Optional
[
str
]
bool
]
:
        
username
=
ask_input
(
f
"
User
for
{
netloc
}
:
"
)
        
if
not
username
:
            
return
None
None
False
        
auth
=
get_keyring_auth
(
netloc
username
)
        
if
auth
and
auth
[
0
]
is
not
None
and
auth
[
1
]
is
not
None
:
            
return
auth
[
0
]
auth
[
1
]
False
        
password
=
ask_password
(
"
Password
:
"
)
        
return
username
password
True
    
def
_should_save_password_to_keyring
(
self
)
-
>
bool
:
        
if
get_keyring_provider
(
)
is
None
:
            
return
False
        
return
ask
(
"
Save
credentials
to
keyring
[
y
/
N
]
:
"
[
"
y
"
"
n
"
]
)
=
=
"
y
"
    
def
handle_401
(
self
resp
:
Response
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
urllib
.
parse
.
urlparse
(
resp
.
url
)
        
username
password
=
self
.
_get_new_credentials
(
            
resp
.
url
            
allow_netrc
=
False
            
allow_keyring
=
True
        
)
        
save
=
False
        
if
not
username
and
not
password
:
            
username
password
save
=
self
.
_prompt_for_password
(
parsed
.
netloc
)
        
self
.
_credentials_to_save
=
None
        
if
username
is
not
None
and
password
is
not
None
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
            
if
save
and
self
.
_should_save_password_to_keyring
(
)
:
                
self
.
_credentials_to_save
=
Credentials
(
                    
url
=
parsed
.
netloc
                    
username
=
username
                    
password
=
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
        
req
.
register_hook
(
"
response
"
self
.
warn_on_401
)
        
if
self
.
_credentials_to_save
:
            
req
.
register_hook
(
"
response
"
self
.
save_credentials
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
warn_on_401
(
self
resp
:
Response
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
Response
callback
to
warn
about
incorrect
credentials
.
"
"
"
        
if
resp
.
status_code
=
=
401
:
            
logger
.
warning
(
                
"
401
Error
Credentials
not
correct
for
%
s
"
                
resp
.
request
.
url
            
)
    
def
save_credentials
(
self
resp
:
Response
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
Response
callback
to
save
credentials
on
success
.
"
"
"
        
keyring
=
get_keyring_provider
(
)
        
assert
not
isinstance
(
            
keyring
KeyRingNullProvider
        
)
"
should
never
reach
here
without
keyring
"
        
creds
=
self
.
_credentials_to_save
        
self
.
_credentials_to_save
=
None
        
if
creds
and
resp
.
status_code
<
400
:
            
try
:
                
logger
.
info
(
"
Saving
credentials
to
keyring
"
)
                
keyring
.
save_auth_info
(
creds
.
url
creds
.
username
creds
.
password
)
            
except
Exception
:
                
logger
.
exception
(
"
Failed
to
save
credentials
"
)
