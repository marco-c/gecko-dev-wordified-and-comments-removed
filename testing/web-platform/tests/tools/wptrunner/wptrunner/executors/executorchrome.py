import
collections
import
copy
import
json
import
os
import
re
import
time
import
uuid
from
typing
import
Any
Mapping
MutableMapping
Optional
from
webdriver
import
error
from
.
base
import
strip_server
from
.
executorwebdriver
import
(
    
WebDriverBaseProtocolPart
    
WebDriverCrashtestExecutor
    
WebDriverAccessibilityProtocolPart
    
WebDriverFedCMProtocolPart
    
WebDriverPrintRefTestExecutor
    
WebDriverProtocol
    
WebDriverBidiProtocol
    
WebDriverRefTestExecutor
    
WebDriverTestDriverProtocolPart
    
WebDriverTestharnessExecutor
    
WebDriverTestharnessProtocolPart
)
from
.
protocol
import
LeakProtocolPart
ProtocolPart
here
=
os
.
path
.
dirname
(
__file__
)
AXNode
=
Mapping
[
str
Any
]
def
_update_capabilities_if_extension_test
(
    
browser
:
Any
capabilities
:
Optional
[
MutableMapping
[
str
Any
]
]
)
-
>
Optional
[
MutableMapping
[
str
Any
]
]
:
    
"
"
"
Updates
ChromeDriver
capabilities
if
the
browser
is
running
an
extension
test
.
"
"
"
    
if
getattr
(
browser
"
is_extension_test
"
False
)
:
        
if
capabilities
is
None
:
            
capabilities
=
{
}
        
else
:
            
capabilities
=
copy
.
deepcopy
(
capabilities
)
        
chrome_options
=
capabilities
.
setdefault
(
"
goog
:
chromeOptions
"
{
}
)
        
args
=
chrome_options
.
setdefault
(
"
args
"
[
]
)
        
def
add_arg
(
arg
:
str
)
-
>
None
:
            
if
arg
not
in
args
:
                
args
.
append
(
arg
)
        
add_arg
(
"
-
-
enable
-
features
=
ExtensionBrowserNamespaceOnWebPages
"
)
        
add_arg
(
"
-
-
extension
-
test
-
api
-
on
-
web
-
pages
"
)
        
add_arg
(
"
-
-
extension
-
test
-
api
-
standardized
-
behavior
"
)
    
return
capabilities
class
ChromeDriverBaseProtocolPart
(
WebDriverBaseProtocolPart
)
:
    
def
create_window
(
self
type
=
"
tab
"
*
*
kwargs
)
:
        
try
:
            
return
super
(
)
.
create_window
(
type
=
type
*
*
kwargs
)
        
except
error
.
WebDriverException
:
            
window_id
=
str
(
uuid
.
uuid4
(
)
)
            
self
.
webdriver
.
execute_script
(
                
"
window
.
open
(
'
about
:
blank
'
'
%
s
'
'
noopener
'
)
"
%
window_id
)
            
return
self
.
_get_test_window
(
window_id
self
.
current_window
)
    
def
_get_test_window
(
self
window_id
parent
timeout
=
5
)
:
        
"
"
"
Find
the
test
window
amongst
all
the
open
windows
.
        
This
is
assumed
to
be
either
the
named
window
or
the
one
after
the
parent
in
the
list
of
        
window
handles
        
:
param
window_id
:
The
DOM
name
of
the
Window
        
:
param
parent
:
The
handle
of
the
current
window
        
:
param
timeout
:
The
time
in
seconds
to
wait
for
the
window
to
appear
.
This
is
because
in
                        
some
implementations
there
'
s
a
race
between
calling
window
.
open
and
the
                        
window
being
added
to
the
list
of
WebDriver
accessible
windows
.
"
"
"
        
test_window
=
None
        
end_time
=
time
.
time
(
)
+
timeout
        
while
time
.
time
(
)
<
end_time
:
            
try
:
                
win_s
=
self
.
webdriver
.
execute_script
(
"
return
window
[
'
%
s
'
]
;
"
%
window_id
)
                
win_obj
=
json
.
loads
(
win_s
)
                
