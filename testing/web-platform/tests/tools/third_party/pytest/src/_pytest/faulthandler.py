import
io
import
os
import
sys
from
typing
import
Generator
from
typing
import
TextIO
import
pytest
from
_pytest
.
config
import
Config
from
_pytest
.
config
.
argparsing
import
Parser
from
_pytest
.
nodes
import
Item
from
_pytest
.
store
import
StoreKey
fault_handler_stderr_key
=
StoreKey
[
TextIO
]
(
)
def
pytest_addoption
(
parser
:
Parser
)
-
>
None
:
    
help
=
(
        
"
Dump
the
traceback
of
all
threads
if
a
test
takes
"
        
"
more
than
TIMEOUT
seconds
to
finish
.
"
    
)
    
parser
.
addini
(
"
faulthandler_timeout
"
help
default
=
0
.
0
)
def
pytest_configure
(
config
:
Config
)
-
>
None
:
    
import
faulthandler
    
if
not
faulthandler
.
is_enabled
(
)
:
        
config
.
pluginmanager
.
register
(
FaultHandlerHooks
(
)
"
faulthandler
-
hooks
"
)
    
else
:
        
timeout
=
FaultHandlerHooks
.
get_timeout_config_value
(
config
)
        
if
timeout
>
0
:
            
config
.
issue_config_time_warning
(
                
pytest
.
PytestConfigWarning
(
                    
"
faulthandler
module
enabled
before
pytest
configuration
step
"
                    
"
'
faulthandler_timeout
'
option
ignored
"
                
)
                
stacklevel
=
2
            
)
class
FaultHandlerHooks
:
    
"
"
"
Implements
hooks
that
will
actually
install
fault
handler
before
tests
execute
    
as
well
as
correctly
handle
pdb
and
internal
errors
.
"
"
"
    
def
pytest_configure
(
self
config
:
Config
)
-
>
None
:
        
import
faulthandler
        
stderr_fd_copy
=
os
.
dup
(
self
.
_get_stderr_fileno
(
)
)
        
config
.
_store
[
fault_handler_stderr_key
]
=
open
(
stderr_fd_copy
"
w
"
)
        
faulthandler
.
enable
(
file
=
config
.
_store
[
fault_handler_stderr_key
]
)
    
def
pytest_unconfigure
(
self
config
:
Config
)
-
>
None
:
        
import
faulthandler
        
faulthandler
.
disable
(
)
        
config
.
_store
[
fault_handler_stderr_key
]
.
close
(
)
        
del
config
.
_store
[
fault_handler_stderr_key
]
        
faulthandler
.
enable
(
file
=
self
.
_get_stderr_fileno
(
)
)
    
staticmethod
    
def
_get_stderr_fileno
(
)
:
        
try
:
            
return
sys
.
stderr
.
fileno
(
)
        
except
(
AttributeError
io
.
UnsupportedOperation
)
:
            
return
sys
.
__stderr__
.
fileno
(
)
    
staticmethod
    
def
get_timeout_config_value
(
config
)
:
        
return
float
(
config
.
getini
(
"
faulthandler_timeout
"
)
or
0
.
0
)
    
pytest
.
hookimpl
(
hookwrapper
=
True
trylast
=
True
)
    
def
pytest_runtest_protocol
(
self
item
:
Item
)
-
>
Generator
[
None
None
None
]
:
        
timeout
=
self
.
get_timeout_config_value
(
item
.
config
)
        
stderr
=
item
.
config
.
_store
[
fault_handler_stderr_key
]
        
if
timeout
>
0
and
stderr
is
not
None
:
            
import
faulthandler
            
faulthandler
.
dump_traceback_later
(
timeout
file
=
stderr
)
            
try
:
                
yield
            
finally
:
                
faulthandler
.
cancel_dump_traceback_later
(
)
        
else
:
            
yield
    
pytest
.
hookimpl
(
tryfirst
=
True
)
    
def
pytest_enter_pdb
(
self
)
-
>
None
:
        
"
"
"
Cancel
any
traceback
dumping
due
to
timeout
before
entering
pdb
.
"
"
"
        
import
faulthandler
        
faulthandler
.
cancel_dump_traceback_later
(
)
    
pytest
.
hookimpl
(
tryfirst
=
True
)
    
def
pytest_exception_interact
(
self
)
-
>
None
:
        
"
"
"
Cancel
any
traceback
dumping
due
to
an
interactive
exception
being
        
raised
.
"
"
"
        
import
faulthandler
        
faulthandler
.
cancel_dump_traceback_later
(
)
