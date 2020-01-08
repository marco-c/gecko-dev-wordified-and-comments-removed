"
"
"
Transform
the
repackage
task
into
an
actual
task
description
.
"
"
"
from
__future__
import
absolute_import
print_function
unicode_literals
import
copy
from
taskgraph
.
transforms
.
base
import
TransformSequence
from
taskgraph
.
util
.
attributes
import
copy_attributes_from_dependent_job
from
taskgraph
.
util
.
schema
import
(
    
validate_schema
    
optionally_keyed_by
    
resolve_keyed_by
    
Schema
)
from
taskgraph
.
util
.
taskcluster
import
get_artifact_prefix
from
taskgraph
.
util
.
platforms
import
archive_format
executable_extension
from
taskgraph
.
util
.
workertypes
import
worker_type_implementation
from
taskgraph
.
transforms
.
task
import
task_description_schema
from
voluptuous
import
Any
Required
Optional
transforms
=
TransformSequence
(
)
task_description_schema
=
{
str
(
k
)
:
v
for
k
v
in
task_description_schema
.
schema
.
iteritems
(
)
}
taskref_or_string
=
Any
(
    
basestring
    
{
Required
(
'
task
-
reference
'
)
:
basestring
}
)
packaging_description_schema
=
Schema
(
{
    
Required
(
'
dependent
-
task
'
)
:
object
    
Required
(
'
depname
'
default
=
'
build
'
)
:
basestring
    
Optional
(
'
label
'
)
:
basestring
    
Optional
(
'
treeherder
'
)
:
task_description_schema
[
'
treeherder
'
]
    
Optional
(
'
locale
'
)
:
basestring
    
Optional
(
'
routes
'
)
:
[
basestring
]
    
Optional
(
'
extra
'
)
:
task_description_schema
[
'
extra
'
]
    
Optional
(
'
shipping
-
product
'
)
:
task_description_schema
[
'
shipping
-
product
'
]
    
Optional
(
'
shipping
-
phase
'
)
:
task_description_schema
[
'
shipping
-
phase
'
]
    
Required
(
'
package
-
formats
'
)
:
optionally_keyed_by
(
'
build
-
platform
'
'
project
'
[
basestring
]
)
    
Required
(
'
mozharness
'
)
:
{
        
Required
(
'
config
'
)
:
optionally_keyed_by
(
'
build
-
platform
'
[
basestring
]
)
        
Optional
(
'
config
-
paths
'
)
:
[
basestring
]
        
Required
(
'
comm
-
checkout
'
default
=
False
)
:
bool
    
}
}
)
PACKAGE_FORMATS
=
{
    
'
mar
'
:
{
        
'
args
'
:
[
'
mar
'
]
        
'
inputs
'
:
{
            
'
input
'
:
'
target
{
archive_format
}
'
            
'
mar
'
:
'
mar
{
executable_extension
}
'
        
}
        
'
output
'
:
"
target
.
complete
.
mar
"
    
}
    
'
mar
-
bz2
'
:
{
        
'
args
'
:
[
'
mar
'
"
-
-
format
"
"
bz2
"
]
        
'
inputs
'
:
{
            
'
input
'
:
'
target
{
archive_format
}
'
            
'
mar
'
:
'
mar
{
executable_extension
}
'
        
}
        
'
output
'
:
"
target
.
bz2
.
complete
.
mar
"
    
}
    
'
dmg
'
:
{
        
'
args
'
:
[
'
dmg
'
]
        
'
inputs
'
:
{
            
'
input
'
:
'
target
{
archive_format
}
'
        
}
        
'
output
'
:
"
target
.
dmg
"
    
}
    
'
installer
'
:
{
        
'
args
'
:
[
            
"
installer
"
            
"
-
-
package
-
name
"
"
firefox
"
            
"
-
-
tag
"
"
{
installer
-
tag
}
"
            
"
-
-
sfx
-
stub
"
"
{
sfx
-
stub
}
"
        
]
        
'
inputs
'
:
{
            
'
package
'
:
'
target
{
archive_format
}
'
            
"
setupexe
"
:
"
setup
.
exe
"
        
}
        
'
output
'
:
"
target
.
installer
.
exe
"
    
}
    
'
installer
-
stub
'
:
{
        
'
args
'
:
[
            
"
installer
"
            
"
-
-
tag
"
"
{
stub
-
installer
-
tag
}
"
            
"
-
-
sfx
-
stub
"
"
{
sfx
-
stub
}
"
        
]
        
'
inputs
'
:
{
            
"
setupexe
"
:
"
setup
-
stub
.
exe
"
        
}
        
'
output
'
:
'
target
.
stub
-
installer
.
exe
'
    
}
}
transforms
.
add
def
validate
(
config
jobs
)
:
    
