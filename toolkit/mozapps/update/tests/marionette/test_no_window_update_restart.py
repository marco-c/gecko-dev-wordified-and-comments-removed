from
marionette_driver
import
Wait
errors
from
marionette_harness
import
MarionetteTestCase
class
TestNoWindowUpdateRestart
(
MarionetteTestCase
)
:
    
def
setUp
(
self
)
:
        
super
(
TestNoWindowUpdateRestart
self
)
.
setUp
(
)
        
self
.
marionette
.
delete_session
(
)
        
self
.
marionette
.
start_session
(
{
"
moz
:
windowless
"
:
True
}
)
        
window
=
self
.
marionette
.
window_handles
[
0
]
        
self
.
marionette
.
switch_to_window
(
window
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
setUpBrowser
(
)
        
self
.
resetUpdate
(
)
    
def
setUpBrowser
(
self
)
:
        
self
.
origAppUpdateAuto
=
self
.
marionette
.
execute_async_script
(
            
"
"
"
            
let
[
resolve
]
=
arguments
;
            
(
async
(
)
=
>
{
                
Services
.
prefs
.
setIntPref
(
"
app
.
update
.
download
.
attempts
"
0
)
;
                
Services
.
prefs
.
setIntPref
(
"
app
.
update
.
download
.
maxAttempts
"
0
)
;
                
Services
.
prefs
.
setBoolPref
(
"
app
.
update
.
staging
.
enabled
"
false
)
;
                
Services
.
prefs
.
setBoolPref
(
"
app
.
update
.
noWindowAutoRestart
.
enabled
"
true
)
;
                
Services
.
prefs
.
setIntPref
(
"
app
.
update
.
noWindowAutoRestart
.
delayMs
"
1000
)
;
                
Services
.
prefs
.
clearUserPref
(
"
testing
.
no_window_update_restart
.
silent_restart_env
"
)
;
                
let
{
UpdateUtils
}
=
ChromeUtils
.
importESModule
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
UpdateUtils
.
sys
.
mjs
"
                
)
;
                
let
origAppUpdateAuto
=
await
UpdateUtils
.
getAppUpdateAutoEnabled
(
)
;
                
await
UpdateUtils
.
setAppUpdateAutoEnabled
(
true
)
;
                
/
/
Prevent
the
update
sync
manager
from
thinking
there
are
two
instances
running
                
let
exePath
=
Services
.
dirsvc
.
get
(
"
XREExeF
"
Ci
.
nsIFile
)
;
                
let
dirProvider
=
{
                    
getFile
:
function
AGP_DP_getFile
(
aProp
aPersistent
)
{
                        
aPersistent
.
value
=
false
;
                        
switch
(
aProp
)
{
                            
case
"
XREExeF
"
:
                                
exePath
.
append
(
"
browser
-
test
"
)
;
                                
return
exePath
;
                        
}
                        
return
null
;
                    
}
                    
QueryInterface
:
ChromeUtils
.
generateQI
(
[
"
nsIDirectoryServiceProvider
"
]
)
                
}
;
                
let
ds
=
Services
.
dirsvc
.
QueryInterface
(
Ci
.
nsIDirectoryService
)
;
                
ds
.
QueryInterface
(
Ci
.
nsIProperties
)
.
undefine
(
"
XREExeF
"
)
;
                
ds
.
registerProvider
(
dirProvider
)
;
                
let
gSyncManager
=
Cc
[
"
mozilla
.
org
/
updates
/
update
-
sync
-
manager
;
1
"
]
.
getService
(
                  
Ci
.
nsIUpdateSyncManager
                
)
;
                
gSyncManager
.
resetLock
(
)
;
                
ds
.
unregisterProvider
(
dirProvider
)
;
                
return
origAppUpdateAuto
;
            
}
)
(
)
.
then
(
resolve
)
;
        
"
"
"
        
)
    
def
tearDown
(
self
)
:
        
self
.
tearDownBrowser
(
)
        
self
.
resetUpdate
(
)
        
self
.
marionette
.
restart
(
in_app
=
False
clean
=
True
)
        
super
(
TestNoWindowUpdateRestart
self
)
.
tearDown
(
)
    
def
tearDownBrowser
(
self
)
:
        
