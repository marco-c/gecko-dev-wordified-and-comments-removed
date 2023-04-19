from
__future__
import
absolute_import
print_function
unicode_literals
import
sys
major
minor
=
sys
.
version_info
[
:
2
]
if
(
major
<
3
)
or
(
major
=
=
3
and
minor
<
5
)
:
    
print
(
        
"
Bootstrap
currently
only
runs
on
Python
3
.
5
+
.
"
        
"
Please
try
re
-
running
with
python3
.
5
+
.
"
    
)
    
sys
.
exit
(
1
)
import
os
import
shutil
import
subprocess
import
tempfile
import
ctypes
from
pathlib
import
Path
from
optparse
import
OptionParser
CLONE_MERCURIAL_PULL_FAIL
=
"
"
"
Failed
to
pull
from
hg
.
mozilla
.
org
.
This
is
most
likely
because
of
unstable
network
connection
.
Try
running
cd
%
s
&
&
hg
pull
https
:
/
/
hg
.
mozilla
.
org
/
mozilla
-
unified
manually
or
download
a
mercurial
bundle
and
use
it
:
https
:
/
/
firefox
-
source
-
docs
.
mozilla
.
org
/
contributing
/
vcs
/
mercurial_bundles
.
html
"
"
"
WINDOWS
=
sys
.
platform
.
startswith
(
"
win32
"
)
or
sys
.
platform
.
startswith
(
"
msys
"
)
VCS_HUMAN_READABLE
=
{
    
"
hg
"
:
"
Mercurial
"
    
"
git
"
:
"
Git
"
}
def
which
(
name
)
:
    
"
"
"
Python
implementation
of
which
.
    
It
returns
the
path
of
an
executable
or
None
if
it
couldn
'
t
be
found
.
    
"
"
"
    
if
WINDOWS
and
name
!
=
"
git
-
cinnabar
"
:
        
name
+
=
"
.
exe
"
    
search_dirs
=
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
    
for
path
in
search_dirs
:
        
test
=
Path
(
path
)
/
name
        
if
test
.
is_file
(
)
and
os
.
access
(
test
os
.
X_OK
)
:
            
return
test
    
return
None
def
validate_clone_dest
(
dest
:
Path
)
:
    
dest
=
dest
.
resolve
(
)
    
if
not
dest
.
exists
(
)
:
        
return
dest
    
if
not
dest
.
is_dir
(
)
:
        
print
(
f
"
ERROR
!
Destination
{
dest
}
exists
but
is
not
a
directory
.
"
)
        
return
None
    
if
not
any
(
dest
.
iterdir
(
)
)
:
        
return
dest
    
else
:
        
print
(
f
"
ERROR
!
Destination
directory
{
dest
}
exists
but
is
nonempty
.
"
)
        
print
(
            
f
"
To
re
-
bootstrap
the
existing
checkout
go
into
'
{
dest
}
'
and
run
'
.
/
mach
bootstrap
'
.
"
        
)
        
return
None
def
input_clone_dest
(
vcs
no_interactive
)
:
    
repo_name
=
"
mozilla
-
unified
"
    
print
(
f
"
Cloning
into
{
repo_name
}
using
{
VCS_HUMAN_READABLE
[
vcs
]
}
.
.
.
"
)
    
while
True
:
        
dest
=
None
        
if
not
no_interactive
:
            
dest
=
input
(
                
f
"
Destination
directory
for
clone
(
leave
empty
to
use
"
                
f
"
default
destination
of
{
repo_name
}
)
:
"
            
)
.
strip
(
)
        
if
not
dest
:
            
dest
=
repo_name
        
dest
=
validate_clone_dest
(
Path
(
dest
)
.
expanduser
(
)
)
        
if
dest
:
            
return
dest
        
if
no_interactive
:
            
return
None
def
hg_clone_firefox
(
hg
:
Path
dest
:
Path
)
:
    
args
=
[
        
str
(
hg
)
        
"
-
-
config
"
        
"
format
.
generaldelta
=
true
"
        
"
init
"
        
str
(
dest
)
    
]
    
res
=
subprocess
.
call
(
args
)
    
if
res
:
        
