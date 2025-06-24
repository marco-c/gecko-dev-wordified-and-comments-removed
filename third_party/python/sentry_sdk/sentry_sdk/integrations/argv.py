import
sys
import
sentry_sdk
from
sentry_sdk
.
integrations
import
Integration
from
sentry_sdk
.
scope
import
add_global_event_processor
from
typing
import
TYPE_CHECKING
if
TYPE_CHECKING
:
    
from
typing
import
Optional
    
from
sentry_sdk
.
_types
import
Event
Hint
class
ArgvIntegration
(
Integration
)
:
    
identifier
=
"
argv
"
    
staticmethod
    
def
setup_once
(
)
:
        
add_global_event_processor
        
def
processor
(
event
hint
)
:
            
if
sentry_sdk
.
get_client
(
)
.
get_integration
(
ArgvIntegration
)
is
not
None
:
                
extra
=
event
.
setdefault
(
"
extra
"
{
}
)
                
if
isinstance
(
extra
dict
)
:
                    
extra
[
"
sys
.
argv
"
]
=
sys
.
argv
            
return
event