self
.
marionette
.
execute_async_script
(
            
"
"
"
            
const
[
origAppUpdateAuto
resolve
]
=
arguments
;
            
(
async
(
)
=
>
{
                
const
{
UpdateUtils
}
=
ChromeUtils
.
importESModule
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
UpdateUtils
.
sys
.
mjs
"
                
)
;
                
await
UpdateUtils
.
setAppUpdateAutoEnabled
(
origAppUpdateAuto
)
;
            
}
)
(
)
.
then
(
resolve
)
;
        
"
"
"
            
script_args
=
(
self
.
origAppUpdateAuto
)
        
)
    
def
test_update_on_last_window_close
(
self
)
:
        
self
.
marionette
.
restart
(
            
callback
=
self
.
prepare_update_and_close_all_windows
in_app
=
True
        
)
        
with
self
.
assertRaises
(
errors
.
TimeoutException
)
:
            
wait
=
Wait
(
                
self
.
marionette
                
ignored_exceptions
=
errors
.
NoSuchWindowException
                
timeout
=
5
            
)
            
wait
.
until
(
lambda
_
:
self
.
marionette
.
window_handles
)
        
self
.
marionette
.
restart
(
in_app
=
True
)
        
self
.
marionette
.
delete_session
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
        
quit_flags_correct
=
self
.
marionette
.
get_pref
(
            
"
testing
.
no_window_update_restart
.
silent_restart_env
"
        
)
        
self
.
assertTrue
(
quit_flags_correct
)
        
update_status
=
self
.
marionette
.
execute_async_script
(
            
"
"
"
            
let
[
updateURLString
resolve
]
=
arguments
;
            
(
async
(
)
=
>
{
                
/
/
Because
post
update
processing
happens
during
early
startup
and
                
/
/
app
.
update
.
disabledForTesting
is
also
set
in
early
startup
it
isn
'
t
                
/
/
especially
well
defined
whether
or
not
post
update
processing
will
have
run
at
                
/
/
this
point
.
Resolve
this
by
forcing
post
update
processing
to
run
.
This
is
as
                
/
/
simple
as
turning
off
app
.
update
.
disabledForTesting
and
calling
into
                
/
/
UpdateManager
since
the
relevant
methods
ensure
that
initialization
has
run
                
/
/
as
long
as
update
isn
'
t
disabled
.
                
/
/
Set
the
update
URL
to
a
local
one
first
to
ensure
we
don
'
t
hit
the
update
server
                
/
/
when
we
turn
off
app
.
update
.
disabledForTesting
.
                
const
mockAppInfo
=
Object
.
create
(
Services
.
appinfo
{
                    
updateURL
:
{
                        
configurable
:
true
                        
enumerable
:
true
                        
writable
:
false
                        
value
:
updateURLString
                    
}
                
}
)
;
                
Services
.
appinfo
=
mockAppInfo
;
                
Services
.
prefs
.
setBoolPref
(
"
app
.
update
.
disabledForTesting
"
false
)
;
                
const
UM
=
                    
Cc
[
"
mozilla
.
org
/
updates
/
update
-
manager
;
1
"
]
.
getService
(
Ci
.
nsIUpdateManager
)
;
                
const
history
=
await
UM
.
getHistory
(
)
;
                
if
(
!
history
.
length
)
{
                    
return
null
;
                
}
                
return
history
[
0
]
.
state
;
            
}
)
(
)
.
then
(
resolve
)
;
        
"
"
"
            
script_args
=
(
self
.
marionette
.
absolute_url
(
"
update
.
xml
"
)
)
        
)
        
self
.
assertIn
(
update_status
[
"
succeeded
"
"
failed
"
]
)
    
def
resetUpdate
(
self
)
:
        
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
UM
=
Cc
[
"
mozilla
.
org
/
updates
/
update
-
manager
;
1
"
]
.
getService
(
Ci
.
nsIUpdateManager
)
;
            
UM
.
internal
.
reload
(
true
)
;
            
let
{
UpdateListener
}
=
ChromeUtils
.
importESModule
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
UpdateListener
.
sys
.
mjs
"
            
)
;
            
UpdateListener
.
reset
(
)
;
            
let
{
AppMenuNotifications
}
=
ChromeUtils
.
importESModule
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
AppMenuNotifications
.
sys
.
mjs
"
            
)
;
            
AppMenuNotifications
.
removeNotification
(
/
.
*
/
)
;
            
/
/
Remove
old
update
files
so
that
they
don
'
t
interfere
with
tests
.
            
let
rootUpdateDir
=
Services
.
dirsvc
.
get
(
"
UpdRootD
"
Ci
.
nsIFile
)
;
            
