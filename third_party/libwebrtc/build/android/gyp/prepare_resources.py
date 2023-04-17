"
"
"
Process
Android
resource
directories
to
generate
.
resources
.
zip
and
R
.
txt
files
.
"
"
"
import
argparse
import
collections
import
os
import
re
import
shutil
import
sys
import
zipfile
from
util
import
build_utils
from
util
import
jar_info_utils
from
util
import
manifest_utils
from
util
import
md5_check
from
util
import
resources_parser
from
util
import
resource_utils
def
_ParseArgs
(
args
)
:
  
"
"
"
Parses
command
line
options
.
  
Returns
:
    
An
options
object
as
from
argparse
.
ArgumentParser
.
parse_args
(
)
  
"
"
"
  
parser
input_opts
output_opts
=
resource_utils
.
ResourceArgsParser
(
)
  
input_opts
.
add_argument
(
      
'
-
-
res
-
sources
-
path
'
      
required
=
True
      
help
=
'
Path
to
a
list
of
input
resources
for
this
target
.
'
)
  
input_opts
.
add_argument
(
      
'
-
-
shared
-
resources
'
      
action
=
'
store_true
'
      
help
=
'
Make
resources
shareable
by
generating
an
onResourcesLoaded
(
)
'
           
'
method
in
the
R
.
java
source
file
.
'
)
  
input_opts
.
add_argument
(
'
-
-
custom
-
package
'
                          
help
=
'
Optional
Java
package
for
main
R
.
java
.
'
)
  
input_opts
.
add_argument
(
      
'
-
-
android
-
manifest
'
      
help
=
'
Optional
AndroidManifest
.
xml
path
.
Only
used
to
extract
a
package
'
           
'
name
for
R
.
java
if
a
-
-
custom
-
package
is
not
provided
.
'
)
  
output_opts
.
add_argument
(
      
'
-
-
resource
-
zip
-
out
'
      
help
=
'
Path
to
a
zip
archive
containing
all
resources
from
'
      
'
-
-
resource
-
dirs
merged
into
a
single
directory
tree
.
'
)
  
output_opts
.
add_argument
(
'
-
-
r
-
text
-
out
'
                    
help
=
'
Path
to
store
the
generated
R
.
txt
file
.
'
)
  
input_opts
.
add_argument
(
      
'
-
-
strip
-
drawables
'
      
action
=
"
store_true
"
      
help
=
'
Remove
drawables
from
the
resources
.
'
)
  
options
=
parser
.
parse_args
(
args
)
  
resource_utils
.
HandleCommonOptions
(
options
)
  
with
open
(
options
.
res_sources_path
)
as
f
:
    
options
.
sources
=
f
.
read
(
)
.
splitlines
(
)
  
options
.
resource_dirs
=
resource_utils
.
DeduceResourceDirsFromFileList
(
      
options
.
sources
)
  
return
options
def
_CheckAllFilesListed
(
resource_files
resource_dirs
)
:
  
resource_files
=
set
(
resource_files
)
  
missing_files
=
[
]
  
for
path
_
in
resource_utils
.
IterResourceFilesInDirectories
(
resource_dirs
)
:
    
if
path
not
in
resource_files
:
      
missing_files
.
append
(
path
)
  
if
missing_files
:
    
sys
.
stderr
.
write
(
'
Error
:
Found
files
not
listed
in
the
sources
list
of
'
                     
'
the
BUILD
.
gn
target
:
\
n
'
)
    
for
path
in
missing_files
:
      
sys
.
stderr
.
write
(
'
{
}
\
n
'
.
format
(
path
)
)
    
sys
.
exit
(
1
)
def
_ZipResources
(
resource_dirs
zip_path
ignore_pattern
)
:
  
files_to_zip
=
[
]
  
path_info
=
resource_utils
.
ResourceInfoFile
(
)
  
for
index
resource_dir
in
enumerate
(
resource_dirs
)
:
    
attributed_aar
=
None
    
if
not
resource_dir
.
startswith
(
'
.
.
'
)
:
      
aar_source_info_path
=
os
.
path
.
join
(
          
os
.
path
.
dirname
(
resource_dir
)
'
source
.
info
'
)
      
if
os
.
path
.
exists
(
aar_source_info_path
)
:
        
attributed_aar
=
jar_info_utils
.
ReadAarSourceInfo
(
aar_source_info_path
)
    
for
path
archive_path
in
resource_utils
.
IterResourceFilesInDirectories
(
        
[
resource_dir
]
ignore_pattern
)
:
      
attributed_path
=
path
      
if
attributed_aar
:
        
attributed_path
=
os
.
path
.
join
(
attributed_aar
'
res
'
                                       
path
[
len
(
resource_dir
)
+
1
:
]
)
      
