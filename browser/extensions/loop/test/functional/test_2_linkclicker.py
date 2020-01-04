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
import
copy
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
from
config
import
CONTENT_SERVER_URL
class
Test2Linkclicker
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
        
standalone_url
=
CONTENT_SERVER_URL
+
"
/
"
        
prefs
=
copy
.
copy
(
FIREFOX_PREFERENCES
)
        
prefs
[
"
loop
.
linkClicker
.
url
"
]
=
standalone_url
        
self
.
marionette
.
set_prefs
(
prefs
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
navigate_to_standalone
(
self
url
)
:
        
self
.
switch_to_standalone
(
)
        
self
.
marionette
.
navigate
(
url
)
    
def
standalone_check_own_link_view
(
self
)
:
        
view_container
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
handle
-
user
-
agent
-
view
-
scroller
"
                                                         
30
)
        
self
.
assertEqual
(
view_container
.
tag_name
"
div
"
"
expect
a
error
container
"
)
    
def
local_leave_room
(
self
)
:
        
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
standalone_join_own_room
(
self
)
:
        
button
=
self
.
wait_for_element_displayed
(
By
.
CLASS_NAME
"
btn
-
info
"
30
)
        
button
.
click
(
)
    
def
standalone_check_error_text
(
self
)
:
        
error_container
=
self
.
wait_for_element_displayed
(
By
.
CLASS_NAME
                                                          
"
failure
"
                                                          
30
)
        
self
.
assertEqual
(
error_container
.
tag_name
"
p
"
"
expect
a
error
container
"
)
    
def
test_2_own_room_test
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
        
room_url
=
self
.
local_get_and_verify_room_url
(
)
        
self
.
local_leave_room
(
)
        
self
.
navigate_to_standalone
(
room_url
)
        
self
.
standalone_check_own_link_view
(
)
        
self
.
standalone_join_own_room
(
)
        
self
.
load_homepage
(
)
        
self
.
local_check_room_self_video
(
)
        
self
.
navigate_to_standalone
(
room_url
)
        
self
.
standalone_join_own_room
(
)
        
self
.
standalone_check_error_text
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
