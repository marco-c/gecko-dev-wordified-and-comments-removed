import
collections
import
copy
import
hashlib
import
json
import
multiprocessing
import
os
.
path
import
re
import
signal
import
subprocess
import
sys
import
gyp
import
gyp
.
common
from
gyp
.
common
import
OrderedSet
import
gyp
.
msvs_emulation
import
gyp
.
MSVSUtil
as
MSVSUtil
import
gyp
.
xcode_emulation
from
cStringIO
import
StringIO
from
gyp
.
common
import
GetEnvironFallback
import
gyp
.
ninja_syntax
as
ninja_syntax
generator_default_variables
=
{
  
'
EXECUTABLE_PREFIX
'
:
'
'
  
'
EXECUTABLE_SUFFIX
'
:
'
'
  
'
STATIC_LIB_PREFIX
'
:
'
lib
'
  
'
STATIC_LIB_SUFFIX
'
:
'
.
a
'
  
'
SHARED_LIB_PREFIX
'
:
'
lib
'
  
'
INTERMEDIATE_DIR
'
:
'
!
INTERMEDIATE_DIR
'
  
'
SHARED_INTERMEDIATE_DIR
'
:
'
!
PRODUCT_DIR
/
gen
'
  
'
PRODUCT_DIR
'
:
'
!
PRODUCT_DIR
'
  
'
CONFIGURATION_NAME
'
:
'
|
CONFIGURATION_NAME
'
  
'
RULE_INPUT_ROOT
'
:
'
{
root
}
'
  
'
RULE_INPUT_DIRNAME
'
:
'
{
dirname
}
'
  
'
RULE_INPUT_PATH
'
:
'
{
source
}
'
  
'
RULE_INPUT_EXT
'
:
'
{
ext
}
'
  
'
RULE_INPUT_NAME
'
:
'
{
name
}
'
}
generator_additional_non_configuration_keys
=
[
]
generator_additional_path_sections
=
[
]
generator_extra_sources_for_rules
=
[
]
generator_filelist_paths
=
None
generator_supports_multiple_toolsets
=
gyp
.
common
.
CrossCompileRequested
(
)
def
StripPrefix
(
arg
prefix
)
:
  
if
arg
.
startswith
(
prefix
)
:
    
return
arg
[
len
(
prefix
)
:
]
  
return
arg
def
QuoteShellArgument
(
arg
flavor
)
:
  
"
"
"
Quote
a
string
such
that
it
will
be
interpreted
as
a
single
argument
  
by
the
shell
.
"
"
"
  
if
re
.
match
(
r
'
^
[
a
-
zA
-
Z0
-
9_
=
.
\
\
/
-
]
+
'
arg
)
:
    
return
arg
  
if
flavor
=
=
'
win
'
:
    
return
gyp
.
msvs_emulation
.
QuoteForRspFile
(
arg
)
  
return
"
'
"
+
arg
.
replace
(
"
'
"
"
'
"
+
'
"
\
'
"
'
+
"
'
"
)
+
"
'
"
def
Define
(
d
flavor
)
:
  
"
"
"
Takes
a
preprocessor
define
and
returns
a
-
D
parameter
that
'
s
ninja
-
and
  
shell
-
escaped
.
"
"
"
  
if
flavor
=
=
'
win
'
:
    
d
=
d
.
replace
(
'
#
'
'
\
\
%
03o
'
%
ord
(
'
#
'
)
)
  
return
QuoteShellArgument
(
ninja_syntax
.
escape
(
'
-
D
'
+
d
)
flavor
)
def
AddArch
(
output
arch
)
:
  
"
"
"
Adds
an
arch
string
to
an
output
path
.
"
"
"
  
output
extension
=
os
.
path
.
splitext
(
output
)
  
return
'
%
s
.
%
s
%
s
'
%
(
output
arch
extension
)
class
Target
(
object
)
:
  
"
"
"
Target
represents
the
paths
used
within
a
single
gyp
target
.
  
Conceptually
building
a
single
target
A
is
a
series
of
steps
:
  
1
)
actions
/
rules
/
copies
generates
source
/
resources
/
etc
.
  
2
)
compiles
generates
.
o
files
  
3
)
link
generates
a
binary
(
library
/
executable
)
  
4
)
bundle
merges
the
above
in
a
mac
bundle
  
(
Any
of
these
steps
can
be
optional
.
)
  
From
a
build
ordering
perspective
a
dependent
target
B
could
just
  
depend
on
the
last
output
of
this
series
of
steps
.
  
But
some
dependent
commands
sometimes
need
to
reach
inside
the
box
.
  
For
example
when
linking
B
it
needs
to
get
the
path
to
the
static
  
library
generated
by
A
.
  
This
object
stores
those
paths
.
To
keep
things
simple
member
  
variables
only
store
concrete
paths
to
single
files
while
methods
  
compute
derived
values
like
"
the
last
output
of
the
target
"
.
  
"
"
"
  
def
__init__
(
self
type
)
:
    
self
.
type
=
type
    
self
.
preaction_stamp
=
None
    
self
.
precompile_stamp
=
None
    
self
.
actions_stamp
=
None
    
self
.
binary
=
None
    
self
.
bundle
=
None
    
self
.
component_objs
=
None
    
self
.
compile_deps
=
None
    
self
.
import_lib
=
None
    
self
.
uses_cpp
=
False
  
def
Linkable
(
self
)
:
    
"
"
"
Return
true
if
this
is
a
target
that
can
be
linked
against
.
"
"
"
    
return
self
.
type
in
(
'
static_library
'
'
shared_library
'
)
  
def
UsesToc
(
self
flavor
)
:
    
"
"
"
Return
true
if
the
target
should
produce
a
restat
rule
based
on
a
TOC
    
file
.
"
"
"
    
if
flavor
=
=
'
win
'
or
self
.
bundle
:
      
return
False
    
return
self
.
type
in
(
'
shared_library
'
'
loadable_module
'
)
  
def
PreActionInput
(
self
flavor
)
:
    
"
"
"
Return
the
path
if
any
that
should
be
used
as
a
dependency
of
    
any
dependent
action
step
.
"
"
"
    
if
self
.
UsesToc
(
flavor
)
:
      
return
self
.
FinalOutput
(
)
+
'
.
TOC
'
    
return
self
.
FinalOutput
(
)
or
self
.
preaction_stamp
  
def
PreCompileInput
(
self
)
:
    
"
"
"
Return
the
path
if
any
that
should
be
used
as
a
dependency
of
    
any
dependent
compile
step
.
"
"
"
    
return
self
.
actions_stamp
or
self
.
precompile_stamp
  
def
FinalOutput
(
self
)
:
    
"
"
"
Return
the
last
output
of
the
target
which
depends
on
all
prior
    
steps
.
"
"
"
    
return
self
.
bundle
or
self
.
binary
or
self
.
actions_stamp
class
NinjaWriter
(
object
)
:
  
def
__init__
(
self
hash_for_rules
target_outputs
base_dir
build_dir
               
output_file
toplevel_build
output_file_name
flavor
               
toplevel_dir
=
None
)
:
    
"
"
"
    
base_dir
:
path
from
source
root
to
directory
containing
this
gyp
file
              
by
gyp
semantics
all
input
paths
are
relative
to
this
    
build_dir
:
path
from
source
root
to
build
output
    
toplevel_dir
:
path
to
the
toplevel
directory
    
"
"
"
    
self
.
hash_for_rules
=
hash_for_rules
    
self
.
target_outputs
=
target_outputs
    
self
.
base_dir
=
base_dir
    
self
.
build_dir
=
build_dir
    
self
.
ninja
=
ninja_syntax
.
Writer
(
output_file
)
    
self
.
toplevel_build
=
toplevel_build
    
self
.
output_file_name
=
output_file_name
    
self
.
flavor
=
flavor
    
self
.
abs_build_dir
=
None
    
if
toplevel_dir
is
not
None
:
      
self
.
abs_build_dir
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
toplevel_dir
                                                        
build_dir
)
)
    
self
.
obj_ext
=
'
.
obj
'
if
flavor
=
=
'
win
'
else
'
.
o
'
    
if
flavor
=
=
'
win
'
:
      
self
.
win_env
=
{
}
      
for
arch
in
(
'
x86
'
'
x64
'
)
:
        
self
.
win_env
[
arch
]
=
'
environment
.
'
+
arch
    
build_to_top
=
gyp
.
common
.
InvertRelativePath
(
build_dir
toplevel_dir
)
    
self
.
build_to_base
=
os
.
path
.
join
(
build_to_top
base_dir
)
    
base_to_top
=
gyp
.
common
.
InvertRelativePath
(
base_dir
toplevel_dir
)
    
self
.
base_to_build
=
os
.
path
.
join
(
base_to_top
build_dir
)
  
def
ExpandSpecial
(
self
path
product_dir
=
None
)
:
    
"
"
"
Expand
specials
like
!
PRODUCT_DIR
in
|
path
|
.
    
If
|
product_dir
|
is
None
assumes
the
cwd
is
already
the
product
    
dir
.
Otherwise
|
product_dir
|
is
the
relative
path
to
the
product
    
dir
.
    
"
"
"
    
PRODUCT_DIR
=
'
!
PRODUCT_DIR
'
    
if
PRODUCT_DIR
in
path
:
      
if
product_dir
:
        
path
=
path
.
replace
(
PRODUCT_DIR
product_dir
)
      
else
:
        
path
=
path
.
replace
(
PRODUCT_DIR
+
'
/
'
'
'
)
        
path
=
path
.
replace
(
PRODUCT_DIR
+
'
\
\
'
'
'
)
        
path
=
path
.
replace
(
PRODUCT_DIR
'
.
'
)
    
INTERMEDIATE_DIR
=
'
!
INTERMEDIATE_DIR
'
    
if
INTERMEDIATE_DIR
in
path
:
      
int_dir
=
self
.
GypPathToUniqueOutput
(
'
gen
'
)
      
path
=
path
.
replace
(
INTERMEDIATE_DIR
                          
os
.
path
.
join
(
product_dir
or
'
'
int_dir
)
)
    
CONFIGURATION_NAME
=
'
|
CONFIGURATION_NAME
'
    
path
=
path
.
replace
(
CONFIGURATION_NAME
self
.
config_name
)
    
return
path
  
def
ExpandRuleVariables
(
self
path
root
dirname
source
ext
name
)
:
    
if
self
.
flavor
=
=
'
win
'
:
      
path
=
self
.
msvs_settings
.
ConvertVSMacros
(
          
path
config
=
self
.
config_name
)
    
path
=
path
.
replace
(
generator_default_variables
[
'
RULE_INPUT_ROOT
'
]
root
)
    
path
=
path
.
replace
(
generator_default_variables
[
'
RULE_INPUT_DIRNAME
'
]
                        
dirname
)
    
path
=
path
.
replace
(
generator_default_variables
[
'
RULE_INPUT_PATH
'
]
source
)
    
path
=
path
.
replace
(
generator_default_variables
[
'
RULE_INPUT_EXT
'
]
ext
)
    
path
=
path
.
replace
(
generator_default_variables
[
'
RULE_INPUT_NAME
'
]
name
)
    
return
path
  
def
GypPathToNinja
(
self
path
env
=
None
)
:
    
"
"
"
Translate
a
gyp
path
to
a
ninja
path
optionally
expanding
environment
    
variable
references
in
|
path
|
with
|
env
|
.
    
See
the
above
discourse
on
path
conversions
.
"
"
"
    
if
env
:
      
if
self
.
flavor
=
=
'
mac
'
:
        
path
=
gyp
.
xcode_emulation
.
ExpandEnvVars
(
path
env
)
      
elif
self
.
flavor
=
=
'
win
'
:
        
path
=
gyp
.
msvs_emulation
.
ExpandMacros
(
path
env
)
    
if
path
.
startswith
(
'
!
'
)
:
      
expanded
=
self
.
ExpandSpecial
(
path
)
      
if
self
.
flavor
=
=
'
win
'
:
        
expanded
=
os
.
path
.
normpath
(
expanded
)
      
return
expanded
    
if
'
|
'
in
path
:
      
path
=
self
.
ExpandSpecial
(
path
)
    
assert
'
'
not
in
path
path
    
return
os
.
path
.
normpath
(
os
.
path
.
join
(
self
.
build_to_base
path
)
)
  
def
GypPathToUniqueOutput
(
self
path
qualified
=
True
)
:
    
"
"
"
Translate
a
gyp
path
to
a
ninja
path
for
writing
output
.
    
If
qualified
is
True
qualify
the
resulting
filename
with
the
name
    
of
the
target
.
This
is
necessary
when
e
.
g
.
compiling
the
same
    
path
twice
for
two
separate
output
targets
.
    
See
the
above
discourse
on
path
conversions
.
"
"
"
    
path
=
self
.
ExpandSpecial
(
path
)
    
assert
not
path
.
startswith
(
'
'
)
path
    
obj
=
'
obj
'
    
if
self
.
toolset
!
=
'
target
'
:
      
obj
+
=
'
.
'
+
self
.
toolset
    
path_dir
path_basename
=
os
.
path
.
split
(
path
)
    
assert
not
os
.
path
.
isabs
(
path_dir
)
(
        
"
'
%
s
'
can
not
be
absolute
path
(
see
crbug
.
com
/
462153
)
.
"
%
path_dir
)
    
if
qualified
:
      
path_basename
=
self
.
name
+
'
.
'
+
path_basename
    
return
os
.
path
.
normpath
(
os
.
path
.
join
(
obj
self
.
base_dir
path_dir
                                         
path_basename
)
)
  
def
WriteCollapsedDependencies
(
self
name
targets
order_only
=
None
)
:
    
"
"
"
Given
a
list
of
targets
return
a
path
for
a
single
file
    
representing
the
result
of
building
all
the
targets
or
None
.
    
Uses
a
stamp
file
if
necessary
.
"
"
"
    
assert
targets
=
=
filter
(
None
targets
)
targets
    
if
len
(
targets
)
=
=
0
:
      
assert
not
order_only
      
return
None
    
if
len
(
targets
)
>
1
or
order_only
:
      
stamp
=
self
.
GypPathToUniqueOutput
(
name
+
'
.
stamp
'
)
      
targets
=
self
.
ninja
.
build
(
stamp
'
stamp
'
targets
order_only
=
order_only
)
      
self
.
ninja
.
newline
(
)
    
return
targets
[
0
]
  
def
_SubninjaNameForArch
(
self
arch
)
:
    
output_file_base
=
os
.
path
.
splitext
(
self
.
output_file_name
)
[
0
]
    
return
'
%
s
.
%
s
.
ninja
'
%
(
output_file_base
arch
)
  
def
WriteSpec
(
self
spec
config_name
generator_flags
)
:
    
"
"
"
The
main
entry
point
for
NinjaWriter
:
write
the
build
rules
for
a
spec
.
    
Returns
a
Target
object
which
represents
the
output
paths
for
this
spec
.
    
Returns
None
if
there
are
no
outputs
(
e
.
g
.
a
settings
-
only
'
none
'
type
    
target
)
.
"
"
"
    
self
.
config_name
=
config_name
    
self
.
name
=
spec
[
'
target_name
'
]
    
self
.
toolset
=
spec
[
'
toolset
'
]
    
config
=
spec
[
'
configurations
'
]
[
config_name
]
    
self
.
target
=
Target
(
spec
[
'
type
'
]
)
    
self
.
is_standalone_static_library
=
bool
(
        
spec
.
get
(
'
standalone_static_library
'
0
)
)
    
self
.
target_rpath
=
generator_flags
.
get
(
'
target_rpath
'
r
'
\
ORIGIN
/
lib
/
'
)
    
self
.
is_mac_bundle
=
gyp
.
xcode_emulation
.
IsMacBundle
(
self
.
flavor
spec
)
    
self
.
xcode_settings
=
self
.
msvs_settings
=
None
    
if
self
.
flavor
=
=
'
mac
'
:
      
self
.
xcode_settings
=
gyp
.
xcode_emulation
.
XcodeSettings
(
spec
)
      
mac_toolchain_dir
=
generator_flags
.
get
(
'
mac_toolchain_dir
'
None
)
      
if
mac_toolchain_dir
:
        
self
.
xcode_settings
.
mac_toolchain_dir
=
mac_toolchain_dir
    
