import
inspect
import
platform
import
sys
import
threading
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
PY_3_8_PLUS
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
8
)
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
if
sys
.
version_info
<
(
3
8
)
:
    
try
:
        
from
typing_extensions
import
Protocol
    
except
ImportError
:
        
Protocol
=
object
else
:
    
from
typing
import
Protocol
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
