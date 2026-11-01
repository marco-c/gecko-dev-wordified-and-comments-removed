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
test_global
(
    
bidi_session
    
top_context
    
is_text_autosizing_enabled
    
default_text_autosizing_state
)
:
    
await
bidi_session
.
emulation
.
set_text_layout_mode_override
(
        
text_layout_mode
=
"
mobile
"
    
)
    
assert
await
is_text_autosizing_enabled
(
top_context
)
is
True
    
another_context
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
is_text_autosizing_enabled
(
another_context
)
is
True
    
await
bidi_session
.
emulation
.
set_text_layout_mode_override
(
        
text_layout_mode
=
None
    
)
    
assert
(
        
await
is_text_autosizing_enabled
(
top_context
)
        
=
=
default_text_autosizing_state
    
)
    
assert
(
        
await
is_text_autosizing_enabled
(
another_context
)
        
=
=
default_text_autosizing_state
    
)