for
job
in
jobs
:
        
label
=
job
.
get
(
'
dependent
-
task
'
object
)
.
__dict__
.
get
(
'
label
'
'
?
no
-
label
?
'
)
        
validate_schema
(
            
packaging_description_schema
job
            
"
In
packaging
(
{
!
r
}
kind
)
task
for
{
!
r
}
:
"
.
format
(
config
.
kind
label
)
)
        
yield
job
transforms
.
add
def
copy_in_useful_magic
(
config
jobs
)
:
    
"
"
"
Copy
attributes
from
upstream
task
to
be
used
for
keyed
configuration
.
"
"
"
    
for
job
in
jobs
:
        
dep
=
job
[
'
dependent
-
task
'
]
        
job
[
'
build
-
platform
'
]
=
dep
.
attributes
.
get
(
"
build_platform
"
)
        
yield
job
transforms
.
add
def
handle_keyed_by
(
config
jobs
)
:
    
"
"
"
Resolve
fields
that
can
be
keyed
by
platform
etc
.
"
"
"
    
fields
=
[
        
'
mozharness
.
config
'
        
'
package
-
formats
'
    
]
    
for
job
in
jobs
:
        
job
=
copy
.
deepcopy
(
job
)
        
for
field
in
fields
:
            
resolve_keyed_by
(
                
item
=
job
field
=
field
                
project
=
config
.
params
[
'
project
'
]
                
item_name
=
"
?
"
            
)
        
yield
job
transforms
.
add
def
make_repackage_description
(
config
jobs
)
:
    
for
job
in
jobs
:
        
dep_job
=
job
[
'
dependent
-
task
'
]
        
label
=
job
.
get
(
'
label
'
                        
dep_job
.
label
.
replace
(
"
signing
-
"
"
repackage
-
"
)
)
        
job
[
'
label
'
]
=
label
        
yield
job
transforms
.
add
def
make_job_description
(
config
jobs
)
:
    
for
job
in
jobs
:
        
dep_job
=
job
[
'
dependent
-
task
'
]
        
dependencies
=
{
dep_job
.
attributes
.
get
(
'
kind
'
)
:
dep_job
.
label
}
        
if
len
(
dep_job
.
dependencies
)
>
1
:
            
raise
NotImplementedError
(
                
"
Can
'
t
repackage
a
signing
task
with
multiple
dependencies
"
)
        
signing_dependencies
=
dep_job
.
dependencies
        
dependencies
.
update
(
signing_dependencies
)
        
attributes
=
copy_attributes_from_dependent_job
(
dep_job
)
        
treeherder
=
job
.
get
(
'
treeherder
'
{
}
)
        
if
attributes
.
get
(
'
nightly
'
)
:
            
treeherder
.
setdefault
(
'
symbol
'
'
Nr
'
)
        
else
:
            
treeherder
.
setdefault
(
'
symbol
'
'
Rpk
'
)
        
dep_th_platform
=
dep_job
.
task
.
get
(
'
extra
'
{
}
)
.
get
(
            
'
treeherder
'
{
}
)
.
get
(
'
machine
'
{
}
)
.
get
(
'
platform
'
'
'
)
        
treeherder
.
setdefault
(
'
platform
'
"
{
}
/
opt
"
.
format
(
dep_th_platform
)
)
        
treeherder
.
setdefault
(
'
tier
'
1
)
        
treeherder
.
setdefault
(
'
kind
'
'
build
'
)
        
build_task
=
None
        
signing_task
=
None
        
for
dependency
in
dependencies
.
keys
(
)
:
            
if
'
signing
'
in
dependency
:
                
signing_task
=
dependency
            
else
:
                
build_task
=
dependency
        
