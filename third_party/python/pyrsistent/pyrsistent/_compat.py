from
six
import
string_types
try
:
    
from
enum
import
Enum
except
:
    
class
Enum
(
object
)
:
pass
try
:
    
from
collections
.
abc
import
(
        
Container
        
Hashable
        
Iterable
        
Mapping
        
Sequence
        
Set
        
Sized
    
)
except
ImportError
:
    
from
collections
import
(
        
Container
        
Hashable
        
Iterable
        
Mapping
        
Sequence
        
Set
        
Sized
    
)
