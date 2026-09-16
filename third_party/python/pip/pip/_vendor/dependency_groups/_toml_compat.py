try
:
    
import
tomllib
except
ImportError
:
    
try
:
        
from
pip
.
_vendor
import
tomli
as
tomllib
    
except
ModuleNotFoundError
:
        
tomllib
=
None
__all__
=
(
"
tomllib
"
)
