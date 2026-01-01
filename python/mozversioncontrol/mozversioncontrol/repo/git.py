import
os
import
platform
import
re
import
shutil
import
stat
import
subprocess
import
sys
import
uuid
from
collections
.
abc
import
Iterator
from
contextlib
import
contextmanager
from
datetime
import
datetime
from
pathlib
import
Path
from
typing
import
Optional
Union
from
mach
.
util
import
(
    
to_optional_path
    
win_to_msys_path
)
from
mozfile
import
which
from
mozpack
.
files
import
FileListFinder
from
packaging
.
version
import
Version
from
mozversioncontrol
.
errors
import
(
    
CannotDeleteFromRootOfRepositoryException
    
MissingVCSExtension
)
from
mozversioncontrol
.
repo
.
base
import
Repository
MINIMUM_GIT_VERSION
=
Version
(
"
2
.
37
"
)
ADD_GIT_CINNABAR_PATH
=
"
"
"
To
add
git
-
cinnabar
to
the
PATH
edit
your
shell
initialization
script
which
may
be
called
{
prefix
}
/
.
bash_profile
or
{
prefix
}
/
.
profile
and
add
the
following
lines
:
    
export
PATH
=
"
{
cinnabar_dir
}
:
PATH
"
Then
restart
your
shell
.
"
"
"
class
GitVersionError
(
Exception
)
:
    
"
"
"
Raised
when
the
installed
git
version
is
too
old
.
"
"
"
    
pass
class
GitRepository
(
Repository
)
:
    
"
"
"
An
implementation
of
Repository
for
Git
repositories
.
"
"
"
    
def
__init__
(
self
path
:
Path
git
=
"
git
"
)
:
        
super
(
)
.
__init__
(
path
tool
=
git
)
    
property
    
def
name
(
self
)
:
        
return
"
git
"
    
property
    
def
head_ref
(
self
)
:
        
return
self
.
_run
(
"
rev
-
parse
"
"
HEAD
"
)
.
strip
(
)
    
def
is_cinnabar_repo
(
self
)
-
>
bool
:
        
"
"
"
Return
True
if
the
repo
is
a
git
-
cinnabar
clone
.
"
"
"
        
try
:
            
self
.
_run
(
                
"
cat
-
file
"
                
"
-
e
"
                
"
2ca566cd74d5d0863ba7ef0529a4f88b2823eb43
^
{
commit
}
"
                
stderr
=
subprocess
.
DEVNULL
            
)
        
except
subprocess
.
CalledProcessError
:
            
output
=
self
.
_run
(
"
for
-
each
-
ref
"
)
            
return
"
refs
/
cinnabar
"
in
output
        
return
False
    
def
get_mozilla_upstream_remotes
(
self
)
-
>
Iterator
[
str
]
:
        
"
"
"
Return
the
Mozilla
-
official
upstream
remotes
for
this
repo
.
"
"
"
        
out
=
self
.
_run
(
"
remote
"
"
-
v
"
)
        
if
not
out
:
            
return
        
remotes
=
out
.
splitlines
(
)
        
if
not
remotes
:
            
return
        
is_cinnabar_repo
=
self
.
is_cinnabar_repo
(
)
        
def
is_official_remote
(
url
:
str
)
-
>
bool
:
            
"
"
"
Determine
if
a
remote
is
official
.
            
Account
for
git
-
cinnabar
remotes
with
hg
.
mozilla
.
org
in
the
name
            
as
well
as
SSH
and
HTTP
remotes
for
Git
-
native
.
            
"
"
"
            
if
(
                
is_cinnabar_repo
                
and
"
hg
.
mozilla
.
org
"
in
url
                
and
not
url
.
endswith
(
(
"
hg
.
mozilla
.
org
/
try
"
"
hg
.
mozilla
.
org
/
try
/
"
)
)
            
)
:
                
return
True
            
return
any
(
                
remote
in
url
                
for
remote
in
(
                    
"
github
.
com
/
mozilla
-
firefox
/
"
                    
"
github
.
com
:
mozilla
-
firefox
/
"
                
)
            
)
        
for
line
in
remotes
:
            
parts
=
line
.
split
(
)
            
if
len
(
parts
)
<
3
:
                
continue
            
name
url
action
*
_
=
parts
            
