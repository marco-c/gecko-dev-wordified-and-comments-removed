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
.
marionette_test
import
(
    
MarionetteTestCase
parameterized
)
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
AccessibleCaretCursorModeTestCase
(
MarionetteTestCase
)
:
    
'
'
'
Test
cases
for
AccessibleCaret
under
cursor
mode
.
    
We
call
the
blinking
cursor
(
nsCaret
)
as
cursor
and
call
AccessibleCaret
as
    
caret
for
short
.
    
'
'
'
    
_input_id
=
'
input
'
    
_input_padding_id
=
'
input
-
padding
'
    
_textarea_id
=
'
textarea
'
    
_textarea_one_line_id
=
'
textarea
-
one
-
line
'
    
_contenteditable_id
=
'
contenteditable
'
    
_cursor_html
=
'
test_carets_cursor
.
html
'
    
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
hide_carets_for_mouse
=
'
layout
.
accessiblecaret
.
hide_carets_for_mouse_input
'
        
self
.
prefs
=
{
            
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
            
self
.
hide_carets_for_mouse
:
False
        
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
open_test_html
(
self
test_html
)
:
        
self
.
marionette
.
navigate
(
self
.
marionette
.
absolute_url
(
test_html
)
)
    
parameterized
(
_input_id
el_id
=
_input_id
)
    
parameterized
(
_textarea_id
el_id
=
_textarea_id
)
    
parameterized
(
_contenteditable_id
el_id
=
_contenteditable_id
)
    
def
test_move_cursor_to_the_right_by_one_character
(
self
el_id
)
:
        
self
.
open_test_html
(
self
.
_cursor_html
)
        
el
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
el_id
)
        
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
move_cursor_to_front
(
)
        
cursor0_x
cursor0_y
=
sel
.
cursor_location
(
)
        
first_caret0_x
first_caret0_y
=
sel
.
first_caret_location
(
)
        
sel
.
move_cursor_by_offset
(
1
)
        
first_caret1_x
first_caret1_y
=
sel
.
first_caret_location
(
)
        
el
.
tap
(
cursor0_x
cursor0_y
)
        
self
.
actions
.
flick
(
el
first_caret0_x
first_caret0_y
                           
first_caret1_x
first_caret1_y
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
        
self
.
assertEqual
(
target_content
sel
.
content
)
    
parameterized
(
_input_id
el_id
=
_input_id
)
    
parameterized
(
_textarea_id
el_id
=
_textarea_id
)
    
parameterized
(
_contenteditable_id
el_id
=
_contenteditable_id
)
    
def
test_move_cursor_to_end_by_dragging_caret_to_bottom_right_corner
(
self
el_id
)
:
        
self
.
open_test_html
(
self
.
_cursor_html
)
        
el
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
el_id
)
        
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
move_cursor_to_front
(
)
        
el
.
tap
(
*
sel
.
cursor_location
(
)
)
        
src_x
src_y
=
sel
.
first_caret_location
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
        
self
.
assertEqual
(
target_content
sel
.
content
)
    
parameterized
(
_input_id
el_id
=
_input_id
)
    
parameterized
(
_textarea_id
el_id
=
_textarea_id
)
    
parameterized
(
_contenteditable_id
el_id
=
_contenteditable_id
)
    
def
test_move_cursor_to_front_by_dragging_caret_to_front
(
self
el_id
)
:
        
self
.
open_test_html
(
self
.
_cursor_html
)
        
el
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
el_id
)
        
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
move_cursor_to_front
(
)
        
dest_x
dest_y
=
sel
.
first_caret_location
(
)
        
el
.
tap
(
)
        
sel
.
move_cursor_to_end
(
)
        
sel
.
move_cursor_by_offset
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
cursor_location
(
)
)
        
src_x
src_y
=
sel
.
first_caret_location
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
        
self
.
assertEqual
(
target_content
sel
.
content
)
    
parameterized
(
_input_id
el_id
=
_input_id
)
    
parameterized
(
_textarea_id
el_id
=
_textarea_id
)
    
parameterized
(
_contenteditable_id
el_id
=
_contenteditable_id
)
    
def
test_dragging_caret_to_top_left_corner_after_timeout
(
self
el_id
)
:
        
