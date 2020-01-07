from
compiler
.
ast
import
Const
from
compiler
.
ast
import
Dict
from
compiler
.
ast
import
Discard
from
compiler
.
ast
import
List
from
compiler
.
ast
import
Module
from
compiler
.
ast
import
Node
from
compiler
.
ast
import
Stmt
import
compiler
import
gyp
.
common
import
gyp
.
simple_copy
import
multiprocessing
import
optparse
import
os
.
path
import
re
import
shlex
import
signal
import
subprocess
import
sys
import
threading
import
time
import
traceback
from
gyp
.
common
import
GypError
from
gyp
.
common
import
OrderedSet
linkable_types
=
[
  
'
executable
'
  
'
shared_library
'
  
'
loadable_module
'
  
'
mac_kernel_extension
'
  
'
windows_driver
'
]
dependency_sections
=
[
'
dependencies
'
'
export_dependent_settings
'
]
base_path_sections
=
[
  
'
destination
'
  
'
files
'
  
'
include_dirs
'
  
'
inputs
'
  
'
libraries
'
  
'
outputs
'
  
'
sources
'
]
path_sections
=
set
(
)
per_process_data
=
{
}
per_process_aux_data
=
{
}
def
IsPathSection
(
section
)
:
  
while
section
and
section
[
-
1
:
]
in
'
=
+
?
!
'
:
    
section
=
section
[
:
-
1
]
  
if
section
in
path_sections
:
    
return
True
  
if
"
_
"
in
section
:
    
tail
=
section
[
-
6
:
]
    
if
tail
[
-
1
]
=
=
'
s
'
:
      
tail
=
tail
[
:
-
1
]
    
if
tail
[
-
5
:
]
in
(
'
_file
'
'
_path
'
)
:
      
return
True
    
return
tail
[
-
4
:
]
=
=
'
_dir
'
  
return
False
base_non_configuration_keys
=
[
  
'
actions
'
  
'
configurations
'
  
'
copies
'
  
'
default_configuration
'
  
'
dependencies
'
  
'
dependencies_original
'
  
'
libraries
'
  
'
postbuilds
'
  
'
product_dir
'
  
'
product_extension
'
  
'
product_name
'
  
'
product_prefix
'
  
'
rules
'
  
'
run_as
'
  
'
sources
'
  
'
standalone_static_library
'
  
'
suppress_wildcard
'
  
'
target_name
'
  
'
toolset
'
  
'
toolsets
'
  
'
type
'
  
'
variables
'
]
non_configuration_keys
=
[
]
invalid_configuration_keys
=
[
  
'
actions
'
  
'
all_dependent_settings
'
  
'
configurations
'
  
'
dependencies
'
  
'
direct_dependent_settings
'
  
'
libraries
'
  
'
link_settings
'
  
'
sources
'
  
'
standalone_static_library
'
  
'
target_name
'
  
'
type
'
]
multiple_toolsets
=
False
generator_filelist_paths
=
None
def
GetIncludedBuildFiles
(
build_file_path
aux_data
included
=
None
)
:
  
"
"
"
Return
a
list
of
all
build
files
included
into
build_file_path
.
  
The
returned
list
will
contain
build_file_path
as
well
as
all
other
files
  
that
it
included
either
directly
or
indirectly
.
Note
that
the
list
may
  
contain
files
that
were
included
into
a
conditional
section
that
evaluated
  
to
false
and
was
not
merged
into
build_file_path
'
s
dict
.
  
aux_data
is
a
dict
containing
a
key
for
each
build
file
or
included
build
  
file
.
Those
keys
provide
access
to
dicts
whose
"
included
"
keys
contain
  
lists
of
all
other
files
included
by
the
build
file
.
  
included
should
be
left
at
its
default
None
value
by
external
callers
.
It
  
is
used
for
recursion
.
  
The
returned
list
will
not
contain
any
duplicate
entries
.
Each
build
file
  
in
the
list
will
be
relative
to
the
current
directory
.
  
"
"
"
  
if
included
=
=
None
:
    
included
=
[
]
  
if
build_file_path
in
included
:
    
return
included
  
included
.
append
(
build_file_path
)
  
for
included_build_file
in
aux_data
[
build_file_path
]
.
get
(
'
included
'
[
]
)
:
    
GetIncludedBuildFiles
(
included_build_file
aux_data
included
)
  
return
included
def
CheckedEval
(
file_contents
)
:
  
"
"
"
Return
the
eval
of
a
gyp
file
.
  
The
gyp
file
is
restricted
to
dictionaries
and
lists
only
and
  
repeated
keys
are
not
allowed
.
  
Note
that
this
is
slower
than
eval
(
)
is
.
  
"
"
"
  
ast
=
compiler
.
parse
(
file_contents
)
  
assert
isinstance
(
ast
Module
)
  
c1
=
ast
.
getChildren
(
)
  
assert
c1
[
0
]
is
None
  
assert
isinstance
(
c1
[
1
]
Stmt
)
  
c2
=
c1
[
1
]
.
getChildren
(
)
  
assert
isinstance
(
c2
[
0
]
Discard
)
  
c3
=
c2
[
0
]
.
getChildren
(
)
  
assert
len
(
c3
)
=
=
1
  
return
CheckNode
(
c3
[
0
]
[
]
)
def
CheckNode
(
node
keypath
)
:
  
if
isinstance
(
node
Dict
)
:
    
c
=
node
.
getChildren
(
)
    
dict
=
{
}
    
for
n
in
range
(
0
len
(
c
)
2
)
:
      
assert
isinstance
(
c
[
n
]
Const
)
      
key
=
c
[
n
]
.
getChildren
(
)
[
0
]
      
if
key
in
dict
:
        
raise
GypError
(
"
Key
'
"
+
key
+
"
'
repeated
at
level
"
+
              
repr
(
len
(
keypath
)
+
1
)
+
"
with
key
path
'
"
+
              
'
.
'
.
join
(
keypath
)
+
"
'
"
)
      
kp
=
list
(
keypath
)
      
kp
.
append
(
key
)
      
dict
[
key
]
=
CheckNode
(
c
[
n
+
1
]
kp
)
    
return
dict
  
elif
isinstance
(
node
List
)
:
    
c
=
node
.
getChildren
(
)
    
children
=
[
]
    
for
index
child
in
enumerate
(
c
)
:
      
kp
=
list
(
keypath
)
      
kp
.
append
(
repr
(
index
)
)
      
children
.
append
(
CheckNode
(
child
kp
)
)
    
return
children
  
elif
isinstance
(
node
Const
)
:
    
return
node
.
getChildren
(
)
[
0
]
  
else
:
    
raise
TypeError
(
"
Unknown
AST
node
at
key
path
'
"
+
'
.
'
.
join
(
keypath
)
+
         
"
'
:
"
+
repr
(
node
)
)
def
LoadOneBuildFile
(
build_file_path
data
aux_data
includes
                     
is_target
check
)
:
  
if
build_file_path
in
data
:
    
return
data
[
build_file_path
]
  
if
os
.
path
.
exists
(
build_file_path
)
:
    
build_file_contents
=
open
(
build_file_path
)
.
read
(
)
  
else
:
    
raise
GypError
(
"
%
s
not
found
(
cwd
:
%
s
)
"
%
(
build_file_path
os
.
getcwd
(
)
)
)
  
build_file_data
=
None
  
try
:
    
if
check
:
      
build_file_data
=
CheckedEval
(
build_file_contents
)
    
else
:
      
build_file_data
=
eval
(
build_file_contents
{
'
__builtins__
'
:
None
}
                             
None
)
  
except
SyntaxError
e
:
    
e
.
filename
=
build_file_path
    
raise
  
except
Exception
e
:
    
gyp
.
common
.
ExceptionAppend
(
e
'
while
reading
'
+
build_file_path
)
    
raise
  
if
type
(
build_file_data
)
is
not
dict
:
    
raise
GypError
(
"
%
s
does
not
evaluate
to
a
dictionary
.
"
%
build_file_path
)
  
data
[
build_file_path
]
=
build_file_data
  
aux_data
[
build_file_path
]
=
{
}
  
if
(
'
skip_includes
'
not
in
build_file_data
or
      
not
build_file_data
[
'
skip_includes
'
]
)
:
    
try
:
      
if
is_target
:
        
LoadBuildFileIncludesIntoDict
(
build_file_data
build_file_path
data
                                      
aux_data
includes
check
)
      
else
:
        
LoadBuildFileIncludesIntoDict
(
build_file_data
build_file_path
data
                                      
aux_data
None
check
)
    
except
Exception
e
:
      
gyp
.
common
.
ExceptionAppend
(
e
                                 
'
while
reading
includes
of
'
+
build_file_path
)
      
raise
  
return
build_file_data
def
LoadBuildFileIncludesIntoDict
(
subdict
subdict_path
data
aux_data
                                  
includes
check
)
:
  
includes_list
=
[
]
  
if
includes
!
=
None
:
    
includes_list
.
extend
(
includes
)
  
if
'
includes
'
in
subdict
:
    
for
include
in
subdict
[
'
includes
'
]
:
      
relative_include
=
\
          
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
os
.
path
.
dirname
(
subdict_path
)
include
)
)
      
includes_list
.
append
(
relative_include
)
    
del
subdict
[
'
includes
'
]
  
for
include
in
includes_list
:
    
if
not
'
included
'
in
aux_data
[
subdict_path
]
:
      
aux_data
[
subdict_path
]
[
'
included
'
]
=
[
]
    
aux_data
[
subdict_path
]
[
'
included
'
]
.
append
(
include
)
    
gyp
.
DebugOutput
(
gyp
.
DEBUG_INCLUDES
"
Loading
Included
File
:
'
%
s
'
"
include
)
    
MergeDicts
(
subdict
               
LoadOneBuildFile
(
include
data
aux_data
None
False
check
)
               
subdict_path
include
)
  
for
k
v
in
subdict
.
iteritems
(
)
:
    
if
type
(
v
)
is
dict
:
      
LoadBuildFileIncludesIntoDict
(
v
subdict_path
data
aux_data
                                    
None
check
)
    
elif
type
(
v
)
is
list
:
      
LoadBuildFileIncludesIntoList
(
v
subdict_path
data
aux_data
                                    
check
)
def
LoadBuildFileIncludesIntoList
(
sublist
sublist_path
data
aux_data
check
)
:
  
for
item
in
sublist
:
    
if
type
(
item
)
is
dict
:
      
LoadBuildFileIncludesIntoDict
(
item
sublist_path
data
aux_data
                                    
None
check
)
    
elif
type
(
item
)
is
list
:
      
LoadBuildFileIncludesIntoList
(
item
sublist_path
data
aux_data
check
)
def
ProcessToolsetsInDict
(
data
)
:
  
if
'
targets
'
in
data
:
    
target_list
=
data
[
'
targets
'
]
    
new_target_list
=
[
]
    
for
target
in
target_list
:
      
if
'
toolset
'
in
target
and
'
toolsets
'
not
in
target
:
        
new_target_list
.
append
(
target
)
        
continue
      
if
multiple_toolsets
:
        
toolsets
=
target
.
get
(
'
toolsets
'
[
'
target
'
]
)
      
else
:
        
toolsets
=
[
'
target
'
]
      
if
'
toolsets
'
in
target
:
        
del
target
[
'
toolsets
'
]
      
if
len
(
toolsets
)
>
0
:
        
for
build
in
toolsets
[
1
:
]
:
          
new_target
=
gyp
.
simple_copy
.
deepcopy
(
target
)
          
new_target
[
'
toolset
'
]
=
build
          
new_target_list
.
append
(
new_target
)
        
target
[
'
toolset
'
]
=
toolsets
[
0
]
        
new_target_list
.
append
(
target
)
    
data
[
'
targets
'
]
=
new_target_list
  
if
'
conditions
'
in
data
:
    
for
condition
in
data
[
'
conditions
'
]
:
      
if
type
(
condition
)
is
list
:
        
for
condition_dict
in
condition
[
1
:
]
:
          
if
type
(
condition_dict
)
is
dict
:
            
ProcessToolsetsInDict
(
condition_dict
)
def
LoadTargetBuildFile
(
build_file_path
data
aux_data
variables
includes
                        
depth
check
load_dependencies
)
:
  
if
depth
:
    
d
=
gyp
.
common
.
RelativePath
(
depth
os
.
path
.
dirname
(
build_file_path
)
)
    
if
d
=
=
'
'
:
      
variables
[
'
DEPTH
'
]
=
'
.
'
    
else
:
      
variables
[
'
DEPTH
'
]
=
d
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
  
if
'
target_build_files
'
in
data
:
    
if
build_file_path
in
data
[
'
target_build_files
'
]
:
      
return
False
    
data
[
'
target_build_files
'
]
.
add
(
build_file_path
)
  
gyp
.
DebugOutput
(
gyp
.
DEBUG_INCLUDES
                  
"
Loading
Target
Build
File
'
%
s
'
"
build_file_path
)
  
