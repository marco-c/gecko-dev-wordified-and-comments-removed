"
"
"
Run
Cargo
for
one
serialized
Rust
build
edge
.
"
"
"
import
argparse
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
from
mozfile
import
json
from
mozshellutil
import
quote
as
shell_quote
from
mozbuild
.
rust_commands
import
(
    
CargoInvocation
    
applies_library_lto
    
cargo_profile_dir
    
compose_cargo_build_edge_argv
    
compose_env
    
load_cargo_spec
)
def
stage_test_libs
(
command
substs
topobjdir
)
:
    
if
command
.
kind
!
=
"
test
"
or
substs
.
get
(
"
OS_ARCH
"
)
=
=
"
Darwin
"
:
        
return
    
bindir
=
Path
(
        
topobjdir
        
substs
.
get
(
"
RUST_TARGET
"
)
        
cargo_profile_dir
(
command
substs
)
        
"
deps
"
    
)
    
bindir
.
mkdir
(
parents
=
True
exist_ok
=
True
)
    
pattern
=
f
"
{
substs
.
get
(
'
DLL_PREFIX
'
)
}
*
{
substs
.
get
(
'
DLL_SUFFIX
'
)
}
"
    
for
lib
in
sorted
(
Path
(
topobjdir
"
dist
"
"
bin
"
)
.
glob
(
pattern
)
)
:
        
shutil
.
copy
(
lib
bindir
)
def
check_networking
(
command
substs
topobjdir
)
:
    
if
(
        
substs
.
get
(
"
OS_ARCH
"
)
!
=
"
Linux
"
        
or
substs
.
get
(
"
MOZ_PROFILE_GENERATE
"
)
        
or
substs
.
get
(
"
RUST_SANCOV_FLAGS
"
)
        
or
substs
.
get
(
"
MOZ_ASAN
"
)
        
or
substs
.
get
(
"
MOZ_TSAN
"
)
        
or
substs
.
get
(
"
MOZ_UBSAN
"
)
        
or
substs
.
get
(
"
MOZ_LTO_RUST_CROSS
"
)
        
or
not
applies_library_lto
(
command
.
kind
command
.
lto
substs
)
    
)
:
        
return
0
    
from
mozbuild
.
action
import
check_binary
    
return
check_binary
.
main
(
[
"
-
-
networking
"
str
(
Path
(
topobjdir
command
.
outputs
[
0
]
)
)
]
)
def
copy_program_pdbs
(
command
topobjdir
)
:
    
for
output
in
command
.
outputs
:
        
program
=
Path
(
topobjdir
output
)
        
crate_pdb
=
program
.
with_name
(
program
.
stem
.
replace
(
"
-
"
"
_
"
)
+
"
.
pdb
"
)
        
program_pdb
=
program
.
with_suffix
(
"
.
pdb
"
)
        
if
crate_pdb
=
=
program_pdb
or
not
crate_pdb
.
exists
(
)
:
            
continue
        
if
(
            
program_pdb
.
exists
(
)
            
and
program_pdb
.
stat
(
)
.
st_mtime
>
=
crate_pdb
.
stat
(
)
.
st_mtime
        
)
:
            
continue
        
shutil
.
copyfile
(
crate_pdb
program_pdb
)
def
main
(
argv
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
Compose
and
run
Cargo
for
a
Rust
build
edge
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
spec
"
        
required
=
True
        
type
=
Path
        
help
=
"
Path
to
the
Cargo
command
spec
of
the
Rust
build
edge
to
run
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
timings
"
action
=
"
store_true
"
help
=
"
Pass
-
-
timings
to
Cargo
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
keep
-
going
"
action
=
"
store_true
"
help
=
"
Pass
-
-
keep
-
going
to
Cargo
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
single
-
job
"
action
=
"
store_true
"
help
=
"
Limit
Cargo
to
one
job
.
"
    
)
    
args
=
parser
.
parse_args
(
argv
)
    
command
substs
topsrcdir
topobjdir
=
load_cargo_spec
(
        
json
.
loads
(
args
.
spec
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
)
    
)
    
stage_test_libs
(
command
substs
topobjdir
)
    
invocation
=
CargoInvocation
.
from_environ
(
os
.
environ
)
    
env
=
compose_env
(
command
substs
os
.
environ
invocation
topsrcdir
topobjdir
)
    
cargo_argv
=
compose_cargo_build_edge_argv
(
        
command
        
substs
        
invocation
        
timings
=
args
.
timings
        
keep_going
=
args
.
keep_going
        
single_job
=
args
.
single_job
    
)
    
if
invocation
.
verbose
:
        
print
(
shell_quote
(
*
cargo_argv
)
flush
=
True
)
    
returncode
=
subprocess
.
run
(
        
cargo_argv
        
env
=
env
        
cwd
=
command
.
working_directory
        
close_fds
=
False
        
check
=
False
    
)
.
returncode
    
if
returncode
=
=
0
:
        
copy_program_pdbs
(
command
topobjdir
)
        
returncode
=
check_networking
(
command
substs
topobjdir
)
    
return
returncode
if
__name__
=
=
"
__main__
"
:
    
sys
.
exit
(
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
)
