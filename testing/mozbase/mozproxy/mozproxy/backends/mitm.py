"
"
"
Functions
to
download
install
setup
and
use
the
mitmproxy
playback
tool
"
"
"
from
__future__
import
absolute_import
import
glob
import
os
import
subprocess
import
sys
import
time
import
socket
import
mozinfo
from
mozprocess
import
ProcessHandler
from
mozproxy
.
backends
.
base
import
Playback
from
mozproxy
.
utils
import
(
    
transform_platform
    
tooltool_download
    
download_file_from_url
    
LOG
)
here
=
os
.
path
.
dirname
(
__file__
)
try
:
    
DEFAULT_CERT_PATH
=
os
.
path
.
join
(
        
os
.
getenv
(
"
HOME
"
)
"
.
mitmproxy
"
"
mitmproxy
-
ca
-
cert
.
cer
"
    
)
except
Exception
:
    
DEFAULT_CERT_PATH
=
os
.
path
.
join
(
        
os
.
getenv
(
"
HOMEDRIVE
"
)
        
os
.
getenv
(
"
HOMEPATH
"
)
        
"
.
mitmproxy
"
        
"
mitmproxy
-
ca
-
cert
.
cer
"
    
)
if
os
.
name
=
=
"
nt
"
and
"
/
"
in
DEFAULT_CERT_PATH
:
    
DEFAULT_CERT_PATH
=
DEFAULT_CERT_PATH
.
replace
(
"
/
"
"
\
\
"
)
MITMDUMP_COMMAND_TIMEOUT
=
30
POLICIES_CONTENT_ON
=
"
"
"
{
  
"
policies
"
:
{
    
"
Certificates
"
:
{
      
"
Install
"
:
[
"
%
(
cert
)
s
"
]
    
}
    
"
Proxy
"
:
{
      
"
Mode
"
:
"
manual
"
      
"
HTTPProxy
"
:
"
%
(
host
)
s
:
8080
"
      
"
SSLProxy
"
:
"
%
(
host
)
s
:
8080
"
      
"
Passthrough
"
:
"
%
(
host
)
s
"
      
"
Locked
"
:
true
    
}
  
}
}
"
"
"
POLICIES_CONTENT_OFF
=
"
"
"
{
  
"
policies
"
:
{
    
"
Proxy
"
:
{
      
"
Mode
"
:
"
none
"
      
"
Locked
"
:
false
    
}
  
}
}
"
"
"
class
Mitmproxy
(
Playback
)
:
    
def
__init__
(
self
config
)
:
        
self
.
config
=
config
        
self
.
mitmproxy_proc
=
None
        
self
.
mitmdump_path
=
None
        
self
.
browser_path
=
config
.
get
(
"
binary
"
)
        
self
.
policies_dir
=
None
        
if
self
.
config
.
get
(
"
obj_path
"
)
is
not
None
:
            
self
.
mozproxy_dir
=
self
.
config
.
get
(
"
obj_path
"
)
        
else
:
            
self
.
mozproxy_dir
=
os
.
path
.
dirname
(
                
os
.
path
.
dirname
(
os
.
environ
[
"
MOZ_UPLOAD_DIR
"
]
)
            
)
        
self
.
mozproxy_dir
=
os
.
path
.
join
(
self
.
mozproxy_dir
"
testing
"
"
mozproxy
"
)
        
self
.
upload_dir
=
os
.
environ
.
get
(
"
MOZ_UPLOAD_DIR
"
self
.
mozproxy_dir
)
        
LOG
.
info
(
            
"
mozproxy_dir
used
for
mitmproxy
downloads
and
exe
files
:
%
s
"
            
%
self
.
mozproxy_dir
        
)
        
os
.
environ
[
"
MOZPROXY_DIR
"
]
=
self
.
mozproxy_dir
    
def
start
(
self
)
:
        
self
.
download
(
)
        
self
.
mitmdump_path
=
os
.
path
.
join
(
self
.
mozproxy_dir
"
mitmdump
"
)
        
self
.
start_mitmproxy_playback
(
self
.
mitmdump_path
self
.
browser_path
)
        
try
:
            
self
.
setup
(
)
        
except
Exception
:
            
