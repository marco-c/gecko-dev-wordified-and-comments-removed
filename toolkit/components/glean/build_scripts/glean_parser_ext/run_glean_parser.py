#
-
*
-
coding
:
utf
-
8
-
*
-
import
cpp
import
js
import
os
import
rust
import
sys
import
jinja2
from
util
import
generate_metric_ids
from
glean_parser
import
lint
parser
translate
util
from
mozbuild
.
util
import
FileAvoidWrite
from
pathlib
import
Path
class
ParserError
(
Exception
)
:
    
"
"
"
Thrown
from
parse
if
something
goes
wrong
"
"
"
    
pass
GIFFT_TYPES
=
{
    
"
Event
"
:
[
"
event
"
]
    
"
Histogram
"
:
[
"
timing_distribution
"
"
memory_distribution
"
"
custom_distribution
"
]
    
"
Scalar
"
:
[
        
"
boolean
"
        
"
labeled_boolean
"
        
"
counter
"
        
"
labeled_counter
"
        
"
string
"
        
"
string_list
"
        
"
timespan
"
        
"
uuid
"
        
"
datetime
"
        
"
quantity
"
        
"
rate
"
        
"
url
"
    
]
}
def
get_parser_options
(
moz_app_version
)
:
    
app_version_major
=
moz_app_version
.
split
(
"
.
"
1
)
[
0
]
    
return
{
        
"
allow_reserved
"
:
False
        
"
expire_by_version
"
:
int
(
app_version_major
)
    
}
def
parse
(
args
)
:
    
"
"
"
    
Parse
and
lint
the
input
files
    
then
return
the
parsed
objects
for
further
processing
.
    
"
"
"
    
yaml_array
=
args
[
:
-
1
]
    
moz_app_version
=
args
[
-
1
]
    
input_files
=
[
Path
(
x
)
for
x
in
yaml_array
]
    
options
=
get_parser_options
(
moz_app_version
)
    
return
parse_with_options
(
input_files
options
)
def
parse_with_options
(
input_files
options
)
:
    
if
lint
.
lint_yaml_files
(
input_files
parser_config
=
options
)
:
        
raise
ParserError
(
"
linter
found
problems
"
)
    
all_objs
=
parser
.
parse_objects
(
input_files
options
)
    
if
util
.
report_validation_errors
(
all_objs
)
:
        
raise
ParserError
(
"
found
validation
errors
during
parse
"
)
    
nits
=
lint
.
lint_metrics
(
all_objs
.
value
options
)
    
if
nits
is
not
None
and
any
(
nit
.
check_name
!
=
"
EXPIRED
"
for
nit
in
nits
)
:
        
raise
ParserError
(
"
glinter
nits
found
during
parse
"
)
    
objects
=
all_objs
.
value
    
translate
.
transform_metrics
(
objects
)
    
return
objects
options
DEPS_LEN
=
15
def
main
(
output_fd
*
args
)
:
    
args
=
args
[
DEPS_LEN
:
]
    
all_objs
options
=
parse
(
args
)
    
rust
.
output_rust
(
all_objs
output_fd
options
)
def
cpp_metrics
(
output_fd
*
args
)
:
    
args
=
args
[
DEPS_LEN
:
]
    
all_objs
options
=
parse
(
args
)
    
cpp
.
output_cpp
(
all_objs
output_fd
options
)
def
js_metrics
(
output_fd
*
args
)
:
    
args
=
args
[
DEPS_LEN
:
]
    
all_objs
options
=
parse
(
args
)
    
js
.
output_js
(
all_objs
output_fd
options
)
def
gifft_map
(
output_fd
*
args
)
:
    
probe_type
=
args
[
-
1
]
    
args
=
args
[
DEPS_LEN
:
-
1
]
    
all_objs
options
=
parse
(
args
)
    
if
probe_type
=
=
"
Event
"
:
        
output_path
=
Path
(
os
.
path
.
dirname
(
output_fd
.
name
)
)
        
with
FileAvoidWrite
(
output_path
/
"
EventExtraGIFFTMaps
.
cpp
"
)
as
cpp_fd
:
            
output_gifft_map
(
output_fd
probe_type
all_objs
cpp_fd
)
    
else
:
        
output_gifft_map
(
output_fd
probe_type
all_objs
None
)
def
output_gifft_map
(
output_fd
probe_type
all_objs
cpp_fd
)
:
    
get_metric_id
=
generate_metric_ids
(
all_objs
)
    
ids_to_probes
=
{
}
    
for
category_name
objs
in
all_objs
.
items
(
)
:
        
for
metric
in
objs
.
values
(
)
:
            
if
(
                
hasattr
(
metric
"
telemetry_mirror
"
)
                
and
metric
.
telemetry_mirror
is
not
None
            
)
:
                
info
=
(
metric
.
telemetry_mirror
f
"
{
category_name
}
.
{
metric
.
name
}
"
)
                
if
metric
.
type
in
GIFFT_TYPES
[
probe_type
]
:
                    
if
any
(
                        
metric
.
telemetry_mirror
=
=
value
[
0
]
                        
for
value
in
ids_to_probes
.
values
(
)
                    
)
:
                        
print
(
                            
f
"
Telemetry
mirror
{
metric
.
telemetry_mirror
}
already
registered
"
                            
file
=
sys
.
stderr
                        
)
                        
sys
.
exit
(
1
)
                    
ids_to_probes
[
get_metric_id
(
metric
)
]
=
info
                
elif
not
any
(
                    
[
                        
metric
.
type
in
types_for_probe
                        
for
types_for_probe
in
GIFFT_TYPES
.
values
(
)
                    
]
                
)
:
                    
print
(
                        
f
"
Glean
metric
{
category_name
}
.
{
metric
.
name
}
is
of
type
{
metric
.
type
}
"
                        
"
which
can
'
t
be
mirrored
(
we
don
'
t
know
how
)
.
"
                        
file
=
sys
.
stderr
                    
)
                    
sys
.
exit
(
1
)
    
env
=
jinja2
.
Environment
(
        
loader
=
jinja2
.
PackageLoader
(
"
run_glean_parser
"
"
templates
"
)
        
trim_blocks
=
True
        
lstrip_blocks
=
True
    
)
    
env
.
filters
[
"
snake_case
"
]
=
lambda
value
:
value
.
replace
(
"
.
"
"
_
"
)
.
replace
(
"
-
"
"
_
"
)
    
env
.
filters
[
"
Camelize
"
]
=
util
.
Camelize
    
template
=
env
.
get_template
(
"
gifft
.
jinja2
"
)
    
output_fd
.
write
(
        
template
.
render
(
            
ids_to_probes
=
ids_to_probes
            
probe_type
=
probe_type
            
id_bits
=
js
.
ID_BITS
            
id_signal_bits
=
js
.
ID_SIGNAL_BITS
        
)
    
)
    
output_fd
.
write
(
"
\
n
"
)
    
if
probe_type
=
=
"
Event
"
:
        
template
=
env
.
get_template
(
"
gifft_events
.
jinja2
"
)
        
cpp_fd
.
write
(
template
.
render
(
all_objs
=
all_objs
)
)
        
cpp_fd
.
write
(
"
\
n
"
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
sys
.
stdout
*
sys
.
argv
[
1
:
]
)