if
job
.
get
(
'
locale
'
)
:
            
dependencies
[
'
build
'
]
=
"
build
-
{
}
/
opt
"
.
format
(
                
dependencies
[
build_task
]
[
13
:
dependencies
[
build_task
]
.
rfind
(
'
-
'
)
]
)
            
build_task
=
'
build
'
        
attributes
=
copy_attributes_from_dependent_job
(
dep_job
)
        
attributes
[
'
repackage_type
'
]
=
'
repackage
'
        
locale
=
None
        
if
job
.
get
(
'
locale
'
)
:
            
locale
=
job
[
'
locale
'
]
            
attributes
[
'
locale
'
]
=
locale
        
level
=
config
.
params
[
'
level
'
]
        
build_platform
=
attributes
[
'
build_platform
'
]
        
use_stub
=
attributes
.
get
(
'
stub
-
installer
'
)
        
repackage_config
=
[
]
        
package_formats
=
job
.
get
(
'
package
-
formats
'
)
        
if
use_stub
:
            
package_formats
+
=
[
'
installer
-
stub
'
]
        
for
format
in
package_formats
:
            
command
=
copy
.
deepcopy
(
PACKAGE_FORMATS
[
format
]
)
            
substs
=
{
                
'
archive_format
'
:
archive_format
(
build_platform
)
                
'
executable_extension
'
:
executable_extension
(
build_platform
)
            
}
            
command
[
'
inputs
'
]
=
{
                
name
:
filename
.
format
(
*
*
substs
)
                
for
name
filename
in
command
[
'
inputs
'
]
.
items
(
)
            
}
            
repackage_config
.
append
(
command
)
        
run
=
job
.
get
(
'
mozharness
'
{
}
)
        
run
.
update
(
{
            
'
using
'
:
'
mozharness
'
            
'
script
'
:
'
mozharness
/
scripts
/
repackage
.
py
'
            
'
job
-
script
'
:
'
taskcluster
/
scripts
/
builder
/
repackage
.
sh
'
            
'
actions
'
:
[
'
setup
'
'
repackage
'
]
            
'
extra
-
workspace
-
cache
-
key
'
:
'
repackage
'
            
'
extra
-
config
'
:
{
                
'
repackage_config
'
:
repackage_config
            
}
        
}
)
        
worker
=
{
            
'
chain
-
of
-
trust
'
:
True
            
'
max
-
run
-
time
'
:
7200
if
build_platform
.
startswith
(
'
win
'
)
else
3600
            
'
skip
-
artifacts
'
:
True
        
}
        
if
locale
:
            
worker
.
setdefault
(
'
env
'
{
}
)
.
update
(
LOCALE
=
locale
)
        
if
build_platform
.
startswith
(
'
win
'
)
:
            
worker_type
=
'
aws
-
provisioner
-
v1
/
gecko
-
%
s
-
b
-
win2012
'
%
level
            
run
[
'
use
-
magic
-
mh
-
args
'
]
=
False
        
else
:
            
if
build_platform
.
startswith
(
(
'
linux
'
'
macosx
'
)
)
:
                
worker_type
=
'
aws
-
provisioner
-
v1
/
gecko
-
%
s
-
b
-
linux
'
%
level
            
else
:
                
raise
NotImplementedError
(
                    
'
Unsupported
build_platform
:
"
{
}
"
'
.
format
(
build_platform
)
                
)
            
run
[
'
tooltool
-
downloads
'
]
=
'
internal
'
            
worker
[
'
docker
-
image
'
]
=
{
"
in
-
tree
"
:
"
debian7
-
amd64
-
build
"
}
        
worker
[
'
artifacts
'
]
=
_generate_task_output_files
(
            
dep_job
worker_type_implementation
(
worker_type
)
            
repackage_config
=
repackage_config
            
locale
=
locale
        
)
        
description
=
(
            
"
Repackaging
for
locale
'
{
locale
}
'
for
build
'
"
            
"
{
build_platform
}
/
{
build_type
}
'
"
.
format
(
                
locale
=
attributes
.
get
(
'
locale
'
'
en
-
US
'
)
                
build_platform
=
attributes
.
get
(
'
build_platform
'
)
                
build_type
=
attributes
.
get
(
'
build_type
'
)
            
)
        
)
        