test_window
=
win_obj
[
"
window
-
fcc6
-
11e5
-
b4f8
-
330a88ab9d7f
"
]
            
except
Exception
:
                
pass
            
if
test_window
is
None
:
                
test_window
=
self
.
_poll_handles_for_test_window
(
parent
)
            
if
test_window
is
not
None
:
                
assert
test_window
!
=
parent
                
return
test_window
            
time
.
sleep
(
0
.
1
)
        
raise
Exception
(
"
unable
to
find
test
window
"
)
    
def
_poll_handles_for_test_window
(
self
parent
)
:
        
test_window
=
None
        
after
=
self
.
webdriver
.
handles
        
if
len
(
after
)
=
=
2
:
            
test_window
=
next
(
iter
(
set
(
after
)
-
{
parent
}
)
)
        
elif
after
[
0
]
=
=
parent
and
len
(
after
)
>
2
:
            
test_window
=
after
[
1
]
        
return
test_window
class
ChromeDriverLeakProtocolPart
(
LeakProtocolPart
)
:
    
def
get_counters
(
self
)
-
>
Mapping
[
str
int
]
:
        
response
=
self
.
parent
.
cdp
.
execute_cdp_command
(
"
Memory
.
getDOMCountersForLeakDetection
"
)
        
counters
:
MutableMapping
[
str
int
]
=
collections
.
Counter
(
{
            
counter
[
"
name
"
]
:
counter
[
"
count
"
]
            
for
counter
in
response
[
"
counters
"
]
        
}
)
        
counters
[
"
live_resources
"
]
-
=
counters
.
pop
(
"
live_ua_css_resources
"
0
)
        
return
counters
class
ChromeDriverTestDriverProtocolPart
(
WebDriverTestDriverProtocolPart
)
:
    
"
"
"
An
interface
to
the
browser
-
side
testdriver
infrastructure
that
lazily
settles
calls
.
"
"
"
    
def
setup
(
self
)
:
        
super
(
)
.
setup
(
)
        
self
.
_pending_message
=
"
"
    
def
send_message
(
self
cmd_id
message_type
status
message
=
None
)
:
        
message_script
=
self
.
_format_send_message_script
(
cmd_id
message_type
status
message
)
        
if
message_type
=
=
"
complete
"
:
            
assert
not
self
.
_pending_message
self
.
_pending_message
            
self
.
_pending_message
=
message_script
        
else
:
            
self
.
webdriver
.
execute_script
(
message_script
)
    
def
_get_next_message_classic
(
self
url
script_resume
)
:
        
try
:
            
message_script
self
.
_pending_message
=
self
.
_pending_message
"
"
            
return
self
.
parent
.
base
.
execute_script
(
message_script
+
script_resume
                                                   
asynchronous
=
True
                                                   
args
=
[
strip_server
(
url
)
]
)
        
except
error
.
JavascriptErrorException
as
js_error
:
            
if
re
.
search
(
r
'
window
\
.
__wptrunner_process_next_event
is
not
a
function
'
                         
js_error
.
message
)
:
                
time
.
sleep
(
0
.
05
)
                
return
None
            
raise
class
ChromeDriverTestharnessProtocolPart
(
WebDriverTestharnessProtocolPart
)
:
    
"
"
"
Implementation
of
testharness
.
js
tests
controlled
by
ChromeDriver
.
    
The
main
difference
from
the
default
WebDriver
testharness
implementation
is
    
that
the
test
window
can
be
reused
between
tests
for
better
performance
.
    
"
"
"
    
def
reset_browser_state
(
self
)
:
        
for
command
params
in
[
            
(
"
Browser
.
resetPermissions
"
None
)
            
(
"
Browser
.
setPermission
"
{
                
"
permission
"
:
{
"
name
"
:
"
background
-
sync
"
}
                
"
setting
"
:
"
granted
"
            
}
)
        
]
:
            
try
:
                
self
.
parent
.
cdp
.
execute_cdp_command
(
command
params
)
            
except
error
.
WebDriverException
:
                
pass
class
ChromeDriverFedCMProtocolPart
(
WebDriverFedCMProtocolPart
)
:
    
def
confirm_idp_login
(
self
)
:
        
