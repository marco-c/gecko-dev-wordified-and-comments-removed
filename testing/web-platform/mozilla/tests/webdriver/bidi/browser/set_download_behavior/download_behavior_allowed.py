import
asyncio
import
tempfile
import
pytest
from
webdriver
.
bidi
.
modules
.
script
import
ContextTarget
pytestmark
=
pytest
.
mark
.
asyncio
DOWNLOAD_WILL_BEGIN
=
"
browsingContext
.
downloadWillBegin
"
DOWNLOAD_END
=
"
browsingContext
.
downloadEnd
"
async
def
test_unique_filename
(
    
bidi_session
    
new_tab
    
inline
    
subscribe_events
    
wait_for_event
    
wait_for_future_safe
)
:
    
await
subscribe_events
(
events
=
[
DOWNLOAD_END
]
)
    
url
=
inline
(
        
"
"
"
<
a
id
=
"
download_link
"
href
=
"
/
_mozilla
/
webdriver
/
support
/
assets
/
big
.
png
"
download
>
download
<
/
a
>
"
"
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
url
wait
=
"
complete
"
    
)
    
on_download_end
=
wait_for_event
(
DOWNLOAD_END
)
    
result
=
await
bidi_session
.
browsing_context
.
locate_nodes
(
        
context
=
new_tab
[
"
context
"
]
locator
=
{
"
type
"
:
"
css
"
"
value
"
:
"
#
download_link
"
}
    
)
    
await
bidi_session
.
script
.
call_function
(
        
arguments
=
[
result
[
"
nodes
"
]
[
0
]
]
        
function_declaration
=
"
(
link
)
=
>
link
.
click
(
)
"
        
target
=
ContextTarget
(
new_tab
[
"
context
"
]
)
        
await_promise
=
True
        
user_activation
=
True
    
)
    
await
wait_for_future_safe
(
on_download_end
)
    
await
subscribe_events
(
events
=
[
DOWNLOAD_WILL_BEGIN
]
)
    
await
bidi_session
.
browser
.
set_download_behavior
(
        
download_behavior
=
{
"
type
"
:
"
allowed
"
"
destinationFolder
"
:
tempfile
.
mkdtemp
(
)
}
    
)
    
on_download_will_begin
=
wait_for_event
(
DOWNLOAD_WILL_BEGIN
)
    
on_download_end
=
wait_for_event
(
DOWNLOAD_END
)
    
await
bidi_session
.
script
.
call_function
(
        
arguments
=
[
result
[
"
nodes
"
]
[
0
]
]
        
function_declaration
=
"
(
link
)
=
>
link
.
click
(
)
"
        
target
=
ContextTarget
(
new_tab
[
"
context
"
]
)
        
await_promise
=
True
        
user_activation
=
True
    
)
    
event
=
await
wait_for_future_safe
(
on_download_will_begin
)
    
filename
=
"
big
.
png
"
    
assert
event
[
"
suggestedFilename
"
]
=
=
filename
    
await
wait_for_future_safe
(
on_download_end
)
    
on_download_will_begin
=
wait_for_event
(
DOWNLOAD_WILL_BEGIN
)
    
await
bidi_session
.
script
.
call_function
(
        
arguments
=
[
result
[
"
nodes
"
]
[
0
]
]
        
function_declaration
=
"
(
link
)
=
>
link
.
click
(
)
"
        
target
=
ContextTarget
(
new_tab
[
"
context
"
]
)
        
await_promise
=
True
        
user_activation
=
True
    
)
    
event
=
await
wait_for_future_safe
(
on_download_will_begin
)
    
assert
"
big
"
in
event
[
"
suggestedFilename
"
]
    
assert
event
[
"
suggestedFilename
"
]
!
=
filename
    
await
bidi_session
.
browser
.
set_download_behavior
(
download_behavior
=
None
)
async
def
test_download_focus
(
    
bidi_session
    
new_tab
    
subscribe_events
    
inline
    
wait_for_event
    
wait_for_future_safe
    
get_document_focus
)
:
    
await
bidi_session
.
browser
.
set_download_behavior
(
        
download_behavior
=
{
"
type
"
:
"
allowed
"
"
destinationFolder
"
:
tempfile
.
mkdtemp
(
)
}
    
)
    
assert
await
get_document_focus
(
new_tab
)
is
True
    
await
subscribe_events
(
events
=
[
DOWNLOAD_END
]
)
    
url
=
inline
(
        
"
"
"
<
a
id
=
"
download_link
"
href
=
"
/
_mozilla
/
webdriver
/
support
/
assets
/
big
.
png
"
download
>
download
<
/
a
>
"
"
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
url
wait
=
"
complete
"
    
)
    
on_download_end
=
wait_for_event
(
DOWNLOAD_END
)
    
result
=
await
bidi_session
.
browsing_context
.
locate_nodes
(
        
context
=
new_tab
[
"
context
"
]
locator
=
{
"
type
"
:
"
css
"
"
value
"
:
"
#
download_link
"
}
    
)
    
await
bidi_session
.
script
.
call_function
(
        
arguments
=
[
result
[
"
nodes
"
]
[
0
]
]
        
function_declaration
=
"
(
link
)
=
>
link
.
click
(
)
"
        
target
=
ContextTarget
(
new_tab
[
"
context
"
]
)
        
await_promise
=
True
        
user_activation
=
True
    
)
    
await
wait_for_future_safe
(
on_download_end
)
    
await
asyncio
.
sleep
(
1
)
    
assert
await
get_document_focus
(
new_tab
)
is
True
    
await
bidi_session
.
browser
.
set_download_behavior
(
download_behavior
=
None
)