print
(
"
unable
to
create
destination
repo
;
please
try
cloning
manually
"
)
        
return
None
    
with
open
(
dest
/
"
.
hg
"
/
"
hgrc
"
"
a
"
)
as
fh
:
        
fh
.
write
(
"
[
paths
]
\
n
"
)
        
fh
.
write
(
"
default
=
https
:
/
/
hg
.
mozilla
.
org
/
mozilla
-
unified
\
n
"
)
        
fh
.
write
(
"
\
n
"
)
        
fh
.
write
(
"
[
format
]
\
n
"
)
        
fh
.
write
(
"
#
This
is
necessary
to
keep
performance
in
check
\
n
"
)
        
fh
.
write
(
"
maxchainlen
=
10000
\
n
"
)
    
res
=
subprocess
.
call
(
        
[
str
(
hg
)
"
pull
"
"
https
:
/
/
hg
.
mozilla
.
org
/
mozilla
-
unified
"
]
cwd
=
str
(
dest
)
    
)
    
print
(
"
"
)
    
if
res
:
        
print
(
CLONE_MERCURIAL_PULL_FAIL
%
dest
)
        
return
None
    
print
(
'
updating
to
"
central
"
-
the
development
head
of
Gecko
and
Firefox
'
)
    
res
=
subprocess
.
call
(
[
str
(
hg
)
"
update
"
"
-
r
"
"
central
"
]
cwd
=
str
(
dest
)
)
    
if
res
:
        
print
(
            
f
"
error
updating
;
you
will
need
to
cd
{
dest
}
&
&
hg
update
-
r
central
"
            
"
manually
"
        
)
    
return
dest
def
git_clone_firefox
(
git
:
Path
dest
:
Path
watchman
:
Path
)
:
    
tempdir
=
None
    
cinnabar
=
None
    
env
=
dict
(
os
.
environ
)
    
try
:
        
cinnabar
=
which
(
"
git
-
cinnabar
"
)
        
if
not
cinnabar
:
            
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
            
tempdir
=
Path
(
tempfile
.
mkdtemp
(
)
)
            
cinnabar_dir
=
tempdir
/
"
git
-
cinnabar
-
master
"
            
subprocess
.
check_call
(
                
[
str
(
git
)
"
clone
"
"
-
-
depth
=
1
"
str
(
cinnabar_url
)
str
(
cinnabar_dir
)
]
                
cwd
=
str
(
tempdir
)
                
env
=
env
            
)
            
env
[
"
PATH
"
]
=
str
(
cinnabar_dir
)
+
os
.
pathsep
+
env
[
"
PATH
"
]
            
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
cinnabar_dir
/
"
download
.
py
"
)
]
                
cwd
=
str
(
cinnabar_dir
)
                
env
=
env
            
)
            
print
(
                
"
WARNING
!
git
-
cinnabar
is
required
for
Firefox
development
"
                
"
with
git
.
After
the
clone
is
complete
the
bootstrapper
"
                
"
will
ask
if
you
would
like
to
configure
git
;
answer
yes
"
                
"
and
be
sure
to
add
git
-
cinnabar
to
your
PATH
according
to
"
                
"
the
bootstrapper
output
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
git
)
                
"
clone
"
                
"
-
b
"
                
"
bookmarks
/
central
"
                
"
hg
:
:
https
:
/
/
hg
.
mozilla
.
org
/
mozilla
-
unified
"
                
str
(
dest
)
            
]
            
env
=
env
        
)
        
subprocess
.
check_call
(
            
[
str
(
git
)
"
config
"
"
fetch
.
prune
"
"
true
"
]
cwd
=
str
(
dest
)
env
=
env
        
)
        
subprocess
.
check_call
(
            
[
str
(
git
)
"
config
"
"
pull
.
ff
"
"
only
"
]
cwd
=
str
(
dest
)
env
=
env
        
)
        
watchman_sample
=
dest
/
"
.
git
/
hooks
/
fsmonitor
-
watchman
.
sample
"
        
if
watchman
and
watchman_sample
.
exists
(
)
:
            
print
(
"
Configuring
watchman
"
)
            
