import
os
import
os
.
path
import
shutil
import
subprocess
import
sys
def
Main
(
args
)
:
  
"
"
"
Main
function
for
the
linker
driver
.
Separates
out
the
arguments
for
  
the
main
compiler
driver
and
the
linker
driver
then
invokes
all
the
  
required
tools
.
  
Args
:
    
args
:
list
of
string
Arguments
to
the
script
.
  
"
"
"
  
if
len
(
args
)
<
2
:
    
raise
RuntimeError
(
"
Usage
:
linker_driver
.
py
[
linker
-
invocation
]
"
)
  
for
i
in
xrange
(
len
(
args
)
)
:
    
if
args
[
i
]
!
=
'
-
-
developer_dir
'
:
      
continue
    
os
.
environ
[
'
DEVELOPER_DIR
'
]
=
args
[
i
+
1
]
    
del
args
[
i
:
i
+
2
]
    
break
  
linker_driver_actions
=
{
}
  
compiler_driver_args
=
[
]
  
for
arg
in
args
[
1
:
]
:
    
if
arg
.
startswith
(
_LINKER_DRIVER_ARG_PREFIX
)
:
      
driver_action
=
ProcessLinkerDriverArg
(
arg
)
      
assert
driver_action
[
0
]
not
in
linker_driver_actions
      
linker_driver_actions
[
driver_action
[
0
]
]
=
driver_action
[
1
]
    
else
:
      
compiler_driver_args
.
append
(
arg
)
  
linker_driver_outputs
=
[
_FindLinkerOutput
(
compiler_driver_args
)
]
  
try
:
    
subprocess
.
check_call
(
compiler_driver_args
)
    
for
action
in
_LINKER_DRIVER_ACTIONS
:
      
name
=
action
[
0
]
      
if
name
in
linker_driver_actions
:
        
linker_driver_outputs
+
=
linker_driver_actions
[
name
]
(
args
)
  
except
:
    
map
(
_RemovePath
linker_driver_outputs
)
    
raise
def
ProcessLinkerDriverArg
(
arg
)
:
  
"
"
"
Processes
a
linker
driver
argument
and
returns
a
tuple
containing
the
  
name
and
unary
lambda
to
invoke
for
that
linker
driver
action
.
  
Args
:
    
arg
:
string
The
linker
driver
argument
.
  
Returns
:
    
A
2
-
tuple
:
      
0
:
The
driver
action
name
as
in
_LINKER_DRIVER_ACTIONS
.
      
1
:
An
1
-
ary
lambda
that
takes
the
full
list
of
arguments
passed
to
         
Main
(
)
.
The
lambda
should
call
the
linker
driver
action
that
         
corresponds
to
the
argument
and
return
a
list
of
outputs
from
the
         
action
.
  
"
"
"
  
if
not
arg
.
startswith
(
_LINKER_DRIVER_ARG_PREFIX
)
:
    
raise
ValueError
(
'
%
s
is
not
a
linker
driver
argument
'
%
(
arg
)
)
  
sub_arg
=
arg
[
len
(
_LINKER_DRIVER_ARG_PREFIX
)
:
]
  
for
driver_action
in
_LINKER_DRIVER_ACTIONS
:
    
(
name
action
)
=
driver_action
    
if
sub_arg
.
startswith
(
name
)
:
      
return
(
name
          
lambda
full_args
:
action
(
sub_arg
[
len
(
name
)
:
]
full_args
)
)
  
raise
ValueError
(
'
Unknown
linker
driver
argument
:
%
s
'
%
(
arg
)
)
def
RunDsymUtil
(
dsym_path_prefix
full_args
)
:
  
"
"
"
Linker
driver
action
for
-
Wcrl
dsym
<
dsym
-
path
-
prefix
>
.
Invokes
dsymutil
  
on
the
linker
'
s
output
and
produces
a
dsym
file
at
|
dsym_file
|
path
.
  
Args
:
    
dsym_path_prefix
:
string
The
path
at
which
the
dsymutil
output
should
be
        
located
.
    
full_args
:
list
of
string
Full
argument
list
for
the
linker
driver
.
  
Returns
:
      
list
of
string
Build
step
outputs
.
  
"
"
"
  
if
not
len
(
dsym_path_prefix
)
:
    
