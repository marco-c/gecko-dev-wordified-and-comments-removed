from
marionette_harness
import
MarionetteTestCase
WindowManagerMixin
class
TestPageSourceChrome
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
TestPageSourceChrome
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
        
new_window
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
new_window
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
TestPageSourceChrome
self
)
.
tearDown
(
)
    
def
testShouldReturnXULDetails
(
self
)
:
        
source
=
self
.
marionette
.
page_source
        
self
.
assertTrue
(
'
<
textbox
id
=
"
textInput
"
'
in
source
)
