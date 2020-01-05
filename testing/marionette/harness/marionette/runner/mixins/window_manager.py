import
sys
from
marionette_driver
import
By
Wait
class
WindowManagerMixin
(
object
)
:
    
_menu_item_new_tab
=
(
By
.
ID
"
menu_newNavigatorTab
"
)
    
def
setUp
(
self
)
:
        
super
(
WindowManagerMixin
self
)
.
setUp
(
)
        
self
.
start_tab
=
self
.
marionette
.
current_window_handle
        
self
.
start_tabs
=
self
.
marionette
.
window_handles
    
def
tearDown
(
self
)
:
        
try
:
            
if
len
(
self
.
marionette
.
window_handles
)
!
=
len
(
self
.
start_tabs
)
:
                
raise
Exception
(
"
Not
all
tabs
as
opened
by
the
test
have
been
closed
"
)
        
finally
:
            
super
(
WindowManagerMixin
self
)
.
tearDown
(
)
    
def
close_all_tabs
(
self
)
:
        
current_window_handles
=
self
.
marionette
.
window_handles
        
if
self
.
start_tab
not
in
current_window_handles
:
            
self
.
start_tab
=
current_window_handles
[
0
]
        
current_window_handles
.
remove
(
self
.
start_tab
)
        
for
handle
in
current_window_handles
:
            
self
.
marionette
.
switch_to_window
(
handle
)
            
self
.
marionette
.
close
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
handle
not
in
mn
.
window_handles
                
message
=
"
Failed
to
close
tab
with
handle
{
}
"
.
format
(
handle
)
            
)
        
self
.
marionette
.
switch_to_window
(
self
.
start_tab
)
    
def
open_tab
(
self
trigger
=
"
menu
"
)
:
        
current_tabs
=
self
.
marionette
.
window_handles
        
try
:
            
if
callable
(
trigger
)
:
                
trigger
(
)
            
elif
trigger
=
=
'
menu
'
:
                
with
self
.
marionette
.
using_context
(
"
chrome
"
)
:
                    
self
.
marionette
.
find_element
(
*
self
.
_menu_item_new_tab
)
.
click
(
)
        
except
Exception
:
            
exc
val
tb
=
sys
.
exc_info
(
)
            
raise
exc
'
Failed
to
trigger
opening
a
new
tab
:
{
}
'
.
format
(
val
)
tb
        
else
:
            
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
len
(
mn
.
window_handles
)
=
=
len
(
current_tabs
)
+
1
                
message
=
"
No
new
tab
has
been
opened
"
            
)
            
[
new_tab
]
=
list
(
set
(
self
.
marionette
.
window_handles
)
-
set
(
current_tabs
)
)
            
return
new_tab
