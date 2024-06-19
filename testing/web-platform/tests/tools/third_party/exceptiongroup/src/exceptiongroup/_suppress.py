from
__future__
import
annotations
import
sys
from
contextlib
import
AbstractContextManager
from
types
import
TracebackType
from
typing
import
TYPE_CHECKING
Optional
Type
cast
if
sys
.
version_info
<
(
3
11
)
:
    
from
.
_exceptions
import
BaseExceptionGroup
if
TYPE_CHECKING
:
    
BaseClass
=
AbstractContextManager
[
None
]
else
:
    
BaseClass
=
AbstractContextManager
class
suppress
(
BaseClass
)
:
    
"
"
"
Backport
of
:
class
:
contextlib
.
suppress
from
Python
3
.
12
.
1
.
"
"
"
    
def
__init__
(
self
*
exceptions
:
type
[
BaseException
]
)
:
        
self
.
_exceptions
=
exceptions
    
def
__enter__
(
self
)
-
>
None
:
        
pass
    
def
__exit__
(
        
self
        
exctype
:
Optional
[
Type
[
BaseException
]
]
        
excinst
:
Optional
[
BaseException
]
        
exctb
:
Optional
[
TracebackType
]
    
)
-
>
bool
:
        
if
exctype
is
None
:
            
return
False
        
if
issubclass
(
exctype
self
.
_exceptions
)
:
            
return
True
        
if
issubclass
(
exctype
BaseExceptionGroup
)
:
            
match
rest
=
cast
(
BaseExceptionGroup
excinst
)
.
split
(
self
.
_exceptions
)
            
if
rest
is
None
:
                
return
True
            
raise
rest
        
return
False