if
action
!
=
"
(
fetch
)
"
:
                
continue
            
if
is_official_remote
(
url
)
:
                
yield
name
    
def
get_mozilla_remote_args
(
self
)
-
>
list
[
str
]
:
        
"
"
"
Return
a
list
of
-
-
remotes
arguments
to
limit
commits
to
official
remotes
.
"
"
"
        
official_remotes
=
[
            
f
"
-
-
remotes
=
{
remote
}
"
for
remote
in
self
.
get_mozilla_upstream_remotes
(
)
        
]
        
return
official_remotes
if
official_remotes
else
[
"
-
-
remotes
"
]
    
property
    
def
base_ref
(
self
)
:
        
remote_args
=
self
.
get_mozilla_remote_args
(
)
        
refs
=
self
.
_run
(
            
"
rev
-
list
"
"
HEAD
"
"
-
-
topo
-
order
"
"
-
-
boundary
"
"
-
-
not
"
*
remote_args
        
)
.
splitlines
(
)
        
if
refs
:
            
return
refs
[
-
1
]
[
1
:
]
        
return
self
.
head_ref
    
def
base_ref_as_hg
(
self
)
:
        
base_ref
=
self
.
base_ref
        
try
:
            
return
self
.
_run
(
"
cinnabar
"
"
git2hg
"
base_ref
)
.
strip
(
)
        
except
subprocess
.
CalledProcessError
:
            
return
    
def
base_ref_as_commit
(
self
)
:
        
return
self
.
base_ref
    
property
    
def
branch
(
self
)
:
        
branch
=
self
.
_run
(
"
symbolic
-
ref
"
"
-
q
"
"
HEAD
"
return_codes
=
[
0
1
]
)
.
strip
(
)
        
if
not
branch
.
startswith
(
"
refs
/
heads
/
"
)
:
            
return
None
        
return
branch
[
len
(
"
refs
/
heads
/
"
)
:
]
    
property
    
def
has_git_cinnabar
(
self
)
:
        
try
:
            
self
.
_run
(
"
cinnabar
"
"
-
-
version
"
)
        
except
subprocess
.
CalledProcessError
:
            
return
False
        
return
True
    
def
get_commit_time
(
self
)
:
        
return
int
(
self
.
_run
(
"
log
"
"
-
1
"
"
-
-
format
=
%
ct
"
)
.
strip
(
)
)
    
def
sparse_checkout_present
(
self
)
:
        
return
False
    
def
get_user_email
(
self
)
:
        
email
=
self
.
_run
(
"
config
"
"
user
.
email
"
return_codes
=
[
0
1
]
)
        
if
not
email
:
            
return
None
        
return
email
.
strip
(
)
    
def
get_user_name
(
self
)
:
        
name
=
self
.
_run
(
"
config
"
"
user
.
name
"
return_codes
=
[
0
1
]
)
        
if
not
name
:
            
return
None
        
return
name
.
strip
(
)
    
def
get_changed_files
(
self
diff_filter
=
"
ADM
"
mode
=
"
unstaged
"
rev
=
None
)
:
        
assert
all
(
f
.
lower
(
)
in
self
.
_valid_diff_filter
for
f
in
diff_filter
)
        
if
rev
is
None
:
            
cmd
=
[
"
diff
"
]
            
if
mode
=
=
"
staged
"
:
                
cmd
.
append
(
"
-
-
cached
"
)
            
elif
mode
=
=
"
all
"
:
                
cmd
.
append
(
"
HEAD
"
)
        
else
:
            
cmd
=
[
"
diff
-
tree
"
"
-
r
"
"
-
-
no
-
commit
-
id
"
rev
]
        
cmd
.
append
(
"
-
-
name
-
only
"
)
        
cmd
.
append
(
"
-
-
diff
-
filter
=
"
+
diff_filter
.
upper
(
)
)
        
return
self
.
_run
(
*
cmd
)
.
splitlines
(
)
    
def
get_outgoing_files
(
self
diff_filter
=
"
ADM
"
upstream
=
None
)
:
        
assert
all
(
f
.
lower
(
)
in
self
.
_valid_diff_filter
for
f
in
diff_filter
)
        
not_condition
=
upstream
if
upstream
else
"
-
-
remotes
"
        
