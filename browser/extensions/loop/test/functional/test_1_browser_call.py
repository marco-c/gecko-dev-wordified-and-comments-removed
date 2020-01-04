from
marionette_driver
.
by
import
By
from
marionette_driver
.
addons
import
Addons
from
marionette
import
MarionetteTestCase
import
os
import
sys
sys
.
path
.
insert
(
1
os
.
path
.
dirname
(
os
.
path
.
abspath
(
__file__
)
)
)
from
serversetup
import
LoopTestServers
from
config
import
FIREFOX_PREFERENCES
from
loopTestDriver
import
LoopTestDriver
class
Test1BrowserCall
(
LoopTestDriver
MarionetteTestCase
)
:
    
def
setUp
(
self
)
:
        
self
.
loop_test_servers
=
LoopTestServers
(
)
        
MarionetteTestCase
.
setUp
(
self
)
        
LoopTestDriver
.
setUp
(
self
self
.
marionette
)
        
self
.
marionette
.
set_prefs
(
FIREFOX_PREFERENCES
)
        
xpi_file
=
os
.
environ
.
get
(
"
LOOP_XPI_FILE
"
)
        
if
xpi_file
:
            
addons
=
Addons
(
self
.
marionette
)
            
addons
.
install
(
os
.
path
.
abspath
(
xpi_file
)
)
        
self
.
e10s_enabled
=
os
.
environ
.
get
(
"
TEST_E10S
"
)
=
=
"
1
"
        
self
.
marionette
.
restart
(
in_app
=
True
)
        
self
.
marionette
.
set_context
(
"
chrome
"
)
    
def
standalone_check_remote_video
(
self
)
:
        
self
.
switch_to_standalone
(
)
        
self
.
check_video
(
"
.
remote
-
video
"
)
    
def
local_check_remote_video
(
self
)
:
        
self
.
switch_to_chatbox
(
)
        
self
.
check_video
(
"
.
remote
-
video
"
)
    
def
send_chat_message
(
self
text
)
:
        
"
"
"
        
Sends
a
chat
message
using
the
current
context
.
        
:
param
text
:
The
text
to
send
.
        
"
"
"
        
chatbox
=
self
.
wait_for_element_displayed
(
By
.
CSS_SELECTOR
                                                  
"
.
text
-
chat
-
box
>
form
>
input
"
)
        
chatbox
.
send_keys
(
text
+
"
\
n
"
)
    
def
check_received_message
(
self
expectedText
)
:
        
"
"
"
        
Checks
a
chat
message
has
been
received
in
the
current
context
.
The
        
test
assumes
only
one
chat
message
will
be
received
during
the
tests
.
        
:
param
expectedText
:
The
expected
text
of
the
chat
message
.
        
"
"
"
        
text_entry
=
self
.
wait_for_element_displayed
(
By
.
CSS_SELECTOR
                                                     
"
.
text
-
chat
-
entry
.
received
>
p
"
)
        
self
.
assertEqual
(
text_entry
.
text
expectedText
                         
"
should
have
received
the
correct
message
"
)
    
def
check_text_messaging
(
self
)
:
        
"
"
"
        
Checks
text
messaging
between
the
generator
and
clicker
in
a
bi
-
directional
        
fashion
.
        
"
"
"
        
self
.
switch_to_chatbox
(
)
        
self
.
send_chat_message
(
"
test1
"
)
        
self
.
switch_to_standalone
(
)
        
self
.
check_received_message
(
"
test1
"
)
        
self
.
send_chat_message
(
"
test2
"
)
        
self
.
switch_to_chatbox
(
)
        
self
.
check_received_message
(
"
test2
"
)
    
def
standalone_check_remote_screenshare
(
self
)
:
        
self
.
switch_to_standalone
(
)
        
self
.
check_video
(
"
.
screen
-
share
-
video
"
)
    
def
remote_leave_room
(
self
)
:
        
self
.
switch_to_standalone
(
)
        
button
=
self
.
marionette
.
find_element
(
By
.
CLASS_NAME
"
btn
-
hangup
"
)
        
