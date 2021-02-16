from
__future__
import
absolute_import
__version__
=
"
3
.
1
.
0
"
from
unittest
.
case
import
(
    
expectedFailure
    
skip
    
SkipTest
)
from
.
decorators
import
(
    
parameterized
    
run_if_manage_instance
    
skip_if_chrome
    
skip_if_desktop
    
skip_if_framescript
    
skip_unless_browser_pref
    
skip_unless_protocol
    
with_parameters
)
from
.
testcases
import
(
    
CommonTestCase
    
MarionetteTestCase
    
MetaParameterized
)