return
self
.
webdriver
.
send_session_command
(
"
POST
"
                                                   
f
"
{
self
.
parent
.
vendor_prefix
}
/
fedcm
/
confirmidplogin
"
)
class
ChromeDriverAccessibilityProtocolPart
(
WebDriverAccessibilityProtocolPart
)
:
    
def
setup
(
self
)
:
        
super
(
)
.
setup
(
)
        
self
.
_nodes_by_id
=
{
}
    
def
teardown
(
self
)
:
        
try
:
            
self
.
parent
.
cdp
.
execute_cdp_command
(
"
Accessibility
.
disable
"
)
        
except
error
.
WebDriverException
:
            
pass
    
def
get_accessibility_properties_for_element
(
self
element
)
:
        
node
=
self
.
_get_ax_node_for_element
(
element
)
        
return
self
.
_serialize_node
(
node
)
if
node
else
{
}
    
def
get_accessibility_properties_for_accessibility_node
(
self
id
)
:
        
node
=
self
.
_find_ax_node_by_ax_node_id
(
id
)
        
return
self
.
_serialize_node
(
node
)
if
node
else
{
}
    
def
_get_full_ax_tree
(
self
)
-
>
Mapping
[
str
AXNode
]
:
        
self
.
parent
.
cdp
.
execute_cdp_command
(
"
Accessibility
.
enable
"
)
        
node_array
=
self
.
parent
.
cdp
.
execute_cdp_command
(
            
"
Accessibility
.
getFullAXTree
"
            
{
}
        
)
.
get
(
"
nodes
"
[
]
)
        
return
{
node
[
"
nodeId
"
]
:
node
for
node
in
node_array
}
    
def
_find_ax_node_by_ax_node_id
(
self
ax_node_id
:
str
)
-
>
Optional
[
AXNode
]
:
        
full_ax_tree
=
self
.
_get_full_ax_tree
(
)
        
node
=
full_ax_tree
.
get
(
ax_node_id
None
)
        
return
node
    
def
_get_ax_node_for_element
(
self
element
:
Any
)
-
>
Optional
[
AXNode
]
:
        
parsed_ids
=
self
.
_extract_chromedriver_ids
(
element
.
id
)
        
if
parsed_ids
and
parsed_ids
.
get
(
"
element
"
)
:
            
return
self
.
_get_ax_node_by_backend_node_id
(
parsed_ids
[
"
element
"
]
)
        
return
None
    
def
_get_ax_node_by_backend_node_id
(
self
backend_node_id
:
str
)
-
>
Optional
[
AXNode
]
:
        
"
"
"
Shared
CDP
call
to
fetch
an
accessibility
node
by
its
backend
ID
.
"
"
"
        
ax_tree
=
self
.
parent
.
cdp
.
execute_cdp_command
(
            
"
Accessibility
.
getPartialAXTree
"
            
{
                
"
backendNodeId
"
:
int
(
backend_node_id
)
                
"
fetchRelatives
"
:
False
            
}
        
)
        
nodes
:
list
[
AXNode
]
=
ax_tree
.
get
(
"
nodes
"
[
]
)
        
return
nodes
[
0
]
if
nodes
else
None
    
def
_serialize_node
(
self
node
:
AXNode
)
-
>
Mapping
[
str
Any
]
:
        
rv
:
dict
[
str
Any
]
=
{
            
"
accessibilityId
"
:
node
[
"
nodeId
"
]
            
"
children
"
:
node
.
get
(
"
childIds
"
[
]
)
        
}
        
if
"
parentId
"
in
node
:
            
rv
[
"
parent
"
]
=
node
[
"
parentId
"
]
        
if
"
role
"
in
node
:
            
rv
[
"
role
"
]
=
node
[
"
role
"
]
.
get
(
"
value
"
)
        
if
"
name
"
in
node
:
            
rv
[
"
label
"
]
=
node
[
"
name
"
]
.
get
(
"
value
"
)
        
if
"
value
"
in
node
:
            
rv
[
"
value
"
]
=
node
[
"
value
"
]
.
get
(
"
value
"
)
        
if
"
description
"
in
node
:
            
