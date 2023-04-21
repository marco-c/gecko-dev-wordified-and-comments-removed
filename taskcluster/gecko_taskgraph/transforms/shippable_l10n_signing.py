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
job
[
"
primary
-
dependency
"
]
        
job
[
"
depname
"
]
=
dep_job
.
label
        
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
job
[
"
primary
-
dependency
"
]
        
upstream_artifact_task
=
job
.
pop
(
"
upstream
-
artifact
-
task
"
dep_job
)
        
job
[
"
attributes
"
]
=
copy_attributes_from_dependent_job
(
dep_job
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
upstream_artifact_task
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
"
notarization
"
in
upstream_artifact_task
.
kind
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
upstream_artifact_task
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
upstream_artifact_task
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
