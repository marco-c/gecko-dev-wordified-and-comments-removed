import
os
import
itertools
import
re
import
sys
from
contextlib
import
redirect_stdout
from
mozbuild
.
base
import
MozbuildObject
from
mozversioncontrol
import
get_repository_object
from
.
compare
import
CompareParser
from
.
.
push
import
push_to_try
generate_try_task_config
from
.
.
util
.
fzf
import
(
    
build_base_cmd
    
fzf_bootstrap
    
FZF_NOT_FOUND
    
setup_tasks_for_fzf
    
run_fzf
)
here
=
os
.
path
.
abspath
(
os
.
path
.
dirname
(
__file__
)
)
build
=
MozbuildObject
.
from_environment
(
cwd
=
here
)
PERFHERDER_BASE_URL
=
(
    
"
https
:
/
/
treeherder
.
mozilla
.
org
/
perfherder
/
"
    
"
compare
?
originalProject
=
try
&
originalRevision
=
%
s
&
newProject
=
try
&
newRevision
=
%
s
"
)
MAX_PERF_TASKS
=
300
class
PerfParser
(
CompareParser
)
:
    
name
=
"
perf
"
    
common_groups
=
[
"
push
"
"
task
"
]
    
task_configs
=
[
        
"
artifact
"
        
"
browsertime
"
        
"
disable
-
pgo
"
        
"
env
"
        
"
gecko
-
profile
"
        
"
path
"
        
"
rebuild
"
    
]
    
platforms
=
{
        
"
android
-
a51
"
:
{
            
"
query
"
:
"
'
android
'
a51
'
shippable
'
aarch64
"
            
"
platform
"
:
"
android
"
        
}
        
"
android
"
:
{
            
"
query
"
:
"
'
android
'
a51
'
shippable
'
aarch64
"
            
"
platform
"
:
"
android
"
        
}
        
"
windows
"
:
{
            
"
query
"
:
"
!
-
32
'
windows
'
shippable
"
            
"
platform
"
:
"
desktop
"
        
}
        
"
linux
"
:
{
            
"
query
"
:
"
!
clang
'
linux
'
shippable
"
            
"
platform
"
:
"
desktop
"
        
}
        
"
macosx
"
:
{
            
"
query
"
:
"
'
osx
'
shippable
"
            
"
platform
"
:
"
desktop
"
        
}
        
"
desktop
"
:
{
            
"
query
"
:
"
!
android
'
shippable
!
-
32
!
clang
"
            
"
platform
"
:
"
desktop
"
        
}
    
}
    
apps
=
{
        
"
firefox
"
:
{
            
"
query
"
:
"
!
chrom
!
geckoview
!
fenix
"
            
"
platforms
"
:
[
"
desktop
"
]
        
}
        
"
chrome
"
:
{
            
"
query
"
:
"
'
chrome
"
            
"
platforms
"
:
[
"
desktop
"
]
        
}
        
"
chromium
"
:
{
            
"
query
"
:
"
'
chromium
"
            
"
platforms
"
:
[
"
desktop
"
]
        
}
        
"
geckoview
"
:
{
            
"
query
"
:
"
'
geckoview
"
            
"
platforms
"
:
[
"
android
"
]
        
}
        
"
fenix
"
:
{
            
"
query
"
:
"
'
fenix
"
            
"
platforms
"
:
[
"
android
"
]
        
}
        
"
chrome
-
m
"
:
{
            
"
query
"
:
"
'
chrome
-
m
"
            
"
platforms
"
:
[
"
android
"
]
        
}
    
}
    
variants
=
{
        
"
no
-
fission
"
:
{
            
"
query
"
:
"
'
nofis
"
            
"
negation
"
:
"
!
nofis
"
            
"
platforms
"
:
[
"
android
"
]
            
"
apps
"
:
[
"
fenix
"
"
geckoview
"
]
        
}
        
"
bytecode
-
cached
"
:
{
            
"
query
"
:
"
'
bytecode
"
            
"
negation
"
:
"
!
bytecode
"
            
"
platforms
"
:
[
"
desktop
"
]
            
"
apps
"
:
[
"
firefox
"
]
        
}
        
"
live
-
sites
"
:
{
            
"
query
"
:
"
'
live
"
            
"
negation
"
:
"
!
live
"
            
"
platforms
"
:
[
"
desktop
"
"
android
"
]
            
"
apps
"
:
list
(
apps
.
keys
(
)
)
        
}
        
"
profiling
"
:
{
            
"
query
"
:
"
'
profil
"
            
"
negation
"
:
"
!
profil
"
            
"
platforms
"
:
[
"
desktop
"
"
android
"
]
            
"
apps
"
:
[
"
firefox
"
"
geckoview
"
"
fenix
"
]
        
}
    
}
    
