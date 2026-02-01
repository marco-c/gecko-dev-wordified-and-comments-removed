import
os
import
sys
from
marionette_driver
import
Wait
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
TestManualRestoreWithTaskbarTabs
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
regular
windows
except
for
a
taskbar
tab
window
.
The
    
session
should
be
over
at
this
point
.
Opening
another
regular
Firefox
    
window
will
open
"
restore
previous
session
"
in
the
hamburger
menu
.
    
And
clicking
it
will
restore
the
correct
session
.
    
"
"
"
    
def
test_restore_without_closing_taskbartab
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
setup_taskbartab_restore_scenario
(
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
newWindow
=
BrowserWindowTracker
.
getTopWindow
(
{
allowTaskbarTabs
:
false
}
)
;
                
return
PanelMultiView
.
getViewNode
(
                    
newWindow
.
document
                    
"
appMenu
-
restoreSession
"
                
)
.
hasAttribute
(
"
disabled
"
)
;
            
"
"
"
            
)
            
False
            
"
The
restore
last
session
button
should
be
visible
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
restoreLastSession
(
)
;
            
"
"
"
        
)
        
Wait
(
self
.
marionette
)
.
until
(
            
lambda
mn
:
mn
.
execute_script
(
                
"
"
"
                
let
newWindow
=
BrowserWindowTracker
.
getTopWindow
(
{
allowTaskbarTabs
:
false
}
)
;
                
return
newWindow
.
gBrowser
.
tabs
.
length
;
                
"
"
"
            
)
            
=
=
2
        
)
class
TestAutoRestoreWithTaskbarTabs
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
regular
windows
except
for
a
taskbar
tab
window
.
The
    
session
should
be
over
at
this
point
.
Opening
another
regular
Firefox
    
window
will
open
automatically
restore
the
correct
session
    
"
"
"
    
def
test_restore_without_closing_taskbartab
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
setup_taskbartab_restore_scenario
(
)
        
Wait
(
self
.
marionette
)
.
until
(
            
lambda
mn
:
mn
.
execute_script
(
                
"
"
"
                
let
newWindow
=
BrowserWindowTracker
.
getTopWindow
(
{
allowTaskbarTabs
:
false
}
)
;
                
return
newWindow
.
gBrowser
.
tabs
.
length
;
                
"
"
"
            
)
            
=
=
3
        
)
