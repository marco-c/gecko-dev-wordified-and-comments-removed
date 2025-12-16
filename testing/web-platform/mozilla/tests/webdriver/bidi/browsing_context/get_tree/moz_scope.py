import
pytest
from
tests
.
bidi
.
browsing_context
import
assert_browsing_context
from
webdriver
.
bidi
import
error
pytestmark
=
pytest
.
mark
.
asyncio
pytest
.
fixture
def
browser_chrome_url
(
current_session
)
:
    
if
current_session
.
capabilities
[
"
platformName
"
]
=
=
"
android
"
:
        
return
"
chrome
:
/
/
geckoview
/
content
/
geckoview
.
xhtml
"
    
else
:
        
return
"
chrome
:
/
/
browser
/
content
/
browser
.
xhtml
"
async
def
test_without_system_access
(
bidi_session
)
:
    
with
pytest
.
raises
(
error
.
UnsupportedOperationException
)
:
        
await
bidi_session
.
browsing_context
.
get_tree
(
            
_extension_params
=
{
"
moz
:
scope
"
:
"
chrome
"
}
        
)
pytest
.
mark
.
allow_system_access
async
def
test_multiple_browser_windows
(
    
bidi_session
new_window
top_context
browser_chrome_url
)
:
    
parent_contexts
=
await
bidi_session
.
browsing_context
.
get_tree
(
        
max_depth
=
0
_extension_params
=
{
"
moz
:
scope
"
:
"
chrome
"
}
    
)
    
assert
len
(
parent_contexts
)
=
=
2
    
assert_browsing_context
(
        
parent_contexts
[
0
]
        
None
        
children
=
None
        
parent
=
None
        
url
=
browser_chrome_url
        
client_window
=
top_context
[
"
clientWindow
"
]
    
)
    
assert
parent_contexts
[
0
]
[
"
context
"
]
!
=
top_context
[
"
context
"
]
    
assert
parent_contexts
[
0
]
[
"
moz
:
scope
"
]
=
=
"
chrome
"
    
assert_browsing_context
(
        
parent_contexts
[
1
]
        
None
        
children
=
None
        
parent
=
None
        
url
=
browser_chrome_url
        
client_window
=
new_window
[
"
clientWindow
"
]
    
)
    
assert
parent_contexts
[
1
]
[
"
context
"
]
!
=
new_window
[
"
context
"
]
    
assert
parent_contexts
[
1
]
[
"
clientWindow
"
]
!
=
top_context
[
"
clientWindow
"
]
    
assert
parent_contexts
[
1
]
[
"
moz
:
scope
"
]
=
=
"
chrome
"
    
assert
parent_contexts
[
0
]
[
"
context
"
]
!
=
parent_contexts
[
1
]
[
"
context
"
]
pytest
.
mark
.
allow_system_access
async
def
test_custom_chrome_window_without_iframes
(
    
bidi_session
top_context
default_chrome_handler
new_chrome_window
)
:
    
if
bidi_session
.
capabilities
[
"
platformName
"
]
=
=
"
android
"
:
        
return
    
chrome_url
=
f
"
{
default_chrome_handler
}
test_dialog
.
xhtml
"
    
new_window
=
new_chrome_window
(
chrome_url
)
    
parent_contexts
=
await
bidi_session
.
browsing_context
.
get_tree
(
        
root
=
new_window
.
id
_extension_params
=
{
"
moz
:
scope
"
:
"
chrome
"
}
    
)
    
assert
len
(
parent_contexts
)
=
=
1
    
assert_browsing_context
(
        
parent_contexts
[
0
]
        
None
        
children
=
0
        
parent
=
None
        
url
=
chrome_url
        
client_window
=
None
    
)
    
assert
len
(
parent_contexts
)
=
=
1
    
assert
parent_contexts
[
0
]
[
"
clientWindow
"
]
!
=
top_context
[
"
clientWindow
"
]
    
assert
parent_contexts
[
0
]
[
"
moz
:
scope
"
]
=
=
"
chrome
"
    
