import
devil_chromium
from
pylib
import
constants
from
pylib
.
base
import
environment
class
LocalMachineEnvironment
(
environment
.
Environment
)
:
  
def
__init__
(
self
_args
output_manager
_error_func
)
:
    
super
(
)
.
__init__
(
output_manager
)
    
devil_chromium
.
Initialize
(
        
output_directory
=
constants
.
GetOutDirectory
(
)
)
  
def
SetUp
(
self
)
:
    
pass
  
def
TearDown
(
self
)
:
    
pass
