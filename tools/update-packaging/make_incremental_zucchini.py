import
argparse
import
configparser
import
functools
import
glob
import
hashlib
import
json
import
logging
import
os
import
re
import
shutil
import
subprocess
import
sys
import
traceback
import
urllib
.
error
import
urllib
.
request
from
concurrent
.
futures
import
ProcessPoolExecutor
from
tempfile
import
NamedTemporaryFile
BCJ_OPTIONS
=
{
    
"
x86
"
:
[
"
-
-
x86
"
]
    
"
x86_64
"
:
[
"
-
-
x86
"
]
    
"
aarch64
"
:
[
]
    
"
macos
-
x86_64
-
aarch64
"
:
[
]
}
logging
.
basicConfig
(
level
=
logging
.
INFO
)
def
log
(
msg
func
=
"
"
)
:
    
logging
.
info
(
f
"
[
pid
:
{
os
.
getpid
(
)
}
]
{
func
}
:
{
msg
}
"
)
def
xz_compression_options
(
arch
)
:
    
return
(
        
"
-
-
compress
"
        
"
-
T1
"
        
"
-
7e
"
        
*
BCJ_OPTIONS
.
get
(
arch
[
]
)
        
"
-
-
lzma2
"
        
"
-
-
format
=
xz
"
        
"
-
-
check
=
crc64
"
        
"
-
-
force
"
    
)
def
get_hash
(
path
)
:
    
h
=
hashlib
.
new
(
"
sha512
"
)
    
with
open
(
path
"
rb
"
)
as
f
:
        
for
chunk
in
iter
(
functools
.
partial
(
f
.
read
4096
)
b
"
"
)
:
            
h
.
update
(
chunk
)
    
return
h
.
hexdigest
(
)
functools
.
cache
def
get_text_from_compressed
(
path
)
:
    
proc
=
subprocess
.
run
(
        
(
"
xz
"
"
-
d
"
"
-
c
"
path
)
        
capture_output
=
True
        
text
=
True
        
check
=
True
    
)
    
return
proc
.
stdout
def
get_option_from_compressed
(
directory
filename
section
option
)
:
    
"
"
"
Gets
an
option
from
an
XZ
compressed
config
file
"
"
"
    
log
(
        
f
"
Extracting
[
{
section
}
]
:
{
option
}
from
{
directory
}
/
*
*
/
{
filename
}
"
        
"
get_option_from_compressed
"
    
)
    
files
=
list
(
glob
.
glob
(
f
"
{
directory
}
/
*
*
/
{
filename
}
"
recursive
=
True
)
)
    
if
not
files
:
        
raise
Exception
(
f
"
Could
not
find
{
filename
}
in
{
directory
}
"
)
    
f
=
files
.
pop
(
)
    
contents
=
get_text_from_compressed
(
f
)
    
config
=
configparser
.
ConfigParser
(
)
    
config
.
read_string
(
contents
)
    
rv
=
config
.
get
(
section
option
)
    
log
(
f
"
Found
{
section
}
.
{
option
}
:
{
rv
}
"
"
get_option_from_compressed
"
)
    
return
rv
def
check_for_forced_update
(
force_list
file_path
)
:
    
"
"
"
Check
for
files
that
are
forced
to
update
.
Note
:
.
chk
files
are
always
force
updated
"
"
"
    
always_force_updated
=
(
        
"
precomplete
"
        
"
Contents
/
Resources
/
precomplete
"
        
"
removed
-
files
"
        
"
Contents
/
Resources
/
removed
-
files
"
        
"
Contents
/
CodeResources
"
    
)
    
return
(
        
file_path
in
always_force_updated
        
or
file_path
.
endswith
(
"
.
chk
"
)
        
or
file_path
in
force_list
    
)
def
list_files_and_dirs
(
dir_path
)
:
    
files
=
[
]
    
dirs
=
[
]
    
for
root
directories
filenames
in
os
.
walk
(
dir_path
)
:
        
for
directory
in
directories
:
            
dirs
.
append
(
os
.
path
.
relpath
(
os
.
path
.
join
(
root
directory
)
dir_path
)
)
        
