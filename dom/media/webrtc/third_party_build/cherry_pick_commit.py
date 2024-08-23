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
filter_git_changes
import
filter_git_changes
from
restore_patch_stack
import
restore_patch_stack
from
run_operations
import
(
    
get_last_line
    
run_git
    
run_hg
    
run_shell
    
update_resume_state
)
from
vendor_and_commit
import
vendor_and_commit
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
write_commit_message_file
(
    
commit_message_filename
    
github_path
    
github_sha
    
bug_number
    
reviewers
)
:
    
print
(
f
"
commit_message_filename
:
{
commit_message_filename
}
"
)
    
print
(
f
"
github_path
:
{
github_path
}
"
)
    
print
(
f
"
github_sha
:
{
github_sha
}
"
)
    
print
(
f
"
bug_number
:
{
bug_number
}
"
)
    
cmd
=
"
git
show
-
-
format
=
%
H
-
-
no
-
patch
{
}
"
.
format
(
github_sha
)
    
stdout_lines
=
run_git
(
cmd
github_path
)
    
github_long_sha
=
stdout_lines
[
0
]
    
print
(
f
"
github_long_sha
:
{
github_long_sha
}
"
)
    
cmd
=
"
git
show
-
-
format
=
%
s
%
n
%
n
%
b
-
-
no
-
patch
{
}
"
.
format
(
github_sha
)
    
github_commit_msg_lines
=
run_git
(
cmd
github_path
)
    
with
open
(
commit_message_filename
"
w
"
)
as
ofile
:
        
ofile
.
write
(
            
"
Bug
{
}
-
Cherry
-
pick
upstream
libwebrtc
commit
{
}
r
?
{
}
"
.
format
(
                
bug_number
github_sha
reviewers
            
)
        
)
        
ofile
.
write
(
"
\
n
"
)
        
ofile
.
write
(
"
\
n
"
)
        
ofile
.
write
(
            
"
Upstream
commit
:
https
:
/
/
webrtc
.
googlesource
.
com
/
src
/
+
/
{
}
"
.
format
(
                
github_long_sha
            
)
        
)
        
ofile
.
write
(
"
\
n
"
)
        
for
line
in
github_commit_msg_lines
:
            
ofile
.
write
(
"
{
}
"
.
format
(
line
)
)
            
ofile
.
write
(
"
\
n
"
)
def
cherry_pick_commit
(
    
commit_message_filename
    
github_path
    
github_sha
)
:
    
print
(
f
"
commit_message_filename
:
{
commit_message_filename
}
"
)
    
print
(
f
"
github_path
:
{
github_path
}
"
)
    
print
(
f
"
github_sha
:
{
github_sha
}
"
)
    
cmd
=
"
git
cherry
-
pick
-
-
no
-
commit
{
}
"
.
format
(
github_sha
)
    
run_git
(
cmd
github_path
)
    
cmd
=
"
git
commit
-
-
file
{
}
"
.
format
(
os
.
path
.
abspath
(
commit_message_filename
)
)
    
run_git
(
cmd
github_path
)
def
write_noop_tracking_file
(
    
github_sha
    
bug_number
)
:
    
noop_basename
=
"
{
}
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
"
.
format
(
github_sha
)
    
noop_filename
=
os
.
path
.
join
(
args
.
state_path
noop_basename
)
    
print
(
f
"
noop_filename
:
{
noop_filename
}
"
)
    
with
open
(
noop_filename
"
w
"
)
as
ofile
:
        
ofile
.
write
(
"
We
cherry
-
picked
this
in
bug
{
}
"
.
format
(
bug_number
)
)
        
ofile
.
write
(
"
\
n
"
)
    
shutil
.
copy
(
noop_filename
args
.
patch_path
)
    
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
os
.
path
.
join
(
args
.
patch_path
noop_basename
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
amend
{
}
"
.
format
(
os
.
path
.
join
(
args
.
patch_path
noop_basename
)
)
    
run_hg
(
cmd
)
if
__name__
=
=
"
__main__
"
:
    
default_target_dir
=
"
third_party
/
libwebrtc
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
    
default_log_dir
=
"
.
moz
-
fast
-
forward
/
logs
"
    
default_tmp_dir
=
"
.
moz
-
fast
-
forward
/
tmp
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
    
default_repo_dir
=
"
.
moz
-
fast
-
forward
/
moz
-
libwebrtc
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
Cherry
-
pick
upstream
libwebrtc
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
target
-
path
"
        
default
=
default_target_dir
        
help
=
"
target
path
for
vendoring
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
default_target_dir
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
log
-
path
"
        
default
=
default_log_dir
        
help
=
"
path
to
log
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
default_log_dir
)
    
)
    
