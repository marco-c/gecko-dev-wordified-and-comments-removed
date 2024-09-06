import
json
from
marionette_harness
import
MarionetteTestCase
vertical_parent_id
=
"
vertical
-
tabs
"
horizontal_parent_id
=
"
TabsToolbar
-
customization
-
target
"
snapshot_pref
=
"
browser
.
uiCustomization
.
horizontalTabstrip
"
customization_pref
=
"
browser
.
uiCustomization
.
state
"
class
TestInitializeVerticalTabs
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
get_area_widgets
(
self
area
)
:
        
return
self
.
marionette
.
execute_script
(
            
f
"
return
CustomizableUI
.
getWidgetIdsInArea
(
CustomizableUI
.
{
area
}
)
"
        
)
    
def
test_vertical_widgets_in_area
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
                
customization_pref
:
None
                
snapshot_pref
:
None
            
}
        
)
        
horiz_tab_ids
=
self
.
get_area_widgets
(
"
AREA_TABSTRIP
"
)
        
vertical_tab_ids
=
self
.
get_area_widgets
(
"
AREA_VERTICAL_TABSTRIP
"
)
        
self
.
assertEqual
(
            
len
(
horiz_tab_ids
)
            
0
            
msg
=
"
The
horizontal
tabstrip
area
is
empty
"
        
)
        
self
.
assertEqual
(
            
len
(
vertical_tab_ids
)
            
1
            
msg
=
"
The
vertical
tabstrip
area
has
a
single
widget
in
it
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
verticalTabs
"
False
)
        
horiz_tab_ids
=
self
.
get_area_widgets
(
"
AREA_TABSTRIP
"
)
        
vertical_tab_ids
=
self
.
get_area_widgets
(
"
AREA_VERTICAL_TABSTRIP
"
)
        
self
.
assertEqual
(
            
horiz_tab_ids
            
[
                
"
firefox
-
view
-
button
"
                
"
tabbrowser
-
tabs
"
                
"
new
-
tab
-
button
"
                
"
alltabs
-
button
"
            
]
            
msg
=
"
The
tabstrip
was
populated
with
the
expected
defaults
"
        
)
        
self
.
assertEqual
(
            
len
(
vertical_tab_ids
)
            
0
            
msg
=
"
The
vertical
tabstrip
area
was
emptied
"
        
)
    
def
test_restore_tabstrip_customizations
(
self
)
:
        
fixture_prefs
=
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
False
        
}
        
self
.
restart_with_prefs
(
            
{
                
*
*
fixture_prefs
                
customization_pref
:
None
                
snapshot_pref
:
None
            
}
        
)
        
self
.
marionette
.
execute_script
(
            
"
CustomizableUI
.
addWidgetToArea
(
'
panic
-
button
'
CustomizableUI
.
AREA_TABSTRIP
0
)
"
        
)
        
saved_state
=
json
.
loads
(
self
.
marionette
.
get_pref
(
customization_pref
)
)
        
horiz_tab_ids
=
self
.
get_area_widgets
(
"
AREA_TABSTRIP
"
)
        
print
(
f
"
After
adding
to
tabstrip
area
horiz_tab_ids
:
{
horiz_tab_ids
}
"
)
        
self
.
assertTrue
(
            
"
panic
-
button
"
in
horiz_tab_ids
"
The
widget
we
added
is
in
the
tabstrip
"
        
)
        
self
.
assertTrue
(
            
"
panic
-
button
"
in
saved_state
[
"
placements
"
]
[
"
TabsToolbar
"
]
            
"
The
widget
we
added
is
included
in
the
saved
customization
state
"
        
)
        
fixture_prefs
[
"
sidebar
.
verticalTabs
"
]
=
True
        
self
.
restart_with_prefs
(
fixture_prefs
)
        
saved_state
=
json
.
loads
(
self
.
marionette
.
get_pref
(
customization_pref
)
)
        
print
(
            
f
"
After
restarting
with
verticalTabs
=
true
saved
customization
:
{
saved_state
}
"
        
)
        
horiz_tab_ids
=
self
.
get_area_widgets
(
"
AREA_TABSTRIP
"
)
        
nav_bar_ids
=
self
.
get_area_widgets
(
"
AREA_NAVBAR
"
)
        
print
(
            
f
"
verticalTabs
is
true
and
horiz_tab_ids
:
{
horiz_tab_ids
}
nav_bar_ids
:
{
nav_bar_ids
}
"
        
)
        
self
.
assertEqual
(
            
len
(
horiz_tab_ids
)
            
0
            
msg
=
"
The
horizontal
tabstrip
area
is
empty
"
        
)
        
self
.
assertTrue
(
            
"
panic
-
button
"
in
nav_bar_ids
"
The
widget
we
added
has
moved
to
the
navbar
"
        
)
        
fixture_prefs
[
"
sidebar
.
verticalTabs
"
]
=
False
        
self
.
restart_with_prefs
(
fixture_prefs
)
        
horiz_tab_ids
=
self
.
get_area_widgets
(
"
AREA_TABSTRIP
"
)
        
self
.
assertEqual
(
            
horiz_tab_ids
[
0
]
            
"
panic
-
button
"
            
msg
=
"
The
customization
was
preserved
after
restarting
in
horizontal
tabs
mode
"
        
)