for
filename
in
filenames
:
            
files
.
append
(
os
.
path
.
relpath
(
os
.
path
.
join
(
root
filename
)
dir_path
)
)
    
return
files
dirs
def
make_add_instruction
(
filename
manifest
)
:
    
"
"
"
Adds
an
instruction
to
the
update
manifest
file
.
"
"
"
    
is_extension
=
re
.
search
(
r
"
distribution
/
extensions
/
.
*
/
"
filename
)
is
not
None
    
if
is_extension
:
        
testdir
=
re
.
sub
(
r
"
(
.
*
distribution
/
extensions
/
[
^
/
]
*
)
/
.
*
"
r
"
\
1
"
filename
)
        
with
open
(
manifest
"
a
"
)
as
file
:
            
file
.
write
(
f
'
add
-
if
"
{
testdir
}
"
"
{
filename
}
"
\
n
'
)
    
else
:
        
with
open
(
manifest
"
a
"
)
as
file
:
            
file
.
write
(
f
'
add
"
{
filename
}
"
\
n
'
)
def
check_for_add_if_not_update
(
filename
)
:
    
basename
=
os
.
path
.
basename
(
filename
)
    
return
(
        
basename
in
{
"
channel
-
prefs
.
js
"
"
update
-
settings
.
ini
"
}
        
or
re
.
search
(
r
"
(
^
|
/
)
ChannelPrefs
\
.
framework
/
"
filename
)
        
or
re
.
search
(
r
"
(
^
|
/
)
UpdateSettings
\
.
framework
/
"
filename
)
    
)
def
make_patch_instruction
(
filename
manifest
)
:
    
with
open
(
manifest
"
a
"
)
as
manifest_file
:
        
manifest_file
.
write
(
f
'
patch
"
{
filename
}
"
\
n
'
)
def
add_remove_instructions
(
remove_array
manifest
)
:
    
with
open
(
manifest
"
a
"
)
as
manifest_file
:
        
for
file
in
remove_array
:
            
manifest_file
.
write
(
f
'
remove
"
{
file
}
"
\
n
'
)
def
make_add_if_not_instruction
(
filename
manifest
)
:
    
with
open
(
manifest
"
a
"
)
as
manifest_file
:
        
manifest_file
.
write
(
f
'
add
-
if
-
not
"
{
filename
}
"
"
{
filename
}
"
\
n
'
)
def
append_remove_instructions
(
newdir
manifest
)
:
    
removed_files_path
=
os
.
path
.
join
(
newdir
"
removed
-
files
"
)
    
if
os
.
path
.
exists
(
removed_files_path
)
:
        
with
NamedTemporaryFile
(
)
as
rmv
open
(
rmv
.
name
"
r
"
)
as
f
:
            
xz_cmd
(
(
"
-
-
decompress
"
)
removed_files_path
rmv
.
name
)
            
removed_files
=
f
.
readlines
(
)
        
with
open
(
manifest
"
a
"
)
as
manifest_file
:
            
for
file
in
removed_files
:
                
manifest_file
.
write
(
f
'
remove
"
{
file
.
strip
(
)
}
"
\
n
'
)
def
mar_extract
(
source_mar
destination
)
:
    
os
.
makedirs
(
destination
exist_ok
=
True
)
    
cmd
=
(
"
mar
"
"
-
C
"
os
.
path
.
abspath
(
destination
)
"
-
x
"
os
.
path
.
abspath
(
source_mar
)
)
    
log
(
f
"
Running
mar
extract
command
:
{
cmd
}
"
"
mar_extract
"
)
    
try
:
        
subprocess
.
run
(
cmd
check
=
True
)
    
except
subprocess
.
CalledProcessError
as
e
:
        
log
(
f
"
Error
extracting
mar
:
{
e
.
stderr
}
"
"
mar_extract
"
)
        
raise
Exception
(
f
"
Mar
failed
with
code
{
e
.
returncode
}
"
)
def
xz_cmd
(
cmd
source_file
destination_file
)
:
    
"
"
"
Run
xz
command
via
pipes
to
avoid
file
extension
checks
.
"
"
"
    
