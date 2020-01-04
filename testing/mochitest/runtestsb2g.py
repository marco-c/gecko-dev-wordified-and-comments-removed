import
json
import
os
import
posixpath
import
sys
import
tempfile
import
traceback
here
=
os
.
path
.
abspath
(
os
.
path
.
dirname
(
__file__
)
)
sys
.
path
.
insert
(
0
here
)
from
runtests
import
MochitestBase
from
mochitest_options
import
MochitestArgumentParser
from
marionette
import
Marionette
from
mozprofile
import
Profile
Preferences
from
mozrunner
.
utils
import
get_stack_fixer_function
import
mozinfo
import
mozleak
class
MochitestB2G
(
MochitestBase
)
:
    
"
"
"
    
Mochitest
class
for
b2g
emulators
and
devices
.
    
"
"
"
    
marionette
=
None
    
remote_log
=
None
    
def
__init__
(
self
marionette_args
                 
logger_options
                 
profile_data_dir
                 
local_binary_dir
                 
locations
=
os
.
path
.
join
(
here
'
server
-
locations
.
txt
'
)
                 
out_of_process
=
True
                 
remote_test_root
=
None
                 
remote_log_file
=
None
)
:
        
MochitestBase
.
__init__
(
self
logger_options
)
        
self
.
marionette_args
=
marionette_args
        
self
.
out_of_process
=
out_of_process
        
self
.
locations_file
=
locations
        
self
.
preferences
=
[
]
        
self
.
webapps
=
None
        
self
.
start_script
=
os
.
path
.
join
(
here
'
start_b2g
.
js
'
)
        
self
.
start_script_args
=
[
self
.
out_of_process
]
        
self
.
product
=
'
b2g
'
        
self
.
remote_chrome_test_dir
=
None
        
self
.
local_log
=
None
        
self
.
local_binary_dir
=
local_binary_dir
        
self
.
preferences
=
[
            
os
.
path
.
join
(
                
profile_data_dir
                
f
)
for
f
in
os
.
listdir
(
profile_data_dir
)
if
f
.
startswith
(
'
pref
'
)
]
        
self
.
webapps
=
[
            
os
.
path
.
join
(
                
profile_data_dir
                
f
)
for
f
in
os
.
listdir
(
profile_data_dir
)
if
f
.
startswith
(
'
webapp
'
)
]
        
if
mozinfo
.
info
[
'
debug
'
]
:
            
self
.
SERVER_STARTUP_TIMEOUT
=
180
        
else
:
            
self
.
SERVER_STARTUP_TIMEOUT
=
90
    
def
buildTestPath
(
self
options
testsToFilter
=
None
)
:
        
if
options
.
manifestFile
!
=
'
tests
.
json
'
:
            
MochitestBase
.
buildTestPath
(
self
options
testsToFilter
disabled
=
False
)
        
return
self
.
buildTestURL
(
options
)
    
def
build_profile
(
self
options
)
:
        
prefs
=
{
}
        
for
path
in
self
.
preferences
:
            
prefs
.
update
(
Preferences
.
read_prefs
(
path
)
)
        
for
v
in
options
.
extraPrefs
:
            
thispref
=
v
.
split
(
"
=
"
1
)
            
if
len
(
thispref
)
<
2
:
                
print
"
Error
:
syntax
error
in
-
-
setpref
=
"
+
v
                
sys
.
exit
(
1
)
            
prefs
[
thispref
[
0
]
]
=
thispref
[
1
]
        
interpolation
=
{
            
"
server
"
:
"
%
s
:
%
s
"
%
            
(
options
.
webServer
             
options
.
httpPort
)
            
"
OOP
"
:
"
true
"
if
self
.
out_of_process
else
"
false
"
}
        
prefs
=
json
.
loads
(
json
.
dumps
(
prefs
)
%
interpolation
)
        
for
pref
in
prefs
:
            
prefs
[
pref
]
=
Preferences
.
cast
(
prefs
[
pref
]
)
        
kwargs
=
{
            
'
addons
'
:
self
.
getExtensionsToInstall
(
options
)
            
'
apps
'
:
self
.
webapps
            
'
locations
'
:
self
.
locations_file
            
'
preferences
'
:
prefs
            
'
proxy
'
:
{
"
remote
"
:
options
.
webServer
}
        
}
        
self
.
profile
=
Profile
(
*
*
kwargs
)
        
options
.
profilePath
=
self
.
profile
.
profile
        
