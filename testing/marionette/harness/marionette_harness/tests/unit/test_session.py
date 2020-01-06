from
marionette_driver
import
errors
from
marionette_harness
import
MarionetteTestCase
class
TestSession
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
TestSession
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
    
def
test_new_session_returns_capabilities
(
self
)
:
        
caps
=
self
.
marionette
.
start_session
(
)
        
self
.
assertIsNotNone
(
self
.
marionette
.
session
)
        
self
.
assertIn
(
"
browserName
"
caps
)
        
self
.
assertIn
(
"
browserVersion
"
caps
)
        
self
.
assertIn
(
"
platformName
"
caps
)
        
self
.
assertIn
(
"
platformVersion
"
caps
)
        
self
.
assertIn
(
"
rotatable
"
caps
)
    
def
test_get_session_id
(
self
)
:
        
self
.
marionette
.
start_session
(
)
        
self
.
assertTrue
(
self
.
marionette
.
session_id
is
not
None
)
        
self
.
assertTrue
(
isinstance
(
self
.
marionette
.
session_id
unicode
)
)
    
def
test_session_already_started
(
self
)
:
        
self
.
marionette
.
start_session
(
)
        
self
.
assertTrue
(
isinstance
(
self
.
marionette
.
session_id
unicode
)
)
        
with
self
.
assertRaises
(
errors
.
SessionNotCreatedException
)
:
            
self
.
marionette
.
_send_message
(
"
newSession
"
{
}
)
    
def
test_no_session
(
self
)
:
        
with
self
.
assertRaises
(
errors
.
InvalidSessionIdException
)
:
            
self
.
marionette
.
get_url
(
)
        
self
.
marionette
.
start_session
(
)
        
self
.
marionette
.
get_url
(
)