parser
.
add_argument
(
        
"
-
-
tmp
-
path
"
        
default
=
default_tmp_dir
        
help
=
"
path
to
tmp
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
default_tmp_dir
)
    
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
"
path
to
script
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
default_script_dir
)
    
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
        
default
=
default_repo_dir
        
help
=
"
path
to
moz
-
libwebrtc
repo
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
default_repo_dir
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
commit
-
sha
"
        
required
=
True
        
help
=
"
sha
of
commit
to
examine
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
commit
-
bug
-
number
"
        
type
=
int
        
required
=
True
        
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
reviewers
"
        
required
=
True
        
help
=
'
reviewers
for
cherry
-
picked
patch
(
like
"
ng
mjf
"
)
'
    
)
    
parser
.
add_argument
(
        
"
-
-
abort
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
abort
an
interrupted
cherry
-
pick
"
    
)
    
parser
.
add_argument
(
        
"
-
-
continue
"
        
dest
=
"
cont
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
continue
an
interrupted
cherry
-
pick
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
restore
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
to
skip
restoring
the
patch
-
stack
if
it
is
already
restored
and
verified
"
    
)
    
args
=
parser
.
parse_args
(
)
    
atexit
.
register
(
early_exit_handler
)
    
commit_message_filename
=
os
.
path
.
join
(
args
.
tmp_path
"
cherry
-
pick
-
commit_msg
.
txt
"
)
    
resume_state_filename
=
os
.
path
.
join
(
args
.
state_path
"
cherry_pick_commit
.
resume
"
)
    
resume_state
=
"
"
    
if
os
.
path
.
exists
(
resume_state_filename
)
:
        
resume_state
=
get_last_line
(
resume_state_filename
)
.
strip
(
)
    
print
(
f
"
resume_state
:
'
{
resume_state
}
'
"
)
    
error_help
=
"
-
-
abort
or
-
-
continue
flags
are
not
allowed
when
not
in
resume
state
"
    
