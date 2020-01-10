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
__future__
import
absolute_import
print_function
unicode_literals
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
(
    
Schema
)
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
(
    
Any
    
Optional
    
Required
)
index_or_string
=
Any
(
    
basestring
    
{
Required
(
'
index
-
search
'
)
:
basestring
}
)
diff_description_schema
=
Schema
(
{
    
Required
(
'
name
'
)
:
basestring
    
Required
(
'
symbol
'
)
:
basestring
    
Optional
(
'
job
-
from
'
)
:
basestring
    
Required
(
'
original
'
)
:
index_or_string
    
Required
(
'
new
'
)
:
index_or_string
    
Optional
(
'
args
'
)
:
basestring
    
Optional
(
'
extra
-
args
'
)
:
basestring
    
Optional
(
'
fail
-
on
-
diff
'
)
:
bool
    
Optional
(
'
unpack
'
)
:
bool
    
Optional
(
'
pre
-
diff
-
commands
'
)
:
[
basestring
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
'
name
'
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
        
for
k
in
(
'
original
'
'
new
'
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
basestring
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
'
index
-
search
'
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
                        
'
label
'
:
'
index
-
search
-
'
+
index
                        
'
description
'
:
index
                        
'
worker
-
type
'
:
'
invalid
/
always
-
optimized
'
                        
'
run
'
:
{
                            
'
using
'
:
'
always
-
optimized
'
                        
}
                        
'
optimization
'
:
{
                            
'
index
-
search
'
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
'
index
-
search
-
'
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
'
.
'
)
[
-
1
]
            
if
'
linux
'
in
os_hint
:
                
artifact
=
'
target
.
tar
.
bz2
'
            
elif
'
macosx
'
in
os_hint
:
                
artifact
=
'
target
.
dmg
'
            
elif
'
android
'
in
os_hint
:
                
artifact
=
'
target
.
apk
'
            
elif
'
win
'
in
os_hint
:
                
artifact
=
'
target
.
zip
'
            
else
:
                
raise
Exception
(
                    
'
Cannot
figure
out
the
OS
for
{
!
r
}
'
.
format
(
value
)
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
                    
'
Cannot
compare
builds
from
different
OSes
'
)
            
urls
[
k
]
=
{
                
'
artifact
-
reference
'
:
'
<
{
}
/
{
}
>
'
.
format
(
                    
dep_name
get_artifact_path
(
task
artifact
)
)
            
}
            
previous_artifact
=
artifact
        
taskdesc
=
{
            
'
label
'
:
'
diff
-
'
+
name
            
'
description
'
:
name
            
'
treeherder
'
:
{
                
'
symbol
'
:
task
[
'
symbol
'
]
                
'
platform
'
:
'
diff
/
opt
'
                
'
kind
'
:
'
other
'
                
'
tier
'
:
2
            
}
            
'
worker
-
type
'
:
'
b
-
linux
'
            
'
worker
'
:
{
                
'
docker
-
image
'
:
{
'
in
-
tree
'
:
'
diffoscope
'
}
                
'
artifacts
'
:
[
{
                    
'
type
'
:
'
file
'
                    
'
path
'
:
'
/
builds
/
worker
/
diff
.
html
'
                    
'
name
'
:
'
public
/
diff
.
html
'
                
}
{
                    
'
type
'
:
'
file
'
                    
'
path
'
:
'
/
builds
/
worker
/
diff
.
txt
'
                    
'
name
'
:
'
public
/
diff
.
txt
'
                
}
]
                
'
env
'
:
{
                    
'
ORIG_URL
'
:
urls
[
'
original
'
]
                    
'
NEW_URL
'
:
urls
[
'
new
'
]
                    
'
DIFFOSCOPE_ARGS
'
:
'
'
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
'
args
'
'
extra
-
args
'
)
if
k
in
task
)
                    
'
PRE_DIFF
'
:
'
;
'
.
join
(
task
.
get
(
'
pre
-
diff
-
commands
'
[
]
)
)
                
}
                
'
max
-
run
-
time
'
:
1800
            
}
            
'
run
'
:
{
                
'
using
'
:
'
run
-
task
'
                
'
checkout
'
:
task
.
get
(
'
unpack
'
False
)
                
'
command
'
:
'
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
'
.
format
(
                    
'
-
-
unpack
'
if
task
.
get
(
'
unpack
'
)
else
'
'
                    
'
-
-
fail
'
if
task
.
get
(
'
fail
-
on
-
diff
'
)
else
'
'
                
)
            
}
            
'
dependencies
'
:
deps
        
}
        
if
artifact
.
endswith
(
'
.
dmg
'
)
:
            
taskdesc
.
setdefault
(
'
fetches
'
{
}
)
.
setdefault
(
'
toolchain
'
[
]
)
.
extend
(
[
                
'
linux64
-
cctools
-
port
'
                
'
linux64
-
libdmg
'
            
]
)
        
yield
taskdesc
