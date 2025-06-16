import
os
import
platform
import
shutil
import
subprocess
import
tempfile
from
pathlib
import
Path
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
describe
-
-
reset
-
author
-
-
no
-
edit
        
"
"
"
        
"
"
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
    
"
src
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
        
mkdir
config
        
echo
1
.
0
>
config
/
milestone
.
txt
        
"
"
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
list
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
"
src
"
]
)
def
repo
(
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
        
if
os
.
getenv
(
"
MOZ_AUTOMATION
"
)
=
=
1
:
            
fetches_dir
=
os
.
environ
.
get
(
"
MOZ_FETCHES_DIR
"
"
"
)
            
jj_dir
=
Path
(
fetches_dir
)
/
"
jj
"
            
if
jj_dir
.
is_dir
(
)
:
                
os
.
environ
[
"
PATH
"
]
=
os
.
pathsep
.
join
(
[
str
(
jj_dir
)
os
.
environ
[
"
PATH
"
]
]
)
            
if
platform
.
system
(
)
=
=
"
Darwin
"
:
                
pytest
.
skip
(
                    
"
jj
tests
disabled
for
MacOS
CI
due
to
incompatible
git
on
workers
"
                
)
        
if
os
.
getenv
(
"
MOZ_AVOID_JJ_VCS
"
)
not
in
(
None
"
0
"
"
"
)
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
        
try
:
            
subprocess
.
call
(
[
"
jj
"
"
-
-
version
"
]
stdout
=
subprocess
.
DEVNULL
)
        
except
OSError
:
            
pytest
.
skip
(
"
jj
unavailable
"
)
    
vcs
=
request
.
param
    
td
=
tempfile
.
TemporaryDirectory
(
prefix
=
f
"
{
vcs
}
-
repo
"
)
    
tmpdir
=
Path
(
td
.
name
)
    
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
        
if
vcs
=
=
"
src
"
and
vcs
not
in
request
.
module
.
STEPS
:
            
pytest
.
skip
(
"
not
applicable
for
src
repo
"
)
        
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
