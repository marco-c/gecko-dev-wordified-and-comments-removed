import
os
import
sys
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
title
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
<
html
>
<
head
>
<
title
>
{
title
}
<
/
title
>
<
/
head
>
<
body
>
<
/
body
>
<
/
html
>
"
class
TestTaskbarTabSessionState
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
1
            
include_private
=
False
            
restore_on_demand
=
False
            
taskbartabs_enable
=
True
            
test_windows
=
set
(
[
                
(
                    
inline
(
"
lorem
ipsom
"
)
                    
inline
(
"
dolor
"
)
                
)
            
]
)
        
)
    
"
"
"
    
Close
all
Firefox
windows
with
the
web
app
being
closed
last
    
the
session
store
state
should
include
the
last
regular
window
    
that
'
s
closed
but
not
the
web
app
    
"
"
"
    
def
test_taskbartab_session_state
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
enforce_gecko_prefs
(
{
"
browser
.
taskbarTabs
.
enabled
"
:
True
}
)
        
self
.
open_taskbartab_window
(
)
        
taskbar_tab_window_handle
=
self
.
marionette
.
close_chrome_window
(
)
[
0
]
        
self
.
marionette
.
switch_to_window
(
taskbar_tab_window_handle
)
        
self
.
marionette
.
set_context
(
"
content
"
)
        
dummy_html
=
self
.
marionette
.
absolute_url
(
"
empty
.
html
"
)
        
self
.
marionette
.
navigate
(
dummy_html
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
"
"
                
const
{
_LastSession
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
SessionStore
.
sys
.
mjs
"
                    
)
;
                
return
_LastSession
.
getState
(
)
.
windows
.
length
            
"
"
"
            
)
            
1
            
"
One
window
should
be
in
the
session
state
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
"
"
                
const
{
_LastSession
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
SessionStore
.
sys
.
mjs
"
                    
)
;
                
return
_LastSession
.
getState
(
)
.
windows
[
0
]
.
tabs
.
length
            
"
"
"
            
)
            
2
            
"
Two
tabs
should
be
in
the
session
state
"
        
)