categories
=
{
        
"
Pageload
"
:
{
            
"
query
"
:
"
'
browsertime
'
tp6
"
            
"
tasks
"
:
[
]
        
}
        
"
Pageload
(
essential
)
"
:
{
            
"
query
"
:
"
'
browsertime
'
tp6
'
essential
"
            
"
tasks
"
:
[
]
        
}
        
"
Pageload
(
live
)
"
:
{
            
"
query
"
:
"
'
browsertime
'
tp6
'
live
"
            
"
tasks
"
:
[
]
        
}
        
"
Bytecode
Cached
"
:
{
            
"
query
"
:
"
'
browsertime
'
bytecode
"
            
"
tasks
"
:
[
]
        
}
        
"
Responsiveness
"
:
{
            
"
query
"
:
"
'
browsertime
'
responsive
"
            
"
tasks
"
:
[
]
        
}
        
"
Benchmarks
"
:
{
            
"
query
"
:
"
'
browsertime
'
benchmark
"
            
"
tasks
"
:
[
]
        
}
    
}
    
arguments
=
[
        
[
            
[
"
-
-
show
-
all
"
]
            
{
                
"
action
"
:
"
store_true
"
                
"
default
"
:
False
                
"
help
"
:
"
Show
all
available
tasks
.
"
            
}
        
]
        
[
            
[
"
-
-
android
"
]
            
{
                
"
action
"
:
"
store_true
"
                
"
default
"
:
False
                
"
help
"
:
"
Show
android
test
categories
(
disabled
by
default
)
.
"
            
}
        
]
        
[
            
[
"
-
-
chrome
"
]
            
{
                
"
action
"
:
"
store_true
"
                
"
default
"
:
False
                
"
help
"
:
"
Show
tests
available
for
Chrome
-
based
browsers
"
                
"
(
disabled
by
default
)
.
"
            
}
        
]
        
[
            
[
"
-
-
live
-
sites
"
]
            
{
                
"
action
"
:
"
store_true
"
                
"
default
"
:
False
                
"
help
"
:
"
Run
tasks
with
live
sites
(
if
possible
)
.
"
                
"
You
can
also
use
the
live
-
sites
variant
.
"
            
}
        
]
        
[
            
[
"
-
-
profile
"
]
            
{
                
"
action
"
:
"
store_true
"
                
"
default
"
:
False
                
"
help
"
:
"
Run
tasks
with
profiling
(
if
possible
)
.
"
                
"
You
can
also
use
the
profiling
variant
.
"
            
}
        
]
        
[
            
[
"
-
-
variants
"
]
            
{
                
"
nargs
"
:
"
*
"
                
"
type
"
:
str
                
"
default
"
:
[
]
                
"
dest
"
:
"
requested_variants
"
                
"
choices
"
:
list
(
variants
.
keys
(
)
)
                
"
help
"
:
"
Show
android
test
categories
.
"
            
}
        
]
        
[
            
[
"
-
-
platforms
"
]
            
{
                
"
nargs
"
:
"
*
"
                
"
type
"
:
str
                
"
default
"
:
[
]
                
"
dest
"
:
"
requested_platforms
"
                
"
choices
"
:
list
(
platforms
.
keys
(
)
)
                
"
help
"
:
"
Select
specific
platforms
to
target
.
Android
only
"
                
"
available
with
-
-
android
.
"
            
}
        
]
        
[
            
[
"
-
-
apps
"
]
            
{
                
"
nargs
"
:
"
*
"
                
"
type
"
:
str
                
"
default
"
:
[
]
                
"
dest
"
:
"
requested_apps
"
                
"
choices
"
:
list
(
apps
.
keys
(
)
)
                
"
help
"
:
"
Select
specific
applications
to
target
.
"
            
}
        
]
    
]
    
def
get_tasks
(
base_cmd
queries
query_arg
=
None
candidate_tasks
=
None
)
:
        
cmd
=
base_cmd
[
:
]
        
