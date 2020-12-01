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
json
import
os
import
signal
import
socket
import
sys
import
time
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
recordings
import
RecordingFile
from
mozproxy
.
utils
import
(
    
download_file_from_url
    
transform_platform
    
tooltool_download
    
get_available_port
    
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
def
normalize_path
(
path
)
:
    
path
=
os
.
path
.
normpath
(
path
)
    
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
        
return
path
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
\
\
"
)
    
return
path
MITMDUMP_COMMAND_TIMEOUT
=
30
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
host
=
(
            
"
127
.
0
.
0
.
1
"
if
"
localhost
"
in
self
.
config
[
"
host
"
]
else
self
.
config
[
"
host
"
]
        
)
        
self
.
port
=
None
        
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
recordings
=
[
]
        
self
.
browser_path
=
"
"
        
if
config
.
get
(
"
binary
"
None
)
:
            
self
.
browser_path
=
os
.
path
.
normpath
(
config
.
get
(
"
binary
"
)
)
        
self
.
policies_dir
=
None
        
self
.
ignore_mitmdump_exit_failure
=
config
.
get
(
            
"
ignore_mitmdump_exit_failure
"
False
        
)
        
self
.
recording_paths
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
playback_version
"
)
is
None
:
            
LOG
.
error
(
                
"
mitmproxy
was
not
provided
with
a
'
playback_version
'
"
                
"
Please
provide
a
valid
playback
version
"
            
)
            
raise
Exception
(
"
playback_version
not
specified
!
"
)
        
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
        
LOG
.
info
(
"
Playback
tool
:
%
s
"
%
self
.
config
[
"
playback_tool
"
]
)
        
LOG
.
info
(
"
Playback
tool
version
:
%
s
"
%
self
.
config
[
"
playback_version
"
]
)
    
def
download_mitm_bin
(
self
)
:
        
manifest
=
os
.
path
.
join
(
            
here
            
"
manifests
"
            
"
mitmproxy
-
rel
-
bin
-
%
s
-
{
platform
}
.
manifest
"
            
%
self
.
config
[
"
playback_version
"
]
        
)
        
transformed_manifest
=
transform_platform
(
manifest
self
.
config
[
"
platform
"
]
)
        
self
.
mitmdump_path
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
join
(
                
self
.
mozproxy_dir
                
"
mitmdump
-
%
s
"
%
self
.
config
[
"
playback_version
"
]
                
"
mitmdump
"
            
)
        
)
        
if
os
.
path
.
exists
(
self
.
mitmdump_path
)
:
            
LOG
.
info
(
"
mitmproxy
binary
already
exists
.
Skipping
download
"
)
        
else
:
            
download_path
=
os
.
path
.
dirname
(
self
.
mitmdump_path
)
            
LOG
.
info
(
"
create
mitmproxy
%
s
dir
"
%
self
.
config
[
"
playback_version
"
]
)
            
if
not
os
.
path
.
exists
(
download_path
)
:
                
os
.
makedirs
(
download_path
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
download_path
            
)
    
def
download_manifest_file
(
self
manifest_path
)
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
        
tooltool_download
(
manifest_path
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
        
with
open
(
manifest_path
)
as
manifest_file
:
            
manifest
=
json
.
load
(
manifest_file
)
            
for
file
in
manifest
:
                
zip_path
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
file
[
"
filename
"
]
)
                
LOG
.
info
(
"
Adding
%
s
to
recording
list
"
%
zip_path
)
                
self
.
recordings
.
append
(
RecordingFile
(
zip_path
)
)
    
def
download_playback_files
(
self
)
:
        
if
"
playback_files
"
not
in
self
.
config
:
            
LOG
.
error
(
                
"
playback_files
value
was
not
provided
.
Proxy
service
wont
'
start
"
            
)
            
raise
Exception
(
"
Please
provide
a
playback_files
list
.
"
)
        
if
not
isinstance
(
self
.
config
[
"
playback_files
"
]
list
)
:
            
LOG
.
error
(
"
playback_files
should
be
a
list
"
)
            
raise
Exception
(
"
playback_files
should
be
a
list
"
)
        
