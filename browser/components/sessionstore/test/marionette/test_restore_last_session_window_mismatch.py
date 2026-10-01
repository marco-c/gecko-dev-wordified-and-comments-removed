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
inline
POPUP_FEATURES
=
"
chrome
dialog
=
no
resizable
toolbar
=
no
"
class
PopupWindowMismatchTestMixin
:
    
"
"
"
    
Bug
2065228
:
restoreLastSession
(
)
reuses
the
current
top
window
for
the
    
first
window
of
the
saved
session
whenever
that
window
isn
'
t
tied
to
a
    
__SS_lastSessionWindowID
.
    
A
window
'
s
popup
-
ness
is
fixed
by
the
toolbar
native
chrome
flag
at
    
creation
time
and
can
'
t
be
changed
afterwards
so
reusing
a
mismatched
    
window
can
never
actually
make
it
look
like
the
restored
session
'
s
window
.
    
Restoring
the
last
session
with
a
saved
window
whose
popup
-
ness
doesn
'
t
    
match
the
current
top
window
should
therefore
open
a
new
window
instead
of
    
reusing
it
leaving
the
top
window
untouched
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
            
test_windows
=
set
(
)
        
)
class
TestRestoreLastSessionPopupIntoNormalWindow
(
    
PopupWindowMismatchTestMixin
SessionStoreTestCase
)
:
    
def
test_restore_last_session_popup_opens_new_window_instead_of_reusing_normal_top_window
(
        
self
    
)
:
        
self
.
replace_current_window
(
features
=
POPUP_FEATURES
)
        
self
.
open_tabs
(
            
self
.
marionette
.
current_chrome_window_handle
(
inline
(
"
popup
tab
"
)
)
        
)
        
self
.
assertTrue
(
            
self
.
is_current_window_popup
(
)
            
msg
=
"
Window
should
be
a
genuine
popup
before
quitting
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
        
startup_window
=
self
.
marionette
.
current_chrome_window_handle
        
self
.
assertFalse
(
            
self
.
is_current_window_popup
(
)
            
msg
=
"
Startup
window
should
be
a
normal
(
non
-
popup
)
window
"
        
)
        
startup_urls_before
=
self
.
get_urls_for_window
(
startup_window
)
        
self
.
restore_last_session
(
)
        
handles
=
self
.
marionette
.
chrome_window_handles
        
self
.
assertEqual
(
            
len
(
handles
)
            
2
            
msg
=
"
Restoring
a
popup
from
last
session
should
open
a
new
window
"
            
"
instead
of
reusing
the
mismatched
normal
startup
window
"
        
)
        
self
.
marionette
.
switch_to_window
(
startup_window
)
        
self
.
assertEqual
(
            
self
.
get_urls_for_window
(
startup_window
)
            
startup_urls_before
            
msg
=
"
Startup
window
'
s
tabs
should
be
untouched
by
the
restore
"
        
)
        
self
.
assertFalse
(
            
self
.
is_current_window_popup
(
)
            
msg
=
"
Startup
window
should
remain
normal
not
be
turned
into
a
popup
"
        
)
        
[
new_window
]
=
[
h
for
h
in
handles
if
h
!
=
startup_window
]
        
self
.
marionette
.
switch_to_window
(
new_window
)
        
self
.
assertTrue
(
            
self
.
is_current_window_popup
(
)
            
msg
=
"
New
window
should
be
created
as
a
popup
to
match
the
restored
session
"
        
)
        
self
.
assertIn
(
            
inline
(
"
popup
tab
"
)
            
self
.
get_urls_for_window
(
new_window
)
            
msg
=
"
New
window
should
contain
the
restored
popup
'
s
tab
"
        
)
class
TestRestoreLastSessionNormalIntoPopupWindow
(
    
PopupWindowMismatchTestMixin
SessionStoreTestCase
)
:
    
def
test_restore_last_session_normal_window_opens_new_window_instead_of_reusing_popup_top_window
(
        
self
    
)
:
        
normal_window
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
normal_window
(
inline
(
"
normal
tab
"
)
)
)
        
self
.
assertFalse
(
            
self
.
is_current_window_popup
(
)
            
msg
=
"
Window
should
be
a
normal
(
non
-
popup
)
window
before
quitting
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
replace_current_window
(
features
=
POPUP_FEATURES
)
        
popup_top_window
=
self
.
marionette
.
current_chrome_window_handle
        
self
.
assertTrue
(
            
self
.
is_current_window_popup
(
)
            
msg
=
"
Top
window
at
restore
time
should
be
a
genuine
popup
"
        
)
        
popup_urls_before
=
self
.
get_urls_for_window
(
popup_top_window
)
        
self
.
restore_last_session
(
)
        
handles
=
self
.
marionette
.
chrome_window_handles
        
self
.
assertEqual
(
            
len
(
handles
)
            
2
            
msg
=
"
Restoring
a
normal
window
from
last
session
should
open
a
"
            
"
new
window
instead
of
reusing
the
mismatched
popup
top
window
"
        
)
        
self
.
marionette
.
switch_to_window
(
popup_top_window
)
        
self
.
assertEqual
(
            
self
.
get_urls_for_window
(
popup_top_window
)
            
popup_urls_before
            
msg
=
"
Popup
top
window
'
s
tabs
should
be
untouched
by
the
restore
"
        
)
        
self
.
assertTrue
(
            
self
.
is_current_window_popup
(
)
            
msg
=
"
Popup
top
window
should
remain
a
popup
not
be
turned
into
a
normal
window
"
        
)
        
[
new_window
]
=
[
h
for
h
in
handles
if
h
!
=
popup_top_window
]
        
self
.
marionette
.
switch_to_window
(
new_window
)
        
self
.
assertFalse
(
            
self
.
is_current_window_popup
(
)
            
msg
=
"
New
window
should
be
created
as
normal
to
match
the
restored
session
"
        
)
        
self
.
assertIn
(
            
inline
(
"
normal
tab
"
)
            
self
.
get_urls_for_window
(
new_window
)
            
msg
=
"
New
window
should
contain
the
restored
normal
window
'
s
tab
"
        
)
class
TestPrivateWindowSessionRestore
(
SessionStoreTestCase
)
:
    
"
"
"
    
Bug
829568
:
Don
'
t
restore
the
last
session
into
an
open
private
window
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
            
test_windows
=
set
(
)
        
)
    
