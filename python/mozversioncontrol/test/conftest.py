import
os
import
shutil
import
subprocess
from
pathlib
import
Path
from
typing
import
List
import
pytest
SETUP
=
{
    
"
hg
"
:
[
        
"
"
"
        
echo
"
foo
"
>
foo
        
echo
"
bar
"
>
bar
        
hg
init
        
hg
add
*
        
hg
commit
-
m
"
Initial
commit
"
        
hg
phase
-
-
public
.
        
"
"
"
        
"
"
"
        
echo
[
paths
]
>
.
hg
/
hgrc
        
echo
"
default
=
.
.
/
remoterepo
"
>
>
.
hg
/
hgrc
        
"
"
"
    
]
    
"
git
"
:
[
        
"
"
"
        
echo
"
foo
"
>
foo
        
echo
"
bar
"
>
bar
        
git
init
        
git
config
user
.
name
"
Testing
McTesterson
"
        
git
config
user
.
email
"
<
test
example
.
org
>
"
        
git
add
*
        
git
commit
-
am
"
Initial
commit
"
        
"
"
"
        
"
"
"
        
git
remote
add
upstream
.
.
/
remoterepo
        
git
fetch
upstream
        
git
branch
-
u
upstream
/
master
        
"
"
"
    
]
    
"
jj
"
:
[
        
"
"
"
        
echo
"
foo
"
>
foo
        
echo
"
bar
"
>
bar
        
git
init
        
git
config
user
.
name
"
Testing
McTesterson
"
        
git
config
user
.
email
"
<
test
example
.
org
>
"
        
git
add
*
        
git
commit
-
am
"
Initial
commit
"
        
"
"
"
        
"
"
"
        
#
Pass
in
user
name
/
email
via
env
vars
because
the
initial
commit
        
#
will
use
them
before
we
have
a
chance
to
configure
them
.
        
JJ_USER
=
"
Testing
McTesterson
"
JJ_EMAIL
=
"
test
example
.
org
"
jj
git
init
-
-
colocate
        
jj
config
set
-
-
repo
user
.
name
"
Testing
McTesterson
"
        
jj
config
set
-
-
repo
user
.
email
"
test
example
.
org
"
        
jj
git
remote
add
upstream
.
.
/
remoterepo
        
jj
git
fetch
-
-
remote
upstream
        
jj
bookmark
track
master
upstream
        
"
"
"
    
]
}
class
RepoTestFixture
:
    
def
__init__
(
self
repo_dir
:
Path
vcs
:
str
steps
:
List
[
str
]
)
:
        
self
.
dir
=
repo_dir
        
self
.
vcs
=
vcs
        
self
.
steps
=
(
shell
(
cmd
self
.
dir
)
for
cmd
in
steps
)
    
def
execute_next_step
(
self
)
:
        
next
(
self
.
steps
)
def
shell
(
cmd
working_dir
)
:
    
for
step
in
cmd
.
split
(
os
.
linesep
)
:
        
subprocess
.
check_call
(
step
shell
=
True
cwd
=
working_dir
)
pytest
.
fixture
(
params
=
[
"
git
"
"
hg
"
"
jj
"
]
)
def
repo
(
tmpdir
request
)
:
    
if
request
.
param
=
=
"
jj
"
:
        
avoid
=
os
.
getenv
(
"
MOZ_AVOID_JJ_VCS
"
)
        
if
avoid
and
avoid
!
=
"
0
"
:
            
pytest
.
skip
(
"
jj
support
disabled
"
)
    
tmpdir
=
Path
(
tmpdir
)
    
vcs
=
request
.
param
    
steps
=
SETUP
[
vcs
]
    
if
hasattr
(
request
.
module
"
STEPS
"
)
:
        
steps
.
extend
(
request
.
module
.
STEPS
[
vcs
]
)
    
repo_dir
=
(
tmpdir
/
"
repo
"
)
.
resolve
(
)
    
(
tmpdir
/
"
repo
"
)
.
mkdir
(
)
    
repo_test_fixture
=
RepoTestFixture
(
repo_dir
vcs
steps
)
    
repo_test_fixture
.
execute_next_step
(
)
    
shutil
.
copytree
(
str
(
repo_dir
)
str
(
tmpdir
/
"
remoterepo
"
)
)
    
repo_test_fixture
.
execute_next_step
(
)
    
yield
repo_test_fixture
