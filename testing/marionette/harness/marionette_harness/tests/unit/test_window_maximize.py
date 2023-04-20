from
marionette_harness
import
MarionetteTestCase
class
TestWindowMaximize
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
max
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
            
return
{
              
width
:
window
.
screen
.
availWidth
              
height
:
window
.
screen
.
availHeight
            
}
"
"
"
            
sandbox
=
None
        
)
        
self
.
marionette
.
set_window_rect
(
            
width
=
self
.
max
[
"
width
"
]
-
100
height
=
self
.
max
[
"
height
"
]
-
100
        
)
        
actual
=
self
.
marionette
.
window_rect
        
self
.
assertNotEqual
(
actual
[
"
width
"
]
self
.
max
[
"
width
"
]
)
        
self
.
assertNotEqual
(
actual
[
"
height
"
]
self
.
max
[
"
height
"
]
)
        
self
.
original_size
=
actual
    
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
set_window_rect
(
            
width
=
self
.
original_size
[
"
width
"
]
height
=
self
.
original_size
[
"
height
"
]
        
)
    
def
test_maximize
(
self
)
:
        
self
.
marionette
.
maximize_window
(
)
