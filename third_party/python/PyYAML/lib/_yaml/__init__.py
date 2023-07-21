import
yaml
if
not
getattr
(
yaml
'
__with_libyaml__
'
False
)
:
    
from
sys
import
version_info
    
exc
=
ModuleNotFoundError
if
version_info
>
=
(
3
6
)
else
ImportError
    
raise
exc
(
"
No
module
named
'
_yaml
'
"
)
else
:
    
from
yaml
.
_yaml
import
*
    
import
warnings
    
warnings
.
warn
(
        
'
The
_yaml
extension
module
is
now
located
at
yaml
.
_yaml
'
        
'
and
its
location
is
subject
to
change
.
To
use
the
'
        
'
LibYAML
-
based
parser
and
emitter
import
from
yaml
:
'
        
'
from
yaml
import
CLoader
as
Loader
CDumper
as
Dumper
.
'
        
DeprecationWarning
    
)
    
del
warnings
__name__
=
'
_yaml
'
__package__
=
'
'