raise
ValueError
(
'
Unspecified
dSYM
output
file
'
)
  
linker_out
=
_FindLinkerOutput
(
full_args
)
  
base
=
os
.
path
.
basename
(
linker_out
)
  
dsym_out
=
os
.
path
.
join
(
dsym_path_prefix
base
+
'
.
dSYM
'
)
  
_RemovePath
(
dsym_out
)
  
subprocess
.
check_call
(
[
'
xcrun
'
'
dsymutil
'
'
-
o
'
dsym_out
linker_out
]
)
  
return
[
dsym_out
]
def
RunSaveUnstripped
(
unstripped_path_prefix
full_args
)
:
  
"
"
"
Linker
driver
action
for
-
Wcrl
unstripped
<
unstripped_path_prefix
>
.
Copies
  
the
linker
output
to
|
unstripped_path_prefix
|
before
stripping
.
  
Args
:
    
unstripped_path_prefix
:
string
The
path
at
which
the
unstripped
output
        
should
be
located
.
    
full_args
:
list
of
string
Full
argument
list
for
the
linker
driver
.
  
Returns
:
    
list
of
string
Build
step
outputs
.
  
"
"
"
  
if
not
len
(
unstripped_path_prefix
)
:
    
raise
ValueError
(
'
Unspecified
unstripped
output
file
'
)
  
linker_out
=
_FindLinkerOutput
(
full_args
)
  
base
=
os
.
path
.
basename
(
linker_out
)
  
unstripped_out
=
os
.
path
.
join
(
unstripped_path_prefix
base
+
'
.
unstripped
'
)
  
shutil
.
copyfile
(
linker_out
unstripped_out
)
  
return
[
unstripped_out
]
def
RunStrip
(
strip_args_string
full_args
)
:
  
"
"
"
Linker
driver
action
for
-
Wcrl
strip
<
strip_arguments
>
.
  
Args
:
      
strip_args_string
:
string
Comma
-
separated
arguments
for
strip
.
      
full_args
:
list
of
string
Full
arguments
for
the
linker
driver
.
  
Returns
:
      
list
of
string
Build
step
outputs
.
  
"
"
"
  
strip_command
=
[
'
xcrun
'
'
strip
'
]
  
if
len
(
strip_args_string
)
>
0
:
    
strip_command
+
=
strip_args_string
.
split
(
'
'
)
  
strip_command
.
append
(
_FindLinkerOutput
(
full_args
)
)
  
subprocess
.
check_call
(
strip_command
)
  
return
[
]
def
_FindLinkerOutput
(
full_args
)
:
  
"
"
"
Finds
the
output
of
the
linker
by
looking
for
the
output
flag
in
its
  
argument
list
.
As
this
is
a
required
linker
argument
raises
an
error
if
it
  
cannot
be
found
.
  
"
"
"
  
try
:
    
output_flag_index
=
full_args
.
index
(
'
-
o
'
)
  
except
ValueError
:
    
output_flag_index
=
full_args
.
index
(
'
-
output
'
)
  
return
full_args
[
output_flag_index
+
1
]
def
_RemovePath
(
path
)
:
  
"
"
"
Removes
the
file
or
directory
at
|
path
|
if
it
exists
.
"
"
"
  
if
os
.
path
.
exists
(
path
)
:
    
if
os
.
path
.
isdir
(
path
)
:
      
shutil
.
rmtree
(
path
)
    
else
:
      
os
.
unlink
(
path
)
_LINKER_DRIVER_ARG_PREFIX
=
'
-
Wcrl
'
"
"
"
List
of
linker
driver
actions
.
The
sort
order
of
this
list
affects
the
order
in
which
the
actions
are
invoked
.
The
first
item
in
the
tuple
is
the
argument
'
s
-
Wcrl
<
sub_argument
>
and
the
second
is
the
function
to
invoke
.
"
"
"
_LINKER_DRIVER_ACTIONS
=
[
    
(
'
dsym
'
RunDsymUtil
)
    
(
'
unstripped
'
RunSaveUnstripped
)
    
(
'
strip
'
RunStrip
)
]
if
__name__
=
=
'
__main__
'
:
  
Main
(
sys
.
argv
)
  
sys
.
exit
(
0
)
