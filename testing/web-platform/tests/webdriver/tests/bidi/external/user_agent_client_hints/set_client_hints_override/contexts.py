import
pytest
from
.
import
SOME_CLIENT_HINTS
pytestmark
=
pytest
.
mark
.
asyncio
async
def
test_contexts
(
bidi_session
new_tab
top_context
        
default_client_hints
assert_client_hints
)
:
    
await
bidi_session
.
user_agent_client_hints
.
set_client_hints_override
(
        
contexts
=
[
new_tab
[
"
context
"
]
]
        
client_hints
=
SOME_CLIENT_HINTS
    
)
    
await
assert_client_hints
(
new_tab
SOME_CLIENT_HINTS
)
    
await
assert_client_hints
(
top_context
default_client_hints
)
    
await
bidi_session
.
user_agent_client_hints
.
set_client_hints_override
(
        
contexts
=
[
new_tab
[
"
context
"
]
]
        
client_hints
=
None
    
)
    
await
assert_client_hints
(
new_tab
default_client_hints
)
    
await
assert_client_hints
(
top_context
default_client_hints
)
async
def
test_multiple_contexts
(
bidi_session
new_tab
default_client_hints
        
assert_client_hints
)
:
    
new_context
=
await
bidi_session
.
browsing_context
.
create
(
type_hint
=
"
tab
"
)
    
await
bidi_session
.
user_agent_client_hints
.
set_client_hints_override
(
        
contexts
=
[
new_tab
[
"
context
"
]
new_context
[
"
context
"
]
]
        
client_hints
=
SOME_CLIENT_HINTS
    
)
    
await
assert_client_hints
(
new_tab
SOME_CLIENT_HINTS
)
    
await
assert_client_hints
(
new_context
SOME_CLIENT_HINTS
)
    
await
bidi_session
.
user_agent_client_hints
.
set_client_hints_override
(
        
contexts
=
[
new_tab
[
"
context
"
]
new_context
[
"
context
"
]
]
        
client_hints
=
None
    
)
    
await
assert_client_hints
(
new_tab
default_client_hints
)
    
await
assert_client_hints
(
new_context
default_client_hints
)
