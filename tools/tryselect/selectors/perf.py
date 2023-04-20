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
