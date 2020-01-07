from
__future__
import
absolute_import
import
os
import
sys
import
tempfile
import
time
import
traceback
from
copy
import
deepcopy
import
mozversion
from
mozprofile
import
Profile
from
mozrunner
import
Runner
FennecEmulatorRunner
from
six
import
reraise
from
.
import
errors
class
GeckoInstance
(
object
)
:
    
required_prefs
=
{
        
"
app
.
normandy
.
api_url
"
:
"
"
        
"
apz
.
content_response_timeout
"
:
60000
        
"
datareporting
.
healthreport
.
about
.
reportUrl
"
:
"
http
:
/
/
%
(
server
)
s
/
dummy
/
abouthealthreport
/
"
        
"
datareporting
.
healthreport
.
documentServerURI
"
:
"
http
:
/
/
%
(
server
)
s
/
dummy
/
healthreport
/
"
        
"
datareporting
.
policy
.
dataSubmissionPolicyBypassNotification
"
:
True
        
"
dom
.
disable_beforeunload
"
:
True
        
"
dom
.
ipc
.
reportProcessHangs
"
:
False
        
"
dom
.
max_chrome_script_run_time
"
:
0
        
"
dom
.
max_script_run_time
"
:
0
        
"
extensions
.
autoDisableScopes
"
:
0
        
"
extensions
.
enabledScopes
"
:
5
        
"
extensions
.
getAddons
.
cache
.
enabled
"
:
False
        
"
extensions
.
installDistroAddons
"
:
False
        
"
extensions
.
shield
-
recipe
-
client
.
api_url
"
:
"
"
        
"
extensions
.
showMismatchUI
"
:
False
        
"
extensions
.
update
.
enabled
"
:
False
        
"
extensions
.
update
.
notifyUser
"
:
False
        
"
extensions
.
webservice
.
discoverURL
"
:
"
http
:
/
/
%
(
server
)
s
/
dummy
/
discoveryURL
"
        
"
focusmanager
.
testmode
"
:
True
        
"
general
.
useragent
.
updates
.
enabled
"
:
False
        
"
geo
.
provider
.
testing
"
:
True
        
"
geo
.
wifi
.
scan
"
:
False
        
"
javascript
.
options
.
showInConsole
"
:
True
        
"
marionette
.
enabled
"
:
True
        
"
marionette
.
defaultPrefs
.
enabled
"
:
True
        
"
marionette
.
prefs
.
recommended
"
:
False
        
"
media
.
gmp
-
manager
.
updateEnabled
"
:
False
        
"
media
.
volume_scale
"
:
"
0
.
01
"
        
"
network
.
http
.
prompt
-
temp
-
redirect
"
:
False
        
"
network
.
http
.
speculative
-
parallel
-
limit
"
:
0
        
"
network
.
manage
-
offline
-
status
"
:
False
        
"
network
.
sntp
.
pools
"
:
"
%
(
server
)
s
"
        
"
security
.
notification_enable_delay
"
:
0
        
"
services
.
settings
.
server
"
:
"
http
:
/
/
%
(
server
)
s
/
dummy
/
blocklist
/
"
        
"
signon
.
rememberSignons
"
:
False
        
"
toolkit
.
startup
.
max_resumed_crashes
"
:
-
1
        
"
toolkit
.
telemetry
.
server
"
:
"
https
:
/
/
%
(
server
)
s
/
dummy
/
telemetry
/
"
        
"
dom
.
file
.
createInChild
"
:
True
    
}
    
def
__init__
(
self
host
=
None
port
=
None
bin
=
None
profile
=
None
addons
=
None
                 
app_args
=
None
symbols_path
=
None
gecko_log
=
None
prefs
=
None
                 
workspace
=
None
verbose
=
0
headless
=
False
)
:
        
self
.
runner_class
=
Runner
        
self
.
app_args
=
app_args
or
[
]
        
self
.
runner
=
None
        
self
.
symbols_path
=
symbols_path
        
self
.
binary
=
bin
        
self
.
marionette_host
=
host
        
self
.
marionette_port
=
port
        
self
.
addons
=
addons
        
self
.
prefs
=
prefs
        
self
.
required_prefs
=
deepcopy
(
self
.
required_prefs
)
        
if
prefs
:
            
self
.
required_prefs
.
update
(
prefs
)
        
self
.
_gecko_log_option
=
gecko_log
        
