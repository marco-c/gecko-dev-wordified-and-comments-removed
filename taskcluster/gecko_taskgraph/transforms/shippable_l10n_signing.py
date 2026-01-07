"
"
"
Transform
the
signing
task
into
an
actual
task
description
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
from
taskgraph
.
util
.
dependencies
import
get_primary_dependency
from
taskgraph
.
util
.
treeherder
import
join_symbol
from
gecko_taskgraph
.
util
.
attributes
import
copy_attributes_from_dependent_job
from
gecko_taskgraph
.
util
.
signed_artifacts
import
(
    
generate_specifications_of_artifacts_to_sign
)
transforms
=
TransformSequence
(
)
transforms
.
add
def
make_signing_description
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
        
dep_job
=
get_primary_dependency
(
config
job
)
        
symbol
=
job
.
get
(
"
treeherder
"
{
}
)
.
get
(
"
symbol
"
"
Bs
"
)
        
symbol
=
"
{
}
{
}
"
.
format
(
symbol
dep_job
.
attributes
.
get
(
"
l10n_chunk
"
)
)
        
group
=
"
L10n
"
        
job
[
"
treeherder
"
]
=
{
            
"
symbol
"
:
join_symbol
(
group
symbol
)
        
}
        
yield
job
transforms
.
add
def
define_upstream_artifacts
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
        
dep_job
=
get_primary_dependency
(
config
job
)
        
job
.
setdefault
(
"
attributes
"
{
}
)
.
update
(
            
copy_attributes_from_dependent_job
(
dep_job
)
        
)
        
if
dep_job
.
attributes
.
get
(
"
chunk_locales
"
)
:
            
job
[
"
attributes
"
]
[
"
chunk_locales
"
]
=
dep_job
.
attributes
.
get
(
"
chunk_locales
"
)
        
locale_specifications
=
generate_specifications_of_artifacts_to_sign
(
            
config
            
job
            
keep_locale_template
=
True
            
dep_kind
=
dep_job
.
kind
        
)
        
upstream_artifacts
=
[
]
        
for
spec
in
locale_specifications
:
            
upstream_task_type
=
"
l10n
"
            
if
dep_job
.
kind
.
endswith
(
(
"
-
mac
-
notarization
"
"
-
mac
-
signing
"
)
)
:
                
upstream_task_type
=
"
scriptworker
"
            
upstream_artifacts
.
append
(
                
{
                    
"
taskId
"
:
{
"
task
-
reference
"
:
f
"
<
{
dep_job
.
kind
}
>
"
}
                    
"
taskType
"
:
upstream_task_type
                    
"
paths
"
:
sorted
(
                        
{
                            
path_template
.
format
(
locale
=
locale
)
                            
for
locale
in
dep_job
.
attributes
.
get
(
"
chunk_locales
"
[
]
)
                            
for
path_template
in
spec
[
"
artifacts
"
]
                        
}
                    
)
                    
"
formats
"
:
spec
[
"
formats
"
]
                
}
            
)
        
job
[
"
upstream
-
artifacts
"
]
=
upstream_artifacts
        
yield
job