button
.
click
(
)
        
self
.
switch_to_chatbox
(
)
        
self
.
wait_for_element_displayed
(
By
.
CLASS_NAME
"
room
-
invitation
-
content
"
)
    
def
local_leave_room
(
self
)
:
        
button
=
self
.
marionette
.
find_element
(
By
.
CLASS_NAME
"
stop
-
sharing
-
button
"
)
        
button
.
click
(
)
    
def
local_get_chatbox_window_expr
(
self
expr
)
:
        
"
"
"
        
:
expr
:
a
sub
-
expression
which
must
begin
with
a
property
of
the
        
global
content
window
(
e
.
g
.
"
location
.
path
"
)
        
:
return
:
the
value
of
the
given
sub
-
expression
as
evaluated
in
the
        
chatbox
content
window
        
"
"
"
        
self
.
marionette
.
set_context
(
"
chrome
"
)
        
self
.
marionette
.
switch_to_frame
(
)
        
chatbox
=
self
.
wait_for_element_exists
(
By
.
TAG_NAME
'
chatbox
'
)
        
script
=
'
'
'
            
let
chatBrowser
=
document
.
getAnonymousElementByAttribute
(
              
arguments
[
0
]
'
anonid
'
              
'
content
'
)
            
/
/
note
that
using
wrappedJSObject
waives
X
-
ray
vision
which
            
/
/
has
security
implications
but
because
we
trust
the
code
            
/
/
running
in
the
chatbox
it
should
be
reasonably
safe
            
let
chatGlobal
=
chatBrowser
.
contentWindow
.
wrappedJSObject
;
            
return
chatGlobal
.
'
'
'
+
expr
        
return
self
.
marionette
.
execute_script
(
script
[
chatbox
]
)
    
def
local_close_conversation
(
self
)
:
        
self
.
marionette
.
set_context
(
"
chrome
"
)
        
self
.
marionette
.
switch_to_frame
(
)
        
chatbox
=
self
.
wait_for_element_exists
(
By
.
TAG_NAME
'
chatbox
'
)
        
close_button
=
chatbox
.
find_element
(
By
.
ANON_ATTRIBUTE
{
"
class
"
:
"
chat
-
loop
-
hangup
chat
-
toolbarbutton
"
}
)
        
close_button
.
click
(
)
    
def
check_feedback_form
(
self
)
:
        
self
.
switch_to_chatbox
(
)
        
feedbackPanel
=
self
.
wait_for_element_displayed
(
By
.
CSS_SELECTOR
"
.
feedback
-
view
-
container
"
)
        
self
.
assertNotEqual
(
feedbackPanel
"
"
)
    
def
check_rename_layout
(
self
)
:
        
self
.
switch_to_panel
(
)
        
renameInput
=
self
.
wait_for_element_displayed
(
By
.
CSS_SELECTOR
"
.
rename
-
input
"
)
        
self
.
assertNotEqual
(
renameInput
"
"
)
    
def
test_1_browser_call
(
self
)
:
        
self
.
load_homepage
(
)
        
self
.
open_panel
(
)
        
self
.
switch_to_panel
(
)
        
self
.
local_start_a_conversation
(
)
        
self
.
local_close_share_panel
(
)
        
self
.
local_check_room_self_video
(
)
        
room_url
=
self
.
local_get_and_verify_room_url
(
)
        
self
.
standalone_load_and_join_room
(
room_url
)
        
self
.
standalone_check_remote_video
(
)
        
self
.
local_check_remote_video
(
)
        
self
.
check_text_messaging
(
)
        
self
.
standalone_check_remote_screenshare
(
)
        
self
.
remote_leave_room
(
)
        
self
.
local_close_conversation
(
)
        
self
.
check_feedback_form
(
)
        
self
.
local_close_conversation
(
)
        
self
.
check_rename_layout
(
)
    
def
tearDown
(
self
)
:
        
self
.
loop_test_servers
.
shutdown
(
)
        
MarionetteTestCase
.
tearDown
(
self
)
