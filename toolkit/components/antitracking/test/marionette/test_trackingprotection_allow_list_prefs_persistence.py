from
marionette_harness
import
MarionetteTestCase
class
TrackingProtectionAllowListPreferenceTestCase
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
browser
.
contentblocking
.
category
"
:
"
strict
"
                
"
privacy
.
trackingprotection
.
allow_list
.
baseline
.
enabled
"
:
False
                
"
privacy
.
trackingprotection
.
allow_list
.
convenience
.
enabled
"
:
False
                
"
privacy
.
trackingprotection
.
allow_list
.
hasMigratedCategoryPrefs
"
:
True
            
}
        
)
        
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
test_state_after_restart
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
clean
=
False
in_app
=
True
)
        
baseline
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
                
return
Services
.
prefs
.
getBoolPref
(
"
privacy
.
trackingprotection
.
allow_list
.
baseline
.
enabled
"
)
            
"
"
"
        
)
        
self
.
assertEqual
(
            
baseline
False
"
Baseline
should
remain
unchanged
on
restart
.
"
        
)
        
convenience
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
                
return
Services
.
prefs
.
getBoolPref
(
"
privacy
.
trackingprotection
.
allow_list
.
convenience
.
enabled
"
)
            
"
"
"
        
)
        
self
.
assertEqual
(
            
convenience
False
"
Convenience
should
remain
unchanged
on
restart
.
"
        
)
