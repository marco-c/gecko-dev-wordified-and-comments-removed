import
copy
GROUP_BY_MAP
=
{
}
def
group_by
(
name
)
:
    
def
wrapper
(
func
)
:
        
GROUP_BY_MAP
[
name
]
=
func
        
return
func
    
return
wrapper
def
group_tasks
(
config
tasks
)
:
    
group_by_fn
=
GROUP_BY_MAP
[
config
[
'
group
-
by
'
]
]
    
groups
=
group_by_fn
(
config
tasks
)
    
for
combinations
in
groups
.
values
(
)
:
        
dependencies
=
[
copy
.
deepcopy
(
t
)
for
t
in
combinations
]
        
yield
dependencies
group_by
(
'
component
'
)
def
component_grouping
(
config
tasks
)
:
    
only_build_types
=
config
.
get
(
"
only
-
for
-
build
-
types
"
)
    
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
task
.
kind
not
in
config
.
get
(
"
kind
-
dependencies
"
[
]
)
:
            
continue
        
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
        
if
only_build_types
:
            
if
not
build_type
or
build_type
not
in
only_build_types
:
                
continue
        
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
'
component
'
)
=
=
'
all
'
        
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
tasks
in
groups
.
items
(
)
:
        
tasks
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
'
build
-
type
'
)
=
=
build_type
        
]
)
    
return
groups
group_by
(
'
build
-
type
'
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
    
only_build_types
=
config
.
get
(
"
only
-
for
-
build
-
types
"
)
    
for
task
in
tasks
:
        
if
task
.
kind
not
in
config
.
get
(
'
kind
-
dependencies
'
[
]
)
:
            
continue
        
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
'
build
-
type
'
)
        
if
only_build_types
:
            
if
not
build_type
or
build_type
not
in
only_build_types
:
                
continue
        
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
