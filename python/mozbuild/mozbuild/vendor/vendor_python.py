import
os
import
shutil
import
subprocess
import
sys
from
pathlib
import
Path
import
mozfile
from
mozfile
import
TemporaryDirectory
from
mozpack
.
files
import
FileFinder
from
mozbuild
.
base
import
MozbuildObject
EXCLUDED_PACKAGES
=
{
    
"
dlmanager
"
    
"
gyp
"
    
"
_venv
"
    
"
vsdownload
"
    
"
moz
.
build
"
    
"
requirements
.
in
"
    
"
ansicon
"
    
"
pip
"
}
class
VendorPython
(
MozbuildObject
)
:
    
def
__init__
(
self
*
args
*
*
kwargs
)
:
        
MozbuildObject
.
__init__
(
self
*
args
virtualenv_name
=
"
vendor
"
*
*
kwargs
)
    
def
vendor
(
self
keep_extra_files
=
False
)
:
        
from
mach
.
python_lockfile
import
PoetryHandle
        
self
.
populate_logger
(
)
        
self
.
log_manager
.
enable_unstructured
(
)
        
vendor_dir
=
Path
(
self
.
topsrcdir
)
/
"
third_party
"
/
"
python
"
        
requirements_in
=
vendor_dir
/
"
requirements
.
in
"
        
poetry_lockfile
=
vendor_dir
/
"
poetry
.
lock
"
        
_sort_requirements_in
(
requirements_in
)
        
with
TemporaryDirectory
(
)
as
work_dir
:
            
work_dir
=
Path
(
work_dir
)
            
poetry
=
PoetryHandle
(
work_dir
)
            
poetry
.
add_requirements_in_file
(
requirements_in
)
            
poetry
.
reuse_existing_lockfile
(
poetry_lockfile
)
            
lockfiles
=
poetry
.
generate_lockfiles
(
do_update
=
False
)
            
pip_lockfile_without_markers
=
work_dir
/
"
requirements
.
no
-
markers
.
txt
"
            
shutil
.
copy
(
str
(
lockfiles
.
pip_lockfile
)
str
(
pip_lockfile_without_markers
)
)
            
remove_environment_markers_from_requirements_txt
(
                
pip_lockfile_without_markers
            
)
            
with
TemporaryDirectory
(
)
as
tmp
:
                
subprocess
.
check_call
(
                    
[
                        
sys
.
executable
                        
"
-
m
"
                        
"
pip
"
                        
"
download
"
                        
"
-
r
"
                        
str
(
pip_lockfile_without_markers
)
                        
"
-
-
no
-
deps
"
                        
"
-
-
dest
"
                        
tmp
                        
"
-
-
abi
"
                        
"
none
"
                        
"
-
-
platform
"
                        
"
any
"
                    
]
                
)
                
_purge_vendor_dir
(
vendor_dir
)
                
self
.
_extract
(
tmp
vendor_dir
keep_extra_files
)
            
requirements_out
=
vendor_dir
/
"
requirements
.
txt
"
            
_copy_file_strip_carriage_return
(
lockfiles
.
pip_lockfile
requirements_out
)
            
_copy_file_strip_carriage_return
(
lockfiles
.
poetry_lockfile
poetry_lockfile
)
            
self
.
repository
.
add_remove_files
(
vendor_dir
)
    
def
_extract
(
self
src
dest
keep_extra_files
=
False
)
:
        
"
"
"
extract
source
distribution
into
vendor
directory
"
"
"
        
ignore
=
(
)
        
if
not
keep_extra_files
:
            
ignore
=
(
"
*
/
doc
"
"
*
/
docs
"
"
*
/
test
"
"
*
/
tests
"
"
*
*
/
.
git
"
)
        
finder
=
FileFinder
(
src
)
        
for
archive
_
in
finder
.
find
(
"
*
"
)
:
            
_
ext
=
os
.
path
.
splitext
(
archive
)
            
archive_path
=
os
.
path
.
join
(
finder
.
base
archive
)
            
if
ext
=
=
"
.
whl
"
:
                
package_name
version
spec
abi
platform_and_suffix
=
archive
.
rsplit
(
                    
"
-
"
4
                
)
                
if
package_name
in
EXCLUDED_PACKAGES
:
                    
print
(
                        
f
"
'
{
package_name
}
'
is
on
the
exclusion
list
and
will
not
be
vendored
.
"
                    
)
                    