task
=
{
            
'
label
'
:
job
[
'
label
'
]
            
'
description
'
:
description
            
'
worker
-
type
'
:
worker_type
            
'
dependencies
'
:
dependencies
            
'
attributes
'
:
attributes
            
'
run
-
on
-
projects
'
:
dep_job
.
attributes
.
get
(
'
run_on_projects
'
)
            
'
treeherder
'
:
treeherder
            
'
routes
'
:
job
.
get
(
'
routes
'
[
]
)
            
'
extra
'
:
job
.
get
(
'
extra
'
{
}
)
            
'
worker
'
:
worker
            
'
run
'
:
run
            
'
fetches
'
:
_generate_download_config
(
dep_job
build_platform
build_task
                                                 
signing_task
locale
=
locale
                                                 
project
=
config
.
params
[
"
project
"
]
)
            
'
release
-
artifacts
'
:
[
artifact
[
'
name
'
]
for
artifact
in
worker
[
'
artifacts
'
]
]
        
}
        
if
build_platform
.
startswith
(
'
macosx
'
)
:
            
task
[
'
toolchains
'
]
=
[
                
'
linux64
-
libdmg
'
                
'
linux64
-
hfsplus
'
                
'
linux64
-
node
'
            
]
        
yield
task
def
_generate_download_config
(
task
build_platform
build_task
signing_task
locale
=
None
                              
project
=
None
)
:
    
locale_path
=
'
{
}
/
'
.
format
(
locale
)
if
locale
else
'
'
    
if
build_platform
.
startswith
(
'
linux
'
)
or
build_platform
.
startswith
(
'
macosx
'
)
:
        
return
{
            
signing_task
:
[
                
{
                    
'
artifact
'
:
'
{
}
target
{
}
'
.
format
(
locale_path
archive_format
(
build_platform
)
)
                    
'
extract
'
:
False
                
}
            
]
            
build_task
:
[
                
'
host
/
bin
/
mar
'
            
]
        
}
    
elif
build_platform
.
startswith
(
'
win
'
)
:
        
fetch_config
=
{
            
signing_task
:
[
                
{
                    
'
artifact
'
:
'
{
}
target
.
zip
'
.
format
(
locale_path
)
                    
'
extract
'
:
False
                
}
                
'
{
}
setup
.
exe
'
.
format
(
locale_path
)
            
]
            
build_task
:
[
                
'
host
/
bin
/
mar
.
exe
'
            
]
        
}
        
use_stub
=
task
.
attributes
.
get
(
'
stub
-
installer
'
)
        
if
use_stub
:
            
fetch_config
[
signing_task
]
.
append
(
'
{
}
setup
-
stub
.
exe
'
.
format
(
locale_path
)
)
        
return
fetch_config
    
raise
NotImplementedError
(
'
Unsupported
build_platform
:
"
{
}
"
'
.
format
(
build_platform
)
)
def
_generate_task_output_files
(
task
worker_implementation
repackage_config
locale
=
None
)
:
    
locale_output_path
=
'
{
}
/
'
.
format
(
locale
)
if
locale
else
'
'
    
artifact_prefix
=
get_artifact_prefix
(
task
)
    
if
worker_implementation
=
=
(
'
docker
-
worker
'
'
linux
'
)
:
        
local_prefix
=
'
/
builds
/
worker
/
workspace
/
'
    
elif
worker_implementation
=
=
(
'
generic
-
worker
'
'
windows
'
)
:
        
local_prefix
=
'
'
    
else
:
        
raise
NotImplementedError
(
            
'
Unsupported
worker
implementation
:
"
{
}
"
'
.
format
(
worker_implementation
)
)
    
output_files
=
[
]
    
for
config
in
repackage_config
:
        
output_files
.
append
(
{
            
'
type
'
:
'
file
'
            
'
path
'
:
'
{
}
build
/
outputs
/
{
}
{
}
'
                    
.
format
(
local_prefix
locale_output_path
config
[
'
output
'
]
)
            
'
name
'
:
'
{
}
/
{
}
{
}
'
.
format
(
artifact_prefix
locale_output_path
config
[
'
output
'
]
)
        
}
)
    
return
output_files
