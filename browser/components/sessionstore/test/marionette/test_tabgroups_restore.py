import
os
import
sys
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
TestAutoRestoreWithTabGroups
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
TestAutoRestoreWithTabGroups
self
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
test_saved_groups_restored
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
            
let
group
=
gBrowser
.
addTabGroup
(
[
gBrowser
.
tabs
[
0
]
]
{
id
:
"
test
-
group
"
label
:
"
test
-
group
"
}
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
getAllTabGroups
(
)
.
length
"
)
            
1
            
"
There
is
one
open
group
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
getAllTabGroups
(
)
.
length
"
)
            
1
            
"
There
is
one
open
group
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
SessionStore
.
savedGroups
.
length
"
)
            
0
            
"
The
group
was
not
saved
because
it
was
automatically
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
            
let
group
=
gBrowser
.
getTabGroupById
(
"
test
-
group
"
)
;
            
group
.
ownerGlobal
.
SessionStore
.
addSavedTabGroup
(
group
)
;
            
group
.
ownerGlobal
.
gBrowser
.
removeTabGroup
(
group
{
animate
:
false
}
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
SessionStore
.
savedGroups
.
length
"
)
            
1
            
"
The
group
is
now
saved
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
getAllTabGroups
(
)
.
length
"
)
            
0
            
"
The
group
was
not
automatically
restored
because
it
was
manually
saved
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
SessionStore
.
savedGroups
.
length
"
)
            
1
            
"
The
saved
group
persists
after
a
second
restart
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
            
SessionStore
.
forgetSavedTabGroup
(
"
test
-
group
"
)
;
            
"
"
"
        
)
