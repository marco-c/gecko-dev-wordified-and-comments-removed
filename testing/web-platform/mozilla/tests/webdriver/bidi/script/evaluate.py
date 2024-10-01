import
asyncio
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
DOCUMENT_LOADED_SCRIPT
=
"
"
"
    
new
Promise
(
resolve
=
>
{
        
const
checkDone
=
(
)
=
>
{
            
if
(
window
.
location
.
href
!
=
=
"
about
:
blank
"
)
{
                
resolve
(
window
.
location
.
href
)
;
            
}
        
}
;
        
if
(
document
.
readyState
=
=
=
"
complete
"
)
{
            
checkDone
(
)
;
        
}
        
window
.
addEventListener
(
"
load
"
checkDone
)
;
    
}
)
    
"
"
"
PAGE
=
"
/
webdriver
/
tests
/
support
/
html
/
default
.
html
?
pipe
=
trickle
(
d1
)
"
async
def
test_retry_during_initial_load
(
bidi_session
url
new_tab
)
:
    
page_url
=
url
(
PAGE
)
    
result
=
await
bidi_session
.
script
.
evaluate
(
        
expression
=
f
"
"
"
window
.
open
(
"
{
page_url
}
"
)
"
"
"
        
await_promise
=
False
        
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
    
)
    
new_window
=
result
[
"
value
"
]
    
try
:
        
result
=
await
bidi_session
.
script
.
evaluate
(
            
expression
=
DOCUMENT_LOADED_SCRIPT
            
await_promise
=
True
            
target
=
ContextTarget
(
new_window
[
"
context
"
]
)
        
)
        
assert
result
[
"
value
"
]
=
=
page_url
    
finally
:
        
await
bidi_session
.
browsing_context
.
close
(
context
=
new_window
[
"
context
"
]
)
async
def
test_retry_during_navigation
(
bidi_session
new_tab
url
)
:
    
page_url
=
url
(
PAGE
)
    
asyncio
.
create_task
(
        
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
page_url
wait
=
"
none
"
        
)
    
)
    
result
=
await
bidi_session
.
script
.
evaluate
(
        
expression
=
DOCUMENT_LOADED_SCRIPT
        
await_promise
=
True
        
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
    
)
    
assert
result
[
"
value
"
]
=
=
page_url
