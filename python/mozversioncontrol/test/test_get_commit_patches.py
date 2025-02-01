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
        
echo
bar
>
>
bar
        
hg
commit
-
m
"
FIRST
PATCH
"
        
"
"
"
        
"
"
"
        
printf
"
baz
\
\
r
\
\
nqux
"
>
baz
        
hg
add
baz
        
hg
commit
-
m
"
SECOND
PATCH
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
        
echo
bar
>
>
bar
        
git
add
bar
        
git
commit
-
m
"
FIRST
PATCH
"
        
"
"
"
        
"
"
"
        
printf
"
baz
\
\
r
\
\
nqux
"
>
baz
        
git
-
c
core
.
autocrlf
=
false
add
baz
        
git
commit
-
m
"
SECOND
PATCH
"
        
"
"
"
    
]
}
def
test_get_commit_patches
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
    
nodes
=
[
]
    
repo
.
execute_next_step
(
)
    
nodes
.
append
(
vcs
.
head_ref
)
    
repo
.
execute_next_step
(
)
    
nodes
.
append
(
vcs
.
head_ref
)
    
patches
=
vcs
.
get_commit_patches
(
nodes
)
    
assert
len
(
patches
)
=
=
2
    
assert
b
"
FIRST
PATCH
"
in
patches
[
0
]
    
assert
b
"
SECOND
PATCH
"
in
patches
[
1
]
    
assert
b
"
baz
\
r
\
n
"
in
patches
[
1
]
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