for
playback_file
in
self
.
config
[
"
playback_files
"
]
:
            
if
playback_file
.
startswith
(
"
https
:
/
/
"
)
and
"
mozilla
.
com
"
in
playback_file
:
                
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
os
.
path
.
basename
(
playback_file
)
)
                
download_file_from_url
(
playback_file
self
.
mozproxy_dir
extract
=
False
)
                
LOG
.
info
(
"
Adding
%
s
to
recording
list
"
%
dest
)
                
self
.
recordings
.
append
(
RecordingFile
(
dest
)
)
                
continue
            
if
not
os
.
path
.
exists
(
playback_file
)
:
                
LOG
.
error
(
                    
"
Zip
or
manifest
file
path
(
%
s
)
does
not
exist
.
Please
provide
a
valid
path
!
"
                    
%
playback_file
                
)
                
raise
Exception
(
"
Zip
or
manifest
file
path
does
not
exist
"
)
            
if
os
.
path
.
splitext
(
playback_file
)
[
1
]
=
=
"
.
zip
"
:
                
LOG
.
info
(
"
Adding
%
s
to
recording
list
"
%
playback_file
)
                
self
.
recordings
.
append
(
RecordingFile
(
playback_file
)
)
            
elif
os
.
path
.
splitext
(
playback_file
)
[
1
]
=
=
"
.
manifest
"
:
                
self
.
download_manifest_file
(
playback_file
)
    
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
        
self
.
download_mitm_bin
(
)
        
