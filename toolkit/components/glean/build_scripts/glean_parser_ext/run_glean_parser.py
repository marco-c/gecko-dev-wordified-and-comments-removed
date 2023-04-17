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
re
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
custom_is_expired
"
:
lambda
expires
:
expires
=
=
"
expired
"
        
or
expires
!
=
"
never
"
        
and
int
(
expires
)
<
=
int
(
app_version_major
)
        
"
custom_validate_expires
"
:
lambda
expires
:
expires
in
(
"
expired
"
"
never
"
)
        
or
re
.
fullmatch
(
r
"
\
d
\
d
+
"
expires
flags
=
re
.
ASCII
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
        
sys
.
exit
(
1
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
        
sys
.
exit
(
1
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
        
sys
.
exit
(
1
)
    
return
all_objs
.
value
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
info
in
ids_to_probes
.
values
(
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
