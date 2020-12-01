from
__future__
import
absolute_import
import
sys
import
unittest
from
marionette_driver
.
by
import
By
from
marionette_driver
.
errors
import
(
    
ElementNotAccessibleException
    
ElementNotInteractableException
    
ElementClickInterceptedException
)
from
marionette_harness
import
MarionetteTestCase
class
TestAccessibility
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
TestAccessibility
self
)
.
setUp
(
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
set_pref
(
"
dom
.
ipc
.
processCount
"
1
)
    
def
tearDown
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
clear_pref
(
"
dom
.
ipc
.
processCount
"
)
    
valid_elementIDs
=
[
        
"
button1
"
        
"
button2
"
        
"
button13
"
        
"
button17
"
    
]
    
invalid_elementIDs
=
[
        
"
button3
"
        
"
button4
"
        
"
button5
"
        
"
button6
"
        
"
button7
"
        
"
button8
"
        
"
button14
"
    
]
    
falsy_elements
=
[
        
"
button9
"
        
"
button10
"
    
]
    
displayed_elementIDs
=
[
"
button1
"
"
button2
"
"
button4
"
"
button5
"
"
button6
"
]
    
displayed_but_have_no_accessible_elementIDs
=
[
        
"
button3
"
        
"
button7
"
        
"
button8
"
        
"
no_accessible_but_displayed
"
    
]
    
disabled_elementIDs
=
[
"
button11
"
"
no_accessible_but_disabled
"
]
    
aria_disabled_elementIDs
=
[
"
button12
"
]
    
pointer_events_none_elementIDs
=
[
"
button15
"
"
button16
"
]
    
valid_option_elementIDs
=
[
"
option1
"
"
option2
"
]
    
def
run_element_test
(
self
ids
testFn
)
:
        
for
id
in
ids
:
            
element
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
id
)
            
testFn
(
element
)
    
def
setup_accessibility
(
self
enable_a11y_checks
=
True
navigate
=
True
)
:
        
self
.
marionette
.
delete_session
(
)
        
self
.
marionette
.
start_session
(
{
"
moz
:
accessibilityChecks
"
:
enable_a11y_checks
}
)
        
self
.
assertEqual
(
            
self
.
marionette
.
session_capabilities
[
"
moz
:
accessibilityChecks
"
]
            
enable_a11y_checks
)
        
if
navigate
:
            
test_accessibility
=
self
.
marionette
.
absolute_url
(
"
test_accessibility
.
html
"
)
            
self
.
marionette
.
navigate
(
test_accessibility
)
    
def
test_valid_single_tap
(
self
)
:
        
self
.
setup_accessibility
(
)
        
self
.
run_element_test
(
self
.
valid_elementIDs
lambda
button
:
button
.
tap
(
)
)
    
def
test_single_tap_raises_element_not_accessible
(
self
)
:
        
self
.
setup_accessibility
(
)
        
self
.
run_element_test
(
self
.
invalid_elementIDs
                              
lambda
button
:
self
.
assertRaises
(
ElementNotAccessibleException
                                                               
button
.
tap
)
)
        
self
.
run_element_test
(
self
.
falsy_elements
                              
lambda
button
:
self
.
assertRaises
(
ElementNotInteractableException
                                                               
button
.
tap
)
)
    
def
test_single_tap_raises_no_exceptions
(
self
)
:
        
self
.
setup_accessibility
(
False
True
)
        
self
.
run_element_test
(
self
.
invalid_elementIDs
lambda
button
:
button
.
tap
(
)
)
        
self
.
run_element_test
(
self
.
falsy_elements
                              
lambda
button
:
self
.
assertRaises
(
ElementNotInteractableException
                                                               
button
.
tap
)
)
    
def
test_valid_click
(
self
)
:
        
self
.
setup_accessibility
(
)
        
self
.
run_element_test
(
self
.
valid_elementIDs
lambda
button
:
button
.
click
(
)
)
    
def
test_click_raises_element_not_accessible
(
self
)
:
        
self
.
setup_accessibility
(
)
        