self
.
stop
(
)
            
raise
    
def
download
(
self
)
:
        
"
"
"
Download
and
unpack
mitmproxy
binary
and
pageset
using
tooltool
"
"
"
        
if
not
os
.
path
.
exists
(
self
.
mozproxy_dir
)
:
            
os
.
makedirs
(
self
.
mozproxy_dir
)
        
LOG
.
info
(
"
downloading
mitmproxy
binary
"
)
        
_manifest
=
os
.
path
.
join
(
here
self
.
config
[
"
playback_binary_manifest
"
]
)
        
transformed_manifest
=
transform_platform
(
_manifest
self
.
config
[
"
platform
"
]
)
        
tooltool_download
(
            
transformed_manifest
self
.
config
[
"
run_local
"
]
self
.
mozproxy_dir
        
)
        
if
"
playback_pageset_manifest
"
in
self
.
config
:
            
LOG
.
info
(
"
downloading
mitmproxy
pageset
"
)
            
_manifest
=
self
.
config
[
"
playback_pageset_manifest
"
]
            
transformed_manifest
=
transform_platform
(
                
_manifest
self
.
config
[
"
platform
"
]
            
)
            
tooltool_download
(
                
transformed_manifest
self
.
config
[
"
run_local
"
]
self
.
mozproxy_dir
            
)
        
if
"
playback_artifacts
"
in
self
.
config
:
            
artifacts
=
self
.
config
[
"
playback_artifacts
"
]
.
split
(
"
"
)
            
for
artifact
in
artifacts
:
                
artifact
=
artifact
.
strip
(
)
                
if
not
artifact
:
                    
continue
                
artifact_name
=
artifact
.
split
(
"
/
"
)
[
-
1
]
                
dest
=
os
.
path
.
join
(
self
.
mozproxy_dir
artifact_name
)
                
download_file_from_url
(
artifact
dest
extract
=
True
)
    
def
stop
(
self
)
:
        
self
.
stop_mitmproxy_playback
(
)
    
def
start_mitmproxy_playback
(
self
mitmdump_path
browser_path
)
:
        
"
"
"
Startup
mitmproxy
and
replay
the
specified
flow
file
"
"
"
        
if
self
.
mitmproxy_proc
is
not
None
:
            
raise
Exception
(
"
Proxy
already
started
.
"
)
        
LOG
.
info
(
"
mitmdump
path
:
%
s
"
%
mitmdump_path
)
        
LOG
.
info
(
"
browser
path
:
%
s
"
%
browser_path
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
PATH
"
]
=
os
.
path
.
dirname
(
browser_path
)
+
os
.
pathsep
+
env
[
"
PATH
"
]
        
command
=
[
mitmdump_path
]
        
if
"
playback_tool_args
"
in
self
.
config
:
            
command
.
extend
(
self
.
config
[
"
playback_tool_args
"
]
)
        
LOG
.
info
(
"
Starting
mitmproxy
playback
using
env
path
:
%
s
"
%
env
[
"
PATH
"
]
)
        
LOG
.
info
(
"
Starting
mitmproxy
playback
using
command
:
%
s
"
%
"
"
.
join
(
command
)
)
        
self
.
mitmproxy_proc
=
ProcessHandler
(
command
                                             
logfile
=
os
.
path
.
join
(
self
.
upload_dir
                                                                  
"
mitmproxy
.
log
"
)
                                             
env
=
env
)
        
self
.
mitmproxy_proc
.
run
(
)
        
end_time
=
time
.
time
(
)
+
MITMDUMP_COMMAND_TIMEOUT
        
ready
=
False
        
while
time
.
time
(
)
<
end_time
:
            
ready
=
self
.
check_proxy
(
)
            
if
ready
:
                
LOG
.
info
(
                    
"
Mitmproxy
playback
successfully
started
as
pid
%
d
"
                    
%
self
.
mitmproxy_proc
.
pid
                
)
                
return
            
time
.
sleep
(
0
.
25
)
        
LOG
.
error
(
"
Aborting
:
Mitmproxy
process
did
not
startup
"
)
        
self
.
stop_mitmproxy_playback
(
)
        
sys
.
exit
(
)
    