os
.
makedirs
(
os
.
path
.
dirname
(
destination_file
)
exist_ok
=
True
)
    
with
open
(
destination_file
"
wb
"
)
as
dest_fd
open
(
source_file
"
rb
"
)
as
source_fd
:
        
try
:
            
subprocess
.
run
(
(
"
xz
"
*
cmd
)
stdin
=
source_fd
stdout
=
dest_fd
check
=
True
)
        
except
subprocess
.
CalledProcessError
as
e
:
            
log
(
                
f
"
XZ
Failure
running
xz
{
cmd
}
on
{
source_file
}
to
{
destination_file
}
:
{
e
.
stderr
}
"
                
"
xz_cmd
"
            
)
            
raise
Exception
(
f
"
XZ
exited
with
code
{
e
.
returncode
}
"
)
def
create_patch
(
from_file
to_file
destination_patch
)
:
    
"
"
"
Create
a
patch
between
2
xz
compressed
files
"
"
"
    
log
(
f
"
{
from_file
}
-
>
{
destination_patch
}
"
"
create_patch
"
)
    
with
(
        
NamedTemporaryFile
(
)
as
from_fd
        
NamedTemporaryFile
(
)
as
to_fd
        
NamedTemporaryFile
(
)
as
patch_fd
    
)
:
        
xz_cmd
(
(
"
-
-
decompress
"
)
from_file
from_fd
.
name
)
        
xz_cmd
(
(
"
-
-
decompress
"
)
to_file
to_fd
.
name
)
        
args
=
[
"
zucchini
"
"
-
gen
"
from_fd
.
name
to_fd
.
name
patch_fd
.
name
]
        
try
:
            
subprocess
.
run
(
args
check
=
True
)
        
except
subprocess
.
CalledProcessError
as
e
:
            
log
(
f
"
Zucchini
failed
to
create
patch
:
\
n
{
e
.
stderr
}
"
"
create_patch
"
)
            
raise
Exception
(
f
"
Zucchini
exited
with
code
:
{
e
.
returncode
}
"
)
        
xz_cmd
(
(
"
-
-
compress
"
"
-
9
"
"
-
e
"
"
-
c
"
)
patch_fd
.
name
destination_patch
)
def
make_partial
(
from_mar_url
to_mar_dir
target_mar
workdir
arch
=
"
"
force
=
None
)
:
    
from_mar
=
os
.
path
.
join
(
workdir
"
from
.
mar
"
)
    
download_file
(
from_mar_url
from_mar
)
    
requested_forced_updates
=
force
or
[
]
    
requested_forced_updates
.
append
(
"
Contents
/
MacOS
/
firefox
"
)
    
manifest_file
=
os
.
path
.
join
(
workdir
"
updatev3
.
manifest
"
)
    
archivefiles
=
[
]
    
from_mar_dir
=
os
.
path
.
join
(
workdir
"
from_mar
"
)
    
mar_extract
(
from_mar
from_mar_dir
)
    
from_version
=
get_option_from_compressed
(
        
from_mar_dir
"
application
.
ini
"
"
App
"
"
Version
"
    
)
    
log
(
f
"
Processing
from_mar
:
{
from_version
}
"
"
make_partial
"
)
    
partials_dir
=
os
.
path
.
abspath
(
os
.
path
.
join
(
workdir
"
partials
"
)
)
    
os
.
makedirs
(
partials_dir
exist_ok
=
True
)
    
oldfiles
olddirs
=
list_files_and_dirs
(
from_mar_dir
)
    
newfiles
newdirs
=
list_files_and_dirs
(
to_mar_dir
)
    
for
newdir
in
newdirs
:
        
os
.
makedirs
(
os
.
path
.
join
(
partials_dir
newdir
)
exist_ok
=
True
)
    
if
not
os
.
path
.
exists
(
        
os
.
path
.
join
(
to_mar_dir
"
precomplete
"
)
    
)
and
not
os
.
path
.
exists
(
        
os
.
path
.
join
(
to_mar_dir
"
Contents
/
Resources
/
precomplete
"
)
    
)
:
        
