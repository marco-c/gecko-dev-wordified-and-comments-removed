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
commit
1
"
        
echo
baz
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
commit
2
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
commit
1
"
        
echo
baz
>
baz
        
git
add
baz
        
git
commit
-
m
"
commit
2
"
        
"
"
"
    
]
}
def
test_get_branch_nodes
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
    
repo
.
execute_next_step
(
)
    
nodes
=
vcs
.
get_branch_nodes
(
)
    
assert
len
(
nodes
)
=
=
2
    
assert
all
(
len
(
node
)
=
=
40
for
node
in
nodes
)
"
Each
node
should
be
a
40
-
char
SHA
.
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