files
=
self
.
_run
(
            
"
log
"
            
"
-
-
name
-
only
"
            
f
"
-
-
diff
-
filter
=
{
diff_filter
.
upper
(
)
}
"
            
"
-
-
oneline
"
            
"
-
-
topo
-
order
"
            
"
-
-
pretty
=
format
:
"
            
"
HEAD
"
            
"
-
-
not
"
            
not_condition
        
)
.
splitlines
(
)
        
return
[
f
for
f
in
files
if
f
]
    
def
add_remove_files
(
self
*
paths
:
Union
[
str
Path
]
force
:
bool
=
False
)
:
        
if
not
paths
:
            
return
        
paths
=
[
str
(
path
)
for
path
in
paths
]
        
cmd
=
[
"
add
"
]
        
if
force
:
            
cmd
.
append
(
"
-
f
"
)
        
cmd
.
extend
(
paths
)
        
self
.
_run
(
*
cmd
)
    
def
forget_add_remove_files
(
self
*
paths
:
Union
[
str
Path
]
)
:
        
if
not
paths
:
            
return
        
paths
=
[
str
(
path
)
for
path
in
paths
]
        
self
.
_run
(
"
reset
"
*
paths
)
    
def
get_tracked_files_finder
(
self
path
=
None
)
:
        
files
=
[
p
for
p
in
self
.
_run
(
"
ls
-
files
"
"
-
z
"
)
.
split
(
"
\
0
"
)
if
p
]
        
return
FileListFinder
(
files
)
    
def
get_ignored_files_finder
(
self
)
:
        
files
=
[
            
p
            
for
p
in
self
.
_run
(
                
"
ls
-
files
"
"
-
i
"
"
-
o
"
"
-
z
"
"
-
-
exclude
-
standard
"
            
)
.
split
(
"
\
0
"
)
            
if
p
        
]
        
return
FileListFinder
(
files
)
    
def
_translate_exclude_expr
(
self
pattern
)
:
        
if
not
pattern
or
pattern
.
startswith
(
"
#
"
)
:
            
return
None
        
pattern
=
pattern
.
replace
(
"
.
*
"
"
*
*
"
)
        
magics
=
[
"
exclude
"
]
        
if
pattern
.
startswith
(
"
^
"
)
:
            
magics
+
=
[
"
top
"
]
            
pattern
=
pattern
[
1
:
]
        
return
"
:
(
{
}
)
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
magics
)
pattern
)
    
def
diff_stream
(
self
rev
=
None
extensions
=
(
)
exclude_file
=
None
context
=
8
)
:
        
commit_range
=
"
HEAD
"
        
if
rev
:
            
commit_range
=
rev
if
"
.
.
"
in
rev
else
f
"
{
rev
}
~
.
.
{
rev
}
"
        
args
=
[
"
diff
"
"
-
-
no
-
color
"
f
"
-
U
{
context
}
"
commit_range
"
-
-
"
]
        
for
dot_extension
in
extensions
:
            
args
+
=
[
f
"
*
{
dot_extension
}
"
]
        
if
exclude_file
is
not
None
:
            
with
open
(
exclude_file
)
as
exclude_pattern_file
:
                
for
pattern
in
exclude_pattern_file
.
readlines
(
)
:
                    
pattern
=
self
.
_translate_exclude_expr
(
pattern
.
rstrip
(
)
)
                    
if
pattern
is
not
None
:
                        
args
.
append
(
pattern
)
        
return
self
.
_pipefrom
(
*
args
)
    
def
working_directory_clean
(
self
untracked
=
False
ignored
=
False
)
:
        
args
=
[
"
status
"
"
-
-
porcelain
"
]
        
if
untracked
:
            
args
.
append
(
"
-
-
untracked
-
files
=
all
"
)
        
else
:
            
args
.
append
(
"
-
-
untracked
-
files
=
no
"
)
        
if
ignored
:
            
args
.
append
(
"
-
-
ignored
"
)
        
return
not
len
(
self
.
_run
(
*
args
)
.
strip
(
)
)
    
def
clean_directory
(
self
path
:
Union
[
str
Path
]
)
:
        
if
Path
(
self
.
path
)
.
samefile
(
path
)
:
            
raise
CannotDeleteFromRootOfRepositoryException
(
)
        
