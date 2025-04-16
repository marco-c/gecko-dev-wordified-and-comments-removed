"
"
"
Use
pywatchman
to
watch
source
directories
and
perform
partial
mach
build
faster
builds
.
"
"
"
import
datetime
import
sys
import
time
import
mozpack
.
path
as
mozpath
import
pywatchman
from
mozpack
.
copier
import
FileCopier
from
mozpack
.
manifests
import
InstallManifest
import
mozbuild
.
util
from
mozbuild
.
backend
import
get_backend_class
def
print_line
(
prefix
m
now
=
None
)
:
    
now
=
now
or
datetime
.
datetime
.
utcnow
(
)
    
print
(
"
[
%
s
%
sZ
]
%
s
"
%
(
prefix
now
.
isoformat
(
)
m
)
)
def
print_copy_result
(
elapsed
destdir
result
verbose
=
True
)
:
    
COMPLETE
=
(
        
"
Elapsed
:
{
elapsed
:
.
2f
}
s
;
From
{
dest
}
:
Kept
{
existing
}
existing
;
"
        
"
Added
/
updated
{
updated
}
;
"
        
"
Removed
{
rm_files
}
files
and
{
rm_dirs
}
directories
.
"
    
)
    
print_line
(
        
"
watch
"
        
COMPLETE
.
format
(
            
elapsed
=
elapsed
            
dest
=
destdir
            
existing
=
result
.
existing_files_count
            
updated
=
result
.
updated_files_count
            
rm_files
=
result
.
removed_files_count
            
rm_dirs
=
result
.
removed_directories_count
        
)
    
)
class
FasterBuildException
(
Exception
)
:
    
def
__init__
(
self
message
cause
)
:
        
Exception
.
__init__
(
self
message
)
        
self
.
cause
=
cause
class
FasterBuildChange
:
    
def
__init__
(
self
)
:
        
self
.
unrecognized
=
set
(
)
        
self
.
input_to_outputs
=
{
}
        
self
.
output_to_inputs
=
{
}
class
Daemon
:
    
def
__init__
(
self
config_environment
)
:
        
self
.
config_environment
=
config_environment
        
self
.
_client
=
None
    
property
    
def
defines
(
self
)
:
        
defines
=
dict
(
self
.
config_environment
.
acdefines
)
        
defines
.
update
(
            
{
                
"
AB_CD
"
:
"
en
-
US
"
            
}
        
)
        
return
defines
    
mozbuild
.
util
.
memoized_property
    
def
file_copier
(
self
)
:
        
file_copier
=
FileCopier
(
)
        
unified_manifest
=
InstallManifest
(
            
mozpath
.
join
(
                
self
.
config_environment
.
topobjdir
"
faster
"
"
unified_install_dist_bin
"
            
)
        
)
        
unified_manifest
.
populate_registry
(
file_copier
defines_override
=
self
.
defines
)
        
return
file_copier
    
def
subscribe_to_topsrcdir
(
self
)
:
        
self
.
subscribe_to_dir
(
"
topsrcdir
"
self
.
config_environment
.
topsrcdir
)
    
def
subscribe_to_dir
(
self
name
dir_to_watch
)
:
        
query
=
{
            
"
empty_on_fresh_instance
"
:
True
            
"
expression
"
:
[
                
"
allof
"
                
[
"
type
"
"
f
"
]
                
[
                    
"
not
"
                    
[
                        
"
anyof
"
                        
[
"
dirname
"
"
.
hg
"
]
                        
[
"
name
"
"
.
hg
"
"
wholename
"
]
                        
[
"
dirname
"
"
.
git
"
]
                        
[
"
name
"
"
.
git
"
"
wholename
"
]
                    
]
                
]
            
]
            
"
fields
"
:
[
"
name
"
]
        
}
        
watch
=
self
.
client
.
query
(
"
watch
-
project
"
dir_to_watch
)
        
if
"
warning
"
in
watch
:
            
print
(
"
WARNING
:
"
watch
[
"
warning
"
]
file
=
sys
.
stderr
)
        
root
=
watch
[
"
watch
"
]
        
if
"
relative_path
"
in
watch
:
            
query
[
"
relative_root
"
]
=
watch
[
"
relative_path
"
]
        
query
[
"
since
"
]
=
self
.
client
.
query
(
"
clock
"
root
{
"
sync_timeout
"
:
30000
}
)
[
            
"
clock
"
        
]
        
return
self
.
client
.
query
(
"
subscribe
"
root
name
query
)
    
def
changed_files
(
self
)
:
        
files
=
set
(
)
        
data
=
self
.
client
.
getSubscription
(
"
topsrcdir
"
)
        
if
data
:
            
for
dat
in
data
:
                
files
|
=
set
(
                    
[
                        
mozpath
.
normpath
(
                            
mozpath
.
join
(
self
.
config_environment
.
topsrcdir
f
)
                        
)
                        
for
f
in
dat
.
get
(
"
files
"
[
]
)
                    
]
                
)
        
return
files
    
def
incremental_copy
(
self
copier
force
=
False
verbose
=
True
)
:
        
if
"
cocoa
"
=
=
self
.
config_environment
.
substs
[
"
MOZ_WIDGET_TOOLKIT
"
]
:
            
bundledir
=
mozpath
.
join
(
                
self
.
config_environment
.
topobjdir
                
"
dist
"
                
self
.
config_environment
.
substs
[
"
MOZ_MACBUNDLE_NAME
"
]
                
"
Contents
"
                
"
Resources
"
            
)
            
start
=
time
.
monotonic
(
)
            
result
=
copier
.
copy
(
                
bundledir
                
skip_if_older
=
not
force
                
remove_unaccounted
=
False
                
remove_all_directory_symlinks
=
False
                
remove_empty_directories
=
False
            
)
            
