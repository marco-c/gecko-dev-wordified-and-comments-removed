import
os
import
subprocess
import
buildconfig
import
mozpack
.
path
as
mozpath
import
toml
def
_get_crate_name
(
crate_path
)
:
    
try
:
        
with
open
(
mozpath
.
join
(
crate_path
"
Cargo
.
toml
"
)
encoding
=
"
utf
-
8
"
)
as
f
:
            
return
toml
.
load
(
f
)
[
"
package
"
]
[
"
name
"
]
    
except
Exception
:
        
return
mozpath
.
basename
(
crate_path
)
CARGO_LOCK
=
mozpath
.
join
(
buildconfig
.
topsrcdir
"
Cargo
.
lock
"
)
CARGO_TOML
=
mozpath
.
join
(
buildconfig
.
topsrcdir
"
Cargo
.
toml
"
)
def
_run_process
(
args
)
:
    
env
=
os
.
environ
.
copy
(
)
    
env
[
"
CARGO
"
]
=
str
(
buildconfig
.
substs
[
"
CARGO
"
]
)
    
env
[
"
RUSTC
"
]
=
str
(
buildconfig
.
substs
[
"
RUSTC
"
]
)
    
p
=
subprocess
.
Popen
(
        
args
env
=
env
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
encoding
=
"
utf
-
8
"
    
)
    
stdout
stderr
=
p
.
communicate
(
)
    
if
p
.
returncode
!
=
0
:
        
print
(
stdout
)
        
print
(
stderr
)
    
return
(
stdout
p
.
returncode
)
def
generate_metadata
(
output
cargo_config
)
:
    
args
=
[
        
buildconfig
.
substs
[
"
CARGO
"
]
        
"
metadata
"
        
"
-
-
all
-
features
"
        
"
-
-
format
-
version
"
        
"
1
"
        
"
-
-
manifest
-
path
"
        
CARGO_TOML
    
]
    
if
not
buildconfig
.
substs
.
get
(
"
JS_STANDALONE
"
)
:
        
args
.
append
(
"
-
-
frozen
"
)
    
stdout
returncode
=
_run_process
(
args
)
    
if
returncode
!
=
0
:
        
return
returncode
    
if
stdout
:
        
output
.
write
(
stdout
)
    
return
set
(
[
CARGO_LOCK
CARGO_TOML
]
)
def
generate
(
output
metadata_path
cbindgen_crate_path
*
in_tree_dependencies
)
:
    
stdout
returncode
=
_run_process
(
[
        
buildconfig
.
substs
[
"
CBINDGEN
"
]
        
buildconfig
.
topsrcdir
        
"
-
-
lockfile
"
        
CARGO_LOCK
        
"
-
-
crate
"
        
_get_crate_name
(
cbindgen_crate_path
)
        
"
-
-
metadata
"
        
metadata_path
        
"
-
-
cpp
-
compat
"
    
]
)
    
if
returncode
!
=
0
:
        
return
returncode
    
if
stdout
:
        
output
.
write
(
stdout
)
    
deps
=
set
(
)
    
deps
.
add
(
CARGO_LOCK
)
    
deps
.
add
(
mozpath
.
join
(
cbindgen_crate_path
"
cbindgen
.
toml
"
)
)
    
for
directory
in
in_tree_dependencies
+
(
cbindgen_crate_path
)
:
        
for
path
dirs
files
in
os
.
walk
(
directory
)
:
            
for
file
in
files
:
                
if
os
.
path
.
splitext
(
file
)
[
1
]
=
=
"
.
rs
"
:
                    
deps
.
add
(
mozpath
.
join
(
path
file
)
)
    
return
deps