self
.
_run
(
"
checkout
"
"
-
-
"
str
(
path
)
)
        
self
.
_run
(
"
clean
"
"
-
df
"
str
(
path
)
)
    
def
update
(
self
ref
)
:
        
self
.
_run
(
"
checkout
"
ref
)
    
def
push_to_try
(
        
self
        
message
:
str
        
changed_files
:
dict
[
str
str
]
=
{
}
        
allow_log_capture
:
bool
=
False
    
)
:
        
if
not
self
.
has_git_cinnabar
:
            
raise
MissingVCSExtension
(
"
cinnabar
"
)
        
with
self
.
try_commit
(
message
changed_files
)
as
head
:
            
cmd
=
(
                
str
(
self
.
_tool
)
                
"
-
c
"
                
"
cinnabar
.
data
=
never
"
                
"
push
"
                
"
hg
:
:
ssh
:
/
/
hg
.
mozilla
.
org
/
try
"
                
f
"
+
{
head
}
:
refs
/
heads
/
branches
/
default
/
tip
"
            
)
            
if
allow_log_capture
:
                
self
.
_push_to_try_with_log_capture
(
                    
cmd
                    
{
                        
"
stdout
"
:
subprocess
.
PIPE
                        
"
stderr
"
:
subprocess
.
STDOUT
                        
"
cwd
"
:
self
.
path
                        
"
universal_newlines
"
:
True
                        
"
bufsize
"
:
1
                    
}
                
)
            
else
:
                
subprocess
.
check_call
(
cmd
cwd
=
self
.
path
)
    
def
set_config
(
self
name
value
)
:
        
self
.
_run
(
"
config
"
name
value
)
    
def
get_commits
(
        
self
        
head
:
Optional
[
str
]
=
None
        
limit
:
Optional
[
int
]
=
None
        
follow
:
Optional
[
list
[
str
]
]
=
None
    
)
-
>
list
[
str
]
:
        
"
"
"
Return
a
list
of
commit
SHAs
for
nodes
on
the
current
branch
.
"
"
"
        
remote_args
=
self
.
get_mozilla_remote_args
(
)
        
cmd
=
[
            
"
log
"
            
head
or
"
HEAD
"
            
"
-
-
reverse
"
            
"
-
-
topo
-
order
"
            
"
-
-
not
"
            
*
remote_args
            
"
-
-
pretty
=
%
H
"
        
]
        
if
limit
is
not
None
:
            
cmd
.
append
(
f
"
-
n
{
limit
}
"
)
        
if
follow
is
not
None
:
            
cmd
+
=
[
"
-
-
"
*
follow
]
        
return
self
.
_run
(
*
cmd
)
.
splitlines
(
)
    
def
get_commit_patches
(
self
nodes
:
list
[
str
]
)
-
>
list
[
bytes
]
:
        
"
"
"
Return
the
contents
of
the
patch
node
in
the
VCS
'
standard
format
.
"
"
"
        
return
[
            
self
.
_run
(
"
format
-
patch
"
node
"
-
1
"
"
-
-
always
"
"
-
-
stdout
"
encoding
=
None
)
            
for
node
in
nodes
        
]
    
contextmanager
    
def
try_commit
(
        
self
commit_message
:
str
changed_files
:
Optional
[
dict
[
str
str
]
]
=
None
    
)
:
        
"
"
"
Create
a
temporary
try
commit
as
a
context
manager
.
        
Create
a
new
commit
using
commit_message
as
the
commit
message
.
The
commit
        
may
be
empty
for
example
when
only
including
try
syntax
.
        
changed_files
may
contain
a
dict
of
file
paths
and
their
contents
        
see
stage_changes
.
        
"
"
"
        
current_head
=
self
.
head_ref
        
def
data
(
content
)
:
            
return
f
"
data
{
len
(
content
)
}
\
n
{
content
}
"
        
author
=
self
.
_run
(
"
var
"
"
GIT_AUTHOR_IDENT
"
)
.
strip
(
)
        
committer
=
self
.
_run
(
"
var
"
"
GIT_COMMITTER_IDENT
"
)
.
strip
(
)
        
branch
=
str
(
uuid
.
uuid4
(
)
)
        
