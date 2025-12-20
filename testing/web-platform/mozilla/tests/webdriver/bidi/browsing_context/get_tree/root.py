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
async
def
test_custom_chrome_window
(
    
bidi_session
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
    
top_level_contexts
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
max_depth
=
1
    
)
    
assert
len
(
top_level_contexts
)
=
=
1
    
assert_browsing_context
(
        
top_level_contexts
[
0
]
        
new_window
.
id
        
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
    
iframes
=
top_level_contexts
[
0
]
[
"
children
"
]
    
iframe_contexts
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
iframes
[
1
]
[
"
context
"
]
    
)
    
assert
len
(
iframe_contexts
)
=
=
1
    
assert_browsing_context
(
        
iframe_contexts
[
0
]
        
iframes
[
1
]
[
"
context
"
]
        
children
=
1
        
parent
=
top_level_contexts
[
0
]
[
"
context
"
]
        
url
=
nested_iframe_url
        
client_window
=
top_level_contexts
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
iframe_contexts
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
top_level_contexts
[
0
]
[
"
context
"
]
    
assert
iframe_contexts
[
0
]
[
"
context
"
]
=
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
iframe_contexts
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
iframe_contexts
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
-
nested
"
    
nested_iframes
=
iframe_contexts
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
top_level_contexts
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
top_level_contexts
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
top_level_contexts
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
