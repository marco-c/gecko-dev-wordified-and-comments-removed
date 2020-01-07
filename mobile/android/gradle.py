from
__future__
import
print_function
import
buildconfig
import
subprocess
from
mozbuild
.
util
import
(
    
ensureParentDir
    
lock_file
)
import
mozpack
.
path
as
mozpath
def
android
(
verb
*
args
)
:
    
lock_path
=
'
{
}
/
gradle
/
mach_android
.
lockfile
'
.
format
(
buildconfig
.
topobjdir
)
    
ensureParentDir
(
lock_path
)
    
lock_instance
=
lock_file
(
lock_path
)
    
try
:
        
cmd
=
[
            
mozpath
.
join
(
buildconfig
.
topsrcdir
'
mach
'
)
            
'
android
'
            
verb
        
]
        
cmd
.
extend
(
args
)
        
subprocess
.
check_call
(
cmd
)
        
return
0
    
finally
:
        
del
lock_instance
def
assemble_app
(
dummy_output_file
*
inputs
)
:
    
return
android
(
'
assemble
-
app
'
)
def
generate_sdk_bindings
(
dummy_output_file
*
args
)
:
    
return
android
(
'
generate
-
sdk
-
bindings
'
*
args
)
