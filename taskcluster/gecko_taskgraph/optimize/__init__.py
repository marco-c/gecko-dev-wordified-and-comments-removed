"
"
"
The
objective
of
optimization
is
to
remove
as
many
tasks
from
the
graph
as
possible
as
efficiently
as
possible
thereby
delivering
useful
results
as
quickly
as
possible
.
For
example
ideally
if
only
a
test
script
is
modified
in
a
push
then
the
resulting
graph
contains
only
the
corresponding
test
suite
task
.
See
taskcluster
/
docs
/
optimization
.
rst
for
more
information
.
"
"
"
from
taskgraph
.
optimize
.
base
import
(
    
Alias
    
All
    
Any
    
Not
    
register_strategy
    
registry
)
from
taskgraph
.
util
.
python_path
import
import_sibling_modules
registry
.
pop
(
"
skip
-
unless
-
changed
"
None
)
import_sibling_modules
(
)
def
split_bugbug_arg
(
arg
substrategies
)
:
    
"
"
"
Split
args
for
bugbug
based
strategies
.
    
Many
bugbug
based
optimizations
require
passing
an
empty
dict
by
reference
    
to
communicate
to
downstream
strategies
.
This
function
passes
the
provided
    
arg
to
the
first
(
non
bugbug
)
strategies
and
a
shared
empty
dict
to
the
    
bugbug
strategy
and
all
substrategies
after
it
.
    
"
"
"
    
from
gecko_taskgraph
.
optimize
.
bugbug
import
BugBugPushSchedules
    
index
=
[
        
i
        
for
i
strategy
in
enumerate
(
substrategies
)
        
if
isinstance
(
strategy
BugBugPushSchedules
)
    
]
[
0
]
    
return
[
arg
]
*
index
+
[
{
}
]
*
(
len
(
substrategies
)
-
index
)
register_strategy
(
"
build
"
args
=
(
"
skip
-
unless
-
schedules
"
)
)
(
Alias
)
register_strategy
(
"
test
"
args
=
(
"
skip
-
unless
-
schedules
"
)
)
(
Alias
)
register_strategy
(
"
test
-
inclusive
"
args
=
(
"
skip
-
unless
-
schedules
"
)
)
(
Alias
)
register_strategy
(
"
test
-
verify
"
args
=
(
"
skip
-
unless
-
schedules
"
)
)
(
Alias
)
register_strategy
(
"
upload
-
symbols
"
args
=
(
"
never
"
)
)
(
Alias
)
register_strategy
(
"
reprocess
-
symbols
"
args
=
(
"
never
"
)
)
(
Alias
)
class
project
:
    
"
"
"
Strategies
that
should
be
applied
per
-
project
.
"
"
"
    
autoland
=
{
        
"
test
"
:
Any
(
            
All
(
                
"
skip
-
unless
-
backstop
"
                
Not
(
"
skip
-
unless
-
expanded
"
)
                
Any
(
                    
"
skip
-
unless
-
schedules
"
                    
"
bugbug
-
reduced
-
manifests
-
fallback
-
last
-
10
-
pushes
"
                    
"
platform
-
disperse
"
                    
split_args
=
split_bugbug_arg
                
)
            
)
            
All
(
                
"
skip
-
unless
-
expanded
"
                
Any
(
                    
"
skip
-
unless
-
schedules
"
                    
"
bugbug
-
reduced
-
manifests
-
fallback
-
low
"
                    
"
platform
-
disperse
"
                    
split_args
=
split_bugbug_arg
                
)
            
)
        
)
        
"
build
"
:
All
(
            
"
skip
-
unless
-
expanded
"
            
Any
(
                
"
skip
-
unless
-
schedules
"
                
"
bugbug
-
reduced
-
fallback
"
                
split_args
=
split_bugbug_arg
            
)
        
)
    
}
    
"
"
"
Strategy
overrides
that
apply
to
autoland
.
"
"
"
class
experimental
:
    
"
"
"
Experimental
strategies
either
under
development
or
used
as
benchmarks
.
    
These
run
as
"
shadow
-
schedulers
"
on
each
autoland
push
(
tier
3
)
and
/
or
can
be
used
    
with
.
/
mach
try
auto
.
E
.
g
:
        
.
/
mach
try
auto
-
-
strategy
relevant_tests
    
"
"
"
    
bugbug_tasks_medium
=
{
        
"
test
"
:
Any
(
            
"
skip
-
unless
-
schedules
"
"
bugbug
-
tasks
-
medium
"
split_args
=
split_bugbug_arg
        
)
    
}
    
"
"
"
Doesn
'
t
limit
platforms
medium
confidence
threshold
.
"
"
"
    
bugbug_tasks_high
=
{
        
"
test
"
:
Any
(
            
"
skip
-
unless
-
schedules
"
"
bugbug
-
tasks
-
high
"
split_args
=
split_bugbug_arg
        
)
    
}
    
"
"
"
Doesn
'
t
limit
platforms
high
confidence
threshold
.
"
"
"
    
bugbug_debug_disperse
=
{
        
"
test
"
:
Any
(
            
"
skip
-
unless
-
schedules
"
            
"
bugbug
-
low
"
            
"
platform
-
debug
"
            
"
platform
-
disperse
"
            
split_args
=
split_bugbug_arg
        
)
    
}
    
"
"
"
Restricts
tests
to
debug
platforms
.
"
"
"
    
bugbug_disperse_low
=
{
        
"
test
"
:
Any
(
            
"
skip
-
unless
-
schedules
"
            
"
bugbug
-
low
"
            
"
platform
-
disperse
"
            
split_args
=
split_bugbug_arg
        
)
    
}
    