if
self
.
flavor
=
=
'
win
'
:
      
self
.
msvs_settings
=
gyp
.
msvs_emulation
.
MsvsSettings
(
spec
                                                           
generator_flags
)
      
arch
=
self
.
msvs_settings
.
GetArch
(
config_name
)
      
self
.
ninja
.
variable
(
'
arch
'
self
.
win_env
[
arch
]
)
      
self
.
ninja
.
variable
(
'
cc
'
'
cl_
'
+
arch
)
      
self
.
ninja
.
variable
(
'
cxx
'
'
cl_
'
+
arch
)
      
self
.
ninja
.
variable
(
'
cc_host
'
'
cl_
'
+
arch
)
      
self
.
ninja
.
variable
(
'
cxx_host
'
'
cl_
'
+
arch
)
      
self
.
ninja
.
variable
(
'
asm
'
'
ml_
'
+
arch
)
    
if
self
.
flavor
=
=
'
mac
'
:
      
self
.
archs
=
self
.
xcode_settings
.
GetActiveArchs
(
config_name
)
      
if
len
(
self
.
archs
)
>
1
:
        
self
.
arch_subninjas
=
dict
(
            
(
arch
ninja_syntax
.
Writer
(
                
OpenOutput
(
os
.
path
.
join
(
self
.
toplevel_build
                                        
self
.
_SubninjaNameForArch
(
arch
)
)
                           
'
w
'
)
)
)
            
for
arch
in
self
.
archs
)
    
actions_depends
=
[
]
    
compile_depends
=
[
]
    
if
'
dependencies
'
in
spec
:
      
for
dep
in
spec
[
'
dependencies
'
]
:
        
if
dep
in
self
.
target_outputs
:
          
target
=
self
.
target_outputs
[
dep
]
          
actions_depends
.
append
(
target
.
PreActionInput
(
self
.
flavor
)
)
          
compile_depends
.
append
(
target
.
PreCompileInput
(
)
)
          
if
target
.
uses_cpp
:
            
self
.
target
.
uses_cpp
=
True
      
actions_depends
=
filter
(
None
actions_depends
)
      
compile_depends
=
filter
(
None
compile_depends
)
      
actions_depends
=
self
.
WriteCollapsedDependencies
(
'
actions_depends
'
                                                        
actions_depends
)
      
compile_depends
=
self
.
WriteCollapsedDependencies
(
'
compile_depends
'
                                                        
compile_depends
)
      
self
.
target
.
preaction_stamp
=
actions_depends
      
self
.
target
.
precompile_stamp
=
compile_depends
    
extra_sources
=
[
]
    
mac_bundle_depends
=
[
]
    
self
.
target
.
actions_stamp
=
self
.
WriteActionsRulesCopies
(
        
spec
extra_sources
actions_depends
mac_bundle_depends
)
    
compile_depends_stamp
=
(
self
.
target
.
actions_stamp
or
compile_depends
)
    
link_deps
=
[
]
    
try
:
      
sources
=
extra_sources
+
spec
.
get
(
'
sources
'
[
]
)
    
except
TypeError
:
      
print
'
extra_sources
:
'
str
(
extra_sources
)
      
print
'
spec
.
get
(
"
sources
"
)
:
'
str
(
spec
.
get
(
'
sources
'
)
)
      
raise
    
if
sources
:
      
if
self
.
flavor
=
=
'
mac
'
and
len
(
self
.
archs
)
>
1
:
        
for
arch
in
self
.
archs
:
          
self
.
ninja
.
subninja
(
self
.
_SubninjaNameForArch
(
arch
)
)
      
pch
=
None
      
if
self
.
flavor
=
=
'
win
'
:
        
gyp
.
msvs_emulation
.
VerifyMissingSources
(
            
sources
self
.
abs_build_dir
generator_flags
self
.
GypPathToNinja
)
        
pch
=
gyp
.
msvs_emulation
.
PrecompiledHeader
(
            
self
.
msvs_settings
config_name
self
.
GypPathToNinja
            
self
.
GypPathToUniqueOutput
self
.
obj_ext
)
      
else
:
        
pch
=
gyp
.
xcode_emulation
.
MacPrefixHeader
(
            
self
.
xcode_settings
self
.
GypPathToNinja
            
lambda
path
lang
:
self
.
GypPathToUniqueOutput
(
path
+
'
-
'
+
lang
)
)
      
link_deps
=
self
.
WriteSources
(
          
self
.
ninja
config_name
config
sources
compile_depends_stamp
pch
          
spec
)
      
obj_outputs
=
[
f
for
f
in
sources
if
f
.
endswith
(
self
.
obj_ext
)
]
      
if
obj_outputs
:
        
if
self
.
flavor
!
=
'
mac
'
or
len
(
self
.
archs
)
=
=
1
:
          
link_deps
+
=
[
self
.
GypPathToNinja
(
o
)
for
o
in
obj_outputs
]
        
else
:
          
print
"
Warning
:
Actions
/
rules
writing
object
files
don
'
t
work
with
"
\
                
"
multiarch
targets
dropping
.
(
target
%
s
)
"
%
spec
[
'
target_name
'
]
    
elif
self
.
flavor
=
=
'
mac
'
and
len
(
self
.
archs
)
>
1
:
      
link_deps
=
collections
.
defaultdict
(
list
)
    
compile_deps
=
self
.
target
.
actions_stamp
or
actions_depends
    
if
self
.
flavor
=
=
'
win
'
and
self
.
target
.
type
=
=
'
static_library
'
:
      
self
.
target
.
component_objs
=
link_deps
      
self
.
target
.
compile_deps
=
compile_deps
    
output
=
None
    
is_empty_bundle
=
not
link_deps
and
not
mac_bundle_depends
    
if
link_deps
or
self
.
target
.
actions_stamp
or
actions_depends
:
      
output
=
self
.
WriteTarget
(
spec
config_name
config
link_deps
                                
compile_deps
)
      
if
self
.
is_mac_bundle
:
        
mac_bundle_depends
.
append
(
output
)
    
if
self
.
is_mac_bundle
:
      
output
=
self
.
WriteMacBundle
(
spec
mac_bundle_depends
is_empty_bundle
)
    
if
not
output
:
      
return
None
    
assert
self
.
target
.
FinalOutput
(
)
output
    
return
self
.
target
  
def
_WinIdlRule
(
self
source
prebuild
outputs
)
:
    
"
"
"
Handle
the
implicit
VS
.
idl
rule
for
one
source
file
.
Fills
|
outputs
|
    
with
files
that
are
generated
.
"
"
"
    
outdir
output
vars
flags
=
self
.
msvs_settings
.
GetIdlBuildData
(
        
source
self
.
config_name
)
    
outdir
=
self
.
GypPathToNinja
(
outdir
)
    
def
fix_path
(
path
rel
=
None
)
:
      
path
=
os
.
path
.
join
(
outdir
path
)
      
dirname
basename
=
os
.
path
.
split
(
source
)
      
root
ext
=
os
.
path
.
splitext
(
basename
)
      
path
=
self
.
ExpandRuleVariables
(
          
path
root
dirname
source
ext
basename
)
      
if
rel
:
        
path
=
os
.
path
.
relpath
(
path
rel
)
      
return
path
    
vars
=
[
(
name
fix_path
(
value
outdir
)
)
for
name
value
in
vars
]
    
output
=
[
fix_path
(
p
)
for
p
in
output
]
    
vars
.
append
(
(
'
outdir
'
outdir
)
)
    
vars
.
append
(
(
'
idlflags
'
flags
)
)
    
input
=
self
.
GypPathToNinja
(
source
)
    
self
.
ninja
.
build
(
output
'
idl
'
input
        
variables
=
vars
order_only
=
prebuild
)
    
outputs
.
extend
(
output
)
  
def
WriteWinIdlFiles
(
self
spec
prebuild
)
:
    
"
"
"
Writes
rules
to
match
MSVS
'
s
implicit
idl
handling
.
"
"
"
    
assert
self
.
flavor
=
=
'
win
'
    
if
self
.
msvs_settings
.
HasExplicitIdlRulesOrActions
(
spec
)
:
      
return
[
]
    
outputs
=
[
]
    
for
source
in
filter
(
lambda
x
:
x
.
endswith
(
'
.
idl
'
)
spec
[
'
sources
'
]
)
:
      
self
.
_WinIdlRule
(
source
prebuild
outputs
)
    
return
outputs
  
def
WriteActionsRulesCopies
(
self
spec
extra_sources
prebuild
                              
mac_bundle_depends
)
:
    
"
"
"
Write
out
the
Actions
Rules
and
Copies
steps
.
Return
a
path
    
representing
the
outputs
of
these
steps
.
"
"
"
    
outputs
=
[
]
    
if
self
.
is_mac_bundle
:
      
mac_bundle_resources
=
spec
.
get
(
'
mac_bundle_resources
'
[
]
)
[
:
]
    
else
:
      
mac_bundle_resources
=
[
]
    
extra_mac_bundle_resources
=
[
]
    
if
'
actions
'
in
spec
:
      
outputs
+
=
self
.
WriteActions
(
spec
[
'
actions
'
]
extra_sources
prebuild
                                   
extra_mac_bundle_resources
)
    
if
'
rules
'
in
spec
:
      
outputs
+
=
self
.
WriteRules
(
spec
[
'
rules
'
]
extra_sources
prebuild
                                 
mac_bundle_resources
                                 
extra_mac_bundle_resources
)
    
if
'
copies
'
in
spec
:
      
outputs
+
=
self
.
WriteCopies
(
spec
[
'
copies
'
]
prebuild
mac_bundle_depends
)
    
if
'
sources
'
in
spec
and
self
.
flavor
=
=
'
win
'
:
      
outputs
+
=
self
.
WriteWinIdlFiles
(
spec
prebuild
)
    
if
self
.
xcode_settings
and
self
.
xcode_settings
.
IsIosFramework
(
)
:
      
self
.
WriteiOSFrameworkHeaders
(
spec
outputs
prebuild
)
    
stamp
=
self
.
WriteCollapsedDependencies
(
'
actions_rules_copies
'
outputs
)
    
if
self
.
is_mac_bundle
:
      
xcassets
=
self
.
WriteMacBundleResources
(
          
extra_mac_bundle_resources
+
mac_bundle_resources
mac_bundle_depends
)
      
partial_info_plist
=
self
.
WriteMacXCassets
(
xcassets
mac_bundle_depends
)
      
self
.
WriteMacInfoPlist
(
partial_info_plist
mac_bundle_depends
)
    
return
stamp
  
def
GenerateDescription
(
self
verb
message
fallback
)
:
    
"
"
"
Generate
and
return
a
description
of
a
build
step
.
    
|
verb
|
is
the
short
summary
e
.
g
.
ACTION
or
RULE
.
    
|
message
|
is
a
hand
-
written
description
or
None
if
not
available
.
    
|
fallback
|
is
the
gyp
-
level
name
of
the
step
usable
as
a
fallback
.
    
"
"
"
    
if
self
.
toolset
!
=
'
target
'
:
      
verb
+
=
'
(
%
s
)
'
%
self
.
toolset
    
if
message
:
      
return
'
%
s
%
s
'
%
(
verb
self
.
ExpandSpecial
(
message
)
)
    
else
:
      
return
'
%
s
%
s
:
%
s
'
%
(
verb
self
.
name
fallback
)
  
def
WriteActions
(
self
actions
extra_sources
prebuild
                   
extra_mac_bundle_resources
)
:
    
env
=
self
.
GetToolchainEnv
(
)
    
all_outputs
=
[
]
    
for
action
in
actions
:
      
name
=
'
%
s_
%
s
'
%
(
action
[
'
action_name
'
]
self
.
hash_for_rules
)
      
description
=
self
.
GenerateDescription
(
'
ACTION
'
                                             
action
.
get
(
'
message
'
None
)
                                             
name
)
      
is_cygwin
=
(
self
.
msvs_settings
.
IsRuleRunUnderCygwin
(
action
)
                   
if
self
.
flavor
=
=
'
win
'
else
False
)
      
args
=
action
[
'
action
'
]
      
depfile
=
action
.
get
(
'
depfile
'
None
)
      
if
depfile
:
        
depfile
=
self
.
ExpandSpecial
(
depfile
self
.
base_to_build
)
      
pool
=
'
console
'
if
int
(
action
.
get
(
'
ninja_use_console
'
0
)
)
else
None
      
rule_name
_
=
self
.
WriteNewNinjaRule
(
name
args
description
                                            
is_cygwin
env
pool
                                            
depfile
=
depfile
)
      
inputs
=
[
self
.
GypPathToNinja
(
i
env
)
for
i
in
action
[
'
inputs
'
]
]
      
if
int
(
action
.
get
(
'
process_outputs_as_sources
'
False
)
)
:
        
extra_sources
+
=
action
[
'
outputs
'
]
      
if
int
(
action
.
get
(
'
process_outputs_as_mac_bundle_resources
'
False
)
)
:
        
extra_mac_bundle_resources
+
=
action
[
'
outputs
'
]
      
outputs
=
[
self
.
GypPathToNinja
(
o
env
)
for
o
in
action
[
'
outputs
'
]
]
      
self
.
ninja
.
build
(
outputs
rule_name
inputs
                       
order_only
=
prebuild
)
      
all_outputs
+
=
outputs
      
self
.
ninja
.
newline
(
)
    
return
all_outputs
  
def
WriteRules
(
self
rules
extra_sources
prebuild
                 
mac_bundle_resources
extra_mac_bundle_resources
)
:
    
env
=
self
.
GetToolchainEnv
(
)
    
all_outputs
=
[
]
    
for
rule
in
rules
:
      
if
'
action
'
not
in
rule
and
not
rule
.
get
(
'
rule_sources
'
[
]
)
:
        
continue
      
name
=
'
%
s_
%
s
'
%
(
rule
[
'
rule_name
'
]
self
.
hash_for_rules
)
      
args
=
rule
[
'
action
'
]
      
description
=
self
.
GenerateDescription
(
          
'
RULE
'
          
rule
.
get
(
'
message
'
None
)
          
(
'
%
s
'
+
generator_default_variables
[
'
RULE_INPUT_PATH
'
]
)
%
name
)
      
is_cygwin
=
(
self
.
msvs_settings
.
IsRuleRunUnderCygwin
(
rule
)
                   
if
self
.
flavor
=
=
'
win
'
else
False
)
      
pool
=
'
console
'
if
int
(
rule
.
get
(
'
ninja_use_console
'
0
)
)
else
None
      
rule_name
args
=
self
.
WriteNewNinjaRule
(
          
name
args
description
is_cygwin
env
pool
)
      
special_locals
=
(
'
source
'
'
root
'
'
dirname
'
'
ext
'
'
name
'
)
      
needed_variables
=
set
(
[
'
source
'
]
)
      
for
argument
in
args
:
        
for
var
in
special_locals
:
          
if
'
{
%
s
}
'
%
var
in
argument
:
            
needed_variables
.
add
(
var
)
      
needed_variables
=
sorted
(
needed_variables
)
      
def
cygwin_munge
(
path
)
:
        
if
is_cygwin
:
          
return
path
.
replace
(
'
\
\
'
'
/
'
)
        
return
path
      
inputs
=
[
self
.
GypPathToNinja
(
i
env
)
for
i
in
rule
.
get
(
'
inputs
'
[
]
)
]
      
sources
=
rule
.
get
(
'
rule_sources
'
[
]
)
      
num_inputs
=
len
(
inputs
)
      
if
prebuild
:
        
num_inputs
+
=
1
      
if
num_inputs
>
2
and
len
(
sources
)
>
2
:
        
inputs
=
[
self
.
WriteCollapsedDependencies
(
          
rule
[
'
rule_name
'
]
inputs
order_only
=
prebuild
)
]
        
prebuild
=
[
]
      
for
source
in
sources
:
        
source
=
os
.
path
.
normpath
(
source
)
        
dirname
basename
=
os
.
path
.
split
(
source
)
        
root
ext
=
os
.
path
.
splitext
(
basename
)
        
outputs
=
[
self
.
ExpandRuleVariables
(
o
root
dirname
                                            
source
ext
basename
)
                   
for
o
in
rule
[
'
outputs
'
]
]
        
