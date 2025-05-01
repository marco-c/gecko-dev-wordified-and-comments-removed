from
marionette_driver
import
Wait
from
marionette_harness
import
MarionetteTestCase
default_visible_pref
=
"
sidebar
.
revamp
.
defaultLauncherVisible
"
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
    
default_visible_pref
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
set_prefs
(
prefs
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
wait_for_startup_idle_promise
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
wait_for_startup_idle_promise
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
            
BrowserInitState
.
startupIdleTaskPromise
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
wait_for_startup_idle_promise
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
                
default_visible_pref
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
remains
hidden
because
defaultLauncherVisible
=
false
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
button
should
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
wait_for_startup_idle_promise
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
un
-
hid
it
in
the
resumed
session
"
        
)
    
def
test_new_sidebar_enabled_default_visible_pref_false
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
browser
.
startup
.
page
"
:
3
                
default_visible_pref
:
False
            
}
        
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
assertTrue
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
visible
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
                
default_visible_pref
:
True
            
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
Sidebar
button
is
still
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
Sidebar
launcher
is
still
visible
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
be
hidden
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
wait_for_startup_idle_promise
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
remains
hidden
on
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
                
default_visible_pref
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
defaultLauncherVisible
is
false
"
        
)