"
"
"
Disperse
tests
across
platforms
low
confidence
threshold
.
"
"
"
    
bugbug_disperse_medium
=
{
        
"
test
"
:
Any
(
            
"
skip
-
unless
-
schedules
"
            
"
bugbug
-
medium
"
            
"
platform
-
disperse
"
            
split_args
=
split_bugbug_arg
        
)
    
}
    
"
"
"
Disperse
tests
across
platforms
medium
confidence
threshold
.
"
"
"
    
bugbug_disperse_reduced_medium
=
{
        
"
test
"
:
Any
(
            
"
skip
-
unless
-
schedules
"
            
"
bugbug
-
reduced
-
manifests
"
            
"
platform
-
disperse
"
            
split_args
=
split_bugbug_arg
        
)
    
}
    
"
"
"
Disperse
tests
across
platforms
medium
confidence
threshold
with
reduced
tasks
.
"
"
"
    
bugbug_reduced_manifests_config_selection_low
=
{
        
"
test
"
:
Any
(
            
"
skip
-
unless
-
schedules
"
            
"
bugbug
-
reduced
-
manifests
-
config
-
selection
-
low
"
            
split_args
=
split_bugbug_arg
        
)
    
}
    
"
"
"
Choose
configs
selected
by
bugbug
low
confidence
threshold
with
reduced
tasks
.
"
"
"
    
bugbug_reduced_manifests_config_selection_medium
=
{
        
"
test
"
:
Any
(
            
"
skip
-
unless
-
schedules
"
            
"
bugbug
-
reduced
-
manifests
-
config
-
selection
"
            
split_args
=
split_bugbug_arg
        
)
    
}
    
"
"
"
Choose
configs
selected
by
bugbug
medium
confidence
threshold
with
reduced
tasks
.
"
"
"
    
bugbug_disperse_medium_no_unseen
=
{
        
"
test
"
:
Any
(
            
"
skip
-
unless
-
schedules
"
            
"
bugbug
-
medium
"
            
"
platform
-
disperse
-
no
-
unseen
"
            
split_args
=
split_bugbug_arg
        
)
    
}
    
"
"
"
Disperse
tests
across
platforms
(
no
modified
for
unseen
configurations
)
medium
confidence
    
threshold
.
"
"
"
    
bugbug_disperse_medium_only_one
=
{
        
"
test
"
:
Any
(
            
"
skip
-
unless
-
schedules
"
            
"
bugbug
-
medium
"
            
"
platform
-
disperse
-
only
-
one
"
            
split_args
=
split_bugbug_arg
        
)
    
}
    
"
"
"
Disperse
tests
across
platforms
(
one
platform
per
group
)
medium
confidence
threshold
.
"
"
"
    
bugbug_disperse_high
=
{
        
"
test
"
:
Any
(
            
"
skip
-
unless
-
schedules
"
            
"
bugbug
-
high
"
            
"
platform
-
disperse
"
            
split_args
=
split_bugbug_arg
        
)
    
}
    
"
"
"
Disperse
tests
across
platforms
high
confidence
threshold
.
"
"
"
    
bugbug_reduced
=
{
        
"
test
"
:
Any
(
            
"
skip
-
unless
-
schedules
"
"
bugbug
-
reduced
"
split_args
=
split_bugbug_arg
        
)
    
}
    
"
"
"
Use
the
reduced
set
of
tasks
(
and
no
groups
)
chosen
by
bugbug
.
"
"
"
    
bugbug_reduced_high
=
{
        
"
test
"
:
Any
(
            
"
skip
-
unless
-
schedules
"
"
bugbug
-
reduced
-
high
"
split_args
=
split_bugbug_arg
        
)
    
}
    
"
"
"
Use
the
reduced
set
of
tasks
(
and
no
groups
)
chosen
by
bugbug
high
    
confidence
threshold
.
"
"
"
    
relevant_tests
=
{
        
"
test
"
:
Any
(
"
skip
-
unless
-
schedules
"
"
skip
-
unless
-
has
-
relevant
-
tests
"
)
    
}
    
"
"
"
Runs
task
containing
tests
in
the
same
directories
as
modified
files
.
"
"
"
class
ExperimentalOverride
:
    
"
"
"
Overrides
dictionaries
that
are
stored
in
a
container
with
new
values
.
    
This
can
be
used
to
modify
all
strategies
in
a
collection
the
same
way
    
presumably
with
strategies
affecting
kinds
of
tasks
tangential
to
the
    
current
context
.
    
Args
:
        
base
(
object
)
:
A
container
class
supporting
attribute
access
.
        
overrides
(
dict
)
:
Values
to
update
any
accessed
dictionaries
with
.
    
"
"
"
    
def
__init__
(
self
base
overrides
)
:
        
self
.
base
=
base
        
self
.
overrides
=
overrides
    
def
__getattr__
(
self
name
)
:
        
val
=
getattr
(
self
.
base
name
)
.
copy
(
)
        
for
name
strategy
in
self
.
overrides
.
items
(
)
:
            
if
isinstance
(
strategy
str
)
and
strategy
.
startswith
(
"
base
:
"
)
:
                
strategy
=
val
[
strategy
[
len
(
"
base
:
"
)
:
]
]
            
val
[
name
]
=
strategy
        
return
val
tryselect
=
ExperimentalOverride
(
    
experimental
    
{
        
"
build
"
:
Any
(
            
"
skip
-
unless
-
schedules
"
"
bugbug
-
reduced
"
split_args
=
split_bugbug_arg
        
)
        
"
test
-
verify
"
:
"
base
:
test
"
        
"
upload
-
symbols
"
:
Alias
(
"
always
"
)
        
"
reprocess
-
symbols
"
:
Alias
(
"
always
"
)
    
}
)
