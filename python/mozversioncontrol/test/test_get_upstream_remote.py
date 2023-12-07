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
remote
add
unified
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
        
git
remote
add
central
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
central
        
"
"
"
        
"
git
remote
remove
unified
"
        
"
git
remote
remove
central
"
    
]
}
def
test_get_upstream_remote
(
repo
)
:
    
if
not
repo
.
vcs
=
=
"
git
"
:
        
return
    
vcs
=
get_repository_object
(
repo
.
dir
)
    
remote
=
vcs
.
get_mozilla_upstream_remote
(
)
    
repo
.
execute_next_step
(
)
    
remote
=
vcs
.
get_mozilla_upstream_remote
(
)
    
assert
remote
=
=
"
unified
"
"
Unified
remote
should
be
preferred
.
"
    
repo
.
execute_next_step
(
)
    
remote
=
vcs
.
get_mozilla_upstream_remote
(
)
    
assert
(
        
remote
=
=
"
central
"
    
)
"
Any
other
official
looking
remote
should
be
returned
second
.
"
    
repo
.
execute_next_step
(
)
    
remote
=
vcs
.
get_mozilla_upstream_remote
(
)
    
assert
(
        
remote
is
None
    
)
"
None
should
be
returned
if
an
official
remote
isn
'
t
found
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