fast_import
=
"
\
n
"
.
join
(
            
[
                
f
"
commit
refs
/
machtry
/
{
branch
}
"
                
"
mark
:
1
"
                
f
"
author
{
author
}
"
                
f
"
committer
{
committer
}
"
                
data
(
commit_message
)
                
f
"
from
{
current_head
}
"
                
"
\
n
"
.
join
(
                    
f
"
M
100644
inline
{
path
}
\
n
{
data
(
content
)
}
"
                    
for
path
content
in
(
changed_files
or
{
}
)
.
items
(
)
                
)
                
f
"
reset
refs
/
machtry
/
{
branch
}
"
                
"
from
0000000000000000000000000000000000000000
"
                
"
get
-
mark
:
1
"
                
"
"
            
]
        
)
        
cmd
=
(
str
(
self
.
_tool
)
"
fast
-
import
"
"
-
-
quiet
"
)
        
stdout
=
subprocess
.
check_output
(
            
cmd
            
cwd
=
self
.
path
            
env
=
self
.
_env
            
input
=
fast_import
.
encode
(
"
utf
-
8
"
)
        
)
        
try_head
=
stdout
.
decode
(
"
ascii
"
)
.
strip
(
)
        
yield
try_head
        
self
.
_run
(
"
update
-
ref
"
"
-
m
"
"
mach
try
:
push
"
"
HEAD
"
try_head
current_head
)
        
self
.
_run
(
            
"
update
-
ref
"
            
"
-
m
"
            
"
mach
try
:
restore
"
            
"
HEAD
"
            
current_head
            
try_head
        
)
    
def
get_last_modified_time_for_file
(
self
path
:
Path
)
:
        
"
"
"
Return
last
modified
in
VCS
time
for
the
specified
file
.
"
"
"
        
out
=
self
.
_run
(
"
log
"
"
-
1
"
"
-
-
format
=
%
ad
"
"
-
-
date
=
iso
"
path
)
        
return
datetime
.
strptime
(
out
.
strip
(
)
"
%
Y
-
%
m
-
%
d
%
H
:
%
M
:
%
S
%
z
"
)
    
def
get_config_key_value
(
self
key
:
str
)
:
        
try
:
            
value
=
subprocess
.
check_output
(
                
[
self
.
_tool
"
config
"
"
-
-
get
"
key
]
                
stderr
=
subprocess
.
DEVNULL
                
text
=
True
            
)
.
strip
(
)
            
return
value
or
None
        
except
subprocess
.
CalledProcessError
:
            
return
None
    
def
set_config_key_value
(
self
key
:
str
value
:
str
)
:
        
"
"
"
        
Set
a
git
config
value
in
the
given
repo
and
print
        
logging
output
indicating
what
was
done
.
        
"
"
"
        
subprocess
.
check_call
(
            
[
self
.
_tool
"
config
"
key
value
]
            
cwd
=
str
(
self
.
path
)
        
)
        
print
(
f
'
Set
git
config
:
"
{
key
}
=
{
value
}
"
'
)
    
def
configure
(
self
state_dir
:
Path
update_only
:
bool
=
False
)
:
        
"
"
"
Run
the
Git
configuration
steps
.
"
"
"
        
if
not
update_only
:
            
print
(
"
Configuring
git
.
.
.
"
)
            
match
=
re
.
search
(
                
r
"
(
\
d
+
\
.
\
d
+
\
.
\
d
+
)
"
                
subprocess
.
check_output
(
                    
[
self
.
_tool
"
-
-
version
"
]
universal_newlines
=
True
                
)
            
)
            
if
not
match
:
                
raise
Exception
(
"
Could
not
find
git
version
"
)
            
git_version
=
Version
(
match
.
group
(
1
)
)
            
moz_automation
=
os
.
environ
.
get
(
"
MOZ_AUTOMATION
"
)
            
if
not
moz_automation
:
                
if
git_version
<
MINIMUM_GIT_VERSION
:
                    
raise
GitVersionError
(
                        
f
"
Your
version
of
git
(
{
git_version
}
)
is
too
old
.
"
                        
f
"
Please
upgrade
to
at
least
version
'
{
MINIMUM_GIT_VERSION
}
'
to
ensure
"
                        
"
full
compatibility
and
performance
.
"
                    
)
            
system
=
platform
.
system
(
)
            
self
.
set_config_key_value
(
key
=
"
core
.
untrackedCache
"
value
=
"
true
"
)
            
