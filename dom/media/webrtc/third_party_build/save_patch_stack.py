import
argparse
import
atexit
import
os
import
re
import
shutil
import
sys
from
run_operations
import
run_git
run_hg
run_shell
error_help
=
None
script_name
=
os
.
path
.
basename
(
__file__
)
atexit
.
register
def
early_exit_handler
(
)
:
    
print
(
f
"
*
*
*
ERROR
*
*
*
{
script_name
}
did
not
complete
successfully
"
)
    
if
error_help
is
not
None
:
        
print
(
error_help
)
def
build_repo_name_from_path
(
input_dir
)
:
    
output_dir
=
os
.
path
.
dirname
(
os
.
path
.
relpath
(
input_dir
)
)
    
if
os
.
path
.
commonpath
(
[
output_dir
"
third_party
"
]
)
!
=
"
"
:
        
output_dir
=
os
.
path
.
relpath
(
output_dir
"
third_party
"
)
    
return
output_dir
def
write_patch_files_with_prefix
(
    
github_path
    
patch_directory
    
start_commit_sha
    
end_commit_sha
    
prefix
)
:
    
cmd
=
f
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
no
-
signature
-
-
output
-
directory
{
patch_directory
}
{
start_commit_sha
}
.
.
{
end_commit_sha
}
"
    
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
r
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
f
"
{
prefix
}
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
def
write_prestack_and_standard_patches
(
    
github_path
    
patch_directory
    
start_commit_sha
    
end_commit_sha
)
:
    
cmd
=
f
"
cd
{
github_path
}
;
git
log
-
-
oneline
{
start_commit_sha
}
.
.
{
end_commit_sha
}
"
    
stdout_lines
=
run_shell
(
cmd
)
    
base_commit_summary
=
"
Bug
1376873
-
Rollup
of
local
modifications
"
    
found_lines
=
[
s
for
s
in
stdout_lines
if
base_commit_summary
in
s
]
    
base_commit_sha
=
found_lines
[
0
]
.
split
(
"
"
)
[
0
]
    
print
(
f
"
Found
base_commit_sha
:
{
base_commit_sha
}
"
)
    
write_patch_files_with_prefix
(
        
github_path
patch_directory
f
"
{
start_commit_sha
}
"
f
"
{
base_commit_sha
}
^
"
"
p
"
    
)
    
write_patch_files_with_prefix
(
        
github_path
patch_directory
f
"
{
base_commit_sha
}
^
"
f
"
{
end_commit_sha
}
"
"
s
"
    
)
def
save_patch_stack
(
    
github_path
    
github_branch
    
patch_directory
    
state_directory
    
target_branch_head
    
bug_number
    
no_pre_stack
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
f
"
git
merge
-
base
{
github_branch
}
{
target_branch_head
}
"
    
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
    
if
no_pre_stack
:
        
write_patch_files_with_prefix
(
            
github_path
patch_directory
f
"
{
merge_base
}
"
f
"
{
github_branch
}
"
"
"
        
)
    
else
:
        
write_prestack_and_standard_patches
(
            
github_path
            
patch_directory
            
f
"
{
merge_base
}
"
            
f
"
{
github_branch
}
"
        
)
    
run_shell
(
f
"
sed
-
i
'
.
bak
'
-
e
'
1d
'
{
patch_directory
}
/
*
.
patch
"
)
    
run_shell
(
f
"
rm
{
patch_directory
}
/
*
.
patch
.
bak
"
)
    
if
state_directory
!
=
"
"
:
        
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
f
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
patch_directory
}
"
    
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
f
"
hg
rm
{
'
'
.
join
(
stdout_lines
)
}
"
        
run_hg
(
cmd
)
    
cmd
=
f
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
patch_directory
}
"
    
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
f
"
hg
add
{
'
'
.
join
(
stdout_lines
)
}
"
        
run_hg
(
cmd
)
    
cmd
=
f
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
patch_directory
}
"
    
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
f
"
Updating
{
len
(
stdout_lines
)
}
files
in
{
patch_directory
}
"
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
                
f
"
hg
commit
-
-
message
'
Bug
{
bug_number
}
-
"
                
f
"
updated
{
build_repo_name_from_path
(
patch_directory
)
}
"
                
f
"
patch
stack
'
{
patch_directory
}
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
    
default_script_dir
=
"
dom
/
media
/
webrtc
/
third_party_build
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
f
"
path
to
save
patches
(
defaults
to
{
default_patch_dir
}
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
state
-
path
"
        
default
=
default_state_dir
        
help
=
f
"
path
to
state
directory
(
defaults
to
{
default_state_dir
}
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
script
-
path
"
        
default
=
default_script_dir
        
help
=
f
"
path
to
script
directory
(
defaults
to
{
default_script_dir
}
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
    
parser
.
add_argument
(
        
"
-
-
no
-
pre
-
stack
"
        
action
=
"
store_true
"
        
default
=
False
        
help
=
"
don
'
t
look
for
pre
-
stack
/
standard
patches
simply
write
the
patches
all
sequentially
"
    
)
    
parser
.
add_argument
(
        
"
-
-
skip
-
startup
-
sanity
"
        
action
=
"
store_true
"
        
default
=
False
        
help
=
"
skip
checking
for
clean
repo
and
doing
the
initial
verify
vendoring
"
    
)
    
args
=
parser
.
parse_args
(
)
    
if
not
args
.
skip_startup_sanity
:
        
error_help
=
(
            
"
There
are
modified
or
untracked
files
in
the
mercurial
repo
.
\
n
"
            
f
"
Please
start
with
a
clean
repo
before
running
{
script_name
}
"
        
)
        
stdout_lines
=
run_hg
(
"
hg
status
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
            
sys
.
exit
(
1
)
        
error_help
=
(
            
f
"
No
moz
-
libwebrtc
github
repo
found
at
{
args
.
repo_path
}
\
n
"
            
f
"
Please
run
restore_patch_stack
.
py
before
running
{
script_name
}
"
        
)
        
if
not
os
.
path
.
exists
(
args
.
repo_path
)
:
            
sys
.
exit
(
1
)
        
error_help
=
None
        
print
(
"
Verifying
vendoring
before
saving
patch
-
stack
.
.
.
"
)
        
run_shell
(
f
"
bash
{
args
.
script_path
}
/
verify_vendoring
.
sh
"
False
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
        
args
.
no_pre_stack
    
)
    
atexit
.
unregister
(
early_exit_handler
)
