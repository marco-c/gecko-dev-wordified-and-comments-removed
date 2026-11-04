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
test_scrollbar_type_overlay
(
    
bidi_session
new_tab
get_scrollbar_width
default_scrollbar_width
)
:
    
assert
await
get_scrollbar_width
(
new_tab
)
=
=
default_scrollbar_width
    
await
bidi_session
.
emulation
.
set_scrollbar_type_override
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
        
scrollbar_type
=
"
overlay
"
    
)
    
assert
await
get_scrollbar_width
(
new_tab
)
=
=
0
    
await
bidi_session
.
emulation
.
set_scrollbar_type_override
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
        
scrollbar_type
=
None
    
)
    
assert
await
get_scrollbar_width
(
new_tab
)
=
=
default_scrollbar_width
async
def
test_scrollbar_type_classic
(
    
bidi_session
new_tab
get_scrollbar_width
default_scrollbar_width
)
:
    
await
bidi_session
.
emulation
.
set_scrollbar_type_override
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
        
scrollbar_type
=
"
classic
"
    
)
    
assert
await
get_scrollbar_width
(
new_tab
)
>
0
    
await
bidi_session
.
emulation
.
set_scrollbar_type_override
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
        
scrollbar_type
=
None
    
)
    
assert
await
get_scrollbar_width
(
new_tab
)
=
=
default_scrollbar_width
