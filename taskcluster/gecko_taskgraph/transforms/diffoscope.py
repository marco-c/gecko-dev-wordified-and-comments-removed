"
"
"
This
transform
construct
tasks
to
perform
diffs
between
builds
as
defined
in
kind
.
yml
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
schema
import
Schema
from
taskgraph
.
util
.
taskcluster
import
get_artifact_path
from
voluptuous
import
Any
Optional
Required
from
gecko_taskgraph
.
transforms
.
task
import
task_description_schema
index_or_string
=
Any
(
    
str
    
{
Required
(
"
index
-
search
"
)
:
str
}
)
diff_description_schema
=
Schema
(
{
    
Required
(
"
name
"
)
:
str
    
Required
(
"
tier
"
)
:
int
    
Required
(
"
symbol
"
)
:
str
    
Optional
(
"
task
-
from
"
)
:
str
    
Required
(
"
original
"
)
:
index_or_string
    
Required
(
"
new
"
)
:
index_or_string
    
Optional
(
"
args
"
)
:
str
    
Optional
(
"
extra
-
args
"
)
:
str
    
Optional
(
"
fail
-
on
-
diff
"
)
:
bool
    
Optional
(
"
artifact
"
)
:
str
    
Optional
(
"
unpack
"
)
:
bool
    
Optional
(
"
pre
-
diff
-
commands
"
)
:
[
str
]
    
Optional
(
"
run
-
on
-
projects
"
)
:
task_description_schema
[
"
run
-
on
-
projects
"
]
    
Optional
(
"
run
-
on
-
repo
-
type
"
)
:
task_description_schema
[
"
run
-
on
-
repo
-
type
"
]
    
Optional
(
"
optimization
"
)
:
task_description_schema
[
"
optimization
"
]
}
)
transforms
=
TransformSequence
(
)
transforms
.
add_validate
(
diff_description_schema
)
transforms
.
add
def
fill_template
(
config
tasks
)
:
    
dummy_tasks
=
{
}
    
for
task
in
tasks
:
        
name
=
task
[
"
name
"
]
        
deps
=
{
}
        
urls
=
{
}
        
previous_artifact
=
None
        
artifact
=
task
.
get
(
"
artifact
"
)
        
for
k
in
(
"
original
"
"
new
"
)
:
            
value
=
task
[
k
]
            
if
isinstance
(
value
str
)
:
                
deps
[
k
]
=
value
                
dep_name
=
k
                
os_hint
=
value
            
else
:
                
index
=
value
[
"
index
-
search
"
]
                
if
index
not
in
dummy_tasks
:
                    
dummy_tasks
[
index
]
=
{
                        
"
label
"
:
"
index
-
search
-
"
+
index
                        
"
description
"
:
index
                        
"
worker
-
type
"
:
"
invalid
/
always
-
optimized
"
                        
"
run
"
:
{
                            
"
using
"
:
"
always
-
optimized
"
                        
}
                        
"
optimization
"
:
{
                            
"
index
-
search
"
:
[
index
]
                        
}
                    
}
                    
yield
dummy_tasks
[
index
]
                
deps
[
index
]
=
"
index
-
search
-
"
+
index
                
dep_name
=
index
                
os_hint
=
index
.
split
(
"
.
"
)
[
-
1
]
            
if
artifact
:
                
pass
            
elif
"
linux
"
in
os_hint
:
                
artifact
=
"
target
.
tar
.
xz
"
            
elif
"
macosx
"
in
os_hint
:
                
artifact
=
"
target
.
dmg
"
            
elif
"
android
"
in
os_hint
:
                
artifact
=
"
target
.
apk
"
            
elif
"
win
"
in
os_hint
:
                
artifact
=
"
target
.
zip
"
            
else
:
                
raise
Exception
(
f
"
Cannot
figure
out
the
OS
for
{
value
!
r
}
"
)
            
if
previous_artifact
is
not
None
and
previous_artifact
!
=
artifact
:
                
raise
Exception
(
"
Cannot
compare
builds
from
different
OSes
"
)
            
urls
[
k
]
=
{
                
"
artifact
-
reference
"
:
f
"
<
{
dep_name
}
/
{
get_artifact_path
(
task
artifact
)
}
>
"
            
}
            
previous_artifact
=
artifact
        
taskdesc
=
{
            
"
label
"
:
"
diff
-
"
+
name
            
"
description
"
:
name
            
"
treeherder
"
:
{
                
"
symbol
"
:
task
[
"
symbol
"
]
                
"
platform
"
:
"
diff
/
opt
"
                
"
kind
"
:
"
other
"
                
"
tier
"
:
task
[
"
tier
"
]
            
}
            
"
worker
-
type
"
:
"
b
-
linux
"
            
"
worker
"
:
{
                
"
docker
-
image
"
:
{
"
in
-
tree
"
:
"
diffoscope
"
}
                
"
artifacts
"
:
[
                    
{
                        
"
type
"
:
"
file
"
                        
"
path
"
:
f
"
/
builds
/
worker
/
{
f
}
"
                        
"
name
"
:
f
"
public
/
{
f
}
"
                    
}
                    
for
f
in
(
                        
"
diff
.
html
"
                        
"
diff
.
txt
"
                    
)
                
]
                
"
env
"
:
{
                    
"
ORIG_URL
"
:
urls
[
"
original
"
]
                    
"
NEW_URL
"
:
urls
[
"
new
"
]
                    
"
DIFFOSCOPE_ARGS
"
:
"
"
.
join
(
                        
task
[
k
]
for
k
in
(
"
args
"
"
extra
-
args
"
)
if
k
in
task
                    
)
                    
"
PRE_DIFF
"
:
"
;
"
.
join
(
task
.
get
(
"
pre
-
diff
-
commands
"
[
]
)
)
                
}
                
"
max
-
run
-
time
"
:
1800
            
}
            
"
run
"
:
{
                
"
using
"
:
"
run
-
task
"
                
"
checkout
"
:
task
.
get
(
"
unpack
"
False
)
                
"
command
"
:
"
/
builds
/
worker
/
bin
/
get_and_diffoscope
{
}
{
}
"
.
format
(
                    
"
-
-
unpack
"
if
task
.
get
(
"
unpack
"
)
else
"
"
                    
"
-
-
fail
"
if
task
.
get
(
"
fail
-
on
-
diff
"
)
else
"
"
                
)
            
}
            
"
dependencies
"
:
deps
            
"
optimization
"
:
task
.
get
(
"
optimization
"
)
            
"
run
-
on
-
repo
-
type
"
:
task
.
get
(
"
run
-
on
-
repo
-
type
"
[
"
git
"
"
hg
"
]
)
        
}
        
if
"
run
-
on
-
projects
"
in
task
:
            
taskdesc
[
"
run
-
on
-
projects
"
]
=
task
[
"
run
-
on
-
projects
"
]
        
if
artifact
.
endswith
(
"
.
dmg
"
)
:
            
taskdesc
.
setdefault
(
"
fetches
"
{
}
)
.
setdefault
(
"
toolchain
"
[
]
)
.
extend
(
[
                
"
linux64
-
cctools
-
port
"
                
"
linux64
-
libdmg
"
            
]
)
        
yield
taskdesc