log
(
"
precomplete
file
is
missing
!
"
"
make_partial
"
)
        
return
1
    
with
open
(
manifest_file
"
w
"
)
as
manifest_fd
:
        
manifest_fd
.
write
(
'
type
"
partial
"
\
n
'
)
    
remove_array
=
[
]
    
for
rel_path
in
oldfiles
:
        
new_file_abs
=
os
.
path
.
join
(
to_mar_dir
rel_path
)
        
old_file_abs
=
os
.
path
.
join
(
from_mar_dir
rel_path
)
        
if
os
.
path
.
exists
(
new_file_abs
)
:
            
patch_file
=
os
.
path
.
join
(
partials_dir
rel_path
)
            
if
check_for_add_if_not_update
(
old_file_abs
)
:
                
make_add_if_not_instruction
(
rel_path
manifest_file
)
                
shutil
.
copy2
(
new_file_abs
patch_file
)
                
archivefiles
.
append
(
rel_path
)
            
elif
check_for_forced_update
(
requested_forced_updates
rel_path
)
:
                
make_add_instruction
(
rel_path
manifest_file
)
                
shutil
.
copy2
(
new_file_abs
patch_file
)
                
archivefiles
.
append
(
rel_path
)
            
elif
(
                
subprocess
.
run
(
                    
(
"
diff
"
old_file_abs
new_file_abs
)
                    
check
=
False
                
)
.
returncode
                
!
=
0
            
)
:
                
create_patch
(
old_file_abs
new_file_abs
f
"
{
patch_file
}
.
patch
"
)
                
if
(
                    
os
.
stat
(
f
"
{
patch_file
}
.
patch
"
)
.
st_size
                    
>
os
.
stat
(
new_file_abs
)
.
st_size
                
)
:
                    
make_add_instruction
(
rel_path
manifest_file
)
                    
os
.
unlink
(
f
"
{
patch_file
}
.
patch
"
)
                    
shutil
.
copy2
(
new_file_abs
patch_file
)
                    
archivefiles
.
append
(
rel_path
)
                
else
:
                    
make_patch_instruction
(
patch_file
manifest_file
)
                    
path_relpath
=
os
.
path
.
relpath
(
patch_file
partials_dir
)
                    
archivefiles
.
append
(
f
"
{
path_relpath
}
.
patch
"
)
        
else
:
            
remove_array
.
append
(
rel_path
)
    
for
newfile_rel
in
newfiles
:
        
new_file_abs
=
os
.
path
.
join
(
to_mar_dir
newfile_rel
)
        
if
newfile_rel
not
in
oldfiles
:
            
patch_file
=
os
.
path
.
join
(
partials_dir
newfile_rel
)
            
make_add_instruction
(
newfile_rel
manifest_file
)
            
archivefiles
.
append
(
newfile_rel
)
            
shutil
.
copy2
(
new_file_abs
patch_file
)
    
add_remove_instructions
(
remove_array
manifest_file
)
    
append_remove_instructions
(
to_mar_dir
manifest_file
)
    
compressed_manifest
=
os
.
path
.
join
(
partials_dir
"
updatev3
.
manifest
"
)
    
xz_cmd
(
xz_compression_options
(
arch
)
manifest_file
compressed_manifest
)
    
archivefiles
.
append
(
"
updatev3
.
manifest
"
)
    
mar_channel_id
=
os
.
environ
.
get
(
"
MAR_CHANNEL_ID
"
"
unknown
"
)
    
version
=
get_option_from_compressed
(
        
to_mar_dir
"
application
.
ini
"
"
App
"
"
Version
"
    
)
    
log
(
f
"
Archive
files
:
{
'
'
.
join
(
archivefiles
)
}
"
"
make_partial
"
)
    
mar_cmd
=
(
        
"
mar
"
        
"
-
H
"
        
mar_channel_id
        
"
-
V
"
        
version
        
"
-
c
"
        
target_mar
        
*
archivefiles
    
)
    
log
(
f
"
Running
mar
command
with
:
{
'
'
.
join
(
mar_cmd
)
}
"
"
make_partial
"
)
    
