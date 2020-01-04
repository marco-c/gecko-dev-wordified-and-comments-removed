#
-
*
-
coding
:
utf
-
8
-
*
-
import
string
from
marionette
import
MarionetteTestCase
from
marionette_driver
.
by
import
By
from
marionette_driver
.
marionette
import
Actions
from
marionette_driver
.
selection
import
SelectionManager
class
CommonCaretTestCase
(
object
)
:
    
'
'
'
Common
test
cases
for
a
collapsed
selection
with
a
single
caret
.
    
To
run
these
test
cases
a
subclass
must
inherit
from
both
this
class
and
    
MarionetteTestCase
.
    
'
'
'
    
def
setUp
(
self
)
:
        
super
(
CommonCaretTestCase
self
)
.
setUp
(
)
        
self
.
actions
=
Actions
(
self
.
marionette
)
    
def
timeout_ms
(
self
)
:
        
'
Return
touch
caret
expiration
time
in
milliseconds
.
'
        
return
self
.
marionette
.
get_pref
(
self
.
caret_timeout_ms_pref
)
    
def
open_test_html
(
self
)
:
        
'
Open
html
for
testing
and
locate
elements
.
'
        
test_html
=
self
.
marionette
.
absolute_url
(
'
test_touchcaret
.
html
'
)
        
self
.
marionette
.
navigate
(
test_html
)
        
self
.
_input
=
self
.
marionette
.
find_element
(
By
.
ID
'
input
'
)
        
self
.
_textarea
=
self
.
marionette
.
find_element
(
By
.
ID
'
textarea
'
)
        
self
.
_contenteditable
=
self
.
marionette
.
find_element
(
By
.
ID
'
contenteditable
'
)
    
def
_test_move_caret_to_the_right_by_one_character
(
self
el
assertFunc
)
:
        
sel
=
SelectionManager
(
el
)
        
content_to_add
=
'
!
'
        
target_content
=
sel
.
content
        
target_content
=
target_content
[
:
1
]
+
content_to_add
+
target_content
[
1
:
]
        
el
.
tap
(
)
        
sel
.
move_caret_to_front
(
)
        
caret0_x
caret0_y
=
sel
.
caret_location
(
)
        
touch_caret0_x
touch_caret0_y
=
sel
.
touch_caret_location
(
)
        
sel
.
move_caret_by_offset
(
1
)
        
touch_caret1_x
touch_caret1_y
=
sel
.
touch_caret_location
(
)
        
el
.
tap
(
caret0_x
caret0_y
)
        
self
.
actions
.
flick
(
el
touch_caret0_x
touch_caret0_y
                           
touch_caret1_x
touch_caret1_y
)
.
perform
(
)
        
self
.
actions
.
key_down
(
content_to_add
)
.
key_up
(
content_to_add
)
.
perform
(
)
        
assertFunc
(
target_content
sel
.
content
)
    
def
_test_move_caret_to_end_by_dragging_touch_caret_to_bottom_right_corner
(
self
el
assertFunc
)
:
        
sel
=
SelectionManager
(
el
)
        
content_to_add
=
'
!
'
        
target_content
=
sel
.
content
+
content_to_add
        
el
.
tap
(
)
        
sel
.
move_caret_to_front
(
)
        
el
.
tap
(
*
sel
.
caret_location
(
)
)
        
src_x
src_y
=
sel
.
touch_caret_location
(
)
        
dest_x
dest_y
=
el
.
size
[
'
width
'
]
el
.
size
[
'
height
'
]
        
self
.
actions
.
flick
(
el
src_x
src_y
dest_x
dest_y
)
.
perform
(
)
        
self
.
actions
.
key_down
(
content_to_add
)
.
key_up
(
content_to_add
)
.
perform
(
)
        
assertFunc
(
target_content
sel
.
content
)
    
def
_test_move_caret_to_front_by_dragging_touch_caret_to_front_of_content
(
self
el
assertFunc
)
:
        
sel
=
SelectionManager
(
el
)
        
content_to_add
=
'
!
'
        
target_content
=
content_to_add
+
sel
.
content
        
el
.
tap
(
)
        
sel
.
move_caret_to_front
(
)
        
dest_x
dest_y
=
sel
.
touch_caret_location
(
)
        
el
.
tap
(
)
        
