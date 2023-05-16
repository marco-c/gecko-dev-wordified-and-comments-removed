import
inspect
import
platform
import
sys
import
threading
import
types
import
warnings
from
collections
.
abc
import
Mapping
Sequence
from
typing
import
_GenericAlias
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
PY_3_9_PLUS
=
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
9
)
PY310
=
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
10
)
PY_3_12_PLUS
=
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
12
)
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
    
warnings
.
warn
(
        
"
Running
interpreter
doesn
'
t
sufficiently
support
code
object
"
        
"
introspection
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
slotted
classes
.
"
        
RuntimeWarning
        
stacklevel
=
2
    
)
class
_AnnotationExtractor
:
    
"
"
"
    
Extract
type
annotations
from
a
callable
returning
None
whenever
there
    
is
none
.
    
"
"
"
    
__slots__
=
[
"
sig
"
]
    
def
__init__
(
self
callable
)
:
        
try
:
            
self
.
sig
=
inspect
.
signature
(
callable
)
        
except
(
ValueError
TypeError
)
:
            
self
.
sig
=
None
    
def
get_first_param_type
(
self
)
:
        
"
"
"
        
Return
the
type
annotation
of
the
first
argument
if
it
'
s
not
empty
.
        
"
"
"
        
if
not
self
.
sig
:
            
return
None
        
params
=
list
(
self
.
sig
.
parameters
.
values
(
)
)
        
if
params
and
params
[
0
]
.
annotation
is
not
inspect
.
Parameter
.
empty
:
            
return
params
[
0
]
.
annotation
        
return
None
    
def
get_return_type
(
self
)
:
        
"
"
"
        
Return
the
return
type
if
it
'
s
not
empty
.
        
"
"
"
        
if
(
            
self
.
sig
            
and
self
.
sig
.
return_annotation
is
not
inspect
.
Signature
.
empty
        
)
:
            
return
self
.
sig
.
return_annotation
        
return
None
def
make_set_closure_cell
(
)
:
    
"
"
"
Return
a
function
of
two
arguments
(
cell
value
)
which
sets
    
the
value
stored
in
the
closure
cell
cell
to
value
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
        
return
set_closure_cell
    
try
:
        
if
sys
.
version_info
>
=
(
3
8
)
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
cell_contents
=
value
        
else
:
            
def
set_first_cellvar_to
(
value
)
:
                
x
=
value
                
return
                
def
force_x_to_be_a_cell
(
)
:
                    
return
x
            
co
=
set_first_cellvar_to
.
__code__
            
if
co
.
co_cellvars
!
=
(
"
x
"
)
or
co
.
co_freevars
!
=
(
)
:
                
raise
AssertionError
            
args
=
[
co
.
co_argcount
]
            
args
.
append
(
co
.
co_kwonlyargcount
)
            
args
.
extend
(
                
[
                    
co
.
co_nlocals
                    
co
.
co_stacksize
                    
co
.
co_flags
                    
co
.
co_code
                    
co
.
co_consts
                    
co
.
co_names
                    
co
.
co_varnames
                    
co
.
co_filename
                    
co
.
co_name
                    
co
.
co_firstlineno
                    
co
.
co_lnotab
                    
co
.
co_cellvars
                    
co
.
co_freevars
                
]
            
)
            
set_first_freevar_code
=
types
.
CodeType
(
*
args
)
            
def
set_closure_cell
(
cell
value
)
:
                
setter
=
types
.
FunctionType
(
                    
set_first_freevar_code
{
}
"
setter
"
(
)
(
cell
)
                
)
                
setter
(
value
)
        
def
make_func_with_cell
(
)
:
            
x
=
None
            
def
func
(
)
:
                
return
x
            
return
func
        
cell
=
make_func_with_cell
(
)
.
__closure__
[
0
]
        
set_closure_cell
(
cell
100
)
        
if
cell
.
cell_contents
!
=
100
:
            
raise
AssertionError
    
except
Exception
:
        
return
just_warn
    
else
:
        
return
set_closure_cell
set_closure_cell
=
make_set_closure_cell
(
)
repr_context
=
threading
.
local
(
)
def
get_generic_base
(
cl
)
:
    
"
"
"
If
this
is
a
generic
class
(
A
[
str
]
)
return
the
generic
base
for
it
.
"
"
"
    
if
cl
.
__class__
is
_GenericAlias
:
        
return
cl
.
__origin__
    
return
None