build_file_data
=
LoadOneBuildFile
(
build_file_path
data
aux_data
                                     
includes
True
check
)
  
build_file_data
[
'
_DEPTH
'
]
=
depth
  
if
'
included_files
'
in
build_file_data
:
    
raise
GypError
(
build_file_path
+
'
must
not
contain
included_files
key
'
)
  
included
=
GetIncludedBuildFiles
(
build_file_path
aux_data
)
  
build_file_data
[
'
included_files
'
]
=
[
]
  
for
included_file
in
included
:
    
included_relative
=
\
        
gyp
.
common
.
RelativePath
(
included_file
                                
os
.
path
.
dirname
(
build_file_path
)
)
    
build_file_data
[
'
included_files
'
]
.
append
(
included_relative
)
  
ProcessToolsetsInDict
(
build_file_data
)
  
ProcessVariablesAndConditionsInDict
(
      
build_file_data
PHASE_EARLY
variables
build_file_path
)
  
ProcessToolsetsInDict
(
build_file_data
)
  
if
'
target_defaults
'
in
build_file_data
:
    
if
'
targets
'
not
in
build_file_data
:
      
raise
GypError
(
"
Unable
to
find
targets
in
build
file
%
s
"
%
                     
build_file_path
)
    
index
=
0
    
while
index
<
len
(
build_file_data
[
'
targets
'
]
)
:
      
old_target_dict
=
build_file_data
[
'
targets
'
]
[
index
]
      
new_target_dict
=
gyp
.
simple_copy
.
deepcopy
(
        
build_file_data
[
'
target_defaults
'
]
)
      
MergeDicts
(
new_target_dict
old_target_dict
                 
build_file_path
build_file_path
)
      
build_file_data
[
'
targets
'
]
[
index
]
=
new_target_dict
      
index
+
=
1
    
del
build_file_data
[
'
target_defaults
'
]
  
dependencies
=
[
]
  
if
'
targets
'
in
build_file_data
:
    
for
target_dict
in
build_file_data
[
'
targets
'
]
:
      
if
'
dependencies
'
not
in
target_dict
:
        
continue
      
for
dependency
in
target_dict
[
'
dependencies
'
]
:
        
dependencies
.
append
(
            
gyp
.
common
.
ResolveTarget
(
build_file_path
dependency
None
)
[
0
]
)
  
if
load_dependencies
:
    
for
dependency
in
dependencies
:
      
try
:
        
LoadTargetBuildFile
(
dependency
data
aux_data
variables
                            
includes
depth
check
load_dependencies
)
      
except
Exception
e
:
        
gyp
.
common
.
ExceptionAppend
(
          
e
'
while
loading
dependencies
of
%
s
'
%
build_file_path
)
        
raise
  
else
:
    
return
(
build_file_path
dependencies
)
def
CallLoadTargetBuildFile
(
global_flags
                            
build_file_path
variables
                            
includes
depth
check
                            
generator_input_info
)
:
  
"
"
"
Wrapper
around
LoadTargetBuildFile
for
parallel
processing
.
     
This
wrapper
is
used
when
LoadTargetBuildFile
is
executed
in
     
a
worker
process
.
  
"
"
"
  
try
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
    
for
key
value
in
global_flags
.
iteritems
(
)
:
      
globals
(
)
[
key
]
=
value
    
SetGeneratorGlobals
(
generator_input_info
)
    
result
=
LoadTargetBuildFile
(
build_file_path
per_process_data
                                 
per_process_aux_data
variables
                                 
includes
depth
check
False
)
    
if
not
result
:
      
return
result
    
(
build_file_path
dependencies
)
=
result
    
build_file_data
=
per_process_data
.
pop
(
build_file_path
)
    
return
(
build_file_path
            
build_file_data
            
dependencies
)
  
except
GypError
e
:
    
sys
.
stderr
.
write
(
"
gyp
:
%
s
\
n
"
%
e
)
    
return
None
  
except
Exception
e
:
    
print
>
>
sys
.
stderr
'
Exception
:
'
e
    
print
>
>
sys
.
stderr
traceback
.
format_exc
(
)
    
return
None
class
ParallelProcessingError
(
Exception
)
:
  
pass
class
ParallelState
(
object
)
:
  
"
"
"
Class
to
keep
track
of
state
when
processing
input
files
in
parallel
.
  
If
build
files
are
loaded
in
parallel
use
this
to
keep
track
of
  
state
during
farming
out
and
processing
parallel
jobs
.
It
'
s
stored
  
in
a
global
so
that
the
callback
function
can
have
access
to
it
.
  
"
"
"
  
def
__init__
(
self
)
:
    
self
.
pool
=
None
    
self
.
condition
=
None
    
self
.
data
=
None
    
self
.
pending
=
0
    
self
.
scheduled
=
set
(
)
    
self
.
dependencies
=
[
]
    
self
.
error
=
False
  
def
LoadTargetBuildFileCallback
(
self
result
)
:
    
"
"
"
Handle
the
results
of
running
LoadTargetBuildFile
in
another
process
.
    
"
"
"
    
self
.
condition
.
acquire
(
)
    
if
not
result
:
      
self
.
error
=
True
      
self
.
condition
.
notify
(
)
      
self
.
condition
.
release
(
)
      
return
    
(
build_file_path0
build_file_data0
dependencies0
)
=
result
    
self
.
data
[
build_file_path0
]
=
build_file_data0
    
self
.
data
[
'
target_build_files
'
]
.
add
(
build_file_path0
)
    
for
new_dependency
in
dependencies0
:
      
if
new_dependency
not
in
self
.
scheduled
:
        
self
.
scheduled
.
add
(
new_dependency
)
        
self
.
dependencies
.
append
(
new_dependency
)
    
self
.
pending
-
=
1
    
self
.
condition
.
notify
(
)
    
self
.
condition
.
release
(
)
def
LoadTargetBuildFilesParallel
(
build_files
data
variables
includes
depth
                                 
check
generator_input_info
)
:
  
parallel_state
=
ParallelState
(
)
  
parallel_state
.
condition
=
threading
.
Condition
(
)
  
parallel_state
.
dependencies
=
list
(
build_files
)
  
parallel_state
.
scheduled
=
set
(
build_files
)
  
parallel_state
.
pending
=
0
  
parallel_state
.
data
=
data
  
try
:
    
parallel_state
.
condition
.
acquire
(
)
    
while
parallel_state
.
dependencies
or
parallel_state
.
pending
:
      
if
parallel_state
.
error
:
        
break
      
if
not
parallel_state
.
dependencies
:
        
parallel_state
.
condition
.
wait
(
)
        
continue
      
dependency
=
parallel_state
.
dependencies
.
pop
(
)
      
parallel_state
.
pending
+
=
1
      
global_flags
=
{
        
'
path_sections
'
:
globals
(
)
[
'
path_sections
'
]
        
'
non_configuration_keys
'
:
globals
(
)
[
'
non_configuration_keys
'
]
        
'
multiple_toolsets
'
:
globals
(
)
[
'
multiple_toolsets
'
]
}
      
if
not
parallel_state
.
pool
:
        
parallel_state
.
pool
=
multiprocessing
.
Pool
(
multiprocessing
.
cpu_count
(
)
)
      
parallel_state
.
pool
.
apply_async
(
          
CallLoadTargetBuildFile
          
args
=
(
global_flags
dependency
                  
variables
includes
depth
check
generator_input_info
)
          
callback
=
parallel_state
.
LoadTargetBuildFileCallback
)
  
except
KeyboardInterrupt
e
:
    
parallel_state
.
pool
.
terminate
(
)
    
raise
e
  
parallel_state
.
condition
.
release
(
)
  
parallel_state
.
pool
.
close
(
)
  
parallel_state
.
pool
.
join
(
)
  
parallel_state
.
pool
=
None
  
if
parallel_state
.
error
:
    
