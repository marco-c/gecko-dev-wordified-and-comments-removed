from
__future__
import
absolute_import
print_function
unicode_literals
from
.
transform
import
loader
as
base_loader
def
loader
(
kind
path
config
params
loaded_tasks
)
:
    
"
"
"
    
Generate
inputs
implementing
PushApk
jobs
.
These
depend
on
signed
multi
-
locales
nightly
builds
.
    
"
"
"
    
jobs
=
base_loader
(
kind
path
config
params
loaded_tasks
)
    
for
job
in
jobs
:
        
dependent_tasks
=
get_dependent_loaded_tasks
(
config
params
loaded_tasks
)
        
if
not
dependent_tasks
:
            
continue
        
job
[
'
dependent
-
tasks
'
]
=
dependent_tasks
        
job
[
'
label
'
]
=
job
[
'
name
'
]
        
yield
job
def
get_dependent_loaded_tasks
(
config
params
loaded_tasks
)
:
    
nightly_tasks
=
(
        
task
for
task
in
loaded_tasks
if
task
.
attributes
.
get
(
'
nightly
'
)
    
)
    
tasks_with_matching_kind
=
(
        
task
for
task
in
nightly_tasks
if
task
.
kind
in
config
.
get
(
'
kind
-
dependencies
'
)
    
)
    
android_tasks
=
(
        
task
for
task
in
tasks_with_matching_kind
        
if
task
.
attributes
.
get
(
'
build_platform
'
'
'
)
.
startswith
(
'
android
'
)
    
)
    
if
params
[
'
project
'
]
in
(
'
mozilla
-
central
'
'
try
'
)
:
        
shipping_tasks
=
list
(
android_tasks
)
    
else
:
        
shipping_tasks
=
[
            
task
for
task
in
android_tasks
            
if
'
aarch64
'
not
in
task
.
attributes
.
get
(
'
build_platform
'
'
'
)
        
]
    
return
shipping_tasks
