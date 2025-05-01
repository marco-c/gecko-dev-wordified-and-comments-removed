from
__future__
import
absolute_import
import
re
from
sentry_sdk
.
_types
import
MYPY
from
sentry_sdk
.
hub
import
Hub
from
sentry_sdk
.
integrations
import
Integration
DidNotEnable
from
sentry_sdk
.
tracing_utils
import
record_sql_queries
try
:
    
from
sqlalchemy
.
engine
import
Engine
    
from
sqlalchemy
.
event
import
listen
    
from
sqlalchemy
import
__version__
as
SQLALCHEMY_VERSION
except
ImportError
:
    
raise
DidNotEnable
(
"
SQLAlchemy
not
installed
.
"
)
if
MYPY
:
    
from
typing
import
Any
    
from
typing
import
ContextManager
    
from
typing
import
Optional
    
from
sentry_sdk
.
tracing
import
Span
class
SqlalchemyIntegration
(
Integration
)
:
    
identifier
=
"
sqlalchemy
"
    
staticmethod
    
def
setup_once
(
)
:
        
try
:
            
version
=
tuple
(
                
map
(
int
re
.
split
(
"
b
|
rc
"
SQLALCHEMY_VERSION
)
[
0
]
.
split
(
"
.
"
)
)
            
)
        
except
(
TypeError
ValueError
)
:
            
raise
DidNotEnable
(
                
"
Unparsable
SQLAlchemy
version
:
{
}
"
.
format
(
SQLALCHEMY_VERSION
)
            
)
        
if
version
<
(
1
2
)
:
            
raise
DidNotEnable
(
"
SQLAlchemy
1
.
2
or
newer
required
.
"
)
        
listen
(
Engine
"
before_cursor_execute
"
_before_cursor_execute
)
        
listen
(
Engine
"
after_cursor_execute
"
_after_cursor_execute
)
        
listen
(
Engine
"
handle_error
"
_handle_error
)
def
_before_cursor_execute
(
    
conn
cursor
statement
parameters
context
executemany
*
args
)
:
    
hub
=
Hub
.
current
    
if
hub
.
get_integration
(
SqlalchemyIntegration
)
is
None
:
        
return
    
ctx_mgr
=
record_sql_queries
(
        
hub
        
cursor
        
statement
        
parameters
        
paramstyle
=
context
and
context
.
dialect
and
context
.
dialect
.
paramstyle
or
None
        
executemany
=
executemany
    
)
    
context
.
_sentry_sql_span_manager
=
ctx_mgr
    
span
=
ctx_mgr
.
__enter__
(
)
    
if
span
is
not
None
:
        
context
.
_sentry_sql_span
=
span
def
_after_cursor_execute
(
conn
cursor
statement
parameters
context
*
args
)
:
    
ctx_mgr
=
getattr
(
        
context
"
_sentry_sql_span_manager
"
None
    
)
    
if
ctx_mgr
is
not
None
:
        
context
.
_sentry_sql_span_manager
=
None
        
ctx_mgr
.
__exit__
(
None
None
None
)
def
_handle_error
(
context
*
args
)
:
    
execution_context
=
context
.
execution_context
    
if
execution_context
is
None
:
        
return
    
span
=
getattr
(
execution_context
"
_sentry_sql_span
"
None
)
    
if
span
is
not
None
:
        
span
.
set_status
(
"
internal_error
"
)
    
ctx_mgr
=
getattr
(
        
execution_context
"
_sentry_sql_span_manager
"
None
    
)
    
if
ctx_mgr
is
not
None
:
        
execution_context
.
_sentry_sql_span_manager
=
None
        
ctx_mgr
.
__exit__
(
None
None
None
)
