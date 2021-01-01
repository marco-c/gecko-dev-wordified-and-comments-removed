try
:
    
from
.
_version
import
version
as
__version__
except
ImportError
:
    
__version__
=
"
unknown
"
__all__
=
[
    
"
PluginManager
"
    
"
PluginValidationError
"
    
"
HookCallError
"
    
"
HookspecMarker
"
    
"
HookimplMarker
"
]
from
.
manager
import
PluginManager
PluginValidationError
from
.
callers
import
HookCallError
from
.
hooks
import
HookspecMarker
HookimplMarker