if
system
=
=
"
Windows
"
:
                
self
.
set_config_key_value
(
key
=
"
core
.
fscache
"
value
=
"
true
"
)
                
self
.
set_config_key_value
(
key
=
"
core
.
fsmonitor
"
value
=
"
true
"
)
            
elif
system
=
=
"
Darwin
"
:
                
self
.
set_config_key_value
(
key
=
"
core
.
fsmonitor
"
value
=
"
true
"
)
            
elif
system
=
=
"
Linux
"
:
                
subprocess
.
run
(
                    
[
self
.
_tool
"
config
"
"
-
-
unset
-
all
"
"
core
.
fsmonitor
"
]
                    
cwd
=
str
(
self
.
path
)
                    
check
=
False
                
)
                
print
(
"
Unset
git
config
:
core
.
fsmonitor
"
)
                
self
.
_ensure_watchman
(
)
        
if
self
.
is_cinnabar_repo
(
)
:
            
cinnabar_dir
=
str
(
self
.
_update_git_cinnabar
(
state_dir
)
)
            
cinnabar
=
to_optional_path
(
which
(
"
git
-
cinnabar
"
)
)
            
if
not
cinnabar
:
                
if
"
MOZILLABUILD
"
in
os
.
environ
:
                    
cinnabar_dir
=
win_to_msys_path
(
cinnabar_dir
)
                    
print
(
                        
ADD_GIT_CINNABAR_PATH
.
format
(
                            
prefix
=
"
%
USERPROFILE
%
"
cinnabar_dir
=
cinnabar_dir
                        
)
                    
)
                
else
:
                    
print
(
                        
ADD_GIT_CINNABAR_PATH
.
format
(
                            
prefix
=
"
~
"
cinnabar_dir
=
cinnabar_dir
                        
)
                    
)
    
def
_update_git_cinnabar
(
self
root_state_dir
:
Path
)
:
        
"
"
"
Update
git
tools
hooks
and
extensions
"
"
"
        
cinnabar_dir
=
root_state_dir
/
"
git
-
cinnabar
"
        
cinnabar_exe
=
cinnabar_dir
/
"
git
-
cinnabar
"
        
if
sys
.
platform
.
startswith
(
(
"
win32
"
"
msys
"
)
)
:
            
cinnabar_exe
=
cinnabar_exe
.
with_suffix
(
"
.
exe
"
)
        
start_over
=
cinnabar_dir
.
exists
(
)
and
not
cinnabar_exe
.
exists
(
)
        
if
cinnabar_exe
.
exists
(
)
:
            
try
:
                
with
cinnabar_exe
.
open
(
"
rb
"
)
as
fh
:
                    
start_over
=
fh
.
read
(
2
)
=
=
b
"
#
!
"
            
except
Exception
:
                
start_over
=
True
        
if
start_over
:
            
def
onerror
(
func
path
exc
)
:
                
if
func
=
=
os
.
unlink
:
                    
os
.
chmod
(
path
stat
.
S_IRWXU
)
                    
func
(
path
)
                
else
:
                    
raise
exc
            
shutil
.
rmtree
(
str
(
cinnabar_dir
)
onerror
=
onerror
)
        
exists
=
cinnabar_exe
.
exists
(
)
        
if
exists
:
            
try
:
                
print
(
"
\
nUpdating
git
-
cinnabar
.
.
.
"
)
                
subprocess
.
check_call
(
[
str
(
cinnabar_exe
)
"
self
-
update
"
]
)
            
except
subprocess
.
CalledProcessError
as
e
:
                
print
(
e
)
        
if
not
exists
or
cinnabar_exe
.
stat
(
)
.
st_size
=
=
0
:
            
import
ssl
            
from
urllib
.
request
import
urlopen
            
import
certifi
            
if
not
cinnabar_dir
.
exists
(
)
:
                
cinnabar_dir
.
mkdir
(
)
            
cinnabar_url
=
"
https
:
/
/
github
.
com
/
glandium
/
git
-
cinnabar
/
"
            
download_py
=
cinnabar_dir
/
"
download
.
py
"
            
with
open
(
download_py
"
wb
"
)
as
fh
:
                
context
=
ssl
.
create_default_context
(
cafile
=
certifi
.
where
(
)
)
                
