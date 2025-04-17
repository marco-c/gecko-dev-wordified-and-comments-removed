import
mozunit
from
mozversioncontrol
import
get_repository_object
def
test_context_manager
(
repo
)
:
    
cmd
=
{
        
"
git
"
:
[
"
show
"
"
-
-
no
-
patch
"
]
        
"
hg
"
:
[
"
tip
"
]
        
"
jj
"
:
[
"
show
"
"
-
"
]
    
}
[
repo
.
vcs
]
    
vcs
=
get_repository_object
(
repo
.
dir
)
    
output_subprocess
=
vcs
.
_run
(
*
cmd
)
    
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
        
assert
vcs
.
_client
.
server
is
None
    
assert
"
Initial
commit
"
in
output_subprocess
    
with
vcs
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
            
assert
vcs
.
_client
.
server
is
not
None
        
output_client
=
vcs
.
_run
(
*
cmd
)
    
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
        
assert
vcs
.
_client
.
server
is
None
    
assert
output_subprocess
=
=
output_client
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