try
:
        
subprocess
.
run
(
mar_cmd
cwd
=
partials_dir
check
=
True
)
    
except
subprocess
.
CalledProcessError
as
e
:
        
log
(
f
"
Error
creating
mar
:
\
n
{
e
.
stderr
}
"
)
        
raise
Exception
(
f
"
Mar
exited
with
code
{
e
.
returncode
}
"
)
    
return
{
        
"
MAR_CHANNEL_ID
"
:
mar_channel_id
        
"
appName
"
:
get_option_from_compressed
(
            
from_mar_dir
filename
=
"
application
.
ini
"
section
=
"
App
"
option
=
"
Name
"
        
)
        
"
from_size
"
:
os
.
path
.
getsize
(
from_mar
)
        
"
from_hash
"
:
get_hash
(
from_mar
)
        
"
from_buildid
"
:
get_option_from_compressed
(
            
from_mar_dir
filename
=
"
application
.
ini
"
section
=
"
App
"
option
=
"
BuildID
"
        
)
        
"
mar
"
:
os
.
path
.
basename
(
target_mar
)
        
"
size
"
:
os
.
path
.
getsize
(
target_mar
)
        
"
from_mar
"
:
from_mar_url
    
}
def
download_file
(
url
save_path
)
:
    
"
"
"
    
Downloads
a
file
from
a
given
URL
and
saves
it
to
disk
.
    
Args
:
    
url
(
str
)
:
The
URL
to
download
the
file
from
.
    
save_path
(
str
)
:
The
path
(
including
filename
)
where
the
file
should
be
saved
.
    
"
"
"
    
try
:
        
urllib
.
request
.
urlretrieve
(
url
save_path
)
        
log
(
f
"
File
downloaded
successfully
:
{
save_path
}
"
"
download_file
"
)
    
except
urllib
.
error
.
URLError
as
e
:
        
log
(
f
"
Error
downloading
file
:
{
url
}
-
>
{
e
}
"
"
download_file
"
)
        
raise
Exception
(
"
Failed
to
download
file
.
"
)
    
except
Exception
as
e
:
        
log
(
f
"
An
unexpected
error
occurred
:
{
url
}
-
>
{
e
}
"
"
download_file
"
)
        
raise
Exception
(
"
Failed
to
download
file
.
"
)
def
process_single
(
    
update_number
    
from_mar_url
    
to_mar_dir
    
target_mar
    
workdir
    
arch
    
force
)
:
    
try
:
        
mar_manifest
=
make_partial
(
            
from_mar_url
to_mar_dir
target_mar
workdir
arch
force
        
)
        
mar_manifest
[
"
update_number
"
]
=
update_number
        
return
None
mar_manifest
    
except
Exception
as
e
:
        
log
(
traceback
.
format_exc
(
)
"
process_single
"
)
        
return
e
None
def
main
(
)
:
    
parser
=
argparse
.
ArgumentParser
(
        
description
=
"
Generate
incremental
update
packages
with
zucchini
.
"
    
)
    
parser
.
add_argument
(
        
"
-
-
from_url
"
help
=
"
Complete
mar
URLs
"
action
=
"
append
"
required
=
True
    
)
    
parser
.
add_argument
(
"
-
-
to_mar
"
help
=
"
To
complete
mar
"
required
=
True
)
    
parser
.
add_argument
(
        
"
-
-
to_mar_url
"
        
help
=
"
To
mar
URL
.
Only
used
for
filling
the
manifest
.
json
file
.
"
        
action
=
"
store
"
        
required
=
False
        
default
=
"
"
    
)
    
parser
.
add_argument
(
"
-
-
target
"
help
=
"
Target
partial
mar
location
"
required
=
True
)
    
parser
.
add_argument
(
        
"
-
-
workdir
"
help
=
"
Work
directory
"
action
=
"
store
"
required
=
True
    
)
    
parser
.
add_argument
(
"
-
-
locale
"
help
=
"
Build
locale
"
action
=
"
store
"
required
=
True
)
    
