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
test_text_layout_mode
(
    
bidi_session
    
new_tab
    
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
new_tab
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
        
text_layout_mode
=
None
    
)
    
assert
(
        
await
is_text_autosizing_enabled
(
new_tab
)
        
=
=
default_text_autosizing_state
    
)
