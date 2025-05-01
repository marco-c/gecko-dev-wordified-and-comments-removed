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
set_pref
(
"
sidebar
.
revamp
"
True
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
restart_with_prefs
(
self
prefs
)
:
        
for
name
value
in
prefs
.
items
(
)
:
            
if
value
is
None
:
                
self
.
marionette
.
clear_pref
(
name
)
            
else
:
                
self
.
marionette
.
set_pref
(
name
value
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
is_launcher_hidden
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
hidden
    
def
test_default_visible_pref
(
self
)
:
        
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
        
self
.
restart_with_prefs
(
            
{
                
default_visible_pref
:
False
                
"
sidebar
.
backupState
"
:
None
            
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
is_launcher_hidden
(
)
            
message
=
"
Launcher
should
be
hidden
after
restart
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
visible
again
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
still
visible
after
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
marionette
.
quit
(
)
        
self
.
marionette
.
start_session
(
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
revamp
"
True
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
verticalTabs
"
True
)
        
self
.
marionette
.
set_pref
(
default_visible_pref
False
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
self
.
is_launcher_hidden
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
