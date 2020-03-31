from
__future__
import
print_function
import
buildconfig
import
mozpack
.
path
as
mozpath
import
os
import
subprocess
import
pytoml
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
)
as
f
:
            
return
pytoml
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
def
_generate
(
output
cbindgen_crate_path
metadata_crate_path
              
in_tree_dependencies
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
'
CARGO
'
]
=
str
(
buildconfig
.
substs
[
'
CARGO
'
]
)
    
env
[
'
RUSTC
'
]
=
str
(
buildconfig
.
substs
[
'
RUSTC
'
]
)
    
p
=
subprocess
.
Popen
(
[
        
buildconfig
.
substs
[
'
CBINDGEN
'
]
        
metadata_crate_path
        
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
cpp
-
compat
"
    
]
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
p
.
returncode
    
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
def
generate
(
output
cbindgen_crate_path
*
in_tree_dependencies
)
:
    
metadata_crate_path
=
mozpath
.
join
(
buildconfig
.
topsrcdir
                                       
"
toolkit
"
"
library
"
"
rust
"
)
    
return
_generate
(
output
cbindgen_crate_path
metadata_crate_path
                     
in_tree_dependencies
)
def
generate_with_same_crate
(
output
cbindgen_crate_path
                             
*
in_tree_dependencies
)
:
    
return
_generate
(
output
cbindgen_crate_path
cbindgen_crate_path
                     
in_tree_dependencies
)