if
query_arg
:
            
cmd
.
extend
(
[
"
-
f
"
query_arg
]
)
        
query_str
tasks
=
run_fzf
(
cmd
sorted
(
candidate_tasks
)
)
        
queries
.
append
(
query_str
)
        
return
set
(
tasks
)
    
def
get_perf_tasks
(
base_cmd
all_tg_tasks
perf_categories
)
:
        
selected_tasks
=
set
(
)
        
queries
=
[
]
        
selected_categories
=
PerfParser
.
get_tasks
(
            
base_cmd
queries
None
perf_categories
        
)
        
for
category
category_info
in
perf_categories
.
items
(
)
:
            
if
category
not
in
selected_categories
:
                
continue
            
print
(
"
Gathering
tasks
for
%
s
category
"
%
category
)
            
category_tasks
=
set
(
)
            
if
category_info
[
"
queries
"
]
:
                
print
(
"
Executing
queries
:
%
s
"
%
"
"
.
join
(
category_info
[
"
queries
"
]
)
)
                
for
perf_query
in
category_info
[
"
queries
"
]
:
                    
if
not
category_tasks
:
                        
category_tasks
|
=
PerfParser
.
get_tasks
(
                            
base_cmd
queries
perf_query
all_tg_tasks
                        
)
                    
else
:
                        
category_tasks
&
=
PerfParser
.
get_tasks
(
                            
base_cmd
queries
perf_query
category_tasks
                        
)
                    
if
len
(
category_tasks
)
=
=
0
:
                        
print
(
"
Failed
to
find
any
tasks
for
query
:
%
s
"
%
perf_query
)
                        
break
            
else
:
                
category_tasks
=
set
(
category_info
[
"
tasks
"
]
)
&
all_tg_tasks
                
if
category_tasks
!
=
set
(
category_info
[
"
tasks
"
]
)
:
                    
print
(
                        
"
Some
expected
tasks
could
not
be
found
:
%
s
"
                        
%
"
"
.
join
(
category_info
[
"
tasks
"
]
-
category_tasks
)
                    
)
            
if
not
category_tasks
:
                
print
(
"
Could
not
find
any
tasks
for
category
%
s
"
%
category
)
            
else
:
                
selected_tasks
|
=
category_tasks
        
if
len
(
selected_tasks
)
>
MAX_PERF_TASKS
:
            
print
(
                
"
That
'
s
a
lot
of
tests
selected
(
%
s
)
!
\
n
"
                
"
These
tests
won
'
t
be
triggered
.
If
this
was
unexpected
"
                
"
please
file
a
bug
in
Testing
:
:
Performance
.
"
%
MAX_PERF_TASKS
            
)
            
return
[
]
[
]
[
]
        
return
selected_tasks
selected_categories
queries
    
def
expand_categories
(
        
android
=
False
        
chrome
=
False
        
live_sites
=
False
        
profile
=
False
        
requested_variants
=
[
]
        
requested_platforms
=
[
]
        
requested_apps
=
[
]
    
)
:
        
"
"
"
Setup
the
perf
categories
.
        
This
has
multiple
steps
:
            
(
1
)
Expand
the
variants
to
all
possible
combinations
            
(
2
)
Expand
the
test
categories
for
all
valid
platform
+
app
combinations
            
(
3
)
Expand
the
categories
from
(
2
)
into
all
possible
combinations
                
by
combining
them
with
those
created
in
(
1
)
.
At
this
stage
                
we
also
check
to
make
sure
the
variant
combination
is
valid
                
in
the
sense
that
it
COULD
run
on
the
platform
.
It
may
still
                
be
undefined
.
        
We
make
use
of
global
queries
to
provide
a
thorough
protection
        
against
unwillingly
scheduling
tasks
we
very
often
don
'
t
want
.
        
Note
that
the
flags
are
not
intersectional
.
This
means
that
if
you
        
have
live_sites
=
True
and
profile
=
False
you
will
get
tasks
which
        
have
profiling
available
to
them
.
However
all
of
those
tasks
must
        
also
be
live
sites
.
        
"
"
"
        
expanded_categories
=
{
}
        
global_queries
=
[
]
        
if
live_sites
:
            
requested_variants
.
append
(
"
live
-
sites
"
)
        
else
:
            
global_queries
.
append
(
PerfParser
.
variants
[
"
live
-
sites
"
]
[
"
negation
"
]
)
        