path_info
.
AddMapping
(
archive_path
attributed_path
)
      
resource_dir_name
=
os
.
path
.
basename
(
resource_dir
)
      
archive_path
=
'
{
}
_
{
}
/
{
}
'
.
format
(
index
resource_dir_name
archive_path
)
      
files_to_zip
.
append
(
(
archive_path
path
)
)
  
path_info
.
Write
(
zip_path
+
'
.
info
'
)
  
with
zipfile
.
ZipFile
(
zip_path
'
w
'
)
as
z
:
    
z
.
comment
=
resource_utils
.
MULTIPLE_RES_MAGIC_STRING
    
build_utils
.
DoZip
(
files_to_zip
z
)
def
_GenerateRTxt
(
options
dep_subdirs
gen_dir
)
:
  
"
"
"
Generate
R
.
txt
file
.
  
Args
:
    
options
:
The
command
-
line
options
tuple
.
    
dep_subdirs
:
List
of
directories
containing
extracted
dependency
resources
.
    
gen_dir
:
Locates
where
the
aapt
-
generated
files
will
go
.
In
particular
      
the
output
file
is
always
generated
as
|
{
gen_dir
}
/
R
.
txt
|
.
  
"
"
"
  
ignore_pattern
=
resource_utils
.
AAPT_IGNORE_PATTERN
  
if
options
.
strip_drawables
:
    
ignore_pattern
+
=
'
:
*
drawable
*
'
  
resource_dirs
=
dep_subdirs
+
options
.
resource_dirs
  
resources_parser
.
RTxtGenerator
(
resource_dirs
ignore_pattern
)
.
WriteRTxtFile
(
      
os
.
path
.
join
(
gen_dir
'
R
.
txt
'
)
)
def
_OnStaleMd5
(
options
)
:
  
with
resource_utils
.
BuildContext
(
)
as
build
:
    
if
options
.
sources
:
      
_CheckAllFilesListed
(
options
.
sources
options
.
resource_dirs
)
    
if
options
.
r_text_in
:
      
r_txt_path
=
options
.
r_text_in
    
else
:
      
dep_subdirs
=
resource_utils
.
ExtractDeps
(
options
.
dependencies_res_zips
                                               
build
.
deps_dir
)
      
_GenerateRTxt
(
options
dep_subdirs
build
.
gen_dir
)
      
r_txt_path
=
build
.
r_txt_path
    
if
options
.
r_text_out
:
      
shutil
.
copyfile
(
r_txt_path
options
.
r_text_out
)
    
if
options
.
resource_zip_out
:
      
ignore_pattern
=
resource_utils
.
AAPT_IGNORE_PATTERN
      
if
options
.
strip_drawables
:
        
ignore_pattern
+
=
'
:
*
drawable
*
'
      
_ZipResources
(
options
.
resource_dirs
options
.
resource_zip_out
                    
ignore_pattern
)
def
main
(
args
)
:
  
args
=
build_utils
.
ExpandFileArgs
(
args
)
  
options
=
_ParseArgs
(
args
)
  
possible_output_paths
=
[
    
options
.
resource_zip_out
    
options
.
r_text_out
  
]
  
output_paths
=
[
x
for
x
in
possible_output_paths
if
x
]
  
input_strings
=
options
.
extra_res_packages
+
[
      
options
.
custom_package
      
options
.
shared_resources
      
options
.
strip_drawables
  
]
  
possible_input_paths
=
[
    
options
.
android_manifest
  
]
  
possible_input_paths
+
=
options
.
include_resources
  
input_paths
=
[
x
for
x
in
possible_input_paths
if
x
]
  
input_paths
.
extend
(
options
.
dependencies_res_zips
)
  
depfile_deps
=
[
]
  
resource_names
=
[
]
  
for
resource_dir
in
options
.
resource_dirs
:
    
for
resource_file
in
build_utils
.
FindInDirectory
(
resource_dir
'
*
'
)
:
      
if
not
resource_file
.
endswith
(
os
.
path
.
join
(
'
empty
'
'
.
keep
'
)
)
:
        
input_paths
.
append
(
resource_file
)
        
depfile_deps
.
append
(
resource_file
)
      
resource_names
.
append
(
os
.
path
.
relpath
(
resource_file
resource_dir
)
)
  
input_strings
.
extend
(
sorted
(
resource_names
)
)
  
md5_check
.
CallAndWriteDepfileIfStale
(
      
lambda
:
_OnStaleMd5
(
options
)
      
options
      
input_paths
=
input_paths
      
input_strings
=
input_strings
      
output_paths
=
output_paths
      
depfile_deps
=
depfile_deps
)
if
__name__
=
=
'
__main__
'
:
  
main
(
sys
.
argv
[
1
:
]
)
