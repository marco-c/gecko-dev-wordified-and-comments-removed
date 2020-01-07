#
coding
:
utf
-
8
from
__future__
import
absolute_import
division
print_function
import
os
as
_os
import
sys
as
_sys
import
warnings
as
_warnings
from
tempfile
import
mkdtemp
class
TemporaryDirectory
(
object
)
:
    
"
"
"
Create
and
return
a
temporary
directory
.
This
has
the
same
    
behavior
as
mkdtemp
but
can
be
used
as
a
context
manager
.
For
    
example
:
        
with
TemporaryDirectory
(
)
as
tmpdir
:
            
.
.
.
    
Upon
exiting
the
context
the
directory
and
everything
contained
    
in
it
are
removed
.
    
"
"
"
    
def
__init__
(
self
suffix
=
"
"
prefix
=
"
tmp
"
dir
=
None
)
:
        
self
.
_closed
=
False
        
self
.
name
=
None
        
self
.
name
=
mkdtemp
(
suffix
prefix
dir
)
    
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
cleanup
(
self
)
:
        
if
self
.
name
and
not
self
.
_closed
:
            
try
:
                
self
.
_rmtree
(
self
.
name
)
            
except
(
TypeError
AttributeError
)
as
ex
:
                
if
"
None
"
not
in
str
(
ex
)
:
                    
raise
                
print
(
"
ERROR
:
{
!
r
}
while
cleaning
up
{
!
r
}
"
.
format
(
ex
self
)
                      
file
=
_sys
.
stderr
)
                
return
            
self
.
_closed
=
True
    
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
__del__
(
self
)
:
        
self
.
cleanup
(
)
    
_listdir
=
staticmethod
(
_os
.
listdir
)
    
_path_join
=
staticmethod
(
_os
.
path
.
join
)
    
_isdir
=
staticmethod
(
_os
.
path
.
isdir
)
    
_islink
=
staticmethod
(
_os
.
path
.
islink
)
    
_remove
=
staticmethod
(
_os
.
remove
)
    
_rmdir
=
staticmethod
(
_os
.
rmdir
)
    
_warn
=
_warnings
.
warn
    
def
_rmtree
(
self
path
)
:
        
for
name
in
self
.
_listdir
(
path
)
:
            
fullname
=
self
.
_path_join
(
path
name
)
            
try
:
                
isdir
=
self
.
_isdir
(
fullname
)
and
not
self
.
_islink
(
fullname
)
            
except
OSError
:
                
isdir
=
False
            
if
isdir
:
                
self
.
_rmtree
(
fullname
)
            
else
:
                
try
:
                    
self
.
_remove
(
fullname
)
                
except
OSError
:
                    
pass
        
try
:
            
self
.
_rmdir
(
path
)
        
except
OSError
:
            
pass
