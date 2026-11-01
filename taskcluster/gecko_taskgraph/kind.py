import
time
from
dataclasses
import
dataclass
replace
from
typing
import
Optional
from
mozsystemmonitor
.
resourcemonitor
import
SystemResourceMonitor
from
taskgraph
.
generator
import
Kind
dataclass
(
frozen
=
True
)
class
ProfiledKind
(
Kind
)
:
    
"
"
"
A
kind
recording
how
long
loading
its
tasks
takes
as
a
marker
in
the
    
resource
usage
profile
including
when
its
tasks
are
loaded
in
a
separate
    
process
whatever
the
multiprocessing
start
method
.
    
forward_path
is
the
file
monitors
in
such
processes
forward
the
marker
to
    
see
SystemResourceMonitor
.
children_forward_path
.
    
"
"
"
    
forward_path
:
Optional
[
str
]
=
None
    
classmethod
    
def
load
(
cls
root_dir
graph_config
kind_name
)
:
        
kind
=
super
(
)
.
load
(
root_dir
graph_config
kind_name
)
        
monitor
=
SystemResourceMonitor
.
instance
        
if
monitor
is
None
:
            
return
kind
        
return
replace
(
kind
forward_path
=
monitor
.
children_forward_path
)
    
def
load_tasks
(
self
parameters
kind_dependencies_tasks
write_artifacts
)
:
        
if
self
.
forward_path
and
SystemResourceMonitor
.
instance
is
None
:
            
SystemResourceMonitor
(
forward_to
=
self
.
forward_path
)
.
start
(
)
        
start
=
time
.
monotonic
(
)
        
try
:
            
tasks
=
super
(
)
.
load_tasks
(
                
parameters
kind_dependencies_tasks
write_artifacts
            
)
        
except
BaseException
:
            
SystemResourceMonitor
.
record_marker
(
                
"
Kind
"
                
start
                
time
.
monotonic
(
)
                
{
"
type
"
:
"
Text
"
"
text
"
:
f
"
{
self
.
name
}
(
failed
)
"
}
            
)
            
raise
        
SystemResourceMonitor
.
record_marker
(
            
"
Kind
"
            
start
            
time
.
monotonic
(
)
            
{
"
type
"
:
"
Text
"
"
text
"
:
f
"
{
self
.
name
}
(
{
len
(
tasks
)
}
tasks
)
"
}
        
)
        
return
tasks
