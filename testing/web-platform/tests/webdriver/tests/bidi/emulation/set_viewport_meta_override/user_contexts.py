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
    
affected_user_context
    
not_affected_user_context
    
is_viewport_meta_active
    
default_viewport_meta_state
)
:
    
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
affected_user_context
        
type_hint
=
"
tab
"
    
)
    
context_in_other_user_context
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
not_affected_user_context
        
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
set_viewport_meta_override
(
        
user_contexts
=
[
affected_user_context
]
        
viewport_meta
=
True
    
)
    
assert
await
is_viewport_meta_active
(
context_in_user_context
)
is
True
    
assert
(
        
await
is_viewport_meta_active
(
context_in_other_user_context
)
        
=
=
default_viewport_meta_state
    
)
    
another_context_in_user_context
=
(
        
await
bidi_session
.
browsing_context
.
create
(
            
user_context
=
affected_user_context
            
type_hint
=
"
tab
"
        
)
    
)
    
assert
(
        
await
is_viewport_meta_active
(
another_context_in_user_context
)
is
True
    
)
    
another_context_in_other_user_context
=
(
        
await
bidi_session
.
browsing_context
.
create
(
            
user_context
=
not_affected_user_context
            
type_hint
=
"
tab
"
        
)
    
)
    
assert
(
        
await
is_viewport_meta_active
(
another_context_in_other_user_context
)
        
=
=
default_viewport_meta_state
    
)
    
await
bidi_session
.
emulation
.
set_viewport_meta_override
(
        
user_contexts
=
[
affected_user_context
]
        
viewport_meta
=
None
    
)
    
assert
(
        
await
is_viewport_meta_active
(
context_in_user_context
)
        
=
=
default_viewport_meta_state
    
)
    
assert
(
        
await
is_viewport_meta_active
(
another_context_in_user_context
)
        
=
=
default_viewport_meta_state
    
)
    
assert
(
        
await
is_viewport_meta_active
(
context_in_other_user_context
)
        
=
=
default_viewport_meta_state
    
)
    
assert
(
        
await
is_viewport_meta_active
(
another_context_in_other_user_context
)
        
=
=
default_viewport_meta_state
    
)
async
def
test_overrides_global
(
    
bidi_session
    
affected_user_context
    
is_viewport_meta_active
    
default_viewport_meta_state
)
:
    
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
affected_user_context
        
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
set_viewport_meta_override
(
        
user_contexts
=
[
affected_user_context
]
        
viewport_meta
=
True
    
)
    
await
bidi_session
.
emulation
.
set_viewport_meta_override
(
        
viewport_meta
=
True
    
)
    
assert
await
is_viewport_meta_active
(
context_in_user_context
)
is
True
    
await
bidi_session
.
emulation
.
set_viewport_meta_override
(
        
user_contexts
=
[
affected_user_context
]
        
viewport_meta
=
None
    
)
    
assert
await
is_viewport_meta_active
(
context_in_user_context
)
is
True
    
await
bidi_session
.
emulation
.
set_viewport_meta_override
(
        
viewport_meta
=
None
    
)
    
assert
(
        
await
is_viewport_meta_active
(
context_in_user_context
)
        
=
=
default_viewport_meta_state
    
)
