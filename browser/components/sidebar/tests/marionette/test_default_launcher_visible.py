import
json
from
pathlib
import
Path
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
restart_with_default_prefs
(
self
prefs
clean
=
False
in_app
=
True
)
:
        
pref_path
=
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
prefs
.
js
"
        
self
.
marionette
.
quit
(
clean
=
clean
in_app
=
in_app
)
        
remove_prefs
=
[
            
f
'
user_pref
(
"
{
name
}
"
'
for
name
value
in
prefs
.
items
(
)
if
value
is
None
        
]
        
if
len
(
remove_prefs
)
>
0
:
            
with
open
(
pref_path
encoding
=
"
utf
-
8
"
)
as
prefs_file
:
                
lines
=
prefs_file
.
readlines
(
)
            
keep_lines
=
[
                
line
for
line
in
lines
if
not
any
(
s
in
line
for
s
in
remove_prefs
)
            
]
            
with
open
(
pref_path
"
w
"
encoding
=
"
utf
-
8
"
)
as
prefs_file
:
                
prefs_file
.
writelines
(
keep_lines
)
        
with
open
(
pref_path
"
a
"
)
as
prefs_file
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
                
prefs_file
.
write
(
f
'
user_pref
(
"
{
name
}
"
{
json
.
dumps
(
value
)
}
)
;
'
)
        
self
.
marionette
.
start_session
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
restart_with_default_prefs
(
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
uiCustomization
.
state
"
:
None
        
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
restart_with_default_prefs
(
{
            
"
sidebar
.
revamp
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
restart_with_default_prefs
(
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
uiCustomization
.
state
"
:
None
        
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
marionette
.
get_pref
(
"
sidebar
.
revamp
"
)
            
"
Before
enabling
sidebar
.
revamp
pref
should
be
false
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
        
self
.
assertTrue
(
            
self
.
marionette
.
get_pref
(
"
sidebar
.
revamp
"
)
            
"
The
sidebar
.
revamp
pref
should
now
be
true
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
marionette
.
get_pref
(
"
sidebar
.
revamp
"
)
            
"
The
sidebar
.
revamp
pref
should
still
be
true
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
restart_with_default_prefs
(
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
uiCustomization
.
state
"
:
None
        
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
restart_with_default_prefs
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