def
stop_mitmproxy_playback
(
self
)
:
        
"
"
"
Stop
the
mitproxy
server
playback
"
"
"
        
if
self
.
mitmproxy_proc
is
None
or
self
.
mitmproxy_proc
.
poll
(
)
is
not
None
:
            
return
        
LOG
.
info
(
            
"
Stopping
mitmproxy
playback
killing
process
%
d
"
%
self
.
mitmproxy_proc
.
pid
        
)
        
exit_code
=
self
.
mitmproxy_proc
.
kill
(
)
        
if
exit_code
!
=
0
:
            
if
exit_code
is
None
:
                
LOG
.
error
(
"
Failed
to
kill
the
mitmproxy
playback
process
"
)
            
else
:
                
LOG
.
error
(
"
Mitmproxy
exited
with
error
code
%
d
"
%
exit_code
)
        
else
:
            
LOG
.
info
(
"
Successfully
killed
the
mitmproxy
playback
process
"
)
        
self
.
mitmproxy_proc
=
None
    
def
check_proxy
(
self
host
=
"
localhost
"
port
=
8080
)
:
        
s
=
socket
.
socket
(
socket
.
AF_INET
socket
.
SOCK_STREAM
)
        
try
:
            
s
.
connect
(
(
host
port
)
)
            
s
.
shutdown
(
socket
.
SHUT_RDWR
)
            
s
.
close
(
)
            
return
True
        
except
socket
.
error
:
            
return
False
class
MitmproxyDesktop
(
Mitmproxy
)
:
    
def
__init__
(
self
config
)
:
        
Mitmproxy
.
__init__
(
self
config
)
    
def
setup
(
self
)
:
        
"
"
"
        
Installs
certificates
.
        
For
Firefox
we
need
to
install
the
generated
mitmproxy
CA
cert
.
For
        
Chromium
this
is
not
necessary
as
it
will
be
started
with
the
        
-
-
ignore
-
certificate
-
errors
cmd
line
arg
.
        
"
"
"
        
if
not
self
.
config
[
"
app
"
]
=
=
"
firefox
"
:
            
return
        
self
.
install_mitmproxy_cert
(
self
.
browser_path
)
    
def
install_mitmproxy_cert
(
self
browser_path
)
:
        
"
"
"
Install
the
CA
certificate
generated
by
mitmproxy
into
Firefox
        
1
.
Create
a
dir
called
'
distribution
'
in
the
same
directory
as
the
Firefox
executable
        
2
.
Create
the
policies
.
json
file
inside
that
folder
;
which
points
to
the
certificate
           
location
and
turns
on
the
the
browser
proxy
settings
        
"
"
"
        
LOG
.
info
(
"
Installing
mitmproxy
CA
certficate
into
Firefox
"
)
        
self
.
policies_dir
=
os
.
path
.
dirname
(
browser_path
)
        
if
"
mac
"
in
self
.
config
[
"
platform
"
]
:
            
self
.
policies_dir
=
os
.
path
.
join
(
self
.
policies_dir
[
:
-
6
]
"
Resources
"
)
        
self
.
policies_dir
=
os
.
path
.
join
(
self
.
policies_dir
"
distribution
"
)
        
self
.
cert_path
=
DEFAULT_CERT_PATH
        
if
mozinfo
.
os
=
=
"
win
"
:
            
self
.
cert_path
=
self
.
cert_path
.
replace
(
"
\
\
"
"
\
\
\
\
"
)
        
if
not
os
.
path
.
exists
(
self
.
policies_dir
)
:
            
LOG
.
info
(
"
creating
folder
:
%
s
"
%
self
.
policies_dir
)
            
os
.
makedirs
(
self
.
policies_dir
)
        
else
:
            
LOG
.
info
(
"
folder
already
exists
:
%
s
"
%
self
.
policies_dir
)
        
self
.
write_policies_json
(
            
self
.
policies_dir
            
policies_content
=
POLICIES_CONTENT_ON
            
%
{
"
cert
"
:
self
.
cert_path
"
host
"
:
self
.
config
[
"
host
"
]
}
        
)
        
if
not
self
.
is_mitmproxy_cert_installed
(
)
:
            
