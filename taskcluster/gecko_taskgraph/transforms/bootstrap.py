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
voluptuous
import
Any
Optional
Required
transforms
=
TransformSequence
(
)
bootstrap_schema
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
image
"
)
:
Any
(
str
{
"
in
-
tree
"
:
str
}
)
        
Required
(
"
pre
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
job
-
from
"
)
:
str
    
}
)
transforms
.
add_validate
(
bootstrap_schema
)
transforms
.
add
def
bootstrap_tasks
(
config
tasks
)
:
    
for
task
in
tasks
:
        
name
=
task
.
pop
(
"
name
"
)
        
image
=
task
.
pop
(
"
image
"
)
        
pre_commands
=
task
.
pop
(
"
pre
-
commands
"
)
        
head_repo
=
config
.
params
[
"
head_repository
"
]
        
head_rev
=
config
.
params
[
"
head_rev
"
]
        
dependencies
=
{
            
name
:
name
            
for
name
task
in
config
.
kind_dependencies_tasks
.
items
(
)
            
if
task
.
attributes
.
get
(
"
local
-
toolchain
"
)
            
and
not
name
.
startswith
(
(
"
toolchain
-
macos
"
"
toolchain
-
win
"
)
)
        
}
        
for
app
in
(
"
browser
"
"
mobile_android
"
)
:
            
commands
=
pre_commands
+
[
                
"
unset
MOZ_AUTOMATION
"
                
f
"
curl
-
O
{
head_repo
}
/
raw
-
file
/
{
head_rev
}
/
python
/
mozboot
/
bin
/
bootstrap
.
py
"
                
f
"
python3
bootstrap
.
py
-
-
no
-
interactive
-
-
application
-
choice
{
app
}
"
                
"
cd
mozilla
-
unified
"
                
"
.
/
mach
configure
-
-
disable
-
bootstrap
"
                
"
.
/
mach
build
"
            
]
            
taskdesc
=
{
                
"
label
"
:
f
"
{
config
.
kind
}
-
{
name
}
-
{
app
}
"
                
"
description
"
:
f
"
Bootstrap
{
app
}
build
on
{
name
}
"
                
"
always
-
target
"
:
True
                
"
scopes
"
:
[
]
                
"
treeherder
"
:
{
                    
"
symbol
"
:
f
"
Boot
(
{
name
}
)
"
                    
"
platform
"
:
{
                        
"
browser
"
:
"
linux64
/
opt
"
                        
"
mobile_android
"
:
"
android
-
5
-
0
-
armv7
/
opt
"
                    
}
[
app
]
                    
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
2
                
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
-
gcp
"
                
"
worker
"
:
{
                    
"
implementation
"
:
"
docker
-
worker
"
                    
"
docker
-
image
"
:
image
                    
"
os
"
:
"
linux
"
                    
"
env
"
:
{
                        
"
GECKO_HEAD_REPOSITORY
"
:
head_repo
                        
"
GECKO_HEAD_REV
"
:
head_rev
                        
"
MACH_NO_TERMINAL_FOOTER
"
:
"
1
"
                        
"
MOZ_SCM_LEVEL
"
:
config
.
params
[
"
level
"
]
                    
}
                    
"
command
"
:
[
"
sh
"
"
-
c
"
"
-
x
"
"
-
e
"
"
&
&
"
.
join
(
commands
)
]
                    
"
max
-
run
-
time
"
:
7200
                
}
                
"
dependencies
"
:
dependencies
                
"
optimization
"
:
{
                    
"
skip
-
unless
-
changed
"
:
[
                        
"
python
/
mozboot
/
bin
/
bootstrap
.
py
"
                        
"
python
/
mozboot
/
mozboot
/
*
*
"
                    
]
                
}
            
}
            
yield
taskdesc
