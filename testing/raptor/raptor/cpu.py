from
__future__
import
absolute_import
def
get_app_cpu_usage
(
raptor
)
:
    
cpu_usage
=
0
    
app_name
=
raptor
.
config
[
'
binary
'
]
    
verbose
=
raptor
.
device
.
_verbose
    
raptor
.
device
.
_verbose
=
False
    
'
'
'
    
There
are
two
ways
to
get
CPU
usage
information
:
    
1
.
By
using
the
'
top
'
command
and
parsing
details
    
2
.
By
using
'
dumpsys
cpuinfo
'
and
parsing
the
details
    
'
top
'
is
our
first
choice
if
it
is
available
but
the
    
parameters
we
use
are
only
available
in
Android
8
or
    
greater
otherwise
we
fall
back
to
using
dumpsys
    
'
'
'
    
if
raptor
.
device
.
version
>
=
8
:
        
cpuinfo
=
raptor
.
device
.
shell_output
(
"
top
-
O
%
CPU
-
n
1
"
)
.
split
(
"
\
n
"
)
        
raptor
.
device
.
_verbose
=
verbose
        
for
line
in
cpuinfo
:
            
data
=
line
.
split
(
)
            
if
data
[
-
1
]
=
=
app_name
:
                
cpu_usage
=
float
(
data
[
3
]
)
    
else
:
        
cpuinfo
=
raptor
.
device
.
shell_output
(
"
dumpsys
cpuinfo
|
grep
%
s
"
%
app_name
)
.
split
(
"
\
n
"
)
        
for
line
in
cpuinfo
:
            
data
=
line
.
split
(
)
            
cpu_usage
=
float
(
data
[
0
]
.
strip
(
'
%
'
)
)
    
return
cpu_usage
def
generate_android_cpu_profile
(
raptor
test_name
)
:
    
if
not
raptor
.
device
or
not
raptor
.
config
[
'
cpu_test
'
]
:
        
return
    
result
=
get_app_cpu_usage
(
raptor
)
    
cpuinfo_data
=
{
        
u
'
type
'
:
u
'
cpu
'
        
u
'
test
'
:
test_name
        
u
'
unit
'
:
u
'
%
'
        
u
'
values
'
:
{
            
u
'
browser_cpu_usage
'
:
result
        
}
    
}
    
raptor
.
control_server
.
submit_supporting_data
(
cpuinfo_data
)
