from
marionette_driver
import
Wait
from
marionette_driver
.
by
import
By
from
marionette_harness
import
MarionetteTestCase
initial_prefs
=
{
    
"
sidebar
.
revamp
"
:
False
    
"
browser
.
startup
.
page
"
:
3
}
class
TestDefaultLauncherVisible
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
        
MarionetteTestCase
.
setUp
(
self
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
        
try
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
        
finally
:
            
super
(
)
.
tearDown
(
)
    
def
_close_last_tab
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
window
.
close
(
)
"
)
    
def
restart_with_prefs
(
self
prefs
)
:
        
self
.
marionette
.
enforce_gecko_prefs
(
prefs
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
        
self
.
wait_for_sidebar_initialized
(
)
    
def
is_launcher_visible
(
self
)
:
        
hidden
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
window
=
BrowserWindowTracker
.
getTopWindow
(
)
;
            
return
window
.
SidebarController
.
sidebarContainer
.
hidden
;
            
"
"
"
        
)
        
return
not
hidden
    
def
is_button_visible
(
self
)
:
        
visible
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
window
=
BrowserWindowTracker
.
getTopWindow
(
)
;
            
const
placement
=
window
.
CustomizableUI
.
getPlacementOfWidget
(
'
sidebar
-
button
'
)
;
            
if
(
!
placement
)
{
                
return
false
;
            
}
            
const
node
=
window
.
document
.
getElementById
(
"
sidebar
-
button
"
)
;
            
return
node
&
&
!
node
.
hidden
;
            
"
"
"
        
)
        
return
visible
    
def
click_toolbar_button
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
window
=
BrowserWindowTracker
.
getTopWindow
(
)
;
            
return
window
.
document
.
getElementById
(
"
sidebar
-
button
"
)
.
click
(
)
            
"
"
"
        
)
    
def
wait_for_sidebar_initialized
(
self
)
:
        
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
            
(
async
(
)
=
>
{
                
await
BrowserInitState
.
startupIdleTaskPromise
;
                
const
win
=
BrowserWindowTracker
.
getTopWindow
(
)
;
                
await
win
.
SidebarController
.
promiseInitialized
;
            
}
)
(
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
    
def
test_first_use_default_visible_pref_false
(
self
)
:
        
self
.
wait_for_sidebar_initialized
(
)
        
self
.
assertFalse
(
            
self
.
is_launcher_visible
(
)
            
"
Sidebar
launcher
is
hidden
"
        
)
        
self
.
assertFalse
(
            
self
.
is_button_visible
(
)
            
"
Sidebar
toolbar
button
is
hidden
"
        
)
        
self
.
restart_with_prefs
(
            
{
                
"
sidebar
.
revamp
"
:
True
                
"
browser
.
startup
.
page
"
:
3
            
}
        
)
        
self
.
assertTrue
(
            
self
.
is_button_visible
(
)
            
"
Sidebar
button
should
be
visible
"
        
)
        
self
.
assertFalse
(
            
self
.
is_launcher_visible
(
)
            
"
Sidebar
launcher
is
expected
to
be
initially
hidden
when
starting
with
sidebar
.
revamp
"
        
)
        
self
.
click_toolbar_button
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
is_launcher_visible
(
)
            
message
=
"
Sidebar
launcher
should
now
be
visible
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
set_context
(
"
chrome
"
)
        
self
.
wait_for_sidebar_initialized
(
)
        
self
.
assertTrue
(
            
self
.
is_launcher_visible
(
)
            
"
Sidebar
launcher
remains
visible
because
user
showed
it
in
the
resumed
session
"
        
)
    
def
test_new_sidebar_enabled_via_settings
(
self
)
:
        
self
.
wait_for_sidebar_initialized
(
)
        
self
.
assertFalse
(
            
self
.
is_launcher_visible
(
)
            
"
Sidebar
launcher
is
not
visible
"
        
)
        
self
.
assertFalse
(
            
self
.
is_button_visible
(
)
            
"
Sidebar
toolbar
button
is
not
visible
"
        
)
        
self
.
marionette
.
set_context
(
"
content
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
preferences
"
)
        
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
browserLayoutShowSidebar
"
)
.
click
(
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
is_button_visible
(
)
            
message
=
"
The
toolbar
button
is
visible
"
        
)
        
