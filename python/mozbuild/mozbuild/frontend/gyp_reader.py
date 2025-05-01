import
os
import
sys
import
time
from
collections
.
abc
import
Iterable
import
gyp
import
gyp
.
msvs_emulation
import
mozpack
.
path
as
mozpath
import
six
from
mozpack
.
files
import
FileFinder
from
mozbuild
import
shellutil
from
mozbuild
.
util
import
expand_variables
from
.
context
import
VARIABLES
ObjDirPath
SourcePath
TemplateContext
from
.
sandbox
import
alphabetical_sorted
sys
.
modules
[
"
gyp
.
generator
.
mozbuild
"
]
=
sys
.
modules
[
__name__
]
chrome_src
=
mozpath
.
abspath
(
    
mozpath
.
join
(
mozpath
.
dirname
(
gyp
.
__file__
)
"
.
.
/
.
.
/
.
.
/
.
.
/
.
.
"
)
)
script_dir
=
mozpath
.
join
(
chrome_src
"
build
"
)
generator_default_variables
=
{
}
for
dirname
in
[
    
"
INTERMEDIATE_DIR
"
    
"
SHARED_INTERMEDIATE_DIR
"
    
"
PRODUCT_DIR
"
    
"
LIB_DIR
"
    
"
SHARED_LIB_DIR
"
]
:
    
generator_default_variables
[
dirname
]
=
"
"
+
dirname
for
unused
in
[
    
"
RULE_INPUT_PATH
"
    
"
RULE_INPUT_ROOT
"
    
"
RULE_INPUT_NAME
"
    
"
RULE_INPUT_DIRNAME
"
    
"
RULE_INPUT_EXT
"
    
"
EXECUTABLE_PREFIX
"
    
"
EXECUTABLE_SUFFIX
"
    
"
STATIC_LIB_PREFIX
"
    
"
STATIC_LIB_SUFFIX
"
    
"
SHARED_LIB_PREFIX
"
    
"
SHARED_LIB_SUFFIX
"
    
"
LINKER_SUPPORTS_ICF
"
]
:
    
generator_default_variables
[
unused
]
=
"
"
class
GypContext
(
TemplateContext
)
:
    
"
"
"
Specialized
Context
for
use
with
data
extracted
from
Gyp
.
    
config
is
the
ConfigEnvironment
for
this
context
.
    
relobjdir
is
the
object
directory
that
will
be
used
for
this
context
    
relative
to
the
topobjdir
defined
in
the
ConfigEnvironment
.
    
"
"
"
    
def
__init__
(
self
config
relobjdir
)
:
        
self
.
_relobjdir
=
relobjdir
        
TemplateContext
.
__init__
(
            
self
template
=
"
Gyp
"
allowed_variables
=
VARIABLES
config
=
config
        
)
def
handle_actions
(
actions
context
action_overrides
)
:
    
idir
=
"
INTERMEDIATE_DIR
/
"
    
for
action
in
actions
:
        
name
=
action
[
"
action_name
"
]
        
if
name
not
in
action_overrides
:
            
raise
RuntimeError
(
"
GYP
action
%
s
not
listed
in
action_overrides
"
%
name
)
        
outputs
=
action
[
"
outputs
"
]
        
if
len
(
outputs
)
>
1
:
            
raise
NotImplementedError
(
                
"
GYP
actions
with
more
than
one
output
not
supported
:
%
s
"
%
name
            
)
        
output
=
outputs
[
0
]
        
if
not
output
.
startswith
(
idir
)
:
            
raise
NotImplementedError
(
                
"
GYP
actions
outputting
to
somewhere
other
than
"
                
"
<
(
INTERMEDIATE_DIR
)
not
supported
:
%
s
"
%
output
            
)
        
output
=
output
[
len
(
idir
)
:
]
        
context
[
"
GENERATED_FILES
"
]
+
=
[
output
]
        
g
=
context
[
"
GENERATED_FILES
"
]
[
output
]
        
g
.
script
=
action_overrides
[
name
]
        
g
.
inputs
=
action
[
"
inputs
"
]
def
handle_copies
(
copies
context
)
:
    
dist
=
"
PRODUCT_DIR
/
dist
/
"
    
