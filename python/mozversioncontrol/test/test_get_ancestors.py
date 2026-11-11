import
subprocess
import
mozunit
import
pytest
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
commit
-
am
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
    
"
jj
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
        
jj
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
        
jj
commit
-
m
"
commit
2
"
        
jj
log
-
n0
        
"
"
"
    
]
}
def
test_get_ancestors
(
repo
)
:
    
if
repo
.
vcs
=
=
"
hg
"
:
        
pytest
.
skip
(
"
get_ancestors
is
only
implemented
for
git
and
jj
"
)
    
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
    
expected
=
subprocess
.
check_output
(
        
[
"
git
"
"
rev
-
parse
"
"
HEAD
"
"
HEAD
~
1
"
"
HEAD
~
2
"
]
cwd
=
repo
.
dir
text
=
True
    
)
.
splitlines
(
)
    
assert
vcs
.
get_ancestors
(
)
=
=
expected
    
assert
vcs
.
get_ancestors
(
limit
=
2
)
=
=
expected
[
:
2
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
