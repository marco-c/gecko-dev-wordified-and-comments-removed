from
gecko_taskgraph
.
transforms
.
base
import
TransformSequence
from
gecko_taskgraph
.
util
.
platforms
import
platform_family
transforms
=
TransformSequence
(
)
transforms
.
add
def
set_build_attributes
(
config
jobs
)
:
    
"
"
"
    
Set
the
build_platform
and
build_type
attributes
based
on
the
job
name
.
    
Although
not
all
jobs
using
this
transform
are
actual
"
builds
"
the
try
    
option
syntax
treats
them
as
such
and
this
arranges
the
attributes
    
appropriately
for
that
purpose
.
    
"
"
"
    
for
job
in
jobs
:
        
build_platform
build_type
=
job
[
"
name
"
]
.
split
(
"
/
"
)
        
if
build_type
=
=
"
pgo
"
:
            
build_platform
=
build_platform
+
"
-
pgo
"
            
build_type
=
"
opt
"
        
attributes
=
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
        
attributes
.
update
(
            
{
                
"
build_platform
"
:
build_platform
                
"
build_type
"
:
build_type
            
}
        
)
        
yield
job
transforms
.
add
def
set_schedules_optimization
(
config
jobs
)
:
    
"
"
"
Set
the
skip
-
unless
-
affected
optimization
based
on
the
build
platform
.
"
"
"
    
for
job
in
jobs
:
        
if
"
when
"
in
job
:
            
yield
job
            
continue
        
build_platform
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
        
job
.
setdefault
(
"
optimization
"
{
"
build
"
:
[
platform_family
(
build_platform
)
]
}
)
        
yield
job
