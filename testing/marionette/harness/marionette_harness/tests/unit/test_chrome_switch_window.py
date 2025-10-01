import
os
import
sys
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
test_switch_window
import
TestSwitchToWindowContent
class
TestSwitchWindowChrome
(
TestSwitchToWindowContent
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
TestSwitchWindowChrome
self
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
        
self
.
close_all_windows
(
)
        
super
(
TestSwitchWindowChrome
self
)
.
tearDown
(
)
    
def
test_switch_to_unloaded_tab
(
self
)
:
        
pass
    
def
test_switch_tabs_for_new_background_window_without_focus_change
(
self
)
:
        
second_tab
=
self
.
open_tab
(
focus
=
True
)
        
self
.
marionette
.
switch_to_window
(
second_tab
focus
=
True
)
        
second_tab_index
=
self
.
get_selected_tab_index
(
)
        
self
.
assertNotEqual
(
second_tab_index
self
.
selected_tab_index
)
        
with
self
.
marionette
.
using_context
(
"
content
"
)
:
            
tab_in_new_window
=
self
.
open_window
(
)
        
self
.
assertEqual
(
self
.
marionette
.
current_window_handle
second_tab
)
        
self
.
assertEqual
(
            
self
.
marionette
.
current_chrome_window_handle
self
.
start_window
        
)
        
self
.
assertEqual
(
self
.
get_selected_tab_index
(
)
second_tab_index
)
        
self
.
marionette
.
switch_to_window
(
tab_in_new_window
focus
=
False
)
        
self
.
assertEqual
(
self
.
marionette
.
current_window_handle
tab_in_new_window
)
        
self
.
assertNotEqual
(
            
self
.
marionette
.
current_chrome_window_handle
self
.
start_window
        
)
        
self
.
assertEqual
(
self
.
get_selected_tab_index
(
)
second_tab_index
)
    
def
test_switch_tabs_for_new_foreground_window_with_focus_change
(
self
)
:
        
second_tab
=
self
.
open_tab
(
)
        
self
.
marionette
.
switch_to_window
(
second_tab
focus
=
True
)
        
second_tab_index
=
self
.
get_selected_tab_index
(
)
        
self
.
assertNotEqual
(
second_tab_index
self
.
selected_tab_index
)
        
with
self
.
marionette
.
using_context
(
"
content
"
)
:
            
tab_in_new_window
=
self
.
open_window
(
focus
=
True
)
        
self
.
assertEqual
(
self
.
marionette
.
current_window_handle
second_tab
)
        
self
.
assertEqual
(
            
self
.
marionette
.
current_chrome_window_handle
self
.
start_window
        
)
        
self
.
assertNotEqual
(
self
.
get_selected_tab_index
(
)
second_tab_index
)
        
self
.
marionette
.
switch_to_window
(
tab_in_new_window
)
        
self
.
assertEqual
(
self
.
marionette
.
current_window_handle
tab_in_new_window
)
        
self
.
assertNotEqual
(
            
self
.
marionette
.
current_chrome_window_handle
self
.
start_window
        
)
        
self
.
assertNotEqual
(
self
.
get_selected_tab_index
(
)
second_tab_index
)
        
self
.
marionette
.
switch_to_window
(
second_tab
focus
=
True
)
        
self
.
assertEqual
(
self
.
marionette
.
current_window_handle
second_tab
)
        
self
.
assertEqual
(
            
self
.
marionette
.
current_chrome_window_handle
self
.
start_window
        
)
    
def
test_switch_tabs_for_new_foreground_window_without_focus_change
(
self
)
:
        
second_tab
=
self
.
open_tab
(
)
        
self
.
marionette
.
switch_to_window
(
second_tab
focus
=
True
)
        
second_tab_index
=
self
.
get_selected_tab_index
(
)
        
self
.
assertNotEqual
(
second_tab_index
self
.
selected_tab_index
)
        
self
.
open_window
(
focus
=
True
)
        
self
.
assertEqual
(
self
.
marionette
.
current_window_handle
second_tab
)
        
self
.
assertEqual
(
            
self
.
marionette
.
current_chrome_window_handle
self
.
start_window
        
)
        
self
.
assertNotEqual
(
self
.
get_selected_tab_index
(
)
second_tab_index
)
        
self
.
marionette
.
switch_to_window
(
second_tab
focus
=
False
)
        
self
.
assertEqual
(
self
.
marionette
.
current_window_handle
second_tab
)
        
self
.
assertEqual
(
            
self
.
marionette
.
current_chrome_window_handle
self
.
start_window
        
)
        
self
.
assertNotEqual
(
self
.
get_selected_tab_index
(
)
second_tab_index
)