LOG
.
error
(
                
"
Aborting
:
failed
to
install
mitmproxy
CA
cert
into
Firefox
desktop
"
            
)
            
self
.
stop_mitmproxy_playback
(
)
            
sys
.
exit
(
)
    
def
write_policies_json
(
self
location
policies_content
)
:
        
policies_file
=
os
.
path
.
join
(
location
"
policies
.
json
"
)
        
LOG
.
info
(
"
writing
:
%
s
"
%
policies_file
)
        
with
open
(
policies_file
"
w
"
)
as
fd
:
            
fd
.
write
(
policies_content
)
    
def
read_policies_json
(
self
location
)
:
        
policies_file
=
os
.
path
.
join
(
location
"
policies
.
json
"
)
        
LOG
.
info
(
"
reading
:
%
s
"
%
policies_file
)
        
with
open
(
policies_file
"
r
"
)
as
fd
:
            
return
fd
.
read
(
)
    
def
is_mitmproxy_cert_installed
(
self
)
:
        
"
"
"
Verify
mitmxproy
CA
cert
was
added
to
Firefox
"
"
"
        
try
:
            
contents
=
self
.
read_policies_json
(
self
.
policies_dir
)
            
LOG
.
info
(
"
Firefox
policies
file
contents
:
"
)
            
LOG
.
info
(
contents
)
            
if
(
                
POLICIES_CONTENT_ON
                
%
{
"
cert
"
:
self
.
cert_path
"
host
"
:
self
.
config
[
"
host
"
]
}
            
)
in
contents
:
                
LOG
.
info
(
"
Verified
mitmproxy
CA
certificate
is
installed
in
Firefox
"
)
            
else
:
                
return
False
        
except
Exception
as
e
:
            
LOG
.
info
(
"
failed
to
read
Firefox
policies
file
exeption
:
%
s
"
%
e
)
            
return
False
        
return
True
    
def
stop
(
self
)
:
        
self
.
stop_mitmproxy_playback
(
)
        
self
.
turn_off_browser_proxy
(
)
    
def
turn_off_browser_proxy
(
self
)
:
        
"
"
"
Turn
off
the
browser
proxy
that
was
used
for
mitmproxy
playback
.
In
Firefox
        
we
need
to
change
the
autoconfig
files
to
revert
the
proxy
;
for
Chromium
the
proxy
        
was
setup
on
the
cmd
line
so
nothing
is
required
here
.
"
"
"
        
if
self
.
config
[
"
app
"
]
=
=
"
firefox
"
and
self
.
policies_dir
is
not
None
:
            
LOG
.
info
(
"
Turning
off
the
browser
proxy
"
)
            
self
.
write_policies_json
(
                
self
.
policies_dir
policies_content
=
POLICIES_CONTENT_OFF
            
)
class
MitmproxyAndroid
(
Mitmproxy
)
:
    
def
__init__
(
self
config
android_device
)
:
        
Mitmproxy
.
__init__
(
self
config
)
        
self
.
android_device
=
android_device
    
property
    
def
certutil_sleep_seconds
(
self
)
:
        
"
"
"
Time
to
sleep
in
seconds
after
issuing
a
certutil
command
.
"
"
"
        
return
10
if
not
self
.
config
[
'
run_local
'
]
else
1
    
def
setup
(
self
)
:
        
"
"
"
For
geckoview
we
need
to
install
the
generated
mitmproxy
CA
cert
"
"
"
        
if
self
.
config
[
"
app
"
]
in
[
"
geckoview
"
"
refbrow
"
"
fenix
"
]
:
            
self
.
install_mitmproxy_cert
(
self
.
browser_path
)
    
def
install_mitmproxy_cert
(
self
browser_path
)
:
        
"
"
"
Install
the
CA
certificate
generated
by
mitmproxy
into
geckoview
android
        
If
running
locally
:
        
1
.
Will
use
the
certutil
tool
from
the
local
Firefox
desktop
build
        
If
running
in
production
:
        
1
.
Get
the
tooltools
manifest
file
for
downloading
hostutils
(
contains
certutil
)
        
2
.
Get
the
certutil
tool
by
downloading
hostutils
using
the
tooltool
manifest
        
