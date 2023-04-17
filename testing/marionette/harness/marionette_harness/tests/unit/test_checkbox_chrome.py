from
__future__
import
absolute_import
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
TestSelectedChrome
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
TestSelectedChrome
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
        
new_window
=
self
.
open_chrome_window
(
            
"
chrome
:
/
/
remote
/
content
/
marionette
/
test
.
xhtml
"
        
)
        
self
.
marionette
.
switch_to_window
(
new_window
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
close_all_windows
(
)
        
finally
:
            
super
(
TestSelectedChrome
self
)
.
tearDown
(
)
    
def
test_selected
(
self
)
:
        
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
box
.
is_selected
(
)
)
        
self
.
assertFalse
(
            
self
.
marionette
.
execute_script
(
"
arguments
[
0
]
.
checked
=
true
;
"
[
box
]
)
        
)
        
self
.
assertTrue
(
box
.
is_selected
(
)
)
