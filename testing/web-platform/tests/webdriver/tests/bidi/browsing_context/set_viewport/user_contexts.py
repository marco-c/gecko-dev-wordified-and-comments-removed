import
pytest
from
webdriver
.
bidi
.
undefined
import
UNDEFINED
from
.
.
.
import
get_device_pixel_ratio
get_viewport_dimensions
pytestmark
=
pytest
.
mark
.
asyncio
async
def
test_set_to_user_context
(
bidi_session
new_tab
create_user_context
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
    
test_viewport
=
{
"
width
"
:
250
"
height
"
:
300
}
    
assert
await
get_viewport_dimensions
(
bidi_session
new_tab
)
!
=
test_viewport
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_1
)
        
!
=
test_viewport
    
)
    
await
bidi_session
.
browsing_context
.
set_viewport
(
        
user_contexts
=
[
user_context
]
viewport
=
test_viewport
    
)
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_1
)
        
=
=
test_viewport
    
)
    
assert
await
get_viewport_dimensions
(
bidi_session
new_tab
)
!
=
test_viewport
    
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
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_2
)
        
=
=
test_viewport
    
)
    
context_in_default_context
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
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_default_context
)
        
!
=
test_viewport
    
)
async
def
test_set_to_default_user_context
(
bidi_session
new_tab
create_user_context
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
    
test_viewport
=
{
"
width
"
:
250
"
height
"
:
300
}
    
assert
await
get_viewport_dimensions
(
bidi_session
new_tab
)
!
=
test_viewport
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_1
)
        
!
=
test_viewport
    
)
    
await
bidi_session
.
browsing_context
.
set_viewport
(
        
user_contexts
=
[
"
default
"
]
viewport
=
test_viewport
    
)
    
assert
await
get_viewport_dimensions
(
bidi_session
new_tab
)
=
=
test_viewport
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_1
)
        
!
=
test_viewport
    
)
    
context_in_default_context
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
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_default_context
)
        
=
=
test_viewport
    
)
    
await
bidi_session
.
browsing_context
.
set_viewport
(
        
user_contexts
=
[
"
default
"
]
viewport
=
None
    
)
async
def
test_set_to_multiple_user_contexts
(
bidi_session
create_user_context
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
    
test_viewport
=
{
"
width
"
:
250
"
height
"
:
300
}
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_1
)
        
!
=
test_viewport
    
)
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_2
)
        
!
=
test_viewport
    
)
    
await
bidi_session
.
browsing_context
.
set_viewport
(
        
user_contexts
=
[
user_context_1
user_context_2
]
viewport
=
test_viewport
    
)
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_1
)
        
=
=
test_viewport
    
)
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_2
)
        
=
=
test_viewport
    
)
async
def
test_undefined_viewport
(
bidi_session
inline
create_user_context
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
    
test_viewport
=
{
"
width
"
:
499
"
height
"
:
599
}
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_1
)
        
!
=
test_viewport
    
)
    
url
=
inline
(
"
<
div
>
foo
<
/
div
>
"
)
    
await
bidi_session
.
browsing_context
.
navigate
(
        
context
=
context_in_user_context_1
[
"
context
"
]
url
=
url
wait
=
"
complete
"
    
)
    
await
bidi_session
.
browsing_context
.
set_viewport
(
        
user_contexts
=
[
user_context
]
viewport
=
test_viewport
    
)
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_1
)
        
=
=
test_viewport
    
)
    
await
bidi_session
.
browsing_context
.
set_viewport
(
        
user_contexts
=
[
user_context
]
viewport
=
UNDEFINED
    
)
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_1
)
        
=
=
test_viewport
    
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
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_2
)
        
=
=
test_viewport
    
)
async
def
test_reset_to_default
(
bidi_session
inline
create_user_context
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
    
original_viewport
=
await
get_viewport_dimensions
(
        
bidi_session
context_in_user_context_1
    
)
    
test_viewport
=
{
"
width
"
:
666
"
height
"
:
333
}
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_1
)
        
!
=
test_viewport
    
)
    
url
=
inline
(
"
<
div
>
foo
<
/
div
>
"
)
    