rv
[
"
description
"
]
=
node
[
"
description
"
]
.
get
(
"
value
"
)
        
allowed_properties
=
{
'
checked
'
'
pressed
'
'
level
'
                              
'
multiline
'
'
orientation
'
'
required
'
                              
'
roledescription
'
'
selected
'
}
        
for
prop
in
node
.
get
(
"
properties
"
[
]
)
:
            
if
prop
[
"
name
"
]
in
allowed_properties
:
                
rv
[
prop
[
"
name
"
]
]
=
prop
[
"
value
"
]
.
get
(
"
value
"
)
        
return
rv
    
staticmethod
    
def
_extract_chromedriver_ids
(
element_id_string
:
str
)
-
>
Optional
[
Mapping
[
str
str
]
]
:
        
"
"
"
        
Extracts
Frame
Document
and
Element
IDs
from
a
ChromeDriver
id
.
        
Expected
format
:
f
.
[
hash
]
.
d
.
[
hash
]
.
e
.
[
id
]
        
"
"
"
        
pattern
=
r
"
^
f
\
.
(
?
P
<
frame
>
[
^
.
]
+
)
\
.
d
\
.
(
?
P
<
document
>
[
^
.
]
+
)
\
.
e
\
.
(
?
P
<
element
>
.
+
)
"
        
match
=
re
.
match
(
pattern
element_id_string
)
        
return
match
.
groupdict
(
)
if
match
else
None
class
ChromeDriverDevToolsProtocolPart
(
ProtocolPart
)
:
    
"
"
"
A
low
-
level
API
for
sending
Chrome
DevTools
Protocol
[
0
]
commands
directly
to
the
browser
.
    
Prefer
using
standard
APIs
where
possible
.
    
[
0
]
:
https
:
/
/
chromedevtools
.
github
.
io
/
devtools
-
protocol
/
    
"
"
"
    
name
=
"
cdp
"
    
def
setup
(
self
)
:
        
self
.
webdriver
=
self
.
parent
.
webdriver
    
def
execute_cdp_command
(
self
command
params
=
None
)
:
        
body
=
{
"
cmd
"
:
command
"
params
"
:
params
or
{
}
}
        
return
self
.
webdriver
.
send_session_command
(
"
POST
"
                                                   
f
"
{
self
.
parent
.
vendor_prefix
}
/
cdp
/
execute
"
                                                   
body
=
body
)
class
ChromeDriverTracingProtocolPart
(
ProtocolPart
)
:
    
name
=
"
tracing
"
    
def
setup
(
self
)
:
        
self
.
webdriver
=
self
.
parent
.
webdriver
    
def
get_trace
(
self
)
:
        
"
"
"
Retrieve
trace
events
accumulated
by
ChromeDriver
.
        
This
also
clears
ChromeDriver
'
s
internal
buffer
of
logged
events
.
        
Returns
:
            
JSON
in
the
trace
array
format
[
0
]
.
        
[
0
]
:
https
:
/
/
docs
.
google
.
com
/
document
/
d
/
1CvAClvFfyA5R
-
PhYUmn5OOQtYMH4h6I0nSsKchNAySU
/
preview
?
tab
=
t
.
0
#
heading
=
h
.
f2f0yd51wi15
        
"
"
"
        
perf_data
=
self
.
webdriver
.
send_session_command
(
"
POST
"
"
se
/
log
"
{
            
"
type
"
:
"
performance
"
        
}
)
        
events
=
[
]
        
for
entry
in
perf_data
:
            
data_collected_event
=
json
.
loads
(
entry
[
"
message
"
]
)
.
get
(
"
message
"
{
}
)
            
if
data_collected_event
.
get
(
"
method
"
)
!
=
"
Tracing
.
dataCollected
"
:
                
continue
            
if
trace_event
:
=
data_collected_event
.
get
(
"
params
"
)
:
                
events
.
append
(
trace_event
)
        
return
events
class
ChromeDriverProtocol
(
WebDriverProtocol
)
:
    
implements
=
[
        
ChromeDriverAccessibilityProtocolPart
        
ChromeDriverBaseProtocolPart
        
ChromeDriverDevToolsProtocolPart
        
ChromeDriverFedCMProtocolPart
        
ChromeDriverTestDriverProtocolPart
        
ChromeDriverTestharnessProtocolPart
        
ChromeDriverTracingProtocolPart
    
]
    
