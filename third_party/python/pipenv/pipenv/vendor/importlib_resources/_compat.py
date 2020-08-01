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
contextlib
import
suppress
except
ImportError
:
    
from
contextlib2
import
suppress
try
:
    
from
functools
import
singledispatch
except
ImportError
:
    
from
singledispatch
import
singledispatch
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
try
:
    
from
importlib
import
metadata
except
ImportError
:
    
import
importlib_metadata
as
metadata
try
:
    
from
zipfile
import
Path
as
ZipPath
except
ImportError
:
    
from
zipp
import
Path
as
ZipPath
try
:
    
from
typing
import
runtime_checkable
except
ImportError
:
    
def
runtime_checkable
(
cls
)
:
        
return
cls
try
:
    
from
typing
import
Protocol
except
ImportError
:
    
Protocol
=
ABC
class
PackageSpec
(
object
)
:
	
def
__init__
(
self
*
*
kwargs
)
:
		
vars
(
self
)
.
update
(
kwargs
)
def
package_spec
(
package
)
:
	
return
getattr
(
package
'
__spec__
'
None
)
or
\
		
PackageSpec
(
			
origin
=
package
.
__file__
			
loader
=
getattr
(
package
'
__loader__
'
None
)
		
)
