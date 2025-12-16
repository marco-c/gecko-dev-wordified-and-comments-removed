import
os
import
sys
from
marionette_driver
import
Wait
from
marionette_driver
.
addons
import
Addons
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
service_worker_testutils
import
(
    
EXT_DIR_PATH
    
EXT_ID
    
PREF_BG_SW_ENABLED
    
PREF_PERSIST_TEMP_ADDONS
    
MarionetteServiceWorkerTestCase
)
class
PurgeExtensionServiceWorkersOnPrefDisabled
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
test_extension_id
=
EXT_ID
        
self
.
marionette
.
set_pref
(
PREF_BG_SW_ENABLED
True
)
        
self
.
marionette
.
set_pref
(
PREF_PERSIST_TEMP_ADDONS
True
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
test_unregistering_service_worker_when_clearing_data
(
self
)
:
        
self
.
install_extension_with_service_worker
(
)
        
self
.
marionette
.
set_pref
(
PREF_BG_SW_ENABLED
False
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
assertFalse
(
self
.
is_extension_service_worker_registered
)
    
def
install_extension_with_service_worker
(
self
)
:
        
addons
=
Addons
(
self
.
marionette
)
        
test_extension_path
=
os
.
path
.
join
(
            
os
.
path
.
dirname
(
self
.
filepath
)
"
data
"
EXT_DIR_PATH
        
)
        
addons
.
install
(
test_extension_path
temp
=
True
)
        
self
.
test_extension_base_url
=
self
.
get_extension_url
(
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
is_extension_service_worker_registered
            
message
=
"
Wait
the
extension
service
worker
to
be
registered
"
        
)
