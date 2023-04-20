import
os
from
marionette_driver
import
Wait
from
marionette_harness
import
MarionetteTestCase
class
MarionetteServiceWorkerTestCase
(
MarionetteTestCase
)
:
    
def
install_service_worker
(
self
path
)
:
        
install_url
=
self
.
marionette
.
absolute_url
(
path
)
        
self
.
marionette
.
navigate
(
install_url
)
        
Wait
(
self
.
marionette
)
.
until
(
            
lambda
_
:
self
.
is_service_worker_registered
            
message
=
"
Service
worker
not
successfully
installed
"
        
)
        
Wait
(
self
.
marionette
timeout
=
10
)
.
until
(
            
lambda
_
:
self
.
profile_serviceworker_txt_exists
            
message
=
"
Service
worker
not
stored
in
profile
"
        
)
        
self
.
marionette
.
navigate
(
"
about
:
blank
"
)
    
property
    
def
profile_serviceworker_txt_exists
(
self
)
:
        
return
"
serviceworker
.
txt
"
in
os
.
listdir
(
self
.
marionette
.
profile_path
)
    
property
    
def
is_service_worker_registered
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
            
return
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
swm
=
Cc
[
"
mozilla
.
org
/
serviceworkers
/
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
nsIServiceWorkerManager
                
)
;
                
let
ssm
=
Services
.
scriptSecurityManager
;
                
let
principal
=
ssm
.
createContentPrincipalFromOrigin
(
arguments
[
0
]
)
;
                
let
serviceWorkers
=
swm
.
getAllRegistrations
(
)
;
                
for
(
let
i
=
0
;
i
<
serviceWorkers
.
length
;
i
+
+
)
{
                    
let
sw
=
serviceWorkers
.
queryElementAt
(
                        
i
                        
Ci
.
nsIServiceWorkerRegistrationInfo
                    
)
;
                    
if
(
sw
.
principal
.
origin
=
=
principal
.
origin
)
{
                        
return
true
;
                    
}
                
}
                
return
false
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
"
)
)
            
)
