import
os
import
sys
from
marionette_driver
import
By
from
marionette_driver
.
errors
import
(
    
InvalidArgumentException
    
NoSuchElementException
    
UnknownException
)
from
marionette_driver
.
localization
import
L10n
from
marionette_harness
import
MarionetteTestCase
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
chrome_handler_mixin
import
ChromeHandlerMixin
class
TestL10n
(
ChromeHandlerMixin
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
TestL10n
self
)
.
setUp
(
)
        
self
.
l10n
=
L10n
(
self
.
marionette
)
    
def
test_localize_property
(
self
)
:
        
properties
=
[
self
.
chrome_base_url
+
"
test_dialog
.
properties
"
]
        
value
=
self
.
l10n
.
localize_property
(
properties
"
testDialog
.
title
"
)
        
self
.
assertEqual
(
value
"
Test
Dialog
"
)
        
self
.
assertRaises
(
            
NoSuchElementException
            
self
.
l10n
.
localize_property
            
properties
            
"
notExistent
"
        
)
    
def
test_localize_property_invalid_arguments
(
self
)
:
        
properties
=
[
"
chrome
:
/
/
global
/
locale
/
filepicker
.
properties
"
]
        
self
.
assertRaises
(
            
NoSuchElementException
            
self
.
l10n
.
localize_property
            
properties
            
"
notExistent
"
        
)
        
self
.
assertRaises
(
            
InvalidArgumentException
            
self
.
l10n
.
localize_property
            
properties
[
0
]
            
"
notExistent
"
        
)
        
self
.
assertRaises
(
            
InvalidArgumentException
self
.
l10n
.
localize_property
properties
True
        
)
