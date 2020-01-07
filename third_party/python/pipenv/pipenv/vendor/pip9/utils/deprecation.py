"
"
"
A
module
that
implements
tooling
to
enable
easy
warnings
about
deprecations
.
"
"
"
from
__future__
import
absolute_import
import
logging
import
warnings
class
PipDeprecationWarning
(
Warning
)
:
    
pass
class
Pending
(
object
)
:
    
pass
class
RemovedInPip10Warning
(
PipDeprecationWarning
)
:
    
pass
class
RemovedInPip11Warning
(
PipDeprecationWarning
Pending
)
:
    
pass
class
Python26DeprecationWarning
(
PipDeprecationWarning
)
:
    
pass
_warnings_showwarning
=
None
def
_showwarning
(
message
category
filename
lineno
file
=
None
line
=
None
)
:
    
if
file
is
not
None
:
        
if
_warnings_showwarning
is
not
None
:
            
_warnings_showwarning
(
                
message
category
filename
lineno
file
line
            
)
    
else
:
        
if
issubclass
(
category
PipDeprecationWarning
)
:
            
logger
=
logging
.
getLogger
(
"
pip
.
deprecations
"
)
            
log_message
=
"
DEPRECATION
:
%
s
"
%
message
            
if
issubclass
(
category
Pending
)
:
                
logger
.
warning
(
log_message
)
            
else
:
                
logger
.
error
(
log_message
)
        
else
:
            
_warnings_showwarning
(
                
message
category
filename
lineno
file
line
            
)
def
install_warning_logger
(
)
:
    
warnings
.
simplefilter
(
"
default
"
PipDeprecationWarning
append
=
True
)
    
global
_warnings_showwarning
    
if
_warnings_showwarning
is
None
:
        
_warnings_showwarning
=
warnings
.
showwarning
        
warnings
.
showwarning
=
_showwarning