sel
.
move_caret_to_end
(
)
        
sel
.
move_caret_by_offset
(
1
backward
=
True
)
        
el
.
tap
(
*
sel
.
caret_location
(
)
)
        
src_x
src_y
=
sel
.
touch_caret_location
(
)
        
self
.
actions
.
flick
(
el
src_x
src_y
dest_x
dest_y
)
.
perform
(
)
        
self
.
actions
.
key_down
(
content_to_add
)
.
key_up
(
content_to_add
)
.
perform
(
)
        
assertFunc
(
target_content
sel
.
content
)
    
def
_test_touch_caret_timeout_by_dragging_it_to_top_left_corner_after_timout
(
self
el
assertFunc
)
:
        
sel
=
SelectionManager
(
el
)
        
content_to_add
=
'
!
'
        
non_target_content
=
content_to_add
+
sel
.
content
        
timeout
=
self
.
timeout_ms
(
)
/
1000
.
0
        
timeout
*
=
3
        
el
.
tap
(
)
        
sel
.
move_caret_to_end
(
)
        
sel
.
move_caret_by_offset
(
1
backward
=
True
)
        
el
.
tap
(
*
sel
.
caret_location
(
)
)
        
src_x
src_y
=
sel
.
touch_caret_location
(
)
        
dest_x
dest_y
=
0
0
        
self
.
actions
.
wait
(
timeout
)
.
flick
(
el
src_x
src_y
dest_x
dest_y
)
.
perform
(
)
        
self
.
actions
.
key_down
(
content_to_add
)
.
key_up
(
content_to_add
)
.
perform
(
)
        
assertFunc
(
non_target_content
sel
.
content
)
    
def
_test_touch_caret_hides_after_receiving_wheel_event
(
self
el
assertFunc
)
:
        
sel
=
SelectionManager
(
el
)
        
content_to_add
=
'
!
'
        
non_target_content
=
content_to_add
+
sel
.
content
        
el
.
tap
(
)
        
sel
.
move_caret_to_end
(
)
        
sel
.
move_caret_by_offset
(
1
backward
=
True
)
        
el
.
tap
(
*
sel
.
caret_location
(
)
)
        
src_x
src_y
=
sel
.
touch_caret_location
(
)
        
dest_x
dest_y
=
0
0
        
el_center_x
el_center_y
=
el
.
rect
[
'
x
'
]
el
.
rect
[
'
y
'
]
        
self
.
marionette
.
execute_script
(
            
'
'
'
            
var
utils
=
window
.
QueryInterface
(
Components
.
interfaces
.
nsIInterfaceRequestor
)
                              
.
getInterface
(
Components
.
interfaces
.
nsIDOMWindowUtils
)
;
            
utils
.
sendWheelEvent
(
arguments
[
0
]
arguments
[
1
]
                                 
0
10
0
WheelEvent
.
DOM_DELTA_PIXEL
                                 
0
0
0
0
)
;
            
'
'
'
            
script_args
=
[
el_center_x
el_center_y
]
            
sandbox
=
'
system
'
        
)
        
self
.
actions
.
flick
(
el
src_x
src_y
dest_x
dest_y
)
.
perform
(
)
        
self
.
actions
.
key_down
(
content_to_add
)
.
key_up
(
content_to_add
)
.
perform
(
)
        
assertFunc
(
non_target_content
sel
.
content
)
    
def
_test_caret_not_appear_when_typing_in_scrollable_content
(
self
el
assertFunc
)
:
        
sel
=
SelectionManager
(
el
)
        
content_to_add
=
'
!
'
        
target_content
=
sel
.
content
+
string
.
ascii_letters
+
content_to_add
        
el
.
tap
(
)
        
sel
.
move_caret_to_end
(
)
        
el
.
send_keys
(
string
.
ascii_letters
)
        
src_x
src_y
=
sel
.
touch_caret_location
(
)
        
dest_x
dest_y
=
0
0
        
self
.
actions
.
flick
(
el
src_x
src_y
dest_x
dest_y
)
.
perform
(
)
        
el
.
send_keys
(
content_to_add
)
        
assertFunc
(
target_content
sel
.
content
)
    
def
test_input_move_caret_to_the_right_by_one_character
(
self
)
:
        
self
.
open_test_html
(
)
        
