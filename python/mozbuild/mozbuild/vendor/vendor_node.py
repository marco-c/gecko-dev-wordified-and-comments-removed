import
hashlib
import
logging
import
os
import
shutil
import
subprocess
from
pathlib
import
Path
from
mozfile
import
json
from
mozbuild
.
base
import
MozbuildObject
from
mozbuild
.
nodeutil
import
find_node_executable
PNPM_ISOLATION
=
[
"
-
-
ignore
-
scripts
"
"
-
-
ignore
-
pnpmfile
"
]
VENDOR_INPUTS
=
(
"
package
.
json
"
"
pnpm
-
workspace
.
yaml
"
"
pnpm
-
lock
.
yaml
"
)
def
hash_inputs
(
vendor_dir
)
:
    
hasher
=
hashlib
.
sha256
(
)
    
for
name
in
VENDOR_INPUTS
:
        
path
=
vendor_dir
/
name
        
if
path
.
exists
(
)
:
            
hasher
.
update
(
path
.
read_bytes
(
)
)
    
return
hasher
.
hexdigest
(
)
class
VendorNode
(
MozbuildObject
)
:
    
def
vendor
(
self
add
=
None
remove
=
None
force
=
False
ignore_modified
=
False
)
:
        
vendor_dir
=
Path
(
self
.
topsrcdir
)
/
"
third_party
"
/
"
node
"
        
hash_file
=
vendor_dir
/
"
vendor
-
inputs
.
hash
"
        
node_modules
=
vendor_dir
/
"
node_modules
"
        
if
not
ignore_modified
:
            
modified
=
sorted
(
                
p
                
for
p
in
self
.
repository
.
get_changed_files
(
"
ADM
"
)
                
if
p
.
replace
(
os
.
sep
"
/
"
)
.
startswith
(
"
third_party
/
node
/
"
)
            
)
            
if
modified
:
                
self
.
log
(
                    
logging
.
ERROR
                    
"
modified_files
"
                    
{
}
                    
"
"
"
You
have
uncommitted
changes
to
the
following
files
:
{
files
}
Please
commit
or
stash
these
changes
before
vendoring
or
re
-
run
with
-
-
ignore
-
modified
.
"
"
"
.
format
(
files
=
"
\
n
"
.
join
(
modified
)
)
                
)
                
return
1
        
node
_
=
find_node_executable
(
)
        
if
not
node
:
            
self
.
log
(
                
logging
.
ERROR
                
"
node_missing
"
                
{
}
                
"
Could
not
find
a
node
executable
.
Run
mach
bootstrap
.
"
            
)
            
return
1
        
from
mozbuild
.
bootstrap
import
bootstrap_toolchain
        
pnpm
=
bootstrap_toolchain
(
"
pnpm
/
bin
/
pnpm
.
cjs
"
)
        
if
not
pnpm
:
            
self
.
log
(
                
logging
.
ERROR
                
"
pnpm_missing
"
                
{
}
                
"
Could
not
find
or
bootstrap
pnpm
.
"
            
)
            
return
1
        
expected_version
=
_expected_pnpm_version
(
vendor_dir
)
        
if
expected_version
:
            
found_version
=
_pnpm_version
(
node
pnpm
)
            
if
found_version
!
=
expected_version
:
                
self
.
log
(
                    
logging
.
ERROR
                    
"
pnpm_version
"
                    
{
}
                    
f
"
third_party
/
node
/
package
.
json
asks
for
pnpm
"
                    
f
"
{
expected_version
}
but
{
pnpm
}
is
{
found_version
}
.
"
                
)
                
return
1
        
for
package
in
add
or
[
]
:
            
subprocess
.
check_call
(
                
[
node
pnpm
"
add
"
"
-
-
save
-
exact
"
]
+
PNPM_ISOLATION
+
[
package
]
                
cwd
=
vendor_dir
            
)
        
for
package
in
remove
or
[
]
:
            
subprocess
.
check_call
(
                
[
node
pnpm
"
remove
"
]
+
PNPM_ISOLATION
+
[
package
]
cwd
=
vendor_dir
            
)
        
install_flags
=
PNPM_ISOLATION
+
[
            
"
-
-
node
-
linker
=
hoisted
"
            
"
-
-
config
.
confirmModulesPurge
=
false
"
        
]
        
lock_file
=
vendor_dir
/
"
pnpm
-
lock
.
yaml
"
        
if
force
and
lock_file
.
exists
(
)
:
            
lock_file
.
unlink
(
)
        
resolve
=
[
node
pnpm
"
install
"
"
-
-
lockfile
-
only
"
]
+
install_flags
        
try
:
            
subprocess
.
check_call
(
resolve
cwd
=
vendor_dir
)
        
except
subprocess
.
CalledProcessError
as
e
:
            
self
.
log
(
                
logging
.
ERROR
                
"
resolve_failed
"
                
{
}
                
"
pnpm
could
not
resolve
the
lock
file
as
it
stands
.
If
a
policy
"
                
"
in
pnpm
-
workspace
.
yaml
rejects
a
version
it
pins
re
-
run
with
"
                
"
-
-
force
to
resolve
from
scratch
.
"
            
)
            
return
e
.
returncode
        
new_hash
=
hash_inputs
(
vendor_dir
)
        
if
node_modules
.
exists
(
)
:
            
shutil
.
rmtree
(
node_modules
)
        
try
:
            
subprocess
.
check_call
(
                
[
node
pnpm
"
install
"
"
-
-
frozen
-
lockfile
"
]
+
install_flags
                
cwd
=
vendor_dir
            
)
        
except
subprocess
.
CalledProcessError
as
e
:
            
self
.
log
(
                
logging
.
ERROR
                
"
install_failed
"
                
{
}
                
"
pnpm
could
not
install
from
the
lock
file
.
third_party
/
node
/
"
                
"
node_modules
was
removed
first
restore
it
from
version
control
.
"
            
)
            
return
e
.
returncode
        
hash_file
.
write_text
(
f
"
{
new_hash
}
\
n
"
newline
=
"
\
n
"
)
        
self
.
repository
.
add_remove_files
(
vendor_dir
)
        
return
0
def
_expected_pnpm_version
(
vendor_dir
)
:
    
manifest
=
json
.
loads
(
(
vendor_dir
/
"
package
.
json
"
)
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
    
name
_
version
=
(
manifest
.
get
(
"
packageManager
"
)
or
"
"
)
.
partition
(
"
"
)
    
return
version
if
name
=
=
"
pnpm
"
else
None
def
_pnpm_version
(
node
pnpm
)
:
    
return
subprocess
.
check_output
(
[
node
pnpm
"
-
-
version
"
]
text
=
True
)
.
strip
(
)
