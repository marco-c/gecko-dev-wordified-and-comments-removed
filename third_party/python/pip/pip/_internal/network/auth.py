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
urllib
.
parse
from
typing
import
Any
Dict
List
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
Credentials
=
Tuple
[
str
str
str
]
try
:
    
import
keyring
except
ImportError
:
    
keyring
=
None
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
    
keyring
=
None
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
    
global
keyring
    
if
not
url
or
not
keyring
:
        
return
None
    
try
:
        
try
:
            
get_credential
=
keyring
.
get_credential
        
except
AttributeError
:
            
pass
        
else
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
        
keyring
=
None
    
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
username
is
None
and
password
is
None
:
            
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
not
keyring
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
(
parsed
.
netloc
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
        
assert
keyring
is
not
None
"
should
never
reach
here
without
keyring
"
        
if
not
keyring
:
            
return
        
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
set_password
(
*
creds
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
