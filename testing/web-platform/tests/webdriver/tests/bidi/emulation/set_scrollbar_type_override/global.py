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
    
affected_user_context
    
get_scrollbar_width
    
default_scrollbar_width
)
:
    
affected_context
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
user_context
=
affected_user_context
    
)
    
assert
(
        
await
get_scrollbar_width
(
affected_context
)
=
=
default_scrollbar_width
    
)
    
await
bidi_session
.
emulation
.
set_scrollbar_type_override
(
        
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
affected_context
)
=
=
0
    
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
user_context
=
affected_user_context
    
)
    
assert
await
get_scrollbar_width
(
another_context
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
        
scrollbar_type
=
None
    
)
    
assert
(
        
await
get_scrollbar_width
(
affected_context
)
=
=
default_scrollbar_width
    
)
    
assert
await
get_scrollbar_width
(
another_context
)
=
=
default_scrollbar_width
