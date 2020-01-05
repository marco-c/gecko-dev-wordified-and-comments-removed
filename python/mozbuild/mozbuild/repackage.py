import
os
import
tempfile
import
tarfile
import
shutil
import
ConfigParser
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
None
        
for
root
dirs
files
in
os
.
walk
(
tmpdir
)
:
            
if
'
application
.
ini
'
in
files
:
                
parser
=
ConfigParser
.
ConfigParser
(
)
                
parser
.
read
(
mozpath
.
join
(
root
'
application
.
ini
'
)
)
                
volume_name
=
parser
.
get
(
'
App
'
'
CodeName
'
)
                
break
        
if
volume_name
is
None
:
            
raise
Exception
(
"
Input
package
does
not
contain
an
application
.
ini
file
"
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
