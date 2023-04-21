import
argparse
import
os
import
re
import
shutil
from
run_operations
import
run_git
run_hg
run_shell
def
save_patch_stack
(
    
github_path
    
github_branch
    
patch_directory
    
state_directory
    
target_branch_head
    
bug_number
)
:
    
files_to_remove
=
os
.
listdir
(
patch_directory
)
    
for
file
in
files_to_remove
:
        
os
.
remove
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
)
    
cmd
=
"
git
merge
-
base
{
}
{
}
"
.
format
(
github_branch
target_branch_head
)
    
stdout_lines
=
run_git
(
cmd
github_path
)
    
merge_base
=
stdout_lines
[
0
]
    
cmd
=
"
git
format
-
patch
-
-
keep
-
subject
-
-
output
-
directory
{
}
{
}
.
.
{
}
"
.
format
(
        
patch_directory
merge_base
github_branch
    
)
    
run_git
(
cmd
github_path
)
    
patches_to_rename
=
os
.
listdir
(
patch_directory
)
    
for
file
in
patches_to_rename
:
        
shortened_name
=
re
.
sub
(
"
^
(
\
d
\
d
\
d
\
d
)
-
.
*
\
.
patch
"
"
\
\
1
.
patch
"
file
)
        
os
.
rename
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
            
os
.
path
.
join
(
patch_directory
shortened_name
)
        
)
    
run_shell
(
"
sed
-
i
'
'
-
e
'
1d
'
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
state_directory
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
state_directory
file
)
patch_directory
)
    
cmd
=
"
hg
status
-
-
no
-
status
-
-
deleted
{
}
"
.
format
(
patch_directory
)
    
stdout_lines
=
run_hg
(
cmd
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
        
cmd
=
"
hg
rm
{
}
"
.
format
(
"
"
.
join
(
stdout_lines
)
)
        
run_hg
(
cmd
)
    
cmd
=
"
hg
status
-
-
no
-
status
-
-
unknown
{
}
"
.
format
(
patch_directory
)
    
stdout_lines
=
run_hg
(
cmd
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
        
cmd
=
"
hg
add
{
}
"
.
format
(
"
"
.
join
(
stdout_lines
)
)
        
run_hg
(
cmd
)
    
cmd
=
"
hg
status
-
-
added
-
-
removed
-
-
modified
{
}
"
.
format
(
patch_directory
)
    
stdout_lines
=
run_hg
(
cmd
)
    
if
(
len
(
stdout_lines
)
)
!
=
0
:
        
print
(
"
Updating
{
}
files
in
{
}
"
.
format
(
len
(
stdout_lines
)
patch_directory
)
)
        
if
bug_number
is
None
:
            
run_hg
(
"
hg
amend
"
)
        
else
:
            
run_shell
(
                
"
hg
commit
-
-
message
'
Bug
{
}
-
updated
libwebrtc
patch
stack
'
"
.
format
(
                    
bug_number
                
)
            
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
    
parser
=
argparse
.
ArgumentParser
(
        
description
=
"
Save
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
target
-
branch
-
head
"
        
required
=
True
        
help
=
"
target
branch
head
for
fast
-
forward
should
match
MOZ_TARGET_UPSTREAM_BRANCH_HEAD
in
config_env
"
    
)
    
parser
.
add_argument
(
        
"
-
-
separate
-
commit
-
bug
-
number
"
        
type
=
int
        
help
=
"
integer
Bugzilla
number
(
example
:
1800920
)
if
provided
will
write
patch
stack
as
separate
commit
"
    
)
    
args
=
parser
.
parse_args
(
)
    
save_patch_stack
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
target_branch_head
        
args
.
separate_commit_bug_number
    
)