manifest
=
self
.
addChromeToProfile
(
options
)
        
self
.
copyExtraFilesToProfile
(
options
)
        
return
manifest
    
def
run_tests
(
self
options
)
:
        
"
"
"
Prepare
configure
run
tests
and
cleanup
"
"
"
        
self
.
setTestRoot
(
options
)
        
manifest
=
self
.
build_profile
(
options
)
        
self
.
logPreamble
(
self
.
getActiveTests
(
options
)
)
        
self
.
message_logger
.
buffering
=
options
.
quiet
        
if
options
.
debugger
or
not
options
.
autorun
:
            
timeout
=
None
        
else
:
            
if
not
options
.
timeout
:
                
if
mozinfo
.
info
[
'
debug
'
]
:
                    
options
.
timeout
=
420
                
else
:
                    
options
.
timeout
=
300
            
timeout
=
options
.
timeout
+
30
.
0
        
self
.
log
.
info
(
"
runtestsb2g
.
py
|
Running
tests
:
start
.
"
)
        
status
=
0
        
try
:
            
def
on_output
(
line
)
:
                
messages
=
self
.
message_logger
.
write
(
line
)
                
for
message
in
messages
:
                    
if
message
[
'
action
'
]
=
=
'
test_start
'
:
                        
self
.
runner
.
last_test
=
message
[
'
test
'
]
            
process_args
=
{
'
processOutputLine
'
:
on_output
                            
'
stream
'
:
None
}
            
self
.
marionette_args
[
'
process_args
'
]
=
process_args
            
self
.
marionette_args
[
'
profile
'
]
=
self
.
profile
            
self
.
marionette_args
[
'
socket_timeout
'
]
=
720
            
self
.
marionette
=
Marionette
(
*
*
self
.
marionette_args
)
            
self
.
runner
=
self
.
marionette
.
runner
            
self
.
app_ctx
=
self
.
runner
.
app_ctx
            
self
.
remote_log
=
posixpath
.
join
(
self
.
app_ctx
.
remote_test_root
                                             
'
log
'
'
mochitest
.
log
'
)
            
if
not
self
.
app_ctx
.
dm
.
dirExists
(
                
posixpath
.
dirname
(
                    
self
.
remote_log
)
)
:
                
self
.
app_ctx
.
dm
.
mkDirs
(
self
.
remote_log
)
            
if
options
.
chrome
:
                
self
.
writeChromeManifest
(
options
)
            
self
.
leak_report_file
=
posixpath
.
join
(
                
self
.
app_ctx
.
remote_test_root
                
'
log
'
                
'
runtests_leaks
.
log
'
)
            
self
.
browserEnv
=
self
.
buildBrowserEnv
(
options
env
=
{
}
)
            
if
mozinfo
.
info
[
                    
'
debug
'
]
and
'
MOZ_DISABLE_NONLOCAL_CONNECTIONS
'
in
self
.
browserEnv
:
                
del
self
.
browserEnv
[
'
MOZ_DISABLE_NONLOCAL_CONNECTIONS
'
]
            
self
.
runner
.
env
.
update
(
self
.
browserEnv
)
            
self
.
killNamedOrphans
(
'
ssltunnel
'
)
            
self
.
killNamedOrphans
(
'
xpcshell
'
)
            
self
.
startServers
(
options
None
)
            
manifestFile
=
options
.
manifestFile
            
options
.
manifestFile
=
None
            
self
.
buildURLOptions
(
options
{
'
MOZ_HIDE_RESULTS_TABLE
'
:
'
1
'
}
)
            
options
.
manifestFile
=
manifestFile
            
self
.
start_script_args
.
append
(
not
options
.
emulator
)
            
self
.
start_script_args
.
append
(
options
.
wifi
)
            
self
.
start_script_args
.
append
(
options
.
chrome
)
            
self
.
runner
.
start
(
outputTimeout
=
timeout
)
            
self
.
marionette
.
wait_for_port
(
)
            
self
.
marionette
.
start_session
(
)
            
self
.
marionette
.
set_context
(
self
.
marionette
.
CONTEXT_CHROME
)
            
self
.
marionette
.
execute_script
(
"
"
"
                
Components
.
utils
.
import
(
"
resource
:
/
/
gre
/
modules
/
Services
.
jsm
"
)
;
                
Services
.
io
.
manageOfflineStatus
=
false
;
                
Services
.
io
.
offline
=
false
;
                
"
"
"
)
            
