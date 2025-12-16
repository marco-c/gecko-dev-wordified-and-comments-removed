from
mozperftest
.
system
.
simpleperf
import
SimpleperfProfiler
PROFILERS
=
{
SimpleperfProfiler
}
class
ProfilingMediator
:
    
"
"
"
Used
to
start
and
stop
any
profilers
setup
through
the
system
later
.
"
"
"
    
def
__init__
(
self
)
:
        
self
.
active_profilers
=
[
]
        
for
profiler
in
PROFILERS
:
            
if
profiler
.
is_enabled
(
)
:
                
self
.
active_profilers
.
append
(
profiler
.
get_controller
(
)
)
    
def
start
(
self
options
=
None
)
:
        
for
profiler
in
self
.
active_profilers
:
            
profiler
.
start
(
options
)
    
def
stop
(
self
output_path
index
)
:
        
for
profiler
in
self
.
active_profilers
:
            
profiler
.
stop
(
output_path
index
)