self
.
_gecko_log
=
None
        
self
.
verbose
=
verbose
        
self
.
headless
=
headless
        
self
.
unresponsive_count
=
0
        
self
.
workspace
=
workspace
        
self
.
_profile
=
profile
    
property
    
def
gecko_log
(
self
)
:
        
if
self
.
_gecko_log
:
            
return
self
.
_gecko_log
        
path
=
self
.
_gecko_log_option
        
if
path
!
=
"
-
"
:
            
if
path
is
None
:
                
path
=
"
gecko
.
log
"
            
elif
os
.
path
.
isdir
(
path
)
:
                
fname
=
"
gecko
-
{
}
.
log
"
.
format
(
time
.
time
(
)
)
                
path
=
os
.
path
.
join
(
path
fname
)
            
path
=
os
.
path
.
realpath
(
path
)
            
if
os
.
access
(
path
os
.
F_OK
)
:
                
os
.
remove
(
path
)
        
self
.
_gecko_log
=
path
        
return
self
.
_gecko_log
    
property
    
def
profile
(
self
)
:
        
return
self
.
_profile
    
profile
.
setter
    
def
profile
(
self
value
)
:
        
self
.
_update_profile
(
value
)
    
def
_update_profile
(
self
profile
=
None
profile_name
=
None
)
:
        
"
"
"
Check
if
the
profile
has
to
be
created
or
replaced
        
:
param
profile
:
A
Profile
instance
to
be
used
.
        
:
param
name
:
Profile
name
to
be
used
in
the
path
.
        
"
"
"
        
if
self
.
runner
and
self
.
runner
.
is_running
(
)
:
            
raise
errors
.
MarionetteException
(
"
The
current
profile
can
only
be
updated
"
                                             
"
when
the
instance
is
not
running
"
)
        
if
isinstance
(
profile
Profile
)
:
            
if
hasattr
(
self
"
_profile
"
)
and
profile
is
self
.
_profile
:
                
return
        
else
:
            
profile_args
=
self
.
profile_args
            
profile_path
=
profile
            
if
isinstance
(
profile_path
basestring
)
:
                
profile_args
[
"
path_from
"
]
=
profile_path
                
profile_args
[
"
path_to
"
]
=
tempfile
.
mkdtemp
(
                    
suffix
=
u
"
.
{
}
"
.
format
(
profile_name
or
os
.
path
.
basename
(
profile_path
)
)
                    
dir
=
self
.
workspace
)
                
os
.
rmdir
(
profile_args
[
"
path_to
"
]
)
                
profile
=
Profile
.
clone
(
*
*
profile_args
)
            
else
:
                
profile_args
[
"
profile
"
]
=
tempfile
.
mkdtemp
(
                    
suffix
=
u
"
.
{
}
"
.
format
(
profile_name
or
"
mozrunner
"
)
                    
dir
=
self
.
workspace
)
                
profile
=
Profile
(
*
*
profile_args
)
                
profile
.
create_new
=
True
        
if
isinstance
(
self
.
profile
Profile
)
:
            
self
.
profile
.
cleanup
(
)
        
self
.
_profile
=
profile
    
def
switch_profile
(
self
profile_name
=
None
clone_from
=
None
)
:
        
"
"
"
Switch
the
profile
by
using
the
given
name
and
optionally
clone
it
.
        
Compared
to
:
attr
:
profile
this
method
allows
to
switch
the
profile
        
by
giving
control
over
the
profile
name
as
used
for
the
new
profile
.
It
        
also
always
creates
a
new
blank
profile
or
as
clone
of
an
existent
one
.
        
:
param
profile_name
:
Optional
name
of
the
profile
which
will
be
used
            
as
part
of
the
profile
path
(
folder
name
containing
the
profile
)
.
        
:
clone_from
:
Optional
if
specified
the
new
profile
will
be
cloned
            
based
on
the
given
profile
.
This
argument
can
be
an
instance
of
            
mozprofile
.
Profile
or
the
path
of
the
profile
.
        
"
"
"
        
if
isinstance
(
clone_from
Profile
)
:
            
clone_from
=
clone_from
.
profile
        
self
.
_update_profile
(
clone_from
profile_name
=
profile_name
)
    
property
    
def
profile_args
(
self
)
:
        
args
=
{
"
preferences
"
:
deepcopy
(
self
.
required_prefs
)
}
        
