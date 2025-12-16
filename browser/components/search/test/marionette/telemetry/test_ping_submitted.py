from
marionette_driver
import
Wait
from
marionette_harness
.
marionette_test
import
MarionetteTestCase
class
TestPingSubmitted
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
enforce_gecko_prefs
(
            
{
                
"
datareporting
.
healthreport
.
uploadEnabled
"
:
True
                
"
telemetry
.
fog
.
test
.
localhost_port
"
:
3000
                
"
browser
.
search
.
log
"
:
True
            
}
        
)
        
script
=
"
"
"
            
let
[
outerResolve
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
                
if
(
!
Services
.
prefs
.
getBoolPref
(
"
browser
.
search
.
serpEventTelemetryCategorization
.
enabled
"
)
)
{
                    
let
inited
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
categorization
-
recorder
-
init
"
)
;
                        
innerResolve
(
)
;
                    
}
"
categorization
-
recorder
-
init
"
)
;
                    
}
)
;
                    
Services
.
prefs
.
setBoolPref
(
"
browser
.
search
.
serpEventTelemetryCategorization
.
enabled
"
true
)
;
                    
await
inited
;
                
}
            
}
)
(
)
.
then
(
outerResolve
)
;
        
"
"
"
        
self
.
marionette
.
execute_async_script
(
script
)
    
def
test_ping_submit_on_start
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
            
const
{
SERPCategorizationRecorder
}
=
ChromeUtils
.
importESModule
(
"
moz
-
src
:
/
/
/
browser
/
components
/
search
/
SERPCategorization
.
sys
.
mjs
"
)
;
            
SERPCategorizationRecorder
.
recordCategorizationTelemetry
(
{
                
organic_category
:
"
3
"
                
organic_num_domains
:
"
1
"
                
organic_num_inconclusive
:
"
0
"
                
organic_num_unknown
:
"
0
"
                
sponsored_category
:
"
4
"
                
sponsored_num_domains
:
"
2
"
                
sponsored_num_inconclusive
:
"
0
"
                
sponsored_num_unknown
:
"
0
"
                
mappings_version
:
"
1
"
                
app_version
:
"
124
"
                
channel
:
"
nightly
"
                
region
:
"
US
"
                
partner_code
:
"
ff
"
                
provider
:
"
example
"
                
tagged
:
"
true
"
                
num_ads_clicked
:
"
0
"
                
num_ads_hidden
:
"
0
"
                
num_ads_loaded
:
"
2
"
                
num_ads_visible
:
"
2
"
            
}
)
;
                
"
"
"
        
)
        
Wait
(
self
.
marionette
timeout
=
60
)
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
execute_script
(
                
"
"
"
            
return
(
Glean
.
serp
.
categorization
.
testGetValue
(
)
?
.
length
?
?
0
)
=
=
1
;
                
"
"
"
            
)
            
message
=
"
Should
have
recorded
a
SERP
categorization
event
before
restart
.
"
        
)
        
self
.
marionette
.
restart
(
clean
=
False
in_app
=
True
)
        
Wait
(
self
.
marionette
timeout
=
60
)
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
execute_script
(
                
"
"
"
            
return
(
Glean
.
serp
.
categorization
.
testGetValue
(
)
?
.
length
?
?
0
)
=
=
0
;
                
"
"
"
            
)
            
message
=
"
SERP
categorization
should
have
been
sent
some
time
after
restart
.
"
        
)
