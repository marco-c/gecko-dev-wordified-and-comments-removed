"
"
"
Utilities
for
code
coverage
related
processings
.
"
"
"
import
logging
import
os
import
posixpath
import
shutil
import
subprocess
from
devil
import
base_error
from
pylib
import
constants
LLVM_PROFDATA_PATH
=
os
.
path
.
join
(
constants
.
DIR_SOURCE_ROOT
'
third_party
'
                                  
'
llvm
-
build
'
'
Release
+
Asserts
'
'
bin
'
                                  
'
llvm
-
profdata
'
)
_PROFRAW_FILE_EXTENSION
=
'
profraw
'
_MERGE_PROFDATA_FILE_NAME
=
'
coverage_merged
.
'
+
_PROFRAW_FILE_EXTENSION
def
GetDeviceClangCoverageDir
(
device
)
:
  
"
"
"
Gets
the
directory
to
generate
clang
coverage
data
on
device
.
  
Args
:
    
device
:
The
working
device
.
  
Returns
:
    
The
directory
path
on
the
device
.
  
"
"
"
  
return
posixpath
.
join
(
device
.
GetExternalStoragePath
(
)
'
chrome
'
'
test
'
                        
'
coverage
'
'
profraw
'
)
def
PullAndMaybeMergeClangCoverageFiles
(
device
device_coverage_dir
output_dir
                                        
output_subfolder_name
)
:
  
"
"
"
Pulls
and
possibly
merges
clang
coverage
file
to
a
single
file
.
  
Only
merges
when
llvm
-
profdata
tool
exists
.
If
so
Merged
file
is
at
  
output_dir
/
coverage_merged
.
profraw
and
raw
profraw
files
before
merging
  
are
deleted
.
  
Args
:
    
device
:
The
working
device
.
    
device_coverage_dir
:
The
directory
storing
coverage
data
on
device
.
    
output_dir
:
The
output
directory
on
host
to
store
the
        
coverage_merged
.
profraw
file
.
    
output_subfolder_name
:
The
subfolder
in
|
output_dir
|
to
pull
        
|
device_coverage_dir
|
into
.
It
will
be
deleted
after
merging
if
        
merging
happens
.
  
"
"
"
  
if
not
device
.
PathExists
(
device_coverage_dir
retries
=
0
)
:
    
logging
.
warning
(
'
Clang
coverage
data
folder
does
not
exist
on
device
:
%
s
'
                    
device_coverage_dir
)
    
return
  
profraw_parent_dir
=
os
.
path
.
join
(
output_dir
output_subfolder_name
)
  
PullClangCoverageFiles
(
device
device_coverage_dir
profraw_parent_dir
)
  
if
os
.
path
.
isfile
(
LLVM_PROFDATA_PATH
)
:
    
profraw_folder_name
=
os
.
path
.
basename
(
        
os
.
path
.
normpath
(
device_coverage_dir
)
)
    
profraw_dir
=
os
.
path
.
join
(
profraw_parent_dir
profraw_folder_name
)
    
MergeClangCoverageFiles
(
output_dir
profraw_dir
)
    
shutil
.
rmtree
(
profraw_parent_dir
)
def
PullClangCoverageFiles
(
device
device_coverage_dir
output_dir
)
:
  
"
"
"
Pulls
clang
coverage
files
on
device
to
host
directory
.
  
Args
:
    
device
:
The
working
device
.
    
device_coverage_dir
:
The
directory
to
store
coverage
data
on
device
.
    
output_dir
:
The
output
directory
on
host
.
  
"
"
"
  
try
:
    
if
not
os
.
path
.
exists
(
output_dir
)
:
      
os
.
makedirs
(
output_dir
)
    
device
.
PullFile
(
device_coverage_dir
output_dir
)
    
if
not
os
.
listdir
(
os
.
path
.
join
(
output_dir
'
profraw
'
)
)
:
      
logging
.
warning
(
'
No
clang
coverage
data
was
generated
for
this
run
'
)
  
except
(
OSError
base_error
.
BaseError
)
as
e
:
    
logging
.
warning
(
'
Failed
to
pull
clang
coverage
data
error
:
%
s
'
e
)
  
finally
:
    
device
.
RemovePath
(
device_coverage_dir
force
=
True
recursive
=
True
)
def
MergeClangCoverageFiles
(
coverage_dir
profdata_dir
)
:
  
"
"
"
Merge
coverage
data
files
.
  
Each
instrumentation
activity
generates
a
separate
profraw
data
file
.
This
  
merges
all
profraw
files
in
profdata_dir
into
a
single
file
in
  
coverage_dir
.
This
happens
after
each
test
rather
than
waiting
until
after
  
all
tests
are
ran
to
reduce
the
memory
footprint
used
by
all
the
profraw
  
files
.
  
Args
:
    
coverage_dir
:
The
path
to
the
coverage
directory
.
    
profdata_dir
:
The
directory
where
the
profraw
data
file
(
s
)
are
located
.
  
Return
:
    
None
  
"
"
"
  
if
not
os
.
path
.
exists
(
profdata_dir
)
:
    
logging
.
debug
(
'
Profraw
directory
does
not
exist
:
%
s
'
profdata_dir
)
    
return
  
merge_file
=
os
.
path
.
join
(
coverage_dir
_MERGE_PROFDATA_FILE_NAME
)
  
profraw_files
=
[
      
os
.
path
.
join
(
profdata_dir
f
)
for
f
in
os
.
listdir
(
profdata_dir
)
      
if
f
.
endswith
(
_PROFRAW_FILE_EXTENSION
)
  
]
  
try
:
    
logging
.
debug
(
'
Merging
target
profraw
files
into
merged
profraw
file
.
'
)
    
subprocess_cmd
=
[
        
LLVM_PROFDATA_PATH
        
'
merge
'
        
'
-
o
'
        
merge_file
        
'
-
sparse
=
true
'
    
]
    
if
os
.
path
.
exists
(
merge_file
)
:
      
subprocess_cmd
.
append
(
merge_file
)
    
subprocess_cmd
.
extend
(
profraw_files
)
    
output
=
subprocess
.
check_output
(
subprocess_cmd
)
.
decode
(
'
utf8
'
)
    
logging
.
debug
(
'
Merge
output
:
%
s
'
output
)
  
except
subprocess
.
CalledProcessError
:
    
logging
.
error
(
        
'
Failed
to
merge
target
profdata
files
to
create
'
        
'
merged
profraw
file
for
files
:
%
s
'
profraw_files
)
  
for
f
in
profraw_files
:
    
os
.
remove
(
f
)
