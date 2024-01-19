import
argparse
import
os
import
re
import
shutil
import
sys
from
fetch_github_repo
import
fetch_repo
from
run_operations
import
get_last_line
run_git
run_hg
run_shell
def
restore_patch_stack
(
    
github_path
    
github_branch
    
patch_directory
    
state_directory
    
tar_name
    
clone_protocol
)
:
    
stdout_lines
=
run_hg
(
"
hg
status
third_party
/
libwebrtc
"
)
    
if
len
(
stdout_lines
)
!
=
0
:
        
print
(
"
There
are
modified
or
untracked
files
under
third_party
/
libwebrtc
"
)
        
print
(
"
Please
cleanup
the
repo
under
third_party
/
libwebrtc
before
running
"
)
        
print
(
os
.
path
.
basename
(
__file__
)
)
        
sys
.
exit
(
1
)
    
print
(
"
fetch
repo
"
)
    
fetch_repo
(
        
github_path
clone_protocol
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
    
print
(
"
clear
no
-
op
-
cherry
-
pick
-
msg
files
"
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
    
print
(
        
"
lookup
latest
vendored
commit
from
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
    
print
(
        
"
checkout
the
previous
vendored
commit
(
{
}
)
with
proper
branch
name
"
.
format
(
            
last_vendored_commit
        
)
    
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
    
print
(
"
Please
run
the
following
command
to
verify
the
state
of
the
patch
-
stack
:
"
)
    
print
(
"
bash
dom
/
media
/
webrtc
/
third_party_build
/
verify_vendoring
.
sh
"
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
    
parser
.
add_argument
(
        
"
-
-
clone
-
protocol
"
        
choices
=
[
"
https
"
"
ssh
"
]
        
default
=
"
https
"
        
help
=
"
Use
either
https
or
ssh
to
clone
the
git
repo
(
ignored
if
tar
file
exists
)
"
    
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
        
args
.
clone_protocol
    
)