for
copy
in
copies
:
        
dest
=
copy
[
"
destination
"
]
        
if
not
dest
.
startswith
(
dist
)
:
            
raise
NotImplementedError
(
                
"
GYP
copies
to
somewhere
other
than
<
(
PRODUCT_DIR
)
/
dist
not
supported
:
%
s
"
                
%
dest
            
)
        
dest_paths
=
dest
[
len
(
dist
)
:
]
.
split
(
"
/
"
)
        
exports
=
context
[
"
EXPORTS
"
]
        
while
dest_paths
:
            
exports
=
getattr
(
exports
dest_paths
.
pop
(
0
)
)
        
exports
+
=
sorted
(
copy
[
"
files
"
]
key
=
lambda
x
:
x
.
lower
(
)
)
def
process_gyp_result
(
    
gyp_result
    
gyp_dir_attrs
    
path
    
config
    
output
    
non_unified_sources
    
action_overrides
)
:
    
flat_list
targets
data
=
gyp_result
    
no_chromium
=
gyp_dir_attrs
.
no_chromium
    
no_unified
=
gyp_dir_attrs
.
no_unified
    
for
target
in
sorted
(
        
gyp
.
common
.
AllTargets
(
flat_list
targets
path
.
replace
(
"
/
"
os
.
sep
)
)
    
)
:
        
build_file
target_name
toolset
=
gyp
.
common
.
ParseQualifiedTarget
(
target
)
        
reldir
=
mozpath
.
relpath
(
mozpath
.
dirname
(
build_file
)
mozpath
.
dirname
(
path
)
)
        
subdir
=
"
%
s_
%
s
"
%
(
            
mozpath
.
splitext
(
mozpath
.
basename
(
build_file
)
)
[
0
]
            
target_name
        
)
        
context
=
GypContext
(
            
config
            
mozpath
.
relpath
(
mozpath
.
join
(
output
reldir
subdir
)
config
.
topobjdir
)
        
)
        
context
.
add_source
(
mozpath
.
abspath
(
build_file
)
)
        
for
f
in
data
[
build_file
]
[
"
included_files
"
]
:
            
context
.
add_source
(
                
mozpath
.
abspath
(
mozpath
.
join
(
mozpath
.
dirname
(
build_file
)
f
)
)
            
)
        
spec
=
targets
[
target
]
        
c
=
"
Debug
"
if
config
.
substs
.
get
(
"
MOZ_DEBUG
"
)
else
"
Release
"
        
if
c
not
in
spec
[
"
configurations
"
]
:
            
raise
RuntimeError
(
                
"
Missing
%
s
gyp
configuration
for
target
%
s
"
                
"
in
%
s
"
%
(
c
target_name
build_file
)
            
)
        
target_conf
=
spec
[
"
configurations
"
]
[
c
]
        
if
"
actions
"
in
spec
:
            
handle_actions
(
spec
[
"
actions
"
]
context
action_overrides
)
        
if
"
copies
"
in
spec
:
            
handle_copies
(
spec
[
"
copies
"
]
context
)
        
use_libs
=
[
]
        
libs
=
[
]
        
def
add_deps
(
s
)
:
            
for
t
in
s
.
get
(
"
dependencies
"
[
]
)
+
s
.
get
(
"
dependencies_original
"
[
]
)
:
                
ty
=
targets
[
t
]
[
"
type
"
]
                
if
ty
in
(
"
static_library
"
"
shared_library
"
)
:
                    
l
=
targets
[
t
]
[
"
target_name
"
]
                    
if
l
not
in
use_libs
:
                        
use_libs
.
append
(
l
)
                
if
ty
in
(
"
static_library
"
"
none
"
)
:
                    
add_deps
(
targets
[
t
]
)
            
libs
.
extend
(
spec
.
get
(
"
libraries
"
[
]
)
)
        
if
no_chromium
:
            
add_deps
(
spec
)
        
os_libs
=
[
]
        
for
l
in
libs
:
            
if
l
.
startswith
(
"
-
"
)
:
                
if
l
.
startswith
(
"
-
l
"
)
:
                    
l
=
l
[
2
:
]
                