parser
.
add_argument
(
        
"
-
-
arch
"
        
help
=
"
Target
Architecture
"
        
action
=
"
store
"
        
choices
=
BCJ_OPTIONS
.
keys
(
)
        
required
=
True
    
)
    
parser
.
add_argument
(
        
"
-
-
force
"
        
help
=
"
Clobber
this
file
in
the
installation
.
Must
be
a
path
to
a
file
to
clobber
in
the
partial
update
.
"
        
action
=
"
append
"
    
)
    
args
=
parser
.
parse_args
(
)
    
base_workdir
=
os
.
path
.
abspath
(
args
.
workdir
)
    
cpus
=
os
.
cpu_count
(
)
    
log
(
f
"
CPUs
available
for
parallel
computing
:
{
cpus
}
"
"
main
"
)
    
target
=
os
.
path
.
abspath
(
args
.
target
)
    
os
.
makedirs
(
target
exist_ok
=
True
)
    
to_mar_dir
=
os
.
path
.
join
(
base_workdir
"
to_mar
"
)
    
mar_extract
(
args
.
to_mar
to_mar_dir
)
    
futures
=
[
]
    
futures_result
=
[
]
    
def
future_cb
(
f
)
:
        
if
not
f
.
cancelled
(
)
:
            
futures_result
.
append
(
f
.
result
(
)
)
        
else
:
            
futures_result
.
append
(
(
"
Cancelled
"
None
)
)
    
with
ProcessPoolExecutor
(
cpus
)
as
executor
:
        
for
update_number
from_url
in
enumerate
(
args
.
from_url
)
:
            
process_workdir
=
os
.
path
.
join
(
base_workdir
str
(
update_number
)
)
            
os
.
makedirs
(
process_workdir
exist_ok
=
True
)
            
target_mar
=
os
.
path
.
join
(
target
f
"
target
.
partial
-
{
update_number
}
.
mar
"
)
            
future
=
executor
.
submit
(
                
process_single
                
update_number
                
from_url
                
to_mar_dir
                
target_mar
                
process_workdir
                
args
.
arch
                
args
.
force
            
)
            
future
.
add_done_callback
(
future_cb
)
            
futures
.
append
(
future
)
    
log
(
"
Finished
all
processes
.
"
"
main
"
)
    
to_mar_info
=
{
        
"
locale
"
:
args
.
locale
        
"
repo
"
:
get_option_from_compressed
(
            
to_mar_dir
            
filename
=
"
platform
.
ini
"
            
section
=
"
Build
"
            
option
=
"
SourceRepository
"
        
)
        
"
revision
"
:
get_option_from_compressed
(
            
to_mar_dir
filename
=
"
platform
.
ini
"
section
=
"
Build
"
option
=
"
SourceStamp
"
        
)
        
"
version
"
:
get_option_from_compressed
(
            
to_mar_dir
filename
=
"
platform
.
ini
"
section
=
"
Build
"
option
=
"
SourceStamp
"
        
)
        
"
to_buildid
"
:
get_option_from_compressed
(
            
to_mar_dir
filename
=
"
application
.
ini
"
section
=
"
App
"
option
=
"
BuildID
"
        
)
        
"
to_hash
"
:
get_hash
(
args
.
to_mar
)
        
"
to_size
"
:
os
.
stat
(
args
.
to_mar
)
.
st_size
        
"
to_mar
"
:
args
.
to_mar_url
    
}
    
errd
=
False
    
results
=
[
]
    
for
error
manifest
in
futures_result
:
        
if
manifest
:
            
manifest
.
update
(
to_mar_info
)
            
results
.
append
(
manifest
)
        
else
:
            
errd
=
True
            
log
(
"
Process
raised
an
exception
!
"
"
main
"
)
            
print
(
error
)
    
if
errd
:
        
sys
.
exit
(
1
)
    
with
open
(
os
.
path
.
join
(
target
"
manifest
.
json
"
)
"
w
"
)
as
fd
:
        
fd
.
write
(
json
.
dumps
(
results
)
)
    
log
(
"
Finished
writing
final
manifest
.
"
"
main
"
)
if
__name__
=
=
"
__main__
"
:
    
main
(
)
