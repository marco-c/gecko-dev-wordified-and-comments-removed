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
stat
import
subprocess
import
tempfile
import
zipfile
from
optparse
import
OptionParser
from
urllib
.
request
import
urlopen
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
developer
.
mozilla
.
org
/
en
-
US
/
docs
/
Mozilla
/
Developer_guide
/
Source_Code
/
Mercurial
/
Bundles
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
os
.
path
.
join
(
path
name
)
        
if
os
.
path
.
isfile
(
test
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
)
:
    
dest
=
os
.
path
.
abspath
(
dest
)
    
if
not
os
.
path
.
exists
(
dest
)
:
        
return
dest
    
if
not
os
.
path
.
isdir
(
dest
)
:
        
print
(
"
ERROR
!
Destination
%
s
exists
but
is
not
a
directory
.
"
%
dest
)
        
return
None
    
if
not
os
.
listdir
(
dest
)
:
        
return
dest
    
else
:
        
print
(
"
ERROR
!
Destination
directory
%
s
exists
but
is
nonempty
.
"
%
dest
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
"
Cloning
into
%
s
using
%
s
.
.
.
"
%
(
repo_name
VCS_HUMAN_READABLE
[
vcs
]
)
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
                
"
default
destination
of
%
s
)
:
"
%
repo_name
            
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
os
.
path
.
expanduser
(
dest
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
dest
)
:
    
args
=
[
        
hg
        
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
        
dest
    
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
os
.
path
.
join
(
dest
"
.
hg
"
"
hgrc
"
)
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
hg
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
dest
    
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
hg
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
dest
)
    
if
res
:
        
print
(
            
"
error
updating
;
you
will
need
to
cd
%
s
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
%
dest
        
)
    
return
dest
def
git_clone_firefox
(
git
dest
watchman
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
(
                
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
archive
/
"
"
master
.
zip
"
            
)
            
tempdir
=
tempfile
.
mkdtemp
(
)
            
with
open
(
os
.
path
.
join
(
tempdir
"
git
-
cinnabar
.
zip
"
)
mode
=
"
w
+
b
"
)
as
archive
:
                
with
urlopen
(
cinnabar_url
)
as
repo
:
                    
shutil
.
copyfileobj
(
repo
archive
)
                
archive
.
seek
(
0
)
                
with
zipfile
.
ZipFile
(
archive
)
as
zipf
:
                    
zipf
.
extractall
(
path
=
tempdir
)
            
cinnabar_dir
=
os
.
path
.
join
(
tempdir
"
git
-
cinnabar
-
master
"
)
            
cinnabar
=
os
.
path
.
join
(
cinnabar_dir
"
git
-
cinnabar
"
)
            
st
=
os
.
stat
(
cinnabar
)
            
os
.
chmod
(
cinnabar
st
.
st_mode
|
stat
.
S_IEXEC
)
            
st
=
os
.
stat
(
os
.
path
.
join
(
cinnabar_dir
"
git
-
remote
-
hg
"
)
)
            
os
.
chmod
(
                
os
.
path
.
join
(
cinnabar_dir
"
git
-
remote
-
hg
"
)
st
.
st_mode
|
stat
.
S_IEXEC
            
)
            
env
[
"
PATH
"
]
=
cinnabar_dir
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
"
git
"
"
cinnabar
"
"
download
"
]
cwd
=
cinnabar_dir
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
                
git
                
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
                
dest
            
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
git
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
dest
env
=
env
)
        
subprocess
.
check_call
(
[
git
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
dest
env
=
env
)
        
watchman_sample
=
os
.
path
.
join
(
dest
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
)
        
if
watchman
and
os
.
path
.
exists
(
watchman_sample
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
os
.
path
.
join
(
dest
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
)
            
if
not
os
.
path
.
exists
(
watchman_config
)
:
                
print
(
"
Copying
%
s
to
%
s
"
%
(
watchman_sample
watchman_config
)
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
dest
)
            
config_args
=
[
git
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
dest
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
tempdir
)
def
clone
(
vcs
no_interactive
)
:
    
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
    
print
(
"
Cloning
Firefox
%
s
repository
to
%
s
"
%
(
VCS_HUMAN_READABLE
[
vcs
]
dest
)
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
os
.
path
.
join
(
srcdir
"
mach
"
)
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
srcdir
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
.
vcs
options
.
no_interactive
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
