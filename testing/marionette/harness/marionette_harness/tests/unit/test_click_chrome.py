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
WindowManagerMixin
class
TestClickChrome
(
WindowManagerMixin
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
TestClickChrome
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
TestClickChrome
self
)
.
tearDown
(
)
    
def
test_click
(
self
)
:
        
def
open_with_js
(
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
              
window
.
open
(
'
chrome
:
/
/
marionette
/
content
/
test
.
xul
'
                          
'
foo
'
'
chrome
centerscreen
'
)
;
"
"
"
)
        
win
=
self
.
open_window
(
open_with_js
)
        
self
.
marionette
.
switch_to_window
(
win
)
        
def
checked
(
)
:
            
return
self
.
marionette
.
execute_script
(
                
"
return
arguments
[
0
]
.
checked
"
                
script_args
=
[
box
]
)
        
box
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
"
testBox
"
)
        
self
.
assertFalse
(
checked
(
)
)
        
box
.
click
(
)
        
self
.
assertTrue
(
checked
(
)
)