self
.
open_test_html
(
self
.
_cursor_html
)
        
el
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
el_id
)
        
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
1
        
self
.
marionette
.
set_pref
(
self
.
caret_timeout_ms_pref
timeout
*
1000
)
        
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
move_cursor_to_end
(
)
        
sel
.
move_cursor_by_offset
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
cursor_location
(
)
)
        
src_x
src_y
=
sel
.
first_caret_location
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
        
self
.
assertNotEqual
(
non_target_content
sel
.
content
)
    
def
test_caret_not_appear_when_typing_in_scrollable_content
(
self
)
:
        
self
.
open_test_html
(
self
.
_cursor_html
)
        
el
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
self
.
_input_id
)
        
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
move_cursor_to_end
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
first_caret_location
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
        
self
.
assertEqual
(
target_content
sel
.
content
)
    
parameterized
(
_input_id
el_id
=
_input_id
)
    
parameterized
(
_input_padding_id
el_id
=
_input_padding_id
)
    
parameterized
(
_textarea_one_line_id
el_id
=
_textarea_one_line_id
)
    
parameterized
(
_contenteditable_id
el_id
=
_contenteditable_id
)
    
def
test_caret_not_jump_when_dragging_to_editable_content_boundary
(
self
el_id
)
:
        
self
.
open_test_html
(
self
.
_cursor_html
)
        
el
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
el_id
)
        
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
move_cursor_to_front
(
)
        
el
.
tap
(
*
sel
.
cursor_location
(
)
)
        
x
y
=
sel
.
first_caret_location
(
)
        
self
.
actions
.
flick
(
el
x
y
x
y
+
50
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
        
self
.
assertNotEqual
(
non_target_content
sel
.
content
)
    
parameterized
(
_input_id
el_id
=
_input_id
)
    
parameterized
(
_input_padding_id
el_id
=
_input_padding_id
)
    
parameterized
(
_textarea_one_line_id
el_id
=
_textarea_one_line_id
)
    
parameterized
(
_contenteditable_id
el_id
=
_contenteditable_id
)
    
def
test_caret_not_jump_to_front_when_dragging_up_to_editable_content_boundary
(
self
el_id
)
:
        
self
.
open_test_html
(
self
.
_cursor_html
)
        
el
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
el_id
)
        
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
move_cursor_to_end
(
)
        
sel
.
move_cursor_by_offset
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
cursor_location
(
)
)
        
x
y
=
sel
.
first_caret_location
(
)
        
self
.
actions
.
flick
(
el
x
y
x
y
-
50
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
        
self
.
assertNotEqual
(
non_target_content
sel
.
content
)
    
def
test_drag_caret_from_front_to_end_across_columns
(
self
)
:
        
self
.
open_test_html
(
'
test_carets_columns
.
html
'
)
        
el
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
columns
-
inner
'
)
        
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
        
before_image_1
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
before
-
image
-
1
'
)
        
before_image_1
.
tap
(
)
        
sel
.
move_cursor_to_front
(
)
        
el
.
tap
(
*
sel
.
cursor_location
(
)
)
        
src_x
src_y
=
sel
.
first_caret_location
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
        
self
.
assertEqual
(
target_content
sel
.
content
)
    
def
test_move_cursor_to_front_by_dragging_caret_to_front_br_element
(
self
)
:
        
self
.
open_test_html
(
self
.
_cursor_html
)
        
el
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
self
.
_contenteditable_id
)
        
sel
=
SelectionManager
(
el
)
        
content_to_add_1
=
'
!
'
        
content_to_add_2
=
'
\
n
\
n
'
        
target_content
=
content_to_add_1
+
content_to_add_2
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
move_cursor_to_front
(
)
        
dest_x
dest_y
=
sel
.
first_caret_location
(
)
        
el
.
send_keys
(
content_to_add_2
)
;
        
el
.
tap
(
)
        
sel
.
move_cursor_to_end
(
)
        
sel
.
move_cursor_by_offset
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
cursor_location
(
)
)
        
src_x
src_y
=
sel
.
first_caret_location
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
content_to_add_1
)
.
key_up
(
content_to_add_1
)
.
perform
(
)
        
self
.
assertEqual
(
target_content
sel
.
content
)