self
.
_test_move_caret_to_the_right_by_one_character
(
self
.
_input
self
.
assertEqual
)
    
def
test_input_move_caret_to_end_by_dragging_touch_caret_to_bottom_right_corner
(
self
)
:
        
self
.
open_test_html
(
)
        
self
.
_test_move_caret_to_end_by_dragging_touch_caret_to_bottom_right_corner
(
self
.
_input
self
.
assertEqual
)
    
def
test_input_move_caret_to_front_by_dragging_touch_caret_to_top_left_corner
(
self
)
:
        
self
.
open_test_html
(
)
        
self
.
_test_move_caret_to_front_by_dragging_touch_caret_to_front_of_content
(
self
.
_input
self
.
assertEqual
)
    
def
test_input_caret_not_appear_when_typing_in_scrollable_content
(
self
)
:
        
self
.
open_test_html
(
)
        
self
.
_test_caret_not_appear_when_typing_in_scrollable_content
(
self
.
_input
self
.
assertEqual
)
    
def
test_input_touch_caret_timeout
(
self
)
:
        
with
self
.
marionette
.
using_prefs
(
{
self
.
caret_timeout_ms_pref
:
1000
}
)
:
            
self
.
open_test_html
(
)
            
self
.
_test_touch_caret_timeout_by_dragging_it_to_top_left_corner_after_timout
(
self
.
_input
self
.
assertNotEqual
)
    
def
test_input_move_caret_to_the_right_by_one_character_disabled
(
self
)
:
        
with
self
.
marionette
.
using_prefs
(
{
self
.
caret_tested_pref
:
False
}
)
:
            
self
.
open_test_html
(
)
            
self
.
_test_move_caret_to_the_right_by_one_character
(
self
.
_input
self
.
assertNotEqual
)
    
def
test_input_move_caret_to_front_by_dragging_touch_caret_to_top_left_corner_disabled
(
self
)
:
        
with
self
.
marionette
.
using_prefs
(
{
self
.
caret_tested_pref
:
False
}
)
:
            
self
.
open_test_html
(
)
            
self
.
_test_move_caret_to_front_by_dragging_touch_caret_to_front_of_content
(
self
.
_input
self
.
assertNotEqual
)
    
def
test_textarea_move_caret_to_the_right_by_one_character
(
self
)
:
        
self
.
open_test_html
(
)
        
self
.
_test_move_caret_to_the_right_by_one_character
(
self
.
_textarea
self
.
assertEqual
)
    
def
test_textarea_move_caret_to_end_by_dragging_touch_caret_to_bottom_right_corner
(
self
)
:
        
self
.
open_test_html
(
)
        
self
.
_test_move_caret_to_end_by_dragging_touch_caret_to_bottom_right_corner
(
self
.
_textarea
self
.
assertEqual
)
    
def
test_textarea_move_caret_to_front_by_dragging_touch_caret_to_top_left_corner
(
self
)
:
        
self
.
open_test_html
(
)
        
self
.
_test_move_caret_to_front_by_dragging_touch_caret_to_front_of_content
(
self
.
_textarea
self
.
assertEqual
)
    
def
test_textarea_touch_caret_timeout
(
self
)
:
        
with
self
.
marionette
.
using_prefs
(
{
self
.
caret_timeout_ms_pref
:
1000
}
)
:
            
self
.
open_test_html
(
)
            
self
.
_test_touch_caret_timeout_by_dragging_it_to_top_left_corner_after_timout
(
self
.
_textarea
self
.
assertNotEqual
)
    
def
test_textarea_move_caret_to_the_right_by_one_character_disabled
(
self
)
:
        
with
self
.
marionette
.
using_prefs
(
{
self
.
caret_tested_pref
:
False
}
)
:
            
self
.
open_test_html
(
)
            
self
.
_test_move_caret_to_the_right_by_one_character
(
self
.
_textarea
self
.
assertNotEqual
)
    
def
test_textarea_move_caret_to_front_by_dragging_touch_caret_to_top_left_corner_disabled
(
self
)
:
        
with
self
.
marionette
.
using_prefs
(
{
self
.
caret_tested_pref
:
False
}
)
:
            
self
.
open_test_html
(
)
            
self
.
_test_move_caret_to_front_by_dragging_touch_caret_to_front_of_content
(
self
.
_textarea
self
.
assertNotEqual
)
    
