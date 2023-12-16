import
pytest
import
random
from
tests
.
support
.
sync
import
AsyncPoll
from
.
.
import
assert_response_event
PAGE_EMPTY_TEXT
RESPONSE_STARTED_EVENT
pytest
.
mark
.
asyncio
async
def
test_cached
(
    
wait_for_event
    
wait_for_future_safe
    
url
    
fetch
    
setup_network_test
)
:
    
network_events
=
await
setup_network_test
(
        
events
=
[
            
RESPONSE_STARTED_EVENT
        
]
    
)
    
events
=
network_events
[
RESPONSE_STARTED_EVENT
]
    
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
    
on_response_started
=
wait_for_event
(
RESPONSE_STARTED_EVENT
)
    
await
fetch
(
cached_url
)
    
await
wait_for_future_safe
(
on_response_started
)
    
assert
len
(
events
)
=
=
1
    
expected_request
=
{
"
method
"
:
"
GET
"
"
url
"
:
cached_url
}
    
expected_response
=
{
        
"
url
"
:
cached_url
        
"
fromCache
"
:
False
        
"
status
"
:
200
    
}
    
assert_response_event
(
        
events
[
0
]
        
expected_request
=
expected_request
        
expected_response
=
expected_response
    
)
    
on_response_started
=
wait_for_event
(
RESPONSE_STARTED_EVENT
)
    
await
fetch
(
cached_url
)
    
await
wait_for_future_safe
(
on_response_started
)
    
assert
len
(
events
)
=
=
2
    
expected_response
=
{
        
"
url
"
:
cached_url
        
"
fromCache
"
:
True
        
"
status
"
:
200
    
}
    
assert_response_event
(
        
events
[
1
]
        
expected_request
=
expected_request
        
expected_response
=
expected_response
    
)
pytest
.
mark
.
asyncio
async
def
test_cached_redirect
(
    
bidi_session
    
url
    
fetch
    
setup_network_test
)
:
    
network_events
=
await
setup_network_test
(
        
events
=
[
            
RESPONSE_STARTED_EVENT
        
]
    
)
    
events
=
network_events
[
RESPONSE_STARTED_EVENT
]
    
text_url
=
url
(
PAGE_EMPTY_TEXT
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
301
&
location
=
{
text_url
}
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
    
await
fetch
(
cached_url
)
    
wait
=
AsyncPoll
(
bidi_session
timeout
=
2
)
    
await
wait
.
until
(
lambda
_
:
len
(
events
)
>
=
2
)
    
assert
len
(
events
)
=
=
2
    
expected_request
=
{
"
method
"
:
"
GET
"
"
url
"
:
cached_url
}
    
expected_response
=
{
        
"
url
"
:
cached_url
        
"
fromCache
"
:
False
        
"
status
"
:
301
    
}
    
assert_response_event
(
        
events
[
0
]
        
expected_request
=
expected_request
        
expected_response
=
expected_response
    
)
    
redirected_request
=
{
"
method
"
:
"
GET
"
"
url
"
:
text_url
}
    
redirected_response
=
{
"
url
"
:
text_url
"
status
"
:
200
}
    
assert_response_event
(
        
events
[
1
]
        
expected_request
=
redirected_request
        
expected_response
=
redirected_response
    
)
    
await
fetch
(
cached_url
)
    
wait
=
AsyncPoll
(
bidi_session
timeout
=
2
)
    
await
wait
.
until
(
lambda
_
:
len
(
events
)
>
=
4
)
    
assert
len
(
events
)
=
=
4
    
expected_response
=
{
        
"
url
"
:
cached_url
        
"
fromCache
"
:
True
        
"
status
"
:
301
    
}
    
assert_response_event
(
        
events
[
2
]
        
expected_request
=
expected_request
        
expected_response
=
expected_response
    
)
    
assert_response_event
(
        
events
[
3
]
        
expected_request
=
redirected_request
        
expected_response
=
redirected_response
    
)
pytest
.
mark
.
parametrize
(
    
"
method
"
    
[
        
"
GET
"
        
"
HEAD
"
        
"
OPTIONS
"
    
]
)
pytest
.
mark
.
asyncio
async
def
test_cached_revalidate
(
    
wait_for_event
wait_for_future_safe
url
fetch
setup_network_test
method
)
:
    
network_events
=
await
setup_network_test
(
        
events
=
[
            
RESPONSE_STARTED_EVENT
        
]
    
)
    
events
=
network_events
[
RESPONSE_STARTED_EVENT
]
    
revalidate_url
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
must
-
revalidate
.
py
?
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
    
on_response_started
=
wait_for_event
(
RESPONSE_STARTED_EVENT
)
    
await
fetch
(
revalidate_url
method
=
method
)
    
await
wait_for_future_safe
(
on_response_started
)
    
assert
len
(
events
)
=
=
1
    
expected_request
=
{
"
method
"
:
method
"
url
"
:
revalidate_url
}
    
expected_response
=
{
        
"
url
"
:
revalidate_url
        
"
fromCache
"
:
False
        
"
status
"
:
200
    
}
    
assert_response_event
(
        
events
[
0
]
        
expected_request
=
expected_request
        
expected_response
=
expected_response
    
)
    
on_response_started
=
wait_for_event
(
RESPONSE_STARTED_EVENT
)
    
await
fetch
(
revalidate_url
method
=
method
headers
=
{
"
return
-
304
"
:
"
true
"
}
)
    
await
wait_for_future_safe
(
on_response_started
)
    
assert
len
(
events
)
=
=
2
    
expected_response
=
{
        
"
url
"
:
revalidate_url
        
"
fromCache
"
:
False
        
"
status
"
:
304
    
}
    
assert_response_event
(
        
events
[
1
]
        
expected_request
=
expected_request
        
expected_response
=
expected_response
    
)
