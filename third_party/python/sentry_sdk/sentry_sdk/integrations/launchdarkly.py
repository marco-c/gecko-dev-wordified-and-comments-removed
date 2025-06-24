from
typing
import
TYPE_CHECKING
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
DidNotEnable
Integration
try
:
    
import
ldclient
    
from
ldclient
.
hook
import
Hook
Metadata
    
if
TYPE_CHECKING
:
        
from
ldclient
import
LDClient
        
from
ldclient
.
hook
import
EvaluationSeriesContext
        
from
ldclient
.
evaluation
import
EvaluationDetail
        
from
typing
import
Any
except
ImportError
:
    
raise
DidNotEnable
(
"
LaunchDarkly
is
not
installed
"
)
class
LaunchDarklyIntegration
(
Integration
)
:
    
identifier
=
"
launchdarkly
"
    
def
__init__
(
self
ld_client
=
None
)
:
        
"
"
"
        
:
param
client
:
An
initialized
LDClient
instance
.
If
a
client
is
not
provided
this
            
integration
will
attempt
to
use
the
shared
global
instance
.
        
"
"
"
        
try
:
            
client
=
ld_client
or
ldclient
.
get
(
)
        
except
Exception
as
exc
:
            
raise
DidNotEnable
(
"
Error
getting
LaunchDarkly
client
.
"
+
repr
(
exc
)
)
        
if
not
client
.
is_initialized
(
)
:
            
raise
DidNotEnable
(
"
LaunchDarkly
client
is
not
initialized
.
"
)
        
client
.
add_hook
(
LaunchDarklyHook
(
)
)
    
staticmethod
    
def
setup_once
(
)
:
        
pass
class
LaunchDarklyHook
(
Hook
)
:
    
property
    
def
metadata
(
self
)
:
        
return
Metadata
(
name
=
"
sentry
-
flag
-
auditor
"
)
    
def
after_evaluation
(
self
series_context
data
detail
)
:
        
if
isinstance
(
detail
.
value
bool
)
:
            
add_feature_flag
(
series_context
.
key
detail
.
value
)
        
return
data
    
def
before_evaluation
(
self
series_context
data
)
:
        
return
data
