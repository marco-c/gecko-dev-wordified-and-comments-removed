import
os
from
mozbuild
.
base
import
MozbuildObject
from
mozversioncontrol
import
get_repository_object
from
tryselect
.
cli
import
BaseTryParser
from
.
fuzzy
import
run
as
fuzzy_run
from
.
again
import
run
as
again_run
here
=
os
.
path
.
abspath
(
os
.
path
.
dirname
(
__file__
)
)
build
=
MozbuildObject
.
from_environment
(
cwd
=
here
)
class
CompareParser
(
BaseTryParser
)
:
    
name
=
"
compare
"
    
arguments
=
[
        
[
            
[
"
-
cc
"
"
-
-
compare
-
commit
"
]
            
{
                
"
default
"
:
None
                
"
help
"
:
"
The
commit
that
you
want
to
compare
your
current
revision
with
"
            
}
        
]
    
]
    
common_groups
=
[
"
task
"
]
    
task_configs
=
[
        
"
rebuild
"
    
]
def
run
(
compare_commit
=
None
*
*
kwargs
)
:
    
vcs
=
get_repository_object
(
build
.
topsrcdir
)
    
if
compare_commit
is
None
:
        
compare_commit
=
vcs
.
base_ref
    
if
vcs
.
branch
:
        
current_revision_ref
=
vcs
.
branch
    
else
:
        
current_revision_ref
=
vcs
.
head_ref
    
try
:
        
fuzzy_run
(
*
*
kwargs
)
        
vcs
.
update
(
compare_commit
)
        
again_run
(
)
    
finally
:
        
vcs
.
update
(
current_revision_ref
)
