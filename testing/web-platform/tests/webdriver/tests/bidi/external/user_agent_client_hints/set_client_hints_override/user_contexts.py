import
pytest
from
.
import
ANOTHER_CLIENT_HINTS
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
test_user_contexts
(
bidi_session
create_user_context
new_tab
        
assert_client_hints
default_client_hints
)
:
    
user_context
=
await
create_user_context
(
)
    
context_in_user_context
=
await
bidi_session
.
browsing_context
.
create
(
        
user_context
=
user_context
type_hint
=
"
tab
"
)
    
await
assert_client_hints
(
new_tab
default_client_hints
)
    
await
bidi_session
.
user_agent_client_hints
.
set_client_hints_override
(
        
user_contexts
=
[
user_context
]
        
client_hints
=
SOME_CLIENT_HINTS
)
    
await
assert_client_hints
(
context_in_user_context
SOME_CLIENT_HINTS
)
    
await
assert_client_hints
(
new_tab
default_client_hints
)
    
another_context_in_user_context
=
await
bidi_session
.
browsing_context
.
create
(
        
user_context
=
user_context
type_hint
=
"
tab
"
)
    
await
assert_client_hints
(
        
another_context_in_user_context
SOME_CLIENT_HINTS
)
async
def
test_set_to_default_user_context
(
bidi_session
new_tab
        
create_user_context
        
assert_client_hints
        
default_client_hints
)
:
    
user_context
=
await
create_user_context
(
)
    
context_in_user_context
=
await
bidi_session
.
browsing_context
.
create
(
        
user_context
=
user_context
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
        
user_contexts
=
[
"
default
"
]
        
client_hints
=
SOME_CLIENT_HINTS
    
)
    
await
assert_client_hints
(
context_in_user_context
default_client_hints
)
    
await
assert_client_hints
(
new_tab
SOME_CLIENT_HINTS
)
    
context_in_default_context
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
assert_client_hints
(
context_in_default_context
SOME_CLIENT_HINTS
)
    
await
bidi_session
.
user_agent_client_hints
.
set_client_hints_override
(
        
user_contexts
=
[
"
default
"
]
        
client_hints
=
None
    
)
async
def
test_set_to_multiple_user_contexts
(
bidi_session
create_user_context
        
assert_client_hints
)
:
    
user_context_1
=
await
create_user_context
(
)
    
context_in_user_context_1
=
await
bidi_session
.
browsing_context
.
create
(
        
user_context
=
user_context_1
type_hint
=
"
tab
"
    
)
    
user_context_2
=
await
create_user_context
(
)
    
context_in_user_context_2
=
await
bidi_session
.
browsing_context
.
create
(
        
user_context
=
user_context_2
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
        
user_contexts
=
[
user_context_1
user_context_2
]
        
client_hints
=
SOME_CLIENT_HINTS
    
)
    
await
assert_client_hints
(
context_in_user_context_1
SOME_CLIENT_HINTS
)
    
await
assert_client_hints
(
context_in_user_context_2
SOME_CLIENT_HINTS
)
async
def
test_set_to_user_context_and_then_to_context
(
bidi_session
        
create_user_context
        
assert_client_hints
        
default_client_hints
)
:
    
user_context
=
await
create_user_context
(
)
    
context_in_user_context
=
await
bidi_session
.
browsing_context
.
create
(
        
user_context
=
user_context
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
        
user_contexts
=
[
user_context
]
        
client_hints
=
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
context_in_user_context
[
"
context
"
]
]
        
client_hints
=
ANOTHER_CLIENT_HINTS
    
)
    
await
assert_client_hints
(
context_in_user_context
ANOTHER_CLIENT_HINTS
)
    
await
bidi_session
.
browsing_context
.
reload
(
        
context
=
context_in_user_context
[
"
context
"
]
wait
=
"
complete
"
    
)
    
await
assert_client_hints
(
context_in_user_context
ANOTHER_CLIENT_HINTS
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
context_in_user_context
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
context_in_user_context
SOME_CLIENT_HINTS
)
    
await
bidi_session
.
browsing_context
.
reload
(
        
context
=
context_in_user_context
[
"
context
"
]
wait
=
"
complete
"
    
)
    
await
assert_client_hints
(
context_in_user_context
SOME_CLIENT_HINTS
)
    
await
bidi_session
.
user_agent_client_hints
.
set_client_hints_override
(
        
user_contexts
=
[
user_context
]
        
client_hints
=
None
    
)
    
await
assert_client_hints
(
context_in_user_context
default_client_hints
)
    
await
bidi_session
.
browsing_context
.
reload
(
        
context
=
context_in_user_context
[
"
context
"
]
wait
=
"
complete
"
    
)
    
await
assert_client_hints
(
context_in_user_context
default_client_hints
)
