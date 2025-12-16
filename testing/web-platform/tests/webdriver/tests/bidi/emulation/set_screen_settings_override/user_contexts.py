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
    
assert_screen_dimensions
    
get_current_screen_dimensions
)
:
    
default_screen_dimensions
=
await
get_current_screen_dimensions
(
new_tab
)
    
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
    
screen_area_override
=
{
"
width
"
:
100
"
height
"
:
100
}
    
await
bidi_session
.
emulation
.
set_screen_settings_override
(
        
user_contexts
=
[
user_context
]
screen_area
=
screen_area_override
    
)
    
await
assert_screen_dimensions
(
        
context_in_user_context_1
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
    
)
    
await
assert_screen_dimensions
(
        
new_tab
        
default_screen_dimensions
[
"
width
"
]
        
default_screen_dimensions
[
"
height
"
]
        
default_screen_dimensions
[
"
availWidth
"
]
        
default_screen_dimensions
[
"
availHeight
"
]
    
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
user_context
type_hint
=
"
tab
"
    
)
    
await
assert_screen_dimensions
(
        
context_in_user_context_2
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
    
)
async
def
test_set_to_default_user_context
(
    
bidi_session
    
new_tab
    
create_user_context
    
assert_screen_dimensions
    
get_current_screen_dimensions
)
:
    
default_screen_dimensions
=
await
get_current_screen_dimensions
(
new_tab
)
    
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
    
screen_area_override
=
{
"
width
"
:
100
"
height
"
:
100
}
    
await
bidi_session
.
emulation
.
set_screen_settings_override
(
        
user_contexts
=
[
"
default
"
]
screen_area
=
screen_area_override
    
)
    
await
assert_screen_dimensions
(
        
new_tab
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
    
)
    
await
assert_screen_dimensions
(
        
context_in_user_context_1
        
default_screen_dimensions
[
"
width
"
]
        
default_screen_dimensions
[
"
height
"
]
        
default_screen_dimensions
[
"
availWidth
"
]
        
default_screen_dimensions
[
"
availHeight
"
]
    
)
    
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
    
await
assert_screen_dimensions
(
        
context_in_default_context_2
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
    
)
    
await
bidi_session
.
emulation
.
set_screen_settings_override
(
        
user_contexts
=
[
"
default
"
]
screen_area
=
None
    
)
async
def
test_set_to_multiple_user_contexts
(
    
bidi_session
    
new_tab
    
create_user_context
    
assert_screen_dimensions
    
get_current_screen_dimensions
)
:
    
default_screen_dimensions
=
await
get_current_screen_dimensions
(
new_tab
)
    
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
    
screen_area_override
=
{
"
width
"
:
100
"
height
"
:
100
}
    
await
bidi_session
.
emulation
.
set_screen_settings_override
(
        
user_contexts
=
[
user_context_1
user_context_2
]
screen_area
=
screen_area_override
    
)
    
await
assert_screen_dimensions
(
        
context_in_user_context_1
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
    
)
    
await
assert_screen_dimensions
(
        
context_in_user_context_2
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
    
)
    
await
bidi_session
.
emulation
.
set_screen_settings_override
(
        
user_contexts
=
[
user_context_1
]
screen_area
=
None
    
)
    
await
assert_screen_dimensions
(
        
context_in_user_context_1
        
default_screen_dimensions
[
"
width
"
]
        
default_screen_dimensions
[
"
height
"
]
        
default_screen_dimensions
[
"
availWidth
"
]
        
default_screen_dimensions
[
"
availHeight
"
]
    
)
    
await
assert_screen_dimensions
(
        
context_in_user_context_2
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
    
)
async
def
test_set_to_user_context_and_then_to_context
(
    
bidi_session
    
create_user_context
    
new_tab
    
assert_screen_dimensions
    
get_current_screen_dimensions
)
:
    
default_screen_dimensions
=
await
get_current_screen_dimensions
(
new_tab
)
    
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
    
