from
taskgraph
.
util
.
dependencies
import
group_by
group_by
(
"
component
"
)
def
component_grouping
(
config
tasks
)
:
    
groups
=
{
}
    
for
task
in
tasks
:
        
component
=
task
.
attributes
.
get
(
"
component
"
)
        
if
component
=
=
"
all
"
:
            
continue
        
build_type
=
task
.
attributes
.
get
(
"
build
-
type
"
)
        
groups
.
setdefault
(
(
component
build_type
)
[
]
)
.
append
(
task
)
    
tasks_for_all_components
=
[
        
task
        
for
task
in
tasks
        
if
task
.
attributes
.
get
(
"
component
"
)
=
=
"
all
"
        
and
task
.
attributes
.
get
(
"
is_final_chunked_task
"
True
)
    
]
    
for
(
_
build_type
)
group_tasks
in
groups
.
items
(
)
:
        
group_tasks
.
extend
(
            
[
                
task
                
for
task
in
tasks_for_all_components
                
if
task
.
attributes
.
get
(
"
build
-
type
"
)
=
=
build_type
            
]
        
)
    
return
groups
.
values
(
)
group_by
(
"
build
-
type
"
)
def
build_type_grouping
(
config
tasks
)
:
    
groups
=
{
}
    
for
task
in
tasks
:
        
if
not
task
.
attributes
.
get
(
"
is_final_chunked_task
"
True
)
:
            
continue
        
build_type
=
task
.
attributes
.
get
(
"
build
-
type
"
)
        
groups
.
setdefault
(
build_type
[
]
)
.
append
(
task
)
    
return
groups
.
values
(
)
