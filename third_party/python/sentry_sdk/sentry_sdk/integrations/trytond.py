import
sentry_sdk
.
hub
import
sentry_sdk
.
utils
import
sentry_sdk
.
integrations
import
sentry_sdk
.
integrations
.
wsgi
from
sentry_sdk
.
_types
import
TYPE_CHECKING
from
trytond
.
exceptions
import
TrytonException
from
trytond
.
wsgi
import
app
if
TYPE_CHECKING
:
    
from
typing
import
Any
class
TrytondWSGIIntegration
(
sentry_sdk
.
integrations
.
Integration
)
:
    
identifier
=
"
trytond_wsgi
"
    
def
__init__
(
self
)
:
        
pass
    
staticmethod
    
def
setup_once
(
)
:
        
app
.
wsgi_app
=
sentry_sdk
.
integrations
.
wsgi
.
SentryWsgiMiddleware
(
app
.
wsgi_app
)
        
def
error_handler
(
e
)
:
            
hub
=
sentry_sdk
.
hub
.
Hub
.
current
            
if
hub
.
get_integration
(
TrytondWSGIIntegration
)
is
None
:
                
return
            
elif
isinstance
(
e
TrytonException
)
:
                
return
            
else
:
                
client
=
hub
.
client
                
event
hint
=
sentry_sdk
.
utils
.
event_from_exception
(
                    
e
                    
client_options
=
client
.
options
                    
mechanism
=
{
"
type
"
:
"
trytond
"
"
handled
"
:
False
}
                
)
                
hub
.
capture_event
(
event
hint
=
hint
)
        
if
hasattr
(
app
"
error_handler
"
)
:
            
app
.
error_handler
            
def
_
(
app
request
e
)
:
                
error_handler
(
e
)
        
else
:
            
app
.
error_handlers
.
append
(
error_handler
)