shutil
.
copyfileobj
(
                    
urlopen
(
f
"
{
cinnabar_url
}
/
raw
/
master
/
download
.
py
"
context
=
context
)
                    
fh
                
)
            
try
:
                
subprocess
.
check_call
(
                    
[
sys
.
executable
str
(
download_py
)
]
cwd
=
str
(
cinnabar_dir
)
                
)
            
except
subprocess
.
CalledProcessError
as
e
:
                
print
(
e
)
            
finally
:
                
download_py
.
unlink
(
)
        
return
cinnabar_dir
    
def
_ensure_watchman
(
self
)
:
        
watchman
=
which
(
"
watchman
"
)
        
if
not
watchman
:
            
print
(
                
"
watchman
is
not
installed
.
Please
install
watchman
and
"
                
"
re
-
run
.
/
mach
vcs
-
setup
to
enable
faster
git
commands
.
"
            
)
            
return
        
print
(
"
Ensuring
watchman
is
properly
configured
.
.
.
"
)
        
hooks
=
Path
(
            
subprocess
.
check_output
(
                
[
                    
self
.
_tool
                    
"
rev
-
parse
"
                    
"
-
-
path
-
format
=
absolute
"
                    
"
-
-
git
-
path
"
                    
"
hooks
"
                
]
                
cwd
=
str
(
self
.
path
)
                
universal_newlines
=
True
            
)
.
strip
(
)
        
)
        
watchman_config
=
hooks
/
"
query
-
watchman
"
        
watchman_sample
=
hooks
/
"
fsmonitor
-
watchman
.
sample
"
        
if
not
watchman_sample
.
exists
(
)
:
            
print
(
                
"
watchman
is
installed
but
the
sample
hook
(
expected
here
:
"
                
f
"
{
watchman_sample
}
)
was
not
found
.
Please
acquire
it
and
copy
"
                
f
"
it
into
.
git
/
hooks
/
and
re
-
run
.
/
mach
vcs
-
setup
.
"
            
)
            
return
        
if
not
watchman_config
.
exists
(
)
:
            
copy_cmd
=
[
                
"
cp
"
                
watchman_sample
                
watchman_config
            
]
            
print
(
f
"
Copying
{
watchman_sample
}
to
{
watchman_config
}
"
)
            
subprocess
.
check_call
(
copy_cmd
cwd
=
str
(
self
.
path
)
)
        
self
.
set_config_key_value
(
key
=
"
core
.
fsmonitor
"
value
=
str
(
watchman_config
)
)
    
def
get_patches_after_ref
(
self
base_ref
)
-
>
str
:
        
"
"
"
        
Retrieve
git
format
-
patch
style
patches
of
all
commits
that
occurred
        
after
base_ref
.
        
"
"
"
        
return
self
.
_run
(
"
format
-
patch
"
f
"
{
base_ref
}
.
.
HEAD
"
"
-
-
stdout
"
)
    
def
get_patch_for_uncommitted_changes
(
        
self
message
:
str
=
"
[
PATCH
]
Uncommitted
changes
"
date
:
datetime
=
None
    
)
-
>
str
:
        
"
"
"
        
Generate
a
git
format
-
patch
style
patch
of
all
uncommitted
changes
in
        
the
working
directory
.
        
"
"
"
        
diff
=
self
.
_run
(
"
diff
"
"
-
-
no
-
color
"
"
HEAD
"
)
        
if
not
diff
.
strip
(
)
:
            
return
"
"
        
if
not
date
:
            
date
=
datetime
.
now
(
)
        
name
=
self
.
get_user_name
(
)
        
email
=
self
.
get_user_email
(
)
        
formatted_date
=
date
.
strftime
(
"
%
a
%
b
%
d
%
H
:
%
M
:
%
S
%
Y
%
z
"
)
        
patch
=
[
            
"
From
0000000000000000000000000000000000000000
Mon
Sep
17
00
:
00
:
00
2001
"
            
f
"
From
:
{
name
}
<
{
email
}
>
"
            
f
"
Date
:
{
formatted_date
}
"
            
f
"
Subject
:
{
message
}
"
            
"
\
n
-
-
-
\
n
"
            
diff
        
]
        
return
"
\
n
"
.
join
(
patch
)