if
profile
:
            
requested_variants
.
append
(
"
profiling
"
)
        
else
:
            
global_queries
.
append
(
PerfParser
.
variants
[
"
profiling
"
]
[
"
negation
"
]
)
        
if
not
chrome
:
            
global_queries
.
append
(
"
!
chrom
"
)
        
expanded_variants
=
[
            
variant_combination
            
for
set_size
in
range
(
len
(
PerfParser
.
variants
.
keys
(
)
)
+
1
)
            
for
variant_combination
in
itertools
.
combinations
(
                
list
(
PerfParser
.
variants
.
keys
(
)
)
set_size
            
)
        
]
        
for
category
category_info
in
PerfParser
.
categories
.
items
(
)
:
            
for
platform
platform_info
in
PerfParser
.
platforms
.
items
(
)
:
                
if
len
(
requested_platforms
)
>
0
and
platform
not
in
requested_platforms
:
                    
continue
                
platform_type
=
platform_info
[
"
platform
"
]
                
if
not
android
and
platform_type
=
=
"
android
"
:
                    
continue
                
new_category
=
category
+
"
%
s
"
%
platform
                
cur_cat
=
{
                    
"
queries
"
:
[
category_info
[
"
query
"
]
]
                    
+
[
platform_info
[
"
query
"
]
]
                    
+
global_queries
                    
"
tasks
"
:
category_info
[
"
tasks
"
]
                    
"
platform
"
:
platform_type
                
}
                
if
len
(
requested_apps
)
=
=
0
:
                    
expanded_categories
[
new_category
]
=
cur_cat
                
for
app
app_info
in
PerfParser
.
apps
.
items
(
)
:
                    
if
len
(
requested_apps
)
>
0
and
app
not
in
requested_apps
:
                        
continue
                    
if
app
.
lower
(
)
in
(
"
chrome
"
"
chromium
"
"
chrome
-
m
"
)
and
not
chrome
:
                        
continue
                    
if
platform_type
not
in
app_info
[
"
platforms
"
]
:
                        
continue
                    
new_app_category
=
new_category
+
"
%
s
"
%
app
                    
expanded_categories
[
new_app_category
]
=
{
                        
"
queries
"
:
cur_cat
[
"
queries
"
]
+
[
app_info
[
"
query
"
]
]
                        
"
tasks
"
:
category_info
[
"
tasks
"
]
                        
"
platform
"
:
platform_type
                    
}
        
if
len
(
requested_variants
)
>
0
:
            
new_categories
=
{
}
            
for
expanded_category
info
in
expanded_categories
.
items
(
)
:
                
for
variant_combination
in
expanded_variants
:
                    
if
not
variant_combination
:
                        
continue
                    
if
not
any
(
                        
variant
in
variant_combination
for
variant
in
requested_variants
                    
)
:
                        
continue
                    
runnable
=
True
                    
for
variant
in
variant_combination
:
                        
if
(
                            
info
[
"
platform
"
]
                            
not
in
PerfParser
.
variants
[
variant
]
[
"
platforms
"
]
                        
)
:
                            
runnable
=
False
                            
break
                    
if
not
runnable
:
                        
continue
                    
new_variant_category
=
expanded_category
+
"
%
s
"
%
"
+
"
.
join
(
                        
variant_combination
                    
)
                    
variant_queries
=
[
                        
v_info
[
"
query
"
]
                        
for
v
v_info
in
PerfParser
.
variants
.
items
(
)
                        
if
v
in
variant_combination
                    
]
                    
new_categories
[
new_variant_category
]
=
{
                        
"
queries
"
:
info
[
"
queries
"
]
+
variant_queries
                        
"
tasks
"
:
info
[
"
tasks
"
]
                    
}
                    
new_queries
=
[
]
                    
for
query
in
new_categories
[
new_variant_category
]
[
"
queries
"
]
:
                        
if
any
(
                            
[
                                
query
=
=
PerfParser
.
variants
.
get
(
variant
)
[
"
negation
"
]
                                
for
variant
in
variant_combination
                            
]
                        
)
:
                            
continue
                        
new_queries
.
append
(
query
)
                    
new_categories
[
new_variant_category
]
[
"
queries
"
]
=
new_queries
            
expanded_categories
.
update
(
new_categories
)
        
return
expanded_categories
