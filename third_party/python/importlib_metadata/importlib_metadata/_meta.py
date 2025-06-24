from
typing
import
Protocol
from
typing
import
Any
Dict
Iterator
List
Optional
TypeVar
Union
overload
_T
=
TypeVar
(
"
_T
"
)
class
PackageMetadata
(
Protocol
)
:
    
def
__len__
(
self
)
-
>
int
:
        
.
.
.
    
def
__contains__
(
self
item
:
str
)
-
>
bool
:
        
.
.
.
    
def
__getitem__
(
self
key
:
str
)
-
>
str
:
        
.
.
.
    
def
__iter__
(
self
)
-
>
Iterator
[
str
]
:
        
.
.
.
    
overload
    
def
get
(
self
name
:
str
failobj
:
None
=
None
)
-
>
Optional
[
str
]
:
        
.
.
.
    
overload
    
def
get
(
self
name
:
str
failobj
:
_T
)
-
>
Union
[
str
_T
]
:
        
.
.
.
    
overload
    
def
get_all
(
self
name
:
str
failobj
:
None
=
None
)
-
>
Optional
[
List
[
Any
]
]
:
        
.
.
.
    
overload
    
def
get_all
(
self
name
:
str
failobj
:
_T
)
-
>
Union
[
List
[
Any
]
_T
]
:
        
"
"
"
        
Return
all
values
associated
with
a
possibly
multi
-
valued
key
.
        
"
"
"
    
property
    
def
json
(
self
)
-
>
Dict
[
str
Union
[
str
List
[
str
]
]
]
:
        
"
"
"
        
A
JSON
-
compatible
form
of
the
metadata
.
        
"
"
"
class
SimplePath
(
Protocol
[
_T
]
)
:
    
"
"
"
    
A
minimal
subset
of
pathlib
.
Path
required
by
PathDistribution
.
    
"
"
"
    
def
joinpath
(
self
other
:
Union
[
str
_T
]
)
-
>
_T
:
        
.
.
.
    
def
__truediv__
(
self
other
:
Union
[
str
_T
]
)
-
>
_T
:
        
.
.
.
    
property
    
def
parent
(
self
)
-
>
_T
:
        
.
.
.
    
def
read_text
(
self
)
-
>
str
:
        
.
.
.
