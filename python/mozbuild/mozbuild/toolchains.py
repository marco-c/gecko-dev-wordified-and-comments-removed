import
os
import
six
def
toolchain_task_definitions
(
)
:
    
import
gecko_taskgraph
    
from
taskgraph
.
generator
import
load_tasks_for_kind
    
params
=
{
"
level
"
:
os
.
environ
.
get
(
"
MOZ_SCM_LEVEL
"
"
3
"
)
}
    
root_dir
=
os
.
path
.
join
(
        
os
.
path
.
dirname
(
__file__
)
"
.
.
"
"
.
.
"
"
.
.
"
"
taskcluster
"
"
ci
"
    
)
    
toolchains
=
load_tasks_for_kind
(
params
"
toolchain
"
root_dir
=
root_dir
)
    
aliased
=
{
}
    
for
t
in
toolchains
.
values
(
)
:
        
aliases
=
t
.
attributes
.
get
(
"
toolchain
-
alias
"
)
        
if
not
aliases
:
            
aliases
=
[
]
        
if
isinstance
(
aliases
six
.
text_type
)
:
            
aliases
=
[
aliases
]
        
for
alias
in
aliases
:
            
aliased
[
"
toolchain
-
{
}
"
.
format
(
alias
)
]
=
t
    
toolchains
.
update
(
aliased
)
    
return
toolchains
