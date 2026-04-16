import
os
import
sys
import
unittest
from
urllib
.
parse
import
quote
sys
.
path
.
append
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
from
session_store_test_case
import
SessionStoreTestCase
def
inline
(
doc
)
:
    
return
f
"
data
:
text
/
html
;
charset
=
utf
-
8
{
quote
(
doc
)
}
"
DEFAULT_WINDOWS
=
set
(
[
    
(
inline
(
"
"
"
<
div
"
>
Lorem
<
/
div
>
"
"
"
)
inline
(
"
"
"
<
div
"
>
Ipsum
<
/
div
>
"
"
"
)
)
]
)
class
TestAutoRestoreWithSplitView
(
SessionStoreTestCase
)
:
    
def
setUp
(
self
)
:
        
super
(
)
.
setUp
(
            
startup_page
=
3
            
include_private
=
False
            
restore_on_demand
=
True
            
test_windows
=
DEFAULT_WINDOWS
        
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
test_splitview_restored_after_quit
(
self
)
:
        
self
.
wait_for_windows
(
            
self
.
all_windows
"
Not
all
requested
windows
have
been
opened
"
        
)
        
self
.
marionette
.
execute_async_script
(
            
"
"
"
            
let
resolve
=
arguments
[
0
]
;
            
gBrowser
.
addTabSplitView
(
[
gBrowser
.
tabs
[
0
]
gBrowser
.
tabs
[
1
]
]
)
;
            
let
{
TabStateFlusher
}
=
ChromeUtils
.
importESModule
(
"
resource
:
/
/
/
modules
/
sessionstore
/
TabStateFlusher
.
sys
.
mjs
"
)
;
            
TabStateFlusher
.
flushWindow
(
gBrowser
.
ownerGlobal
)
.
then
(
resolve
)
;
            
"
"
"
        
)
        
self
.
assertEqual
(
            
self
.
marionette
.
execute_script
(
                
"
return
gBrowser
.
tabs
[
0
]
.
splitview
.
tabs
.
length
"
            
)
            
2
            
"
There
is
a
splitview
with
two
tabs
"
        
)
        
self
.
marionette
.
quit
(
)
        
self
.
marionette
.
start_session
(
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
        
self
.
assertEqual
(
            
self
.
marionette
.
execute_script
(
                
"
return
gBrowser
.
tabs
[
0
]
.
splitview
.
tabs
.
length
"
            
)
            
2
            
"
Splitview
with
two
tabs
restored
"
        
)
    
unittest
.
skipIf
(
        
sys
.
platform
.
startswith
(
"
darwin
"
)
        
"
macOS
does
not
close
Firefox
when
the
last
window
closes
"
    
)
    
def
test_splitview_restored_after_closing_last_window
(
self
)
:
        
self
.
wait_for_windows
(
            
self
.
all_windows
"
Not
all
requested
windows
have
been
opened
"
        
)
        
self
.
marionette
.
execute_async_script
(
            
"
"
"
            
let
resolve
=
arguments
[
0
]
;
            
gBrowser
.
addTabSplitView
(
[
gBrowser
.
tabs
[
0
]
gBrowser
.
tabs
[
1
]
]
)
;
            
let
{
TabStateFlusher
}
=
ChromeUtils
.
importESModule
(
"
resource
:
/
/
/
modules
/
sessionstore
/
TabStateFlusher
.
sys
.
mjs
"
)
;
            
TabStateFlusher
.
flushWindow
(
gBrowser
.
ownerGlobal
)
.
then
(
resolve
)
;
            
"
"
"
        
)
        
self
.
assertEqual
(
            
self
.
marionette
.
execute_script
(
                
"
return
gBrowser
.
tabs
[
0
]
.
splitview
.
tabs
.
length
"
            
)
            
2
            
"
There
is
a
splitview
with
two
tabs
"
        
)
        
self
.
marionette
.
quit
(
callback
=
self
.
_close_window
)
        
self
.
marionette
.
start_session
(
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
        
self
.
assertEqual
(
            
self
.
marionette
.
execute_script
(
                
"
return
gBrowser
.
tabs
[
0
]
.
splitview
.
tabs
.
length
"
            
)
            
2
            
"
Splitview
with
two
tabs
restored
"
        
)