args
[
"
preferences
"
]
[
"
marionette
.
port
"
]
=
self
.
marionette_port
        
args
[
"
preferences
"
]
[
"
marionette
.
defaultPrefs
.
port
"
]
=
self
.
marionette_port
        
if
self
.
prefs
:
            
args
[
"
preferences
"
]
.
update
(
self
.
prefs
)
        
if
self
.
verbose
:
            
level
=
"
TRACE
"
if
self
.
verbose
>
=
2
else
"
DEBUG
"
            
args
[
"
preferences
"
]
[
"
marionette
.
log
.
level
"
]
=
level
            
args
[
"
preferences
"
]
[
"
marionette
.
logging
"
]
=
level
        
if
"
-
jsdebugger
"
in
self
.
app_args
:
            
args
[
"
preferences
"
]
.
update
(
{
                
"
devtools
.
browsertoolbox
.
panel
"
:
"
jsdebugger
"
                
"
devtools
.
debugger
.
remote
-
enabled
"
:
True
                
"
devtools
.
chrome
.
enabled
"
:
True
                
"
devtools
.
debugger
.
prompt
-
connection
"
:
False
                
"
marionette
.
debugging
.
clicktostart
"
:
True
            
}
)
        
if
self
.
addons
:
            
args
[
"
addons
"
]
=
self
.
addons
        
return
args
    
classmethod
    
def
create
(
cls
app
=
None
*
args
*
*
kwargs
)
:
        
try
:
            
if
not
app
and
kwargs
[
"
bin
"
]
is
not
None
:
                
app_id
=
mozversion
.
get_version
(
binary
=
kwargs
[
"
bin
"
]
)
[
"
application_id
"
]
                
app
=
app_ids
[
app_id
]
            
instance_class
=
apps
[
app
]
        
except
(
IOError
KeyError
)
:
            
exc
val
tb
=
sys
.
exc_info
(
)
            
msg
=
'
Application
"
{
0
}
"
unknown
(
should
be
one
of
{
1
}
)
'
            
reraise
(
NotImplementedError
msg
.
format
(
app
apps
.
keys
(
)
)
tb
)
        
return
instance_class
(
*
args
*
*
kwargs
)
    
def
start
(
self
)
:
        
self
.
_update_profile
(
self
.
profile
)
        
self
.
runner
=
self
.
runner_class
(
*
*
self
.
_get_runner_args
(
)
)
        
self
.
runner
.
start
(
)
    
def
_get_runner_args
(
self
)
:
        
process_args
=
{
            
"
processOutputLine
"
:
[
NullOutput
(
)
]
        
}
        
if
self
.
gecko_log
=
=
"
-
"
:
            
process_args
[
"
stream
"
]
=
sys
.
stdout
        
else
:
            
process_args
[
"
logfile
"
]
=
self
.
gecko_log
        
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
self
.
headless
:
            
env
[
"
MOZ_HEADLESS
"
]
=
"
1
"
            
env
[
"
DISPLAY
"
]
=
"
77
"
        
env
.
update
(
{
"
MOZ_CRASHREPORTER
"
:
"
1
"
                    
"
MOZ_CRASHREPORTER_NO_REPORT
"
:
"
1
"
                    
"
MOZ_CRASHREPORTER_SHUTDOWN
"
:
"
1
"
                    
}
)
        
return
{
            
"
binary
"
:
self
.
binary
            
"
profile
"
:
self
.
profile
            
"
cmdargs
"
:
[
"
-
no
-
remote
"
"
-
marionette
"
]
+
self
.
app_args
            
"
env
"
:
env
            
"
symbols_path
"
:
self
.
symbols_path
            
"
process_args
"
:
process_args
        
}
    
def
close
(
self
clean
=
False
)
:
        
"
"
"
        
Close
the
managed
Gecko
process
.
        
Depending
on
self
.
runner_class
setting
clean
to
True
may
also
kill
        
the
emulator
process
in
which
this
instance
is
running
.
        
:
param
clean
:
If
True
also
perform
runner
cleanup
.
        
"
"
"
        
if
self
.
runner
:
            
self
.
runner
.
stop
(
)
            
if
clean
:
                
self
.
runner
.
cleanup
(
)
        
if
clean
:
            
if
isinstance
(
self
.
profile
Profile
)
:
                
self
.
profile
.
cleanup
(
)
            
self
.
profile
=
None
    
def
restart
(
self
prefs
=
None
clean
=
True
)
:
        
