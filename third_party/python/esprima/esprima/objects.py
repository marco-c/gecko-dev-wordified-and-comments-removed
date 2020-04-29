#
-
*
-
coding
:
utf
-
8
-
*
-
from
__future__
import
absolute_import
unicode_literals
def
toDict
(
value
)
:
    
from
.
visitor
import
ToDictVisitor
    
return
ToDictVisitor
(
)
.
visit
(
value
)
class
Array
(
list
)
:
    
pass
class
Object
(
object
)
:
    
def
toDict
(
self
)
:
        
from
.
visitor
import
ToDictVisitor
        
return
ToDictVisitor
(
)
.
visit
(
self
)
    
def
__repr__
(
self
)
:
        
from
.
visitor
import
ReprVisitor
        
return
ReprVisitor
(
)
.
visit
(
self
)
    
def
__getattr__
(
self
name
)
:
        
return
None
