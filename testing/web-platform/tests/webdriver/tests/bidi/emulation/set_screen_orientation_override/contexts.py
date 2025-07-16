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
test_contexts
(
        
bidi_session
new_tab
top_context
get_screen_orientation
        
some_bidi_screen_orientation
some_web_screen_orientation
        
default_screen_orientation
)
:
    
await
bidi_session
.
emulation
.
set_screen_orientation_override
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
        
screen_orientation
=
some_bidi_screen_orientation
    
)
    
assert
await
get_screen_orientation
(
        
new_tab
)
=
=
some_web_screen_orientation
    
assert
await
get_screen_orientation
(
        
top_context
)
=
=
default_screen_orientation
    
await
bidi_session
.
emulation
.
set_screen_orientation_override
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
screen_orientation
=
None
    
)
    
assert
await
get_screen_orientation
(
new_tab
)
=
=
default_screen_orientation
    
assert
await
get_screen_orientation
(
        
top_context
)
=
=
default_screen_orientation
async
def
test_multiple_contexts
(
        
bidi_session
new_tab
top_context
get_screen_orientation
        
some_bidi_screen_orientation
some_web_screen_orientation
        
default_screen_orientation
)
:
    
await
bidi_session
.
emulation
.
set_screen_orientation_override
(
        
contexts
=
[
top_context
[
"
context
"
]
new_tab
[
"
context
"
]
]
        
screen_orientation
=
some_bidi_screen_orientation
    
)
    
assert
await
get_screen_orientation
(
new_tab
)
=
=
some_web_screen_orientation
    
assert
await
get_screen_orientation
(
        
top_context
)
=
=
some_web_screen_orientation
    
await
bidi_session
.
emulation
.
set_screen_orientation_override
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
        
screen_orientation
=
None
    
)
    
assert
await
get_screen_orientation
(
new_tab
)
=
=
default_screen_orientation
    
assert
await
get_screen_orientation
(
top_context
)
=
=
some_web_screen_orientation
    
await
bidi_session
.
emulation
.
set_screen_orientation_override
(
        
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
        
screen_orientation
=
None
    
)
    
assert
await
get_screen_orientation
(
new_tab
)
=
=
default_screen_orientation
    
assert
await
get_screen_orientation
(
        
top_context
)
=
=
default_screen_orientation
