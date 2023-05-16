from
pathlib
import
Path
from
marionette_driver
import
Wait
from
marionette_harness
import
MarionetteTestCase
class
MovedOriginDirectoryCleanupTestCase
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
enforce_gecko_prefs
(
            
{
                
"
privacy
.
sanitize
.
sanitizeOnShutdown
"
:
True
                
"
privacy
.
clearOnShutdown
.
offlineApps
"
:
True
                
"
dom
.
quotaManager
.
backgroundTask
.
enabled
"
:
False
            
}
        
)
        
self
.
moved_origin_directory
=
(
            
Path
(
self
.
marionette
.
profile_path
)
/
"
storage
"
/
"
to
-
be
-
removed
"
/
"
foo
"
        
)
        
self
.
moved_origin_directory
.
mkdir
(
parents
=
True
exist_ok
=
True
)
        
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
            
self
.
marionette
.
execute_script
(
                
"
"
"
                
Services
.
cookies
.
add
(
                    
"
example
.
local
"
                    
"
path
"
                    
"
name
"
                    
"
value
"
                    
false
                    
false
                    
false
                    
Math
.
floor
(
Date
.
now
(
)
/
1000
)
+
24
*
60
*
60
                    
{
}
                    
Ci
.
nsICookie
.
SAMESITE_NONE
                    
Ci
.
nsICookie
.
SCHEME_UNSET
                
)
;
                
"
"
"
            
)
    
def
removeAllCookies
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
            
self
.
marionette
.
execute_script
(
                
"
"
"
                
Services
.
cookies
.
removeAll
(
)
;
                
"
"
"
            
)
    
def
test_ensure_cleanup_by_quit
(
self
)
:
        
self
.
assertTrue
(
            
self
.
moved_origin_directory
.
exists
(
)
            
"
to
-
be
-
removed
subdirectory
must
exist
"
        
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
assertFalse
(
            
self
.
moved_origin_directory
.
exists
(
)
            
"
to
-
be
-
removed
subdirectory
must
disappear
"
        
)
    
def
test_ensure_cleanup_at_crashed_restart
(
self
)
:
        
self
.
assertTrue
(
            
self
.
moved_origin_directory
.
exists
(
)
            
"
to
-
be
-
removed
subdirectory
must
exist
"
        
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
(
                
"
offlineApps
"
in
self
.
marionette
.
get_pref
(
"
privacy
.
sanitize
.
pending
"
)
            
)
            
message
=
"
privacy
.
sanitize
.
pending
must
include
offlineApps
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
not
self
.
moved_origin_directory
.
exists
(
)
            
message
=
"
to
-
be
-
removed
subdirectory
must
disappear
"
        
)
    
def
test_ensure_cleanup_by_quit_with_background_task
(
self
)
:
        
self
.
assertTrue
(
            
self
.
moved_origin_directory
.
exists
(
)
            
"
to
-
be
-
removed
subdirectory
must
exist
"
        
)
        
self
.
marionette
.
set_pref
(
"
dom
.
quotaManager
.
backgroundTask
.
enabled
"
True
)
        
self
.
marionette
.
quit
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
not
self
.
moved_origin_directory
.
exists
(
)
            
message
=
"
to
-
be
-
removed
subdirectory
must
disappear
"
        
)
    
def
test_ensure_no_cleanup_when_disabled
(
self
)
:
        
self
.
assertTrue
(
            
self
.
moved_origin_directory
.
exists
(
)
            
"
to
-
be
-
removed
subdirectory
must
exist
"
        
)
        
self
.
marionette
.
set_pref
(
"
privacy
.
sanitize
.
sanitizeOnShutdown
"
False
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
assertTrue
(
            
self
.
moved_origin_directory
.
exists
(
)
            
"
to
-
be
-
removed
subdirectory
must
not
disappear
"
        
)
    
def
test_ensure_no_cleanup_when_no_cookie
(
self
)
:
        
self
.
assertTrue
(
            
self
.
moved_origin_directory
.
exists
(
)
            
"
to
-
be
-
removed
subdirectory
must
exist
"
        
)
        
self
.
removeAllCookies
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
assertTrue
(
            
self
.
moved_origin_directory
.
exists
(
)
            
"
to
-
be
-
removed
subdirectory
must
not
disappear
"
        
)
