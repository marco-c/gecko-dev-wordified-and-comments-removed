import
pytest
from
bidi
.
support
.
container_isolation
import
container_isolation
from
webdriver
.
bidi
.
error
import
NoSuchUserContextException
pytestmark
=
[
pytest
.
mark
.
asyncio
container_isolation
]
async
def
test_user_contexts
(
bidi_session
session_user_context
)
:
    
collector
=
await
bidi_session
.
network
.
add_data_collector
(
        
data_types
=
[
"
response
"
]
        
max_encoded_data_size
=
1000
        
user_contexts
=
[
session_user_context
]
    
)
    
await
bidi_session
.
network
.
remove_data_collector
(
collector
=
collector
)
async
def
test_user_contexts_outside_container
(
bidi_session
)
:
    
with
pytest
.
raises
(
NoSuchUserContextException
)
:
        
await
bidi_session
.
network
.
add_data_collector
(
            
data_types
=
[
"
response
"
]
            
max_encoded_data_size
=
1000
            
user_contexts
=
[
"
default
"
]
        
)
