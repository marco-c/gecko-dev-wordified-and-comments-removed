from
__future__
import
absolute_import
import
copy
import
requests
from
marionette_harness
import
MarionetteTestCase
class
TestCommandLineArguments
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
TestCommandLineArguments
self
)
.
setUp
(
)
        
self
.
orig_arguments
=
copy
.
copy
(
self
.
marionette
.
instance
.
app_args
)
    
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
instance
.
app_args
=
self
.
orig_arguments
        
self
.
marionette
.
quit
(
clean
=
True
)
        
super
(
TestCommandLineArguments
self
)
.
tearDown
(
)
    
def
is_bidi_enabled
(
self
)
:
        
with
self
.
marionette
.
using_context
(
"
chrome
"
)
:
            
bidi_enabled
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
{
RemoteAgent
}
=
ChromeUtils
.
import
(
                
"
chrome
:
/
/
remote
/
content
/
components
/
RemoteAgent
.
jsm
"
              
)
;
              
return
!
!
RemoteAgent
.
webDriverBiDi
;
            
"
"
"
            
)
    
def
test_debugger_address_cdp_status
(
self
)
:
        
debugger_address
=
self
.
marionette
.
session_capabilities
.
get
(
            
"
moz
:
debuggerAddress
"
        
)
        
self
.
assertIsNone
(
debugger_address
)
        
self
.
marionette
.
enforce_gecko_prefs
(
{
"
remote
.
active
-
protocols
"
:
1
}
)
        
try
:
            
self
.
marionette
.
quit
(
)
            
self
.
marionette
.
instance
.
app_args
.
append
(
"
-
remote
-
debugging
-
port
"
)
            
self
.
marionette
.
start_session
(
)
            
debugger_address
=
self
.
marionette
.
session_capabilities
.
get
(
                
"
moz
:
debuggerAddress
"
            
)
            
self
.
assertIsNone
(
debugger_address
)
        
finally
:
            
self
.
marionette
.
clear_pref
(
"
remote
.
active
-
protocols
"
)
            
self
.
marionette
.
restart
(
)
        
self
.
marionette
.
quit
(
)
        
self
.
marionette
.
instance
.
switch_profile
(
)
        
self
.
marionette
.
start_session
(
)
        
debugger_address
=
self
.
marionette
.
session_capabilities
.
get
(
            
"
moz
:
debuggerAddress
"
        
)
        
self
.
assertEqual
(
debugger_address
"
127
.
0
.
0
.
1
:
9222
"
)
        
result
=
requests
.
get
(
url
=
"
http
:
/
/
{
}
/
json
/
version
"
.
format
(
debugger_address
)
)
        
self
.
assertTrue
(
result
.
ok
)
    
def
test_websocket_url
(
self
)
:
        
self
.
assertNotIn
(
"
webSocketUrl
"
self
.
marionette
.
session_capabilities
)
        
self
.
marionette
.
enforce_gecko_prefs
(
{
"
remote
.
active
-
protocols
"
:
2
}
)
        
try
:
            
self
.
marionette
.
quit
(
)
            
self
.
marionette
.
instance
.
app_args
.
append
(
"
-
remote
-
debugging
-
port
"
)
            
self
.
marionette
.
start_session
(
{
"
webSocketUrl
"
:
True
}
)
            
self
.
assertNotIn
(
"
webSocketUrl
"
self
.
marionette
.
session_capabilities
)
        
finally
:
            
self
.
marionette
.
clear_pref
(
"
remote
.
active
-
protocols
"
)
            
self
.
marionette
.
restart
(
)
        
if
self
.
is_bidi_enabled
(
)
:
            
self
.
marionette
.
quit
(
)
            
self
.
marionette
.
instance
.
switch_profile
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
webSocketUrl
"
:
True
}
)
            
session_id
=
self
.
marionette
.
session_id
            
websocket_url
=
self
.
marionette
.
session_capabilities
.
get
(
"
webSocketUrl
"
)
            
self
.
assertEqual
(
                
websocket_url
"
ws
:
/
/
127
.
0
.
0
.
1
:
9222
/
session
/
{
}
"
.
format
(
session_id
)
            
)
    
def
test_start_page_about_blank
(
self
)
:
        
if
self
.
is_bidi_enabled
(
)
:
            
self
.
marionette
.
quit
(
)
            
self
.
marionette
.
instance
.
app_args
.
append
(
"
-
remote
-
debugging
-
port
=
0
"
)
            
self
.
marionette
.
start_session
(
{
"
webSocketUrl
"
:
True
}
)
            
self
.
assertEqual
(
self
.
marionette
.
get_url
(
)
"
about
:
blank
"
)
    
def
test_startup_timeout
(
self
)
:
        
try
:
            
self
.
marionette
.
quit
(
)
            
with
self
.
assertRaisesRegexp
(
IOError
"
Process
killed
after
0s
"
)
:
                
self
.
marionette
.
start_session
(
timeout
=
0
)
        
finally
:
            
self
.
marionette
.
start_session
(
)