"
"
"
        
Close
then
start
the
managed
Gecko
process
.
        
:
param
prefs
:
Dictionary
of
preference
names
and
values
.
        
:
param
clean
:
If
True
reset
the
profile
before
starting
.
        
"
"
"
        
if
prefs
:
            
self
.
prefs
=
prefs
        
else
:
            
self
.
prefs
=
None
        
self
.
close
(
clean
=
clean
)
        
self
.
start
(
)
class
FennecInstance
(
GeckoInstance
)
:
    
fennec_prefs
=
{
        
"
browser
.
dom
.
window
.
dump
.
enabled
"
:
True
        
"
browser
.
snippets
.
enabled
"
:
False
        
"
browser
.
snippets
.
syncPromo
.
enabled
"
:
False
        
"
browser
.
snippets
.
firstrunHomepage
.
enabled
"
:
False
        
"
browser
.
safebrowsing
.
blockedURIs
.
enabled
"
:
False
        
"
browser
.
safebrowsing
.
downloads
.
enabled
"
:
False
        
"
browser
.
safebrowsing
.
passwords
.
enabled
"
:
False
        
"
browser
.
safebrowsing
.
malware
.
enabled
"
:
False
        
"
browser
.
safebrowsing
.
phishing
.
enabled
"
:
False
        
"
browser
.
sessionstore
.
resume_from_crash
"
:
False
        
"
browser
.
tabs
.
remote
.
autostart
"
:
False
        
"
browser
.
tabs
.
disableBackgroundZombification
"
:
True
    
}
    
def
__init__
(
self
emulator_binary
=
None
avd_home
=
None
avd
=
None
                 
adb_path
=
None
serial
=
None
connect_to_running_emulator
=
False
                 
package_name
=
None
*
args
*
*
kwargs
)
:
        
