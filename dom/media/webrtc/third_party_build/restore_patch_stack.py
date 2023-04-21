import
argparse
import
os
import
re
import
shutil
from
fetch_github_repo
import
fetch_repo
from
run_operations
import
run_git
run_shell
def
get_last_line
(
file_path
)
:
    
with
open
(
file_path
"
rb
"
)
as
f
:
        
try
:
            
f
.
seek
(
-
2
os
.
SEEK_END
)
            
while
f
.
read
(
1
)
!
=
b
"
\
n
"
:
                
f
.
seek
(
-
2
os
.
SEEK_CUR
)
        
except
OSError
:
            
f
.
seek
(
0
)
        
return
f
.
readline
(
)
.
decode
(
)
.
strip
(
)
def
restore_patch_stack
(
    
github_path
github_branch
patch_directory
state_directory
tar_name
)
:
    
fetch_repo
(
github_path
True
os
.
path
.
join
(
state_directory
tar_name
)
)
    
run_shell
(
"
rm
{
}
/
*
.
no
-
op
-
cherry
-
pick
-
msg
|
|
true
"
.
format
(
state_directory
)
)
    
file
=
os
.
path
.
abspath
(
"
third_party
/
libwebrtc
/
README
.
moz
-
ff
-
commit
"
)
    
last_vendored_commit
=
get_last_line
(
file
)
    
cmd
=
"
git
checkout
-
b
{
}
{
}
"
.
format
(
github_branch
last_vendored_commit
)
    
run_git
(
cmd
github_path
)
    
print
(
"
Restoring
patch
stack
"
)
    
run_shell
(
"
cd
{
}
&
&
git
am
{
}
/
*
.
patch
"
.
format
(
github_path
patch_directory
)
)
    
no_op_files
=
[
        
path
        
for
path
in
os
.
listdir
(
patch_directory
)
        
if
re
.
findall
(
"
.
*
no
-
op
-
cherry
-
pick
-
msg
"
path
)
    
]
    
for
file
in
no_op_files
:
        
shutil
.
copy
(
os
.
path
.
join
(
patch_directory
file
)
state_directory
)
if
__name__
=
=
"
__main__
"
:
    
default_patch_dir
=
"
third_party
/
libwebrtc
/
moz
-
patch
-
stack
"
    
default_state_dir
=
"
.
moz
-
fast
-
forward
"
    
default_tar_name
=
"
moz
-
libwebrtc
.
tar
.
gz
"
    
parser
=
argparse
.
ArgumentParser
(
        
description
=
"
Restore
moz
-
libwebrtc
github
patch
stack
"
    
)
    
parser
.
add_argument
(
        
"
-
-
repo
-
path
"
        
required
=
True
        
help
=
"
path
to
libwebrtc
repo
"
    
)
    
parser
.
add_argument
(
        
"
-
-
branch
"
        
default
=
"
mozpatches
"
        
help
=
"
moz
-
libwebrtc
branch
(
defaults
to
mozpatches
)
"
    
)
    
parser
.
add_argument
(
        
"
-
-
patch
-
path
"
        
default
=
default_patch_dir
        
help
=
"
path
to
save
patches
(
defaults
to
{
}
)
"
.
format
(
default_patch_dir
)
    
)
    
parser
.
add_argument
(
        
"
-
-
tar
-
name
"
        
default
=
default_tar_name
        
help
=
"
name
of
tar
file
(
defaults
to
{
}
)
"
.
format
(
default_tar_name
)
    
)
    
parser
.
add_argument
(
        
"
-
-
state
-
path
"
        
default
=
default_state_dir
        
help
=
"
path
to
state
directory
(
defaults
to
{
}
)
"
.
format
(
default_state_dir
)
    
)
    
args
=
parser
.
parse_args
(
)
    
restore_patch_stack
(
        
args
.
repo_path
        
args
.
branch
        
os
.
path
.
abspath
(
args
.
patch_path
)
        
args
.
state_path
        
args
.
tar_name
    
)