if
len
(
resume_state
)
=
=
0
and
(
args
.
abort
or
args
.
cont
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
    
error_help
=
"
cherry
-
pick
in
progress
use
-
-
abort
or
-
-
continue
"
    
if
len
(
resume_state
)
!
=
0
and
not
args
.
abort
and
not
args
.
cont
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
    
if
args
.
abort
:
        
run_hg
(
"
hg
revert
-
-
all
"
)
        
run_hg
(
"
hg
purge
{
}
"
.
format
(
args
.
target_path
)
)
        
if
not
(
resume_state
=
=
"
resume2
"
or
resume_state
=
=
"
resume3
"
)
:
            
stdout_lines
=
run_hg
(
"
hg
log
-
-
template
{
desc
|
firstline
}
\
n
-
r
.
"
)
            
print
(
"
stdout_lines
before
filter
:
{
}
"
.
format
(
stdout_lines
)
)
            
stdout_lines
=
[
                
line
                
for
line
in
stdout_lines
                
if
re
.
findall
(
"
Cherry
-
pick
upstream
libwebrtc
commit
"
line
)
            
]
            
print
(
"
looking
for
commit
:
{
}
"
.
format
(
stdout_lines
)
)
            
if
len
(
stdout_lines
)
>
0
:
                
cmd
=
"
hg
prune
.
"
                
print
(
"
calling
'
{
}
'
"
.
format
(
cmd
)
)
                
run_hg
(
cmd
)
        
print
(
"
restoring
patch
stack
"
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
            
"
https
"
        
)
        
print
(
"
reset
resume
file
"
)
        
update_resume_state
(
"
"
resume_state_filename
)
        
print
(
"
after
resetting
resume
file
"
)
        
atexit
.
unregister
(
early_exit_handler
)
        
sys
.
exit
(
0
)
    
error_help
=
(
        
f
"
There
are
modified
or
untracked
files
under
{
args
.
target_path
}
.
\
n
"
        
f
"
Please
cleanup
the
repo
under
{
args
.
target_path
}
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
f
"
hg
status
{
args
.
target_path
}
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
None
    
if
len
(
resume_state
)
=
=
0
:
        
update_resume_state
(
"
resume2
"
resume_state_filename
)
        
if
args
.
skip_restore
is
False
:
            
print
(
"
restoring
patch
stack
"
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
                
"
https
"
            
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
    
cmd
=
f
"
git
rev
-
parse
-
-
short
{
args
.
commit_sha
}
"
    
args
.
commit_sha
=
run_git
(
cmd
args
.
repo_path
)
[
0
]
    
if
len
(
resume_state
)
=
=
0
or
resume_state
=
=
"
resume2
"
:
        
resume_state
=
"
"
        
update_resume_state
(
"
resume3
"
resume_state_filename
)
        
print
(
"
verifying
patch
stack
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
    
if
len
(
resume_state
)
=
=
0
or
resume_state
=
=
"
resume3
"
:
        
resume_state
=
"
"
        
update_resume_state
(
"
resume4
"
resume_state_filename
)
        
print
(
"
-
-
-
-
-
-
-
"
)
        
print
(
f
"
-
-
-
-
-
-
-
write
commit
message
file
{
commit_message_filename
}
"
)
        
print
(
"
-
-
-
-
-
-
-
"
)
        
write_commit_message_file
(
            
commit_message_filename
            
args
.
repo_path
            
args
.
commit_sha
            
args
.
commit_bug_number
            
args
.
reviewers
        
)
    
if
len
(
resume_state
)
=
=
0
or
resume_state
=
=
"
resume4
"
:
        
resume_state
=
"
"
        
update_resume_state
(
"
resume5
"
resume_state_filename
)
        
print
(
"
-
-
-
-
-
-
-
"
)
        
print
(
f
"
-
-
-
-
-
-
-
cherry
-
pick
{
args
.
commit_sha
}
into
{
args
.
repo_path
}
"
)
        
print
(
"
-
-
-
-
-
-
-
"
)
        
full_commit_message_filename
=
os
.
path
.
abspath
(
commit_message_filename
)
        
error_help
=
(
            
f
"
The
cherry
-
pick
operation
of
{
args
.
commit_sha
}
has
failed
.
\
n
"
            
"
To
fix
this
issue
you
will
need
to
jump
to
the
github
\
n
"
            
f
"
repo
at
{
args
.
repo_path
}
.
\
n
"
            
"
Please
resolve
all
the
cherry
-
pick
conflicts
and
commit
the
changes
\
n
"
            
"
using
:
\
n
"
            
f
"
git
commit
-
-
file
{
full_commit_message_filename
}
\
n
"
            
"
\
n
"
            
"
When
the
github
cherry
-
pick
is
complete
resume
running
this
\
n
"
            
f
"
script
(
{
script_name
}
)
"
        
)
        
cherry_pick_commit
(
            
commit_message_filename
            
args
.
repo_path
            
args
.
commit_sha
        
)
        
error_help
=
None
    
if
len
(
resume_state
)
=
=
0
or
resume_state
=
=
"
resume5
"
:
        
resume_state
=
"
"
        
update_resume_state
(
"
resume6
"
resume_state_filename
)
        
print
(
"
-
-
-
-
-
-
-
"
)
        
print
(
f
"
-
-
-
-
-
-
-
vendor
from
{
args
.
repo_path
}
"
)
        
print
(
"
-
-
-
-
-
-
-
"
)
        
error_help
=
(
            
f
"
Vendoring
the
newly
cherry
-
picked
git
commit
(
{
args
.
commit_sha
}
)
has
failed
.
\
n
"
            
"
The
mercurial
repo
is
in
an
unknown
state
.
This
failure
is
\
n
"
            
"
rare
and
thus
makes
it
difficult
to
provide
definitive
guidance
.
\
n
"
            
"
In
essence
the
current
failing
command
is
:
\
n
"
            
f
"
.
/
mach
python
{
args
.
script_path
}
/
vendor_and_commit
.
py
\
\
\
n
"
            
f
"
-
-
script
-
path
{
args
.
script_path
}
\
\
\
n
"
            
f
"
-
-
repo
-
path
{
args
.
repo_path
}
\
\
\
n
"
            
f
"
-
-
branch
{
args
.
branch
}
\
\
\
n
"
            
f
"
-
-
commit
-
sha
{
args
.
commit_sha
}
\
\
\
n
"
            
f
"
-
-
target
-
path
{
args
.
target_path
}
\
\
\
n
"
            
f
"
-
-
state
-
path
{
args
.
state_path
}
\
\
\
n
"
            
f
"
-
-
log
-
path
{
args
.
log_path
}
\
\
\
n
"
            
f
"
-
-
commit
-
msg
-
path
{
commit_message_filename
}
\
n
"
            
"
\
n
"
            
"
Additional
guidance
may
be
in
the
terminal
output
above
.
Resolve
\
n
"
            
"
issues
encountered
by
vendor_and_commit
.
py
followed
by
re
-
running
\
n
"
            
"
vendor_and_commit
.
py
to
resume
/
complete
its
processing
.
After
\
n
"
            
"
vendor_and_commit
.
py
completes
successfully
resume
running
\
n
"
            
f
"
this
script
(
{
script_name
}
)
"
        
)
        
vendor_and_commit
(
            
args
.
script_path
            
args
.
repo_path
            
args
.
branch
            
args
.
commit_sha
            
args
.
target_path
            
args
.
state_path
            
args
.
log_path
            
commit_message_filename
        
)
        
error_help
=
None
    
if
len
(
resume_state
)
=
=
0
or
resume_state
=
=
"
resume6
"
:
        
resume_state
=
"
"
        
update_resume_state
(
"
resume7
"
resume_state_filename
)
        
error_help
=
(
            
"
Reverting
change
to
'
third_party
/
libwebrtc
/
README
.
mozilla
'
\
n
"
            
"
has
failed
.
The
cherry
-
pick
commit
should
not
modify
\
n
"
            
"
'
third_party
/
libwebrtc
/
README
.
mozilla
'
.
If
necessary
\
n
"
            
"
manually
revert
changes
to
'
third_party
/
libwebrtc
/
README
.
mozilla
'
\
n
"
            
f
"
and
re
-
run
{
script_name
}
\
n
"
            
"
to
complete
the
cherry
-
pick
processing
.
"
        
)
        
cmd
=
"
hg
revert
-
r
tip
^
third_party
/
libwebrtc
/
README
.
mozilla
"
        
run_hg
(
cmd
)
        
cmd
=
"
hg
amend
"
        
run_hg
(
cmd
)
        
error_help
=
None
    
if
len
(
resume_state
)
=
=
0
or
resume_state
=
=
"
resume7
"
:
        
resume_state
=
"
"
        
update_resume_state
(
"
resume8
"
resume_state_filename
)
        
cmd
=
"
hg
status
-
-
change
tip
-
-
exclude
'
*
*
/
README
.
*
'
"
        
stdout_lines
=
run_shell
(
cmd
)
        
print
(
"
Mercurial
changes
:
\
n
{
}
"
.
format
(
stdout_lines
)
)
        
hg_file_change_cnt
=
len
(
stdout_lines
)
        
git_paths_changed
=
filter_git_changes
(
args
.
repo_path
args
.
commit_sha
None
)
        
print
(
"
github
changes
:
\
n
{
}
"
.
format
(
git_paths_changed
)
)
        
git_file_change_cnt
=
len
(
git_paths_changed
)
        
error_help
=
(
            
f
"
Vendoring
the
cherry
-
pick
of
commit
{
args
.
commit_sha
}
has
failed
due
to
mismatched
\
n
"
            
f
"
changed
file
counts
between
mercurial
(
{
hg_file_change_cnt
}
)
and
git
(
{
git_file_change_cnt
}
)
.
\
n
"
            
"
This
may
be
because
the
mozilla
patch
-
stack
was
not
verified
after
\
n
"
            
"
running
restore_patch_stack
.
py
.
After
reconciling
the
changes
in
\
n
"
            
f
"
the
newly
committed
mercurial
patch
please
re
-
run
{
script_name
}
to
complete
\
n
"
            
"
the
cherry
-
pick
processing
.
"
        
)
        
if
hg_file_change_cnt
!
=
git_file_change_cnt
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
    
if
len
(
resume_state
)
=
=
0
or
resume_state
=
=
"
resume8
"
:
        
resume_state
=
"
"
        
update_resume_state
(
"
"
resume_state_filename
)
        
print
(
"
-
-
-
-
-
-
-
"
)
        
print
(
"
-
-
-
-
-
-
-
write
the
noop
tracking
file
"
)
        
print
(
"
-
-
-
-
-
-
-
"
)
        
write_noop_tracking_file
(
args
.
commit_sha
args
.
commit_bug_number
)
    
atexit
.
unregister
(
early_exit_handler
)
