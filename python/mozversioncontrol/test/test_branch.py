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
=
=
"
git
"
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