if
l
not
in
os_libs
:
                    
os_libs
.
append
(
l
)
            
elif
l
.
endswith
(
"
.
lib
"
)
:
                
l
=
l
[
:
-
4
]
                
if
l
not
in
os_libs
:
                    
os_libs
.
append
(
l
)
            
elif
l
:
                
l
=
os
.
path
.
basename
(
l
)
                
if
l
not
in
use_libs
:
                    
use_libs
.
append
(
l
)
        
if
spec
[
"
type
"
]
=
=
"
none
"
:
            
if
not
(
"
actions
"
in
spec
or
"
copies
"
in
spec
)
:
                
continue
        
elif
spec
[
"
type
"
]
in
(
"
static_library
"
"
shared_library
"
"
executable
"
)
:
            
name
=
six
.
ensure_text
(
spec
[
"
target_name
"
]
)
            
if
spec
[
"
type
"
]
in
(
"
static_library
"
"
shared_library
"
)
:
                
if
name
.
startswith
(
"
lib
"
)
:
                    
name
=
name
[
3
:
]
                
context
[
"
LIBRARY_NAME
"
]
=
name
            
else
:
                
context
[
"
PROGRAM
"
]
=
name
            
if
spec
[
"
type
"
]
=
=
"
shared_library
"
:
                
context
[
"
FORCE_SHARED_LIB
"
]
=
True
            
elif
(
                
spec
[
"
type
"
]
=
=
"
static_library
"
                
and
spec
.
get
(
"
variables
"
{
}
)
.
get
(
"
no_expand_libs
"
"
0
"
)
=
=
"
1
"
            
)
:
                
context
[
"
NO_EXPAND_LIBS
"
]
=
True
            
if
use_libs
:
                
context
[
"
USE_LIBS
"
]
=
sorted
(
use_libs
key
=
lambda
s
:
s
.
lower
(
)
)
            
if
os_libs
:
                
context
[
"
OS_LIBS
"
]
=
os_libs
            
sources
=
[
]
            
unified_sources
=
[
]
            
extensions
=
set
(
)
            
use_defines_in_asflags
=
False
            
for
f
in
spec
.
get
(
"
sources
"
[
]
)
:
                
ext
=
mozpath
.
splitext
(
f
)
[
-
1
]
                
extensions
.
add
(
ext
)
                
if
f
.
startswith
(
"
INTERMEDIATE_DIR
/
"
)
:
                    
s
=
ObjDirPath
(
context
f
.
replace
(
"
INTERMEDIATE_DIR
/
"
"
!
"
)
)
                
else
:
                    
s
=
SourcePath
(
context
f
)
                
if
ext
=
=
"
.
h
"
:
                    
continue
                
if
ext
=
=
"
.
def
"
:
                    
context
[
"
SYMBOLS_FILE
"
]
=
s
                
elif
ext
!
=
"
.
S
"
and
not
no_unified
and
s
not
in
non_unified_sources
:
                    
unified_sources
.
append
(
s
)
                
else
:
                    
sources
.
append
(
s
)
                
if
ext
=
=
"
.
s
"
:
                    
use_defines_in_asflags
=
True
            
context
[
"
SOURCES
"
]
=
alphabetical_sorted
(
sources
)
            
context
[
"
UNIFIED_SOURCES
"
]
=
alphabetical_sorted
(
unified_sources
)
            
defines
=
target_conf
.
get
(
"
defines
"
[
]
)
            
if
config
.
substs
[
"
CC_TYPE
"
]
=
=
"
clang
-
cl
"
and
no_chromium
:
                
msvs_settings
=
gyp
.
msvs_emulation
.
MsvsSettings
(
spec
{
}
)
                
msvs_settings
.
vs_version
.
short_name
=
int
(
                    
msvs_settings
.
vs_version
.
short_name
                
)
                
defines
.
extend
(
msvs_settings
.
GetComputedDefines
(
c
)
)
            
for
define
in
defines
:
                
if
"
=
"
in
define
:
                    
name
value
=
define
.
split
(
"
=
"
1
)
                    
context
[
"
DEFINES
"
]
[
name
]
=
value
                
else
:
                    
