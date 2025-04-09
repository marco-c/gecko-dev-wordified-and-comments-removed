import
pytest
from
webdriver
.
bidi
.
modules
.
emulation
import
CoordinatesOptions
from
.
import
get_current_geolocation
TEST_COORDINATES
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
url
create_user_context
new_tab
set_geolocation_permission
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
    
test_url
=
url
(
"
/
common
/
blank
.
html
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
test_url
        
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
navigate
(
        
context
=
new_tab
[
"
context
"
]
        
url
=
test_url
        
wait
=
"
complete
"
    
)
    
await
set_geolocation_permission
(
new_tab
)
    
await
set_geolocation_permission
(
new_tab
user_context
)
    
default_coordinates
=
await
get_current_geolocation
(
        
bidi_session
context_in_user_context_1
    
)
    
assert
default_coordinates
!
=
TEST_COORDINATES
    
assert
await
get_current_geolocation
(
bidi_session
new_tab
)
=
=
default_coordinates
    
await
bidi_session
.
emulation
.
set_geolocation_override
(
        
user_contexts
=
[
user_context
]
        
coordinates
=
CoordinatesOptions
(
            
latitude
=
TEST_COORDINATES
[
"
latitude
"
]
            
longitude
=
TEST_COORDINATES
[
"
longitude
"
]
            
accuracy
=
TEST_COORDINATES
[
"
accuracy
"
]
        
)
    
)
    
assert
(
        
await
get_current_geolocation
(
bidi_session
context_in_user_context_1
)
        
=
=
TEST_COORDINATES
    
)
    
assert
await
get_current_geolocation
(
bidi_session
new_tab
)
=
=
default_coordinates
    
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
bidi_session
.
browsing_context
.
navigate
(
        
context
=
context_in_user_context_2
[
"
context
"
]
        
url
=
test_url
        
wait
=
"
complete
"
    
)
    
assert
(
        
await
get_current_geolocation
(
bidi_session
context_in_user_context_2
)
        
=
=
TEST_COORDINATES
    
)
async
def
test_set_to_default_user_context
(
    
bidi_session
new_tab
create_user_context
url
set_geolocation_permission
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
    
test_url
=
url
(
"
/
common
/
blank
.
html
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
test_url
        
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
navigate
(
        
context
=
new_tab
[
"
context
"
]
        
url
=
test_url
        
wait
=
"
complete
"
    
)
    
await
set_geolocation_permission
(
new_tab
)
    
await
set_geolocation_permission
(
new_tab
user_context
)
    
default_coordinates
=
await
get_current_geolocation
(
bidi_session
new_tab
)
    
assert
default_coordinates
!
=
TEST_COORDINATES
    
await
bidi_session
.
emulation
.
set_geolocation_override
(
        
user_contexts
=
[
"
default
"
]
        
coordinates
=
CoordinatesOptions
(
            
latitude
=
TEST_COORDINATES
[
"
latitude
"
]
            
longitude
=
TEST_COORDINATES
[
"
longitude
"
]
            
accuracy
=
TEST_COORDINATES
[
"
accuracy
"
]
        
)
    
)
    
assert
(
        
await
get_current_geolocation
(
bidi_session
context_in_user_context_1
)
        
=
=
default_coordinates
    
)
    
assert
await
get_current_geolocation
(
bidi_session
new_tab
)
=
=
TEST_COORDINATES
    
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
bidi_session
.
browsing_context
.
navigate
(
        
context
=
context_in_default_context_2
[
"
context
"
]
        
url
=
test_url
        
wait
=
"
complete
"
    
)
    
assert
(
        
await
get_current_geolocation
(
bidi_session
context_in_default_context_2
)
        
=
=
TEST_COORDINATES
    
)
    
await
bidi_session
.
emulation
.
set_geolocation_override
(
        
user_contexts
=
[
"
default
"
]
coordinates
=
None
    
)
async
def
test_set_to_multiple_user_contexts
(
    
bidi_session
create_user_context
url
set_geolocation_permission
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
    
test_url
=
url
(
"
/
common
/
blank
.
html
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
test_url
        
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
navigate
(
        
context
=
context_in_user_context_2
[
"
context
"
]
        
url
=
test_url
        
wait
=
"
complete
"
    
)
    
await
set_geolocation_permission
(
context_in_user_context_1
user_context_1
)
    
await
set_geolocation_permission
(
context_in_user_context_2
user_context_2
)
    
await
bidi_session
.
emulation
.
set_geolocation_override
(
        
user_contexts
=
[
user_context_1
user_context_2
]
        
coordinates
=
CoordinatesOptions
(
            
latitude
=
TEST_COORDINATES
[
"
latitude
"
]
            
longitude
=
TEST_COORDINATES
[
"
longitude
"
]
            
accuracy
=
TEST_COORDINATES
[
"
accuracy
"
]
        
)
    
)
    
assert
(
        
await
get_current_geolocation
(
bidi_session
context_in_user_context_1
)
        
=
=
TEST_COORDINATES
    
)
    
assert
(
        
await
get_current_geolocation
(
bidi_session
context_in_user_context_2
)
        
=
=
TEST_COORDINATES
    
)
async
def
test_set_to_user_context_and_then_to_context
(
    
bidi_session
create_user_context
url
new_tab
set_geolocation_permission
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
    
test_url
=
url
(
"
/
common
/
blank
.
html
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
test_url
        
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
navigate
(
        
context
=
new_tab
[
"
context
"
]
        
url
=
test_url
        
wait
=
"
complete
"
    
)
    
await
set_geolocation_permission
(
new_tab
)
    
await
set_geolocation_permission
(
new_tab
user_context
)
    
default_coordinates
=
await
get_current_geolocation
(
        
bidi_session
context_in_user_context_1
    
)
    
assert
default_coordinates
!
=
TEST_COORDINATES
    
await
bidi_session
.
emulation
.
set_geolocation_override
(
        
user_contexts
=
[
user_context
]
        
coordinates
=
CoordinatesOptions
(
            
latitude
=
TEST_COORDINATES
[
"
latitude
"
]
            
longitude
=
TEST_COORDINATES
[
"
longitude
"
]
            
accuracy
=
TEST_COORDINATES
[
"
accuracy
"
]
        
)
    
)
    
new_geolocation_coordinates
=
{
"
latitude
"
:
30
"
longitude
"
:
20
"
accuracy
"
:
3
}
    
await
bidi_session
.
emulation
.
set_geolocation_override
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
        
coordinates
=
CoordinatesOptions
(
            
latitude
=
new_geolocation_coordinates
[
"
latitude
"
]
            
longitude
=
new_geolocation_coordinates
[
"
longitude
"
]
            
accuracy
=
new_geolocation_coordinates
[
"
accuracy
"
]
        
)
    
)
    
assert
(
        
await
get_current_geolocation
(
bidi_session
context_in_user_context_1
)
        
=
=
new_geolocation_coordinates
    
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
get_current_geolocation
(
bidi_session
context_in_user_context_1
)
        
=
=
new_geolocation_coordinates
    
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
bidi_session
.
browsing_context
.
navigate
(
        
context
=
context_in_user_context_2
[
"
context
"
]
        
url
=
test_url
        
wait
=
"
complete
"
    
)
    
assert
(
        
await
get_current_geolocation
(
bidi_session
context_in_user_context_2
)
        
=
=
TEST_COORDINATES
    
)
    
await
bidi_session
.
emulation
.
set_geolocation_override
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
        
coordinates
=
None
    
)
    
assert
(
        
await
get_current_geolocation
(
bidi_session
context_in_user_context_1
)
        
=
=
default_coordinates
    
)
