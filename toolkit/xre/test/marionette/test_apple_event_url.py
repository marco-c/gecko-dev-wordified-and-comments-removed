"
"
"
Test
that
URLs
delivered
via
macOS
Apple
Events
survive
the
profile
manager
relaunch
.
When
Firefox
is
launched
via
open
https
:
/
/
.
.
.
on
macOS
with
StartWithLastProfile
=
false
the
profile
manager
dialog
appears
and
Firefox
relaunches
after
a
profile
is
selected
.
On
macOS
15
+
URLs
from
Apple
Events
can
be
lost
during
this
relaunch
if
they
arrive
after
InitializeMacApp
(
)
exits
.
See
bug
2036237
.
This
test
automates
the
full
flow
:
sets
StartWithLastProfile
=
false
quits
Firefox
relaunches
via
Apple
Event
with
a
URL
dismisses
the
profile
dialog
with
Enter
and
reconnects
via
Marionette
to
verify
the
URL
was
opened
.
"
"
"
import
os
import
subprocess
import
time
from
marionette_harness
import
MarionetteTestCase
class
TestAppleEventURL
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
)
.
setUp
(
)
        
self
.
original_start_with_last
=
None
        
self
.
original_port
=
self
.
marionette
.
port
    
def
tearDown
(
self
)
:
        
self
.
marionette
.
port
=
self
.
original_port
        
try
:
            
if
(
                
self
.
marionette
.
session
is
not
None
                
and
self
.
original_start_with_last
is
not
None
            
)
:
                
with
self
.
marionette
.
using_context
(
self
.
marionette
.
CONTEXT_CHROME
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
                        
const
svc
=
Cc
[
"
mozilla
.
org
/
toolkit
/
profile
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
nsIToolkitProfileService
)
;
                        
svc
.
startWithLastProfile
=
arguments
[
0
]
;
                        
svc
.
flush
(
)
;
                        
"
"
"
                        
script_args
=
[
self
.
original_start_with_last
]
                        
sandbox
=
"
system
"
                    
)
        
except
Exception
:
            
pass
        
try
:
            
if
self
.
marionette
.
session
is
not
None
:
                
with
self
.
marionette
.
using_context
(
self
.
marionette
.
CONTEXT_CHROME
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
                            
while
(
win
.
gBrowser
.
tabs
.
length
>
1
)
{
                                
win
.
gBrowser
.
removeTab
(
win
.
gBrowser
.
tabs
.
at
(
-
1
)
)
;
                            
}
                        
}
                        
"
"
"
                        
sandbox
=
"
system
"
                    
)
        
except
Exception
:
            
pass
        
try
:
            
if
self
.
marionette
.
session
is
not
None
:
                
self
.
marionette
.
quit
(
in_app
=
True
)
        
except
Exception
:
            
pass
        
if
self
.
marionette
.
session
is
None
:
            
process_name
=
self
.
_get_process_name
(
)
            
subprocess
.
run
(
                
[
                    
"
osascript
"
                    
"
-
e
"
                    
f
'
tell
application
"
{
process_name
}
"
to
quit
'
                
]
                
capture_output
=
True
                
timeout
=
10
                
check
=
False
            
)
        
super
(
)
.
tearDown
(
)
    
def
_get_app_bundle_path
(
self
)
:
        
binary
=
self
.
marionette
.
instance
.
binary
        
parts
=
binary
.
split
(
"
/
"
)
        
for
i
part
in
enumerate
(
parts
)
:
            
if
part
.
endswith
(
"
.
app
"
)
:
                
return
"
/
"
.
join
(
parts
[
:
i
+
1
]
)
        
return
None
    
def
_get_process_name
(
self
)
:
        
"
"
"
Derive
the
System
Events
process
name
from
the
app
bundle
.
"
"
"
        
app_bundle
=
self
.
_get_app_bundle_path
(
)
        
if
app_bundle
:
            
return
os
.
path
.
basename
(
app_bundle
)
.
removesuffix
(
"
.
app
"
)
        
return
"
firefox
"
    
def
_wait_for_tab_with_url
(
self
url_substring
timeout
=
10
)
:
        
deadline
=
time
.
monotonic
(
)
+
timeout
        
while
time
.
monotonic
(
)
<
deadline
:
            
with
self
.
marionette
.
using_context
(
self
.
marionette
.
CONTEXT_CHROME
)
:
                
