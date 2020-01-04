import
os
from
mozbuild
import
shellutil
def
check_top_objdir
(
topobjdir
)
:
    
top_make
=
os
.
path
.
join
(
topobjdir
'
Makefile
'
)
    
if
not
os
.
path
.
exists
(
top_make
)
:
        
print
(
'
Your
tree
has
not
been
built
yet
.
Please
run
'
            
'
|
mach
build
|
with
no
arguments
.
'
)
        
return
False
    
return
True
def
get_build_vars
(
directory
cmd
)
:
    
build_vars
=
{
}
    
def
on_line
(
line
)
:
        
elements
=
[
s
.
strip
(
)
for
s
in
line
.
split
(
'
=
'
1
)
]
        
if
len
(
elements
)
!
=
2
:
            
return
        
build_vars
[
elements
[
0
]
]
=
elements
[
1
]
    
try
:
        
old_logger
=
cmd
.
log_manager
.
replace_terminal_handler
(
None
)
        
cmd
.
_run_make
(
directory
=
directory
target
=
'
showbuild
'
log
=
False
                
print_directory
=
False
allow_parallel
=
False
silent
=
True
                
line_handler
=
on_line
)
    
finally
:
        
cmd
.
log_manager
.
replace_terminal_handler
(
old_logger
)
    
return
build_vars
def
sanitize_cflags
(
flags
)
:
    
sanitized
=
[
]
    
saw_xclang
=
False
    
for
flag
in
flags
:
        
if
flag
=
=
'
-
Xclang
'
:
            
saw_xclang
=
True
        
elif
saw_xclang
:
            
saw_xclang
=
False
        
else
:
            
sanitized
.
append
(
flag
)
    
return
sanitized
