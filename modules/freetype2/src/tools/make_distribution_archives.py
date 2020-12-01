"
"
"
Generate
distribution
archives
for
a
given
FreeType
2
release
.
"
"
"
from
__future__
import
print_function
import
argparse
import
atexit
import
os
import
shutil
import
subprocess
import
sys
import
tempfile
_TOP_DIR
=
os
.
path
.
abspath
(
os
.
path
.
join
(
__file__
"
.
.
"
"
.
.
"
"
.
.
"
)
)
_SCRIPT_DIR
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
join
(
_TOP_DIR
"
builds
"
"
meson
"
"
"
)
)
def
get_cmd_output
(
cmd
cwd
=
None
)
:
    
"
"
"
Run
a
command
and
return
its
output
as
a
string
.
"
"
"
    
if
cwd
is
not
None
:
        
out
=
subprocess
.
check_output
(
cmd
cwd
=
cwd
)
    
else
:
        
out
=
subprocess
.
check_output
(
cmd
)
    
return
out
.
decode
(
"
utf
-
8
"
)
.
rstrip
(
)
def
is_git_dir_clean
(
git_dir
)
:
    
"
"
"
Return
True
iff
|
git_dir
|
is
a
git
directory
in
clean
state
.
"
"
"
    
out
=
get_cmd_output
(
[
"
git
"
"
status
"
"
-
-
porcelain
"
]
cwd
=
git_dir
)
    
return
len
(
out
)
=
=
0
def
main
(
)
:
    
parser
=
argparse
.
ArgumentParser
(
description
=
__doc__
)
    
parser
.
add_argument
(
        
"
-
-
source_dir
"
default
=
_TOP_DIR
help
=
"
Source
directory
path
.
"
    
)
    
parser
.
add_argument
(
        
"
-
-
version
"
        
help
=
(
            
"
Specify
alternate
FreeType
version
(
it
is
otherwise
extracted
"
            
"
from
current
sources
by
default
)
.
"
        
)
    
)
    
parser
.
add_argument
(
        
"
-
-
gnu
-
config
-
dir
"
        
help
=
(
            
"
Path
of
input
directory
containing
recent
config
.
guess
and
"
            
"
config
.
sub
files
from
GNU
config
.
"
        
)
    
)
    
parser
.
add_argument
(
        
"
-
-
build
-
dir
"
        
help
=
"
Specify
build
directory
.
Only
used
for
debugging
this
script
.
"
    
)
    
parser
.
add_argument
(
        
"
-
-
ignore
-
clean
-
check
"
        
action
=
"
store_true
"
        
help
=
(
            
"
Do
not
check
for
a
clean
source
git
repository
.
Only
used
for
"
            
"
debugging
this
script
.
"
        
)
    
)
    
parser
.
add_argument
(
        
"
output_dir
"
help
=
"
Output
directory
for
generated
archives
.
"
    
)
    
args
=
parser
.
parse_args
(
)
    
git_dir
=
args
.
source_dir
if
args
.
source_dir
else
_TOP_DIR
    
if
not
args
.
ignore_clean_check
and
not
is_git_dir_clean
(
git_dir
)
:
        
sys
.
stderr
.
write
(
            
"
ERROR
:
Your
git
repository
is
not
in
a
clean
state
:
%
s
\
n
"
            
%
git_dir
        
)
        
return
1
    
if
args
.
version
:
        
version
=
args
.
version
    
else
:
        
version
=
get_cmd_output
(
            
[
                
sys
.
executable
                
os
.
path
.
join
(
_SCRIPT_DIR
"
extract_freetype_version
.
py
"
)
                
os
.
path
.
join
(
_TOP_DIR
"
include
"
"
freetype
"
"
freetype
.
h
"
)
            
]
        
)
    
if
args
.
build_dir
:
        
build_dir
=
args
.
build_dir
        
if
not
os
.
path
.
exists
(
build_dir
)
:
            
os
.
makedirs
(
build_dir
)
        
else
:
            
for
item
in
os
.
listdir
(
build_dir
)
:
                
file_path
=
os
.
path
.
join
(
build_dir
item
)
                
