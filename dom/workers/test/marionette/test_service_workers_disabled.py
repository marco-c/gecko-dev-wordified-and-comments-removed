import
os
import
sys
sys
.
path
.
append
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
from
service_worker_utils
import
MarionetteServiceWorkerTestCase
class
ServiceWorkersDisabledTestCase
(
MarionetteServiceWorkerTestCase
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
install_service_worker
(
"
serviceworker
/
install_serviceworker
.
html
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
)
.
tearDown
(
)
    
def
test_service_workers_disabled_at_startup
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
profile
.
set_preferences
(
            
{
                
"
dom
.
serviceWorkers
.
enabled
"
:
False
            
}
        
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
assertFalse
(
            
self
.
is_service_worker_registered
            
"
Service
worker
registration
should
have
been
purged
"
        
)
