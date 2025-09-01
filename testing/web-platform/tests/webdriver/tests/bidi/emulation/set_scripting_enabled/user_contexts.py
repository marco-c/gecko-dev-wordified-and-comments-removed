import
pytest
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
        
is_scripting_enabled
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
    
assert
await
is_scripting_enabled
(
new_tab
)
is
True
    
await
bidi_session
.
emulation
.
set_scripting_enabled
(
        
user_contexts
=
[
user_context
]
        
enabled
=
False
)
    
assert
await
is_scripting_enabled
(
context_in_user_context
)
is
False
    
assert
await
is_scripting_enabled
(
new_tab
)
is
True
    
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
    
assert
await
is_scripting_enabled
(
        
another_context_in_user_context
)
is
False
async
def
test_set_to_default_user_context
(
        
bidi_session
        
new_tab
        
create_user_context
        
is_scripting_enabled
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
set_scripting_enabled
(
        
user_contexts
=
[
"
default
"
]
        
enabled
=
False
    
)
    
assert
await
is_scripting_enabled
(
context_in_user_context
)
is
True
    
assert
await
is_scripting_enabled
(
new_tab
)
is
False
    
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
    
assert
await
is_scripting_enabled
(
context_in_default_context
)
is
False
    
await
bidi_session
.
emulation
.
set_scripting_enabled
(
        
user_contexts
=
[
"
default
"
]
        
enabled
=
None
    
)
async
def
test_set_to_multiple_user_contexts
(
        
bidi_session
        
create_user_context
        
is_scripting_enabled
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
set_scripting_enabled
(
        
user_contexts
=
[
user_context_1
user_context_2
]
        
enabled
=
False
    
)
    
assert
await
is_scripting_enabled
(
context_in_user_context_1
)
is
False
    
assert
await
is_scripting_enabled
(
context_in_user_context_2
)
is
False
async
def
test_set_to_user_context_and_then_to_context
(
        
bidi_session
        
create_user_context
        
new_tab
        
is_scripting_enabled
)
:
    
user_context
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
set_scripting_enabled
(
        
user_contexts
=
[
user_context
]
        
enabled
=
False
    
)
    
await
bidi_session
.
emulation
.
set_scripting_enabled
(
        
contexts
=
[
context_in_user_context_1
[
"
context
"
]
]
        
enabled
=
None
    
)
    
assert
await
is_scripting_enabled
(
context_in_user_context_1
)
is
True
    
await
bidi_session
.
browsing_context
.
reload
(
        
context
=
context_in_user_context_1
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
    
assert
await
is_scripting_enabled
(
context_in_user_context_1
)
is
True
    
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
user_context
type_hint
=
"
tab
"
    
)
    
assert
await
is_scripting_enabled
(
context_in_user_context_2
)
is
False
    
await
bidi_session
.
emulation
.
set_scripting_enabled
(
        
contexts
=
[
context_in_user_context_1
[
"
context
"
]
]
        
enabled
=
None
    
)
    
assert
await
is_scripting_enabled
(
context_in_user_context_1
)
is
True
