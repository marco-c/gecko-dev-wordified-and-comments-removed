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
git
remote
add
blah
https
:
/
/
example
.
com
/
blah
"
        
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
        
git
remote
add
try
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
try
        
"
"
"
    
]
}
def
test_get_upstream_remotes
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
    
repo
.
execute_next_step
(
)
    
vcs
=
get_repository_object
(
repo
.
dir
)
    
remotes
=
vcs
.
get_mozilla_remote_args
(
)
    
assert
remotes
=
=
[
        
"
-
-
remotes
"
    
]
"
Default
-
-
remotes
passed
without
finding
official
remote
.
"
    
repo
.
execute_next_step
(
)
    
remotes
=
sorted
(
vcs
.
get_mozilla_remote_args
(
)
)
    
assert
remotes
=
=
[
        
"
-
-
remotes
=
central
"
        
"
-
-
remotes
=
unified
"
    
]
"
Multiple
non
-
try
remote
arguments
should
be
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
