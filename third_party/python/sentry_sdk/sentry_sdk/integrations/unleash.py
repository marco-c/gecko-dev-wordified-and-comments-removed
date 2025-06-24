from
functools
import
wraps
from
typing
import
Any
from
sentry_sdk
.
feature_flags
import
add_feature_flag
from
sentry_sdk
.
integrations
import
Integration
DidNotEnable
try
:
    
from
UnleashClient
import
UnleashClient
except
ImportError
:
    
raise
DidNotEnable
(
"
UnleashClient
is
not
installed
"
)
class
UnleashIntegration
(
Integration
)
:
    
identifier
=
"
unleash
"
    
staticmethod
    
def
setup_once
(
)
:
        
old_is_enabled
=
UnleashClient
.
is_enabled
        
wraps
(
old_is_enabled
)
        
def
sentry_is_enabled
(
self
feature
*
args
*
*
kwargs
)
:
            
enabled
=
old_is_enabled
(
self
feature
*
args
*
*
kwargs
)
            
add_feature_flag
(
feature
enabled
)
            
return
enabled
        
UnleashClient
.
is_enabled
=
sentry_is_enabled