watchman_config
=
dest
/
"
.
git
/
hooks
/
query
-
watchman
"
            
if
not
watchman_config
.
exists
(
)
:
                
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
                
copy_args
=
[
                    
"
cp
"
                    
"
.
git
/
hooks
/
fsmonitor
-
watchman
.
sample
"
                    
"
.
git
/
hooks
/
query
-
watchman
"
                
]
                
subprocess
.
check_call
(
copy_args
cwd
=
str
(
dest
)
)
            
config_args
=
[
                
str
(
git
)
                
"
config
"
                
"
core
.
fsmonitor
"
                
"
.
git
/
hooks
/
query
-
watchman
"
            
]
            
subprocess
.
check_call
(
config_args
cwd
=
str
(
dest
)
env
=
env
)
        
return
dest
    
finally
:
        
if
not
cinnabar
:
            
print
(
                
"
Failed
to
install
git
-
cinnabar
.
Try
performing
a
manual
"
                
"
installation
:
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
wiki
/
"
                
"
Mozilla
:
-
A
-
git
-
workflow
-
for
-
Gecko
-
development
"
            
)
        
if
tempdir
:
            
shutil
.
rmtree
(
str
(
tempdir
)
)
def
add_microsoft_defender_antivirus_exclusions
(
dest
no_system_changes
)
:
    
if
no_system_changes
:
        
return
    
powershell_exe
=
which
(
"
powershell
"
)
    
if
not
powershell_exe
:
        
return
    
def
print_attempt_exclusion
(
path
)
:
        
print
(
            
f
"
Attempting
to
add
exclusion
path
to
Microsoft
Defender
Antivirus
for
:
{
path
}
"
        
)
    
powershell_exe
=
str
(
powershell_exe
)
    
paths
=
[
]
    
repo_dir
=
Path
.
cwd
(
)
/
dest
    
paths
.
append
(
repo_dir
)
    
print_attempt_exclusion
(
repo_dir
)
    
mozillabuild_dir
=
os
.
getenv
(
"
MOZILLABUILD
"
)
    
if
mozillabuild_dir
:
        
paths
.
append
(
mozillabuild_dir
)
        
print_attempt_exclusion
(
mozillabuild_dir
)
    
mozbuild_dir
=
Path
.
home
(
)
/
"
.
mozbuild
"
    
paths
.
append
(
mozbuild_dir
)
    
print_attempt_exclusion
(
mozbuild_dir
)
    
args
=
"
;
"
.
join
(
f
"
Add
-
MpPreference
-
ExclusionPath
'
{
path
}
'
"
for
path
in
paths
)
    
command
=
f
'
-
Command
"
{
args
}
"
'
    
ctypes
.
windll
.
shell32
.
ShellExecuteW
(
None
"
runas
"
powershell_exe
command
None
0
)
def
clone
(
options
)
:
    
vcs
=
options
.
vcs
    
no_interactive
=
options
.
no_interactive
    
no_system_changes
=
options
.
no_system_changes
    
hg
=
which
(
"
hg
"
)
    
if
not
hg
:
        
print
(
            
"
Mercurial
is
not
installed
.
Mercurial
is
required
to
clone
"
            
"
Firefox
%
s
.
"
%
(
"
even
when
cloning
with
Git
"
if
vcs
=
=
"
git
"
else
"
"
)
        
)
        
try
:
            
import
mercurial
            
print
(
                
"
Hint
:
have
you
made
sure
that
Mercurial
is
installed
to
a
"
                
"
location
in
your
PATH
?
"
            
)
        
except
ImportError
:
            
print
(
"
Try
installing
hg
with
pip3
install
Mercurial
.
"
)
        
return
None
    
if
vcs
=
=
"
hg
"
:
        
binary
=
hg
    
else
:
        
binary
=
which
(
vcs
)
        
if
not
binary
:
            
print
(
"
Git
is
not
installed
.
"
)
            
print
(
"
Try
installing
git
using
your
system
package
manager
.
"
)
            
return
None
    
dest
=
input_clone_dest
(
vcs
no_interactive
)
    
if
not
dest
:
        
return
None
    
