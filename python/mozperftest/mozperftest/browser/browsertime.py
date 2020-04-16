import
collections
import
json
import
os
import
stat
import
sys
import
re
import
shutil
from
mozbuild
.
util
import
mkdir
import
mozpack
.
path
as
mozpath
from
mozperftest
.
browser
.
noderunner
import
NodeRunner
from
mozperftest
.
utils
import
host_platform
AUTOMATION
=
"
MOZ_AUTOMATION
"
in
os
.
environ
BROWSERTIME_SRC_ROOT
=
os
.
path
.
dirname
(
__file__
)
PILLOW_VERSION
=
"
6
.
0
.
0
"
PYSSIM_VERSION
=
"
0
.
4
"
host_fetches
=
{
    
"
darwin
"
:
{
        
"
ffmpeg
"
:
{
            
"
type
"
:
"
static
-
url
"
            
"
url
"
:
"
https
:
/
/
github
.
com
/
ncalexan
/
geckodriver
/
releases
/
download
/
v0
.
24
.
0
-
android
/
ffmpeg
-
4
.
1
.
1
-
macos64
-
static
.
zip
"
            
"
path
"
:
"
ffmpeg
-
4
.
1
.
1
-
macos64
-
static
"
        
}
    
}
    
"
linux64
"
:
{
        
"
ffmpeg
"
:
{
            
"
type
"
:
"
static
-
url
"
            
"
url
"
:
"
https
:
/
/
github
.
com
/
ncalexan
/
geckodriver
/
releases
/
download
/
v0
.
24
.
0
-
android
/
ffmpeg
-
4
.
1
.
4
-
i686
-
static
.
tar
.
xz
"
            
"
path
"
:
"
ffmpeg
-
4
.
1
.
4
-
i686
-
static
"
        
}
    
}
    
"
win64
"
:
{
        
"
ffmpeg
"
:
{
            
"
type
"
:
"
static
-
url
"
            
"
url
"
:
"
https
:
/
/
github
.
com
/
ncalexan
/
geckodriver
/
releases
/
download
/
v0
.
24
.
0
-
android
/
ffmpeg
-
4
.
1
.
1
-
win64
-
static
.
zip
"
            
"
path
"
:
"
ffmpeg
-
4
.
1
.
1
-
win64
-
static
"
        
}
        
"
ImageMagick
"
:
{
            
"
type
"
:
"
static
-
url
"
            
"
url
"
:
"
https
:
/
/
ftp
.
icm
.
edu
.
pl
/
packages
/
ImageMagick
/
binaries
/
ImageMagick
-
7
.
0
.
8
-
39
-
portable
-
Q16
-
x64
.
zip
"
            
"
path
"
:
"
ImageMagick
-
7
.
0
.
8
"
        
}
    
}
}
class
BrowsertimeRunner
(
NodeRunner
)
:
    
def
__init__
(
self
mach_cmd
)
:
        
super
(
BrowsertimeRunner
self
)
.
__init__
(
mach_cmd
)
        
self
.
topsrcdir
=
mach_cmd
.
topsrcdir
        
self
.
_mach_context
=
mach_cmd
.
_mach_context
        
self
.
virtualenv_manager
=
mach_cmd
.
virtualenv_manager
        
self
.
proxy
=
None
        
self
.
_created_dirs
=
[
]
    
property
    
def
artifact_cache_path
(
self
)
:
        
"
"
"
Downloaded
artifacts
will
be
kept
here
.
"
"
"
        
return
mozpath
.
join
(
self
.
_mach_context
.
state_dir
"
cache
"
"
browsertime
"
)
    
property
    
def
state_path
(
self
)
:
        
"
"
"
Unpacked
artifacts
will
be
kept
here
.
"
"
"
        
res
=
mozpath
.
join
(
self
.
_mach_context
.
state_dir
"
browsertime
"
)
        
mkdir
(
res
)
        
return
res
    
property
    
def
browsertime_js
(
self
)
:
        
root
=
os
.
environ
.
get
(
"
BROWSERTIME
"
self
.
state_path
)
        
return
os
.
path
.
join
(
            
root
"
node_modules
"
"
browsertime
"
"
bin
"
"
browsertime
.
js
"
        
)
    
def
setup_prerequisites
(
self
)
:
        
"
"
"
Install
browsertime
and
visualmetrics
.
py
prerequisites
.
        
"
"
"
        
from
mozbuild
.
action
.
tooltool
import
unpack_file
        
from
mozbuild
.
artifact_cache
import
ArtifactCache
        
if
not
AUTOMATION
and
host_platform
(
)
.
startswith
(
"
linux
"
)
:
            
try
:
                
from
shutil
import
which
            
except
ImportError
:
                
from
shutil_which
import
which
            