if
int
(
rule
.
get
(
'
process_outputs_as_sources
'
False
)
)
:
          
extra_sources
+
=
outputs
        
was_mac_bundle_resource
=
source
in
mac_bundle_resources
        
if
was_mac_bundle_resource
or
\
            
int
(
rule
.
get
(
'
process_outputs_as_mac_bundle_resources
'
False
)
)
:
          
extra_mac_bundle_resources
+
=
outputs
          
if
was_mac_bundle_resource
:
            
mac_bundle_resources
.
remove
(
source
)
        
extra_bindings
=
[
]
        
for
var
in
needed_variables
:
          
if
var
=
=
'
root
'
:
            
extra_bindings
.
append
(
(
'
root
'
cygwin_munge
(
root
)
)
)
          
elif
var
=
=
'
dirname
'
:
            
dirname_expanded
=
self
.
ExpandSpecial
(
dirname
self
.
base_to_build
)
            
extra_bindings
.
append
(
(
'
dirname
'
cygwin_munge
(
dirname_expanded
)
)
)
          
elif
var
=
=
'
source
'
:
            
source_expanded
=
self
.
ExpandSpecial
(
source
self
.
base_to_build
)
            
extra_bindings
.
append
(
(
'
source
'
cygwin_munge
(
source_expanded
)
)
)
          
elif
var
=
=
'
ext
'
:
            
extra_bindings
.
append
(
(
'
ext
'
ext
)
)
          
elif
var
=
=
'
name
'
:
            
extra_bindings
.
append
(
(
'
name
'
cygwin_munge
(
basename
)
)
)
          
else
:
            
assert
var
=
=
None
repr
(
var
)
        
outputs
=
[
self
.
GypPathToNinja
(
o
env
)
for
o
in
outputs
]
        
if
self
.
flavor
=
=
'
win
'
:
          
extra_bindings
.
append
(
(
'
unique_name
'
              
hashlib
.
md5
(
outputs
[
0
]
)
.
hexdigest
(
)
)
)
        
self
.
ninja
.
build
(
outputs
rule_name
self
.
GypPathToNinja
(
source
)
                         
implicit
=
inputs
                         
order_only
=
prebuild
                         
variables
=
extra_bindings
)
        
all_outputs
.
extend
(
outputs
)
    
return
all_outputs
  
def
WriteCopies
(
self
copies
prebuild
mac_bundle_depends
)
:
    
outputs
=
[
]
    
if
self
.
xcode_settings
:
      
extra_env
=
self
.
xcode_settings
.
GetPerTargetSettings
(
)
      
env
=
self
.
GetToolchainEnv
(
additional_settings
=
extra_env
)
    
else
:
      
env
=
self
.
GetToolchainEnv
(
)
    
for
copy
in
copies
:
      
for
path
in
copy
[
'
files
'
]
:
        
path
=
os
.
path
.
normpath
(
path
)
        
basename
=
os
.
path
.
split
(
path
)
[
1
]
        
src
=
self
.
GypPathToNinja
(
path
env
)
        
dst
=
self
.
GypPathToNinja
(
os
.
path
.
join
(
copy
[
'
destination
'
]
basename
)
                                  
env
)
        
outputs
+
=
self
.
ninja
.
build
(
dst
'
copy
'
src
order_only
=
prebuild
)
        
if
self
.
is_mac_bundle
:
          
if
dst
.
startswith
(
self
.
xcode_settings
.
GetBundleContentsFolderPath
(
)
)
:
            
mac_bundle_depends
.
append
(
dst
)
    
return
outputs
  
def
WriteiOSFrameworkHeaders
(
self
spec
outputs
prebuild
)
:
    
"
"
"
Prebuild
steps
to
generate
hmap
files
and
copy
headers
to
destination
.
"
"
"
    
framework
=
self
.
ComputeMacBundleOutput
(
)
    
all_sources
=
spec
[
'
sources
'
]
    
copy_headers
=
spec
[
'
mac_framework_headers
'
]
    
output
=
self
.
GypPathToUniqueOutput
(
'
headers
.
hmap
'
)
    
self
.
xcode_settings
.
header_map_path
=
output
    
all_headers
=
map
(
self
.
GypPathToNinja
                      
filter
(
lambda
x
:
x
.
endswith
(
(
'
.
h
'
)
)
all_sources
)
)
    
variables
=
[
(
'
framework
'
framework
)
                 
(
'
copy_headers
'
map
(
self
.
GypPathToNinja
copy_headers
)
)
]
    
outputs
.
extend
(
self
.
ninja
.
build
(
        
output
'
compile_ios_framework_headers
'
all_headers
        
variables
=
variables
order_only
=
prebuild
)
)
  
def
WriteMacBundleResources
(
self
resources
bundle_depends
)
:
    
"
"
"
Writes
ninja
edges
for
'
mac_bundle_resources
'
.
"
"
"
    
xcassets
=
[
]
    
extra_env
=
self
.
xcode_settings
.
GetPerTargetSettings
(
)
    
env
=
self
.
GetSortedXcodeEnv
(
additional_settings
=
extra_env
)
    
env
=
self
.
ComputeExportEnvString
(
env
)
    
isBinary
=
self
.
xcode_settings
.
IsBinaryOutputFormat
(
self
.
config_name
)
    
for
output
res
in
gyp
.
xcode_emulation
.
GetMacBundleResources
(
        
generator_default_variables
[
'
PRODUCT_DIR
'
]
        
self
.
xcode_settings
map
(
self
.
GypPathToNinja
resources
)
)
:
      
output
=
self
.
ExpandSpecial
(
output
)
      
if
os
.
path
.
splitext
(
output
)
[
-
1
]
!
=
'
.
xcassets
'
:
        
self
.
ninja
.
build
(
output
'
mac_tool
'
res
                         
variables
=
[
(
'
mactool_cmd
'
'
copy
-
bundle
-
resource
'
)
\
                                    
(
'
env
'
env
)
(
'
binary
'
isBinary
)
]
)
        
bundle_depends
.
append
(
output
)
      
else
:
        
xcassets
.
append
(
res
)
    
return
xcassets
  
def
WriteMacXCassets
(
self
xcassets
bundle_depends
)
:
    
"
"
"
Writes
ninja
edges
for
'
mac_bundle_resources
'
.
xcassets
files
.
    
This
add
an
invocation
of
'
actool
'
via
the
'
mac_tool
.
py
'
helper
script
.
    
It
assumes
that
the
assets
catalogs
define
at
least
one
imageset
and
    
thus
an
Assets
.
car
file
will
be
generated
in
the
application
resources
    
directory
.
If
this
is
not
the
case
then
the
build
will
probably
be
done
    
at
each
invocation
of
ninja
.
"
"
"
    
if
not
xcassets
:
      
return
    
extra_arguments
=
{
}
    
settings_to_arg
=
{
        
'
XCASSETS_APP_ICON
'
:
'
app
-
icon
'
        
'
XCASSETS_LAUNCH_IMAGE
'
:
'
launch
-
image
'
    
}
    
settings
=
self
.
xcode_settings
.
xcode_settings
[
self
.
config_name
]
    
for
settings_key
arg_name
in
settings_to_arg
.
iteritems
(
)
:
      
value
=
settings
.
get
(
settings_key
)
      
if
value
:
        
extra_arguments
[
arg_name
]
=
value
    
partial_info_plist
=
None
    
if
extra_arguments
:
      
partial_info_plist
=
self
.
GypPathToUniqueOutput
(
          
'
assetcatalog_generated_info
.
plist
'
)
      
extra_arguments
[
'
output
-
partial
-
info
-
plist
'
]
=
partial_info_plist
    
outputs
=
[
]
    
outputs
.
append
(
        
os
.
path
.
join
(
            
self
.
xcode_settings
.
GetBundleResourceFolder
(
)
            
'
Assets
.
car
'
)
)
    
if
partial_info_plist
:
      
outputs
.
append
(
partial_info_plist
)
    
keys
=
QuoteShellArgument
(
json
.
dumps
(
extra_arguments
)
self
.
flavor
)
    
extra_env
=
self
.
xcode_settings
.
GetPerTargetSettings
(
)
    
env
=
self
.
GetSortedXcodeEnv
(
additional_settings
=
extra_env
)
    
env
=
self
.
ComputeExportEnvString
(
env
)
    
bundle_depends
.
extend
(
self
.
ninja
.
build
(
        
outputs
'
compile_xcassets
'
xcassets
        
variables
=
[
(
'
env
'
env
)
(
'
keys
'
keys
)
]
)
)
    
return
partial_info_plist
  
def
WriteMacInfoPlist
(
self
partial_info_plist
bundle_depends
)
:
    
"
"
"
Write
build
rules
for
bundle
Info
.
plist
files
.
"
"
"
    
info_plist
out
defines
extra_env
=
gyp
.
xcode_emulation
.
GetMacInfoPlist
(
        
generator_default_variables
[
'
PRODUCT_DIR
'
]
        
self
.
xcode_settings
self
.
GypPathToNinja
)
    
if
not
info_plist
:
      
return
    
out
=
self
.
ExpandSpecial
(
out
)
    
if
defines
:
      
intermediate_plist
=
self
.
GypPathToUniqueOutput
(
          
os
.
path
.
basename
(
info_plist
)
)
      
defines
=
'
'
.
join
(
[
Define
(
d
self
.
flavor
)
for
d
in
defines
]
)
      
info_plist
=
self
.
ninja
.
build
(
          
intermediate_plist
'
preprocess_infoplist
'
info_plist
          
variables
=
[
(
'
defines
'
defines
)
]
)
    
env
=
self
.
GetSortedXcodeEnv
(
additional_settings
=
extra_env
)
    
env
=
self
.
ComputeExportEnvString
(
env
)
    
if
partial_info_plist
:
      
intermediate_plist
=
self
.
GypPathToUniqueOutput
(
'
merged_info
.
plist
'
)
      
info_plist
=
self
.
ninja
.
build
(
          
intermediate_plist
'
merge_infoplist
'
          
[
partial_info_plist
info_plist
]
)
    
keys
=
self
.
xcode_settings
.
GetExtraPlistItems
(
self
.
config_name
)
    
keys
=
QuoteShellArgument
(
json
.
dumps
(
keys
)
self
.
flavor
)
    
isBinary
=
self
.
xcode_settings
.
IsBinaryOutputFormat
(
self
.
config_name
)
    
self
.
ninja
.
build
(
out
'
copy_infoplist
'
info_plist
                     
variables
=
[
(
'
env
'
env
)
(
'
keys
'
keys
)
                                
(
'
binary
'
isBinary
)
]
)
    
bundle_depends
.
append
(
out
)
  
def
WriteSources
(
self
ninja_file
config_name
config
sources
predepends
                   
precompiled_header
spec
)
:
    
"
"
"
Write
build
rules
to
compile
all
of
|
sources
|
.
"
"
"
    
if
self
.
toolset
=
=
'
host
'
:
      
self
.
ninja
.
variable
(
'
ar
'
'
ar_host
'
)
      
self
.
ninja
.
variable
(
'
cc
'
'
cc_host
'
)
      
self
.
ninja
.
variable
(
'
cxx
'
'
cxx_host
'
)
      
self
.
ninja
.
variable
(
'
ld
'
'
ld_host
'
)
      
self
.
ninja
.
variable
(
'
ldxx
'
'
ldxx_host
'
)
      
self
.
ninja
.
variable
(
'
nm
'
'
nm_host
'
)
      
self
.
ninja
.
variable
(
'
readelf
'
'
readelf_host
'
)
    
if
self
.
flavor
!
=
'
mac
'
or
len
(
self
.
archs
)
=
=
1
:
      
return
self
.
WriteSourcesForArch
(
          
self
.
ninja
config_name
config
sources
predepends
          
precompiled_header
spec
)
    
else
:
      
return
dict
(
(
arch
self
.
WriteSourcesForArch
(
            
self
.
arch_subninjas
[
arch
]
config_name
config
sources
predepends
            
precompiled_header
spec
arch
=
arch
)
)
          
for
arch
in
self
.
archs
)
  
def
WriteSourcesForArch
(
self
ninja_file
config_name
config
sources
                          
predepends
precompiled_header
spec
arch
=
None
)
:
    
"
"
"
Write
build
rules
to
compile
all
of
|
sources
|
.
"
"
"
    
extra_defines
=
[
]
    
if
self
.
flavor
=
=
'
mac
'
:
      
cflags
=
self
.
xcode_settings
.
GetCflags
(
config_name
arch
=
arch
)
      
cflags_c
=
self
.
xcode_settings
.
GetCflagsC
(
config_name
)
      
cflags_cc
=
self
.
xcode_settings
.
GetCflagsCC
(
config_name
)
      
cflags_objc
=
[
'
cflags_c
'
]
+
\
                    
self
.
xcode_settings
.
GetCflagsObjC
(
config_name
)
      
cflags_objcc
=
[
'
cflags_cc
'
]
+
\
                     
self
.
xcode_settings
.
GetCflagsObjCC
(
config_name
)
    
elif
self
.
flavor
=
=
'
win
'
:
      
asmflags
=
self
.
msvs_settings
.
GetAsmflags
(
config_name
)
      
cflags
=
self
.
msvs_settings
.
GetCflags
(
config_name
)
      
cflags_c
=
self
.
msvs_settings
.
GetCflagsC
(
config_name
)
      
cflags_cc
=
self
.
msvs_settings
.
GetCflagsCC
(
config_name
)
      
extra_defines
=
self
.
msvs_settings
.
GetComputedDefines
(
config_name
)
      
pdbpath_c
=
pdbpath_cc
=
self
.
msvs_settings
.
GetCompilerPdbName
(
          
config_name
self
.
ExpandSpecial
)
      
if
not
pdbpath_c
:
        
obj
=
'
obj
'
        
if
self
.
toolset
!
=
'
target
'
:
          
obj
+
=
'
.
'
+
self
.
toolset
        
pdbpath
=
os
.
path
.
normpath
(
os
.
path
.
join
(
obj
self
.
base_dir
self
.
name
)
)
        
pdbpath_c
=
pdbpath
+
'
.
c
.
pdb
'
        
pdbpath_cc
=
pdbpath
+
'
.
cc
.
pdb
'
      
self
.
WriteVariableList
(
ninja_file
'
pdbname_c
'
[
pdbpath_c
]
)
      
self
.
WriteVariableList
(
ninja_file
'
pdbname_cc
'
[
pdbpath_cc
]
)
      
self
.
WriteVariableList
(
ninja_file
'
pchprefix
'
[
self
.
name
]
)
    
else
:
      
cflags
=
config
.
get
(
'
cflags
'
[
]
)
      
cflags_c
=
config
.
get
(
'
cflags_c
'
[
]
)
      
cflags_cc
=
config
.
get
(
'
cflags_cc
'
[
]
)
    
if
self
.
toolset
=
=
'
target
'
:
      
cflags_c
=
(
os
.
environ
.
get
(
'
CPPFLAGS
'
'
'
)
.
split
(
)
+
                  
os
.
environ
.
get
(
'
CFLAGS
'
'
'
)
.
split
(
)
+
cflags_c
)
      
cflags_cc
=
(
os
.
environ
.
get
(
'
CPPFLAGS
'
'
'
)
.
split
(
)
+
                   
os
.
environ
.
get
(
'
CXXFLAGS
'
'
'
)
.
split
(
)
+
cflags_cc
)
    
elif
self
.
toolset
=
=
'
host
'
:
      
cflags_c
=
(
os
.
environ
.
get
(
'
CPPFLAGS_host
'
'
'
)
.
split
(
)
+
                  
os
.
environ
.
get
(
'
CFLAGS_host
'
'
'
)
.
split
(
)
+
cflags_c
)
      
cflags_cc
=
(
os
.
environ
.
get
(
'
CPPFLAGS_host
'
'
'
)
.
split
(
)
+
                   
os
.
environ
.
get
(
'
CXXFLAGS_host
'
'
'
)
.
split
(
)
+
cflags_cc
)
    
defines
=
config
.
get
(
'
defines
'
[
]
)
+
extra_defines
    
self
.
WriteVariableList
(
ninja_file
'
defines
'
                           
[
Define
(
d
self
.
flavor
)
for
d
in
defines
]
)
    
if
self
.
flavor
=
=
'
win
'
:
      
