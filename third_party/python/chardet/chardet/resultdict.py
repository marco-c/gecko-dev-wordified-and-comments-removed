from
typing
import
TYPE_CHECKING
Optional
if
TYPE_CHECKING
:
    
from
typing
import
TypedDict
    
class
ResultDict
(
TypedDict
)
:
        
encoding
:
Optional
[
str
]
        
confidence
:
float
        
language
:
Optional
[
str
]
else
:
    
ResultDict
=
dict