sys
.
exit
(
1
)
LBRACKETS
=
set
(
'
{
[
(
'
)
BRACKETS
=
{
'
}
'
:
'
{
'
'
]
'
:
'
[
'
'
)
'
:
'
(
'
}
def
FindEnclosingBracketGroup
(
input_str
)
:
  
stack
=
[
]
  
start
=
-
1
  
for
index
char
in
enumerate
(
input_str
)
:
    
if
char
in
LBRACKETS
:
      
stack
.
append
(
char
)
      
if
start
=
=
-
1
:
        
start
=
index
    
elif
char
in
BRACKETS
:
      
if
not
stack
:
        
return
(
-
1
-
1
)
      
if
stack
.
pop
(
)
!
=
BRACKETS
[
char
]
:
        
return
(
-
1
-
1
)
      
if
not
stack
:
        
return
(
start
index
+
1
)
  
return
(
-
1
-
1
)
def
IsStrCanonicalInt
(
string
)
:
  
"
"
"
Returns
True
if
|
string
|
is
in
its
canonical
integer
form
.
  
The
canonical
form
is
such
that
str
(
int
(
string
)
)
=
=
string
.
  
"
"
"
  
if
type
(
string
)
is
str
:
    
if
string
:
      
if
string
=
=
"
0
"
:
        
return
True
      
if
string
[
0
]
=
=
"
-
"
:
        
string
=
string
[
1
:
]
        
if
not
string
:
          
return
False
      
if
'
1
'
<
=
string
[
0
]
<
=
'
9
'
:
        
return
string
.
isdigit
(
)
  
return
False
early_variable_re
=
re
.
compile
(
    
r
'
(
?
P
<
replace
>
(
?
P
<
type
>
<
(
?
:
(
?
:
!
?
?
)
|
\
|
)
?
)
'
    
r
'
(
?
P
<
command_string
>
[
-
a
-
zA
-
Z0
-
9_
.
]
+
)
?
'
    
r
'
\
(
(
?
P
<
is_array
>
\
s
*
\
[
?
)
'
    
r
'
(
?
P
<
content
>
.
*
?
)
(
\
]
?
)
\
)
)
'
)
late_variable_re
=
re
.
compile
(
    
r
'
(
?
P
<
replace
>
(
?
P
<
type
>
>
(
?
:
(
?
:
!
?
?
)
|
\
|
)
?
)
'
    
r
'
(
?
P
<
command_string
>
[
-
a
-
zA
-
Z0
-
9_
.
]
+
)
?
'
    
r
'
\
(
(
?
P
<
is_array
>
\
s
*
\
[
?
)
'
    
r
'
(
?
P
<
content
>
.
*
?
)
(
\
]
?
)
\
)
)
'
)
latelate_variable_re
=
re
.
compile
(
    
r
'
(
?
P
<
replace
>
(
?
P
<
type
>
[
\
^
]
(
?
:
(
?
:
!
?
?
)
|
\
|
)
?
)
'
    
r
'
(
?
P
<
command_string
>
[
-
a
-
zA
-
Z0
-
9_
.
]
+
)
?
'
    
r
'
\
(
(
?
P
<
is_array
>
\
s
*
\
[
?
)
'
    
r
'
(
?
P
<
content
>
.
*
?
)
(
\
]
?
)
\
)
)
'
)
cached_command_results
=
{
}
def
FixupPlatformCommand
(
cmd
)
:
  
if
sys
.
platform
=
=
'
win32
'
:
    
if
type
(
cmd
)
is
list
:
      
cmd
=
[
re
.
sub
(
'
^
cat
'
'
type
'
cmd
[
0
]
)
]
+
cmd
[
1
:
]
    
else
:
      
cmd
=
re
.
sub
(
'
^
cat
'
'
type
'
cmd
)
  
return
cmd
PHASE_EARLY
=
0
PHASE_LATE
=
1
PHASE_LATELATE
=
2
def
ExpandVariables
(
input
phase
variables
build_file
)
:
  
if
phase
=
=
PHASE_EARLY
:
    
variable_re
=
early_variable_re
    
expansion_symbol
=
'
<
'
  
elif
phase
=
=
PHASE_LATE
:
    
variable_re
=
late_variable_re
    
expansion_symbol
=
'
>
'
  
elif
phase
=
=
PHASE_LATELATE
:
    
variable_re
=
latelate_variable_re
    
expansion_symbol
=
'
^
'
  
else
:
    
assert
False
  
input_str
=
str
(
input
)
  
if
IsStrCanonicalInt
(
input_str
)
:
    
return
int
(
input_str
)
  
if
expansion_symbol
not
in
input_str
:
    
return
input_str
  
matches
=
list
(
variable_re
.
finditer
(
input_str
)
)
  
if
not
matches
:
    
return
input_str
  
output
=
input_str
  
matches
.
reverse
(
)
  
for
match_group
in
matches
:
    
match
=
match_group
.
groupdict
(
)
    
gyp
.
DebugOutput
(
gyp
.
DEBUG_VARIABLES
"
Matches
:
%
r
"
match
)
    
run_command
=
'
!
'
in
match
[
'
type
'
]
    
command_string
=
match
[
'
command_string
'
]
    
file_list
=
'
|
'
in
match
[
'
type
'
]
    
replace_start
=
match_group
.
start
(
'
replace
'
)
    
replace_end
=
match_group
.
end
(
'
replace
'
)
    
(
c_start
c_end
)
=
FindEnclosingBracketGroup
(
input_str
[
replace_start
:
]
)
    
replace_end
=
replace_start
+
c_end
    
replacement
=
input_str
[
replace_start
:
replace_end
]
    
contents_start
=
replace_start
+
c_start
+
1
    
contents_end
=
replace_end
-
1
    
contents
=
input_str
[
contents_start
:
contents_end
]
    
if
file_list
:
      
processed_variables
=
gyp
.
simple_copy
.
deepcopy
(
variables
)
      
ProcessListFiltersInDict
(
contents
processed_variables
)
      
contents
=
ExpandVariables
(
contents
phase
                                 
processed_variables
build_file
)
    
else
:
      
contents
=
ExpandVariables
(
contents
phase
variables
build_file
)
    
contents
=
contents
.
strip
(
)
    
expand_to_list
=
'
'
in
match
[
'
type
'
]
and
input_str
=
=
replacement
    
if
run_command
or
file_list
:
      
build_file_dir
=
os
.
path
.
dirname
(
build_file
)
      
if
build_file_dir
=
=
'
'
and
not
file_list
:
        
build_file_dir
=
None
    
if
file_list
:
      
if
type
(
contents
)
is
list
:
        
contents_list
=
contents
      
else
:
        
contents_list
=
contents
.
split
(
'
'
)
      
replacement
=
contents_list
[
0
]
      
if
os
.
path
.
isabs
(
replacement
)
:
        
raise
GypError
(
'
|
cannot
handle
absolute
paths
got
"
%
s
"
'
%
replacement
)
      
if
not
generator_filelist_paths
:
        
path
=
os
.
path
.
join
(
build_file_dir
replacement
)
      
else
:
        
if
os
.
path
.
isabs
(
build_file_dir
)
:
          
toplevel
=
generator_filelist_paths
[
'
toplevel
'
]
          
rel_build_file_dir
=
gyp
.
common
.
RelativePath
(
build_file_dir
toplevel
)
        
else
:
          
rel_build_file_dir
=
build_file_dir
        
qualified_out_dir
=
generator_filelist_paths
[
'
qualified_out_dir
'
]
        
path
=
os
.
path
.
join
(
qualified_out_dir
rel_build_file_dir
replacement
)
        
gyp
.
common
.
EnsureDirExists
(
path
)
      
replacement
=
gyp
.
common
.
RelativePath
(
path
build_file_dir
)
      
f
=
gyp
.
common
.
WriteOnDiff
(
path
)
      
for
i
in
contents_list
[
1
:
]
:
        
f
.
write
(
'
%
s
\
n
'
%
i
)
      
f
.
close
(
)
    
elif
run_command
:
      
use_shell
=
True
      
if
match
[
'
is_array
'
]
:
        
contents
=
eval
(
contents
)
        
use_shell
=
False
      
cache_key
=
(
str
(
contents
)
build_file_dir
)
      
cached_value
=
cached_command_results
.
get
(
cache_key
None
)
      
if
cached_value
is
None
:
        
gyp
.
DebugOutput
(
gyp
.
DEBUG_VARIABLES
                        
"
Executing
command
'
%
s
'
in
directory
'
%
s
'
"
                        
contents
build_file_dir
)
        
replacement
=
'
'
        
if
command_string
=
=
'
pymod_do_main
'
:
          
oldwd
=
os
.
getcwd
(
)
          
if
build_file_dir
:
            
os
.
chdir
(
build_file_dir
)
          
try
:
            
parsed_contents
=
shlex
.
split
(
contents
)
            
try
:
              
py_module
=
__import__
(
parsed_contents
[
0
]
)
            
except
ImportError
as
e
:
              
raise
GypError
(
"
Error
importing
pymod_do_main
"
                             
"
module
(
%
s
)
:
%
s
"
%
(
parsed_contents
[
0
]
e
)
)
            
replacement
=
str
(
py_module
.
DoMain
(
parsed_contents
[
1
:
]
)
)
.
rstrip
(
)
          
finally
:
            
os
.
chdir
(
oldwd
)
          
assert
replacement
!
=
None
        
elif
command_string
:
          
raise
GypError
(
"
Unknown
command
string
'
%
s
'
in
'
%
s
'
.
"
%
                         
(
command_string
contents
)
)
        
else
:
          
contents
=
FixupPlatformCommand
(
contents
)
          
try
:
            
p
=
subprocess
.
Popen
(
contents
shell
=
use_shell
                                 
stdout
=
subprocess
.
PIPE
                                 
stderr
=
subprocess
.
PIPE
                                 
stdin
=
subprocess
.
PIPE
                                 
cwd
=
build_file_dir
)
          
except
Exception
e
:
            
raise
GypError
(
"
%
s
while
executing
command
'
%
s
'
in
%
s
"
%
                           
(
e
contents
build_file
)
)
          
p_stdout
p_stderr
=
p
.
communicate
(
'
'
)
          
if
p
.
wait
(
)
!
=
0
or
p_stderr
:
            
sys
.
stderr
.
write
(
p_stderr
)
            
raise
GypError
(
"
Call
to
'
%
s
'
returned
exit
status
%
d
while
in
%
s
.
"
%
                           
(
contents
p
.
returncode
build_file
)
)
          
replacement
=
p_stdout
.
rstrip
(
)
        
cached_command_results
[
cache_key
]
=
replacement
      
else
:
        
gyp
.
DebugOutput
(
gyp
.
DEBUG_VARIABLES
                        
"
Had
cache
value
for
command
'
%
s
'
in
directory
'
%
s
'
"
                        
contents
build_file_dir
)
        
replacement
=
cached_value
    
else
:
      
if
not
contents
in
variables
:
        
if
contents
[
-
1
]
in
[
'
!
'
'
/
'
]
:
          
replacement
=
[
]
        
else
:
          
raise
GypError
(
'
Undefined
variable
'
+
contents
+
                         
'
in
'
+
build_file
)
      
else
:
        
replacement
=
variables
[
contents
]
    
if
type
(
replacement
)
is
list
:
      
for
item
in
replacement
:
        
if
not
contents
[
-
1
]
=
=
'
/
'
and
type
(
item
)
not
in
(
str
int
)
:
          
raise
GypError
(
'
Variable
'
+
contents
+
                         
'
must
expand
to
a
string
or
list
of
strings
;
'
+
                         
'
list
contains
a
'
+
                         
item
.
__class__
.
__name__
)
      
ProcessVariablesAndConditionsInList
(
replacement
phase
variables
                                          
build_file
)
    
elif
type
(
replacement
)
not
in
(
str
int
)
:
          
raise
GypError
(
'
Variable
'
+
contents
+
                         
'
must
expand
to
a
string
or
list
of
strings
;
'
+
                         
'
found
a
'
+
replacement
.
__class__
.
__name__
)
    
if
expand_to_list
:
      
if
type
(
replacement
)
is
list
:
        
output
=
replacement
[
:
]
      
else
:
        
output
=
shlex
.
split
(
str
(
replacement
)
)
    
else
:
      
encoded_replacement
=
'
'
      
if
type
(
replacement
)
is
list
:
        
encoded_replacement
=
gyp
.
common
.
EncodePOSIXShellList
(
replacement
)
      
else
:
        
encoded_replacement
=
replacement
      
output
=
output
[
:
replace_start
]
+
str
(
encoded_replacement
)
+
\
               
output
[
replace_end
:
]
    
input_str
=
output
  
if
output
=
=
input
:
    
gyp
.
DebugOutput
(
gyp
.
DEBUG_VARIABLES
                    
"
Found
only
identity
matches
on
%
r
avoiding
infinite
"
                    
"
recursion
.
"
                    
output
)
  
else
:
    
gyp
.
DebugOutput
(
gyp
.
DEBUG_VARIABLES
"
Found
output
%
r
recursing
.
"
output
)
    
if
type
(
output
)
is
list
:
      
if
output
and
type
(
output
[
0
]
)
is
list
:
        
pass
      
else
:
        
new_output
=
[
]
        
for
item
in
output
:
          
new_output
.
append
(
              
ExpandVariables
(
item
phase
variables
build_file
)
)
        
output
=
new_output
    
else
:
      
output
=
ExpandVariables
(
output
phase
variables
build_file
)
  
if
type
(
output
)
is
list
:
    
for
index
in
xrange
(
0
len
(
output
)
)
:
      
if
IsStrCanonicalInt
(
output
[
index
]
)
:
        
output
[
index
]
=
int
(
output
[
index
]
)
  
elif
IsStrCanonicalInt
(
output
)
:
    
output
=
int
(
output
)
  
return
output
cached_conditions_asts
=
{
}
def
EvalCondition
(
condition
conditions_key
phase
variables
build_file
)
:
  
"
"
"
Returns
the
dict
that
should
be
used
or
None
if
the
result
was
  
that
nothing
should
be
used
.
"
"
"
  
if
type
(
condition
)
is
not
list
:
    
raise
GypError
(
conditions_key
+
'
must
be
a
list
'
)
  
if
len
(
condition
)
<
2
:
    
raise
GypError
(
conditions_key
+
'
'
+
condition
[
0
]
+
                   
'
must
be
at
least
length
2
not
'
+
str
(
len
(
condition
)
)
)
  
i
=
0
  
result
=
None
  
while
i
<
len
(
condition
)
:
    
cond_expr
=
condition
[
i
]
    
true_dict
=
condition
[
i
+
1
]
    
if
type
(
true_dict
)
is
not
dict
:
      
raise
GypError
(
'
{
}
{
}
must
be
followed
by
a
dictionary
not
{
}
'
.
format
(
        
conditions_key
cond_expr
type
(
true_dict
)
)
)
    
if
len
(
condition
)
>
i
+
2
and
type
(
condition
[
i
+
2
]
)
is
dict
:
      
false_dict
=
condition
[
i
+
2
]
      
i
=
i
+
3
      
if
i
!
=
len
(
condition
)
:
        
raise
GypError
(
'
{
}
{
}
has
{
}
unexpected
trailing
items
'
.
format
(
          
conditions_key
cond_expr
len
(
condition
)
-
i
)
)
    
else
:
      
false_dict
=
None
      
i
=
i
+
2
    
if
result
=
=
None
:
      
result
=
EvalSingleCondition
(
          
cond_expr
true_dict
false_dict
phase
variables
build_file
)
  
return
result
def
EvalSingleCondition
(
    
cond_expr
true_dict
false_dict
phase
variables
build_file
)
:
  
"
"
"
Returns
true_dict
if
cond_expr
evaluates
to
true
and
false_dict
  
otherwise
.
"
"
"
  
cond_expr_expanded
=
ExpandVariables
(
cond_expr
phase
variables
                                       
build_file
)
  
if
type
(
cond_expr_expanded
)
not
in
(
str
int
)
:
    
raise
ValueError
(
          
'
Variable
expansion
in
this
context
permits
str
and
int
'
+
\
            
'
only
found
'
+
cond_expr_expanded
.
__class__
.
__name__
)
  
try
:
    
if
cond_expr_expanded
in
cached_conditions_asts
:
      
ast_code
=
cached_conditions_asts
[
cond_expr_expanded
]
    
else
:
      
ast_code
=
compile
(
cond_expr_expanded
'
<
string
>
'
'
eval
'
)
      
cached_conditions_asts
[
cond_expr_expanded
]
=
ast_code
    
if
eval
(
ast_code
{
'
__builtins__
'
:
None
}
variables
)
:
      
return
true_dict
    
return
false_dict
  
except
SyntaxError
e
:
    
syntax_error
=
SyntaxError
(
'
%
s
while
evaluating
condition
\
'
%
s
\
'
in
%
s
'
                               
'
at
character
%
d
.
'
%
                               
(
str
(
e
.
args
[
0
]
)
e
.
text
build_file
e
.
offset
)
                               
e
.
filename
e
.
lineno
e
.
offset
e
.
text
)
    
raise
syntax_error
  
except
NameError
e
:
    
gyp
.
common
.
ExceptionAppend
(
e
'
while
evaluating
condition
\
'
%
s
\
'
in
%
s
'
%
                               
(
cond_expr_expanded
build_file
)
)
    
raise
GypError
(
e
)
def
ProcessConditionsInDict
(
the_dict
phase
variables
build_file
)
:
  
if
phase
=
=
PHASE_EARLY
:
    
conditions_key
=
'
conditions
'
  
elif
phase
=
=
PHASE_LATE
:
    
conditions_key
=
'
target_conditions
'
  
elif
phase
=
=
PHASE_LATELATE
:
    
return
  
else
:
    
assert
False
  
if
not
conditions_key
in
the_dict
:
    
return
  
conditions_list
=
the_dict
[
conditions_key
]
  
del
the_dict
[
conditions_key
]
  
for
condition
in
conditions_list
:
    
merge_dict
=
EvalCondition
(
condition
conditions_key
phase
variables
                               
build_file
)
    
if
merge_dict
!
=
None
:
      
ProcessVariablesAndConditionsInDict
(
merge_dict
phase
                                          
variables
build_file
)
      
MergeDicts
(
the_dict
merge_dict
build_file
build_file
)
def
LoadAutomaticVariablesFromDict
(
variables
the_dict
)
:
  
for
key
value
in
the_dict
.
iteritems
(
)
:
    
if
type
(
value
)
in
(
str
int
list
)
:
      
variables
[
'
_
'
+
key
]
=
value
def
LoadVariablesFromVariablesDict
(
variables
the_dict
the_dict_key
)
:
  
for
key
value
in
the_dict
.
get
(
'
variables
'
{
}
)
.
iteritems
(
)
:
    
if
type
(
value
)
not
in
(
str
int
list
)
:
      
continue
    
if
key
.
endswith
(
'
%
'
)
:
      
variable_name
=
key
[
:
-
1
]
      
if
variable_name
in
variables
:
        
continue
      
if
the_dict_key
is
'
variables
'
and
variable_name
in
the_dict
:
        
value
=
the_dict
[
variable_name
]
    
else
:
      
variable_name
=
key
    
variables
[
variable_name
]
=
value
def
ProcessVariablesAndConditionsInDict
(
the_dict
phase
variables_in
                                        
build_file
the_dict_key
=
None
)
:
  
"
"
"
Handle
all
variable
and
command
expansion
and
conditional
evaluation
.
  
This
function
is
the
public
entry
point
for
all
variable
expansions
and
  
conditional
evaluations
.
The
variables_in
dictionary
will
not
be
modified
  
by
this
function
.
  
"
"
"
  
variables
=
variables_in
.
copy
(
)
  
LoadAutomaticVariablesFromDict
(
variables
the_dict
)
  
if
'
variables
'
in
the_dict
:
    
for
key
value
in
the_dict
[
'
variables
'
]
.
iteritems
(
)
:
      
variables
[
key
]
=
value
    
ProcessVariablesAndConditionsInDict
(
the_dict
[
'
variables
'
]
phase
                                        
variables
build_file
'
variables
'
)
  
LoadVariablesFromVariablesDict
(
variables
the_dict
the_dict_key
)
  
for
key
value
in
the_dict
.
iteritems
(
)
:
    
if
key
!
=
'
variables
'
and
type
(
value
)
is
str
:
      
expanded
=
ExpandVariables
(
value
phase
variables
build_file
)
      
if
type
(
expanded
)
not
in
(
str
int
)
:
        
raise
ValueError
(
              
'
Variable
expansion
in
this
context
permits
str
and
int
'
+
\
              
'
only
found
'
+
expanded
.
__class__
.
__name__
+
'
for
'
+
key
)
      
the_dict
[
key
]
=
expanded
  
variables
=
variables_in
.
copy
(
)
  
LoadAutomaticVariablesFromDict
(
variables
the_dict
)
  
LoadVariablesFromVariablesDict
(
variables
the_dict
the_dict_key
)
  
ProcessConditionsInDict
(
the_dict
phase
variables
build_file
)
  
variables
=
variables_in
.
copy
(
)
  
LoadAutomaticVariablesFromDict
(
variables
the_dict
)
  
LoadVariablesFromVariablesDict
(
variables
the_dict
the_dict_key
)
  
for
key
value
in
the_dict
.
iteritems
(
)
:
    
if
key
=
=
'
variables
'
or
type
(
value
)
is
str
:
      
continue
    
if
type
(
value
)
is
dict
:
      
ProcessVariablesAndConditionsInDict
(
value
phase
variables
                                          
build_file
key
)
    
elif
type
(
value
)
is
list
:
      
ProcessVariablesAndConditionsInList
(
value
phase
variables
                                          
build_file
)
    
elif
type
(
value
)
is
not
int
:
      
raise
TypeError
(
'
Unknown
type
'
+
value
.
__class__
.
__name__
+
\
                      
'
for
'
+
key
)
def
ProcessVariablesAndConditionsInList
(
the_list
phase
variables
                                        
build_file
)
:
  
index
=
0
  
while
index
<
len
(
the_list
)
:
    
item
=
the_list
[
index
]
    
if
type
(
item
)
is
dict
:
      
ProcessVariablesAndConditionsInDict
(
item
phase
variables
build_file
)
    
elif
type
(
item
)
is
list
:
      
ProcessVariablesAndConditionsInList
(
item
phase
variables
build_file
)
    
elif
type
(
item
)
is
str
:
      
expanded
=
ExpandVariables
(
item
phase
variables
build_file
)
      
if
type
(
expanded
)
in
(
str
int
)
:
        
the_list
[
index
]
=
expanded
      
elif
type
(
expanded
)
is
list
:
        
the_list
[
index
:
index
+
1
]
=
expanded
        
index
+
=
len
(
expanded
)
        
continue
      
else
:
        
raise
ValueError
(
              
'
Variable
expansion
in
this
context
permits
strings
and
'
+
\
              
'
lists
only
found
'
+
expanded
.
__class__
.
__name__
+
'
at
'
+
\
              
index
)
    
elif
type
(
item
)
is
not
int
:
      
raise
TypeError
(
'
Unknown
type
'
+
item
.
__class__
.
__name__
+
\
                      
'
at
index
'
+
index
)
    
index
=
index
+
1
def
BuildTargetsDict
(
data
)
:
  
"
"
"
Builds
a
dict
mapping
fully
-
qualified
target
names
to
their
target
dicts
.
  
|
data
|
is
a
dict
mapping
loaded
build
files
by
pathname
relative
to
the
  
current
directory
.
Values
in
|
data
|
are
build
file
contents
.
For
each
  
|
data
|
value
with
a
"
targets
"
key
the
value
of
the
"
targets
"
key
is
taken
  
as
a
list
containing
target
dicts
.
Each
target
'
s
fully
-
qualified
name
is
  
constructed
from
the
pathname
of
the
build
file
(
|
data
|
key
)
and
its
  
"
target_name
"
property
.
These
fully
-
qualified
names
are
used
as
the
keys
  
in
the
returned
dict
.
These
keys
provide
access
to
the
target
dicts
  
the
dicts
in
the
"
targets
"
lists
.
  
"
"
"
  
targets
=
{
}
  
for
build_file
in
data
[
'
target_build_files
'
]
:
    
for
target
in
data
[
build_file
]
.
get
(
'
targets
'
[
]
)
:
      
target_name
=
gyp
.
common
.
QualifiedTarget
(
build_file
                                               
target
[
'
target_name
'
]
                                               
target
[
'
toolset
'
]
)
      
if
target_name
in
targets
:
        
raise
GypError
(
'
Duplicate
target
definitions
for
'
+
target_name
)
      
targets
[
target_name
]
=
target
  
return
targets
def
QualifyDependencies
(
targets
)
:
  
"
"
"
Make
dependency
links
fully
-
qualified
relative
to
the
current
directory
.
  
|
targets
|
is
a
dict
mapping
fully
-
qualified
target
names
to
their
target
  
dicts
.
For
each
target
in
this
dict
keys
known
to
contain
dependency
  
links
are
examined
and
any
dependencies
referenced
will
be
rewritten
  
so
that
they
are
fully
-
qualified
and
relative
to
the
current
directory
.
  
All
rewritten
dependencies
are
suitable
for
use
as
keys
to
|
targets
|
or
a
  
similar
dict
.
  
"
"
"
  
all_dependency_sections
=
[
dep
+
op
                             
for
dep
in
dependency_sections
                             
for
op
in
(
'
'
'
!
'
'
/
'
)
]
  
for
target
target_dict
in
targets
.
iteritems
(
)
:
    
target_build_file
=
gyp
.
common
.
BuildFile
(
target
)
    
toolset
=
target_dict
[
'
toolset
'
]
    
for
dependency_key
in
all_dependency_sections
:
      
dependencies
=
target_dict
.
get
(
dependency_key
[
]
)
      
for
index
in
xrange
(
0
len
(
dependencies
)
)
:
        
dep_file
dep_target
dep_toolset
=
gyp
.
common
.
ResolveTarget
(
            
target_build_file
dependencies
[
index
]
toolset
)
        
if
not
multiple_toolsets
:
          
dep_toolset
=
toolset
        
dependency
=
gyp
.
common
.
QualifiedTarget
(
dep_file
                                                
dep_target
                                                
dep_toolset
)
        
dependencies
[
index
]
=
dependency
        
if
dependency_key
!
=
'
dependencies
'
and
\
           
dependency
not
in
target_dict
[
'
dependencies
'
]
:
          
raise
GypError
(
'
Found
'
+
dependency
+
'
in
'
+
dependency_key
+
                         
'
of
'
+
target
+
'
but
not
in
dependencies
'
)
def
ExpandWildcardDependencies
(
targets
data
)
:
  
"
"
"
Expands
dependencies
specified
as
build_file
:
*
.
  
For
each
target
in
|
targets
|
examines
sections
containing
links
to
other
  
targets
.
If
any
such
section
contains
a
link
of
the
form
build_file
:
*
it
  
is
taken
as
a
wildcard
link
and
is
expanded
to
list
each
target
in
  
build_file
.
The
|
data
|
dict
provides
access
to
build
file
dicts
.
  
Any
target
that
does
not
wish
to
be
included
by
wildcard
can
provide
an
  
optional
"
suppress_wildcard
"
key
in
its
target
dict
.
When
present
and
  
true
a
wildcard
dependency
link
will
not
include
such
targets
.
  
All
dependency
names
including
the
keys
to
|
targets
|
and
the
values
in
each
  
dependency
list
must
be
qualified
when
this
function
is
called
.
  
"
"
"
  
for
target
target_dict
in
targets
.
iteritems
(
)
:
    
toolset
=
target_dict
[
'
toolset
'
]
    
target_build_file
=
gyp
.
common
.
BuildFile
(
target
)
    
for
dependency_key
in
dependency_sections
:
      
dependencies
=
target_dict
.
get
(
dependency_key
[
]
)
      
index
=
0
      
while
index
<
len
(
dependencies
)
:
        
(
dependency_build_file
dependency_target
dependency_toolset
)
=
\
            
gyp
.
common
.
ParseQualifiedTarget
(
dependencies
[
index
]
)
        
if
dependency_target
!
=
'
*
'
and
dependency_toolset
!
=
'
*
'
:
          
index
=
index
+
1
          
continue
        
if
dependency_build_file
=
=
target_build_file
:
          
raise
GypError
(
'
Found
wildcard
in
'
+
dependency_key
+
'
of
'
+
                         
target
+
'
referring
to
same
build
file
'
)
        
del
dependencies
[
index
]
        
index
=
index
-
1
        
dependency_target_dicts
=
data
[
dependency_build_file
]
[
'
targets
'
]
        
for
dependency_target_dict
in
dependency_target_dicts
:
          
if
int
(
dependency_target_dict
.
get
(
'
suppress_wildcard
'
False
)
)
:
            
continue
          
dependency_target_name
=
dependency_target_dict
[
'
target_name
'
]
          
if
(
dependency_target
!
=
'
*
'
and
              
dependency_target
!
=
dependency_target_name
)
:
            
continue
          
dependency_target_toolset
=
dependency_target_dict
[
'
toolset
'
]
          
if
(
dependency_toolset
!
=
'
*
'
and
              
dependency_toolset
!
=
dependency_target_toolset
)
:
            
continue
          
dependency
=
gyp
.
common
.
QualifiedTarget
(
dependency_build_file
                                                  
dependency_target_name
                                                  
dependency_target_toolset
)
          
index
=
index
+
1
          
dependencies
.
insert
(
index
dependency
)
        
index
=
index
+
1
def
Unify
(
l
)
:
  
"
"
"
Removes
duplicate
elements
from
l
keeping
the
first
element
.
"
"
"
  
seen
=
{
}
  
return
[
seen
.
setdefault
(
e
e
)
for
e
in
l
if
e
not
in
seen
]
def
RemoveDuplicateDependencies
(
targets
)
:
  
"
"
"
Makes
sure
every
dependency
appears
only
once
in
all
targets
'
s
dependency
  
lists
.
"
"
"
  
for
target_name
target_dict
in
targets
.
iteritems
(
)
:
    
for
dependency_key
in
dependency_sections
:
      
dependencies
=
target_dict
.
get
(
dependency_key
[
]
)
      
if
dependencies
:
        
target_dict
[
dependency_key
]
=
Unify
(
dependencies
)
def
Filter
(
l
item
)
:
  
"
"
"
Removes
item
from
l
.
"
"
"
  
res
=
{
}
  
return
[
res
.
setdefault
(
e
e
)
for
e
in
l
if
e
!
=
item
]
def
RemoveSelfDependencies
(
targets
)
:
  
"
"
"
Remove
self
dependencies
from
targets
that
have
the
prune_self_dependency
  
variable
set
.
"
"
"
  
for
target_name
target_dict
in
targets
.
iteritems
(
)
:
    
for
dependency_key
in
dependency_sections
:
      
dependencies
=
target_dict
.
get
(
dependency_key
[
]
)
      
if
dependencies
:
        
for
t
in
dependencies
:
          
if
t
=
=
target_name
:
            
if
targets
[
t
]
.
get
(
'
variables
'
{
}
)
.
get
(
'
prune_self_dependency
'
0
)
:
              
target_dict
[
dependency_key
]
=
Filter
(
dependencies
target_name
)
def
RemoveLinkDependenciesFromNoneTargets
(
targets
)
:
  
"
"
"
Remove
dependencies
having
the
'
link_dependency
'
attribute
from
the
'
none
'
  
targets
.
"
"
"
  
for
target_name
target_dict
in
targets
.
iteritems
(
)
:
    
for
dependency_key
in
dependency_sections
:
      
dependencies
=
target_dict
.
get
(
dependency_key
[
]
)
      
if
dependencies
:
        
for
t
in
dependencies
:
          
if
target_dict
.
get
(
'
type
'
None
)
=
=
'
none
'
:
            
if
targets
[
t
]
.
get
(
'
variables
'
{
}
)
.
get
(
'
link_dependency
'
0
)
:
              
target_dict
[
dependency_key
]
=
\
                  
Filter
(
target_dict
[
dependency_key
]
t
)
class
DependencyGraphNode
(
object
)
:
  
"
"
"
  
Attributes
:
    
ref
:
A
reference
to
an
object
that
this
DependencyGraphNode
represents
.
    
dependencies
:
List
of
DependencyGraphNodes
on
which
this
one
depends
.
    
dependents
:
List
of
DependencyGraphNodes
that
depend
on
this
one
.
  
"
"
"
  
class
CircularException
(
GypError
)
:
    
pass
  
def
__init__
(
self
ref
)
:
    
self
.
ref
=
ref
    
self
.
dependencies
=
[
]
    
self
.
dependents
=
[
]
  
def
__repr__
(
self
)
:
    
return
'
<
DependencyGraphNode
:
%
r
>
'
%
self
.
ref
  
def
FlattenToList
(
self
)
:
    
flat_list
=
OrderedSet
(
)
    
def
ExtractNodeRef
(
node
)
:
      
"
"
"
Extracts
the
object
that
the
node
represents
from
the
given
node
.
"
"
"
      
return
node
.
ref
    
in_degree_zeros
=
sorted
(
self
.
dependents
[
:
]
key
=
ExtractNodeRef
)
    
while
in_degree_zeros
:
      
node
=
in_degree_zeros
.
pop
(
)
      
flat_list
.
add
(
node
.
ref
)
      
for
node_dependent
in
sorted
(
node
.
dependents
key
=
ExtractNodeRef
)
:
        
is_in_degree_zero
=
True
        
for
node_dependent_dependency
in
(
sorted
(
node_dependent
.
dependencies
                                                 
key
=
ExtractNodeRef
)
)
:
          
if
not
node_dependent_dependency
.
ref
in
flat_list
:
            
is_in_degree_zero
=
False
            
break
        
if
is_in_degree_zero
:
          
in_degree_zeros
+
=
[
node_dependent
]
    
return
list
(
flat_list
)
  
def
FindCycles
(
self
)
:
    
"
"
"
    
Returns
a
list
of
cycles
in
the
graph
where
each
cycle
is
its
own
list
.
    
"
"
"
    
results
=
[
]
    
visited
=
set
(
)
    
def
Visit
(
node
path
)
:
      
for
child
in
node
.
dependents
:
        
if
child
in
path
:
          
results
.
append
(
[
child
]
+
path
[
:
path
.
index
(
child
)
+
1
]
)
        
elif
not
child
in
visited
:
          
visited
.
add
(
child
)
          
Visit
(
child
[
child
]
+
path
)
    
visited
.
add
(
self
)
    
Visit
(
self
[
self
]
)
    
return
results
  
def
DirectDependencies
(
self
dependencies
=
None
)
:
    
"
"
"
Returns
a
list
of
just
direct
dependencies
.
"
"
"
    
if
dependencies
=
=
None
:
      
dependencies
=
[
]
    
for
dependency
in
self
.
dependencies
:
      
if
dependency
.
ref
!
=
None
and
dependency
.
ref
not
in
dependencies
:
        
dependencies
.
append
(
dependency
.
ref
)
    
return
dependencies
  
def
_AddImportedDependencies
(
self
targets
dependencies
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
direct
dependencies
adds
indirect
dependencies
that
    
other
dependencies
have
declared
to
export
their
settings
.
    
This
method
does
not
operate
on
self
.
Rather
it
operates
on
the
list
    
of
dependencies
in
the
|
dependencies
|
argument
.
For
each
dependency
in
    
that
list
if
any
declares
that
it
exports
the
settings
of
one
of
its
    
own
dependencies
those
dependencies
whose
settings
are
"
passed
through
"
    
are
added
to
the
list
.
As
new
items
are
added
to
the
list
they
too
will
    
be
processed
so
it
is
possible
to
import
settings
through
multiple
levels
    
of
dependencies
.
    
This
method
is
not
terribly
useful
on
its
own
it
depends
on
being
    
"
primed
"
with
a
list
of
direct
dependencies
such
as
one
provided
by
    
DirectDependencies
.
DirectAndImportedDependencies
is
intended
to
be
the
    
public
entry
point
.
    
"
"
"
    
if
dependencies
=
=
None
:
      
dependencies
=
[
]
    
index
=
0
    
while
index
<
len
(
dependencies
)
:
      
dependency
=
dependencies
[
index
]
      
dependency_dict
=
targets
[
dependency
]
      
add_index
=
1
      
for
imported_dependency
in
\
          
dependency_dict
.
get
(
'
export_dependent_settings
'
[
]
)
:
        
if
imported_dependency
not
in
dependencies
:
          
dependencies
.
insert
(
index
+
add_index
imported_dependency
)
          
add_index
=
add_index
+
1
      
index
=
index
+
1
    
return
dependencies
  
def
DirectAndImportedDependencies
(
self
targets
dependencies
=
None
)
:
    
"
"
"
Returns
a
list
of
a
target
'
s
direct
dependencies
and
all
indirect
    
dependencies
that
a
dependency
has
advertised
settings
should
be
exported
    
through
the
dependency
for
.
    
"
"
"
    
dependencies
=
self
.
DirectDependencies
(
dependencies
)
    
return
self
.
_AddImportedDependencies
(
targets
dependencies
)
  
def
DeepDependencies
(
self
dependencies
=
None
)
:
    
"
"
"
Returns
an
OrderedSet
of
all
of
a
target
'
s
dependencies
recursively
.
"
"
"
    
if
dependencies
is
None
:
      
dependencies
=
OrderedSet
(
)
    
for
dependency
in
self
.
dependencies
:
      
if
dependency
.
ref
is
None
:
        
continue
      
if
dependency
.
ref
not
in
dependencies
:
        
dependency
.
DeepDependencies
(
dependencies
)
        
dependencies
.
add
(
dependency
.
ref
)
    
return
dependencies
  
def
_LinkDependenciesInternal
(
self
targets
include_shared_libraries
                                
dependencies
=
None
initial
=
True
)
:
    
"
"
"
Returns
an
OrderedSet
of
dependency
targets
that
are
linked
    
into
this
target
.
    
This
function
has
a
split
personality
depending
on
the
setting
of
    
|
initial
|
.
Outside
callers
should
always
leave
|
initial
|
at
its
default
    
setting
.
    
When
adding
a
target
to
the
list
of
dependencies
this
function
will
    
recurse
into
itself
with
|
initial
|
set
to
False
to
collect
dependencies
    
that
are
linked
into
the
linkable
target
for
which
the
list
is
being
built
.
    
If
|
include_shared_libraries
|
is
False
the
resulting
dependencies
will
not
    
include
shared_library
targets
that
are
linked
into
this
target
.
    
"
"
"
    
if
dependencies
is
None
:
      
dependencies
=
OrderedSet
(
)
    
if
self
.
ref
is
None
:
      
return
dependencies
    
if
'
target_name
'
not
in
targets
[
self
.
ref
]
:
      
raise
GypError
(
"
Missing
'
target_name
'
field
in
target
.
"
)
    
if
'
type
'
not
in
targets
[
self
.
ref
]
:
      
raise
GypError
(
"
Missing
'
type
'
field
in
target
%
s
"
%
                     
targets
[
self
.
ref
]
[
'
target_name
'
]
)
    
target_type
=
targets
[
self
.
ref
]
[
'
type
'
]
    
is_linkable
=
target_type
in
linkable_types
    
if
initial
and
not
is_linkable
:
      
return
dependencies
    
if
(
target_type
=
=
'
none
'
and
        
not
targets
[
self
.
ref
]
.
get
(
'
dependencies_traverse
'
True
)
)
:
      
dependencies
.
add
(
self
.
ref
)
      
return
dependencies
    
if
not
initial
and
target_type
in
(
'
executable
'
'
loadable_module
'
                                       
'
mac_kernel_extension
'
                                       
'
windows_driver
'
)
:
      
return
dependencies
    
if
(
not
initial
and
target_type
=
=
'
shared_library
'
and
        
not
include_shared_libraries
)
:
      
return
dependencies
    
if
self
.
ref
not
in
dependencies
:
      
dependencies
.
add
(
self
.
ref
)
      
if
initial
or
not
is_linkable
:
        
for
dependency
in
self
.
dependencies
:
          
dependency
.
_LinkDependenciesInternal
(
targets
                                               
include_shared_libraries
                                               
dependencies
False
)
    
return
dependencies
  
def
DependenciesForLinkSettings
(
self
targets
)
:
    
"
"
"
    
Returns
a
list
of
dependency
targets
whose
link_settings
should
be
merged
    
into
this
target
.
    
"
"
"
    
include_shared_libraries
=
\
        
targets
[
self
.
ref
]
.
get
(
'
allow_sharedlib_linksettings_propagation
'
True
)
    
return
self
.
_LinkDependenciesInternal
(
targets
include_shared_libraries
)
  
def
DependenciesToLinkAgainst
(
self
targets
)
:
    
"
"
"
    
Returns
a
list
of
dependency
targets
that
are
linked
into
this
target
.
    
"
"
"
    
return
self
.
_LinkDependenciesInternal
(
targets
True
)
def
BuildDependencyList
(
targets
)
:
  
dependency_nodes
=
{
}
  
for
target
spec
in
targets
.
iteritems
(
)
:
    
if
target
not
in
dependency_nodes
:
      
dependency_nodes
[
target
]
=
DependencyGraphNode
(
target
)
  
root_node
=
DependencyGraphNode
(
None
)
  
for
target
spec
in
targets
.
iteritems
(
)
:
    
target_node
=
dependency_nodes
[
target
]
    
target_build_file
=
gyp
.
common
.
BuildFile
(
target
)
    
dependencies
=
spec
.
get
(
'
dependencies
'
)
    
if
not
dependencies
:
      
target_node
.
dependencies
=
[
root_node
]
      
root_node
.
dependents
.
append
(
target_node
)
    
else
:
      
for
dependency
in
dependencies
:
        
dependency_node
=
dependency_nodes
.
get
(
dependency
)
        
if
not
dependency_node
:
          
raise
GypError
(
"
Dependency
'
%
s
'
not
found
while
"
                         
"
trying
to
load
target
%
s
"
%
(
dependency
target
)
)
        
target_node
.
dependencies
.
append
(
dependency_node
)
        
dependency_node
.
dependents
.
append
(
target_node
)
  
flat_list
=
root_node
.
FlattenToList
(
)
  
if
len
(
flat_list
)
!
=
len
(
targets
)
:
    
if
not
root_node
.
dependents
:
      
target
=
targets
.
keys
(
)
[
0
]
      
target_node
=
dependency_nodes
[
target
]
      
target_node
.
dependencies
.
append
(
root_node
)
      
root_node
.
dependents
.
append
(
target_node
)
    
cycles
=
[
]
    
for
cycle
in
root_node
.
FindCycles
(
)
:
      
paths
=
[
node
.
ref
for
node
in
cycle
]
      
cycles
.
append
(
'
Cycle
:
%
s
'
%
'
-
>
'
.
join
(
paths
)
)
    
raise
DependencyGraphNode
.
CircularException
(
        
'
Cycles
in
dependency
graph
detected
:
\
n
'
+
'
\
n
'
.
join
(
cycles
)
)
  
return
[
dependency_nodes
flat_list
]
def
VerifyNoGYPFileCircularDependencies
(
targets
)
:
  
dependency_nodes
=
{
}
  
for
target
in
targets
.
iterkeys
(
)
:
    
build_file
=
gyp
.
common
.
BuildFile
(
target
)
    
if
not
build_file
in
dependency_nodes
:
      
dependency_nodes
[
build_file
]
=
DependencyGraphNode
(
build_file
)
  
for
target
spec
in
targets
.
iteritems
(
)
:
    
build_file
=
gyp
.
common
.
BuildFile
(
target
)
    
build_file_node
=
dependency_nodes
[
build_file
]
    
target_dependencies
=
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
    
for
dependency
in
target_dependencies
:
      
try
:
        
dependency_build_file
=
gyp
.
common
.
BuildFile
(
dependency
)
      
except
GypError
e
:
        
gyp
.
common
.
ExceptionAppend
(
            
e
'
while
computing
dependencies
of
.
gyp
file
%
s
'
%
build_file
)
        
raise
      
if
dependency_build_file
=
=
build_file
:
        
continue
      
dependency_node
=
dependency_nodes
.
get
(
dependency_build_file
)
      
if
not
dependency_node
:
        
raise
GypError
(
"
Dependancy
'
%
s
'
not
found
"
%
dependency_build_file
)
      
if
dependency_node
not
in
build_file_node
.
dependencies
:
        
build_file_node
.
dependencies
.
append
(
dependency_node
)
        
dependency_node
.
dependents
.
append
(
build_file_node
)
  
root_node
=
DependencyGraphNode
(
None
)
  
for
build_file_node
in
dependency_nodes
.
itervalues
(
)
:
    
if
len
(
build_file_node
.
dependencies
)
=
=
0
:
      
build_file_node
.
dependencies
.
append
(
root_node
)
      
root_node
.
dependents
.
append
(
build_file_node
)
  
flat_list
=
root_node
.
FlattenToList
(
)
  
if
len
(
flat_list
)
!
=
len
(
dependency_nodes
)
:
    
if
not
root_node
.
dependents
:
      
file_node
=
dependency_nodes
.
values
(
)
[
0
]
      
file_node
.
dependencies
.
append
(
root_node
)
      
root_node
.
dependents
.
append
(
file_node
)
    
cycles
=
[
]
    
for
cycle
in
root_node
.
FindCycles
(
)
:
      
paths
=
[
node
.
ref
for
node
in
cycle
]
      
cycles
.
append
(
'
Cycle
:
%
s
'
%
'
-
>
'
.
join
(
paths
)
)
    
raise
DependencyGraphNode
.
CircularException
(
        
'
Cycles
in
.
gyp
file
dependency
graph
detected
:
\
n
'
+
'
\
n
'
.
join
(
cycles
)
)
def
DoDependentSettings
(
key
flat_list
targets
dependency_nodes
)
:
  
for
target
in
flat_list
:
    
target_dict
=
targets
[
target
]
    
build_file
=
gyp
.
common
.
BuildFile
(
target
)
    
if
key
=
=
'
all_dependent_settings
'
:
      
dependencies
=
dependency_nodes
[
target
]
.
DeepDependencies
(
)
    
elif
key
=
=
'
direct_dependent_settings
'
:
      
dependencies
=
\
          
dependency_nodes
[
target
]
.
DirectAndImportedDependencies
(
targets
)
    
elif
key
=
=
'
link_settings
'
:
      
dependencies
=
\
          
dependency_nodes
[
target
]
.
DependenciesForLinkSettings
(
targets
)
    
else
:
      
raise
GypError
(
"
DoDependentSettings
doesn
'
t
know
how
to
determine
"
                      
'
dependencies
for
'
+
key
)
    
for
dependency
in
dependencies
:
      
dependency_dict
=
targets
[
dependency
]
      
if
not
key
in
dependency_dict
:
        
continue
      
dependency_build_file
=
gyp
.
common
.
BuildFile
(
dependency
)
      
MergeDicts
(
target_dict
dependency_dict
[
key
]
                 
build_file
dependency_build_file
)
def
AdjustStaticLibraryDependencies
(
flat_list
targets
dependency_nodes
                                    
sort_dependencies
)
:
  
for
target
in
flat_list
:
    
target_dict
=
targets
[
target
]
    
target_type
=
target_dict
[
'
type
'
]
    
if
target_type
=
=
'
static_library
'
:
      
if
not
'
dependencies
'
in
target_dict
:
        
continue
      
target_dict
[
'
dependencies_original
'
]
=
target_dict
.
get
(
          
'
dependencies
'
[
]
)
[
:
]
      
dependencies
=
\
          
dependency_nodes
[
target
]
.
DirectAndImportedDependencies
(
targets
)
      
index
=
0
      
while
index
<
len
(
dependencies
)
:
        
dependency
=
dependencies
[
index
]
        
dependency_dict
=
targets
[
dependency
]
        
if
(
dependency_dict
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
and
\
            
not
dependency_dict
.
get
(
'
hard_dependency
'
False
)
)
or
\
           
(
dependency_dict
[
'
type
'
]
!
=
'
static_library
'
and
\
            
not
dependency
in
target_dict
[
'
dependencies
'
]
)
:
          
del
dependencies
[
index
]
        
else
:
          
index
=
index
+
1
      
if
len
(
dependencies
)
>
0
:
        
target_dict
[
'
dependencies
'
]
=
dependencies
      
else
:
        
del
target_dict
[
'
dependencies
'
]
    
elif
target_type
in
linkable_types
:
      
link_dependencies
=
\
          
dependency_nodes
[
target
]
.
DependenciesToLinkAgainst
(
targets
)
      
for
dependency
in
link_dependencies
:
        
if
dependency
=
=
target
:
          
continue
        
if
not
'
dependencies
'
in
target_dict
:
          
target_dict
[
'
dependencies
'
]
=
[
]
        
if
not
dependency
in
target_dict
[
'
dependencies
'
]
:
          
target_dict
[
'
dependencies
'
]
.
append
(
dependency
)
      
if
sort_dependencies
and
'
dependencies
'
in
target_dict
:
        
target_dict
[
'
dependencies
'
]
=
[
dep
for
dep
in
reversed
(
flat_list
)
                                       
if
dep
in
target_dict
[
'
dependencies
'
]
]
exception_re
=
re
.
compile
(
r
'
'
'
[
"
'
]
?
[
-
/
<
>
^
]
'
'
'
)
def
MakePathRelative
(
to_file
fro_file
item
)
:
  
if
to_file
=
=
fro_file
or
exception_re
.
match
(
item
)
:
    
return
item
  
else
:
    
ret
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
        
gyp
.
common
.
RelativePath
(
os
.
path
.
dirname
(
fro_file
)
                                
os
.
path
.
dirname
(
to_file
)
)
                                
item
)
)
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
    
if
item
[
-
1
]
=
=
'
/
'
:
      
ret
+
=
'
/
'
    
return
ret
def
MergeLists
(
to
fro
to_file
fro_file
is_paths
=
False
append
=
True
)
:
  
is_hashable
=
lambda
val
:
val
.
__hash__
  
def
is_in_set_or_list
(
x
s
l
)
:
    
if
is_hashable
(
x
)
:
      
return
x
in
s
    
return
x
in
l
  
prepend_index
=
0
  
hashable_to_set
=
set
(
x
for
x
in
to
if
is_hashable
(
x
)
)
  
for
item
in
fro
:
    
singleton
=
False
    
if
type
(
item
)
in
(
str
int
)
:
      
if
is_paths
:
        
to_item
=
MakePathRelative
(
to_file
fro_file
item
)
      
else
:
        
to_item
=
item
      
if
not
(
type
(
item
)
is
str
and
item
.
startswith
(
'
-
'
)
)
:
        
singleton
=
True
    
elif
type
(
item
)
is
dict
:
      
to_item
=
{
}
      
MergeDicts
(
to_item
item
to_file
fro_file
)
    
elif
type
(
item
)
is
list
:
      
to_item
=
[
]
      
MergeLists
(
to_item
item
to_file
fro_file
)
    
else
:
      
raise
TypeError
(
          
'
Attempt
to
merge
list
item
of
unsupported
type
'
+
\
          
item
.
__class__
.
__name__
)
    
if
append
:
      
if
not
singleton
or
not
is_in_set_or_list
(
to_item
hashable_to_set
to
)
:
        
to
.
append
(
to_item
)
        
if
is_hashable
(
to_item
)
:
          
hashable_to_set
.
add
(
to_item
)
    
else
:
      
while
singleton
and
to_item
in
to
:
        
to
.
remove
(
to_item
)
      
to
.
insert
(
prepend_index
to_item
)
      
if
is_hashable
(
to_item
)
:
        
hashable_to_set
.
add
(
to_item
)
      
prepend_index
=
prepend_index
+
1
def
MergeDicts
(
to
fro
to_file
fro_file
)
:
  
for
k
v
in
fro
.
iteritems
(
)
:
    
if
k
in
to
:
      
bad_merge
=
False
      
if
type
(
v
)
in
(
str
int
)
:
        
if
type
(
to
[
k
]
)
not
in
(
str
int
)
:
          
bad_merge
=
True
      
elif
type
(
v
)
is
not
type
(
to
[
k
]
)
:
        
bad_merge
=
True
      
if
bad_merge
:
        
raise
TypeError
(
            
'
Attempt
to
merge
dict
value
of
type
'
+
v
.
__class__
.
__name__
+
\
            
'
into
incompatible
type
'
+
to
[
k
]
.
__class__
.
__name__
+
\
            
'
for
key
'
+
k
)
    
if
type
(
v
)
in
(
str
int
)
:
      
is_path
=
IsPathSection
(
k
)
      
if
is_path
:
        
to
[
k
]
=
MakePathRelative
(
to_file
fro_file
v
)
      
else
:
        
to
[
k
]
=
v
    
elif
type
(
v
)
is
dict
:
      
if
not
k
in
to
:
        
to
[
k
]
=
{
}
      
MergeDicts
(
to
[
k
]
v
to_file
fro_file
)
    
elif
type
(
v
)
is
list
:
      
ext
=
k
[
-
1
]
      
append
=
True
      
if
ext
=
=
'
=
'
:
        
list_base
=
k
[
:
-
1
]
        
lists_incompatible
=
[
list_base
list_base
+
'
?
'
]
        
to
[
list_base
]
=
[
]
      
elif
ext
=
=
'
+
'
:
        
list_base
=
k
[
:
-
1
]
        
lists_incompatible
=
[
list_base
+
'
=
'
list_base
+
'
?
'
]
        
append
=
False
      
elif
ext
=
=
'
?
'
:
        
list_base
=
k
[
:
-
1
]
        
lists_incompatible
=
[
list_base
list_base
+
'
=
'
list_base
+
'
+
'
]
      
else
:
        
list_base
=
k
        
lists_incompatible
=
[
list_base
+
'
=
'
list_base
+
'
?
'
]
      
for
list_incompatible
in
lists_incompatible
:
        
if
list_incompatible
in
fro
:
          
raise
GypError
(
'
Incompatible
list
policies
'
+
k
+
'
and
'
+
                         
list_incompatible
)
      
if
list_base
in
to
:
        
if
ext
=
=
'
?
'
:
          
continue
        
elif
type
(
to
[
list_base
]
)
is
not
list
:
          
raise
TypeError
(
              
'
Attempt
to
merge
dict
value
of
type
'
+
v
.
__class__
.
__name__
+
\
              
'
into
incompatible
type
'
+
to
[
list_base
]
.
__class__
.
__name__
+
\
              
'
for
key
'
+
list_base
+
'
(
'
+
k
+
'
)
'
)
      
else
:
        
to
[
list_base
]
=
[
]
      
is_paths
=
IsPathSection
(
list_base
)
      
MergeLists
(
to
[
list_base
]
v
to_file
fro_file
is_paths
append
)
    
else
:
      
raise
TypeError
(
          
'
Attempt
to
merge
dict
value
of
unsupported
type
'
+
\
          
v
.
__class__
.
__name__
+
'
for
key
'
+
k
)
def
MergeConfigWithInheritance
(
new_configuration_dict
build_file
                               
target_dict
configuration
visited
)
:
  
if
configuration
in
visited
:
    
return
  
configuration_dict
=
target_dict
[
'
configurations
'
]
[
configuration
]
  
for
parent
in
configuration_dict
.
get
(
'
inherit_from
'
[
]
)
:
    
MergeConfigWithInheritance
(
new_configuration_dict
build_file
                               
target_dict
parent
visited
+
[
configuration
]
)
  
MergeDicts
(
new_configuration_dict
configuration_dict
             
build_file
build_file
)
  
if
'
abstract
'
in
new_configuration_dict
:
    
del
new_configuration_dict
[
'
abstract
'
]
def
SetUpConfigurations
(
target
target_dict
)
:
  
key_suffixes
=
[
'
=
'
'
+
'
'
?
'
'
!
'
'
/
'
]
  
build_file
=
gyp
.
common
.
BuildFile
(
target
)
  
if
not
'
configurations
'
in
target_dict
:
    
target_dict
[
'
configurations
'
]
=
{
'
Default
'
:
{
}
}
  
if
not
'
default_configuration
'
in
target_dict
:
    
concrete
=
[
i
for
(
i
config
)
in
target_dict
[
'
configurations
'
]
.
iteritems
(
)
                
if
not
config
.
get
(
'
abstract
'
)
]
    
target_dict
[
'
default_configuration
'
]
=
sorted
(
concrete
)
[
0
]
  
merged_configurations
=
{
}
  
configs
=
target_dict
[
'
configurations
'
]
  
for
(
configuration
old_configuration_dict
)
in
configs
.
iteritems
(
)
:
    
if
old_configuration_dict
.
get
(
'
abstract
'
)
:
      
continue
    
new_configuration_dict
=
{
}
    
for
(
key
target_val
)
in
target_dict
.
iteritems
(
)
:
      
key_ext
=
key
[
-
1
:
]
      
if
key_ext
in
key_suffixes
:
        
key_base
=
key
[
:
-
1
]
      
else
:
        
key_base
=
key
      
if
not
key_base
in
non_configuration_keys
:
        
new_configuration_dict
[
key
]
=
gyp
.
simple_copy
.
deepcopy
(
target_val
)
    
MergeConfigWithInheritance
(
new_configuration_dict
build_file
                               
target_dict
configuration
[
]
)
    
merged_configurations
[
configuration
]
=
new_configuration_dict
  
for
configuration
in
merged_configurations
.
keys
(
)
:
    
target_dict
[
'
configurations
'
]
[
configuration
]
=
(
        
merged_configurations
[
configuration
]
)
  
for
configuration
in
target_dict
[
'
configurations
'
]
.
keys
(
)
:
    
old_configuration_dict
=
target_dict
[
'
configurations
'
]
[
configuration
]
    
if
old_configuration_dict
.
get
(
'
abstract
'
)
:
      
del
target_dict
[
'
configurations
'
]
[
configuration
]
  
delete_keys
=
[
]
  
for
key
in
target_dict
:
    
key_ext
=
key
[
-
1
:
]
    
if
key_ext
in
key_suffixes
:
      
key_base
=
key
[
:
-
1
]
    
else
:
      
key_base
=
key
    
if
not
key_base
in
non_configuration_keys
:
      
delete_keys
.
append
(
key
)
  
for
key
in
delete_keys
:
    
del
target_dict
[
key
]
  
for
configuration
in
target_dict
[
'
configurations
'
]
.
keys
(
)
:
    
configuration_dict
=
target_dict
[
'
configurations
'
]
[
configuration
]
    
for
key
in
configuration_dict
.
keys
(
)
:
      
if
key
in
invalid_configuration_keys
:
        
raise
GypError
(
'
%
s
not
allowed
in
the
%
s
configuration
found
in
'
                       
'
target
%
s
'
%
(
key
configuration
target
)
)
def
ProcessListFiltersInDict
(
name
the_dict
)
:
  
"
"
"
Process
regular
expression
and
exclusion
-
based
filters
on
lists
.
  
An
exclusion
list
is
in
a
dict
key
named
with
a
trailing
"
!
"
like
  
"
sources
!
"
.
Every
item
in
such
a
list
is
removed
from
the
associated
  
main
list
which
in
this
example
would
be
"
sources
"
.
Removed
items
are
  
placed
into
a
"
sources_excluded
"
list
in
the
dict
.
  
Regular
expression
(
regex
)
filters
are
contained
in
dict
keys
named
with
a
  
trailing
"
/
"
such
as
"
sources
/
"
to
operate
on
the
"
sources
"
list
.
Regex
  
filters
in
a
dict
take
the
form
:
    
'
sources
/
'
:
[
[
'
exclude
'
'
_
(
linux
|
mac
|
win
)
\
\
.
cc
'
]
                  
[
'
include
'
'
_mac
\
\
.
cc
'
]
]
  
The
first
filter
says
to
exclude
all
files
ending
in
_linux
.
cc
_mac
.
cc
and
  
_win
.
cc
.
The
second
filter
then
includes
all
files
ending
in
_mac
.
cc
that
  
are
now
or
were
once
in
the
"
sources
"
list
.
Items
matching
an
"
exclude
"
  
filter
are
subject
to
the
same
processing
as
would
occur
if
they
were
listed
  
by
name
in
an
exclusion
list
(
ending
in
"
!
"
)
.
Items
matching
an
"
include
"
  
filter
are
brought
back
into
the
main
list
if
previously
excluded
by
an
  
exclusion
list
or
exclusion
regex
filter
.
Subsequent
matching
"
exclude
"
  
patterns
can
still
cause
items
to
be
excluded
after
matching
an
"
include
"
.
  
"
"
"
  
lists
=
[
]
  
del_lists
=
[
]
  
for
key
value
in
the_dict
.
iteritems
(
)
:
    
operation
=
key
[
-
1
]
    
if
operation
!
=
'
!
'
and
operation
!
=
'
/
'
:
      
continue
    
if
type
(
value
)
is
not
list
:
      
raise
ValueError
(
name
+
'
key
'
+
key
+
'
must
be
list
not
'
+
\
                       
value
.
__class__
.
__name__
)
    
list_key
=
key
[
:
-
1
]
    
if
list_key
not
in
the_dict
:
      
del_lists
.
append
(
key
)
      
continue
    
if
type
(
the_dict
[
list_key
]
)
is
not
list
:
      
value
=
the_dict
[
list_key
]
      
raise
ValueError
(
name
+
'
key
'
+
list_key
+
\
                       
'
must
be
list
not
'
+
\
                       
value
.
__class__
.
__name__
+
'
when
applying
'
+
\
                       
{
'
!
'
:
'
exclusion
'
'
/
'
:
'
regex
'
}
[
operation
]
)
    
if
not
list_key
in
lists
:
      
lists
.
append
(
list_key
)
  
for
del_list
in
del_lists
:
    
del
the_dict
[
del_list
]
  
for
list_key
in
lists
:
    
the_list
=
the_dict
[
list_key
]
    
list_actions
=
list
(
(
-
1
)
*
len
(
the_list
)
)
    
exclude_key
=
list_key
+
'
!
'
    
if
exclude_key
in
the_dict
:
      
for
exclude_item
in
the_dict
[
exclude_key
]
:
        
for
index
in
xrange
(
0
len
(
the_list
)
)
:
          
if
exclude_item
=
=
the_list
[
index
]
:
            
list_actions
[
index
]
=
0
      
del
the_dict
[
exclude_key
]
    
regex_key
=
list_key
+
'
/
'
    
if
regex_key
in
the_dict
:
      
for
regex_item
in
the_dict
[
regex_key
]
:
        
[
action
pattern
]
=
regex_item
        
pattern_re
=
re
.
compile
(
pattern
)
        
if
action
=
=
'
exclude
'
:
          
action_value
=
0
        
elif
action
=
=
'
include
'
:
          
action_value
=
1
        
else
:
          
raise
ValueError
(
'
Unrecognized
action
'
+
action
+
'
in
'
+
name
+
\
                           
'
key
'
+
regex_key
)
        
for
index
in
xrange
(
0
len
(
the_list
)
)
:
          
list_item
=
the_list
[
index
]
          
if
list_actions
[
index
]
=
=
action_value
:
            
continue
          
if
pattern_re
.
search
(
list_item
)
:
            
list_actions
[
index
]
=
action_value
      
del
the_dict
[
regex_key
]
    
excluded_key
=
list_key
+
'
_excluded
'
    
if
excluded_key
in
the_dict
:
      
raise
GypError
(
name
+
'
key
'
+
excluded_key
+
                     
'
must
not
be
present
prior
'
                     
'
to
applying
exclusion
/
regex
filters
for
'
+
list_key
)
    
excluded_list
=
[
]
    
for
index
in
xrange
(
len
(
list_actions
)
-
1
-
1
-
1
)
:
      
if
list_actions
[
index
]
=
=
0
:
        
excluded_list
.
insert
(
0
the_list
[
index
]
)
        
del
the_list
[
index
]
    
if
len
(
excluded_list
)
>
0
:
      
the_dict
[
excluded_key
]
=
excluded_list
  
for
key
value
in
the_dict
.
iteritems
(
)
:
    
if
type
(
value
)
is
dict
:
      
ProcessListFiltersInDict
(
key
value
)
    
elif
type
(
value
)
is
list
:
      
ProcessListFiltersInList
(
key
value
)
def
ProcessListFiltersInList
(
name
the_list
)
:
  
for
item
in
the_list
:
    
if
type
(
item
)
is
dict
:
      
ProcessListFiltersInDict
(
name
item
)
    
elif
type
(
item
)
is
list
:
      
ProcessListFiltersInList
(
name
item
)
def
ValidateTargetType
(
target
target_dict
)
:
  
"
"
"
Ensures
the
'
type
'
field
on
the
target
is
one
of
the
known
types
.
  
Arguments
:
    
target
:
string
name
of
target
.
    
target_dict
:
dict
target
spec
.
  
Raises
an
exception
on
error
.
  
"
"
"
  
VALID_TARGET_TYPES
=
(
'
executable
'
'
loadable_module
'
                        
'
static_library
'
'
shared_library
'
                        
'
mac_kernel_extension
'
'
none
'
'
windows_driver
'
)
  
target_type
=
target_dict
.
get
(
'
type
'
None
)
  
if
target_type
not
in
VALID_TARGET_TYPES
:
    
raise
GypError
(
"
Target
%
s
has
an
invalid
target
type
'
%
s
'
.
"
                   
"
Must
be
one
of
%
s
.
"
%
                   
(
target
target_type
'
/
'
.
join
(
VALID_TARGET_TYPES
)
)
)
  
if
(
target_dict
.
get
(
'
standalone_static_library
'
0
)
and
      
not
target_type
=
=
'
static_library
'
)
:
    
raise
GypError
(
'
Target
%
s
has
type
%
s
but
standalone_static_library
flag
is
'
                   
'
only
valid
for
static_library
type
.
'
%
(
target
                                                             
target_type
)
)
def
ValidateSourcesInTarget
(
target
target_dict
build_file
                            
duplicate_basename_check
)
:
  
if
not
duplicate_basename_check
:
    
return
  
if
target_dict
.
get
(
'
type
'
None
)
!
=
'
static_library
'
:
    
return
  
sources
=
target_dict
.
get
(
'
sources
'
[
]
)
  
basenames
=
{
}
  
for
source
in
sources
:
    
name
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
    
is_compiled_file
=
ext
in
[
        
'
.
c
'
'
.
cc
'
'
.
cpp
'
'
.
cxx
'
'
.
m
'
'
.
mm
'
'
.
s
'
'
.
S
'
]
    
if
not
is_compiled_file
:
      
continue
    
basename
=
os
.
path
.
basename
(
name
)
    
basenames
.
setdefault
(
basename
[
]
)
.
append
(
source
)
  
error
=
'
'
  
for
basename
files
in
basenames
.
iteritems
(
)
:
    
if
len
(
files
)
>
1
:
      
error
+
=
'
%
s
:
%
s
\
n
'
%
(
basename
'
'
.
join
(
files
)
)
  
if
error
:
    
print
(
'
static
library
%
s
has
several
files
with
the
same
basename
:
\
n
'
%
          
target
+
error
+
'
libtool
on
Mac
cannot
handle
that
.
Use
'
          
'
-
-
no
-
duplicate
-
basename
-
check
to
disable
this
validation
.
'
)
    
raise
GypError
(
'
Duplicate
basenames
in
sources
section
see
list
above
'
)
def
ValidateRulesInTarget
(
target
target_dict
extra_sources_for_rules
)
:
  
"
"
"
Ensures
that
the
rules
sections
in
target_dict
are
valid
and
consistent
  
and
determines
which
sources
they
apply
to
.
  
Arguments
:
    
target
:
string
name
of
target
.
    
target_dict
:
dict
target
spec
containing
"
rules
"
and
"
sources
"
lists
.
    
extra_sources_for_rules
:
a
list
of
keys
to
scan
for
rule
matches
in
        
addition
to
'
sources
'
.
  
"
"
"
  
rule_names
=
{
}
  
rule_extensions
=
{
}
  
rules
=
target_dict
.
get
(
'
rules
'
[
]
)
  
for
rule
in
rules
:
    
rule_name
=
rule
[
'
rule_name
'
]
    
if
rule_name
in
rule_names
:
      
raise
GypError
(
'
rule
%
s
exists
in
duplicate
target
%
s
'
%
                     
(
rule_name
target
)
)
    
rule_names
[
rule_name
]
=
rule
    
rule_extension
=
rule
[
'
extension
'
]
    
if
rule_extension
.
startswith
(
'
.
'
)
:
      
rule_extension
=
rule_extension
[
1
:
]
    
if
rule_extension
in
rule_extensions
:
      
raise
GypError
(
(
'
extension
%
s
associated
with
multiple
rules
'
+
                      
'
target
%
s
rules
%
s
and
%
s
'
)
%
                     
(
rule_extension
target
                      
rule_extensions
[
rule_extension
]
[
'
rule_name
'
]
                      
rule_name
)
)
    
rule_extensions
[
rule_extension
]
=
rule
    
if
'
rule_sources
'
in
rule
:
      
raise
GypError
(
            
'
rule_sources
must
not
exist
in
input
target
%
s
rule
%
s
'
%
            
(
target
rule_name
)
)
    
rule_sources
=
[
]
    
source_keys
=
[
'
sources
'
]
    
source_keys
.
extend
(
extra_sources_for_rules
)
    
for
source_key
in
source_keys
:
      
for
source
in
target_dict
.
get
(
source_key
[
]
)
:
        
(
source_root
source_extension
)
=
os
.
path
.
splitext
(
source
)
        
if
source_extension
.
startswith
(
'
.
'
)
:
          
source_extension
=
source_extension
[
1
:
]
        
if
source_extension
=
=
rule_extension
:
          
rule_sources
.
append
(
source
)
    
if
len
(
rule_sources
)
>
0
:
      
rule
[
'
rule_sources
'
]
=
rule_sources
def
ValidateRunAsInTarget
(
target
target_dict
build_file
)
:
  
target_name
=
target_dict
.
get
(
'
target_name
'
)
  
run_as
=
target_dict
.
get
(
'
run_as
'
)
  
if
not
run_as
:
    
return
  
if
type
(
run_as
)
is
not
dict
:
    
raise
GypError
(
"
The
'
run_as
'
in
target
%
s
from
file
%
s
should
be
a
"
                   
"
dictionary
.
"
%
                   
(
target_name
build_file
)
)
  
action
=
run_as
.
get
(
'
action
'
)
  
if
not
action
:
    
raise
GypError
(
"
The
'
run_as
'
in
target
%
s
from
file
%
s
must
have
an
"
                   
"
'
action
'
section
.
"
%
                   
(
target_name
build_file
)
)
  
if
type
(
action
)
is
not
list
:
    
raise
GypError
(
"
The
'
action
'
for
'
run_as
'
in
target
%
s
from
file
%
s
"
                   
"
must
be
a
list
.
"
%
                   
(
target_name
build_file
)
)
  
working_directory
=
run_as
.
get
(
'
working_directory
'
)
  
if
working_directory
and
type
(
working_directory
)
is
not
str
:
    
raise
GypError
(
"
The
'
working_directory
'
for
'
run_as
'
in
target
%
s
"
                   
"
in
file
%
s
should
be
a
string
.
"
%
                   
(
target_name
build_file
)
)
  
environment
=
run_as
.
get
(
'
environment
'
)
  
if
environment
and
type
(
environment
)
is
not
dict
:
    
raise
GypError
(
"
The
'
environment
'
for
'
run_as
'
in
target
%
s
"
                   
"
in
file
%
s
should
be
a
dictionary
.
"
%
                   
(
target_name
build_file
)
)
def
ValidateActionsInTarget
(
target
target_dict
build_file
)
:
  
'
'
'
Validates
the
inputs
to
the
actions
in
a
target
.
'
'
'
  
target_name
=
target_dict
.
get
(
'
target_name
'
)
  
actions
=
target_dict
.
get
(
'
actions
'
[
]
)
  
for
action
in
actions
:
    
action_name
=
action
.
get
(
'
action_name
'
)
    
if
not
action_name
:
      
raise
GypError
(
"
Anonymous
action
in
target
%
s
.
"
                     
"
An
action
must
have
an
'
action_name
'
field
.
"
%
                     
target_name
)
    
inputs
=
action
.
get
(
'
inputs
'
None
)
    
if
inputs
is
None
:
      
raise
GypError
(
'
Action
in
target
%
s
has
no
inputs
.
'
%
target_name
)
    
action_command
=
action
.
get
(
'
action
'
)
    
if
action_command
and
not
action_command
[
0
]
:
      
raise
GypError
(
"
Empty
action
as
command
in
target
%
s
.
"
%
target_name
)
def
TurnIntIntoStrInDict
(
the_dict
)
:
  
"
"
"
Given
dict
the_dict
recursively
converts
all
integers
into
strings
.
  
"
"
"
  
for
k
v
in
the_dict
.
items
(
)
:
    
if
type
(
v
)
is
int
:
      
v
=
str
(
v
)
      
the_dict
[
k
]
=
v
    
elif
type
(
v
)
is
dict
:
      
TurnIntIntoStrInDict
(
v
)
    
elif
type
(
v
)
is
list
:
      
TurnIntIntoStrInList
(
v
)
    
if
type
(
k
)
is
int
:
      
del
the_dict
[
k
]
      
the_dict
[
str
(
k
)
]
=
v
def
TurnIntIntoStrInList
(
the_list
)
:
  
"
"
"
Given
list
the_list
recursively
converts
all
integers
into
strings
.
  
"
"
"
  
for
index
in
xrange
(
0
len
(
the_list
)
)
:
    
item
=
the_list
[
index
]
    
if
type
(
item
)
is
int
:
      
the_list
[
index
]
=
str
(
item
)
    
elif
type
(
item
)
is
dict
:
      
TurnIntIntoStrInDict
(
item
)
    
elif
type
(
item
)
is
list
:
      
TurnIntIntoStrInList
(
item
)
def
PruneUnwantedTargets
(
targets
flat_list
dependency_nodes
root_targets
                         
data
)
:
  
"
"
"
Return
only
the
targets
that
are
deep
dependencies
of
|
root_targets
|
.
"
"
"
  
qualified_root_targets
=
[
]
  
for
target
in
root_targets
:
    
target
=
target
.
strip
(
)
    
qualified_targets
=
gyp
.
common
.
FindQualifiedTargets
(
target
flat_list
)
    
if
not
qualified_targets
:
      
raise
GypError
(
"
Could
not
find
target
%
s
"
%
target
)
    
qualified_root_targets
.
extend
(
qualified_targets
)
  
wanted_targets
=
{
}
  
for
target
in
qualified_root_targets
:
    
wanted_targets
[
target
]
=
targets
[
target
]
    
for
dependency
in
dependency_nodes
[
target
]
.
DeepDependencies
(
)
:
      
wanted_targets
[
dependency
]
=
targets
[
dependency
]
  
wanted_flat_list
=
[
t
for
t
in
flat_list
if
t
in
wanted_targets
]
  
for
build_file
in
data
[
'
target_build_files
'
]
:
    
if
not
'
targets
'
in
data
[
build_file
]
:
      
continue
    
new_targets
=
[
]
    
for
target
in
data
[
build_file
]
[
'
targets
'
]
:
      
qualified_name
=
gyp
.
common
.
QualifiedTarget
(
build_file
                                                  
target
[
'
target_name
'
]
                                                  
target
[
'
toolset
'
]
)
      
if
qualified_name
in
wanted_targets
:
        
new_targets
.
append
(
target
)
    
data
[
build_file
]
[
'
targets
'
]
=
new_targets
  
return
wanted_targets
wanted_flat_list
def
VerifyNoCollidingTargets
(
targets
)
:
  
"
"
"
Verify
that
no
two
targets
in
the
same
directory
share
the
same
name
.
  
Arguments
:
    
targets
:
A
list
of
targets
in
the
form
'
path
/
to
/
file
.
gyp
:
target_name
'
.
  
"
"
"
  
used
=
{
}
  
for
target
in
targets
:
    
path
name
=
target
.
rsplit
(
'
:
'
1
)
    
subdir
gyp
=
os
.
path
.
split
(
path
)
    
if
not
subdir
:
      
subdir
=
'
.
'
    
key
=
subdir
+
'
:
'
+
name
    
if
key
in
used
:
      
raise
GypError
(
'
Duplicate
target
name
"
%
s
"
in
directory
"
%
s
"
used
both
'
                     
'
in
"
%
s
"
and
"
%
s
"
.
'
%
(
name
subdir
gyp
used
[
key
]
)
)
    
used
[
key
]
=
gyp
def
SetGeneratorGlobals
(
generator_input_info
)
:
  
global
path_sections
  
path_sections
=
set
(
base_path_sections
)
  
path_sections
.
update
(
generator_input_info
[
'
path_sections
'
]
)
  
global
non_configuration_keys
  
non_configuration_keys
=
base_non_configuration_keys
[
:
]
  
non_configuration_keys
.
extend
(
generator_input_info
[
'
non_configuration_keys
'
]
)
  
global
multiple_toolsets
  
multiple_toolsets
=
generator_input_info
[
      
'
generator_supports_multiple_toolsets
'
]
  
global
generator_filelist_paths
  
generator_filelist_paths
=
generator_input_info
[
'
generator_filelist_paths
'
]
def
Load
(
build_files
variables
includes
depth
generator_input_info
check
         
circular_check
duplicate_basename_check
parallel
root_targets
)
:
  
SetGeneratorGlobals
(
generator_input_info
)
  
extra_sources_for_rules
=
generator_input_info
[
'
extra_sources_for_rules
'
]
  
data
=
{
'
target_build_files
'
:
set
(
)
}
  
build_files
=
set
(
map
(
os
.
path
.
normpath
build_files
)
)
  
if
parallel
:
    
LoadTargetBuildFilesParallel
(
build_files
data
variables
includes
depth
                                 
check
generator_input_info
)
  
else
:
    
aux_data
=
{
}
    
for
build_file
in
build_files
:
      
try
:
        
LoadTargetBuildFile
(
build_file
data
aux_data
                            
variables
includes
depth
check
True
)
      
except
Exception
e
:
        
gyp
.
common
.
ExceptionAppend
(
e
'
while
trying
to
load
%
s
'
%
build_file
)
        
raise
  
targets
=
BuildTargetsDict
(
data
)
  
QualifyDependencies
(
targets
)
  
RemoveSelfDependencies
(
targets
)
  
ExpandWildcardDependencies
(
targets
data
)
  
RemoveLinkDependenciesFromNoneTargets
(
targets
)
  
for
target_name
target_dict
in
targets
.
iteritems
(
)
:
    
tmp_dict
=
{
}
    
for
key_base
in
dependency_sections
:
      
for
op
in
(
'
'
'
!
'
'
/
'
)
:
        
key
=
key_base
+
op
        
if
key
in
target_dict
:
          
tmp_dict
[
key
]
=
target_dict
[
key
]
          
del
target_dict
[
key
]
    
ProcessListFiltersInDict
(
target_name
tmp_dict
)
    
for
key
in
tmp_dict
:
      
target_dict
[
key
]
=
tmp_dict
[
key
]
  
RemoveDuplicateDependencies
(
targets
)
  
if
circular_check
:
    
VerifyNoGYPFileCircularDependencies
(
targets
)
  
[
dependency_nodes
flat_list
]
=
BuildDependencyList
(
targets
)
  
if
root_targets
:
    
targets
flat_list
=
PruneUnwantedTargets
(
        
targets
flat_list
dependency_nodes
root_targets
data
)
  
VerifyNoCollidingTargets
(
flat_list
)
  
for
settings_type
in
[
'
all_dependent_settings
'
                        
'
direct_dependent_settings
'
                        
'
link_settings
'
]
:
    
DoDependentSettings
(
settings_type
flat_list
targets
dependency_nodes
)
    
for
target
in
flat_list
:
      
if
settings_type
in
targets
[
target
]
:
        
del
targets
[
target
]
[
settings_type
]
  
gii
=
generator_input_info
  
if
gii
[
'
generator_wants_static_library_dependencies_adjusted
'
]
:
    
AdjustStaticLibraryDependencies
(
flat_list
targets
dependency_nodes
                                    
gii
[
'
generator_wants_sorted_dependencies
'
]
)
  
for
target
in
flat_list
:
    
target_dict
=
targets
[
target
]
    
build_file
=
gyp
.
common
.
BuildFile
(
target
)
    
ProcessVariablesAndConditionsInDict
(
        
target_dict
PHASE_LATE
variables
build_file
)
  
for
target
in
flat_list
:
    
target_dict
=
targets
[
target
]
    
SetUpConfigurations
(
target
target_dict
)
  
for
target
in
flat_list
:
    
target_dict
=
targets
[
target
]
    
ProcessListFiltersInDict
(
target
target_dict
)
  
for
target
in
flat_list
:
    
target_dict
=
targets
[
target
]
    
build_file
=
gyp
.
common
.
BuildFile
(
target
)
    
ProcessVariablesAndConditionsInDict
(
        
target_dict
PHASE_LATELATE
variables
build_file
)
  
for
target
in
flat_list
:
    
target_dict
=
targets
[
target
]
    
build_file
=
gyp
.
common
.
BuildFile
(
target
)
    
ValidateTargetType
(
target
target_dict
)
    
ValidateSourcesInTarget
(
target
target_dict
build_file
                            
duplicate_basename_check
)
    
ValidateRulesInTarget
(
target
target_dict
extra_sources_for_rules
)
    
ValidateRunAsInTarget
(
target
target_dict
build_file
)
    
ValidateActionsInTarget
(
target
target_dict
build_file
)
  
TurnIntIntoStrInDict
(
data
)
  
return
[
flat_list
targets
data
]