super
(
FennecInstance
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
required_prefs
.
update
(
FennecInstance
.
fennec_prefs
)
        
self
.
runner_class
=
FennecEmulatorRunner
        
self
.
_package_name
=
package_name
        
self
.
emulator_binary
=
emulator_binary
        
self
.
avd_home
=
avd_home
        
self
.
adb_path
=
adb_path
        
self
.
avd
=
avd
        
self
.
serial
=
serial
        
self
.
connect_to_running_emulator
=
connect_to_running_emulator
    
property
    
def
package_name
(
self
)
:
        
"
"
"
        
Name
of
app
to
run
on
emulator
.
        
Note
that
FennecInstance
does
not
use
self
.
binary
        
"
"
"
        
if
self
.
_package_name
is
None
:
            
self
.
_package_name
=
"
org
.
mozilla
.
fennec
"
            
user
=
os
.
getenv
(
"
USER
"
)
            
if
user
:
                
self
.
_package_name
+
=
"
_
"
+
user
        
return
self
.
_package_name
    
def
start
(
self
)
:
        
self
.
_update_profile
(
self
.
profile
)
        
self
.
runner
=
self
.
runner_class
(
*
*
self
.
_get_runner_args
(
)
)
        
try
:
            
if
self
.
connect_to_running_emulator
:
                
self
.
runner
.
device
.
connect
(
)
            
self
.
runner
.
start
(
)
        
except
Exception
as
e
:
            
exc
val
tb
=
sys
.
exc_info
(
)
            
message
=
"
Error
possibly
due
to
runner
or
device
args
:
{
}
"
            
reraise
(
exc
message
.
format
(
e
.
message
)
tb
)
        
logcat_args
=
{
            
"
filterspec
"
:
"
Gecko
"
            
"
serial
"
:
self
.
runner
.
device
.
app_ctx
.
device_serial
        
}
        
if
self
.
gecko_log
=
=
"
-
"
:
            
logcat_args
[
"
stream
"
]
=
sys
.
stdout
        
else
:
            
logcat_args
[
"
logfile
"
]
=
self
.
gecko_log
        
self
.
runner
.
device
.
start_logcat
(
*
*
logcat_args
)
        
self
.
runner
.
device
.
device
.
forward
(
            
local
=
"
tcp
:
{
}
"
.
format
(
self
.
marionette_port
)
            
remote
=
"
tcp
:
{
}
"
.
format
(
self
.
marionette_port
)
)
    
def
_get_runner_args
(
self
)
:
        
process_args
=
{
            
"
processOutputLine
"
:
[
NullOutput
(
)
]
        
}
        
runner_args
=
{
            
"
app
"
:
self
.
package_name
            
"
avd_home
"
:
self
.
avd_home
            
"
adb_path
"
:
self
.
adb_path
            
"
binary
"
:
self
.
emulator_binary
            
"
profile
"
:
self
.
profile
            
"
cmdargs
"
:
[
"
-
marionette
"
]
+
self
.
app_args
            
"
symbols_path
"
:
self
.
symbols_path
            
"
process_args
"
:
process_args
            
"
logdir
"
:
self
.
workspace
or
os
.
getcwd
(
)
            
"
serial
"
:
self
.
serial
        
}
        
if
self
.
avd
:
            
runner_args
[
"
avd
"
]
=
self
.
avd
        
return
runner_args
    
def
close
(
self
clean
=
False
)
:
        
"
"
"
        
Close
the
managed
Gecko
process
.
        
If
clean
is
True
and
the
Fennec
instance
is
running
in
an
        
emulator
managed
by
mozrunner
this
will
stop
the
emulator
.
        
:
param
clean
:
If
True
also
perform
runner
cleanup
.
        
"
"
"
        
super
(
FennecInstance
self
)
.
close
(
clean
)
        
if
clean
and
self
.
runner
and
self
.
runner
.
device
.
connected
:
            
try
:
                
self
.
runner
.
device
.
device
.
remove_forwards
(
                    
"
tcp
:
{
}
"
.
format
(
self
.
marionette_port
)
)
                
self
.
unresponsive_count
=
0
            
except
Exception
:
                
self
.
unresponsive_count
+
=
1
                
traceback
.
print_exception
(
*
sys
.
exc_info
(
)
)
class
DesktopInstance
(
GeckoInstance
)
:
    
desktop_prefs
=
{
        
"
app
.
update
.
enabled
"
:
False
        
"
browser
.
dom
.
window
.
dump
.
enabled
"
:
True
        
"
browser
.
download
.
panel
.
shown
"
:
True
        
"
browser
.
EULA
.
override
"
:
True
        
"
browser
.
pagethumbnails
.
capturing_disabled
"
:
True
        
"
browser
.
safebrowsing
.
blockedURIs
.
enabled
"
:
False
        
"
browser
.
safebrowsing
.
downloads
.
enabled
"
:
False
        
"
browser
.
safebrowsing
.
passwords
.
enabled
"
:
False
        
"
browser
.
safebrowsing
.
malware
.
enabled
"
:
False
        
"
browser
.
safebrowsing
.
phishing
.
enabled
"
:
False
        
"
browser
.
search
.
update
"
:
False
        
"
browser
.
sessionstore
.
resume_from_crash
"
:
False
        
"
browser
.
shell
.
checkDefaultBrowser
"
:
False
        
"
browser
.
tabs
.
remote
.
autostart
"
:
False
        
"
browser
.
startup
.
homepage_override
.
mstone
"
:
"
ignore
"
        
"
browser
.
startup
.
page
"
:
0
        
"
toolkit
.
cosmeticAnimations
.
enabled
"
:
False
        
"
browser
.
tabs
.
warnOnClose
"
:
False
        
"
browser
.
tabs
.
warnOnCloseOtherTabs
"
:
False
        
"
browser
.
tabs
.
warnOnOpen
"
:
False
        
"
browser
.
uitour
.
enabled
"
:
False
        
"
browser
.
urlbar
.
suggest
.
searches
"
:
False
        
"
browser
.
urlbar
.
userMadeSearchSuggestionsChoice
"
:
True
        
"
startup
.
homepage_welcome_url
"
:
"
about
:
blank
"
        
"
startup
.
homepage_welcome_url
.
additional
"
:
"
"
    
}
    
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
DesktopInstance
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
required_prefs
.
update
(
DesktopInstance
.
desktop_prefs
)
class
NullOutput
(
object
)
:
    
def
__call__
(
self
line
)
:
        
pass
apps
=
{
    
'
fennec
'
:
FennecInstance
    
'
fxdesktop
'
:
DesktopInstance
}
app_ids
=
{
    
'
{
aa3c5121
-
dab2
-
40e2
-
81ca
-
7ea25febc110
}
'
:
'
fennec
'
    
'
{
ec8030f7
-
c20a
-
464f
-
9b0e
-
13a3a9e97384
}
'
:
'
fxdesktop
'
}
