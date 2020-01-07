from
__future__
import
absolute_import
class
BaseLib
(
object
)
:
    
"
"
"
A
base
class
that
handles
lazily
setting
the
"
client
"
class
attribute
.
"
"
"
    
def
__init__
(
self
marionette
)
:
        
self
.
_marionette
=
marionette
    
property
    
def
marionette
(
self
)
:
        
return
self
.
_marionette
