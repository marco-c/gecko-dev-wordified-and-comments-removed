import
re
from
typing
import
Literal
Union
from
taskgraph
.
util
.
attributes
import
_match_run_on
INTEGRATION_PROJECTS
=
{
    
"
autoland
"
}
TRUNK_PROJECTS
=
INTEGRATION_PROJECTS
|
{
"
mozilla
-
central
"
"
comm
-
central
"
}
PROJECT_RELEASE_BRANCHES
:
dict
[
str
Union
[
list
[
str
]
Literal
[
True
]
]
]
=
{
    
"
firefox
"
:
[
        
"
main
"
        
"
beta
"
        
"
release
"
        
"
esr115
"
        
"
esr128
"
        
"
esr140
"
    
]
    
"
mozilla
-
central
"
:
True
    
"
mozilla
-
beta
"
:
True
    
"
mozilla
-
release
"
:
True
    
"
mozilla
-
esr115
"
:
True
    
"
mozilla
-
esr128
"
:
True
    
"
mozilla
-
esr140
"
:
True
    
"
comm
-
central
"
:
True
    
"
comm
-
beta
"
:
True
    
"
comm
-
release
"
:
True
    
"
comm
-
esr115
"
:
True
    
"
comm
-
esr128
"
:
True
    
"
comm
-
esr140
"
:
True
    
"
pine
"
:
True
    
"
larch
"
:
True
    
"
maple
"
:
True
    
"
cypress
"
:
True
}
RELEASE_PROJECTS
=
set
(
PROJECT_RELEASE_BRANCHES
)
RELEASE_PROMOTION_PROJECTS
=
{
    
"
jamun
"
    
"
maple
"
    
"
try
"
    
"
try
-
comm
-
central
"
}
|
RELEASE_PROJECTS
TEMPORARY_PROJECTS
=
set
(
    
{
        
"
oak
"
    
}
)
TRY_PROJECTS
=
{
    
"
staging
-
firefox
"
    
"
try
"
    
"
try
-
comm
-
central
"
}
ALL_PROJECTS
=
RELEASE_PROMOTION_PROJECTS
|
TRUNK_PROJECTS
|
TEMPORARY_PROJECTS
RUN_ON_PROJECT_ALIASES
=
{
    
"
all
"
:
lambda
params
:
True
    
"
integration
"
:
lambda
params
:
(
        
params
[
"
project
"
]
in
INTEGRATION_PROJECTS
or
params
[
"
project
"
]
=
=
"
toolchains
"
    
)
    
"
release
"
:
lambda
params
:
(
        
release_level
(
params
)
=
=
"
production
"
or
params
[
"
project
"
]
=
=
"
toolchains
"
    
)
    
"
trunk
"
:
lambda
params
:
(
        
params
[
"
project
"
]
in
TRUNK_PROJECTS
or
params
[
"
project
"
]
=
=
"
toolchains
"
    
)
    
"
trunk
-
only
"
:
lambda
params
:
params
[
"
project
"
]
in
TRUNK_PROJECTS
    
"
autoland
"
:
lambda
params
:
params
[
"
project
"
]
in
(
"
autoland
"
"
toolchains
"
)
    
"
autoland
-
only
"
:
lambda
params
:
params
[
"
project
"
]
=
=
"
autoland
"
    
"
mozilla
-
central
"
:
lambda
params
:
params
[
"
project
"
]
    
in
(
"
mozilla
-
central
"
"
toolchains
"
)
    
"
mozilla
-
central
-
only
"
:
lambda
params
:
params
[
"
project
"
]
=
=
"
mozilla
-
central
"
}
_COPYABLE_ATTRIBUTES
=
(
    
"
accepted
-
mar
-
channel
-
ids
"
    
"
artifact_map
"
    
"
artifact_prefix
"
    
"
build_platform
"
    
"
build_type
"
    
"
l10n_chunk
"
    
"
locale
"
    
"
mar
-
channel
-
id
"
    
"
maven_packages
"
    
"
nightly
"
    
"
required_signoffs
"
    
"
shippable
"
    
"
shipping_phase
"
    
"
shipping_product
"
    
"
signed
"
    
"
stub
-
installer
"
    
"
update
-
channel
"
)
def
match_run_on_projects
(
params
run_on_projects
)
:
    
"
"
"
Determine
whether
the
given
project
is
included
in
the
run
-
on
-
projects
    
parameter
applying
expansions
for
things
like
"
integration
"
mentioned
in
    
the
attribute
documentation
.
"
"
"
    
aliases
=
RUN_ON_PROJECT_ALIASES
.
keys
(
)
    
run_aliases
=
set
(
aliases
)
&
set
(
run_on_projects
)
    
if
run_aliases
:
        
if
any
(
RUN_ON_PROJECT_ALIASES
[
alias
]
(
params
)
for
alias
in
run_aliases
)
:
            
return
True
    
return
params
[
"
project
"
]
in
run_on_projects
def
match_run_on_hg_branches
(
hg_branch
run_on_hg_branches
)
:
    
"
"
"
Determine
whether
the
given
project
is
included
in
the
run
-
on
-
hg
-
branches
    
parameter
.
Allows
'
all
'
.
"
"
"
    
if
"
all
"
in
run_on_hg_branches
:
        
return
True
    
for
expected_hg_branch_pattern
in
run_on_hg_branches
:
        
if
re
.
match
(
expected_hg_branch_pattern
hg_branch
)
:
            
return
True
    
return
False
match_run_on_repo_type
=
_match_run_on
def
copy_attributes_from_dependent_job
(
dep_job
denylist
=
(
)
)
:
    
return
{
        
attr
:
dep_job
.
attributes
[
attr
]
        
for
attr
in
_COPYABLE_ATTRIBUTES
        
if
attr
in
dep_job
.
attributes
and
attr
not
in
denylist
    
}
def
sorted_unique_list
(
*
args
)
:
    
"
"
"
Join
one
or
more
lists
and
return
a
sorted
list
of
unique
members
"
"
"
    
combined
=
set
(
)
.
union
(
*
args
)
    
return
sorted
(
combined
)
def
release_level
(
params
)
:
    
"
"
"
    
Whether
this
is
a
staging
release
or
not
.
    
:
return
str
:
One
of
"
production
"
or
"
staging
"
.
    
"
"
"
    
if
branches
:
=
PROJECT_RELEASE_BRANCHES
.
get
(
params
.
get
(
"
project
"
)
)
:
        
if
branches
is
True
:
            
return
"
production
"
        
m
=
re
.
match
(
r
"
refs
/
heads
/
(
\
S
+
)
"
params
[
"
head_ref
"
]
)
        
if
m
is
not
None
and
m
.
group
(
1
)
in
branches
:
            
return
"
production
"
    
return
"
staging
"
def
is_try
(
params
)
:
    
"
"
"
    
Determine
whether
this
graph
is
being
built
on
a
try
project
or
for
    
mach
try
fuzzy
.
    
"
"
"
    
return
"
try
"
in
params
[
"
project
"
]
or
params
[
"
try_mode
"
]
=
=
"
try_select
"
def
task_name
(
task
)
:
    
if
task
.
label
.
startswith
(
task
.
kind
+
"
-
"
)
:
        
return
task
.
label
[
len
(
task
.
kind
)
+
1
:
]
    
raise
AttributeError
(
f
"
Task
{
task
.
label
}
does
not
have
a
name
.
"
)
