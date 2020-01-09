import
unittest
from
.
import
filtration_test
def
load_tests
(
loader
tests
pattern
)
:
    
suite
=
unittest
.
TestSuite
(
)
    
suite
.
addTest
(
filtration_test
.
suite
)
    
return
suite
if
__name__
=
=
'
__main__
'
:
    
unittest
.
main
(
)
