import
os
import
tempfile
import
tarfile
import
shutil
import
mozpack
.
path
as
mozpath
from
mozpack
.
dmg
import
create_dmg
from
application_ini
import
get_application_ini_value
def
repackage_dmg
(
infile
output
)
:
    
if
not
tarfile
.
is_tarfile
(
infile
)
:
        
raise
Exception
(
"
Input
file
%
s
is
not
a
valid
tarfile
.
"
%
infile
)
    
tmpdir
=
tempfile
.
mkdtemp
(
)
    
try
:
        
with
tarfile
.
open
(
infile
)
as
tar
:
            
tar
.
extractall
(
path
=
tmpdir
)
        
try
:
            
os
.
remove
(
mozpath
.
join
(
tmpdir
'
'
)
)
        
except
OSError
as
e
:
            
if
e
.
errno
!
=
errno
.
ENOENT
:
                
raise
        
volume_name
=
get_application_ini_value
(
tmpdir
'
App
'
'
CodeName
'
                                                
fallback
=
'
Name
'
)
        
create_dmg
(
tmpdir
output
volume_name
[
]
)
    
finally
:
        
shutil
.
rmtree
(
tmpdir
)