assert
parent_contexts
[
0
]
[
"
moz
:
name
"
]
=
=
"
null
"
pytest
.
mark
.
allow_system_access
async
def
test_custom_chrome_window_with_iframes
(
    
bidi_session
top_context
default_chrome_handler
new_chrome_window
)
:
    
if
bidi_session
.
capabilities
[
"
platformName
"
]
=
=
"
android
"
:
        
return
    
chrome_url
=
f
"
{
default_chrome_handler
}
test
.
xhtml
"
    
iframe_url
=
f
"
{
default_chrome_handler
}
test_iframe
.
xhtml
"
    
nested_iframe_url
=
f
"
{
default_chrome_handler
}
test_nested_iframe
.
xhtml
"
    
new_window
=
new_chrome_window
(
chrome_url
)
    
parent_contexts
=
await
bidi_session
.
browsing_context
.
get_tree
(
        
root
=
new_window
.
id
_extension_params
=
{
"
moz
:
scope
"
:
"
chrome
"
}
    
)
    
assert_browsing_context
(
        
parent_contexts
[
0
]
        
None
        
children
=
2
        
parent
=
None
        
url
=
chrome_url
        
client_window
=
None
    
)
    
assert
parent_contexts
[
0
]
[
"
clientWindow
"
]
!
=
top_context
[
"
clientWindow
"
]
    
assert
parent_contexts
[
0
]
[
"
moz
:
scope
"
]
=
=
"
chrome
"
    
assert
parent_contexts
[
0
]
[
"
moz
:
name
"
]
=
=
"
null
"
    
iframes
=
parent_contexts
[
0
]
[
"
children
"
]
    
assert_browsing_context
(
        
iframes
[
0
]
        
None
        
children
=
0
        
parent_expected
=
False
        
url
=
iframe_url
        
client_window
=
parent_contexts
[
0
]
[
"
clientWindow
"
]
    
)
    
assert
iframes
[
0
]
[
"
context
"
]
!
=
parent_contexts
[
0
]
[
"
context
"
]
    
assert
iframes
[
0
]
[
"
moz
:
scope
"
]
=
=
"
chrome
"
    
assert
iframes
[
0
]
[
"
moz
:
name
"
]
=
=
"
iframe
"
    
assert_browsing_context
(
        
iframes
[
1
]
        
None
        
children
=
1
        
parent_expected
=
False
        
url
=
nested_iframe_url
        
client_window
=
parent_contexts
[
0
]
[
"
clientWindow
"
]
    
)
    
assert
iframes
[
1
]
[
"
context
"
]
!
=
parent_contexts
[
0
]
[
"
context
"
]
    
assert
iframes
[
1
]
[
"
context
"
]
!
=
iframes
[
0
]
[
"
context
"
]
    
assert
iframes
[
1
]
[
"
moz
:
scope
"
]
=
=
"
chrome
"
    
assert
iframes
[
1
]
[
"
moz
:
name
"
]
=
=
"
iframe
-
nested
"
    
nested_iframes
=
iframes
[
1
]
[
"
children
"
]
    
assert_browsing_context
(
        
nested_iframes
[
0
]
        
None
        
children
=
0
        
parent_expected
=
False
        
url
=
iframe_url
        
client_window
=
parent_contexts
[
0
]
[
"
clientWindow
"
]
    
)
    
assert
iframes
[
1
]
[
"
context
"
]
!
=
parent_contexts
[
0
]
[
"
context
"
]
    
assert
iframes
[
1
]
[
"
context
"
]
!
=
iframes
[
0
]
[
"
context
"
]
    
assert
nested_iframes
[
0
]
[
"
context
"
]
!
=
iframes
[
1
]
[
"
context
"
]
    
assert
nested_iframes
[
0
]
[
"
context
"
]
!
=
parent_contexts
[
0
]
[
"
context
"
]
    
assert
nested_iframes
[
0
]
[
"
moz
:
scope
"
]
=
=
"
chrome
"
    
assert
nested_iframes
[
0
]
[
"
moz
:
name
"
]
=
=
"
iframe
"
