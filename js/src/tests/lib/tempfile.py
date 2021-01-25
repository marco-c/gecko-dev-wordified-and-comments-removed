from
__future__
import
absolute_import
try
:
    
from
tempfile
import
TemporaryDirectory
except
ImportError
:
    
import
tempfile
    
import
shutil
    
from
contextlib
import
contextmanager
    
contextmanager
    
def
TemporaryDirectory
(
*
args
*
*
kwds
)
:
        
d
=
tempfile
.
mkdtemp
(
*
args
*
*
kwds
)
        
try
:
            
yield
d
        
finally
:
            
shutil
.
rmtree
(
d
)
