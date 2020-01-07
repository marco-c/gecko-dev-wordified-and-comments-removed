from
__future__
import
absolute_import
division
print_function
import
platform
import
sys
import
types
import
warnings
PY2
=
sys
.
version_info
[
0
]
=
=
2
PYPY
=
platform
.
python_implementation
(
)
=
=
"
PyPy
"
if
PYPY
or
sys
.
version_info
[
:
2
]
>
=
(
3
6
)
:
    
ordered_dict
=
dict
else
:
    
from
collections
import
OrderedDict
    
ordered_dict
=
OrderedDict
if
PY2
:
    
from
UserDict
import
IterableUserDict
    
def
isclass
(
klass
)
:
        
return
isinstance
(
klass
(
type
types
.
ClassType
)
)
    
TYPE
=
"
type
"
    
def
iteritems
(
d
)
:
        
return
d
.
iteritems
(
)
    
class
ReadOnlyDict
(
IterableUserDict
)
:
        
"
"
"
        
Best
-
effort
read
-
only
dict
wrapper
.
        
"
"
"
        
def
__setitem__
(
self
key
val
)
:
            
raise
TypeError
(
"
'
mappingproxy
'
object
does
not
support
item
"
                            
"
assignment
"
)
        
def
update
(
self
_
)
:
            
raise
AttributeError
(
"
'
mappingproxy
'
object
has
no
attribute
"
                                 
"
'
update
'
"
)
        
def
__delitem__
(
self
_
)
:
            
raise
TypeError
(
"
'
mappingproxy
'
object
does
not
support
item
"
                            
"
deletion
"
)
        
def
clear
(
self
)
:
            
raise
AttributeError
(
"
'
mappingproxy
'
object
has
no
attribute
"
                                 
"
'
clear
'
"
)
        
def
pop
(
self
key
default
=
None
)
:
            
raise
AttributeError
(
"
'
mappingproxy
'
object
has
no
attribute
"
                                 
"
'
pop
'
"
)
        
def
popitem
(
self
)
:
            
raise
AttributeError
(
"
'
mappingproxy
'
object
has
no
attribute
"
                                 
"
'
popitem
'
"
)
        
def
setdefault
(
self
key
default
=
None
)
:
            
raise
AttributeError
(
"
'
mappingproxy
'
object
has
no
attribute
"
                                 
"
'
setdefault
'
"
)
        
def
__repr__
(
self
)
:
            
return
"
mappingproxy
(
"
+
repr
(
self
.
data
)
+
"
)
"
    
def
metadata_proxy
(
d
)
:
        
res
=
ReadOnlyDict
(
)
        
res
.
data
.
update
(
d
)
        
return
res
else
:
    
def
isclass
(
klass
)
:
        
return
isinstance
(
klass
type
)
    
TYPE
=
"
class
"
    
def
iteritems
(
d
)
:
        
return
d
.
items
(
)
    
def
metadata_proxy
(
d
)
:
        
return
types
.
MappingProxyType
(
dict
(
d
)
)
def
import_ctypes
(
)
:
    
"
"
"
    
Moved
into
a
function
for
testability
.
    
"
"
"
    
import
ctypes
    
return
ctypes
if
not
PY2
:
    
def
just_warn
(
*
args
*
*
kw
)
:
        
"
"
"
        
We
only
warn
on
Python
3
because
we
are
not
aware
of
any
concrete
        
consequences
of
not
setting
the
cell
on
Python
2
.
        
"
"
"
        
warnings
.
warn
(
            
"
Missing
ctypes
.
Some
features
like
bare
super
(
)
or
accessing
"
            
"
__class__
will
not
work
with
slots
classes
.
"
            
RuntimeWarning
            
stacklevel
=
2
        
)
else
:
    
def
just_warn
(
*
args
*
*
kw
)
:
        
"
"
"
        
We
only
warn
on
Python
3
because
we
are
not
aware
of
any
concrete
        
consequences
of
not
setting
the
cell
on
Python
2
.
        
"
"
"
def
make_set_closure_cell
(
)
:
    
"
"
"
    
Moved
into
a
function
for
testability
.
    
"
"
"
    
if
PYPY
:
        
def
set_closure_cell
(
cell
value
)
:
            
cell
.
__setstate__
(
(
value
)
)
    
else
:
        
try
:
            
ctypes
=
import_ctypes
(
)
            
set_closure_cell
=
ctypes
.
pythonapi
.
PyCell_Set
            
set_closure_cell
.
argtypes
=
(
ctypes
.
py_object
ctypes
.
py_object
)
            
set_closure_cell
.
restype
=
ctypes
.
c_int
        
except
Exception
:
            
set_closure_cell
=
just_warn
    
return
set_closure_cell
set_closure_cell
=
make_set_closure_cell
(
)
