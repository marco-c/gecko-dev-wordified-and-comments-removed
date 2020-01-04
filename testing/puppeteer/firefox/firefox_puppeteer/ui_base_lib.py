from
marionette_driver
.
marionette
import
HTMLElement
from
firefox_puppeteer
.
base
import
BaseLib
from
firefox_puppeteer
.
ui
.
windows
import
BaseWindow
class
UIBaseLib
(
BaseLib
)
:
    
"
"
"
A
base
class
for
all
UI
element
wrapper
classes
inside
a
chrome
window
.
"
"
"
    
def
__init__
(
self
marionette_getter
window
element
)
:
        
assert
isinstance
(
window
BaseWindow
)
        
assert
isinstance
(
element
HTMLElement
)
        
BaseLib
.
__init__
(
self
marionette_getter
)
        
self
.
_window
=
window
        
self
.
_element
=
element
    
property
    
def
element
(
self
)
:
        
"
"
"
Returns
the
reference
to
the
underlying
DOM
element
.
        
:
returns
:
Reference
to
the
DOM
element
        
"
"
"
        
return
self
.
_element
    
property
    
def
window
(
self
)
:
        
"
"
"
Returns
the
reference
to
the
chrome
window
.
        
:
returns
:
:
class
:
BaseWindow
instance
of
the
chrome
window
.
        
"
"
"
        
return
self
.
_window