continue
                
target_package_dir
=
os
.
path
.
join
(
dest
package_name
)
                
os
.
mkdir
(
target_package_dir
)
                
mozfile
.
extract
(
archive_path
target_package_dir
ignore
=
ignore
)
                
_denormalize_symlinks
(
target_package_dir
)
            
else
:
                
package_name
archive_postfix
=
archive
.
rsplit
(
"
-
"
1
)
                
package_dir
=
os
.
path
.
join
(
dest
package_name
)
                
if
package_name
in
EXCLUDED_PACKAGES
:
                    
print
(
                        
f
"
'
{
package_name
}
'
is
on
the
exclusion
list
and
will
not
be
vendored
.
"
                    
)
                    
continue
                
extracted_files
=
mozfile
.
extract
(
archive_path
dest
ignore
=
ignore
)
                
assert
len
(
extracted_files
)
=
=
1
                
extracted_package_dir
=
extracted_files
[
0
]
                
mozfile
.
move
(
extracted_package_dir
package_dir
)
                
_denormalize_symlinks
(
package_dir
)
def
_sort_requirements_in
(
requirements_in
:
Path
)
:
    
requirements
=
{
}
    
with
requirements_in
.
open
(
mode
=
"
r
"
newline
=
"
\
n
"
)
as
f
:
        
comments
=
[
]
        
for
line
in
f
.
readlines
(
)
:
            
line
=
line
.
strip
(
)
            
if
not
line
or
line
.
startswith
(
"
#
"
)
:
                
comments
.
append
(
line
)
                
continue
            
name
version
=
line
.
split
(
"
=
=
"
)
            
requirements
[
name
]
=
version
comments
            
comments
=
[
]
    
with
requirements_in
.
open
(
mode
=
"
w
"
newline
=
"
\
n
"
)
as
f
:
        
for
name
(
version
comments
)
in
sorted
(
requirements
.
items
(
)
)
:
            
if
comments
:
                
f
.
write
(
"
{
}
\
n
"
.
format
(
"
\
n
"
.
join
(
comments
)
)
)
            
f
.
write
(
"
{
}
=
=
{
}
\
n
"
.
format
(
name
version
)
)
def
remove_environment_markers_from_requirements_txt
(
requirements_txt
:
Path
)
:
    
with
requirements_txt
.
open
(
mode
=
"
r
"
newline
=
"
\
n
"
)
as
f
:
        
lines
=
f
.
readlines
(
)
    
markerless_lines
=
[
]
    
continuation_token
=
"
\
\
"
    
for
line
in
lines
:
        
line
=
line
.
rstrip
(
)
        
if
not
line
.
startswith
(
"
"
)
and
not
line
.
startswith
(
"
#
"
)
and
"
;
"
in
line
:
            
has_continuation_token
=
line
.
endswith
(
continuation_token
)
            
line
=
line
.
split
(
"
;
"
)
[
0
]
            
if
has_continuation_token
:
                
line
+
=
continuation_token
            
markerless_lines
.
append
(
line
)
        
else
:
            
markerless_lines
.
append
(
line
)
    
with
requirements_txt
.
open
(
mode
=
"
w
"
newline
=
"
\
n
"
)
as
f
:
        
f
.
write
(
"
\
n
"
.
join
(
markerless_lines
)
)
def
_purge_vendor_dir
(
vendor_dir
)
:
    
for
child
in
Path
(
vendor_dir
)
.
iterdir
(
)
:
        
if
child
.
name
not
in
EXCLUDED_PACKAGES
:
            
mozfile
.
remove
(
str
(
child
)
)
def
_denormalize_symlinks
(
target
)
:
    
link_finder
=
FileFinder
(
target
)
    
for
_
f
in
link_finder
.
find
(
"
*
*
"
)
:
        
if
os
.
path
.
islink
(
f
.
path
)
:
            
link_target
=
os
.
path
.
realpath
(
f
.
path
)
            
os
.
unlink
(
f
.
path
)
            
shutil
.
copyfile
(
link_target
f
.
path
)
def
_copy_file_strip_carriage_return
(
file_src
:
Path
file_dst
)
:
    
shutil
.
copyfileobj
(
file_src
.
open
(
mode
=
"
r
"
)
file_dst
.
open
(
mode
=
"
w
"
newline
=
"
\
n
"
)
)
