from
__future__
import
annotations
import
os
from
collections
.
abc
import
Iterator
from
typing
import
(
    
Any
    
Protocol
    
TypeVar
    
overload
)
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
str
|
None
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
str
|
_T
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
list
[
Any
]
|
None
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
list
[
Any
]
|
_T
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
dict
[
str
str
|
list
[
str
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
Distribution
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
str
|
os
.
PathLike
[
str
]
    
)
-
>
SimplePath
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
str
|
os
.
PathLike
[
str
]
    
)
-
>
SimplePath
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
SimplePath
:
.
.
.
    
def
read_text
(
self
encoding
=
None
)
-
>
str
:
.
.
.
    
def
read_bytes
(
self
)
-
>
bytes
:
.
.
.
    
def
exists
(
self
)
-
>
bool
:
.
.
.