context
[
"
DEFINES
"
]
[
define
]
=
True
            
product_dir_dist
=
"
PRODUCT_DIR
/
dist
/
"
            
for
include
in
target_conf
.
get
(
"
include_dirs
"
[
]
)
:
                
if
include
.
startswith
(
product_dir_dist
)
:
                    
include
=
"
!
/
dist
/
include
/
"
+
include
[
len
(
product_dir_dist
)
:
]
                
elif
include
.
startswith
(
config
.
topobjdir
)
:
                    
include
=
"
!
/
"
+
mozpath
.
relpath
(
include
config
.
topobjdir
)
                
else
:
                    
if
include
.
startswith
(
"
/
"
)
:
                        
resolved
=
mozpath
.
abspath
(
                            
mozpath
.
join
(
config
.
topsrcdir
include
[
1
:
]
)
                        
)
                    
elif
not
include
.
startswith
(
(
"
!
"
"
%
"
)
)
:
                        
resolved
=
mozpath
.
abspath
(
                            
mozpath
.
join
(
mozpath
.
dirname
(
build_file
)
include
)
                        
)
                    
if
not
include
.
startswith
(
(
"
!
"
"
%
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
                        
resolved
                    
)
:
                        
continue
                
context
[
"
LOCAL_INCLUDES
"
]
+
=
[
include
]
            
context
[
"
ASFLAGS
"
]
=
target_conf
.
get
(
"
asflags_mozilla
"
[
]
)
            
if
use_defines_in_asflags
and
defines
:
                
context
[
"
ASFLAGS
"
]
+
=
[
"
-
D
"
+
d
for
d
in
defines
]
            
if
config
.
substs
[
"
OS_TARGET
"
]
=
=
"
SunOS
"
:
                
context
[
"
LDFLAGS
"
]
=
target_conf
.
get
(
"
ldflags
"
[
]
)
            
flags
=
target_conf
.
get
(
"
cflags_mozilla
"
[
]
)
            
if
flags
:
                
suffix_map
=
{
                    
"
.
c
"
:
"
CFLAGS
"
                    
"
.
cpp
"
:
"
CXXFLAGS
"
                    
"
.
cc
"
:
"
CXXFLAGS
"
                    
"
.
m
"
:
"
CMFLAGS
"
                    
"
.
mm
"
:
"
CMMFLAGS
"
                
}
                
variables
=
(
suffix_map
[
e
]
for
e
in
extensions
if
e
in
suffix_map
)
                
for
var
in
variables
:
                    
for
f
in
flags
:
                        
f
=
expand_variables
(
f
config
.
substs
)
.
split
(
)
                        
if
not
f
:
                            
continue
                        
if
isinstance
(
f
str
)
:
                            
context
[
var
]
.
append
(
f
)
                        
else
:
                            
context
[
var
]
.
extend
(
f
)
        
else
:
            
raise
NotImplementedError
(
"
Unsupported
gyp
target
type
:
%
s
"
%
spec
[
"
type
"
]
)
        
if
not
no_chromium
:
            
context
[
"
LOCAL_INCLUDES
"
]
+
=
[
                
"
!
/
ipc
/
ipdl
/
_ipdlheaders
"
                
"
/
ipc
/
chromium
/
src
"
            
]
            
if
config
.
substs
[
"
OS_TARGET
"
]
=
=
"
WINNT
"
:
                
context
[
"
DEFINES
"
]
[
"
UNICODE
"
]
=
True
                
context
[
"
DEFINES
"
]
[
"
_UNICODE
"
]
=
True
        
context
[
"
COMPILE_FLAGS
"
]
[
"
OS_INCLUDES
"
]
=
[
]
        
for
key
value
in
gyp_dir_attrs
.
sandbox_vars
.
items
(
)
:
            
if
context
.
get
(
key
)
and
isinstance
(
context
[
key
]
list
)
:
                
context
[
key
]
=
value
+
context
[
key
]
            
elif
context
.
get
(
key
)
and
isinstance
(
context
[
key
]
dict
)
:
                
context
[
key
]
.
update
(
value
)
            
else
:
                
context
[
key
]
=
value
        
yield
context
def
load_gyp
(
*
args
)
:
    
_
flat_list
targets
data
=
gyp
.
Load
(
*
args
)
    
return
flat_list
targets
data
class
GypProcessor
:
    
"
"
"
Reads
a
gyp
configuration
in
the
background
using
the
given
executor
and
    
emits
GypContexts
for
the
backend
to
process
.
    
config
is
a
ConfigEnvironment
path
is
the
path
to
a
root
gyp
configuration
    
file
and
output
is
the
base
path
under
which
the
objdir
for
the
various
    
gyp
dependencies
will
be
.
gyp_dir_attrs
are
attributes
set
for
the
dir
    
from
moz
.
build
.
    
"
"
"
    
def
__init__
(
        
self
        
config
        
gyp_dir_attrs
        
path
        
output
        
executor
        
action_overrides
        
non_unified_sources
    
)
:
        
self
.
_path
=
path
        
self
.
_config
=
config
        
self
.
_output
=
output
        
self
.
_non_unified_sources
=
non_unified_sources
        
self
.
_gyp_dir_attrs
=
gyp_dir_attrs
        
self
.
_action_overrides
=
action_overrides
        
self
.
execution_time
=
0
.
0
        
self
.
_results
=
[
]
        
if
config
.
substs
[
"
CC_TYPE
"
]
=
=
"
clang
-
cl
"
:
            
os
.
environ
.
update
(
                
{
                    
"
GYP_MSVS_OVERRIDE_PATH
"
:
"
fake_path
"
                    
"
GYP_MSVS_VERSION
"
:
config
.
substs
[
"
MSVS_VERSION
"
]
                
}
            
)
        
params
=
{
            
"
parallel
"
:
False
            
"
generator_flags
"
:
{
}
            
"
build_files
"
:
[
path
]
            
"
root_targets
"
:
None
        
}
        
os
.
environ
.
update
(
            
CC
=
config
.
substs
[
"
CC
"
]
            
CFLAGS
=
shellutil
.
quote
(
*
config
.
substs
[
"
CC_BASE_FLAGS
"
]
)
        
)
        
if
gyp_dir_attrs
.
no_chromium
:
            
includes
=
[
]
            
depth
=
mozpath
.
dirname
(
path
)
        
else
:
            
depth
=
chrome_src
            
includes
=
[
mozpath
.
join
(
script_dir
"
gyp_includes
"
"
common
.
gypi
"
)
]
            
finder
=
FileFinder
(
chrome_src
)
            
includes
.
extend
(
                
mozpath
.
join
(
chrome_src
name
)
                
for
name
_
in
finder
.
find
(
"
*
/
supplement
.
gypi
"
)
            
)
        
def
normalize
(
obj
)
:
            
if
isinstance
(
obj
dict
)
:
                
return
{
k
:
normalize
(
v
)
for
k
v
in
obj
.
items
(
)
}
            
if
isinstance
(
obj
str
)
:
                
return
str
(
obj
)
            
if
isinstance
(
obj
Iterable
)
:
                
return
[
normalize
(
o
)
for
o
in
obj
]
            
return
obj
        
str_vars
=
normalize
(
gyp_dir_attrs
.
variables
)
        
str_vars
[
"
python
"
]
=
sys
.
executable
        
self
.
_gyp_loader_future
=
executor
.
submit
(
            
load_gyp
[
path
]
"
mozbuild
"
str_vars
includes
depth
params
        
)
    
property
    
def
results
(
self
)
:
        
if
self
.
_results
:
            
for
res
in
self
.
_results
:
                
yield
res
        
else
:
            
t0
=
time
.
monotonic
(
)
            
flat_list
targets
data
=
self
.
_gyp_loader_future
.
result
(
)
            
self
.
execution_time
+
=
time
.
monotonic
(
)
-
t0
            
results
=
[
]
            
for
res
in
process_gyp_result
(
                
(
flat_list
targets
data
)
                
self
.
_gyp_dir_attrs
                
self
.
_path
                
self
.
_config
                
self
.
_output
                
self
.
_non_unified_sources
                
self
.
_action_overrides
            
)
:
                
results
.
append
(
res
)
                
yield
res
            
self
.
_results
=
results
