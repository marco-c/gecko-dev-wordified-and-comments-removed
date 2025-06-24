from
__future__
import
absolute_import
from
sentry_sdk
.
_compat
import
text_type
from
sentry_sdk
.
_types
import
TYPE_CHECKING
from
sentry_sdk
.
consts
import
SPANDATA
from
sentry_sdk
.
db
.
explain_plan
.
sqlalchemy
import
attach_explain_plan_to_span
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
add_query_source
record_sql_queries
from
sentry_sdk
.
utils
import
capture_internal_exceptions
parse_version
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
TYPE_CHECKING
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
        
version
=
parse_version
(
SQLALCHEMY_VERSION
)
        
if
version
is
None
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
        
_set_db_data
(
span
conn
)
        
if
hub
.
client
:
            
options
=
hub
.
client
.
options
[
"
_experiments
"
]
.
get
(
"
attach_explain_plans
"
)
            
if
options
is
not
None
:
                
attach_explain_plan_to_span
(
                    
span
                    
conn
                    
statement
                    
parameters
                    
options
                
)
        
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
    
span
=
getattr
(
context
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
        
with
capture_internal_exceptions
(
)
:
            
add_query_source
(
hub
span
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
def
_get_db_system
(
name
)
:
    
name
=
text_type
(
name
)
    
if
"
sqlite
"
in
name
:
        
return
"
sqlite
"
    
if
"
postgres
"
in
name
:
        
return
"
postgresql
"
    
if
"
mariadb
"
in
name
:
        
return
"
mariadb
"
    
if
"
mysql
"
in
name
:
        
return
"
mysql
"
    
if
"
oracle
"
in
name
:
        
return
"
oracle
"
    
return
None
def
_set_db_data
(
span
conn
)
:
    
db_system
=
_get_db_system
(
conn
.
engine
.
name
)
    
if
db_system
is
not
None
:
        
span
.
set_data
(
SPANDATA
.
DB_SYSTEM
db_system
)
    
if
conn
.
engine
.
url
is
None
:
        
return
    
db_name
=
conn
.
engine
.
url
.
database
    
if
db_name
is
not
None
:
        
span
.
set_data
(
SPANDATA
.
DB_NAME
db_name
)
    
server_address
=
conn
.
engine
.
url
.
host
    
if
server_address
is
not
None
:
        
span
.
set_data
(
SPANDATA
.
SERVER_ADDRESS
server_address
)
    
server_port
=
conn
.
engine
.
url
.
port
    
if
server_port
is
not
None
:
        
span
.
set_data
(
SPANDATA
.
SERVER_PORT
server_port
)
