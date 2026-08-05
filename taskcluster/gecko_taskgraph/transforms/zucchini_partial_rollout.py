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
zucchini_transforms
=
TransformSequence
(
)
partials_transforms
=
TransformSequence
(
)
LEGACY_PARTIALS_PROJECTS
=
{
    
"
mozilla
-
beta
"
    
"
mozilla
-
release
"
    
"
mozilla
-
esr115
"
    
"
mozilla
-
esr140
"
}
partials_transforms
.
add
def
filter_legacy_partials_by_project
(
config
tasks
)
:
    
"
"
"
Only
generate
legacy
"
partials
"
tasks
on
legacy
release
channels
.
    
partials
-
zucchini
is
used
on
every
other
project
so
on
non
-
legacy
projects
    
we
skip
generating
the
legacy
"
partials
"
tasks
entirely
.
This
is
the
inverse
    
of
the
filtering
applied
by
the
zucchini_transforms
below
.
    
"
"
"
    
if
config
.
params
[
"
project
"
]
not
in
LEGACY_PARTIALS_PROJECTS
:
        
return
    
yield
from
tasks
zucchini_transforms
.
add
def
filter_partials_by_project
(
config
tasks
)
:
    
"
"
"
Control
the
rollout
of
partials
-
zucchini
across
release
channels
.
    
This
transform
manages
the
gradual
transition
from
the
legacy
"
partials
"
implementation
    
to
the
new
"
partials
-
zucchini
"
implementation
.
It
ensures
that
partials
-
zucchini
is
only
    
used
on
nightly
builds
allowing
thorough
testing
before
the
implementation
rides
the
    
train
to
beta
release
and
ESR
channels
.
    
The
transform
filters
tasks
based
on
their
primary
dependency
(
partials
or
partials
-
zucchini
)
    
and
the
current
project
/
channel
ensuring
the
appropriate
implementation
is
used
for
each
    
release
channel
.
    
"
"
"
    
for
task
in
tasks
:
        
primary_dep
=
get_primary_dependency
(
config
task
)
        
assert
primary_dep
        
if
primary_dep
.
kind
not
in
(
            
"
partials
"
            
"
partials
-
zucchini
"
            
"
partials
-
zucchini
-
l10n
"
        
)
:
            
yield
task
            
continue
        
if
(
            
primary_dep
.
kind
=
=
"
partials
"
            
and
config
.
params
[
"
project
"
]
not
in
LEGACY_PARTIALS_PROJECTS
        
)
:
            
continue
        
if
(
            
primary_dep
.
kind
in
(
"
partials
-
zucchini
"
"
partials
-
zucchini
-
l10n
"
)
            
and
config
.
params
[
"
project
"
]
in
LEGACY_PARTIALS_PROJECTS
        
)
:
            
continue
        
yield
task