self
.
run_element_test
(
self
.
invalid_elementIDs
                              
lambda
button
:
self
.
assertRaises
(
ElementNotAccessibleException
                                                               
button
.
click
)
)
        
self
.
run_element_test
(
self
.
falsy_elements
                              
lambda
button
:
self
.
assertRaises
(
ElementNotInteractableException
                                                               
button
.
click
)
)
    
def
test_click_raises_no_exceptions
(
self
)
:
        
self
.
setup_accessibility
(
False
True
)
        
self
.
run_element_test
(
self
.
invalid_elementIDs
lambda
button
:
button
.
click
(
)
)
        
self
.
run_element_test
(
self
.
falsy_elements
                              
lambda
button
:
self
.
assertRaises
(
ElementNotInteractableException
                                                               
button
.
click
)
)
    
def
test_element_visible_but_not_visible_to_accessbility
(
self
)
:
        
self
.
setup_accessibility
(
)
        
self
.
run_element_test
(
self
.
displayed_but_have_no_accessible_elementIDs
                              
lambda
element
:
self
.
assertRaises
(
ElementNotAccessibleException
                                                                
element
.
is_displayed
)
)
    
def
test_element_is_visible_to_accessibility
(
self
)
:
        
self
.
setup_accessibility
(
)
        
self
.
run_element_test
(
self
.
displayed_elementIDs
lambda
element
:
element
.
is_displayed
(
)
)
    
def
test_element_is_not_enabled_to_accessbility
(
self
)
:
        
self
.
setup_accessibility
(
)
        
self
.
run_element_test
(
self
.
aria_disabled_elementIDs
                              
lambda
element
:
self
.
assertRaises
(
ElementNotAccessibleException
                                                                
element
.
is_enabled
)
)
        
self
.
run_element_test
(
self
.
pointer_events_none_elementIDs
                              
lambda
element
:
self
.
assertRaises
(
ElementNotAccessibleException
                                                                
element
.
is_enabled
)
)
        
self
.
run_element_test
(
self
.
aria_disabled_elementIDs
                              
lambda
element
:
self
.
assertRaises
(
ElementNotAccessibleException
                                                                
element
.
click
)
)
        
if
not
self
.
marionette
.
session_capabilities
[
"
moz
:
webdriverClick
"
]
:
            
self
.
run_element_test
(
self
.
pointer_events_none_elementIDs
                                  
lambda
element
:
self
.
assertRaises
(
ElementNotAccessibleException
                                                                    
element
.
click
)
)
        
self
.
setup_accessibility
(
False
False
)
        
self
.
run_element_test
(
self
.
aria_disabled_elementIDs
                              
lambda
element
:
element
.
is_enabled
(
)
)
        
self
.
run_element_test
(
self
.
pointer_events_none_elementIDs
                              
lambda
element
:
element
.
is_enabled
(
)
)
        
self
.
run_element_test
(
self
.
aria_disabled_elementIDs
                              
lambda
element
:
element
.
click
(
)
)
        
if
not
self
.
marionette
.
session_capabilities
[
"
moz
:
webdriverClick
"
]
:
            
self
.
run_element_test
(
self
.
pointer_events_none_elementIDs
                                  
lambda
element
:
element
.
click
(
)
)
    
def
test_element_is_enabled_to_accessibility
(
self
)
:
        
self
.
setup_accessibility
(
)
        
self
.
run_element_test
(
self
.
disabled_elementIDs
lambda
element
:
element
.
is_enabled
(
)
)
    
def
test_send_keys_raises_no_exception
(
self
)
:
        
self
.
setup_accessibility
(
)
        
self
.
run_element_test
(
[
'
input1
'
]
lambda
element
:
element
.
send_keys
(
"
a
"
)
)
    
def
test_is_selected_raises_no_exception
(
self
)
:
        
self
.
setup_accessibility
(
)
        
self
.
run_element_test
(
self
.
valid_option_elementIDs
lambda
element
:
element
.
is_selected
(
)
)
        
self
.
run_element_test
(
self
.
valid_elementIDs
lambda
element
:
element
.
is_selected
(
)
)
