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
    
not_affected_context
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
not_affected_user_context
    
)
    
assert
await
get_scrollbar_width
(
affected_context
)
=
=
default_scrollbar_width
    
assert
await
get_scrollbar_width
(
not_affected_context
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
        
user_contexts
=
[
affected_user_context
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
affected_context
)
=
=
0
    
assert
await
get_scrollbar_width
(
not_affected_context
)
=
=
default_scrollbar_width
    
another_affected_context
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
    
another_not_affected_context
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
not_affected_user_context
    
)
    
assert
await
get_scrollbar_width
(
another_affected_context
)
=
=
0
    
assert
(
        
await
get_scrollbar_width
(
another_not_affected_context
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
        
user_contexts
=
[
affected_user_context
]
        
scrollbar_type
=
None
    
)
    
assert
await
get_scrollbar_width
(
affected_context
)
=
=
default_scrollbar_width
    
assert
await
get_scrollbar_width
(
not_affected_context
)
=
=
default_scrollbar_width
    
assert
(
        
await
get_scrollbar_width
(
another_affected_context
)
        
=
=
default_scrollbar_width
    
)
    
assert
(
        
await
get_scrollbar_width
(
another_not_affected_context
)
        
=
=
default_scrollbar_width
    
)
async
def
test_multiple_user_contexts
(
    
bidi_session
    
create_user_context
    
get_scrollbar_width
    
default_scrollbar_width
)
:
    
user_context_1
=
await
create_user_context
(
)
    
user_context_2
=
await
create_user_context
(
)
    
context_1
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
user_context_1
    
)
    
context_2
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
user_context_2
    
)
    
await
bidi_session
.
emulation
.
set_scrollbar_type_override
(
        
user_contexts
=
[
user_context_1
user_context_2
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
context_1
)
=
=
0
    
assert
await
get_scrollbar_width
(
context_2
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
        
user_contexts
=
[
user_context_1
user_context_2
]
        
scrollbar_type
=
None
    
)
    
assert
await
get_scrollbar_width
(
context_1
)
=
=
default_scrollbar_width
    
assert
await
get_scrollbar_width
(
context_2
)
=
=
default_scrollbar_width
async
def
test_overrides_global
(
    
bidi_session
    
affected_user_context
    
get_scrollbar_width
    
default_scrollbar_width
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
        
type_hint
=
"
tab
"
user_context
=
affected_user_context
    
)
    
await
bidi_session
.
emulation
.
set_scrollbar_type_override
(
        
user_contexts
=
[
affected_user_context
]
        
scrollbar_type
=
"
classic
"
    
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
context_in_user_context
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
        
user_contexts
=
[
affected_user_context
]
        
scrollbar_type
=
None
    
)
    
assert
await
get_scrollbar_width
(
context_in_user_context
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
context_in_user_context
)
        
=
=
default_scrollbar_width
    
)
