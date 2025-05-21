import
hashlib
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
uv
.
lock
"
    
"
uv
.
lock
.
hash
"
    
"
pyproject
.
toml
"
    
"
requirements
.
txt
"
    
"
ansicon
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
        
super
(
)
.
__init__
(
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
        
add
=
None
        
remove
=
None
        
upgrade
=
False
        
upgrade_package
=
None
        
force
=
False
    
)
:
        
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
        
requirements_file_name
=
"
requirements
.
txt
"
        
requirements_path
=
vendor_dir
/
requirements_file_name
        
uv_lock_file
=
vendor_dir
/
"
uv
.
lock
"
        
vendored_lock_file_hash_file
=
vendor_dir
/
"
uv
.
lock
.
hash
"
        
os
.
environ
[
"
UV_PROJECT_ENVIRONMENT
"
]
=
os
.
environ
.
get
(
"
VIRTUAL_ENV
"
None
)
        
if
add
:
            
for
package
in
add
:
                
subprocess
.
check_call
(
[
"
uv
"
"
add
"
package
]
cwd
=
vendor_dir
)
        
if
remove
:
            
for
package
in
remove
:
                
subprocess
.
check_call
(
[
"
uv
"
"
remove
"
package
]
cwd
=
vendor_dir
)
        
lock_command
=
[
"
uv
"
"
lock
"
]
        
if
upgrade
:
            
lock_command
.
extend
(
[
"
-
U
"
]
)
        
if
upgrade_package
:
            
for
package
in
upgrade_package
:
                
lock_command
.
extend
(
[
"
-
P
"
package
]
)
        
subprocess
.
check_call
(
lock_command
cwd
=
vendor_dir
)
        
if
not
force
:
            
vendored_lock_file_hash_value
=
vendored_lock_file_hash_file
.
read_text
(
                
encoding
=
"
utf
-
8
"
            
)
.
strip
(
)
            
new_lock_file_hash_value
=
hash_file_text
(
uv_lock_file
)
            
if
vendored_lock_file_hash_value
=
=
new_lock_file_hash_value
:
                
print
(
                    
"
No
changes
detected
in
uv
.
lock
since
last
vendor
.
Nothing
to
do
.
(
You
can
re
-
run
this
command
with
'
-
-
force
'
to
force
vendoring
)
"
                
)
                
return
            
print
(
"
Changes
detected
in
uv
.
lock
.
"
)
        
print
(
"
Re
-
vendoring
all
dependencies
.
"
)
        
subprocess
.
check_call
(
            
[
                
"
uv
"
                
"
export
"
                
"
-
-
format
"
                
"
requirements
-
txt
"
                
"
-
o
"
                
requirements_file_name
                
"
-
q
"
            
]
            
cwd
=
vendor_dir
        
)
        
remove_environment_markers_from_requirements_txt
(
requirements_path
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
requirements_path
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
        
vendored_lock_file_hash_file
.
write_text
(
            
encoding
=
"
utf
-
8
"
data
=
hash_file_text
(
uv_lock_file
)
        
)
        
self
.
repository
.
add_remove_files
(
vendor_dir
)
        
egg_info_files
=
list
(
vendor_dir
.
glob
(
"
*
*
/
*
.
egg
-
info
/
*
"
)
)
        
if
egg_info_files
:
            
self
.
repository
.
add_remove_files
(
*
egg_info_files
force
=
True
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
hash_file_text
(
file_path
)
:
    
hash_func
=
hashlib
.
new
(
"
sha256
"
)
    
file_content
=
file_path
.
read_text
(
encoding
=
"
utf
-
8
"
)
    
hash_func
.
update
(
file_content
.
encode
(
"
utf
-
8
"
)
)
    
return
hash_func
.
hexdigest
(
)