print_copy_result
(
                
time
.
monotonic
(
)
-
start
bundledir
result
verbose
=
verbose
            
)
        
destdir
=
mozpath
.
join
(
self
.
config_environment
.
topobjdir
"
dist
"
"
bin
"
)
        
start
=
time
.
monotonic
(
)
        
result
=
copier
.
copy
(
            
destdir
            
skip_if_older
=
not
force
            
remove_unaccounted
=
False
            
remove_all_directory_symlinks
=
False
            
remove_empty_directories
=
False
        
)
        
print_copy_result
(
time
.
monotonic
(
)
-
start
destdir
result
verbose
=
verbose
)
    
def
input_changes
(
self
verbose
=
True
)
:
        
"
"
"
        
Return
an
iterator
of
FasterBuildChange
instances
as
inputs
        
to
the
faster
build
system
change
.
        
"
"
"
        
if
verbose
:
            
print_line
(
"
watch
"
"
Connecting
to
watchman
"
)
        
self
.
client
=
pywatchman
.
client
(
timeout
=
5
.
0
)
        
try
:
            
if
verbose
:
                
print_line
(
"
watch
"
"
Checking
watchman
capabilities
"
)
            
self
.
client
.
capabilityCheck
(
                
required
=
[
                    
"
clock
-
sync
-
timeout
"
                    
"
cmd
-
watch
-
project
"
                    
"
term
-
dirname
"
                    
"
wildmatch
"
                
]
            
)
            
if
verbose
:
                
print_line
(
                    
"
watch
"
                    
f
"
Subscribing
to
{
self
.
config_environment
.
topsrcdir
}
"
                
)
            
self
.
subscribe_to_topsrcdir
(
)
            
if
verbose
:
                
print_line
(
"
watch
"
f
"
Watching
{
self
.
config_environment
.
topsrcdir
}
"
)
            
input_to_outputs
=
self
.
file_copier
.
input_to_outputs_tree
(
)
            
for
input
outputs
in
input_to_outputs
.
items
(
)
:
                
if
not
outputs
:
                    
raise
Exception
(
                        
f
"
Refusing
to
watch
input
(
{
input
}
)
with
no
outputs
"
                    
)
            
while
True
:
                
try
:
                    
self
.
client
.
receive
(
)
                    
changed
=
self
.
changed_files
(
)
                    
if
not
changed
:
                        
continue
                    
result
=
FasterBuildChange
(
)
                    
for
change
in
changed
:
                        
if
change
in
input_to_outputs
:
                            
result
.
input_to_outputs
[
change
]
=
set
(
                                
input_to_outputs
[
change
]
                            
)
                        
else
:
                            
result
.
unrecognized
.
add
(
change
)
                    
for
input
outputs
in
result
.
input_to_outputs
.
items
(
)
:
                        
for
output
in
outputs
:
                            
if
output
not
in
result
.
output_to_inputs
:
                                
result
.
output_to_inputs
[
output
]
=
set
(
)
                            
result
.
output_to_inputs
[
output
]
.
add
(
input
)
                    
yield
result
                
except
pywatchman
.
SocketTimeout
:
                    
self
.
client
.
query
(
"
version
"
)
        
except
pywatchman
.
CommandError
as
e
:
            
raise
FasterBuildException
(
                
e
                
f
"
Command
error
using
pywatchman
to
watch
{
self
.
config_environment
.
topsrcdir
}
"
            
)
        
except
pywatchman
.
SocketTimeout
as
e
:
            
raise
FasterBuildException
(
                
e
                
f
"
Socket
timeout
using
pywatchman
to
watch
{
self
.
config_environment
.
topsrcdir
}
"
            
)
        
finally
:
            
self
.
client
.
close
(
)
    
def
output_changes
(
self
verbose
=
True
)
:
        
"
"
"
        
Return
an
iterator
of
FasterBuildChange
instances
as
outputs
        
from
the
faster
build
system
are
updated
.
        
"
"
"
        
for
change
in
self
.
input_changes
(
verbose
=
verbose
)
:
            
now
=
datetime
.
datetime
.
utcnow
(
)
            
for
unrecognized
in
sorted
(
change
.
unrecognized
)
:
                
print_line
(
"
watch
"
f
"
!
{
unrecognized
}
"
now
=
now
)
            
all_outputs
=
set
(
)
            
for
input
in
sorted
(
change
.
input_to_outputs
)
:
                
outputs
=
change
.
input_to_outputs
[
input
]
                
print_line
(
"
watch
"
f
"
<
{
input
}
"
now
=
now
)
                
for
output
in
sorted
(
outputs
)
:
                    
print_line
(
"
watch
"
f
"
>
{
output
}
"
now
=
now
)
                
all_outputs
|
=
outputs
            
if
all_outputs
:
                
partial_copier
=
FileCopier
(
)
                
for
output
in
all_outputs
:
                    
partial_copier
.
add
(
output
self
.
file_copier
[
output
]
)
                
self
.
incremental_copy
(
partial_copier
force
=
True
verbose
=
verbose
)
                
yield
change
    
def
watch
(
self
verbose
=
True
)
:
        
try
:
            
active_backend
=
self
.
config_environment
.
substs
.
get
(
                
"
BUILD_BACKENDS
"
[
None
]
            
)
[
0
]
            
if
active_backend
:
                
backend_cls
=
get_backend_class
(
active_backend
)
(
self
.
config_environment
)
        
except
Exception
:
            
backend_cls
=
None
        
for
change
in
self
.
output_changes
(
verbose
=
verbose
)
:
            
if
backend_cls
:
                
backend_cls
.
post_build
(
self
.
config_environment
None
1
False
0
)