for
base_part
in
WebDriverProtocol
.
implements
:
        
if
base_part
.
name
not
in
{
part
.
name
for
part
in
implements
}
:
            
implements
.
append
(
base_part
)
    
vendor_prefix
=
"
goog
"
    
def
__init__
(
self
executor
browser
capabilities
*
*
kwargs
)
:
        
self
.
implements
=
list
(
ChromeDriverProtocol
.
implements
)
        
if
getattr
(
browser
"
leak_check
"
False
)
:
            
self
.
implements
.
append
(
ChromeDriverLeakProtocolPart
)
        
capabilities
=
_update_capabilities_if_extension_test
(
            
browser
capabilities
)
        
super
(
)
.
__init__
(
executor
browser
capabilities
*
*
kwargs
)
class
ChromeDriverBidiProtocol
(
WebDriverBidiProtocol
)
:
    
implements
=
[
        
ChromeDriverAccessibilityProtocolPart
        
ChromeDriverBaseProtocolPart
        
ChromeDriverDevToolsProtocolPart
        
ChromeDriverFedCMProtocolPart
        
ChromeDriverTestharnessProtocolPart
        
ChromeDriverTracingProtocolPart
    
]
    
for
base_part
in
WebDriverBidiProtocol
.
implements
:
        
if
base_part
.
name
not
in
{
part
.
name
for
part
in
implements
}
:
            
implements
.
append
(
base_part
)
    
vendor_prefix
=
"
goog
"
    
def
__init__
(
self
executor
browser
capabilities
*
*
kwargs
)
:
        
self
.
implements
=
list
(
ChromeDriverBidiProtocol
.
implements
)
        
if
getattr
(
browser
"
leak_check
"
False
)
:
            
self
.
implements
.
append
(
ChromeDriverLeakProtocolPart
)
        
capabilities
=
_update_capabilities_if_extension_test
(
            
browser
capabilities
)
        
super
(
)
.
__init__
(
executor
browser
capabilities
*
*
kwargs
)
def
_evaluate_sanitized_result
(
executor_cls
)
:
    
if
hasattr
(
executor_cls
"
base_convert_result
"
)
:
        
return
executor_cls
    
executor_cls
.
base_convert_result
=
executor_cls
.
convert_result
    
def
convert_result
(
self
test
result
*
*
kwargs
)
:
        
test_result
subtest_results
=
self
.
base_convert_result
(
test
result
*
*
kwargs
)
        
if
test_result
.
extra
.
get
(
"
leak_counters
"
)
:
            
test_result
=
test
.
make_result
(
"
CRASH
"
                                           
test_result
.
message
                                           
test_result
.
expected
                                           
test_result
.
extra
                                           
test_result
.
stack
                                           
test_result
.
known_intermittent
)
        
if
self
.
sanitizer_enabled
:
            
if
test_result
.
status
in
{
"
ERROR
"
"
FAIL
"
"
INTERNAL
-
ERROR
"
"
PRECONDITION_FAILED
"
}
:
                
test_result
.
status
=
test_result
.
default_expected
            
return
test_result
[
]
        
return
test_result
subtest_results
    
executor_cls
.
convert_result
=
convert_result
    
return
executor_cls
_evaluate_sanitized_result
class
ChromeDriverCrashTestExecutor
(
WebDriverCrashtestExecutor
)
:
    
protocol_cls
=
ChromeDriverProtocol
    
def
__init__
(
self
*
args
sanitizer_enabled
=
False
enable_tracing
=
False
*
*
kwargs
)
:
        
super
(
)
.
__init__
(
*
args
*
*
kwargs
)
        
self
.
sanitizer_enabled
=
sanitizer_enabled
        
self
.
enable_tracing
=
enable_tracing
    
def
do_test
(
self
test
)
:
        
file_result
subtest_results
=
super
(
)
.
do_test
(
test
)
        
if
self
.
enable_tracing
:
            
file_result
.
extra
[
"
trace
"
]
=
self
.
protocol
.
tracing
.
get_trace
(
)
        
