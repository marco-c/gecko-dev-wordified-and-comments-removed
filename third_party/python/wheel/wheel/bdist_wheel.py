from
typing
import
TYPE_CHECKING
from
warnings
import
warn
warn
(
    
"
The
'
wheel
'
package
is
no
longer
the
canonical
location
of
the
'
bdist_wheel
'
"
    
"
command
and
will
be
removed
in
a
future
release
.
Please
update
to
setuptools
"
    
"
v70
.
1
or
later
which
contains
an
integrated
version
of
this
command
.
"
    
DeprecationWarning
    
stacklevel
=
1
)
if
TYPE_CHECKING
:
    
from
.
_bdist_wheel
import
bdist_wheel
as
bdist_wheel
else
:
    
try
:
        
from
setuptools
.
command
.
bdist_wheel
import
bdist_wheel
    
except
ImportError
:
        
from
.
_bdist_wheel
import
bdist_wheel
as
bdist_wheel