screen_area_override
=
{
"
width
"
:
100
"
height
"
:
100
}
    
await
bidi_session
.
emulation
.
set_screen_settings_override
(
        
user_contexts
=
[
user_context
]
screen_area
=
screen_area_override
    
)
    
another_screen_area_override
=
{
"
width
"
:
200
"
height
"
:
200
}
    
await
bidi_session
.
emulation
.
set_screen_settings_override
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
        
screen_area
=
another_screen_area_override
    
)
    
await
assert_screen_dimensions
(
        
context_in_user_context_1
        
another_screen_area_override
[
"
width
"
]
        
another_screen_area_override
[
"
height
"
]
        
another_screen_area_override
[
"
width
"
]
        
another_screen_area_override
[
"
height
"
]
    
)
    
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
    
await
assert_screen_dimensions
(
        
context_in_user_context_1
        
another_screen_area_override
[
"
width
"
]
        
another_screen_area_override
[
"
height
"
]
        
another_screen_area_override
[
"
width
"
]
        
another_screen_area_override
[
"
height
"
]
    
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
user_context
type_hint
=
"
tab
"
    
)
    
await
assert_screen_dimensions
(
        
context_in_user_context_2
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
    
)
    
await
bidi_session
.
emulation
.
set_screen_settings_override
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
screen_area
=
None
    
)
    
await
assert_screen_dimensions
(
        
context_in_user_context_1
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
    
)
    
await
bidi_session
.
emulation
.
set_screen_settings_override
(
        
user_contexts
=
[
user_context
]
screen_area
=
None
    
)
    
await
assert_screen_dimensions
(
        
context_in_user_context_2
        
default_screen_dimensions
[
"
width
"
]
        
default_screen_dimensions
[
"
height
"
]
        
default_screen_dimensions
[
"
availWidth
"
]
        
default_screen_dimensions
[
"
availHeight
"
]
    
)
async
def
test_set_to_context_and_then_to_user_context
(
    
bidi_session
    
create_user_context
    
new_tab
    
assert_screen_dimensions
    
get_current_screen_dimensions
)
:
    
default_screen_dimensions
=
await
get_current_screen_dimensions
(
new_tab
)
    
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
    
screen_area_override
=
{
"
width
"
:
100
"
height
"
:
100
}
    
await
bidi_session
.
emulation
.
set_screen_settings_override
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
        
screen_area
=
screen_area_override
    
)
    
await
assert_screen_dimensions
(
        
context_in_user_context_1
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
    
)
    
another_screen_area_override
=
{
"
width
"
:
200
"
height
"
:
200
}
    
await
bidi_session
.
emulation
.
set_screen_settings_override
(
        
user_contexts
=
[
user_context
]
        
screen_area
=
another_screen_area_override
    
)
    
await
assert_screen_dimensions
(
        
context_in_user_context_1
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
    
)
    
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
    
await
assert_screen_dimensions
(
        
context_in_user_context_1
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
    
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
user_context
type_hint
=
"
tab
"
    
)
    
await
assert_screen_dimensions
(
        
context_in_user_context_2
        
another_screen_area_override
[
"
width
"
]
        
another_screen_area_override
[
"
height
"
]
        
another_screen_area_override
[
"
width
"
]
        
another_screen_area_override
[
"
height
"
]
    
)
    
await
bidi_session
.
emulation
.
set_screen_settings_override
(
        
user_contexts
=
[
user_context
]
        
screen_area
=
None
    
)
    
await
assert_screen_dimensions
(
        
context_in_user_context_1
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
        
screen_area_override
[
"
width
"
]
        
screen_area_override
[
"
height
"
]
    
)
    
await
assert_screen_dimensions
(
        
context_in_user_context_2
        
default_screen_dimensions
[
"
width
"
]
        
default_screen_dimensions
[
"
height
"
]
        
default_screen_dimensions
[
"
availWidth
"
]
        
default_screen_dimensions
[
"
availHeight
"
]
    
)