im_programs
=
(
"
compare
"
"
convert
"
"
mogrify
"
)
            
for
im_program
in
im_programs
:
                
prog
=
which
(
im_program
)
                
if
not
prog
:
                    
print
(
                        
"
Error
:
On
Linux
ImageMagick
must
be
on
the
PATH
.
"
                        
"
Install
ImageMagick
manually
and
try
again
(
or
update
PATH
)
.
"
                        
"
On
Ubuntu
and
Debian
try
sudo
apt
-
get
install
imagemagick
.
"
                        
"
On
Fedora
try
sudo
dnf
install
imagemagick
.
"
                        
"
On
CentOS
try
sudo
yum
install
imagemagick
.
"
                    
)
                    
return
1
        
artifact_cache
=
ArtifactCache
(
            
self
.
artifact_cache_path
log
=
self
.
log
skip_cache
=
False
        
)
        
fetches
=
host_fetches
[
host_platform
(
)
]
        
for
tool
fetch
in
sorted
(
fetches
.
items
(
)
)
:
            
archive
=
artifact_cache
.
fetch
(
fetch
[
"
url
"
]
)
            
if
fetch
.
get
(
"
unpack
"
True
)
:
                
cwd
=
os
.
getcwd
(
)
                
try
:
                    
mkdir
(
self
.
state_path
)
                    
os
.
chdir
(
self
.
state_path
)
                    
self
.
info
(
"
Unpacking
temporary
location
{
path
}
"
path
=
archive
)
                    
if
"
win64
"
in
host_platform
(
)
and
"
imagemagick
"
in
tool
.
lower
(
)
:
                        
mkdir
(
fetch
.
get
(
"
path
"
)
)
                        
os
.
chdir
(
os
.
path
.
join
(
self
.
state_path
fetch
.
get
(
"
path
"
)
)
)
                        
unpack_file
(
archive
)
                        
os
.
chdir
(
self
.
state_path
)
                    
else
:
                        
unpack_file
(
archive
)
                    
path
=
os
.
path
.
join
(
self
.
state_path
fetch
.
get
(
"
path
"
)
)
                    
if
not
os
.
path
.
exists
(
path
)
:
                        
raise
Exception
(
"
Cannot
find
an
extracted
directory
:
%
s
"
%
path
)
                    
try
:
                        
for
root
dirs
files
in
os
.
walk
(
path
)
:
                            
for
edir
in
dirs
:
                                
loc_to_change
=
os
.
path
.
join
(
root
edir
)
                                
st
=
os
.
stat
(
loc_to_change
)
                                
os
.
chmod
(
loc_to_change
st
.
st_mode
|
stat
.
S_IEXEC
)
                            
for
efile
in
files
:
                                
loc_to_change
=
os
.
path
.
join
(
root
efile
)
                                
st
=
os
.
stat
(
loc_to_change
)
                                
os
.
chmod
(
loc_to_change
st
.
st_mode
|
stat
.
S_IEXEC
)
                    
except
Exception
as
e
:
                        
raise
Exception
(
                            
"
Could
not
set
executable
bit
in
%
s
error
:
%
s
"
                            
%
(
path
str
(
e
)
)
                        
)
                
finally
:
                    
os
.
chdir
(
cwd
)
    
def
_need_install
(
self
package
)
:
        
from
pip
.
_internal
.
req
.
constructors
import
install_req_from_line
        
req
=
install_req_from_line
(
"
Pillow
"
)
        
req
.
check_if_exists
(
use_user_site
=
False
)
        
if
req
.
satisfied_by
is
None
:
            
return
True
        
venv_site_lib
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
self
.
virtualenv_manager
.
bin_path
"
.
.
"
"
lib
"
)
        
)
        
site_packages
=
os
.
path
.
abspath
(
req
.
satisfied_by
.
location
)
        
return
not
site_packages
.
startswith
(
venv_site_lib
)
    
def
setup
(
self
should_clobber
=
False
new_upstream_url
=
"
"
)
:
        
"
"
"
Install
browsertime
and
visualmetrics
.
py
prerequisites
and
the
Node
.
js
package
.
        
"
"
"
        
super
(
BrowsertimeRunner
self
)
.
setup
(
)
        
for
dep
in
(
"
Pillow
=
=
%
s
"
%
PILLOW_VERSION
"
pyssim
=
=
%
s
"
%
PYSSIM_VERSION
)
:
            
if
self
.
_need_install
(
dep
)
:
                
self
.
virtualenv_manager
.
_run_pip
(
[
"
install
"
dep
]
)
        
if
os
.
path
.
exists
(
self
.
browsertime_js
)
:
            
return
        
sys
.
path
.
append
(
mozpath
.
join
(
self
.
topsrcdir
"
tools
"
"
lint
"
"
eslint
"
)
)
        
