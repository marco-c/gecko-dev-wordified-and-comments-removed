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
marionette_driver
import
Wait
errors
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
.
format
(
        
title
    
)
class
TestSessionRestoreClosedTabs
(
SessionStoreTestCase
)
:
    
"
"
"
    
Test
that
closed
tabs
persist
between
sessions
and
    
that
any
previously
open
tabs
are
added
to
the
recently
    
closed
tab
list
.
When
a
previous
session
is
restored
    
an
open
tab
is
restored
and
removed
from
the
closed
tabs
list
.
    
If
additional
tabs
are
opened
(
and
closed
)
before
a
previous
    
session
is
restored
those
should
be
merged
with
the
restored
open
    
and
closed
tabs
preserving
their
state
.
    
"
"
"
    
def
setUp
(
self
)
:
        
super
(
TestSessionRestoreClosedTabs
self
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
    
def
test_restore
(
self
)
:
        
self
.
marionette
.
execute_script
(
            
"
"
"
            
Services
.
prefs
.
setBoolPref
(
"
browser
.
sessionstore
.
persist_closed_tabs_between_sessions
"
true
)
;
            
"
"
"
        
)
        
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
            
let
tab
=
gBrowser
.
tabs
[
1
]
;
            
gBrowser
.
removeTab
(
tab
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
flush
(
tab
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
            
let
{
SessionStore
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
            
let
state
=
JSON
.
parse
(
SessionStore
.
getBrowserState
(
)
)
;
            
return
state
.
windows
[
0
]
.
_closedTabs
.
length
;
            
"
"
"
            
)
            
2
            
msg
=
"
Should
have
2
closed
tabs
after
restart
.
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
            
let
{
SessionStore
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
            
let
state
=
JSON
.
parse
(
SessionStore
.
getBrowserState
(
)
)
;
            
return
state
.
windows
[
0
]
.
_closedTabs
[
0
]
.
removeAfterRestore
;
            
"
"
"
            
)
            
True
            
msg
=
"
Previously
open
tab
that
was
added
to
closedTabs
should
have
removeAfterRestore
property
.
"
        
)
        
win
=
self
.
marionette
.
current_chrome_window_handle
        
self
.
open_tabs
(
win
(
inline
(
"
sit
"
)
inline
(
"
amet
"
)
)
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
                
return
gBrowser
.
tabs
[
0
]
.
label
                
"
"
"
            
)
            
"
sit
"
            
msg
=
"
First
open
tab
should
now
be
sit
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
                
return
gBrowser
.
tabs
[
1
]
.
label
                
"
"
"
            
)
            
"
amet
"
            
msg
=
"
Second
open
tab
should
be
amet
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
                
return
gBrowser
.
tabs
.
length
                
"
"
"
            
)
            
2
            
msg
=
"
should
have
2
tabs
open
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
            
let
tab
=
gBrowser
.
tabs
[
1
]
;
            
gBrowser
.
removeTab
(
tab
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
flush
(
tab
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
wait_for_tabcount
(
1
"
Waiting
for
1
tabs
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
lazy
=
{
}
;
                
ChromeUtils
.
defineESModuleGetters
(
lazy
{
                    
SessionStore
:
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
                
}
)
;
                
function
observeClosedTabsChange
(
)
{
                    
return
new
Promise
(
resolve
=
>
{
                        
function
observe
(
subject
topic
data
)
{
                            
if
(
topic
=
=
"
sessionstore
-
closed
-
objects
-
changed
"
)
{
                                
Services
.
obs
.
removeObserver
(
this
"
sessionstore
-
closed
-
objects
-
changed
"
)
;
                                
resolve
(
'
observed
closed
objects
changed
'
)
;
                            
}
;
                        
}
                        
Services
.
obs
.
addObserver
(
observe
"
sessionstore
-
closed
-
objects
-
changed
"
)
;
                    
}
)
;
                
}
;
                
async
function
checkForClosedTabs
(
)
{
                    
let
closedTabsObserver
=
observeClosedTabsChange
(
)
;
                    
lazy
.
SessionStore
.
restoreLastSession
(
)
;
                    
await
closedTabsObserver
;
                    
let
state
=
JSON
.
parse
(
lazy
.
SessionStore
.
getBrowserState
(
)
)
;
                    
return
state
.
windows
[
0
]
.
_closedTabs
.
length
;
                
}
                
return
checkForClosedTabs
(
)
;
                
"
"
"
            
)
            
2
            
msg
=
"
Should
have
2
closed
tab
after
restoring
session
.
"
        
)
        
self
.
wait_for_tabcount
(
2
"
Waiting
for
2
tabs
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
                
return
gBrowser
.
tabs
[
0
]
.
label
                
"
"
"
            
)
            
"
sit
"
            
msg
=
"
Newly
opened
tab
should
still
exist
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
                
return
gBrowser
.
tabs
[
1
]
.
label
                
"
"
"
            
)
            
"
lorem
ipsom
"
            
msg
=
"
The
open
tab
from
the
previous
session
should
be
restored
"
        
)
        
self
.
marionette
.
execute_script
(
            
"
"
"
            
Services
.
prefs
.
clearUserPref
(
"
browser
.
sessionstore
.
persist_closed_tabs_between_sessions
"
)
;
            
"
"
"
        
)
    
def
wait_for_tabcount
(
self
expected_tabcount
message
timeout
=
5
)
:
        
current_tabcount
=
None
        
def
check
(
_
)
:
            
nonlocal
current_tabcount
            
current_tabcount
=
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
.
length
;
"
            
)
            
return
current_tabcount
=
=
expected_tabcount
        
try
:
            
wait
=
Wait
(
self
.
marionette
timeout
=
timeout
interval
=
0
.
1
)
            
wait
.
until
(
check
message
=
message
)
        
except
errors
.
TimeoutException
as
e
:
            
message
=
(
                
f
"
{
e
.
message
}
.
Expected
{
expected_tabcount
}
got
{
current_tabcount
}
.
"
            
)
            
raise
errors
.
TimeoutException
(
message
)