add_microsoft_defender_antivirus_exclusions
(
dest
no_system_changes
)
    
print
(
f
"
Cloning
Firefox
{
VCS_HUMAN_READABLE
[
vcs
]
}
repository
to
{
dest
}
"
)
    
if
vcs
=
=
"
hg
"
:
        
return
hg_clone_firefox
(
binary
dest
)
    
else
:
        
watchman
=
which
(
"
watchman
"
)
        
return
git_clone_firefox
(
binary
dest
watchman
)
def
bootstrap
(
srcdir
:
Path
application_choice
no_interactive
no_system_changes
)
:
    
args
=
[
sys
.
executable
"
mach
"
]
    
if
no_interactive
:
        
args
+
=
[
"
-
-
no
-
interactive
"
]
    
args
+
=
[
"
bootstrap
"
]
    
if
application_choice
:
        
args
+
=
[
"
-
-
application
-
choice
"
application_choice
]
    
if
no_system_changes
:
        
args
+
=
[
"
-
-
no
-
system
-
changes
"
]
    
print
(
"
Running
%
s
"
%
"
"
.
join
(
args
)
)
    
return
subprocess
.
call
(
args
cwd
=
str
(
srcdir
)
)
def
main
(
args
)
:
    
parser
=
OptionParser
(
)
    
parser
.
add_option
(
        
"
-
-
application
-
choice
"
        
dest
=
"
application_choice
"
        
help
=
'
Pass
in
an
application
choice
(
see
"
APPLICATIONS
"
in
'
        
"
python
/
mozboot
/
mozboot
/
bootstrap
.
py
)
instead
of
using
the
"
        
"
default
interactive
prompt
.
"
    
)
    
parser
.
add_option
(
        
"
-
-
vcs
"
        
dest
=
"
vcs
"
        
default
=
"
hg
"
        
choices
=
[
"
git
"
"
hg
"
]
        
help
=
"
VCS
(
hg
or
git
)
to
use
for
downloading
the
source
code
"
        
"
instead
of
using
the
default
interactive
prompt
.
"
    
)
    
parser
.
add_option
(
        
"
-
-
no
-
interactive
"
        
dest
=
"
no_interactive
"
        
action
=
"
store_true
"
        
help
=
"
Answer
yes
to
any
(
Y
/
n
)
interactive
prompts
.
"
    
)
    
parser
.
add_option
(
        
"
-
-
no
-
system
-
changes
"
        
dest
=
"
no_system_changes
"
        
action
=
"
store_true
"
        
help
=
"
Only
executes
actions
that
leave
the
system
"
"
configuration
alone
.
"
    
)
    
options
leftover
=
parser
.
parse_args
(
args
)
    
try
:
        
srcdir
=
clone
(
options
)
        
if
not
srcdir
:
            
return
1
        
print
(
"
Clone
complete
.
"
)
        
print
(
            
"
If
you
need
to
run
the
tooling
bootstrapping
again
"
            
"
then
consider
running
'
.
/
mach
bootstrap
'
instead
.
"
        
)
        
if
not
options
.
no_interactive
:
            
remove_bootstrap_file
=
input
(
                
"
Unless
you
are
going
to
have
more
local
copies
of
Firefox
source
code
"
                
"
this
'
bootstrap
.
py
'
file
is
no
longer
needed
and
can
be
deleted
.
"
                
"
Clean
up
the
bootstrap
.
py
file
?
(
Y
/
n
)
"
            
)
            
if
not
remove_bootstrap_file
:
                
remove_bootstrap_file
=
"
y
"
        
if
options
.
no_interactive
or
remove_bootstrap_file
=
=
"
y
"
:
            
try
:
                
Path
(
sys
.
argv
[
0
]
)
.
unlink
(
)
            
except
FileNotFoundError
:
                
print
(
"
File
could
not
be
found
!
"
)
        
return
bootstrap
(
            
srcdir
            
options
.
application_choice
            
options
.
no_interactive
            
options
.
no_system_changes
        
)
    
except
Exception
:
        
print
(
"
Could
not
bootstrap
Firefox
!
Consider
filing
a
bug
.
"
)
        
raise
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
sys
.
argv
)
)