def
test_restore_last_session_normal_window_opens_new_window_instead_of_reusing_private_top_window
(
        
self
    
)
:
        
normal_window
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
normal_window
(
inline
(
"
normal
tab
"
)
)
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
        
private_window
=
self
.
open_window
(
private
=
True
)
        
self
.
marionette
.
close_chrome_window
(
)
        
self
.
marionette
.
switch_to_window
(
private_window
)
        
private_urls_before
=
self
.
get_urls_for_window
(
private_window
)
        
self
.
restore_last_session
(
)
        
handles
=
self
.
marionette
.
chrome_window_handles
        
self
.
assertEqual
(
            
len
(
handles
)
            
2
            
msg
=
"
Restoring
a
normal
window
from
the
last
session
should
open
"
            
"
a
new
window
instead
of
reusing
the
mismatched
private
top
window
"
        
)
        
self
.
marionette
.
switch_to_window
(
private_window
)
        
self
.
assertEqual
(
            
self
.
get_urls_for_window
(
private_window
)
            
private_urls_before
            
msg
=
"
Private
top
window
'
s
tabs
should
be
untouched
by
the
restore
"
        
)
        
[
new_window
]
=
[
h
for
h
in
handles
if
h
!
=
private_window
]
        
self
.
marionette
.
switch_to_window
(
new_window
)
        
self
.
assertFalse
(
            
self
.
is_current_window_popup
(
)
            
msg
=
"
New
window
should
be
created
as
normal
to
match
the
restored
session
"
        
)
        
self
.
assertIn
(
            
inline
(
"
normal
tab
"
)
            
self
.
get_urls_for_window
(
new_window
)
            
msg
=
"
New
window
should
contain
the
restored
normal
window
'
s
tab
"
        
)
class
TestTaskbarTabWindowSessionRestore
(
SessionStoreTestCase
)
:
    
"
"
"
    
Bug
1915738
:
Don
'
t
restore
last
session
into
an
open
taskbar
tab
window
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
            
test_windows
=
set
(
)
        
)
    
def
test_restore_last_session_normal_window_opens_new_window_instead_of_reusing_taskbar_tab_top_window
(
        
self
    
)
:
        
normal_window
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
normal_window
(
inline
(
"
normal
tab
"
)
)
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
open_taskbartab_window
(
)
        
taskbartab_window
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
taskbartab_window
)
        
self
.
assertTrue
(
            
self
.
marionette
.
execute_script
(
                
"
return
document
.
documentElement
.
hasAttribute
(
'
taskbartab
'
)
;
"
            
)
            
msg
=
"
Top
window
at
restore
time
should
be
a
genuine
taskbar
tab
window
"
        
)
        
taskbartab_urls_before
=
self
.
get_urls_for_window
(
taskbartab_window
)
        
self
.
restore_last_session
(
)
        
handles
=
self
.
marionette
.
chrome_window_handles
        
self
.
assertEqual
(
            
len
(
handles
)
            
2
            
msg
=
"
Restoring
a
normal
window
from
last
session
should
open
a
new
"
            
"
window
instead
of
reusing
the
mismatched
taskbar
tab
top
window
"
        
)
        
self
.
marionette
.
switch_to_window
(
taskbartab_window
)
        
self
.
assertEqual
(
            
self
.
get_urls_for_window
(
taskbartab_window
)
            
taskbartab_urls_before
            
msg
=
"
Taskbar
tab
top
window
'
s
tabs
should
be
untouched
by
the
restore
"
        
)
        
[
new_window
]
=
[
h
for
h
in
handles
if
h
!
=
taskbartab_window
]
        
self
.
marionette
.
switch_to_window
(
new_window
)
        
self
.
assertFalse
(
            
self
.
is_current_window_popup
(
)
            
msg
=
"
New
window
should
be
created
as
normal
to
match
the
restored
session
"
        
)
        
self
.
assertIn
(
            
inline
(
"
normal
tab
"
)
            
self
.
get_urls_for_window
(
new_window
)
            
msg
=
"
New
window
should
contain
the
restored
normal
window
'
s
tab
"
        
)
