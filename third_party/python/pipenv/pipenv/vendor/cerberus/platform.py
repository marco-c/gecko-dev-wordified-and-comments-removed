"
"
"
Platform
-
dependent
objects
"
"
"
import
sys
PYTHON_VERSION
=
float
(
sys
.
version_info
[
0
]
)
+
float
(
sys
.
version_info
[
1
]
)
/
10
if
PYTHON_VERSION
<
3
:
    
_str_type
=
basestring
    
_int_types
=
(
int
long
)
else
:
    
_str_type
=
str
    
_int_types
=
(
int
)
if
PYTHON_VERSION
<
3
.
3
:
    
from
collections
import
(
        
Callable
        
Container
        
Hashable
        
Iterable
        
Mapping
        
MutableMapping
        
Sequence
        
Set
        
Sized
    
)
else
:
    
from
collections
.
abc
import
(
        
Callable
        
Container
        
Hashable
        
Iterable
        
Mapping
        
MutableMapping
        
Sequence
        
Set
        
Sized
    
)
