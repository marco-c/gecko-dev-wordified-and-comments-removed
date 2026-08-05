from
copy
import
deepcopy
import
pytest
from
webdriver
.
bidi
.
error
import
UnsupportedOperationException
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
async
def
test_evaluate_parent_process_context
(
parent_process_context
)
:
    
bidi_session
context_id
=
parent_process_context
    
with
pytest
.
raises
(
UnsupportedOperationException
)
:
        
await
bidi_session
.
script
.
evaluate
(
            
expression
=
"
1
+
1
"
            
target
=
ContextTarget
(
context_id
)
            
await_promise
=
False
        
)
pytest
.
mark
.
geckodriver
(
allow_system_access
=
True
)
pytest
.
mark
.
parametrize
(
    
"
expression
expected_value
"
    
[
        
(
            
"
ChromeUtils
.
getClassName
(
document
.
defaultView
)
"
            
{
"
type
"
:
"
string
"
"
value
"
:
"
Window
"
}
        
)
        
(
            
"
Ci
.
nsICookie
.
SAMESITE_STRICT
"
            
{
"
type
"
:
"
number
"
"
value
"
:
2
}
        
)
    
]
    
ids
=
[
"
chrome
-
utils
"
"
interface
"
]
)
async
def
test_evaluate_chrome_context_with_system_access
(
    
bidi_session
chrome_context
expression
expected_value
)
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
expression
        
target
=
ContextTarget
(
chrome_context
[
"
context
"
]
)
        
await_promise
=
False
    
)
    
assert
result
=
=
expected_value
pytest
.
mark
.
geckodriver
(
allow_system_access
=
True
)
async
def
test_evaluate_parent_process_context_with_system_access
(
    
bidi_session
new_tab
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
"
about
:
about
"
wait
=
"
complete
"
    
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
"
1
+
1
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
False
    
)
    
assert
result
=
=
{
"
type
"
:
"
number
"
"
value
"
:
2
}