await
bidi_session
.
browsing_context
.
navigate
(
        
context
=
context_in_user_context_1
[
"
context
"
]
url
=
url
wait
=
"
complete
"
    
)
    
await
bidi_session
.
browsing_context
.
set_viewport
(
        
user_contexts
=
[
user_context
]
viewport
=
test_viewport
    
)
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_1
)
        
=
=
test_viewport
    
)
    
await
bidi_session
.
browsing_context
.
set_viewport
(
        
user_contexts
=
[
user_context
]
viewport
=
None
    
)
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_1
)
        
=
=
original_viewport
    
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
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_2
)
        
=
=
original_viewport
    
)
async
def
test_set_viewport_and_device_pixel_ratio
(
bidi_session
create_user_context
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
    
test_viewport
=
{
"
width
"
:
250
"
height
"
:
300
}
    
await
bidi_session
.
browsing_context
.
set_viewport
(
        
user_contexts
=
[
user_context
]
viewport
=
test_viewport
    
)
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_1
)
        
=
=
test_viewport
    
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
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_2
)
        
=
=
test_viewport
    
)
    
test_device_pixel_ratio
=
2
    
await
bidi_session
.
browsing_context
.
set_viewport
(
        
user_contexts
=
[
user_context
]
device_pixel_ratio
=
test_device_pixel_ratio
    
)
    
assert
(
        
await
get_device_pixel_ratio
(
bidi_session
context_in_user_context_1
)
        
=
=
test_device_pixel_ratio
    
)
    
assert
(
        
await
get_device_pixel_ratio
(
bidi_session
context_in_user_context_2
)
        
=
=
test_device_pixel_ratio
    
)
    
context_in_user_context_3
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
(
        
await
get_device_pixel_ratio
(
bidi_session
context_in_user_context_3
)
        
=
=
test_device_pixel_ratio
    
)
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_3
)
        
=
=
test_viewport
    
)
async
def
test_set_to_user_context_and_then_to_context
(
    
bidi_session
create_user_context
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
    
test_viewport
=
{
"
width
"
:
250
"
height
"
:
300
}
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_1
)
        
!
=
test_viewport
    
)
    
await
bidi_session
.
browsing_context
.
set_viewport
(
        
user_contexts
=
[
user_context
]
viewport
=
test_viewport
    
)
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_1
)
        
=
=
test_viewport
    
)
    
new_test_viewport
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
browsing_context
.
set_viewport
(
        
context
=
context_in_user_context_1
[
"
context
"
]
viewport
=
new_test_viewport
    
)
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_1
)
        
=
=
new_test_viewport
    
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
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_1
)
        
=
=
new_test_viewport
    
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
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_2
)
        
=
=
test_viewport
    
)
async
def
test_set_viewport_to_user_context_and_then_device_pixel_ratio_to_context
(
    
bidi_session
create_user_context
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
    
original_dpr
=
await
get_device_pixel_ratio
(
bidi_session
context_in_user_context_1
)
    
test_dpr
=
original_dpr
+
1
    
test_viewport
=
{
"
width
"
:
250
"
height
"
:
300
}
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_1
)
        
!
=
test_viewport
    
)
    
await
bidi_session
.
browsing_context
.
set_viewport
(
        
user_contexts
=
[
user_context
]
viewport
=
test_viewport
    
)
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_1
)
        
=
=
test_viewport
    
)
    
await
bidi_session
.
browsing_context
.
set_viewport
(
        
context
=
context_in_user_context_1
[
"
context
"
]
device_pixel_ratio
=
test_dpr
    
)
    
assert
(
        
await
get_device_pixel_ratio
(
bidi_session
context_in_user_context_1
)
        
=
=
test_dpr
    
)
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_1
)
        
=
=
test_viewport
    
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
    
assert
(
        
await
get_viewport_dimensions
(
bidi_session
context_in_user_context_2
)
        
=
=
test_viewport
    
)
    
assert
(
        
await
get_device_pixel_ratio
(
bidi_session
context_in_user_context_2
)
        
=
=
original_dpr
    
)
