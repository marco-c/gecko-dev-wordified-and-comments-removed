import
pytest
pytestmark
=
pytest
.
mark
.
asyncio
SOME_USER_AGENT
=
"
SOME_USER_AGENT
"
ANOTHER_USER_AGENT
=
"
ANOTHER_USER_AGENT
"
async
def
test_user_contexts
(
bidi_session
create_user_context
new_tab
        
assert_user_agent
default_user_agent
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
assert_user_agent
(
new_tab
default_user_agent
)
    
await
bidi_session
.
emulation
.
set_user_agent_override
(
        
user_contexts
=
[
user_context
]
        
user_agent
=
SOME_USER_AGENT
)
    
await
assert_user_agent
(
context_in_user_context
SOME_USER_AGENT
)
    
await
assert_user_agent
(
new_tab
default_user_agent
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
assert_user_agent
(
        
another_context_in_user_context
SOME_USER_AGENT
)
async
def
test_set_to_default_user_context
(
bidi_session
new_tab
        
create_user_context
assert_user_agent
default_user_agent
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
emulation
.
set_user_agent_override
(
        
user_contexts
=
[
"
default
"
]
        
user_agent
=
SOME_USER_AGENT
    
)
    
await
assert_user_agent
(
context_in_user_context
default_user_agent
)
    
await
assert_user_agent
(
new_tab
SOME_USER_AGENT
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
assert_user_agent
(
context_in_default_context
SOME_USER_AGENT
)
    
await
bidi_session
.
emulation
.
set_user_agent_override
(
        
user_contexts
=
[
"
default
"
]
        
user_agent
=
None
    
)
async
def
test_set_to_multiple_user_contexts
(
bidi_session
create_user_context
        
assert_user_agent
default_user_agent
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
emulation
.
set_user_agent_override
(
        
user_contexts
=
[
user_context_1
user_context_2
]
        
user_agent
=
SOME_USER_AGENT
    
)
    
await
assert_user_agent
(
context_in_user_context_1
SOME_USER_AGENT
)
    
await
assert_user_agent
(
context_in_user_context_2
SOME_USER_AGENT
)
async
def
test_set_to_user_context_and_then_to_context
(
bidi_session
        
create_user_context
new_tab
assert_user_agent
default_user_agent
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
emulation
.
set_user_agent_override
(
        
user_contexts
=
[
user_context
]
        
user_agent
=
SOME_USER_AGENT
    
)
    
await
bidi_session
.
emulation
.
set_user_agent_override
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
        
user_agent
=
ANOTHER_USER_AGENT
    
)
    
await
assert_user_agent
(
context_in_user_context
ANOTHER_USER_AGENT
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
assert_user_agent
(
context_in_user_context
ANOTHER_USER_AGENT
)
    
await
bidi_session
.
emulation
.
set_user_agent_override
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
        
user_agent
=
None
    
)
    
await
assert_user_agent
(
context_in_user_context
SOME_USER_AGENT
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
assert_user_agent
(
context_in_user_context
SOME_USER_AGENT
)
    
await
bidi_session
.
emulation
.
set_user_agent_override
(
        
user_contexts
=
[
user_context
]
        
user_agent
=
None
    
)
    
await
assert_user_agent
(
context_in_user_context
default_user_agent
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
assert_user_agent
(
context_in_user_context
default_user_agent
)
