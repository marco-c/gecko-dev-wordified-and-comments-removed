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
"
Removing
existing
repo
:
{
}
"
.
format
(
github_path
)
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
"
cd
{
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
}
"
.
format
(
                
os
.
path
.
dirname
(
github_path
)
os
.
path
.
basename
(
tar_path
)
            
)
            
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
                
"
git
clone
https
:
/
/
github
.
com
/
mozilla
/
libwebrtc
{
}
"
.
format
(
github_path
)
                
capture_output
            
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
list
"
github_path
)
    
stdout_lines
=
[
        
path
for
path
in
stdout_lines
if
re
.
findall
(
"
^
remote
.
upstream
.
url
.
*
"
path
)
    
]
    
if
len
(
stdout_lines
)
=
=
0
:
        
print
(
"
Fetching
upstream
"
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
        
run_git
(
            
"
git
remote
add
upstream
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
"
github_path
        
)
        
run_git
(
"
git
fetch
upstream
"
github_path
)
        
run_git
(
"
git
merge
upstream
/
master
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
(
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
)
already
configured
"
        
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
upstream
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
upstream
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
upstream
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
"
cd
{
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
}
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
dirname
(
github_path
)
            
os
.
path
.
basename
(
tar_path
)
            
os
.
path
.
basename
(
github_path
)
        
)
        
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