Then
both
locally
and
in
production
:
        
1
.
Create
an
NSS
certificate
database
in
the
geckoview
browser
profile
dir
only
           
if
it
doesn
'
t
already
exist
.
Use
this
certutil
command
:
           
certutil
-
N
-
d
sql
:
<
path
to
profile
>
-
-
empty
-
password
        
2
.
Import
the
mitmproxy
certificate
into
the
database
i
.
e
.
:
           
certutil
-
A
-
d
sql
:
<
path
to
profile
>
-
n
"
some
nickname
"
-
t
TC
-
a
-
i
<
path
to
CA
.
pem
>
        
"
"
"
        
if
self
.
config
[
'
run_local
'
]
:
            
self
.
certutil
=
os
.
path
.
join
(
os
.
environ
[
'
MOZ_HOST_BIN
'
]
'
certutil
'
)
            
if
not
(
os
.
path
.
isfile
(
self
.
certutil
)
and
os
.
access
(
self
.
certutil
os
.
X_OK
)
)
:
                
LOG
.
critical
(
"
Abort
:
unable
to
execute
certutil
:
{
}
"
.
format
(
self
.
certutil
)
)
                
raise
            
self
.
certutil
=
os
.
environ
[
'
MOZ_HOST_BIN
'
]
            
os
.
environ
[
'
LD_LIBRARY_PATH
'
]
=
self
.
certutil
        
else
:
            
LOG
.
info
(
"
downloading
certutil
binary
(
hostutils
)
"
)
            
if
os
.
environ
.
get
(
"
GECKO_HEAD_REPOSITORY
"
None
)
is
None
:
                
LOG
.
critical
(
"
Abort
:
unable
to
get
GECKO_HEAD_REPOSITORY
"
)
                
raise
            
if
os
.
environ
.
get
(
"
GECKO_HEAD_REV
"
None
)
is
None
:
                
LOG
.
critical
(
"
Abort
:
unable
to
get
GECKO_HEAD_REV
"
)
                
raise
            
if
os
.
environ
.
get
(
"
HOSTUTILS_MANIFEST_PATH
"
None
)
is
not
None
:
                
manifest_url
=
os
.
path
.
join
(
                    
os
.
environ
[
"
GECKO_HEAD_REPOSITORY
"
]
                    
"
raw
-
file
"
                    
os
.
environ
[
"
GECKO_HEAD_REV
"
]
                    
os
.
environ
[
"
HOSTUTILS_MANIFEST_PATH
"
]
                
)
            
else
:
                
LOG
.
critical
(
"
Abort
:
unable
to
get
HOSTUTILS_MANIFEST_PATH
!
"
)
                
raise
            
_dest
=
os
.
path
.
join
(
self
.
mozproxy_dir
"
hostutils
.
manifest
"
)
            
have_manifest
=
download_file_from_url
(
manifest_url
_dest
)
            
if
not
have_manifest
:
                
LOG
.
critical
(
"
failed
to
download
the
hostutils
tooltool
manifest
"
)
                
raise
            
tooltool_download
(
_dest
self
.
config
[
"
run_local
"
]
self
.
mozproxy_dir
)
            
self
.
certutil
=
glob
.
glob
(
                
os
.
path
.
join
(
self
.
mozproxy_dir
"
host
-
utils
*
[
!
z
]
"
)
            
)
[
0
]
            
os
.
environ
[
"
LD_LIBRARY_PATH
"
]
=
self
.
certutil
        
bin_suffix
=
mozinfo
.
info
.
get
(
"
bin_suffix
"
"
"
)
        
self
.
certutil
=
os
.
path
.
join
(
self
.
certutil
"
certutil
"
+
bin_suffix
)
        
if
os
.
path
.
isfile
(
self
.
certutil
)
:
            
LOG
.
info
(
"
certutil
is
found
at
:
%
s
"
%
self
.
certutil
)
        
else
:
            
LOG
.
critical
(
"
unable
to
find
certutil
at
%
s
"
%
self
.
certutil
)
            
raise
        
self
.
local_cert_path
=
DEFAULT_CERT_PATH
        
LOG
.
info
(
            
"
checking
if
the
nss
cert
db
already
exists
in
the
android
browser
profile
"
        
)
        