if
os
.
path
.
isdir
(
file_path
)
:
                    
shutil
.
rmtree
(
file_path
)
                
else
:
                    
os
.
unlink
(
file_path
)
    
else
:
        
build_dir
=
tempfile
.
mkdtemp
(
prefix
=
"
freetype
-
dist
-
"
)
        
def
clean_build_dir
(
)
:
            
shutil
.
rmtree
(
build_dir
)
        
atexit
.
register
(
clean_build_dir
)
    
source_files
=
[
        
f
        
for
f
in
get_cmd_output
(
[
"
git
"
"
ls
-
files
"
]
cwd
=
git_dir
)
.
split
(
"
\
n
"
)
        
if
os
.
path
.
basename
(
f
)
not
in
(
"
.
gitignore
"
"
.
mailmap
"
)
    
]
    
freetype_dir
=
"
freetype
-
"
+
version
    
tmp_src_dir
=
os
.
path
.
join
(
build_dir
freetype_dir
)
    
os
.
makedirs
(
tmp_src_dir
)
    
for
src
in
source_files
:
        
dst
=
os
.
path
.
join
(
tmp_src_dir
src
)
        
dst_dir
=
os
.
path
.
dirname
(
dst
)
        
if
not
os
.
path
.
exists
(
dst_dir
)
:
            
os
.
makedirs
(
dst_dir
)
        
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
git_dir
src
)
dst
)
    
subprocess
.
check_call
(
[
"
/
bin
/
sh
"
"
autogen
.
sh
"
]
cwd
=
tmp_src_dir
)
    
shutil
.
rmtree
(
        
os
.
path
.
join
(
tmp_src_dir
"
builds
"
"
unix
"
"
autom4te
.
cache
"
)
    
)
    
if
args
.
gnu_config_dir
:
        
for
f
in
(
"
config
.
guess
"
"
config
.
sub
"
)
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
args
.
gnu_config_dir
f
)
                
os
.
path
.
join
(
tmp_src_dir
"
builds
"
"
unix
"
f
)
            
)
    
subprocess
.
check_call
(
        
[
            
sys
.
executable
            
os
.
path
.
join
(
_SCRIPT_DIR
"
generate_reference_docs
.
py
"
)
            
"
-
-
input
-
dir
"
            
tmp_src_dir
            
"
-
-
version
"
            
version
            
"
-
-
output
-
dir
"
            
os
.
path
.
join
(
tmp_src_dir
"
docs
"
)
        
]
    
)
    
shutil
.
rmtree
(
os
.
path
.
join
(
tmp_src_dir
"
docs
"
"
markdown
"
)
)
    
os
.
unlink
(
os
.
path
.
join
(
tmp_src_dir
"
docs
"
"
mkdocs
.
yml
"
)
)
    
freetype_tar
=
freetype_dir
+
"
.
tar
"
    
subprocess
.
check_call
(
        
[
"
tar
"
"
-
H
"
"
ustar
"
"
-
chf
"
freetype_tar
freetype_dir
]
        
cwd
=
build_dir
    
)
    
subprocess
.
check_call
(
        
[
"
gzip
"
"
-
9
"
"
-
-
keep
"
freetype_tar
]
cwd
=
build_dir
    
)
    
subprocess
.
check_call
(
[
"
xz
"
"
-
-
keep
"
freetype_tar
]
cwd
=
build_dir
)
    
ftwinversion
=
"
ft
"
+
"
"
.
join
(
version
.
split
(
"
.
"
)
)
    
subprocess
.
check_call
(
        
[
"
zip
"
"
-
qlr9
"
ftwinversion
+
"
.
zip
"
freetype_dir
]
cwd
=
build_dir
    
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
output_dir
)
:
        
os
.
makedirs
(
args
.
output_dir
)
    
for
f
in
(
        
freetype_tar
+
"
.
gz
"
        
freetype_tar
+
"
.
xz
"
        
ftwinversion
+
"
.
zip
"
    
)
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
build_dir
f
)
os
.
path
.
join
(
args
.
output_dir
f
)
        
)
    
return
0
if
__name__
=
=
"
__main__
"
:
    
sys
.
exit
(
main
(
)
)
