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
test_enabled_set_override_and_reset
(
bidi_session
top_context
        
is_scripting_enabled
)
:
    
assert
await
is_scripting_enabled
(
top_context
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
        
enabled
=
False
        
contexts
=
[
top_context
[
"
context
"
]
]
    
)
    
assert
await
is_scripting_enabled
(
top_context
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
        
enabled
=
None
        
contexts
=
[
top_context
[
"
context
"
]
]
    
)
    
assert
await
is_scripting_enabled
(
top_context
)
is
True
