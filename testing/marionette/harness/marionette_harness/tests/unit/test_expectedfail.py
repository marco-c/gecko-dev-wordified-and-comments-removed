from
marionette_harness
import
MarionetteTestCase
class
TestFail
(
MarionetteTestCase
)
:
    
def
test_fails
(
self
)
:
        
self
.
assertEqual
(
True
False
)