self
.
WriteVariableList
(
ninja_file
'
asmflags
'
                             
map
(
self
.
ExpandSpecial
asmflags
)
)
      
self
.
WriteVariableList
(
ninja_file
'
rcflags
'
          
[
QuoteShellArgument
(
self
.
ExpandSpecial
(
f
)
self
.
flavor
)
           
for
f
in
self
.
msvs_settings
.
GetRcflags
(
config_name
                                                  
self
.
GypPathToNinja
)
]
)
    
include_dirs
=
config
.
get
(
'
include_dirs
'
[
]
)
    
env
=
self
.
GetToolchainEnv
(
)
    
if
self
.
flavor
=
=
'
win
'
:
      
include_dirs
=
self
.
msvs_settings
.
AdjustIncludeDirs
(
include_dirs
                                                          
config_name
)
    
self
.
WriteVariableList
(
ninja_file
'
includes
'
        
[
QuoteShellArgument
(
'
-
I
'
+
self
.
GypPathToNinja
(
i
env
)
self
.
flavor
)
         
for
i
in
include_dirs
]
)
    
if
self
.
flavor
=
=
'
win
'
:
      
midl_include_dirs
=
config
.
get
(
'
midl_include_dirs
'
[
]
)
      
midl_include_dirs
=
self
.
msvs_settings
.
AdjustMidlIncludeDirs
(
          
midl_include_dirs
config_name
)
      
self
.
WriteVariableList
(
ninja_file
'
midl_includes
'
          
[
QuoteShellArgument
(
'
-
I
'
+
self
.
GypPathToNinja
(
i
env
)
self
.
flavor
)
           
for
i
in
midl_include_dirs
]
)
    
pch_commands
=
precompiled_header
.
GetPchBuildCommands
(
arch
)
    
if
self
.
flavor
=
=
'
mac
'
:
      
for
ext
var
in
[
(
'
c
'
'
cflags_pch_c
'
)
(
'
cc
'
'
cflags_pch_cc
'
)
                       
(
'
m
'
'
cflags_pch_objc
'
)
(
'
mm
'
'
cflags_pch_objcc
'
)
]
:
        
include
=
precompiled_header
.
GetInclude
(
ext
arch
)
        
if
include
:
ninja_file
.
variable
(
var
include
)
    
arflags
=
config
.
get
(
'
arflags
'
[
]
)
    
self
.
WriteVariableList
(
ninja_file
'
cflags
'
                           
map
(
self
.
ExpandSpecial
cflags
)
)
    
self
.
WriteVariableList
(
ninja_file
'
cflags_c
'
                           
map
(
self
.
ExpandSpecial
cflags_c
)
)
    
self
.
WriteVariableList
(
ninja_file
'
cflags_cc
'
                           
map
(
self
.
ExpandSpecial
cflags_cc
)
)
    
if
self
.
flavor
=
=
'
mac
'
:
      
self
.
WriteVariableList
(
ninja_file
'
cflags_objc
'
                             
map
(
self
.
ExpandSpecial
cflags_objc
)
)
      
self
.
WriteVariableList
(
ninja_file
'
cflags_objcc
'
                             
map
(
self
.
ExpandSpecial
cflags_objcc
)
)
    
self
.
WriteVariableList
(
ninja_file
'
arflags
'
                           
map
(
self
.
ExpandSpecial
arflags
)
)
    
ninja_file
.
newline
(
)
    
outputs
=
[
]
    
has_rc_source
=
False
    
for
source
in
sources
:
      
filename
ext
=
os
.
path
.
splitext
(
source
)
      
ext
=
ext
[
1
:
]
      
obj_ext
=
self
.
obj_ext
      
if
ext
in
(
'
cc
'
'
cpp
'
'
cxx
'
)
:
        
command
=
'
cxx
'
        
self
.
target
.
uses_cpp
=
True
      
elif
ext
=
=
'
c
'
or
(
ext
=
=
'
S
'
and
self
.
flavor
!
=
'
win
'
)
:
        
command
=
'
cc
'
      
elif
ext
=
=
'
s
'
and
self
.
flavor
!
=
'
win
'
:
        
command
=
'
cc_s
'
      
elif
(
self
.
flavor
=
=
'
win
'
and
ext
=
=
'
asm
'
and
            
not
self
.
msvs_settings
.
HasExplicitAsmRules
(
spec
)
)
:
        
command
=
'
asm
'
        
obj_ext
=
'
_asm
.
obj
'
      
elif
self
.
flavor
=
=
'
mac
'
and
ext
=
=
'
m
'
:
        
command
=
'
objc
'
      
elif
self
.
flavor
=
=
'
mac
'
and
ext
=
=
'
mm
'
:
        
command
=
'
objcxx
'
        
self
.
target
.
uses_cpp
=
True
      
elif
self
.
flavor
=
=
'
win
'
and
ext
=
=
'
rc
'
:
        
command
=
'
rc
'
        
obj_ext
=
'
.
res
'
        
has_rc_source
=
True
      
else
:
        
continue
      
input
=
self
.
GypPathToNinja
(
source
)
      
output
=
self
.
GypPathToUniqueOutput
(
filename
+
obj_ext
)
      
if
arch
is
not
None
:
        
output
=
AddArch
(
output
arch
)
      
implicit
=
precompiled_header
.
GetObjDependencies
(
[
input
]
[
output
]
arch
)
      
variables
=
[
]
      
if
self
.
flavor
=
=
'
win
'
:
        
variables
output
implicit
=
precompiled_header
.
GetFlagsModifications
(
            
input
output
implicit
command
cflags_c
cflags_cc
            
self
.
ExpandSpecial
)
      
ninja_file
.
build
(
output
command
input
                       
implicit
=
[
gch
for
_
_
gch
in
implicit
]
                       
order_only
=
predepends
variables
=
variables
)
      
outputs
.
append
(
output
)
    
if
has_rc_source
:
      
resource_include_dirs
=
config
.
get
(
'
resource_include_dirs
'
include_dirs
)
      
self
.
WriteVariableList
(
ninja_file
'
resource_includes
'
          
[
QuoteShellArgument
(
'
-
I
'
+
self
.
GypPathToNinja
(
i
env
)
self
.
flavor
)
           
for
i
in
resource_include_dirs
]
)
    
self
.
WritePchTargets
(
ninja_file
pch_commands
)
    
ninja_file
.
newline
(
)
    
return
outputs
  
def
WritePchTargets
(
self
ninja_file
pch_commands
)
:
    
"
"
"
Writes
ninja
rules
to
compile
prefix
headers
.
"
"
"
    
if
not
pch_commands
:
      
return
    
for
gch
lang_flag
lang
input
in
pch_commands
:
      
var_name
=
{
        
'
c
'
:
'
cflags_pch_c
'
        
'
cc
'
:
'
cflags_pch_cc
'
        
'
m
'
:
'
cflags_pch_objc
'
        
'
mm
'
:
'
cflags_pch_objcc
'
      
}
[
lang
]
      
map
=
{
'
c
'
:
'
cc
'
'
cc
'
:
'
cxx
'
'
m
'
:
'
objc
'
'
mm
'
:
'
objcxx
'
}
      
cmd
=
map
.
get
(
lang
)
      
ninja_file
.
build
(
gch
cmd
input
variables
=
[
(
var_name
lang_flag
)
]
)
  
def
WriteLink
(
self
spec
config_name
config
link_deps
compile_deps
)
:
    
"
"
"
Write
out
a
link
step
.
Fills
out
target
.
binary
.
"
"
"
    
if
self
.
flavor
!
=
'
mac
'
or
len
(
self
.
archs
)
=
=
1
:
      
return
self
.
WriteLinkForArch
(
          
self
.
ninja
spec
config_name
config
link_deps
compile_deps
)
    
else
:
      
output
=
self
.
ComputeOutput
(
spec
)
      
inputs
=
[
self
.
WriteLinkForArch
(
self
.
arch_subninjas
[
arch
]
spec
                                      
config_name
config
link_deps
[
arch
]
                                      
compile_deps
arch
=
arch
)
                
for
arch
in
self
.
archs
]
      
extra_bindings
=
[
]
      
build_output
=
output
      
if
not
self
.
is_mac_bundle
:
        
self
.
AppendPostbuildVariable
(
extra_bindings
spec
output
output
)
      
if
(
spec
[
'
type
'
]
in
(
'
shared_library
'
'
loadable_module
'
)
and
          
not
self
.
is_mac_bundle
)
:
        
extra_bindings
.
append
(
(
'
lib
'
output
)
)
        
self
.
ninja
.
build
(
[
output
output
+
'
.
TOC
'
]
'
solipo
'
inputs
            
variables
=
extra_bindings
)
      
else
:
        
self
.
ninja
.
build
(
build_output
'
lipo
'
inputs
variables
=
extra_bindings
)
      
return
output
  
def
WriteLinkForArch
(
self
ninja_file
spec
config_name
config
                       
link_deps
compile_deps
arch
=
None
)
:
    
"
"
"
Write
out
a
link
step
.
Fills
out
target
.
binary
.
"
"
"
    
command
=
{
      
'
executable
'
:
'
link
'
      
'
loadable_module
'
:
'
solink_module
'
      
'
shared_library
'
:
'
solink
'
    
}
[
spec
[
'
type
'
]
]
    
command_suffix
=
'
'
    
implicit_deps
=
set
(
)
    
solibs
=
set
(
)
    
order_deps
=
set
(
)
    
if
compile_deps
:
      
order_deps
.
add
(
compile_deps
)
    
if
'
dependencies
'
in
spec
:
      
extra_link_deps
=
set
(
)
      
for
dep
in
spec
[
'
dependencies
'
]
:
        
target
=
self
.
target_outputs
.
get
(
dep
)
        
if
not
target
:
          
continue
        
linkable
=
target
.
Linkable
(
)
        
if
linkable
:
          
new_deps
=
[
]
          
if
(
self
.
flavor
=
=
'
win
'
and
              
target
.
component_objs
and
              
self
.
msvs_settings
.
IsUseLibraryDependencyInputs
(
config_name
)
)
:
            
new_deps
=
target
.
component_objs
            
if
target
.
compile_deps
:
              
order_deps
.
add
(
target
.
compile_deps
)
          
elif
self
.
flavor
=
=
'
win
'
and
target
.
import_lib
:
            
new_deps
=
[
target
.
import_lib
]
          
elif
target
.
UsesToc
(
self
.
flavor
)
:
            
solibs
.
add
(
target
.
binary
)
            
implicit_deps
.
add
(
target
.
binary
+
'
.
TOC
'
)
          
else
:
            
new_deps
=
[
target
.
binary
]
          
for
new_dep
in
new_deps
:
            
if
new_dep
not
in
extra_link_deps
:
              
extra_link_deps
.
add
(
new_dep
)
              
link_deps
.
append
(
new_dep
)
        
final_output
=
target
.
FinalOutput
(
)
        
if
not
linkable
or
final_output
!
=
target
.
binary
:
          
implicit_deps
.
add
(
final_output
)
    
extra_bindings
=
[
]
    
if
self
.
target
.
uses_cpp
and
self
.
flavor
!
=
'
win
'
:
      
extra_bindings
.
append
(
(
'
ld
'
'
ldxx
'
)
)
    
output
=
self
.
ComputeOutput
(
spec
arch
)
    
if
arch
is
None
and
not
self
.
is_mac_bundle
:
      
self
.
AppendPostbuildVariable
(
extra_bindings
spec
output
output
)
    
is_executable
=
spec
[
'
type
'
]
=
=
'
executable
'
    
if
self
.
toolset
=
=
'
target
'
:
      
env_ldflags
=
os
.
environ
.
get
(
'
LDFLAGS
'
'
'
)
.
split
(
)
    
elif
self
.
toolset
=
=
'
host
'
:
      
env_ldflags
=
os
.
environ
.
get
(
'
LDFLAGS_host
'
'
'
)
.
split
(
)
    
if
self
.
flavor
=
=
'
mac
'
:
      
ldflags
=
self
.
xcode_settings
.
GetLdflags
(
config_name
          
self
.
ExpandSpecial
(
generator_default_variables
[
'
PRODUCT_DIR
'
]
)
          
self
.
GypPathToNinja
arch
)
      
ldflags
=
env_ldflags
+
ldflags
    
elif
self
.
flavor
=
=
'
win
'
:
      
manifest_base_name
=
self
.
GypPathToUniqueOutput
(
          
self
.
ComputeOutputFileName
(
spec
)
)
      
ldflags
intermediate_manifest
manifest_files
=
\
          
self
.
msvs_settings
.
GetLdflags
(
config_name
self
.
GypPathToNinja
                                        
self
.
ExpandSpecial
manifest_base_name
                                        
output
is_executable
                                        
self
.
toplevel_build
)
      
ldflags
=
env_ldflags
+
ldflags
      
self
.
WriteVariableList
(
ninja_file
'
manifests
'
manifest_files
)
      
implicit_deps
=
implicit_deps
.
union
(
manifest_files
)
      
if
intermediate_manifest
:
        
self
.
WriteVariableList
(
            
ninja_file
'
intermediatemanifest
'
[
intermediate_manifest
]
)
      
command_suffix
=
_GetWinLinkRuleNameSuffix
(
          
self
.
msvs_settings
.
IsEmbedManifest
(
config_name
)
)
      
def_file
=
self
.
msvs_settings
.
GetDefFile
(
self
.
GypPathToNinja
)
      
if
def_file
:
        
implicit_deps
.
add
(
def_file
)
    
else
:
      
ldflags
=
env_ldflags
+
config
.
get
(
'
ldflags
'
[
]
)
      
if
is_executable
and
len
(
solibs
)
:
        
rpath
=
'
lib
/
'
        
if
self
.
toolset
!
=
'
target
'
:
          
rpath
+
=
self
.
toolset
          
ldflags
.
append
(
r
'
-
Wl
-
rpath
=
\
ORIGIN
/
%
s
'
%
rpath
)
        
else
:
          
ldflags
.
append
(
'
-
Wl
-
rpath
=
%
s
'
%
self
.
target_rpath
)
        
ldflags
.
append
(
'
-
Wl
-
rpath
-
link
=
%
s
'
%
rpath
)
    
self
.
WriteVariableList
(
ninja_file
'
ldflags
'
                           
map
(
self
.
ExpandSpecial
ldflags
)
)
    
library_dirs
=
config
.
get
(
'
library_dirs
'
[
]
)
    
if
self
.
flavor
=
=
'
win
'
:
      
library_dirs
=
[
self
.
msvs_settings
.
ConvertVSMacros
(
l
config_name
)
                      
for
l
in
library_dirs
]
      
library_dirs
=
[
'
/
LIBPATH
:
'
+
QuoteShellArgument
(
self
.
GypPathToNinja
(
l
)
                                                       
self
.
flavor
)
                      
for
l
in
library_dirs
]
    
else
:
      
library_dirs
=
[
QuoteShellArgument
(
'
-
L
'
+
self
.
GypPathToNinja
(
l
)
                                         
self
.
flavor
)
                      
for
l
in
library_dirs
]
    
libraries
=
gyp
.
common
.
uniquer
(
map
(
self
.
ExpandSpecial
                                       
spec
.
get
(
'
libraries
'
[
]
)
)
)
    
if
self
.
flavor
=
=
'
mac
'
:
      
libraries
=
self
.
xcode_settings
.
AdjustLibraries
(
libraries
config_name
)
    
elif
self
.
flavor
=
=
'
win
'
:
      
libraries
=
self
.
msvs_settings
.
AdjustLibraries
(
libraries
)
    
self
.
WriteVariableList
(
ninja_file
'
libs
'
library_dirs
+
libraries
)
    
linked_binary
=
output
    
if
command
in
(
'
solink
'
'
solink_module
'
)
:
      
extra_bindings
.
append
(
(
'
soname
'
os
.
path
.
split
(
output
)
[
1
]
)
)
      
extra_bindings
.
append
(
(
'
lib
'
                            
gyp
.
common
.
EncodePOSIXShellArgument
(
output
)
)
)
      
if
self
.
flavor
!
=
'
win
'
:
        
link_file_list
=
output
        
if
self
.
is_mac_bundle
:
          
link_file_list
=
self
.
xcode_settings
.
GetWrapperName
(
)
        