self
.
download_playback_files
(
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
wait
(
self
timeout
=
1
)
:
        
"
"
"
Wait
until
the
mitmproxy
process
has
terminated
.
"
"
"
        
while
True
:
            
returncode
=
self
.
mitmproxy_proc
.
wait
(
timeout
)
            
if
returncode
is
not
None
:
                
return
returncode
    
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
            
try
:
                
self
.
stop
(
)
            
except
Exception
:
                
LOG
.
error
(
"
MitmProxy
failed
to
STOP
.
"
exc_info
=
True
)
            
LOG
.
error
(
"
Setup
of
MitmProxy
failed
.
"
exc_info
=
True
)
            
raise
    
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
        
self
.
port
=
get_available_port
(
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
        
command
.
extend
(
[
"
-
-
listen
-
host
"
self
.
host
"
-
-
listen
-
port
"
str
(
self
.
port
)
]
)
        
if
self
.
config
.
get
(
"
playback_record
"
)
:
            
command
.
extend
(
[
"
-
w
"
self
.
config
.
get
(
"
playback_record
"
)
]
)
        
elif
len
(
self
.
recordings
)
>
0
:
            
script
=
os
.
path
.
join
(
                
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
realpath
(
__file__
)
)
                
"
scripts
"
                
"
alternate
-
server
-
replay
.
py
"
            
)
            
self
.
recording_paths
=
[
                
normalize_path
(
recording
.
recording_path
)
                
for
recording
in
self
.
recordings
            
]
            
if
self
.
config
[
"
playback_version
"
]
in
[
"
4
.
0
.
4
"
"
5
.
1
.
1
"
]
:
                
args
=
[
                    
"
-
v
"
                    
"
-
-
set
"
                    
"
upstream_cert
=
false
"
                    
"
-
-
set
"
                    
"
upload_dir
=
"
+
normalize_path
(
self
.
upload_dir
)
                    
"
-
-
set
"
                    
"
websocket
=
false
"
                    
"
-
-
set
"
                    
"
server_replay_files
=
{
}
"
.
format
(
"
"
.
join
(
self
.
recording_paths
)
)
                    
"
-
-
scripts
"
                    
normalize_path
(
script
)
                
]
                
command
.
extend
(
args
)
            
else
:
                
raise
Exception
(
"
Mitmproxy
version
is
unknown
!
"
)
        
else
:
            
raise
Exception
(
                
"
Mitmproxy
can
'
t
start
playback
!
Playback
settings
missing
.
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
        
if
not
os
.
path
.
dirname
(
self
.
browser_path
)
in
env
[
"
PATH
"
]
:
            
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
self
.
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
            
processStderrLine
=
LOG
.
error
            
storeOutput
=
False
        
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
host
=
self
.
host
port
=
self
.
port
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
on
%
s
:
%
d
as
pid
%
d
"
                    
%
(
self
.
host
self
.
port
self
.
mitmproxy_proc
.
pid
)
                
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
1
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
            
LOG
.
info
(
"
Sending
CTRL_BREAK_EVENT
to
mitmproxy
"
)
            
os
.
kill
(
self
.
mitmproxy_proc
.
pid
signal
.
CTRL_BREAK_EVENT
)
            
time
.
sleep
(
2
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
        
self
.
mitmproxy_proc
=
None
        
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
                
return
            
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
                
from
mozprocess
.
winprocess
import
ERROR_CONTROL_C_EXIT
                
if
exit_code
=
=
ERROR_CONTROL_C_EXIT
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
                        
"
with
exit
code
%
d
"
%
exit_code
                    
)
                    
return
            
log_func
=
LOG
.
error
            
if
self
.
ignore_mitmdump_exit_failure
:
                
log_func
=
LOG
.
info
            
log_func
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
    
def
check_proxy
(
self
host
port
)
:
        
"
"
"
Check
that
mitmproxy
process
is
working
by
doing
a
socket
call
using
the
proxy
settings
        
:
param
host
:
Host
of
the
proxy
server
        
:
param
port
:
Port
of
the
proxy
server
        
:
return
:
True
if
the
proxy
service
is
working
        
"
"
"
        
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
    
def
confidence
(
self
)
:
        
"
"
"
Extract
confidence
metrics
from
the
netlocs
file
        
and
convert
them
to
perftest
results
        
"
"
"
        
if
len
(
self
.
recordings
)
=
=
0
:
            
LOG
.
warning
(
                
"
Proxy
service
did
not
load
a
recording
file
.
"
                
"
Confidence
metrics
will
nt
be
generated
"
            
)
            
return
        
file_name
=
(
            
"
mitm_netlocs_
%
s
.
json
"
            
%
os
.
path
.
splitext
(
os
.
path
.
basename
(
self
.
recordings
[
0
]
.
recording_path
)
)
[
0
]
        
)
        
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
join
(
self
.
upload_dir
file_name
)
)
        
if
os
.
path
.
exists
(
path
)
:
            
try
:
                
LOG
.
info
(
"
Reading
confidence
values
from
:
%
s
"
%
path
)
                
with
open
(
path
"
r
"
)
as
f
:
                    
data
=
json
.
load
(
f
)
                    
return
{
                        
"
replay
-
confidence
"
:
{
                            
"
values
"
:
data
[
"
replay
-
confidence
"
]
                            
"
subtest
-
prefix
-
type
"
:
False
                            
"
unit
"
:
"
%
"
                            
"
shouldAlert
"
:
False
                            
"
lowerIsBetter
"
:
False
                        
}
                        
"
recording
-
proportion
-
used
"
:
{
                            
"
values
"
:
data
[
"
recording
-
proportion
-
used
"
]
                            
"
subtest
-
prefix
-
type
"
:
False
                            
"
unit
"
:
"
%
"
                            
"
shouldAlert
"
:
False
                            
"
lowerIsBetter
"
:
False
                        
}
                        
"
not
-
replayed
"
:
{
                            
"
values
"
:
data
[
"
not
-
replayed
"
]
                            
"
subtest
-
prefix
-
type
"
:
False
                            
"
shouldAlert
"
:
False
                            
"
unit
"
:
"
a
.
u
.
"
                        
}
                        
"
replayed
"
:
{
                            
"
values
"
:
data
[
"
replayed
"
]
                            
"
subtest
-
prefix
-
type
"
:
False
                            
"
unit
"
:
"
a
.
u
.
"
                            
"
shouldAlert
"
:
False
                            
"
lowerIsBetter
"
:
False
                        
}
                    
}
            
except
Exception
:
                
LOG
.
info
(
"
Can
'
t
read
netlocs
file
!
"
exc_info
=
True
)
                
return
None
        
else
:
            
LOG
.
info
(
"
Netlocs
file
is
not
available
!
Cant
find
%
s
"
%
path
)
            
return
None
