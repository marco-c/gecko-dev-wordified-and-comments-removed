from
__future__
import
absolute_import
import
os
import
subprocess
import
pytest
SETUP
=
{
    
'
hg
'
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
        
"
"
"
        
"
"
"
        
echo
"
[
paths
]
\
ndefault
=
.
.
/
remoterepo
"
>
.
hg
/
hgrc
        
"
"
"
    
]
    
'
git
'
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
}
def
shell
(
cmd
)
:
    
subprocess
.
check_call
(
cmd
shell
=
True
)
pytest
.
yield_fixture
(
params
=
[
'
git
'
'
hg
'
]
)
def
repo
(
tmpdir
request
)
:
    
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
'
STEPS
'
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
    
repo
=
tmpdir
.
mkdir
(
'
repo
'
)
    
repo
.
vcs
=
vcs
    
repo
.
step
=
(
shell
(
cmd
)
for
cmd
in
steps
)
    
oldcwd
=
os
.
getcwd
(
)
    
os
.
chdir
(
repo
.
strpath
)
    
next
(
repo
.
step
)
    
repo
.
copy
(
tmpdir
.
join
(
'
remoterepo
'
)
)
    
next
(
repo
.
step
)
    
yield
repo
    
os
.
chdir
(
oldcwd
)