param1
=
"
sql
:
%
s
/
"
%
self
.
config
[
"
local_profile_dir
"
]
        
command
=
[
self
.
certutil
"
-
d
"
param1
"
-
L
"
]
        
try
:
            
subprocess
.
check_output
(
command
env
=
os
.
environ
.
copy
(
)
)
            
LOG
.
info
(
"
the
nss
cert
db
already
exists
"
)
            
cert_db_exists
=
True
        
except
subprocess
.
CalledProcessError
:
            
LOG
.
info
(
"
nss
cert
db
doesn
'
t
exist
yet
"
)
            
cert_db_exists
=
False
        
time
.
sleep
(
self
.
certutil_sleep_seconds
)
        
if
not
cert_db_exists
:
            
param1
=
"
sql
:
%
s
/
"
%
self
.
config
[
"
local_profile_dir
"
]
            
command
=
[
self
.
certutil
"
-
N
"
"
-
v
"
"
-
d
"
param1
"
-
-
empty
-
password
"
]
            
LOG
.
info
(
"
creating
nss
cert
database
using
command
:
%
s
"
%
"
"
.
join
(
command
)
)
            
cmd_proc
=
subprocess
.
Popen
(
command
env
=
os
.
environ
.
copy
(
)
)
            
time
.
sleep
(
self
.
certutil_sleep_seconds
)
            
cmd_terminated
=
cmd_proc
.
poll
(
)
            
if
cmd_terminated
is
None
:
                
LOG
.
critical
(
"
nss
cert
db
creation
command
failed
to
complete
"
)
                
raise
        
command
=
[
            
self
.
certutil
            
"
-
A
"
            
"
-
d
"
            
param1
            
"
-
n
"
            
"
mitmproxy
-
cert
"
            
"
-
t
"
            
"
TC
"
            
"
-
a
"
            
"
-
i
"
            
self
.
local_cert_path
        
]
        
LOG
.
info
(
            
"
importing
mitmproxy
cert
into
db
using
command
:
%
s
"
%
"
"
.
join
(
command
)
        
)
        
cmd_proc
=
subprocess
.
Popen
(
command
env
=
os
.
environ
.
copy
(
)
)
        
time
.
sleep
(
self
.
certutil_sleep_seconds
)
        
cmd_terminated
=
cmd_proc
.
poll
(
)
        
if
cmd_terminated
is
None
:
            
LOG
.
critical
(
                
"
command
to
import
mitmproxy
cert
into
cert
db
failed
to
complete
"
            
)
        
if
not
self
.
is_mitmproxy_cert_installed
(
)
:
            
LOG
.
error
(
"
Aborting
:
failed
to
install
mitmproxy
CA
cert
into
Firefox
"
)
            
self
.
stop_mitmproxy_playback
(
)
            
sys
.
exit
(
)
    
def
is_mitmproxy_cert_installed
(
self
)
:
        
"
"
"
Verify
mitmxproy
CA
cert
was
added
to
Firefox
on
android
"
"
"
        
LOG
.
info
(
"
verifying
that
the
mitmproxy
ca
cert
is
installed
on
android
"
)
        
LOG
.
info
(
            
"
getting
the
list
of
certs
in
the
nss
cert
db
in
the
android
browser
profile
"
        
)
        
param1
=
"
sql
:
%
s
/
"
%
self
.
config
[
"
local_profile_dir
"
]
        
command
=
[
self
.
certutil
"
-
d
"
param1
"
-
L
"
]
        
try
:
            
cmd_output
=
subprocess
.
check_output
(
command
env
=
os
.
environ
.
copy
(
)
)
        
except
subprocess
.
CalledProcessError
:
            
LOG
.
critical
(
"
certutil
command
failed
"
)
            
raise
        
time
.
sleep
(
self
.
certutil_sleep_seconds
)
        
LOG
.
info
(
cmd_output
)
        
if
"
mitmproxy
-
cert
"
in
cmd_output
:
            
LOG
.
info
(
                
"
verfied
the
mitmproxy
-
cert
is
installed
in
the
nss
cert
db
on
android
"
            
)
            
return
True
        
return
False