import
setup_helper
        
if
not
new_upstream_url
:
            
self
.
setup_prerequisites
(
)
        
for
file
in
(
"
package
.
json
"
"
package
-
lock
.
json
"
)
:
            
src
=
mozpath
.
join
(
BROWSERTIME_SRC_ROOT
file
)
            
target
=
mozpath
.
join
(
self
.
state_path
file
)
            
if
not
os
.
path
.
exists
(
target
)
:
                
shutil
.
copyfile
(
src
target
)
        
package_json_path
=
mozpath
.
join
(
self
.
state_path
"
package
.
json
"
)
        
if
new_upstream_url
:
            
self
.
info
(
                
"
Updating
browsertime
node
module
version
in
{
package_json_path
}
"
                
"
to
{
new_upstream_url
}
"
                
new_upstream_url
=
new_upstream_url
                
package_json_path
=
package_json_path
            
)
            
if
not
re
.
search
(
"
/
tarball
/
[
a
-
f0
-
9
]
{
40
}
"
new_upstream_url
)
:
                
raise
ValueError
(
                    
"
New
upstream
URL
does
not
end
with
/
tarball
/
[
a
-
f0
-
9
]
{
40
}
:
'
{
}
'
"
.
format
(
                        
new_upstream_url
                    
)
                
)
            
with
open
(
package_json_path
)
as
f
:
                
existing_body
=
json
.
loads
(
                    
f
.
read
(
)
object_pairs_hook
=
collections
.
OrderedDict
                
)
            
existing_body
[
"
devDependencies
"
]
[
"
browsertime
"
]
=
new_upstream_url
            
updated_body
=
json
.
dumps
(
existing_body
)
            
with
open
(
package_json_path
"
w
"
)
as
f
:
                
f
.
write
(
updated_body
)
        
if
not
setup_helper
.
check_node_executables_valid
(
)
:
            
return
        
if
AUTOMATION
:
            
os
.
environ
[
"
CHROMEDRIVER_SKIP_DOWNLOAD
"
]
=
"
true
"
            
os
.
environ
[
"
GECKODRIVER_SKIP_DOWNLOAD
"
]
=
"
true
"
        
self
.
info
(
            
"
Installing
browsertime
node
module
from
{
package_json
}
"
            
package_json
=
package_json_path
        
)
        
setup_helper
.
package_setup
(
            
self
.
state_path
            
"
browsertime
"
            
should_update
=
new_upstream_url
!
=
"
"
            
should_clobber
=
should_clobber
            
no_optional
=
new_upstream_url
or
AUTOMATION
        
)
    
def
append_env
(
self
append_path
=
True
)
:
        
env
=
super
(
BrowsertimeRunner
self
)
.
append_env
(
append_path
)
        
fetches
=
host_fetches
[
host_platform
(
)
]
        
path
=
env
.
get
(
"
PATH
"
"
"
)
.
split
(
os
.
pathsep
)
        
path_to_ffmpeg
=
mozpath
.
join
(
self
.
state_path
fetches
[
"
ffmpeg
"
]
[
"
path
"
]
)
        
path_to_imagemagick
=
None
        
if
"
ImageMagick
"
in
fetches
:
            
path_to_imagemagick
=
mozpath
.
join
(
                
self
.
state_path
fetches
[
"
ImageMagick
"
]
[
"
path
"
]
            
)
        
if
path_to_imagemagick
:
            
path
.
insert
(
                
0
                
self
.
state_path
                
if
host_platform
(
)
.
startswith
(
"
win
"
)
                
else
mozpath
.
join
(
path_to_imagemagick
"
bin
"
)
            
)
        
path
.
insert
(
            
0
            
path_to_ffmpeg
            
if
host_platform
(
)
.
startswith
(
"
linux
"
)
            
else
mozpath
.
join
(
path_to_ffmpeg
"
bin
"
)
        
)
        
if
"
win64
"
in
host_platform
(
)
and
path_to_imagemagick
:
            
path
.
insert
(
2
path_to_imagemagick
)
        
if
host_platform
(
)
=
=
"
darwin
"
:
            
for
p
in
os
.
environ
[
"
PATH
"
]
.
split
(
os
.
pathsep
)
:
                
p
=
p
.
strip
(
)
                
if
not
p
or
p
in
path
:
                    
continue
                
path
.
append
(
p
)
        
if
path_to_imagemagick
:
            
env
.
update
(
                
{
                    
"
LD_LIBRARY_PATH
"
:
mozpath
.
join
(
path_to_imagemagick
"
lib
"
)
                    
"
DYLD_LIBRARY_PATH
"
:
mozpath
.
join
(
path_to_imagemagick
"
lib
"
)
                    
"
MAGICK_HOME
"
:
path_to_imagemagick
                
}
            
)
        