let
updateDir
=
rootUpdateDir
.
clone
(
)
;
            
updateDir
.
append
(
"
updates
"
)
;
            
let
patchDir
=
updateDir
.
clone
(
)
;
            
patchDir
.
append
(
"
0
"
)
;
            
let
filesToRemove
=
[
]
;
            
let
addFileToRemove
=
(
dir
filename
)
=
>
{
                
let
file
=
dir
.
clone
(
)
;
                
file
.
append
(
filename
)
;
                
filesToRemove
.
push
(
file
)
;
            
}
;
            
addFileToRemove
(
rootUpdateDir
"
active
-
update
.
xml
"
)
;
            
addFileToRemove
(
rootUpdateDir
"
updates
.
xml
"
)
;
            
addFileToRemove
(
patchDir
"
update
.
status
"
)
;
            
addFileToRemove
(
patchDir
"
update
.
version
"
)
;
            
addFileToRemove
(
patchDir
"
update
.
mar
"
)
;
            
addFileToRemove
(
patchDir
"
updater
.
ini
"
)
;
            
addFileToRemove
(
updateDir
"
backup
-
update
.
log
"
)
;
            
addFileToRemove
(
updateDir
"
last
-
update
.
log
"
)
;
            
addFileToRemove
(
patchDir
"
update
.
log
"
)
;
            
for
(
const
file
of
filesToRemove
)
{
                
try
{
                    
if
(
file
.
exists
(
)
)
{
                        
file
.
remove
(
false
)
;
                    
}
                
}
catch
(
e
)
{
                    
console
.
warn
(
"
Unable
to
remove
file
.
Path
:
'
"
+
file
.
path
+
"
'
Exception
:
"
+
e
)
;
                
}
            
}
        
"
"
"
        
)
    
def
prepare_update_and_close_all_windows
(
self
)
:
        
self
.
marionette
.
execute_async_script
(
            
"
"
"
            
let
[
updateURLString
resolve
]
=
arguments
;
            
(
async
(
)
=
>
{
                
let
updateDownloadedPromise
=
new
Promise
(
innerResolve
=
>
{
                    
Services
.
obs
.
addObserver
(
function
callback
(
)
{
                        
Services
.
obs
.
removeObserver
(
callback
"
update
-
downloaded
"
)
;
                        
innerResolve
(
)
;
                    
}
"
update
-
downloaded
"
)
;
                
}
)
;
                
/
/
Set
the
update
URL
to
the
one
that
was
passed
in
.
                
let
mockAppInfo
=
Object
.
create
(
Services
.
appinfo
{
                    
updateURL
:
{
                        
configurable
:
true
                        
enumerable
:
true
                        
writable
:
false
                        
value
:
updateURLString
                    
}
                
}
)
;
                
Services
.
appinfo
=
mockAppInfo
;
                
/
/
We
aren
'
t
going
to
flip
this
until
after
the
URL
is
set
because
the
test
fails
                
/
/
if
we
hit
the
real
update
server
.
                
Services
.
prefs
.
setBoolPref
(
"
app
.
update
.
disabledForTesting
"
false
)
;
                
let
aus
=
Cc
[
"
mozilla
.
org
/
updates
/
update
-
service
;
1
"
]
                    
.
getService
(
Ci
.
nsIApplicationUpdateService
)
;
                
await
aus
.
checkForBackgroundUpdates
(
)
;
                
await
updateDownloadedPromise
;
                
Services
.
obs
.
addObserver
(
(
aSubject
aTopic
aData
)
=
>
{
                    
let
silent_restart
=
Services
.
env
.
get
(
"
MOZ_APP_SILENT_START
"
)
=
=
1
&
&
Services
.
env
.
get
(
"
MOZ_APP_RESTART
"
)
=
=
1
;
                    
Services
.
prefs
.
setBoolPref
(
"
testing
.
no_window_update_restart
.
silent_restart_env
"
silent_restart
)
;
                
}
"
quit
-
application
-
granted
"
)
;
                
for
(
const
win
of
Services
.
wm
.
getEnumerator
(
"
navigator
:
browser
"
)
)
{
                    
win
.
close
(
)
;
                
}
            
}
)
(
)
.
then
(
resolve
)
;
        
"
"
"
            
script_args
=
(
self
.
marionette
.
absolute_url
(
"
update
.
xml
"
)
)
        
)
