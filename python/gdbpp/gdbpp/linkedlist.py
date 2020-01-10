from
__future__
import
absolute_import
from
gdbpp
import
GeckoPrettyPrinter
GeckoPrettyPrinter
(
'
mozilla
:
:
LinkedList
'
'
^
mozilla
:
:
LinkedList
<
.
*
>
'
)
class
linkedlist_printer
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
        
self
.
t_ptr_type
=
value
.
type
.
template_argument
(
0
)
.
pointer
(
)
    
def
children
(
self
)
:
        
sentinel
=
self
.
value
[
'
sentinel
'
]
        
pSentinel
=
sentinel
.
address
        
pNext
=
sentinel
[
'
mNext
'
]
        
i
=
0
        
while
pSentinel
!
=
pNext
:
            
list_elem
=
pNext
.
dereference
(
)
            
list_value
=
pNext
.
cast
(
self
.
t_ptr_type
)
            
yield
(
'
%
d
'
%
i
list_value
)
            
pNext
=
list_elem
[
'
mNext
'
]
            
i
+
=
1
    
def
to_string
(
self
)
:
        
return
str
(
self
.
value
.
type
)
    
def
display_hint
(
self
)
:
        
return
'
array
'
