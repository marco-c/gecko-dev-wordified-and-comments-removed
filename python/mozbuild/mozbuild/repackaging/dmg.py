import
tarfile
from
pathlib
import
Path
import
mozfile
from
mozpack
.
dmg
import
create_dmg
from
mozbuild
.
bootstrap
import
bootstrap_toolchain
from
mozbuild
.
repackaging
.
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
    
dmg_tool
=
bootstrap_toolchain
(
"
dmg
/
dmg
"
)
    
if
not
dmg_tool
:
        
raise
Exception
(
"
DMG
tool
not
found
"
)
    
hfs_tool
=
bootstrap_toolchain
(
"
dmg
/
hfsplus
"
)
    
if
not
hfs_tool
:
        
raise
Exception
(
"
HFS
tool
not
found
"
)
    
mkfshfs_tool
=
bootstrap_toolchain
(
"
hfsplus
/
newfs_hfs
"
)
    
if
not
mkfshfs_tool
:
        
raise
Exception
(
"
MKFSHFS
tool
not
found
"
)
    
with
mozfile
.
TemporaryDirectory
(
)
as
tmp
:
        
tmpdir
=
Path
(
tmp
)
        
mozfile
.
extract_tarball
(
infile
tmpdir
)
        
symlink
=
tmpdir
/
"
"
        
if
symlink
.
is_file
(
)
:
            
symlink
.
unlink
(
)
        
volume_name
=
get_application_ini_value
(
            
str
(
tmpdir
)
"
App
"
"
CodeName
"
fallback
=
"
Name
"
        
)
        
create_dmg
(
            
source_directory
=
tmpdir
            
output_dmg
=
Path
(
output
)
            
volume_name
=
volume_name
            
extra_files
=
[
]
            
dmg_tool
=
Path
(
dmg_tool
)
            
hfs_tool
=
Path
(
hfs_tool
)
            
mkfshfs_tool
=
Path
(
mkfshfs_tool
)
        
)
