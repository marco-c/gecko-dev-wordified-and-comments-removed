import
shutil
import
tarfile
from
pathlib
import
Path
import
mozfile
from
mozbuild
.
bootstrap
import
bootstrap_toolchain
from
mozpack
.
pkg
import
create_pkg
def
repackage_pkg
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
    
xar_tool
=
bootstrap_toolchain
(
"
xar
/
xar
"
)
    
if
not
xar_tool
:
        
raise
Exception
(
"
Could
not
find
xar
tool
.
"
)
    
mkbom_tool
=
bootstrap_toolchain
(
"
mkbom
/
mkbom
"
)
    
if
not
mkbom_tool
:
        
raise
Exception
(
"
Could
not
find
mkbom
tool
.
"
)
    
cpio_tool
=
shutil
.
which
(
"
cpio
"
)
    
if
not
cpio_tool
:
        
raise
Exception
(
"
Could
not
find
cpio
.
"
)
    
with
mozfile
.
TemporaryDirectory
(
)
as
tmpdir
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
        
app_list
=
list
(
Path
(
tmpdir
)
.
glob
(
"
*
.
app
"
)
)
        
if
len
(
app_list
)
!
=
1
:
            
raise
Exception
(
                
"
Input
file
should
contain
a
single
.
app
file
.
%
s
found
.
"
                
%
len
(
app_list
)
            
)
        
create_pkg
(
            
source_app
=
Path
(
app_list
[
0
]
)
            
output_pkg
=
Path
(
output
)
            
mkbom_tool
=
Path
(
mkbom_tool
)
            
xar_tool
=
Path
(
xar_tool
)
            
cpio_tool
=
Path
(
cpio_tool
)
        
)
