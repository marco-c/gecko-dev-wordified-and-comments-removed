import
mozunit
from
mozversioncontrol
import
get_repository_object
STEPS
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
        
hg
bookmark
test
        
"
"
"
        
"
"
"
        
echo
"
bar
"
>
foo
        
hg
commit
-
m
"
second
commit
"
        
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
        
git
checkout
-
b
test
        
"
"
"
        
"
"
"
        
echo
"
bar
"
>
foo
        
git
commit
-
a
-
m
"
second
commit
"
        
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
        
jj
bookmark
set
test
        
"
"
"
        
"
"
"
        
jj
new
-
m
"
xyzzy
"
zzzzzzzz
        
jj
new
-
m
"
second
commit
"
test
        
echo
"
bar
"
>
foo
        
"
"
"
    
]
}
def
test_branch
(
repo
)
:
    
vcs
=
get_repository_object
(
repo
.
dir
)
    
if
vcs
.
name
in
(
"
git
"
"
jj
"
)
:
        
assert
vcs
.
branch
=
=
"
master
"
    
else
:
        
assert
vcs
.
branch
is
None
    
repo
.
execute_next_step
(
)
    
assert
vcs
.
branch
=
=
"
test
"
    
repo
.
execute_next_step
(
)
    
assert
vcs
.
branch
=
=
"
test
"
    
vcs
.
update
(
vcs
.
head_ref
)
    
if
repo
.
vcs
=
=
"
jj
"
:
        
assert
vcs
.
branch
=
=
"
test
"
    
else
:
        
assert
vcs
.
branch
is
None
    
vcs
.
update
(
"
test
"
)
    
assert
vcs
.
branch
=
=
"
test
"
    
if
repo
.
vcs
=
=
"
jj
"
:
        
vcs
.
update
(
"
description
(
'
xyzzy
'
)
"
)
        
assert
vcs
.
branch
is
None
if
__name__
=
=
"
__main__
"
:
    
mozunit
.
main
(
)