result
=
self
.
marionette
.
execute_script
(
                    
"
"
"
                    
const
substring
=
arguments
[
0
]
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
                        
for
(
const
tab
of
win
.
gBrowser
.
tabs
)
{
                            
const
url
=
tab
.
linkedBrowser
.
currentURI
.
spec
;
                            
if
(
url
.
includes
(
substring
)
)
{
                                
return
url
;
                            
}
                        
}
                    
}
                    
return
null
;
                    
"
"
"
                    
script_args
=
[
url_substring
]
                    
sandbox
=
"
system
"
                
)
                
if
result
:
                    
return
result
            
time
.
sleep
(
0
.
5
)
        
return
None
    
def
test_apple_event_url_survives_profile_manager
(
self
)
:
        
"
"
"
URL
from
Apple
Event
must
survive
the
profile
manager
relaunch
.
"
"
"
        
app_bundle
=
self
.
_get_app_bundle_path
(
)
        
self
.
assertIsNotNone
(
app_bundle
"
Could
not
determine
.
app
bundle
path
"
)
        
test_url
=
"
about
:
license
"
        
with
self
.
marionette
.
using_context
(
self
.
marionette
.
CONTEXT_CHROME
)
:
            
self
.
original_start_with_last
=
self
.
marionette
.
execute_script
(
                
"
"
"
                
const
svc
=
Cc
[
"
mozilla
.
org
/
toolkit
/
profile
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
nsIToolkitProfileService
)
;
                
const
orig
=
svc
.
startWithLastProfile
;
                
svc
.
startWithLastProfile
=
false
;
                
svc
.
flush
(
)
;
                
return
orig
;
                
"
"
"
                
sandbox
=
"
system
"
            
)
        
self
.
marionette
.
quit
(
)
        
subprocess
.
run
(
            
[
                
"
open
"
                
"
-
a
"
                
app_bundle
                
test_url
                
"
-
-
env
"
                
"
MOZ_MARIONETTE
=
1
"
                
"
-
-
env
"
                
"
MOZ_REMOTE_ALLOW_SYSTEM_ACCESS
=
1
"
            
]
            
check
=
True
            
timeout
=
10
        
)
        
process_name
=
self
.
_get_process_name
(
)
        
dialog_dismissed
=
False
        
for
attempt
in
range
(
10
)
:
            
time
.
sleep
(
1
)
            
result
=
subprocess
.
run
(
                
[
                    
"
osascript
"
                    
"
-
e
"
                    
f
'
tell
application
"
System
Events
"
\
n
'
                    
f
'
tell
process
"
{
process_name
}
"
\
n
'
                    
f
"
set
frontmost
to
true
\
n
"
                    
f
"
delay
0
.
5
\
n
"
                    
f
"
keystroke
return
\
n
"
                    
f
"
end
tell
\
n
"
                    
f
"
end
tell
"
                
]
                
capture_output
=
True
                
timeout
=
10
                
check
=
False
            
)
            
if
result
.
returncode
=
=
0
:
                
dialog_dismissed
=
True
                
break
        
self
.
assertTrue
(
            
dialog_dismissed
            
"
Could
not
dismiss
profile
manager
dialog
via
osascript
.
"
            
"
Ensure
System
Events
accessibility
is
enabled
.
"
        
)
        
from
marionette_driver
import
transport
        
self
.
marionette
.
port
=
2828
        
self
.
marionette
.
raise_for_port
(
timeout
=
30
check_process_status
=
False
)
        
self
.
marionette
.
client
=
transport
.
TcpTransport
(
            
self
.
marionette
.
host
            
2828
            
self
.
marionette
.
socket_timeout
        
)
        
self
.
marionette
.
protocol
_
=
self
.
marionette
.
client
.
connect
(
)
        
resp
=
self
.
marionette
.
_send_message
(
            
"
WebDriver
:
NewSession
"
{
"
strictFileInteractability
"
:
True
}
        
)
        
self
.
marionette
.
session_id
=
resp
[
"
sessionId
"
]
        
self
.
marionette
.
session
=
resp
[
"
capabilities
"
]
        
self
.
marionette
.
cleanup_ran
=
False
        
self
.
marionette
.
process_id
=
self
.
marionette
.
session
.
get
(
"
moz
:
processID
"
)
        
self
.
marionette
.
profile
=
self
.
marionette
.
session
.
get
(
"
moz
:
profile
"
)
        
found_url
=
self
.
_wait_for_tab_with_url
(
"
about
:
license
"
)
        
self
.
assertIsNotNone
(
            
found_url
            
"
Expected
about
:
license
to
be
opened
via
Apple
Event
"
            
"
after
profile
manager
relaunch
(
bug
2036237
)
"
        
)
