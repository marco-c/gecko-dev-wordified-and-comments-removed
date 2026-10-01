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
test_viewport_meta
(
    
bidi_session
    
new_tab
    
is_viewport_meta_active
    
default_viewport_meta_state
)
:
    
await
bidi_session
.
emulation
.
set_viewport_meta_override
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
        
viewport_meta
=
True
    
)
    
assert
await
is_viewport_meta_active
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
set_viewport_meta_override
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
        
viewport_meta
=
None
    
)
    
assert
(
        
await
is_viewport_meta_active
(
new_tab
)
=
=
default_viewport_meta_state
    
)
