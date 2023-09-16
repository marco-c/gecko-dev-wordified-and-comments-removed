from
marionette_driver
import
errors
Wait
from
marionette_harness
import
MarionetteTestCase
class
TestWindowless
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
TestWindowless
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
windowless
"
:
True
}
)
    
def
tearDown
(
self
)
:
        
self
.
marionette
.
restart
(
in_app
=
True
)
        
self
.
marionette
.
delete_session
(
)
        
super
(
TestWindowless
self
)
.
tearDown
(
)
    
def
wait_for_first_window
(
self
)
:
        
wait
=
Wait
(
            
self
.
marionette
            
ignored_exceptions
=
errors
.
NoSuchWindowException
            
timeout
=
5
        
)
        
return
wait
.
until
(
lambda
_
:
self
.
marionette
.
window_handles
)
    
def
test_last_chrome_window_can_be_closed
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
            
handles
=
self
.
marionette
.
chrome_window_handles
            
self
.
assertGreater
(
len
(
handles
)
0
)
            
self
.
marionette
.
switch_to_window
(
handles
[
0
]
)
            
self
.
marionette
.
close_chrome_window
(
)
            
self
.
assertEqual
(
len
(
self
.
marionette
.
chrome_window_handles
)
0
)
    
def
test_last_content_window_can_be_closed
(
self
)
:
        
handles
=
self
.
marionette
.
window_handles
        
self
.
assertGreater
(
len
(
handles
)
0
)
        
self
.
marionette
.
switch_to_window
(
handles
[
0
]
)
        
self
.
marionette
.
close
(
)
        
self
.
assertEqual
(
len
(
self
.
marionette
.
window_handles
)
0
)
    
def
test_no_window_handles_after_silent_restart
(
self
)
:
        
handles
=
self
.
marionette
.
window_handles
        
self
.
assertGreater
(
len
(
handles
)
0
)
        
self
.
marionette
.
restart
(
silent
=
True
)
        
with
self
.
assertRaises
(
errors
.
TimeoutException
)
:
            
self
.
wait_for_first_window
(
)
        
self
.
marionette
.
restart
(
in_app
=
True
)
        
handles
=
self
.
wait_for_first_window
(
)
        
self
.
assertGreater
(
len
(
handles
)
0
)
        
self
.
marionette
.
switch_to_window
(
handles
[
0
]
)
