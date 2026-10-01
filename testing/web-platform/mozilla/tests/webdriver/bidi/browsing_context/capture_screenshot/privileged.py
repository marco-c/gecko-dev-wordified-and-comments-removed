from
copy
import
deepcopy
import
pytest
from
tests
.
bidi
.
browsing_context
.
capture_screenshot
import
(
    
get_physical_element_dimensions
    
get_physical_viewport_dimensions
)
from
tests
.
support
.
image
import
png_dimensions
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
browsing_context
import
BoxOptions
ElementOptions
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
ABOUT_URL
=
"
about
:
about
"
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
test_capture_screenshot_in_parent_process_context_with_system_access
(
    
bidi_session
chrome_context
)
:
    
expected_size
=
await
get_physical_viewport_dimensions
(
bidi_session
chrome_context
)
    
data
=
await
bidi_session
.
browsing_context
.
capture_screenshot
(
        
context
=
chrome_context
[
"
context
"
]
    
)
    
assert
png_dimensions
(
data
)
=
=
pytest
.
approx
(
expected_size
abs
=
1
.
0
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
async
def
test_capture_screenshot_in_parent_process_context_supports_clip_type_box
(
    
bidi_session
chrome_context
)
:
    
expected_height
=
22
    
expected_width
=
33
    
data
=
await
bidi_session
.
browsing_context
.
capture_screenshot
(
        
context
=
chrome_context
[
"
context
"
]
        
clip
=
BoxOptions
(
            
x
=
10
            
y
=
10
            
width
=
expected_width
            
height
=
expected_height
        
)
    
)
    
assert
png_dimensions
(
data
)
=
=
(
expected_width
expected_height
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
async
def
test_capture_screenshot_in_parent_process_context_supports_clip_type_element
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
    
new_window
=
new_chrome_window
(
f
"
{
default_chrome_handler
}
test
.
xhtml
"
)
    
context
=
{
"
context
"
:
new_window
.
id
}
    
element
=
await
bidi_session
.
script
.
evaluate
(
        
await_promise
=
False
        
expression
=
"
document
.
querySelector
(
'
#
textInput
'
)
"
        
target
=
ContextTarget
(
context
[
"
context
"
]
)
    
)
    
expected_size
=
await
get_physical_element_dimensions
(
        
bidi_session
context
element
    
)
    
data
=
await
bidi_session
.
browsing_context
.
capture_screenshot
(
        
context
=
context
[
"
context
"
]
clip
=
ElementOptions
(
element
=
element
)
    
)
    
screenshot_size
=
png_dimensions
(
data
)
    
assert
screenshot_size
=
=
pytest
.
approx
(
expected_size
abs
=
1
.
0
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
async
def
test_capture_screenshot_in_parent_process_context_supports_origin_document
(
    
bidi_session
chrome_context
)
:
    
origin_document_data
=
await
bidi_session
.
browsing_context
.
capture_screenshot
(
        
context
=
chrome_context
[
"
context
"
]
origin
=
"
document
"
    
)
    
origin_viewport_data
=
await
bidi_session
.
browsing_context
.
capture_screenshot
(
        
context
=
chrome_context
[
"
context
"
]
origin
=
"
viewport
"
    
)
    
assert
png_dimensions
(
origin_document_data
)
=
=
png_dimensions
(
origin_viewport_data
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
async
def
test_capture_screenshot_in_privilegedabout_context_about_url_with_system_access
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
certificate
"
wait
=
"
complete
"
    
)
    
data
=
await
bidi_session
.
browsing_context
.
capture_screenshot
(
        
context
=
new_tab
[
"
context
"
]
    
)
    
(
actual_width
actual_height
)
=
png_dimensions
(
data
)
    
assert
actual_width
>
0
    
assert
actual_height
>
0
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
test_capture_screenshot_in_webextension_context_with_system_access
(
    
bidi_session
install_new_tab_extension
)
:
    
context_id
ext_url
=
install_new_tab_extension
    
data
=
await
bidi_session
.
browsing_context
.
capture_screenshot
(
context
=
context_id
)
    
(
actual_width
actual_height
)
=
png_dimensions
(
data
)
    
assert
actual_width
>
0
    
assert
actual_height
>
0
async
def
test_capture_screenshot_in_parent_process_context
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
browsing_context
.
capture_screenshot
(
context
=
context_id
)
async
def
test_capture_screenshot_in_privilegedabout_context
(
    
configuration
geckodriver
)
:
    
url
=
"
about
:
certificate
"
    
config
=
deepcopy
(
configuration
)
    
config
[
"
capabilities
"
]
[
"
moz
:
firefoxOptions
"
]
[
"
args
"
]
.
append
(
url
)
    
config
[
"
capabilities
"
]
[
"
moz
:
firefoxOptions
"
]
[
"
androidIntentArguments
"
]
=
[
        
"
-
d
"
        
url
    
]
    
config
[
"
capabilities
"
]
[
"
webSocketUrl
"
]
=
True
    
driver
=
geckodriver
(
config
=
config
force_new
=
True
)
    
try
:
        
driver
.
new_session
(
)
        
bidi_session
=
driver
.
session
.
bidi_session
        
await
bidi_session
.
start
(
)
        
contexts
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
)
        
page_context
=
next
(
(
ctx
for
ctx
in
contexts
if
ctx
[
"
url
"
]
=
=
url
)
None
)
        
assert
page_context
is
not
None
f
"
No
context
found
with
URL
{
url
}
"
        
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
browsing_context
.
capture_screenshot
(
                
context
=
page_context
[
"
context
"
]
            
)
    
finally
:
        
await
driver
.
stop
(
)
async
def
test_capture_screenshot_in_webextension_context
(
    
bidi_session
install_new_tab_extension
)
:
    
context_id
_
=
install_new_tab_extension
    
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
browsing_context
.
capture_screenshot
(
context
=
context_id
)
