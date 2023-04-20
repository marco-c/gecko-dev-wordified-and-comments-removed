import
os
import
subprocess
import
tempfile
def
main
(
output_fd
def_file
llvm_dlltool
*
llvm_dlltool_args
)
:
    
(
tmp_fd
tmp_output
)
=
tempfile
.
mkstemp
(
)
    
os
.
close
(
tmp_fd
)
    
try
:
        
cmd
=
[
llvm_dlltool
]
        
cmd
.
extend
(
llvm_dlltool_args
)
        
cmd
+
=
[
"
-
d
"
def_file
"
-
l
"
tmp_output
]
        
subprocess
.
check_call
(
cmd
)
        
with
open
(
tmp_output
"
rb
"
)
as
tmplib
:
            
output_fd
.
write
(
tmplib
.
read
(
)
)
    
finally
:
        
os
.
remove
(
tmp_output
)