def
test_contenteditable_move_caret_to_the_right_by_one_character
(
self
)
:
        
self
.
open_test_html
(
)
        
self
.
_test_move_caret_to_the_right_by_one_character
(
self
.
_contenteditable
self
.
assertEqual
)
    
def
test_contenteditable_move_caret_to_end_by_dragging_touch_caret_to_bottom_right_corner
(
self
)
:
        
self
.
open_test_html
(
)
        
self
.
_test_move_caret_to_end_by_dragging_touch_caret_to_bottom_right_corner
(
self
.
_contenteditable
self
.
assertEqual
)
    
def
test_contenteditable_move_caret_to_front_by_dragging_touch_caret_to_top_left_corner
(
self
)
:
        
self
.
open_test_html
(
)
        
self
.
_test_move_caret_to_front_by_dragging_touch_caret_to_front_of_content
(
self
.
_contenteditable
self
.
assertEqual
)
    
def
test_contenteditable_touch_caret_timeout
(
self
)
:
        
with
self
.
marionette
.
using_prefs
(
{
self
.
caret_timeout_ms_pref
:
1000
}
)
:
            
self
.
open_test_html
(
)
            
self
.
_test_touch_caret_timeout_by_dragging_it_to_top_left_corner_after_timout
(
self
.
_contenteditable
self
.
assertNotEqual
)
    
def
test_contenteditable_move_caret_to_the_right_by_one_character_disabled
(
self
)
:
        
with
self
.
marionette
.
using_prefs
(
{
self
.
caret_tested_pref
:
False
}
)
:
            
self
.
open_test_html
(
)
            
self
.
_test_move_caret_to_the_right_by_one_character
(
self
.
_contenteditable
self
.
assertNotEqual
)
    
def
test_contenteditable_move_caret_to_front_by_dragging_touch_caret_to_top_left_corner_disabled
(
self
)
:
        
with
self
.
marionette
.
using_prefs
(
{
self
.
caret_tested_pref
:
False
}
)
:
            
self
.
open_test_html
(
)
            
self
.
_test_move_caret_to_front_by_dragging_touch_caret_to_front_of_content
(
self
.
_contenteditable
self
.
assertNotEqual
)
class
TouchCaretTestCase
(
CommonCaretTestCase
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
TouchCaretTestCase
self
)
.
setUp
(
)
        
self
.
caret_tested_pref
=
'
touchcaret
.
enabled
'
        
self
.
caret_timeout_ms_pref
=
'
touchcaret
.
expiration
.
time
'
        
self
.
prefs
=
{
            
'
layout
.
accessiblecaret
.
enabled
'
:
False
            
self
.
caret_tested_pref
:
True
            
self
.
caret_timeout_ms_pref
:
0
        
}
        
self
.
marionette
.
set_prefs
(
self
.
prefs
)
    
def
test_input_touch_caret_hides_after_receiving_wheel_event
(
self
)
:
        
self
.
open_test_html
(
)
        
self
.
_test_touch_caret_hides_after_receiving_wheel_event
(
self
.
_input
self
.
assertNotEqual
)
    
def
test_textarea_touch_caret_hides_after_receiving_wheel_event
(
self
)
:
        
self
.
open_test_html
(
)
        
self
.
_test_touch_caret_hides_after_receiving_wheel_event
(
self
.
_textarea
self
.
assertNotEqual
)
    
def
test_contenteditable_touch_caret_hides_after_receiving_wheel_event
(
self
)
:
        
self
.
open_test_html
(
)
        
self
.
_test_touch_caret_hides_after_receiving_wheel_event
(
self
.
_contenteditable
self
.
assertNotEqual
)
class
AccessibleCaretCursorModeTestCase
(
CommonCaretTestCase
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
AccessibleCaretCursorModeTestCase
self
)
.
setUp
(
)
        
self
.
caret_tested_pref
=
'
layout
.
accessiblecaret
.
enabled
'
        
self
.
caret_timeout_ms_pref
=
'
layout
.
accessiblecaret
.
timeout_ms
'
        
self
.
prefs
=
{
            
'
touchcaret
.
enabled
'
:
False
            
self
.
caret_tested_pref
:
True
            
self
.
caret_timeout_ms_pref
:
0
        
}
        
self
.
marionette
.
set_prefs
(
self
.
prefs
)
