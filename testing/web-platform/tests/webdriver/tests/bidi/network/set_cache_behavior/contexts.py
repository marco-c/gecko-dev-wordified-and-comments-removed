import
pytest
import
random
from
.
.
import
RESPONSE_COMPLETED_EVENT
pytestmark
=
pytest
.
mark
.
asyncio
async
def
test_one_context
(
    
bidi_session
    
setup_network_test
    
top_context
    
new_tab
    
url
    
inline
    
is_request_from_cache
)
:
    
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
inline
(
"
foo
"
)
        
wait
=
"
complete
"
    
)
    
await
setup_network_test
(
        
events
=
[
RESPONSE_COMPLETED_EVENT
]
        
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
    
)
    
cached_url
=
url
(
        
f
"
/
webdriver
/
tests
/
support
/
http_handlers
/
cached
.
py
?
status
=
200
&
nocache
=
{
random
.
random
(
)
}
"
    
)
    
assert
await
is_request_from_cache
(
url
=
cached_url
context
=
top_context
)
is
False
    
assert
await
is_request_from_cache
(
url
=
cached_url
context
=
new_tab
)
is
True
    
await
bidi_session
.
network
.
set_cache_behavior
(
        
cache_behavior
=
"
bypass
"
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
    
)
    
assert
await
is_request_from_cache
(
url
=
cached_url
context
=
top_context
)
is
True
    
assert
await
is_request_from_cache
(
url
=
cached_url
context
=
new_tab
)
is
False
    
await
bidi_session
.
network
.
set_cache_behavior
(
        
cache_behavior
=
"
default
"
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
    
)
pytest
.
mark
.
parametrize
(
"
type_hint
"
[
"
tab
"
"
window
"
]
)
async
def
test_new_context
(
    
bidi_session
    
setup_network_test
    
top_context
    
url
    
inline
    
is_request_from_cache
    
type_hint
)
:
    
await
setup_network_test
(
events
=
[
RESPONSE_COMPLETED_EVENT
]
)
    
cached_url
=
url
(
        
f
"
/
webdriver
/
tests
/
support
/
http_handlers
/
cached
.
py
?
status
=
200
&
nocache
=
{
random
.
random
(
)
}
"
    
)
    
assert
await
is_request_from_cache
(
url
=
cached_url
)
is
False
    
assert
await
is_request_from_cache
(
url
=
cached_url
)
is
True
    
await
bidi_session
.
network
.
set_cache_behavior
(
        
cache_behavior
=
"
bypass
"
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
    
)
    
assert
await
is_request_from_cache
(
url
=
cached_url
context
=
top_context
)
is
False
    
new_context
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
type_hint
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
new_context
[
"
context
"
]
        
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
        
wait
=
"
complete
"
    
)
    
assert
await
is_request_from_cache
(
cached_url
context
=
new_context
)
is
True
    
await
bidi_session
.
network
.
set_cache_behavior
(
        
cache_behavior
=
"
default
"
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
    
)