self
.
marionette
.
execute_script
(
"
"
"
                
let
SECURITY_PREF
=
"
security
.
turn_off_all_security_so_that_viruses_can_take_over_this_computer
"
;
                
Services
.
prefs
.
setBoolPref
(
SECURITY_PREF
true
)
;
                
if
(
!
testUtils
.
hasOwnProperty
(
"
specialPowersObserver
"
)
)
{
                  
let
loader
=
Components
.
classes
[
"
mozilla
.
org
/
moz
/
jssubscript
-
loader
;
1
"
]
                    
.
getService
(
Components
.
interfaces
.
mozIJSSubScriptLoader
)
;
                  
loader
.
loadSubScript
(
"
chrome
:
/
/
specialpowers
/
content
/
SpecialPowersObserver
.
jsm
"
                    
testUtils
)
;
                  
testUtils
.
specialPowersObserver
=
new
testUtils
.
SpecialPowersObserver
(
)
;
                  
testUtils
.
specialPowersObserver
.
init
(
)
;
                
}
                
"
"
"
)
            
if
options
.
chrome
:
                
self
.
app_ctx
.
dm
.
removeDir
(
self
.
remote_chrome_test_dir
)
                
self
.
app_ctx
.
dm
.
mkDir
(
self
.
remote_chrome_test_dir
)
                
local
=
MochitestBase
.
getChromeTestDir
(
self
options
)
                
local
=
os
.
path
.
join
(
local
"
chrome
"
)
                
remote
=
self
.
remote_chrome_test_dir
                
self
.
log
.
info
(
                    
"
pushing
%
s
to
%
s
on
device
.
.
.
"
%
                    
(
local
remote
)
)
                
self
.
app_ctx
.
dm
.
pushDir
(
local
remote
)
            
self
.
execute_start_script
(
)
            
status
=
self
.
runner
.
wait
(
)
            
if
status
is
None
:
                
status
=
124
            
local_leak_file
=
tempfile
.
NamedTemporaryFile
(
)
            
self
.
app_ctx
.
dm
.
getFile
(
                
self
.
leak_report_file
                
local_leak_file
.
name
)
            
self
.
app_ctx
.
dm
.
removeFile
(
self
.
leak_report_file
)
            
mozleak
.
process_leak_log
(
                
local_leak_file
.
name
                
leak_thresholds
=
options
.
leakThresholds
                
ignore_missing_leaks
=
options
.
ignoreMissingLeaks
                
log
=
self
.
log
                
stack_fixer
=
get_stack_fixer_function
(
options
.
utilityPath
                                                     
options
.
symbolsPath
)
            
)
        
except
KeyboardInterrupt
:
            
self
.
log
.
info
(
"
runtests
.
py
|
Received
keyboard
interrupt
.
\
n
"
)
            
status
=
-
1
        
except
:
            
traceback
.
print_exc
(
)
            
self
.
log
.
error
(
                
"
Automation
Error
:
Received
unexpected
exception
while
running
application
\
n
"
)
            
if
hasattr
(
self
'
runner
'
)
:
                
self
.
runner
.
check_for_crashes
(
)
            
status
=
1
        
self
.
stopServers
(
)
        
self
.
log
.
info
(
"
runtestsb2g
.
py
|
Running
tests
:
end
.
"
)
        
if
manifest
is
not
None
:
            
self
.
cleanup
(
manifest
options
)
        
return
status
    
def
getGMPPluginPath
(
self
options
)
:
        
if
options
.
gmp_path
:
            
return
options
.
gmp_path
        
return
'
/
system
/
b2g
/
gmp
-
clearkey
/
0
.
1
'
    
def
getChromeTestDir
(
self
options
)
:
        
if
hasattr
(
self
'
app_ctx
'
)
:
            
self
.
remote_chrome_test_dir
=
posixpath
.
join
(
                
self
.
app_ctx
.
remote_test_root
                
'
chrome
'
)
            
return
self
.
remote_chrome_test_dir
        
return
'
dummy
-
chrome
-
test
-
dir
'
    
def
cleanup
(
self
manifest
options
)
:
        
if
self
.
local_log
:
            
self
.
app_ctx
.
dm
.
getFile
(
self
.
remote_log
self
.
local_log
)
            
self
.
app_ctx
.
dm
.
removeFile
(
self
.
remote_log
)
        
if
options
.
pidFile
!
=
"
"
:
            
try
:
                
