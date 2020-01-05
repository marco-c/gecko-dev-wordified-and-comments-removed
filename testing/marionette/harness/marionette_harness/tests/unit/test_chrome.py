from
marionette_driver
import
By
from
marionette_harness
import
MarionetteTestCase
WindowManagerMixin
class
ChromeTests
(
WindowManagerMixin
MarionetteTestCase
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
ChromeTests
self
)
.
setUp
(
)
        
self
.
marionette
.
set_context
(
'
chrome
'
)
    
def
tearDown
(
self
)
:
        
self
.
close_all_windows
(
)
        
super
(
ChromeTests
self
)
.
tearDown
(
)
    
def
test_hang_until_timeout
(
self
)
:
        
def
open_with_menu
(
)
:
            
menu
=
self
.
marionette
.
find_element
(
By
.
ID
'
aboutName
'
)
            
menu
.
click
(
)
        
new_window
=
self
.
open_window
(
trigger
=
open_with_menu
)
        
self
.
marionette
.
switch_to_window
(
new_window
)
        
try
:
            
try
:
                
raise
NotImplementedError
(
'
Exception
should
not
cause
a
hang
when
'
                                          
'
closing
the
chrome
window
'
)
            
finally
:
                
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
self
.
start_window
)
        
except
NotImplementedError
:
            
pass
