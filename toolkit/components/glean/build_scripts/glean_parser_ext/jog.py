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
"
"
"
Outputter
to
generate
Rust
code
for
metrics
.
"
"
"
import
jinja2
from
js
import
ID_BITS
from
util
import
type_ids_and_categories
from
glean_parser
import
util
common_metric_data_args
=
[
    
"
name
"
    
"
category
"
    
"
send_in_pings
"
    
"
lifetime
"
    
"
disabled
"
    
"
dynamic_label
"
]
def
load_monkeypatches
(
)
:
    
"
"
"
    
Monkeypatch
jinja
template
loading
because
we
'
re
not
glean_parser
.
    
We
'
re
glean_parser_ext
.
    
"
"
"
    
def
get_local_template
(
template_name
filters
=
(
)
)
:
        
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
rust
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
camelize
"
]
=
util
.
camelize
        
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
        
for
filter_name
filter_func
in
filters
:
            
env
.
filters
[
filter_name
]
=
filter_func
        
return
env
.
get_template
(
template_name
)
    
util
.
get_jinja2_template
=
get_local_template
def
output_factory
(
objs
output_fd
options
=
{
}
)
:
    
"
"
"
    
Given
a
tree
of
objects
output
Rust
code
to
the
file
-
like
object
output_fd
.
    
Specifically
Rust
code
that
can
generate
Rust
metrics
instances
.
    
:
param
objs
:
A
tree
of
objects
(
metrics
and
pings
)
as
returned
from
    
parser
.
parse_objects
.
    
:
param
output_fd
:
Writeable
file
to
write
the
output
to
.
    
:
param
options
:
options
dictionary
presently
unused
.
    
"
"
"
    
load_monkeypatches
(
)
    
metric_types
categories
=
type_ids_and_categories
(
objs
)
    
template
=
util
.
get_jinja2_template
(
        
"
jog_factory
.
jinja2
"
        
filters
=
(
(
"
snake_case
"
util
.
snake_case
)
)
    
)
    
output_fd
.
write
(
        
template
.
render
(
            
all_objs
=
objs
            
common_metric_data_args
=
common_metric_data_args
            
extra_args
=
util
.
extra_args
            
metric_types
=
metric_types
            
runtime_metric_bit
=
ID_BITS
-
1
            
ID_BITS
=
ID_BITS
        
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
def
output_yaml
(
objs
output_fd
options
=
{
}
)
:
    
"
"
"
    
Given
a
tree
of
objects
output
YAML
to
the
file
-
like
object
output_fd
.
    
Specifically
YAML
that
describes
all
the
metrics
and
pings
defined
in
objs
.
    
:
param
objs
:
A
tree
of
objects
(
metrics
and
pings
)
as
returned
from
    
parser
.
parse_objects
.
    
:
param
output_fd
:
Writeable
file
to
write
the
output
to
.
    
:
param
options
:
options
dictionary
presently
unused
.
    
"
"
"
    
load_monkeypatches
(
)
