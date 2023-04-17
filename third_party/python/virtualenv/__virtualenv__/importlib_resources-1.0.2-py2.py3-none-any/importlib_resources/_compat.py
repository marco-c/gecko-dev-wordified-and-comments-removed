from
__future__
import
absolute_import
try
:
    
from
pathlib
import
Path
PurePath
except
ImportError
:
    
from
pathlib2
import
Path
PurePath
try
:
    
from
abc
import
ABC
except
ImportError
:
    
from
abc
import
ABCMeta
    
class
ABC
(
object
)
:
        
__metaclass__
=
ABCMeta
try
:
    
FileNotFoundError
=
FileNotFoundError
except
NameError
:
    
FileNotFoundError
=
OSError
