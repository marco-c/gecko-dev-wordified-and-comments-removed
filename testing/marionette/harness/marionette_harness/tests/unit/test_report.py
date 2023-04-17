from
__future__
import
absolute_import
from
marionette_harness
import
(
    
expectedFailure
    
MarionetteTestCase
    
skip
    
unexpectedSuccess
)
class
TestReport
(
MarionetteTestCase
)
:
    
def
test_pass
(
self
)
:
        
assert
True
    
skip
(
"
Skip
Message
"
)
    
def
test_skip
(
self
)
:
        
assert
False
    
expectedFailure
    
def
test_error
(
self
)
:
        
raise
Exception
(
)
    
unexpectedSuccess
    
def
test_unexpected_pass
(
self
)
:
        
assert
True