if
arch
:
          
link_file_list
+
=
'
.
'
+
arch
        
link_file_list
+
=
'
.
rsp
'
        
link_file_list
=
link_file_list
.
replace
(
'
'
'
_
'
)
        
extra_bindings
.
append
(
          
(
'
link_file_list
'
            
gyp
.
common
.
EncodePOSIXShellArgument
(
link_file_list
)
)
)
      
if
self
.
flavor
=
=
'
win
'
:
        
extra_bindings
.
append
(
(
'
binary
'
output
)
)
        
if
(
'
/
NOENTRY
'
not
in
ldflags
and
            
not
self
.
msvs_settings
.
GetNoImportLibrary
(
config_name
)
)
:
          
self
.
target
.
import_lib
=
output
+
'
.
lib
'
          
extra_bindings
.
append
(
(
'
implibflag
'
                                 
'
/
IMPLIB
:
%
s
'
%
self
.
target
.
import_lib
)
)
          
pdbname
=
self
.
msvs_settings
.
GetPDBName
(
              
config_name
self
.
ExpandSpecial
output
+
'
.
pdb
'
)
          
output
=
[
output
self
.
target
.
import_lib
]
          
if
pdbname
:
            
output
.
append
(
pdbname
)
      
elif
not
self
.
is_mac_bundle
:
        
output
=
[
output
output
+
'
.
TOC
'
]
      
else
:
        
command
=
command
+
'
_notoc
'
    
elif
self
.
flavor
=
=
'
win
'
:
      
extra_bindings
.
append
(
(
'
binary
'
output
)
)
      
pdbname
=
self
.
msvs_settings
.
GetPDBName
(
          
config_name
self
.
ExpandSpecial
output
+
'
.
pdb
'
)
      
if
pdbname
:
        
output
=
[
output
pdbname
]
    
if
len
(
solibs
)
:
      
extra_bindings
.
append
(
(
'
solibs
'
          
gyp
.
common
.
EncodePOSIXShellList
(
sorted
(
solibs
)
)
)
)
    
ninja_file
.
build
(
output
command
+
command_suffix
link_deps
                     
implicit
=
sorted
(
implicit_deps
)
                     
order_only
=
list
(
order_deps
)
                     
variables
=
extra_bindings
)
    
return
linked_binary
  
def
WriteTarget
(
self
spec
config_name
config
link_deps
compile_deps
)
:
    
extra_link_deps
=
any
(
self
.
target_outputs
.
get
(
dep
)
.
Linkable
(
)
                          
for
dep
in
spec
.
get
(
'
dependencies
'
[
]
)
                          
if
dep
in
self
.
target_outputs
)
    
if
spec
[
'
type
'
]
=
=
'
none
'
or
(
not
link_deps
and
not
extra_link_deps
)
:
      
self
.
target
.
binary
=
compile_deps
      
self
.
target
.
type
=
'
none
'
    
elif
spec
[
'
type
'
]
=
=
'
static_library
'
:
      
self
.
target
.
binary
=
self
.
ComputeOutput
(
spec
)
      
if
(
self
.
flavor
not
in
(
'
mac
'
'
openbsd
'
'
netbsd
'
'
win
'
)
and
not
          
self
.
is_standalone_static_library
)
:
        
self
.
ninja
.
build
(
self
.
target
.
binary
'
alink_thin
'
link_deps
                         
order_only
=
compile_deps
)
      
else
:
        
variables
=
[
]
        
if
self
.
xcode_settings
:
          
libtool_flags
=
self
.
xcode_settings
.
GetLibtoolflags
(
config_name
)
          
if
libtool_flags
:
            
variables
.
append
(
(
'
libtool_flags
'
libtool_flags
)
)
        
if
self
.
msvs_settings
:
          
libflags
=
self
.
msvs_settings
.
GetLibFlags
(
config_name
                                                    
self
.
GypPathToNinja
)
          
variables
.
append
(
(
'
libflags
'
libflags
)
)
        
if
self
.
flavor
!
=
'
mac
'
or
len
(
self
.
archs
)
=
=
1
:
          
self
.
AppendPostbuildVariable
(
variables
spec
                                       
self
.
target
.
binary
self
.
target
.
binary
)
          
self
.
ninja
.
build
(
self
.
target
.
binary
'
alink
'
link_deps
                           
order_only
=
compile_deps
variables
=
variables
)
        
else
:
          
inputs
=
[
]
          
for
arch
in
self
.
archs
:
            
output
=
self
.
ComputeOutput
(
spec
arch
)
            
self
.
arch_subninjas
[
arch
]
.
build
(
output
'
alink
'
link_deps
[
arch
]
                                            
order_only
=
compile_deps
                                            
variables
=
variables
)
            
inputs
.
append
(
output
)
          
self
.
AppendPostbuildVariable
(
variables
spec
                                       
self
.
target
.
binary
self
.
target
.
binary
)
          
self
.
ninja
.
build
(
self
.
target
.
binary
'
alink
'
inputs
                           
variables
=
variables
)
    
else
:
      
self
.
target
.
binary
=
self
.
WriteLink
(
spec
config_name
config
link_deps
                                          
compile_deps
)
    
return
self
.
target
.
binary
  
def
WriteMacBundle
(
self
spec
mac_bundle_depends
is_empty
)
:
    
assert
self
.
is_mac_bundle
    
package_framework
=
spec
[
'
type
'
]
in
(
'
shared_library
'
'
loadable_module
'
)
    
output
=
self
.
ComputeMacBundleOutput
(
)
    
if
is_empty
:
      
output
+
=
'
.
stamp
'
    
variables
=
[
]
    
self
.
AppendPostbuildVariable
(
variables
spec
output
self
.
target
.
binary
                                 
is_command_start
=
not
package_framework
)
    
if
package_framework
and
not
is_empty
:
      
if
spec
[
'
type
'
]
=
=
'
shared_library
'
and
self
.
xcode_settings
.
isIOS
:
        
self
.
ninja
.
build
(
output
'
package_ios_framework
'
mac_bundle_depends
                         
variables
=
variables
)
      
else
:
        
variables
.
append
(
(
'
version
'
self
.
xcode_settings
.
GetFrameworkVersion
(
)
)
)
        
self
.
ninja
.
build
(
output
'
package_framework
'
mac_bundle_depends
                         
variables
=
variables
)
    
else
:
      
self
.
ninja
.
build
(
output
'
stamp
'
mac_bundle_depends
                       
variables
=
variables
)
    
self
.
target
.
bundle
=
output
    
return
output
  
def
GetToolchainEnv
(
self
additional_settings
=
None
)
:
    
"
"
"
Returns
the
variables
toolchain
would
set
for
build
steps
.
"
"
"
    
env
=
self
.
GetSortedXcodeEnv
(
additional_settings
=
additional_settings
)
    
if
self
.
flavor
=
=
'
win
'
:
      
env
=
self
.
GetMsvsToolchainEnv
(
          
additional_settings
=
additional_settings
)
    
return
env
  
def
GetMsvsToolchainEnv
(
self
additional_settings
=
None
)
:
    
"
"
"
Returns
the
variables
Visual
Studio
would
set
for
build
steps
.
"
"
"
    
return
self
.
msvs_settings
.
GetVSMacroEnv
(
'
!
PRODUCT_DIR
'
                                             
config
=
self
.
config_name
)
  
def
GetSortedXcodeEnv
(
self
additional_settings
=
None
)
:
    
"
"
"
Returns
the
variables
Xcode
would
set
for
build
steps
.
"
"
"
    
assert
self
.
abs_build_dir
    
abs_build_dir
=
self
.
abs_build_dir
    
return
gyp
.
xcode_emulation
.
GetSortedXcodeEnv
(
        
self
.
xcode_settings
abs_build_dir
        
os
.
path
.
join
(
abs_build_dir
self
.
build_to_base
)
self
.
config_name
        
additional_settings
)
  
def
GetSortedXcodePostbuildEnv
(
self
)
:
    
"
"
"
Returns
the
variables
Xcode
would
set
for
postbuild
steps
.
"
"
"
    
postbuild_settings
=
{
}
    
strip_save_file
=
self
.
xcode_settings
.
GetPerTargetSetting
(
        
'
CHROMIUM_STRIP_SAVE_FILE
'
)
    
if
strip_save_file
:
      
postbuild_settings
[
'
CHROMIUM_STRIP_SAVE_FILE
'
]
=
strip_save_file
    
return
self
.
GetSortedXcodeEnv
(
additional_settings
=
postbuild_settings
)
  
def
AppendPostbuildVariable
(
self
variables
spec
output
binary
                              
is_command_start
=
False
)
:
    
"
"
"
Adds
a
'
postbuild
'
variable
if
there
is
a
postbuild
for
|
output
|
.
"
"
"
    
postbuild
=
self
.
GetPostbuildCommand
(
spec
output
binary
is_command_start
)
    
if
postbuild
:
      
variables
.
append
(
(
'
postbuilds
'
postbuild
)
)
  
def
GetPostbuildCommand
(
self
spec
output
output_binary
is_command_start
)
:
    
"
"
"
Returns
a
shell
command
that
runs
all
the
postbuilds
and
removes
    
|
output
|
if
any
of
them
fails
.
If
|
is_command_start
|
is
False
then
the
    
returned
string
will
start
with
'
&
&
'
.
"
"
"
    
if
not
self
.
xcode_settings
or
spec
[
'
type
'
]
=
=
'
none
'
or
not
output
:
      
return
'
'
    
output
=
QuoteShellArgument
(
output
self
.
flavor
)
    
postbuilds
=
gyp
.
xcode_emulation
.
GetSpecPostbuildCommands
(
spec
quiet
=
True
)
    
if
output_binary
is
not
None
:
      
postbuilds
=
self
.
xcode_settings
.
AddImplicitPostbuilds
(
          
self
.
config_name
          
os
.
path
.
normpath
(
os
.
path
.
join
(
self
.
base_to_build
output
)
)
          
QuoteShellArgument
(
              
os
.
path
.
normpath
(
os
.
path
.
join
(
self
.
base_to_build
output_binary
)
)
              
self
.
flavor
)
          
postbuilds
quiet
=
True
)
    
if
not
postbuilds
:
      
return
'
'
    
postbuilds
.
insert
(
0
gyp
.
common
.
EncodePOSIXShellList
(
        
[
'
cd
'
self
.
build_to_base
]
)
)
    
env
=
self
.
ComputeExportEnvString
(
self
.
GetSortedXcodePostbuildEnv
(
)
)
    
commands
=
env
+
'
(
'
+
\
        
'
&
&
'
.
join
(
[
ninja_syntax
.
escape
(
command
)
for
command
in
postbuilds
]
)
    
command_string
=
(
commands
+
'
)
;
G
=
?
;
'
                      
'
(
(
exit
G
)
|
|
rm
-
rf
%
s
)
'
%
output
+
'
&
&
exit
G
)
'
)
    
if
is_command_start
:
      
