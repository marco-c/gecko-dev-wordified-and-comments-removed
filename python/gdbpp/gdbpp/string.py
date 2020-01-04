import
gdb
from
gdbpp
import
GeckoPrettyPrinter
GeckoPrettyPrinter
(
'
nsString
'
'
^
ns
.
*
String
'
)
class
string_printer
(
object
)
:
    
def
__init__
(
self
value
)
:
        
self
.
value
=
value
    
def
to_string
(
self
)
:
        
return
self
.
value
[
'
mData
'
]
    
def
display_hint
(
self
)
:
        
return
'
string
'
