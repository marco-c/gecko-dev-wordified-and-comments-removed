from
telemetry_harness
.
ping_filters
import
MAIN_SHUTDOWN_PING
from
telemetry_harness
.
testcase
import
TelemetryTestCase
class
TestUnicodeEncoding
(
TelemetryTestCase
)
:
    
"
"
"
Tests
for
Firefox
Telemetry
Unicode
encoding
.
"
"
"
    
def
test_unicode_encoding
(
self
)
:
        
"
"
"
Test
for
Firefox
Telemetry
Unicode
encoding
.
"
"
"
        
pref
=
"
app
.
support
.
baseURL
"
        
orig
=
"
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
            
value
=
self
.
marionette
.
execute_script
(
                
r
"
"
"
                
Services
.
prefs
.
setStringPref
(
"
{
pref
}
"
"
{
orig
}
"
)
;
                
return
Services
.
prefs
.
getStringPref
(
"
{
pref
}
"
)
;
                
"
"
"
.
format
(
                    
orig
=
orig
                    
pref
=
pref
                
)
            
)
        
self
.
assertEqual
(
value
orig
)
        
ping1
=
self
.
wait_for_ping
(
self
.
restart_browser
MAIN_SHUTDOWN_PING
)
        
self
.
assertEqual
(
            
ping1
[
"
environment
"
]
[
"
settings
"
]
[
"
userPrefs
"
]
[
pref
]
            
orig
        
)
