"
"
"
Add
dependencies
to
release
tasks
.
"
"
"
from
taskgraph
.
transforms
.
base
import
TransformSequence
PHASES
=
[
"
build
"
"
promote
"
"
push
"
"
ship
"
]
transforms
=
TransformSequence
(
)
transforms
.
add
def
add_dependencies
(
config
jobs
)
:
    
for
job
in
jobs
:
        
dependencies
=
{
}
        
product
=
job
.
get
(
"
shipping
-
product
"
)
        
phase
=
job
.
get
(
"
shipping
-
phase
"
)
        
if
product
is
None
:
            
continue
        
for
dep_task
in
config
.
kind_dependencies_tasks
.
values
(
)
:
            
dep_phase
=
dep_task
.
attributes
.
get
(
"
shipping_phase
"
)
            
if
dep_phase
and
PHASES
.
index
(
dep_phase
)
>
PHASES
.
index
(
phase
)
:
                
continue
            
if
dep_task
.
attributes
.
get
(
"
build_platform
"
)
and
job
.
get
(
                
"
attributes
"
{
}
            
)
.
get
(
"
build_platform
"
)
:
                
if
(
                    
dep_task
.
attributes
[
"
build_platform
"
]
                    
!
=
job
[
"
attributes
"
]
[
"
build_platform
"
]
                
)
:
                    
continue
            
if
product
=
=
"
firefox
-
android
"
:
                
from
android_taskgraph
.
release_type
import
does_task_match_release_type
                
if
not
does_task_match_release_type
(
                    
dep_task
config
.
params
[
"
release_type
"
]
                
)
:
                    
continue
            
if
(
                
dep_task
.
task
.
get
(
"
shipping
-
product
"
)
=
=
product
                
or
dep_task
.
attributes
.
get
(
"
shipping_product
"
)
=
=
product
            
)
:
                
dependencies
[
dep_task
.
label
]
=
dep_task
.
label
        
job
.
setdefault
(
"
dependencies
"
{
}
)
.
update
(
dependencies
)
        
yield
job
