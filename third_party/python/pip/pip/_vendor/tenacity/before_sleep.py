import
typing
from
pip
.
_vendor
.
tenacity
import
_utils
if
typing
.
TYPE_CHECKING
:
    
import
logging
    
from
pip
.
_vendor
.
tenacity
import
RetryCallState
def
before_sleep_nothing
(
retry_state
:
"
RetryCallState
"
)
-
>
None
:
    
"
"
"
Before
call
strategy
that
does
nothing
.
"
"
"
def
before_sleep_log
(
    
logger
:
"
logging
.
Logger
"
    
log_level
:
int
    
exc_info
:
bool
=
False
)
-
>
typing
.
Callable
[
[
"
RetryCallState
"
]
None
]
:
    
"
"
"
Before
call
strategy
that
logs
to
some
logger
the
attempt
.
"
"
"
    
def
log_it
(
retry_state
:
"
RetryCallState
"
)
-
>
None
:
        
if
retry_state
.
outcome
.
failed
:
            
ex
=
retry_state
.
outcome
.
exception
(
)
            
verb
value
=
"
raised
"
f
"
{
ex
.
__class__
.
__name__
}
:
{
ex
}
"
            
if
exc_info
:
                
local_exc_info
=
retry_state
.
outcome
.
exception
(
)
            
else
:
                
local_exc_info
=
False
        
else
:
            
verb
value
=
"
returned
"
retry_state
.
outcome
.
result
(
)
            
local_exc_info
=
False
        
logger
.
log
(
            
log_level
            
f
"
Retrying
{
_utils
.
get_callback_name
(
retry_state
.
fn
)
}
"
            
f
"
in
{
retry_state
.
next_action
.
sleep
}
seconds
as
it
{
verb
}
{
value
}
.
"
            
exc_info
=
local_exc_info
        
)
    
return
log_it