os
.
remove
(
options
.
pidFile
)
                
os
.
remove
(
options
.
pidFile
+
"
.
xpcshell
.
pid
"
)
            
except
:
                
print
"
Warning
:
cleaning
up
pidfile
'
%
s
'
was
unsuccessful
from
the
test
harness
"
%
options
.
pidFile
        
if
getattr
(
self
'
runner
'
False
)
:
            
if
self
.
local_log
:
                
self
.
app_ctx
.
dm
.
getFile
(
self
.
remote_log
self
.
local_log
)
                
self
.
app_ctx
.
dm
.
removeFile
(
self
.
remote_log
)
            
self
.
runner
.
cleanup
(
)
            
self
.
runner
=
None
    
def
startServers
(
self
options
debuggerInfo
)
:
        
"
"
"
Create
the
servers
on
the
host
and
start
them
up
"
"
"
        
savedXre
=
options
.
xrePath
        
savedUtility
=
options
.
utilityPath
        
savedProfie
=
options
.
profilePath
        
options
.
xrePath
=
self
.
local_binary_dir
        
options
.
utilityPath
=
self
.
local_binary_dir
        
options
.
profilePath
=
tempfile
.
mkdtemp
(
)
        
MochitestBase
.
startServers
(
self
options
debuggerInfo
)
        
options
.
xrePath
=
savedXre
        
options
.
utilityPath
=
savedUtility
        
options
.
profilePath
=
savedProfie
    
def
buildURLOptions
(
self
options
env
)
:
        
self
.
local_log
=
options
.
logFile
        
options
.
logFile
=
self
.
remote_log
        
options
.
profilePath
=
self
.
profile
.
profile
        
MochitestBase
.
buildURLOptions
(
self
options
env
)
        
test_url
=
self
.
buildTestPath
(
options
)
        
if
"
manifestFile
=
tests
.
json
"
not
in
self
.
urlOpts
:
            
self
.
urlOpts
.
append
(
"
manifestFile
=
%
s
"
%
options
.
manifestFile
)
        
if
len
(
self
.
urlOpts
)
>
0
:
            
test_url
+
=
"
?
"
+
"
&
"
.
join
(
self
.
urlOpts
)
        
self
.
start_script_args
.
append
(
test_url
)
        
options
.
profilePath
=
self
.
app_ctx
.
remote_profile
        
options
.
logFile
=
self
.
local_log
def
run_test_harness
(
options
)
:
    
marionette_args
=
{
        
'
adb_path
'
:
options
.
adbPath
        
'
emulator
'
:
options
.
emulator
        
'
no_window
'
:
options
.
noWindow
        
'
logdir
'
:
options
.
logdir
        
'
busybox
'
:
options
.
busybox
        
'
symbols_path
'
:
options
.
symbolsPath
        
'
sdcard
'
:
options
.
sdcard
        
'
homedir
'
:
options
.
b2gPath
    
}
    
if
options
.
marionette
:
        
host
port
=
options
.
marionette
.
split
(
'
:
'
)
        
marionette_args
[
'
host
'
]
=
host
        
marionette_args
[
'
port
'
]
=
int
(
port
)
    
if
(
options
is
None
)
:
        
print
"
ERROR
:
Invalid
options
specified
use
-
-
help
for
a
list
of
valid
options
"
        
sys
.
exit
(
1
)
    
mochitest
=
MochitestB2G
(
        
marionette_args
        
options
        
options
.
profile_data_dir
        
options
.
xrePath
        
remote_log_file
=
options
.
remoteLogFile
)
    
if
(
options
is
None
)
:
        
sys
.
exit
(
1
)
    
retVal
=
1
    
try
:
        
mochitest
.
cleanup
(
None
options
)
        
retVal
=
mochitest
.
run_tests
(
options
)
    
except
:
        
print
"
Automation
Error
:
Exception
caught
while
running
tests
"
        
traceback
.
print_exc
(
)
        
mochitest
.
stopServers
(
)
        
try
:
            
mochitest
.
cleanup
(
None
options
)
        
except
:
            
pass
        
retVal
=
1
    
mochitest
.
message_logger
.
finish
(
)
    
return
retVal
def
main
(
)
:
    
parser
=
MochitestArgumentParser
(
app
=
'
b2g
'
)
    
options
=
parser
.
parse_args
(
)
    
return
run_test_harness
(
options
)
if
__name__
=
=
"
__main__
"
:
    
sys
.
exit
(
main
(
)
)