self
.
assertTrue
(
            
self
.
is_launcher_visible
(
)
            
"
The
launcher
is
shown
when
revamp
is
enabled
by
the
user
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
set_context
(
"
chrome
"
)
        
self
.
wait_for_sidebar_initialized
(
)
        
self
.
assertTrue
(
            
self
.
is_launcher_visible
(
)
            
"
Sidebar
launcher
should
still
be
shown
after
restart
"
        
)
    
def
test_new_sidebar_enabled_at_runtime_via_nimbus
(
self
)
:
        
self
.
wait_for_sidebar_initialized
(
)
        
self
.
assertFalse
(
            
self
.
is_launcher_visible
(
)
            
"
Sidebar
launcher
is
not
visible
"
        
)
        
self
.
assertFalse
(
            
self
.
is_button_visible
(
)
            
"
Sidebar
toolbar
button
is
not
visible
"
        
)
        
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
window
=
BrowserWindowTracker
.
getTopWindow
(
)
;
            
window
.
NimbusFeatures
.
sidebar
.
getVariable
=
(
)
=
>
false
;
            
"
"
"
        
)
        
showLauncherOnEnabled
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
window
=
BrowserWindowTracker
.
getTopWindow
(
)
;
            
return
window
.
SidebarController
.
SidebarManager
.
showLauncherOnEnabled
;
            
"
"
"
        
)
        
self
.
assertFalse
(
            
showLauncherOnEnabled
            
"
showLauncherOnEnabled
should
be
false
when
with
the
mocked
NimbusFeatures
getVariable
"
        
)
        
self
.
marionette
.
set_prefs
(
            
{
                
"
sidebar
.
revamp
"
:
True
                
"
sidebar
.
revamp
.
defaultLauncherVisible
"
:
False
            
}
        
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
is_button_visible
(
)
            
message
=
"
The
toolbar
button
is
visible
"
        
)
        
self
.
assertFalse
(
            
self
.
is_launcher_visible
(
)
            
"
The
launcher
is
hidden
when
revamp
is
not
initiated
by
the
user
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
set_context
(
"
chrome
"
)
        
self
.
wait_for_sidebar_initialized
(
)
        
self
.
assertFalse
(
            
self
.
is_launcher_visible
(
)
            
"
The
launcher
is
remains
hidden
after
a
restart
"
        
)
    
def
test_vertical_tabs_default_hidden
(
self
)
:
        
self
.
restart_with_prefs
(
            
{
                
"
sidebar
.
revamp
"
:
True
                
"
sidebar
.
verticalTabs
"
:
True
                
"
sidebar
.
visibility
"
:
"
always
-
show
"
            
}
        
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
is_launcher_visible
(
)
            
message
=
"
Sidebar
launcher
should
be
initially
visible
"
        
)
        
tabsWidth
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
window
=
BrowserWindowTracker
.
getTopWindow
(
)
;
            
return
document
.
getElementById
(
"
vertical
-
tabs
"
)
.
getBoundingClientRect
(
)
.
width
;
            
"
"
"
        
)
        
self
.
assertGreater
(
tabsWidth
0
"
#
vertical
-
tabs
element
has
width
"
)
        
self
.
marionette
.
set_pref
(
"
sidebar
.
visibility
"
"
hide
-
sidebar
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
not
self
.
is_launcher_visible
(
)
            
message
=
"
Sidebar
launcher
should
become
hidden
when
hide
-
sidebar
visibility
is
set
and
defaultLauncherVisible2
is
false
"
        
)