return
file_result
subtest_results
_evaluate_sanitized_result
class
ChromeDriverRefTestExecutor
(
WebDriverRefTestExecutor
)
:
    
protocol_cls
=
ChromeDriverProtocol
    
def
__init__
(
self
*
args
sanitizer_enabled
=
False
enable_tracing
=
False
*
*
kwargs
)
:
        
super
(
)
.
__init__
(
*
args
*
*
kwargs
)
        
self
.
sanitizer_enabled
=
sanitizer_enabled
        
self
.
enable_tracing
=
enable_tracing
    
def
do_test
(
self
test
)
:
        
file_result
subtest_results
=
super
(
)
.
do_test
(
test
)
        
if
self
.
enable_tracing
:
            
file_result
.
extra
[
"
trace
"
]
=
self
.
protocol
.
tracing
.
get_trace
(
)
        
return
file_result
subtest_results
_evaluate_sanitized_result
class
ChromeDriverTestharnessExecutor
(
WebDriverTestharnessExecutor
)
:
    
def
__init__
(
self
*
args
sanitizer_enabled
=
False
enable_tracing
=
False
reuse_window
=
False
                 
*
*
kwargs
)
:
        
require_webdriver_bidi
=
kwargs
.
get
(
"
browser_settings
"
{
}
)
.
get
(
            
"
require_webdriver_bidi
"
None
)
        
if
require_webdriver_bidi
:
            
self
.
protocol_cls
=
ChromeDriverBidiProtocol
        
else
:
            
self
.
protocol_cls
=
ChromeDriverProtocol
        
super
(
)
.
__init__
(
*
args
*
*
kwargs
)
        
self
.
sanitizer_enabled
=
sanitizer_enabled
        
self
.
enable_tracing
=
enable_tracing
        
self
.
reuse_window
=
reuse_window
    
def
create_test_window
(
self
protocol
)
:
        
test_window
=
self
.
protocol
.
testharness
.
persistent_test_window
        
if
test_window
:
            
try
:
                
protocol
.
base
.
set_window
(
test_window
)
                
protocol
.
base
.
load
(
"
about
:
blank
"
)
                
protocol
.
cdp
.
execute_cdp_command
(
"
Page
.
resetNavigationHistory
"
)
            
except
error
.
WebDriverException
:
                
protocol
.
testharness
.
close_windows
(
[
test_window
]
)
                
protocol
.
base
.
set_window
(
protocol
.
testharness
.
runner_handle
)
                
test_window
=
self
.
protocol
.
testharness
.
persistent_test_window
=
None
        
if
not
test_window
:
            
test_window
=
super
(
)
.
create_test_window
(
protocol
)
            
if
self
.
reuse_window
:
                
self
.
logger
.
info
(
f
"
Created
new
test
window
{
test_window
}
"
)
        
if
self
.
reuse_window
:
            
self
.
protocol
.
testharness
.
persistent_test_window
=
test_window
        
return
test_window
    
def
do_test
(
self
test
)
:
        
file_result
subtest_results
=
super
(
)
.
do_test
(
test
)
        
if
self
.
enable_tracing
:
            
file_result
.
extra
[
"
trace
"
]
=
self
.
protocol
.
tracing
.
get_trace
(
)
        
return
file_result
subtest_results
_evaluate_sanitized_result
class
ChromeDriverPrintRefTestExecutor
(
WebDriverPrintRefTestExecutor
)
:
    
protocol_cls
=
ChromeDriverProtocol
    
def
__init__
(
self
*
args
sanitizer_enabled
=
False
enable_tracing
=
False
*
*
kwargs
)
:
        
super
(
)
.
__init__
(
*
args
*
*
kwargs
)
        
self
.
sanitizer_enabled
=
sanitizer_enabled
        
self
.
enable_tracing
=
enable_tracing
    
def
do_test
(
self
test
)
:
        
file_result
subtest_results
=
super
(
)
.
do_test
(
test
)
        
if
self
.
enable_tracing
:
            
file_result
.
extra
[
"
trace
"
]
=
self
.
protocol
.
tracing
.
get_trace
(
)
        
return
file_result
subtest_results
