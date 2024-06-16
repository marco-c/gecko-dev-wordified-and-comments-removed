import
time
from
unittest
.
util
import
safe_repr
from
marionette_driver
.
by
import
By
from
marionette_driver
.
keys
import
Keys
from
marionette_harness
import
MarionetteTestCase
known_errors
=
[
    
{
        
"
message
"
:
"
app
.
normandy
.
api_url
is
not
set
"
    
}
    
{
        
"
message
"
:
'
Error
:
Unexpected
content
-
type
"
text
/
plain
'
        
"
filename
"
:
"
RemoteSettingsClient
"
    
}
    
{
        
"
message
"
:
"
key_browserToolbox
"
    
}
    
{
        
"
message
"
:
"
key_quickRestart
"
    
}
    
{
        
"
message
"
:
"
key_toggleReaderMode
"
    
}
    
{
        
"
message
"
:
"
(
NS_ERROR_NOT_IMPLEMENTED
)
[
nsIAppStartup
.
secondsSinceLastOSRestart
]
"
        
"
filename
"
:
"
BrowserGlue
"
    
}
]
headless_errors
=
[
{
"
message
"
:
"
TelemetryEnvironment
:
:
_isDefaultBrowser
"
}
]
class
TestNoErrorsNewProfile
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
MarionetteTestCase
self
)
.
setUp
(
)
        
self
.
maxDiff
=
None
        
self
.
marionette
.
set_context
(
"
chrome
"
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
    
def
ensure_proper_startup
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
resolve
=
arguments
[
0
]
;
            
let
{
BrowserInitState
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
/
modules
/
BrowserGlue
.
sys
.
mjs
"
)
;
            
let
promises
=
[
              
BrowserInitState
.
startupIdleTaskPromise
              
gBrowserInit
.
idleTasksFinished
.
promise
            
]
;
            
Promise
.
all
(
promises
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
        
if
self
.
marionette
.
session_capabilities
[
"
platformName
"
]
=
=
"
mac
"
:
            
self
.
mod_key
=
Keys
.
META
        
else
:
            
self
.
mod_key
=
Keys
.
CONTROL
        
url_bar
=
self
.
marionette
.
execute_script
(
"
return
gURLBar
.
inputField
"
)
        
url_bar
.
send_keys
(
self
.
mod_key
"
l
"
)
        
new_tab_button
=
self
.
marionette
.
find_element
(
By
.
ID
"
new
-
tab
-
button
"
)
        
new_tab_button
.
click
(
)
        
time
.
sleep
(
5
)
    
def
get_all_errors
(
self
)
:
        
return
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
resolve
=
arguments
[
0
]
;
            
/
/
Get
all
the
messages
from
the
console
service
            
/
/
and
then
get
all
of
the
ones
from
the
console
API
storage
.
            
let
msgs
=
Services
.
console
.
getMessageArray
(
)
;
            
const
ConsoleAPIStorage
=
Cc
[
              
"
mozilla
.
org
/
consoleAPI
-
storage
;
1
"
            
]
.
getService
(
Ci
.
nsIConsoleAPIStorage
)
;
            
const
getCircularReplacer
=
(
)
=
>
{
              
const
seen
=
new
WeakSet
(
)
;
              
return
(
key
value
)
=
>
{
                
if
(
typeof
value
=
=
=
"
object
"
&
&
value
!
=
=
null
)
{
                  
if
(
seen
.
has
(
value
)
)
{
                    
return
"
<
circular
ref
>
"
;
                  
}
                  
seen
.
add
(
value
)
;
                
}
                
return
value
;
              
}
;
            
}
;
            
/
/
Take
cyclical
values
out
add
a
simplified
'
message
'
prop
            
/
/
that
matches
how
things
work
for
the
console
service
objects
.
            
const
consoleApiMessages
=
ConsoleAPIStorage
.
getEvents
(
)
.
map
(
ev
=
>
{
              
let
rv
;
              
try
{
                
rv
=
structuredClone
(
ev
)
;
              
}
catch
(
ex
)
{
                
rv
=
JSON
.
parse
(
JSON
.
stringify
(
ev
getCircularReplacer
(
)
)
)
;
              
}
              
delete
rv
.
wrappedJSObject
;
              
rv
.
message
=
ev
.
arguments
.
join
(
"
"
)
;
              
return
rv
;
            
}
)
;
            
resolve
(
msgs
.
concat
(
consoleApiMessages
)
)
;
            
"
"
"
        
)
    
def
should_ignore_error
(
self
error
)
:
        
if
not
"
message
"
in
error
:
            
print
(
"
Unparsable
error
:
"
)
            
print
(
safe_repr
(
error
)
)
            
return
False
        
error_filename
=
error
.
get
(
"
filename
"
"
"
)
        
error_msg
=
error
[
"
message
"
]
        
headless
=
self
.
marionette
.
session_capabilities
[
"
moz
:
headless
"
]
        
all_known_errors
=
known_errors
+
(
headless_errors
if
headless
else
[
]
)
        
for
known_error
in
all_known_errors
:
            
known_filename
=
known_error
.
get
(
"
filename
"
"
"
)
            
known_msg
=
known_error
[
"
message
"
]
            
if
known_msg
in
error_msg
and
known_filename
in
error_filename
:
                
print
(
                    
"
Known
error
seen
:
%
s
(
%
s
)
"
                    
%
(
error
[
"
message
"
]
error
.
get
(
"
filename
"
"
no
filename
"
)
)
                
)
                
return
True
        
return
False
    
def
short_error_display
(
self
errors
)
:
        
rv
=
[
]
        
for
error
in
errors
:
            
rv
+
=
[
                
{
                    
"
message
"
:
error
.
get
(
"
message
"
"
No
message
!
?
"
)
                    
"
filename
"
:
error
.
get
(
"
filename
"
"
No
filename
!
?
"
)
                
}
            
]
        
return
rv
    
def
test_no_errors
(
self
)
:
        
self
.
ensure_proper_startup
(
)
        
errors
=
self
.
get_all_errors
(
)
        
errors
[
:
]
=
[
error
for
error
in
errors
if
not
self
.
should_ignore_error
(
error
)
]
        
if
len
(
errors
)
>
0
:
            
print
(
"
Unexpected
errors
encountered
:
"
)
            
for
error
in
errors
:
                
print
(
safe_repr
(
error
)
)
        
self
.
assertEqual
(
self
.
short_error_display
(
errors
)
[
]
)