return
'
(
'
+
command_string
+
'
&
&
'
    
else
:
      
return
'
&
&
(
'
+
command_string
  
def
ComputeExportEnvString
(
self
env
)
:
    
"
"
"
Given
an
environment
returns
a
string
looking
like
        
'
export
FOO
=
foo
;
export
BAR
=
"
{
FOO
}
bar
;
'
    
that
exports
|
env
|
to
the
shell
.
"
"
"
    
export_str
=
[
]
    
for
k
v
in
env
:
      
export_str
.
append
(
'
export
%
s
=
%
s
;
'
%
          
(
k
ninja_syntax
.
escape
(
gyp
.
common
.
EncodePOSIXShellArgument
(
v
)
)
)
)
    
return
'
'
.
join
(
export_str
)
  
def
ComputeMacBundleOutput
(
self
)
:
    
"
"
"
Return
the
'
output
'
(
full
output
path
)
to
a
bundle
output
directory
.
"
"
"
    
assert
self
.
is_mac_bundle
    
path
=
generator_default_variables
[
'
PRODUCT_DIR
'
]
    
return
self
.
ExpandSpecial
(
        
os
.
path
.
join
(
path
self
.
xcode_settings
.
GetWrapperName
(
)
)
)
  
def
ComputeOutputFileName
(
self
spec
type
=
None
)
:
    
"
"
"
Compute
the
filename
of
the
final
output
for
the
current
target
.
"
"
"
    
if
not
type
:
      
type
=
spec
[
'
type
'
]
    
default_variables
=
copy
.
copy
(
generator_default_variables
)
    
CalculateVariables
(
default_variables
{
'
flavor
'
:
self
.
flavor
}
)
    
DEFAULT_PREFIX
=
{
      
'
loadable_module
'
:
default_variables
[
'
SHARED_LIB_PREFIX
'
]
      
'
shared_library
'
:
default_variables
[
'
SHARED_LIB_PREFIX
'
]
      
'
static_library
'
:
default_variables
[
'
STATIC_LIB_PREFIX
'
]
      
'
executable
'
:
default_variables
[
'
EXECUTABLE_PREFIX
'
]
      
}
    
prefix
=
spec
.
get
(
'
product_prefix
'
DEFAULT_PREFIX
.
get
(
type
'
'
)
)
    
DEFAULT_EXTENSION
=
{
        
'
loadable_module
'
:
default_variables
[
'
SHARED_LIB_SUFFIX
'
]
        
'
shared_library
'
:
default_variables
[
'
SHARED_LIB_SUFFIX
'
]
        
'
static_library
'
:
default_variables
[
'
STATIC_LIB_SUFFIX
'
]
        
'
executable
'
:
default_variables
[
'
EXECUTABLE_SUFFIX
'
]
      
}
    
extension
=
spec
.
get
(
'
product_extension
'
)
    
if
extension
:
      
extension
=
'
.
'
+
extension
    
else
:
      
extension
=
DEFAULT_EXTENSION
.
get
(
type
'
'
)
    
if
'
product_name
'
in
spec
:
      
target
=
spec
[
'
product_name
'
]
    
else
:
      
target
=
spec
[
'
target_name
'
]
      
if
prefix
=
=
'
lib
'
:
        
target
=
StripPrefix
(
target
'
lib
'
)
    
if
type
in
(
'
static_library
'
'
loadable_module
'
'
shared_library
'
                        
'
executable
'
)
:
      
return
'
%
s
%
s
%
s
'
%
(
prefix
target
extension
)
    
elif
type
=
=
'
none
'
:
      
return
'
%
s
.
stamp
'
%
target
    
else
:
      
raise
Exception
(
'
Unhandled
output
type
%
s
'
%
type
)
  
def
ComputeOutput
(
self
spec
arch
=
None
)
:
    
"
"
"
Compute
the
path
for
the
final
output
of
the
spec
.
"
"
"
    
type
=
spec
[
'
type
'
]
    
if
self
.
flavor
=
=
'
win
'
:
      
override
=
self
.
msvs_settings
.
GetOutputName
(
self
.
config_name
                                                  
self
.
ExpandSpecial
)
      
if
override
:
        
return
override
    
if
arch
is
None
and
self
.
flavor
=
=
'
mac
'
and
type
in
(
        
'
static_library
'
'
executable
'
'
shared_library
'
'
loadable_module
'
)
:
      
filename
=
self
.
xcode_settings
.
GetExecutablePath
(
)
    
else
:
      
filename
=
self
.
ComputeOutputFileName
(
spec
type
)
    
if
arch
is
None
and
'
product_dir
'
in
spec
:
      
path
=
os
.
path
.
join
(
spec
[
'
product_dir
'
]
filename
)
      
return
self
.
ExpandSpecial
(
path
)
    
type_in_output_root
=
[
'
executable
'
'
loadable_module
'
]
    
if
self
.
flavor
=
=
'
mac
'
and
self
.
toolset
=
=
'
target
'
:
      
type_in_output_root
+
=
[
'
shared_library
'
'
static_library
'
]
    
elif
self
.
flavor
=
=
'
win
'
and
self
.
toolset
=
=
'
target
'
:
      
type_in_output_root
+
=
[
'
shared_library
'
]
    
if
arch
is
not
None
:
      
archdir
=
'
arch
'
      
if
self
.
toolset
!
=
'
target
'
:
        
archdir
=
os
.
path
.
join
(
'
arch
'
'
%
s
'
%
self
.
toolset
)
      
return
os
.
path
.
join
(
archdir
AddArch
(
filename
arch
)
)
    
elif
type
in
type_in_output_root
or
self
.
is_standalone_static_library
:
      
return
filename
    
elif
type
=
=
'
shared_library
'
:
      
libdir
=
'
lib
'
      
if
self
.
toolset
!
=
'
target
'
:
        
libdir
=
os
.
path
.
join
(
'
lib
'
'
%
s
'
%
self
.
toolset
)
      
return
os
.
path
.
join
(
libdir
filename
)
    
else
:
      
return
self
.
GypPathToUniqueOutput
(
filename
qualified
=
False
)
  
def
WriteVariableList
(
self
ninja_file
var
values
)
:
    
assert
not
isinstance
(
values
str
)
    
if
values
is
None
:
      
values
=
[
]
    
ninja_file
.
variable
(
var
'
'
.
join
(
values
)
)
  
def
WriteNewNinjaRule
(
self
name
args
description
is_cygwin
env
pool
                        
depfile
=
None
)
:
    
"
"
"
Write
out
a
new
ninja
"
rule
"
statement
for
a
given
command
.
    
Returns
the
name
of
the
new
rule
and
a
copy
of
|
args
|
with
variables
    
expanded
.
"
"
"
    
if
self
.
flavor
=
=
'
win
'
:
      
args
=
[
self
.
msvs_settings
.
ConvertVSMacros
(
                  
arg
self
.
base_to_build
config
=
self
.
config_name
)
              
for
arg
in
args
]
      
description
=
self
.
msvs_settings
.
ConvertVSMacros
(
          
description
config
=
self
.
config_name
)
    
elif
self
.
flavor
=
=
'
mac
'
:
      
args
=
[
gyp
.
xcode_emulation
.
ExpandEnvVars
(
arg
env
)
for
arg
in
args
]
      
description
=
gyp
.
xcode_emulation
.
ExpandEnvVars
(
description
env
)
    
rule_name
=
self
.
name
    
if
self
.
toolset
=
=
'
target
'
:
      
rule_name
+
=
'
.
'
+
self
.
toolset
    
rule_name
+
=
'
.
'
+
name
    
rule_name
=
re
.
sub
(
'
[
^
a
-
zA
-
Z0
-
9_
]
'
'
_
'
rule_name
)
    
protect
=
[
'
{
root
}
'
'
{
dirname
}
'
'
{
source
}
'
'
{
ext
}
'
'
{
name
}
'
]
    
protect
=
'
(
?
!
'
+
'
|
'
.
join
(
map
(
re
.
escape
protect
)
)
+
'
)
'
    
description
=
re
.
sub
(
protect
+
r
'
\
'
'
_
'
description
)
    
rspfile
=
None
    
rspfile_content
=
None
    
args
=
[
self
.
ExpandSpecial
(
arg
self
.
base_to_build
)
for
arg
in
args
]
    
if
self
.
flavor
=
=
'
win
'
:
      
rspfile
=
rule_name
+
'
.
unique_name
.
rsp
'
      
run_in
=
'
'
if
is_cygwin
else
'
'
+
self
.
build_to_base
      
if
is_cygwin
:
        
rspfile_content
=
self
.
msvs_settings
.
BuildCygwinBashCommandLine
(
            
args
self
.
build_to_base
)
      
else
:
        
rspfile_content
=
gyp
.
msvs_emulation
.
EncodeRspFileList
(
args
)
      
command
=
(
'
%
s
gyp
-
win
-
tool
action
-
wrapper
arch
'
%
sys
.
executable
+
                 
rspfile
+
run_in
)
    
else
:
      
env
=
self
.
ComputeExportEnvString
(
env
)
      
command
=
gyp
.
common
.
EncodePOSIXShellList
(
args
)
      
command
=
'
cd
%
s
;
'
%
self
.
build_to_base
+
env
+
command
    
self
.
ninja
.
rule
(
rule_name
command
description
depfile
=
depfile
                    
restat
=
True
pool
=
pool
                    
rspfile
=
rspfile
rspfile_content
=
rspfile_content
)
    
self
.
ninja
.
newline
(
)
    
return
rule_name
args
def
CalculateVariables
(
default_variables
params
)
:
  
"
"
"
Calculate
additional
variables
for
use
in
the
build
(
called
by
gyp
)
.
"
"
"
  
global
generator_additional_non_configuration_keys
  
global
generator_additional_path_sections
  
flavor
=
gyp
.
common
.
GetFlavor
(
params
)
  
if
flavor
=
=
'
mac
'
:
    
default_variables
.
setdefault
(
'
OS
'
'
mac
'
)
    
default_variables
.
setdefault
(
'
SHARED_LIB_SUFFIX
'
'
.
dylib
'
)
    
default_variables
.
setdefault
(
'
SHARED_LIB_DIR
'
                                 
generator_default_variables
[
'
PRODUCT_DIR
'
]
)
    
default_variables
.
setdefault
(
'
LIB_DIR
'
                                 
generator_default_variables
[
'
PRODUCT_DIR
'
]
)
    
import
gyp
.
generator
.
xcode
as
xcode_generator
    
generator_additional_non_configuration_keys
=
getattr
(
xcode_generator
        
'
generator_additional_non_configuration_keys
'
[
]
)
    
generator_additional_path_sections
=
getattr
(
xcode_generator
        
'
generator_additional_path_sections
'
[
]
)
    
global
generator_extra_sources_for_rules
    
generator_extra_sources_for_rules
=
getattr
(
xcode_generator
        
'
generator_extra_sources_for_rules
'
[
]
)
  
elif
flavor
=
=
'
win
'
:
    
exts
=
gyp
.
MSVSUtil
.
TARGET_TYPE_EXT
    
default_variables
.
setdefault
(
'
OS
'
'
win
'
)
    
default_variables
[
'
EXECUTABLE_SUFFIX
'
]
=
'
.
'
+
exts
[
'
executable
'
]
    
default_variables
[
'
STATIC_LIB_PREFIX
'
]
=
'
'
    
default_variables
[
'
STATIC_LIB_SUFFIX
'
]
=
'
.
'
+
exts
[
'
static_library
'
]
    
default_variables
[
'
SHARED_LIB_PREFIX
'
]
=
'
'
    
default_variables
[
'
SHARED_LIB_SUFFIX
'
]
=
'
.
'
+
exts
[
'
shared_library
'
]
    
import
gyp
.
generator
.
msvs
as
msvs_generator
    
generator_additional_non_configuration_keys
=
getattr
(
msvs_generator
        
'
generator_additional_non_configuration_keys
'
[
]
)
    
generator_additional_path_sections
=
getattr
(
msvs_generator
        
'
generator_additional_path_sections
'
[
]
)
    
gyp
.
msvs_emulation
.
CalculateCommonVariables
(
default_variables
params
)
  
else
:
    
operating_system
=
flavor
    
if
flavor
=
=
'
android
'
:
      
operating_system
=
'
linux
'
    
default_variables
.
setdefault
(
'
OS
'
operating_system
)
    
default_variables
.
setdefault
(
'
SHARED_LIB_SUFFIX
'
'
.
so
'
)
    
default_variables
.
setdefault
(
'
SHARED_LIB_DIR
'
                                 
os
.
path
.
join
(
'
!
PRODUCT_DIR
'
'
lib
'
)
)
    
default_variables
.
setdefault
(
'
LIB_DIR
'
                                 
os
.
path
.
join
(
'
!
PRODUCT_DIR
'
'
obj
'
)
)
def
ComputeOutputDir
(
params
)
:
  
"
"
"
Returns
the
path
from
the
toplevel_dir
to
the
build
output
directory
.
"
"
"
  
generator_dir
=
os
.
path
.
relpath
(
params
[
'
options
'
]
.
generator_output
or
'
.
'
)
  
output_dir
=
params
.
get
(
'
generator_flags
'
{
}
)
.
get
(
'
output_dir
'
'
out
'
)
  
return
os
.
path
.
normpath
(
os
.
path
.
join
(
generator_dir
output_dir
)
)
def
CalculateGeneratorInputInfo
(
params
)
:
  
"
"
"
Called
by
__init__
to
initialize
generator
values
based
on
params
.
"
"
"
  
toplevel
=
params
[
'
options
'
]
.
toplevel_dir
  
qualified_out_dir
=
os
.
path
.
normpath
(
os
.
path
.
join
(
      
toplevel
ComputeOutputDir
(
params
)
'
gypfiles
'
)
)
  
global
generator_filelist_paths
  
generator_filelist_paths
=
{
      
'
toplevel
'
:
toplevel
      
'
qualified_out_dir
'
:
qualified_out_dir
  
}
def
OpenOutput
(
path
mode
=
'
w
'
)
:
  
"
"
"
Open
|
path
|
for
writing
creating
directories
if
necessary
.
"
"
"
  
gyp
.
common
.
EnsureDirExists
(
path
)
  
return
open
(
path
mode
)
def
CommandWithWrapper
(
cmd
wrappers
prog
)
:
  
wrapper
=
wrappers
.
get
(
cmd
'
'
)
  
if
wrapper
:
    
return
wrapper
+
'
'
+
prog
  
return
prog
def
GetDefaultConcurrentLinks
(
)
:
  
"
"
"
Returns
a
best
-
guess
for
a
number
of
concurrent
links
.
"
"
"
  
pool_size
=
int
(
os
.
environ
.
get
(
'
GYP_LINK_CONCURRENCY
'
0
)
)
  
if
pool_size
:
    
return
pool_size
  
if
sys
.
platform
in
(
'
win32
'
'
cygwin
'
)
:
    
import
ctypes
    
class
MEMORYSTATUSEX
(
ctypes
.
Structure
)
:
      
_fields_
=
[
        
(
"
dwLength
"
ctypes
.
c_ulong
)
        
(
"
dwMemoryLoad
"
ctypes
.
c_ulong
)
        
(
"
ullTotalPhys
"
ctypes
.
c_ulonglong
)
        
(
"
ullAvailPhys
"
ctypes
.
c_ulonglong
)
        
(
"
ullTotalPageFile
"
ctypes
.
c_ulonglong
)
        
(
"
ullAvailPageFile
"
ctypes
.
c_ulonglong
)
        
(
"
ullTotalVirtual
"
ctypes
.
c_ulonglong
)
        
(
"
ullAvailVirtual
"
ctypes
.
c_ulonglong
)
        
(
"
sullAvailExtendedVirtual
"
ctypes
.
c_ulonglong
)
      
]
    
stat
=
MEMORYSTATUSEX
(
)
    
stat
.
dwLength
=
ctypes
.
sizeof
(
stat
)
    
ctypes
.
windll
.
kernel32
.
GlobalMemoryStatusEx
(
ctypes
.
byref
(
stat
)
)
    
mem_limit
=
max
(
1
stat
.
ullTotalPhys
/
(
5
*
(
2
*
*
30
)
)
)
    
hard_cap
=
max
(
1
int
(
os
.
environ
.
get
(
'
GYP_LINK_CONCURRENCY_MAX
'
2
*
*
32
)
)
)
    
return
min
(
mem_limit
hard_cap
)
  
elif
sys
.
platform
.
startswith
(
'
linux
'
)
:
    
if
os
.
path
.
exists
(
"
/
proc
/
meminfo
"
)
:
      
with
open
(
"
/
proc
/
meminfo
"
)
as
meminfo
:
        
memtotal_re
=
re
.
compile
(
r
'
^
MemTotal
:
\
s
*
(
\
d
*
)
\
s
*
kB
'
)
        
for
line
in
meminfo
:
          
match
=
memtotal_re
.
match
(
line
)
          
if
not
match
:
            
continue
          
return
max
(
1
int
(
match
.
group
(
1
)
)
/
(
8
*
(
2
*
*
20
)
)
)
    
return
1
  
elif
sys
.
platform
=
=
'
darwin
'
:
    
try
:
      
avail_bytes
=
int
(
subprocess
.
check_output
(
[
'
sysctl
'
'
-
n
'
'
hw
.
memsize
'
]
)
)
      
return
max
(
1
avail_bytes
/
(
4
*
(
2
*
*
30
)
)
)
    
except
:
      
return
1
  
else
:
    
return
1
def
_GetWinLinkRuleNameSuffix
(
embed_manifest
)
:
  
"
"
"
Returns
the
suffix
used
to
select
an
appropriate
linking
rule
depending
on
  
whether
the
manifest
embedding
is
enabled
.
"
"
"
  
return
'
_embed
'
if
embed_manifest
else
'
'
def
_AddWinLinkRules
(
master_ninja
embed_manifest
)
:
  
"
"
"
Adds
link
rules
for
Windows
platform
to
|
master_ninja
|
.
"
"
"
  
def
FullLinkCommand
(
ldcmd
out
binary_type
)
:
    
resource_name
=
{
      
'
exe
'
:
'
1
'
      
'
dll
'
:
'
2
'
    
}
[
binary_type
]
    
return
'
%
(
python
)
s
gyp
-
win
-
tool
link
-
with
-
manifests
arch
%
(
embed
)
s
'
\
           
'
%
(
out
)
s
"
%
(
ldcmd
)
s
"
%
(
resname
)
s
mt
rc
"
intermediatemanifest
"
'
\
           
'
manifests
'
%
{
               
'
python
'
:
sys
.
executable
               
'
out
'
:
out
               
'
ldcmd
'
:
ldcmd
               
'
resname
'
:
resource_name
               
'
embed
'
:
embed_manifest
}
  
rule_name_suffix
=
_GetWinLinkRuleNameSuffix
(
embed_manifest
)
  
use_separate_mspdbsrv
=
(
      
int
(
os
.
environ
.
get
(
'
GYP_USE_SEPARATE_MSPDBSRV
'
'
0
'
)
)
!
=
0
)
  
dlldesc
=
'
LINK
%
s
(
DLL
)
binary
'
%
rule_name_suffix
.
upper
(
)
  
dllcmd
=
(
'
%
s
gyp
-
win
-
tool
link
-
wrapper
arch
%
s
'
            
'
ld
/
nologo
implibflag
/
DLL
/
OUT
:
binary
'
            
'
binary
.
rsp
'
%
(
sys
.
executable
use_separate_mspdbsrv
)
)
  
dllcmd
=
FullLinkCommand
(
dllcmd
'
binary
'
'
dll
'
)
  
master_ninja
.
rule
(
'
solink
'
+
rule_name_suffix
                    
description
=
dlldesc
command
=
dllcmd
                    
rspfile
=
'
binary
.
rsp
'
                    
rspfile_content
=
'
libs
in_newline
ldflags
'
                    
restat
=
True
                    
pool
=
'
link_pool
'
)
  
master_ninja
.
rule
(
'
solink_module
'
+
rule_name_suffix
                    
description
=
dlldesc
command
=
dllcmd
                    
rspfile
=
'
binary
.
rsp
'
                    
rspfile_content
=
'
libs
in_newline
ldflags
'
                    
restat
=
True
                    
pool
=
'
link_pool
'
)
  
exe_cmd
=
(
'
%
s
gyp
-
win
-
tool
link
-
wrapper
arch
%
s
'
             
'
ld
/
nologo
/
OUT
:
binary
binary
.
rsp
'
%
              
(
sys
.
executable
use_separate_mspdbsrv
)
)
  
exe_cmd
=
FullLinkCommand
(
exe_cmd
'
binary
'
'
exe
'
)
  
master_ninja
.
rule
(
'
link
'
+
rule_name_suffix
                    
description
=
'
LINK
%
s
binary
'
%
rule_name_suffix
.
upper
(
)
                    
command
=
exe_cmd
                    
rspfile
=
'
binary
.
rsp
'
                    
rspfile_content
=
'
in_newline
libs
ldflags
'
                    
pool
=
'
link_pool
'
)
def
GenerateOutputForConfig
(
target_list
target_dicts
data
params
                            
config_name
)
:
  
options
=
params
[
'
options
'
]
  
flavor
=
gyp
.
common
.
GetFlavor
(
params
)
  
generator_flags
=
params
.
get
(
'
generator_flags
'
{
}
)
  
build_dir
=
os
.
path
.
normpath
(
      
os
.
path
.
join
(
ComputeOutputDir
(
params
)
config_name
)
)
  
toplevel_build
=
os
.
path
.
join
(
options
.
toplevel_dir
build_dir
)
  
master_ninja_file
=
OpenOutput
(
os
.
path
.
join
(
toplevel_build
'
build
.
ninja
'
)
)
  
master_ninja
=
ninja_syntax
.
Writer
(
master_ninja_file
width
=
120
)
  
gyp
.
common
.
CopyTool
(
flavor
toplevel_build
generator_flags
)
  
if
flavor
=
=
'
win
'
:
    
ar
=
'
lib
.
exe
'
    
cc
=
'
UNSET
'
    
cxx
=
'
UNSET
'
    
ld
=
'
link
.
exe
'
    
ld_host
=
'
ld
'
  
else
:
    
ar
=
'
ar
'
    
cc
=
'
cc
'
    
cxx
=
'
c
+
+
'
    
ld
=
'
cc
'
    
ldxx
=
'
cxx
'
    
ld_host
=
'
cc_host
'
    
ldxx_host
=
'
cxx_host
'
  
ar_host
=
ar
  
cc_host
=
None
  
cxx_host
=
None
  
cc_host_global_setting
=
None
  
cxx_host_global_setting
=
None
  
clang_cl
=
None
  
nm
=
'
nm
'
  
nm_host
=
'
nm
'
  
readelf
=
'
readelf
'
  
readelf_host
=
'
readelf
'
  
build_file
_
_
=
gyp
.
common
.
ParseQualifiedTarget
(
target_list
[
0
]
)
  
make_global_settings
=
data
[
build_file
]
.
get
(
'
make_global_settings
'
[
]
)
  
build_to_root
=
gyp
.
common
.
InvertRelativePath
(
build_dir
                                                
options
.
toplevel_dir
)
  
wrappers
=
{
}
  
for
key
value
in
make_global_settings
:
    
if
key
=
=
'
AR
'
:
      
ar
=
os
.
path
.
join
(
build_to_root
value
)
    
if
key
=
=
'
AR
.
host
'
:
      
ar_host
=
os
.
path
.
join
(
build_to_root
value
)
    
if
key
=
=
'
CC
'
:
      
cc
=
os
.
path
.
join
(
build_to_root
value
)
      
if
cc
.
endswith
(
'
clang
-
cl
'
)
:
        
clang_cl
=
cc
    
if
key
=
=
'
CXX
'
:
      
cxx
=
os
.
path
.
join
(
build_to_root
value
)
    
if
key
=
=
'
CC
.
host
'
:
      
cc_host
=
os
.
path
.
join
(
build_to_root
value
)
      
cc_host_global_setting
=
value
    
if
key
=
=
'
CXX
.
host
'
:
      
cxx_host
=
os
.
path
.
join
(
build_to_root
value
)
      
cxx_host_global_setting
=
value
    
if
key
=
=
'
LD
'
:
      
ld
=
os
.
path
.
join
(
build_to_root
value
)
    
if
key
=
=
'
LD
.
host
'
:
      
ld_host
=
os
.
path
.
join
(
build_to_root
value
)
    
if
key
=
=
'
NM
'
:
      
nm
=
os
.
path
.
join
(
build_to_root
value
)
    
if
key
=
=
'
NM
.
host
'
:
      
nm_host
=
os
.
path
.
join
(
build_to_root
value
)
    
if
key
=
=
'
READELF
'
:
      
readelf
=
os
.
path
.
join
(
build_to_root
value
)
    
if
key
=
=
'
READELF
.
host
'
:
      
readelf_host
=
os
.
path
.
join
(
build_to_root
value
)
    
if
key
.
endswith
(
'
_wrapper
'
)
:
      
wrappers
[
key
[
:
-
len
(
'
_wrapper
'
)
]
]
=
os
.
path
.
join
(
build_to_root
value
)
  
for
key
value
in
os
.
environ
.
iteritems
(
)
:
    
if
key
.
lower
(
)
.
endswith
(
'
_wrapper
'
)
:
      
key_prefix
=
key
[
:
-
len
(
'
_wrapper
'
)
]
      
key_prefix
=
re
.
sub
(
r
'
\
.
HOST
'
'
.
host
'
key_prefix
)
      
wrappers
[
key_prefix
]
=
os
.
path
.
join
(
build_to_root
value
)
  
mac_toolchain_dir
=
generator_flags
.
get
(
'
mac_toolchain_dir
'
None
)
  
if
mac_toolchain_dir
:
    
wrappers
[
'
LINK
'
]
=
"
export
DEVELOPER_DIR
=
'
%
s
'
&
&
"
%
mac_toolchain_dir
  
if
flavor
=
=
'
win
'
:
    
configs
=
[
target_dicts
[
qualified_target
]
[
'
configurations
'
]
[
config_name
]
               
for
qualified_target
in
target_list
]
    
shared_system_includes
=
None
    
if
not
generator_flags
.
get
(
'
ninja_use_custom_environment_files
'
0
)
:
      
shared_system_includes
=
\
          
gyp
.
msvs_emulation
.
ExtractSharedMSVSSystemIncludes
(
              
configs
generator_flags
)
    
cl_paths
=
gyp
.
msvs_emulation
.
GenerateEnvironmentFiles
(
        
toplevel_build
generator_flags
shared_system_includes
OpenOutput
)
    
for
arch
path
in
sorted
(
cl_paths
.
iteritems
(
)
)
:
      
if
clang_cl
:
        
path
=
clang_cl
      
command
=
CommandWithWrapper
(
'
CC
'
wrappers
          
QuoteShellArgument
(
path
'
win
'
)
)
      
if
clang_cl
:
        
command
+
=
(
'
-
m32
'
if
arch
=
=
'
x86
'
else
'
-
m64
'
)
      
master_ninja
.
variable
(
'
cl_
'
+
arch
command
)
  
cc
=
GetEnvironFallback
(
[
'
CC_target
'
'
CC
'
]
cc
)
  
master_ninja
.
variable
(
'
cc
'
CommandWithWrapper
(
'
CC
'
wrappers
cc
)
)
  
cxx
=
GetEnvironFallback
(
[
'
CXX_target
'
'
CXX
'
]
cxx
)
  
master_ninja
.
variable
(
'
cxx
'
CommandWithWrapper
(
'
CXX
'
wrappers
cxx
)
)
  
if
flavor
=
=
'
win
'
:
    
master_ninja
.
variable
(
'
ld
'
ld
)
    
master_ninja
.
variable
(
'
idl
'
'
midl
.
exe
'
)
    
master_ninja
.
variable
(
'
ar
'
ar
)
    
master_ninja
.
variable
(
'
rc
'
'
rc
.
exe
'
)
    
master_ninja
.
variable
(
'
ml_x86
'
'
ml
.
exe
'
)
    
master_ninja
.
variable
(
'
ml_x64
'
'
ml64
.
exe
'
)
    
master_ninja
.
variable
(
'
mt
'
'
mt
.
exe
'
)
  
else
:
    
master_ninja
.
variable
(
'
ld
'
CommandWithWrapper
(
'
LINK
'
wrappers
ld
)
)
    
master_ninja
.
variable
(
'
ldxx
'
CommandWithWrapper
(
'
LINK
'
wrappers
ldxx
)
)
    
master_ninja
.
variable
(
'
ar
'
GetEnvironFallback
(
[
'
AR_target
'
'
AR
'
]
ar
)
)
    
if
flavor
!
=
'
mac
'
:
      
master_ninja
.
variable
(
          
'
nm
'
GetEnvironFallback
(
[
'
NM_target
'
'
NM
'
]
nm
)
)
      
master_ninja
.
variable
(
          
'
readelf
'
GetEnvironFallback
(
[
'
READELF_target
'
'
READELF
'
]
readelf
)
)
  
if
generator_supports_multiple_toolsets
:
    
if
not
cc_host
:
      
cc_host
=
cc
    
if
not
cxx_host
:
      
cxx_host
=
cxx
    
master_ninja
.
variable
(
'
ar_host
'
GetEnvironFallback
(
[
'
AR_host
'
]
ar_host
)
)
    
master_ninja
.
variable
(
'
nm_host
'
GetEnvironFallback
(
[
'
NM_host
'
]
nm_host
)
)
    
master_ninja
.
variable
(
'
readelf_host
'
                          
GetEnvironFallback
(
[
'
READELF_host
'
]
readelf_host
)
)
    
cc_host
=
GetEnvironFallback
(
[
'
CC_host
'
]
cc_host
)
    
cxx_host
=
GetEnvironFallback
(
[
'
CXX_host
'
]
cxx_host
)
    
if
'
(
CC
)
'
in
cc_host
and
cc_host_global_setting
:
      
cc_host
=
cc_host_global_setting
.
replace
(
'
(
CC
)
'
cc
)
    
if
'
(
CXX
)
'
in
cxx_host
and
cxx_host_global_setting
:
      
cxx_host
=
cxx_host_global_setting
.
replace
(
'
(
CXX
)
'
cxx
)
    
master_ninja
.
variable
(
'
cc_host
'
                          
CommandWithWrapper
(
'
CC
.
host
'
wrappers
cc_host
)
)
    
master_ninja
.
variable
(
'
cxx_host
'
                          
CommandWithWrapper
(
'
CXX
.
host
'
wrappers
cxx_host
)
)
    
if
flavor
=
=
'
win
'
:
      
master_ninja
.
variable
(
'
ld_host
'
ld_host
)
    
else
:
      
master_ninja
.
variable
(
'
ld_host
'
CommandWithWrapper
(
          
'
LINK
'
wrappers
ld_host
)
)
      
master_ninja
.
variable
(
'
ldxx_host
'
CommandWithWrapper
(
          
'
LINK
'
wrappers
ldxx_host
)
)
  
master_ninja
.
newline
(
)
  
master_ninja
.
pool
(
'
link_pool
'
depth
=
GetDefaultConcurrentLinks
(
)
)
  
master_ninja
.
newline
(
)
  
deps
=
'
msvc
'
if
flavor
=
=
'
win
'
else
'
gcc
'
  
if
flavor
!
=
'
win
'
:
    
master_ninja
.
rule
(
      
'
cc
'
      
description
=
'
CC
out
'
      
command
=
(
'
cc
-
MMD
-
MF
out
.
d
defines
includes
cflags
cflags_c
'
              
'
cflags_pch_c
-
c
in
-
o
out
'
)
      
depfile
=
'
out
.
d
'
      
deps
=
deps
)
    
master_ninja
.
rule
(
      
'
cc_s
'
      
description
=
'
CC
out
'
      
command
=
(
'
cc
defines
includes
cflags
cflags_c
'
              
'
cflags_pch_c
-
c
in
-
o
out
'
)
)
    
master_ninja
.
rule
(
      
'
cxx
'
      
description
=
'
CXX
out
'
      
command
=
(
'
cxx
-
MMD
-
MF
out
.
d
defines
includes
cflags
cflags_cc
'
              
'
cflags_pch_cc
-
c
in
-
o
out
'
)
      
depfile
=
'
out
.
d
'
      
deps
=
deps
)
  
else
:
    
cc_command
=
(
'
ninja
-
t
msvc
-
e
arch
'
+
                  
'
-
-
'
                  
'
cc
/
nologo
/
showIncludes
/
FC
'
                  
'
out
.
rsp
/
c
in
/
Fo
out
/
Fd
pdbname_c
'
)
    
cxx_command
=
(
'
ninja
-
t
msvc
-
e
arch
'
+
                   
'
-
-
'
                   
'
cxx
/
nologo
/
showIncludes
/
FC
'
                   
'
out
.
rsp
/
c
in
/
Fo
out
/
Fd
pdbname_cc
'
)
    
master_ninja
.
rule
(
      
'
cc
'
      
description
=
'
CC
out
'
      
command
=
cc_command
      
rspfile
=
'
out
.
rsp
'
      
rspfile_content
=
'
defines
includes
cflags
cflags_c
'
      
deps
=
deps
)
    
master_ninja
.
rule
(
      
'
cxx
'
      
description
=
'
CXX
out
'
      
command
=
cxx_command
      
rspfile
=
'
out
.
rsp
'
      
rspfile_content
=
'
defines
includes
cflags
cflags_cc
'
      
deps
=
deps
)
    
master_ninja
.
rule
(
      
'
idl
'
      
description
=
'
IDL
in
'
      
command
=
(
'
%
s
gyp
-
win
-
tool
midl
-
wrapper
arch
outdir
'
               
'
tlb
h
dlldata
iid
proxy
in
'
               
'
midl_includes
idlflags
'
%
sys
.
executable
)
)
    
master_ninja
.
rule
(
      
'
rc
'
      
description
=
'
RC
in
'
      
command
=
(
'
%
s
gyp
-
win
-
tool
rc
-
wrapper
'
               
'
arch
rc
defines
resource_includes
rcflags
/
fo
out
in
'
%
               
sys
.
executable
)
)
    
master_ninja
.
rule
(
      
'
asm
'
      
description
=
'
ASM
out
'
      
command
=
(
'
%
s
gyp
-
win
-
tool
asm
-
wrapper
'
               
'
arch
asm
defines
includes
asmflags
/
c
/
Fo
out
in
'
%
               
sys
.
executable
)
)
  
if
flavor
!
=
'
mac
'
and
flavor
!
=
'
win
'
:
    
master_ninja
.
rule
(
      
'
alink
'
      
description
=
'
AR
out
'
      
command
=
'
rm
-
f
out
&
&
ar
rcs
arflags
out
in
'
)
    
master_ninja
.
rule
(
      
'
alink_thin
'
      
description
=
'
AR
out
'
      
command
=
'
rm
-
f
out
&
&
ar
rcsT
arflags
out
in
'
)
    
mtime_preserving_solink_base
=
(
        
'
if
[
!
-
e
lib
-
o
!
-
e
lib
.
TOC
]
;
then
'
        
'
%
(
solink
)
s
&
&
%
(
extract_toc
)
s
>
lib
.
TOC
;
else
'
        
'
%
(
solink
)
s
&
&
%
(
extract_toc
)
s
>
lib
.
tmp
&
&
'
        
'
if
!
cmp
-
s
lib
.
tmp
lib
.
TOC
;
then
mv
lib
.
tmp
lib
.
TOC
;
'
        
'
fi
;
fi
'
        
%
{
'
solink
'
:
              
'
ld
-
shared
ldflags
-
o
lib
-
Wl
-
soname
=
soname
%
(
suffix
)
s
'
            
'
extract_toc
'
:
              
(
'
{
readelf
-
d
lib
|
grep
SONAME
;
'
               
'
nm
-
gD
-
f
p
lib
|
cut
-
f1
-
2
-
d
\
'
\
'
;
}
'
)
}
)
    
master_ninja
.
rule
(
      
'
solink
'
      
description
=
'
SOLINK
lib
'
      
restat
=
True
      
command
=
mtime_preserving_solink_base
%
{
'
suffix
'
:
'
link_file_list
'
}
      
rspfile
=
'
link_file_list
'
      
rspfile_content
=
          
'
-
Wl
-
-
whole
-
archive
in
solibs
-
Wl
-
-
no
-
whole
-
archive
libs
'
      
pool
=
'
link_pool
'
)
    
master_ninja
.
rule
(
      
'
solink_module
'
      
description
=
'
SOLINK
(
module
)
lib
'
      
restat
=
True
      
command
=
mtime_preserving_solink_base
%
{
'
suffix
'
:
'
link_file_list
'
}
      
rspfile
=
'
link_file_list
'
      
rspfile_content
=
'
-
Wl
-
-
start
-
group
in
-
Wl
-
-
end
-
group
solibs
libs
'
      
pool
=
'
link_pool
'
)
    
master_ninja
.
rule
(
      
'
link
'
      
description
=
'
LINK
out
'
      
command
=
(
'
ld
ldflags
-
o
out
'
               
'
-
Wl
-
-
start
-
group
in
-
Wl
-
-
end
-
group
solibs
libs
'
)
      
pool
=
'
link_pool
'
)
  
elif
flavor
=
=
'
win
'
:
    
master_ninja
.
rule
(
        
'
alink
'
        
description
=
'
LIB
out
'
        
command
=
(
'
%
s
gyp
-
win
-
tool
link
-
wrapper
arch
False
'
                 
'
ar
/
nologo
/
ignore
:
4221
/
OUT
:
out
out
.
rsp
'
%
                 
sys
.
executable
)
        
rspfile
=
'
out
.
rsp
'
        
rspfile_content
=
'
in_newline
libflags
'
)
    
_AddWinLinkRules
(
master_ninja
embed_manifest
=
True
)
    
_AddWinLinkRules
(
master_ninja
embed_manifest
=
False
)
  
else
:
    
master_ninja
.
rule
(
      
'
objc
'
      
description
=
'
OBJC
out
'
      
command
=
(
'
cc
-
MMD
-
MF
out
.
d
defines
includes
cflags
cflags_objc
'
               
'
cflags_pch_objc
-
c
in
-
o
out
'
)
      
depfile
=
'
out
.
d
'
      
deps
=
deps
)
    
master_ninja
.
rule
(
      
'
objcxx
'
      
description
=
'
OBJCXX
out
'
      
command
=
(
'
cxx
-
MMD
-
MF
out
.
d
defines
includes
cflags
cflags_objcc
'
               
'
cflags_pch_objcc
-
c
in
-
o
out
'
)
      
depfile
=
'
out
.
d
'
      
deps
=
deps
)
    
master_ninja
.
rule
(
      
'
alink
'
      
description
=
'
LIBTOOL
-
STATIC
out
POSTBUILDS
'
      
command
=
'
rm
-
f
out
&
&
'
              
'
.
/
gyp
-
mac
-
tool
filter
-
libtool
libtool
libtool_flags
'
              
'
-
static
-
o
out
in
'
              
'
postbuilds
'
)
    
master_ninja
.
rule
(
      
'
lipo
'
      
description
=
'
LIPO
out
POSTBUILDS
'
      
command
=
'
rm
-
f
out
&
&
lipo
-
create
in
-
output
out
postbuilds
'
)
    
master_ninja
.
rule
(
      
'
solipo
'
      
description
=
'
SOLIPO
out
POSTBUILDS
'
      
command
=
(
          
'
rm
-
f
lib
lib
.
TOC
&
&
lipo
-
create
in
-
output
lib
postbuilds
&
&
'
          
'
%
(
extract_toc
)
s
>
lib
.
TOC
'
          
%
{
'
extract_toc
'
:
                
'
{
otool
-
l
lib
|
grep
LC_ID_DYLIB
-
A
5
;
'
                
'
nm
-
gP
lib
|
cut
-
f1
-
2
-
d
\
'
\
'
|
grep
-
v
U
;
true
;
}
'
}
)
)
    
solink_base
=
'
ld
%
(
type
)
s
ldflags
-
o
lib
%
(
suffix
)
s
'
    
mtime_preserving_solink_base
=
(
        
'
if
[
!
-
e
lib
-
o
!
-
e
lib
.
TOC
]
|
|
'
             
'
otool
-
l
lib
|
grep
-
q
LC_REEXPORT_DYLIB
;
then
'
          
'
%
(
solink
)
s
&
&
%
(
extract_toc
)
s
>
lib
.
TOC
;
'
        
'
else
'
          
'
%
(
solink
)
s
&
&
%
(
extract_toc
)
s
>
lib
.
tmp
&
&
'
          
'
if
!
cmp
-
s
lib
.
tmp
lib
.
TOC
;
then
'
            
'
mv
lib
.
tmp
lib
.
TOC
;
'
          
'
fi
;
'
        
'
fi
'
        
%
{
'
solink
'
:
solink_base
            
'
extract_toc
'
:
              
'
{
otool
-
l
lib
|
grep
LC_ID_DYLIB
-
A
5
;
'
              
'
nm
-
gP
lib
|
cut
-
f1
-
2
-
d
\
'
\
'
|
grep
-
v
U
;
true
;
}
'
}
)
    
solink_suffix
=
'
link_file_list
postbuilds
'
    
master_ninja
.
rule
(
      
'
solink
'
      
description
=
'
SOLINK
lib
POSTBUILDS
'
      
restat
=
True
      
command
=
mtime_preserving_solink_base
%
{
'
suffix
'
:
solink_suffix
                                              
'
type
'
:
'
-
shared
'
}
      
rspfile
=
'
link_file_list
'
      
rspfile_content
=
'
in
solibs
libs
'
      
pool
=
'
link_pool
'
)
    
master_ninja
.
rule
(
      
'
solink_notoc
'
      
description
=
'
SOLINK
lib
POSTBUILDS
'
      
restat
=
True
      
command
=
solink_base
%
{
'
suffix
'
:
solink_suffix
'
type
'
:
'
-
shared
'
}
      
rspfile
=
'
link_file_list
'
      
rspfile_content
=
'
in
solibs
libs
'
      
pool
=
'
link_pool
'
)
    
master_ninja
.
rule
(
      
'
solink_module
'
      
description
=
'
SOLINK
(
module
)
lib
POSTBUILDS
'
      
restat
=
True
      
command
=
mtime_preserving_solink_base
%
{
'
suffix
'
:
solink_suffix
                                              
'
type
'
:
'
-
bundle
'
}
      
rspfile
=
'
link_file_list
'
      
rspfile_content
=
'
in
solibs
libs
'
      
pool
=
'
link_pool
'
)
    
master_ninja
.
rule
(
      
'
solink_module_notoc
'
      
description
=
'
SOLINK
(
module
)
lib
POSTBUILDS
'
      
restat
=
True
      
command
=
solink_base
%
{
'
suffix
'
:
solink_suffix
'
type
'
:
'
-
bundle
'
}
      
rspfile
=
'
link_file_list
'
      
rspfile_content
=
'
in
solibs
libs
'
      
pool
=
'
link_pool
'
)
    
master_ninja
.
rule
(
      
'
link
'
      
description
=
'
LINK
out
POSTBUILDS
'
      
command
=
(
'
ld
ldflags
-
o
out
'
               
'
in
solibs
libs
postbuilds
'
)
      
pool
=
'
link_pool
'
)
    
master_ninja
.
rule
(
      
'
preprocess_infoplist
'
      
description
=
'
PREPROCESS
INFOPLIST
out
'
      
command
=
(
'
cc
-
E
-
P
-
Wno
-
trigraphs
-
x
c
defines
in
-
o
out
&
&
'
               
'
plutil
-
convert
xml1
out
out
'
)
)
    
master_ninja
.
rule
(
      
'
copy_infoplist
'
      
description
=
'
COPY
INFOPLIST
in
'
      
command
=
'
env
.
/
gyp
-
mac
-
tool
copy
-
info
-
plist
in
out
binary
keys
'
)
    
master_ninja
.
rule
(
      
'
merge_infoplist
'
      
description
=
'
MERGE
INFOPLISTS
in
'
      
command
=
'
env
.
/
gyp
-
mac
-
tool
merge
-
info
-
plist
out
in
'
)
    
master_ninja
.
rule
(
      
'
compile_xcassets
'
      
description
=
'
COMPILE
XCASSETS
in
'
      
command
=
'
env
.
/
gyp
-
mac
-
tool
compile
-
xcassets
keys
in
'
)
    
master_ninja
.
rule
(
      
'
compile_ios_framework_headers
'
      
description
=
'
COMPILE
HEADER
MAPS
AND
COPY
FRAMEWORK
HEADERS
in
'
      
command
=
'
env
.
/
gyp
-
mac
-
tool
compile
-
ios
-
framework
-
header
-
map
out
'
              
'
framework
in
&
&
env
.
/
gyp
-
mac
-
tool
'
              
'
copy
-
ios
-
framework
-
headers
framework
copy_headers
'
)
    
master_ninja
.
rule
(
      
'
mac_tool
'
      
description
=
'
MACTOOL
mactool_cmd
in
'
      
command
=
'
env
.
/
gyp
-
mac
-
tool
mactool_cmd
in
out
binary
'
)
    
master_ninja
.
rule
(
      
'
package_framework
'
      
description
=
'
PACKAGE
FRAMEWORK
out
POSTBUILDS
'
      
command
=
'
.
/
gyp
-
mac
-
tool
package
-
framework
out
version
postbuilds
'
              
'
&
&
touch
out
'
)
    
master_ninja
.
rule
(
      
'
package_ios_framework
'
      
description
=
'
PACKAGE
IOS
FRAMEWORK
out
POSTBUILDS
'
      
command
=
'
.
/
gyp
-
mac
-
tool
package
-
ios
-
framework
out
postbuilds
'
              
'
&
&
touch
out
'
)
  
if
flavor
=
=
'
win
'
:
    
master_ninja
.
rule
(
      
'
stamp
'
      
description
=
'
STAMP
out
'
      
command
=
'
%
s
gyp
-
win
-
tool
stamp
out
'
%
sys
.
executable
)
  
else
:
    
master_ninja
.
rule
(
      
'
stamp
'
      
description
=
'
STAMP
out
'
      
command
=
'
{
postbuilds
}
touch
out
'
)
  
if
flavor
=
=
'
win
'
:
    
master_ninja
.
rule
(
      
'
copy
'
      
description
=
'
COPY
in
out
'
      
command
=
'
%
s
gyp
-
win
-
tool
recursive
-
mirror
in
out
'
%
sys
.
executable
)
  
elif
flavor
=
=
'
zos
'
:
    
master_ninja
.
rule
(
      
'
copy
'
      
description
=
'
COPY
in
out
'
      
command
=
'
rm
-
rf
out
&
&
cp
-
fRP
in
out
'
)
  
else
:
    
master_ninja
.
rule
(
      
'
copy
'
      
description
=
'
COPY
in
out
'
      
command
=
'
ln
-
f
in
out
2
>
/
dev
/
null
|
|
(
rm
-
rf
out
&
&
cp
-
af
in
out
)
'
)
  
master_ninja
.
newline
(
)
  
all_targets
=
set
(
)
  
for
build_file
in
params
[
'
build_files
'
]
:
    
for
target
in
gyp
.
common
.
AllTargets
(
target_list
                                        
target_dicts
                                        
os
.
path
.
normpath
(
build_file
)
)
:
      
all_targets
.
add
(
target
)
  
all_outputs
=
set
(
)
  
target_outputs
=
{
}
  
target_short_names
=
{
}
  
empty_target_names
=
set
(
)
  
non_empty_target_names
=
set
(
)
  
for
qualified_target
in
target_list
:
    
build_file
name
toolset
=
\
        
gyp
.
common
.
ParseQualifiedTarget
(
qualified_target
)
    
this_make_global_settings
=
data
[
build_file
]
.
get
(
'
make_global_settings
'
[
]
)
    
assert
make_global_settings
=
=
this_make_global_settings
(
        
"
make_global_settings
needs
to
be
the
same
for
all
targets
.
%
s
vs
.
%
s
"
%
        
(
this_make_global_settings
make_global_settings
)
)
    
spec
=
target_dicts
[
qualified_target
]
    
if
flavor
=
=
'
mac
'
:
      
gyp
.
xcode_emulation
.
MergeGlobalXcodeSettingsToSpec
(
data
[
build_file
]
spec
)
    
build_file
=
gyp
.
common
.
RelativePath
(
build_file
options
.
toplevel_dir
                                         
False
)
    
qualified_target_for_hash
=
gyp
.
common
.
QualifiedTarget
(
build_file
name
                                                           
toolset
)
    
hash_for_rules
=
hashlib
.
md5
(
qualified_target_for_hash
)
.
hexdigest
(
)
    
base_path
=
os
.
path
.
dirname
(
build_file
)
    
obj
=
'
obj
'
    
if
toolset
!
=
'
target
'
:
      
obj
+
=
'
.
'
+
toolset
    
output_file
=
os
.
path
.
join
(
obj
base_path
name
+
'
.
ninja
'
)
    
ninja_output
=
StringIO
(
)
    
writer
=
NinjaWriter
(
hash_for_rules
target_outputs
base_path
build_dir
                         
ninja_output
                         
toplevel_build
output_file
                         
flavor
toplevel_dir
=
options
.
toplevel_dir
)
    
target
=
writer
.
WriteSpec
(
spec
config_name
generator_flags
)
    
if
ninja_output
.
tell
(
)
>
0
:
      
with
OpenOutput
(
os
.
path
.
join
(
toplevel_build
output_file
)
)
as
ninja_file
:
        
ninja_file
.
write
(
ninja_output
.
getvalue
(
)
)
      
ninja_output
.
close
(
)
      
master_ninja
.
subninja
(
output_file
)
    
if
target
:
      
if
name
!
=
target
.
FinalOutput
(
)
and
spec
[
'
toolset
'
]
=
=
'
target
'
:
        
target_short_names
.
setdefault
(
name
[
]
)
.
append
(
target
)
      
target_outputs
[
qualified_target
]
=
target
      
if
qualified_target
in
all_targets
:
        
all_outputs
.
add
(
target
.
FinalOutput
(
)
)
      
non_empty_target_names
.
add
(
name
)
    
else
:
      
empty_target_names
.
add
(
name
)
  
if
target_short_names
:
    
master_ninja
.
newline
(
)
    
master_ninja
.
comment
(
'
Short
names
for
targets
.
'
)
    
for
short_name
in
sorted
(
target_short_names
)
:
      
master_ninja
.
build
(
short_name
'
phony
'
[
x
.
FinalOutput
(
)
for
x
in
                                               
target_short_names
[
short_name
]
]
)
  
empty_target_names
=
empty_target_names
-
non_empty_target_names
  
if
empty_target_names
:
    
master_ninja
.
newline
(
)
    
master_ninja
.
comment
(
'
Empty
targets
(
output
for
completeness
)
.
'
)
    
for
name
in
sorted
(
empty_target_names
)
:
      
master_ninja
.
build
(
name
'
phony
'
)
  
if
all_outputs
:
    
master_ninja
.
newline
(
)
    
master_ninja
.
build
(
'
all
'
'
phony
'
sorted
(
all_outputs
)
)
    
master_ninja
.
default
(
generator_flags
.
get
(
'
default_target
'
'
all
'
)
)
  
master_ninja_file
.
close
(
)
def
PerformBuild
(
data
configurations
params
)
:
  
options
=
params
[
'
options
'
]
  
for
config
in
configurations
:
    
builddir
=
os
.
path
.
join
(
options
.
toplevel_dir
'
out
'
config
)
    
arguments
=
[
'
ninja
'
'
-
C
'
builddir
]
    
print
'
Building
[
%
s
]
:
%
s
'
%
(
config
arguments
)
    
subprocess
.
check_call
(
arguments
)
def
CallGenerateOutputForConfig
(
arglist
)
:
  
signal
.
signal
(
signal
.
SIGINT
signal
.
SIG_IGN
)
  
(
target_list
target_dicts
data
params
config_name
)
=
arglist
  
GenerateOutputForConfig
(
target_list
target_dicts
data
params
config_name
)
def
GenerateOutput
(
target_list
target_dicts
data
params
)
:
  
target_dicts
=
gyp
.
xcode_emulation
.
CloneConfigurationForDeviceAndEmulator
(
      
target_dicts
)
  
user_config
=
params
.
get
(
'
generator_flags
'
{
}
)
.
get
(
'
config
'
None
)
  
if
gyp
.
common
.
GetFlavor
(
params
)
=
=
'
win
'
:
    
target_list
target_dicts
=
MSVSUtil
.
ShardTargets
(
target_list
target_dicts
)
    
target_list
target_dicts
=
MSVSUtil
.
InsertLargePdbShims
(
        
target_list
target_dicts
generator_default_variables
)
  
if
user_config
:
    
GenerateOutputForConfig
(
target_list
target_dicts
data
params
                            
user_config
)
  
else
:
    
config_names
=
target_dicts
[
target_list
[
0
]
]
[
'
configurations
'
]
.
keys
(
)
    
if
params
[
'
parallel
'
]
:
      
try
:
        
pool
=
multiprocessing
.
Pool
(
len
(
config_names
)
)
        
arglists
=
[
]
        
for
config_name
in
config_names
:
          
arglists
.
append
(
              
(
target_list
target_dicts
data
params
config_name
)
)
        
pool
.
map
(
CallGenerateOutputForConfig
arglists
)
      
except
KeyboardInterrupt
e
:
        
pool
.
terminate
(
)
        
raise
e
    
else
:
      
for
config_name
in
config_names
:
        
GenerateOutputForConfig
(
target_list
target_dicts
data
params
                                
config_name
)