return
env
    
def
extra_default_args
(
self
args
=
[
]
)
:
        
def
extract_browser_name
(
args
)
:
            
"
Extracts
the
browser
name
if
any
"
            
res
=
re
.
findall
(
"
(
-
-
browser
|
-
b
)
[
=
]
(
[
\
w
]
+
)
"
"
"
.
join
(
args
)
)
            
if
res
=
=
[
]
:
                
return
None
            
return
res
[
0
]
[
-
1
]
        
def
matches
(
args
*
flags
)
:
            
"
Return
True
if
any
argument
matches
any
of
the
given
flags
(
maybe
with
an
argument
)
.
"
            
for
flag
in
flags
:
                
if
flag
in
args
or
any
(
arg
.
startswith
(
flag
+
"
=
"
)
for
arg
in
args
)
:
                    
return
True
            
return
False
        
extra_args
=
[
]
        
specifies_browser
=
matches
(
args
"
-
b
"
"
-
-
browser
"
)
        
if
not
specifies_browser
:
            
extra_args
.
extend
(
(
"
-
b
"
"
firefox
"
)
)
        
specifies_har
=
matches
(
args
"
-
-
har
"
"
-
-
skipHar
"
"
-
-
gzipHar
"
)
        
if
not
specifies_har
:
            
extra_args
.
append
(
"
-
-
skipHar
"
)
        
if
not
matches
(
args
"
-
-
android
"
)
:
            
specifies_binaryPath
=
matches
(
                
args
                
"
-
-
firefox
.
binaryPath
"
                
"
-
-
firefox
.
release
"
                
"
-
-
firefox
.
nightly
"
                
"
-
-
firefox
.
beta
"
                
"
-
-
firefox
.
developer
"
            
)
            
if
not
specifies_binaryPath
:
                
specifies_binaryPath
=
extract_browser_name
(
args
)
=
=
"
chrome
"
            
if
not
specifies_binaryPath
:
                
try
:
                    
extra_args
.
extend
(
(
"
-
-
firefox
.
binaryPath
"
self
.
get_binary_path
(
)
)
)
                
except
Exception
:
                    
print
(
                        
"
Please
run
|
.
/
mach
build
|
"
                        
"
or
specify
a
Firefox
binary
with
-
-
firefox
.
binaryPath
.
"
                    
)
                    
return
1
        
if
extra_args
:
            
self
.
debug
(
                
"
Running
browsertime
with
extra
default
arguments
:
{
extra_args
}
"
                
extra_args
=
extra_args
            
)
        
return
extra_args
    
def
get_profile
(
self
metadata
)
:
        
from
mozprofile
import
create_profile
        
profile
=
create_profile
(
app
=
"
firefox
"
)
        
prefs
=
metadata
.
get_browser_prefs
(
)
        
profile
.
set_preferences
(
prefs
)
        
self
.
info
(
"
Created
profile
at
%
s
"
%
profile
.
profile
)
        
self
.
_created_dirs
.
append
(
profile
.
profile
)
        
return
profile
    
def
__call__
(
self
metadata
)
:
        
profile
=
self
.
get_profile
(
metadata
)
        
test_script
=
metadata
.
get_arg
(
"
tests
"
)
[
0
]
        
result_dir
=
os
.
path
.
join
(
os
.
path
.
dirname
(
__file__
)
"
browsertime
-
results
"
)
        
args
=
[
            
"
-
-
resultDir
"
            
result_dir
            
"
-
-
firefox
.
profileTemplate
"
            
profile
.
profile
            
"
-
vvv
"
            
"
-
-
iterations
"
            
"
1
"
            
test_script
        
]
        
extra_options
=
metadata
.
get_arg
(
"
extra_options
"
)
        
if
extra_options
:
            
for
option
in
extra_options
.
split
(
"
"
)
:
                
option
=
option
.
strip
(
)
                
if
not
option
:
                    
continue
                
option
=
option
.
split
(
"
=
"
)
                
if
len
(
option
)
!
=
2
:
                    
continue
                
name
value
=
option
                
args
+
=
[
"
-
-
"
+
name
value
]
        
firefox_args
=
[
"
-
-
firefox
.
developer
"
]
        
extra
=
self
.
extra_default_args
(
args
=
firefox_args
)
        
command
=
[
self
.
browsertime_js
]
+
extra
+
args
        
self
.
info
(
"
Running
browsertime
with
this
command
%
s
"
%
"
"
.
join
(
command
)
)
        
self
.
node
(
command
)
        
metadata
.
set_result
(
result_dir
)
        
return
metadata
    
def
teardown
(
self
)
:
        
for
dir
in
self
.
_created_dirs
:
            
if
os
.
path
.
exists
(
dir
)
:
                
shutil
.
rmtree
(
dir
)
