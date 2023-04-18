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
_manager
import
PluginManager
PluginValidationError
from
.
_callers
import
HookCallError
from
.
_hooks
import
HookspecMarker
HookimplMarker
