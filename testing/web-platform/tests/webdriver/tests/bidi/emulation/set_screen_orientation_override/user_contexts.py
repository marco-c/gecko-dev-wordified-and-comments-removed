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
        
get_screen_orientation
some_bidi_screen_orientation
        
some_web_screen_orientation
default_screen_orientation
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
    
assert
await
get_screen_orientation
(
new_tab
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
        
user_contexts
=
[
user_context
]
        
screen_orientation
=
some_bidi_screen_orientation
    
)
    
assert
await
get_screen_orientation
(
        
context_in_user_context_1
)
=
=
some_web_screen_orientation
    
assert
await
get_screen_orientation
(
new_tab
)
=
=
default_screen_orientation
    
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
get_screen_orientation
(
        
context_in_user_context_2
)
=
=
some_web_screen_orientation
async
def
test_set_to_default_user_context
(
bidi_session
new_tab
        
create_user_context
get_screen_orientation
        
some_bidi_screen_orientation
some_web_screen_orientation
        
default_screen_orientation
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
set_screen_orientation_override
(
        
user_contexts
=
[
"
default
"
]
        
screen_orientation
=
some_bidi_screen_orientation
    
)
    
assert
await
get_screen_orientation
(
        
context_in_user_context_1
)
=
=
default_screen_orientation
    
assert
await
get_screen_orientation
(
new_tab
)
=
=
some_web_screen_orientation
    
context_in_default_context_2
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
get_screen_orientation
(
        
context_in_default_context_2
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
        
user_contexts
=
[
"
default
"
]
screen_orientation
=
None
    
)
async
def
test_set_to_multiple_user_contexts
(
bidi_session
create_user_context
        
get_screen_orientation
some_bidi_screen_orientation
        
some_web_screen_orientation
default_screen_orientation
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
set_screen_orientation_override
(
        
user_contexts
=
[
user_context_1
user_context_2
]
        
screen_orientation
=
some_bidi_screen_orientation
)
    
assert
await
get_screen_orientation
(
        
context_in_user_context_1
)
=
=
some_web_screen_orientation
    
assert
await
get_screen_orientation
(
        
context_in_user_context_2
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
        
user_contexts
=
[
user_context_1
]
        
screen_orientation
=
None
)
    
assert
await
get_screen_orientation
(
        
context_in_user_context_1
)
=
=
default_screen_orientation
    
assert
await
get_screen_orientation
(
        
context_in_user_context_2
)
=
=
some_web_screen_orientation
async
def
test_set_to_user_context_and_then_to_context
(
bidi_session
        
create_user_context
new_tab
get_screen_orientation
        
some_bidi_screen_orientation
some_web_screen_orientation
        
another_bidi_screen_orientation
another_web_screen_orientation
        
default_screen_orientation
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
set_screen_orientation_override
(
        
user_contexts
=
[
user_context
]
        
screen_orientation
=
some_bidi_screen_orientation
)
    
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
context_in_user_context_1
[
"
context
"
]
]
        
screen_orientation
=
another_bidi_screen_orientation
)
    
assert
await
get_screen_orientation
(
        
context_in_user_context_1
)
=
=
another_web_screen_orientation
    
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
get_screen_orientation
(
        
context_in_user_context_1
)
=
=
another_web_screen_orientation
    
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
get_screen_orientation
(
        
context_in_user_context_2
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
context_in_user_context_1
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
        
context_in_user_context_1
)
=
=
default_screen_orientation
