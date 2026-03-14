import
os
import
pytest
from
tests
.
support
.
sync
import
AsyncPoll
from
webdriver
.
error
import
TimeoutException
from
.
.
import
using_context
pytestmark
=
pytest
.
mark
.
asyncio
pytest
.
mark
.
allow_system_access
pytest
.
mark
.
parametrize
(
    
"
event_name
"
    
[
        
"
browsingContext
.
contextCreated
"
        
"
browsingContext
.
contextDestroyed
"
        
"
browsingContext
.
navigationStarted
"
        
"
browsingContext
.
navigationFailed
"
    
]
)
async
def
test_webextension_popup_context
(
    
bidi_session
    
current_session
    
install_webextension
    
subscribe_events
    
top_context
    
event_name
)
:
    
path
=
os
.
path
.
join
(
        
os
.
path
.
abspath
(
os
.
path
.
dirname
(
__file__
)
)
        
"
.
.
"
        
"
support
"
        
"
popup_webextension
"
    
)
    
extension_data
=
{
"
type
"
:
"
path
"
"
path
"
:
path
}
    
await
install_webextension
(
extension_data
=
extension_data
)
    
await
subscribe_events
(
events
=
[
event_name
]
)
    
events
=
[
]
    
async
def
on_event
(
method
data
)
:
        
events
.
append
(
data
)
    
remove_listener
=
bidi_session
.
add_event_listener
(
event_name
on_event
)
    
with
using_context
(
current_session
"
chrome
"
)
:
        
button
=
current_session
.
find
.
css
(
            
"
toolbaritem
[
label
=
TestPopupExtension
]
"
all
=
False
        
)
        
mouse_chain
=
current_session
.
actions
.
sequence
(
            
"
pointer
"
"
pointer_id
"
{
"
pointerType
"
:
"
mouse
"
}
        
)
        
mouse_chain
.
pointer_move
(
0
0
origin
=
button
)
.
pointer_down
(
)
.
pointer_up
(
)
.
pause
(
            
100
        
)
.
pointer_down
(
)
.
pointer_up
(
)
.
perform
(
)
    
wait
=
AsyncPoll
(
bidi_session
timeout
=
0
.
5
)
    
with
pytest
.
raises
(
TimeoutException
)
:
        
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
0
)
    
remove_listener
(
)
