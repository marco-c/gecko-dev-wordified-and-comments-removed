try
:
    
import
unittest2
as
unittest
except
ImportError
:
    
import
unittest
from
pyasn1
import
debug
class
BaseTestCase
(
unittest
.
TestCase
)
:
    
def
setUp
(
self
)
:
        
debug
.
setLogger
(
debug
.
Debug
(
'
all
'
printer
=
lambda
*
x
:
None
)
)
    
def
tearDown
(
self
)
:
        
debug
.
setLogger
(
None
)
