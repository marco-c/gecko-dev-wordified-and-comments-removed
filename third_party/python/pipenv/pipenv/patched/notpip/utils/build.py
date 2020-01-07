from
__future__
import
absolute_import
import
os
.
path
import
tempfile
from
pip9
.
utils
import
rmtree
class
BuildDirectory
(
object
)
:
    
def
__init__
(
self
name
=
None
delete
=
None
)
:
        
if
name
is
None
and
delete
is
None
:
            
delete
=
True
        
if
name
is
None
:
            
name
=
os
.
path
.
realpath
(
tempfile
.
mkdtemp
(
prefix
=
"
pip
-
build
-
"
)
)
            
if
delete
is
None
:
                
delete
=
True
        
self
.
name
=
name
        
self
.
delete
=
delete
    
def
__repr__
(
self
)
:
        
return
"
<
{
}
{
!
r
}
>
"
.
format
(
self
.
__class__
.
__name__
self
.
name
)
    
def
__enter__
(
self
)
:
        
return
self
.
name
    
def
__exit__
(
self
exc
value
tb
)
:
        
self
.
cleanup
(
)
    
def
cleanup
(
self
)
:
        
if
self
.
delete
:
            
rmtree
(
self
.
name
)
