import
struct
from
optparse
import
OptionParser
import
matplotlib
.
pyplot
as
plt
import
debug_dump_pb2
def
GetNextMessageSize
(
file_to_parse
)
:
    
data
=
file_to_parse
.
read
(
4
)
    
if
data
=
=
'
'
:
        
return
0
    
return
struct
.
unpack
(
'
<
I
'
data
)
[
0
]
def
GetNextMessageFromFile
(
file_to_parse
)
:
    
message_size
=
GetNextMessageSize
(
file_to_parse
)
    
if
message_size
=
=
0
:
        
return
None
    
try
:
        
event
=
debug_dump_pb2
.
Event
(
)
        
event
.
ParseFromString
(
file_to_parse
.
read
(
message_size
)
)
    
except
IOError
:
        
print
'
Invalid
message
in
file
'
        
return
None
    
return
event
def
InitMetrics
(
)
:
    
metrics
=
{
}
    
event
=
debug_dump_pb2
.
Event
(
)
    
for
metric
in
event
.
network_metrics
.
DESCRIPTOR
.
fields
:
        
metrics
[
metric
.
name
]
=
{
'
time
'
:
[
]
'
value
'
:
[
]
}
    
return
metrics
def
InitDecisions
(
)
:
    
decisions
=
{
}
    
event
=
debug_dump_pb2
.
Event
(
)
    
for
decision
in
event
.
encoder_runtime_config
.
DESCRIPTOR
.
fields
:
        
decisions
[
decision
.
name
]
=
{
'
time
'
:
[
]
'
value
'
:
[
]
}
    
return
decisions
def
ParseAnaDump
(
dump_file_to_parse
)
:
    
with
open
(
dump_file_to_parse
'
rb
'
)
as
file_to_parse
:
        
metrics
=
InitMetrics
(
)
        
decisions
=
InitDecisions
(
)
        
first_time_stamp
=
None
        
while
True
:
            
event
=
GetNextMessageFromFile
(
file_to_parse
)
            
if
event
is
None
:
                
break
            
if
first_time_stamp
is
None
:
                
first_time_stamp
=
event
.
timestamp
            
if
event
.
type
=
=
debug_dump_pb2
.
Event
.
ENCODER_RUNTIME_CONFIG
:
                
for
decision
in
event
.
encoder_runtime_config
.
DESCRIPTOR
.
fields
:
                    
if
event
.
encoder_runtime_config
.
HasField
(
decision
.
name
)
:
                        
decisions
[
decision
.
name
]
[
'
time
'
]
.
append
(
                            
event
.
timestamp
-
first_time_stamp
)
                        
decisions
[
decision
.
name
]
[
'
value
'
]
.
append
(
                            
getattr
(
event
.
encoder_runtime_config
                                    
decision
.
name
)
)
            
if
event
.
type
=
=
debug_dump_pb2
.
Event
.
NETWORK_METRICS
:
                
for
metric
in
event
.
network_metrics
.
DESCRIPTOR
.
fields
:
                    
if
event
.
network_metrics
.
HasField
(
metric
.
name
)
:
                        
metrics
[
metric
.
name
]
[
'
time
'
]
.
append
(
event
.
timestamp
-
                                                            
first_time_stamp
)
                        
metrics
[
metric
.
name
]
[
'
value
'
]
.
append
(
                            
getattr
(
event
.
network_metrics
metric
.
name
)
)
    
return
(
metrics
decisions
)
def
main
(
)
:
    
parser
=
OptionParser
(
)
    
parser
.
add_option
(
"
-
f
"
                      
"
-
-
dump_file
"
                      
dest
=
"
dump_file_to_parse
"
                      
help
=
"
dump
file
to
parse
"
)
    
parser
.
add_option
(
'
-
m
'
                      
'
-
-
metric_plot
'
                      
default
=
[
]
                      
type
=
str
                      
help
=
'
metric
key
(
name
of
the
metric
)
to
plot
'
                      
dest
=
'
metric_keys
'
                      
action
=
'
append
'
)
    
parser
.
add_option
(
'
-
d
'
                      
'
-
-
decision_plot
'
                      
default
=
[
]
                      
type
=
str
                      
help
=
'
decision
key
(
name
of
the
decision
)
to
plot
'
                      
dest
=
'
decision_keys
'
                      
action
=
'
append
'
)
    
options
=
parser
.
parse_args
(
)
[
0
]
    
if
options
.
dump_file_to_parse
is
None
:
        
print
"
No
dump
file
to
parse
is
set
.
\
n
"
        
parser
.
print_help
(
)
        
exit
(
)
    
(
metrics
decisions
)
=
ParseAnaDump
(
options
.
dump_file_to_parse
)
    
metric_keys
=
options
.
metric_keys
    
decision_keys
=
options
.
decision_keys
    
plot_count
=
len
(
metric_keys
)
+
len
(
decision_keys
)
    
if
plot_count
=
=
0
:
        
print
"
You
have
to
set
at
least
one
metric
or
decision
to
plot
.
\
n
"
        
parser
.
print_help
(
)
        
exit
(
)
    
plots
=
[
]
    
if
plot_count
=
=
1
:
        
f
mp_plot
=
plt
.
subplots
(
)
        
plots
.
append
(
mp_plot
)
    
else
:
        
f
mp_plots
=
plt
.
subplots
(
plot_count
sharex
=
True
)
        
plots
.
extend
(
mp_plots
.
tolist
(
)
)
    
for
key
in
metric_keys
:
        
plot
=
plots
.
pop
(
)
        
plot
.
grid
(
True
)
        
plot
.
set_title
(
key
+
"
(
metric
)
"
)
        
plot
.
plot
(
metrics
[
key
]
[
'
time
'
]
metrics
[
key
]
[
'
value
'
]
)
    
for
key
in
decision_keys
:
        
plot
=
plots
.
pop
(
)
        
plot
.
grid
(
True
)
        
plot
.
set_title
(
key
+
"
(
decision
)
"
)
        
plot
.
plot
(
decisions
[
key
]
[
'
time
'
]
decisions
[
key
]
[
'
value
'
]
)
    
f
.
subplots_adjust
(
hspace
=
0
.
3
)
    
plt
.
show
(
)
if
__name__
=
=
"
__main__
"
:
    
main
(
)
