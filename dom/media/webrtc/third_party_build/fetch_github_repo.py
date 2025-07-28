import
argparse
import
os
import
shutil
from
run_operations
import
run_git
run_shell
def
fetch_repo
(
github_path
force_fetch
tar_path
)
:
    
capture_output
=
False
    
if
force_fetch
and
os
.
path
.
exists
(
github_path
)
:
        
print
(
f
"
Removing
existing
repo
:
{
github_path
}
"
)
        
shutil
.
rmtree
(
github_path
)
    
if
not
os
.
path
.
exists
(
github_path
)
:
        
if
os
.
path
.
exists
(
tar_path
)
:
            
print
(
"
Using
tar
file
to
reconstitute
repo
"
)
            
cmd
=
f
"
cd
{
os
.
path
.
dirname
(
github_path
)
}
;
tar
-
-
extract
-
-
gunzip
-
-
file
=
{
os
.
path
.
basename
(
tar_path
)
}
"
            
run_shell
(
cmd
capture_output
)
        
else
:
            
print
(
"
Cloning
github
repo
"
)
            
run_shell
(
                
f
"
git
clone
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
{
github_path
}
"
                
capture_output
            
)
    
run_git
(
"
git
checkout
master
"
github_path
)
    
stdout_lines
=
run_git
(
        
"
git
config
-
-
local
-
-
get
-
all
remote
.
origin
.
fetch
"
github_path
    
)
    
if
len
(
stdout_lines
)
=
=
1
:
        
print
(
"
Fetching
upstream
branch
-
heads
"
)
        
run_git
(
            
"
git
config
-
-
local
-
-
add
remote
.
origin
.
fetch
+
refs
/
branch
-
heads
/
*
:
refs
/
remotes
/
branch
-
heads
/
*
"
            
github_path
        
)
        
run_git
(
"
git
fetch
"
github_path
)
    
else
:
        
print
(
"
Upstream
remote
branch
-
heads
already
configured
"
)
    
run_git
(
"
git
show
branch
-
heads
/
5059
"
github_path
)
    
run_git
(
"
git
config
-
-
local
core
.
autocrlf
false
"
github_path
)
    
run_git
(
"
git
fetch
-
-
all
"
github_path
)
    
if
not
os
.
path
.
exists
(
tar_path
)
:
        
print
(
"
Creating
tar
file
for
quicker
restore
"
)
        
cmd
=
f
"
cd
{
os
.
path
.
dirname
(
github_path
)
}
;
tar
-
-
create
-
-
gzip
-
-
file
=
{
os
.
path
.
basename
(
tar_path
)
}
{
os
.
path
.
basename
(
github_path
)
}
"
        
run_shell
(
cmd
capture_output
)
if
__name__
=
=
"
__main__
"
:
    
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
force
-
fetch
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
force
rebuild
an
existing
repo
directory
"
    
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
f
"
name
of
tar
file
(
defaults
to
{
default_tar_name
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
    
args
=
parser
.
parse_args
(
)
    
fetch_repo
(
        
args
.
repo_path
        
args
.
force_fetch
        
os
.
path
.
join
(
args
.
state_path
args
.
tar_name
)
    
)
