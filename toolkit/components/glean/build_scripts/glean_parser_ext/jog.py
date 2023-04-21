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
enum
import
json
import
sys
import
jinja2
from
glean_parser
import
util
from
glean_parser
.
metrics
import
Rate
from
util
import
type_ids_and_categories
from
js
import
ID_BITS
PING_INDEX_BITS
RUNTIME_METRIC_BIT
=
ID_BITS
-
1
RUNTIME_PING_BIT
=
PING_INDEX_BITS
-
1
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
known_extra_args
=
[
    
"
time_unit
"
    
"
memory_unit
"
    
"
allowed_extra_keys
"
    
"
reason_codes
"
    
"
range_min
"
    
"
range_max
"
    
"
bucket_count
"
    
"
histogram_type
"
    
"
numerators
"
]
known_ping_args
=
[
    
"
name
"
    
"
include_client_id
"
    
"
send_if_empty
"
    
"
reason_codes
"
]
def
ensure_jog_support_for_args
(
)
:
    
"
"
"
    
glean_parser
or
the
Glean
SDK
might
add
new
metric
/
ping
args
.
    
To
ensure
JOG
doesn
'
t
fall
behind
in
support
    
we
check
the
list
of
JOG
-
supported
args
vs
glean_parser
'
s
.
    
We
fail
the
build
if
glean_parser
has
one
or
more
we
haven
'
t
seen
before
.
    
"
"
"
    
unknown_args
=
set
(
util
.
extra_metric_args
)
-
set
(
known_extra_args
)
    
unknown_args
|
=
set
(
util
.
ping_args
)
-
set
(
known_ping_args
)
    
if
len
(
unknown_args
)
:
        
print
(
f
"
Unknown
glean_parser
args
{
unknown_args
}
"
)
        
print
(
"
JOG
must
be
updated
to
support
the
new
args
"
)
        
sys
.
exit
(
1
)
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
    
ensure_jog_support_for_args
(
)
    
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
RUNTIME_METRIC_BIT
            
runtime_ping_bit
=
RUNTIME_PING_BIT
            
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
camel_to_snake
(
s
)
:
    
assert
"
_
"
not
in
s
"
JOG
doesn
'
t
encode
metric
typenames
with
underscores
"
    
return
"
"
.
join
(
[
"
_
"
+
c
.
lower
(
)
if
c
.
isupper
(
)
else
c
for
c
in
s
]
)
.
lstrip
(
"
_
"
)
def
output_file
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
them
to
the
file
-
like
object
output_fd
.
    
Specifically
in
a
format
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
                 
Presently
a
dictionary
with
keys
of
literals
"
pings
"
and
"
tags
"
                 
as
well
as
one
key
per
metric
category
mapped
to
lists
of
                 
pings
tags
and
metrics
(
respecitvely
)
    
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
    
ensure_jog_support_for_args
(
)
    
jog_data
=
{
"
pings
"
:
[
]
"
metrics
"
:
{
}
}
    
if
"
tags
"
in
objs
:
        
del
objs
[
"
tags
"
]
    
pings
=
objs
[
"
pings
"
]
    
del
objs
[
"
pings
"
]
    
for
ping
in
pings
.
values
(
)
:
        
ping_arg_list
=
[
]
        
for
arg
in
known_ping_args
:
            
if
hasattr
(
ping
arg
)
:
                
ping_arg_list
.
append
(
getattr
(
ping
arg
)
)
        
jog_data
[
"
pings
"
]
.
append
(
ping_arg_list
)
    
def
encode
(
value
)
:
        
if
isinstance
(
value
enum
.
Enum
)
:
            
return
value
.
name
        
if
isinstance
(
value
Rate
)
:
            
args
=
[
]
            
for
arg_name
in
common_metric_data_args
[
:
-
1
]
:
                
args
.
append
(
getattr
(
value
arg_name
)
)
            
args
.
append
(
None
)
            
return
args
        
return
json
.
dumps
(
value
)
    
for
category
metrics
in
objs
.
items
(
)
:
        
dict_cat
=
jog_data
[
"
metrics
"
]
.
setdefault
(
category
[
]
)
        
for
metric
in
metrics
.
values
(
)
:
            
metric_arg_list
=
[
camel_to_snake
(
metric
.
__class__
.
__name__
)
]
            
for
arg
in
common_metric_data_args
[
:
-
1
]
:
                
if
arg
in
[
"
category
"
]
:
                    
continue
                
metric_arg_list
.
append
(
getattr
(
metric
arg
)
)
            
extra
=
{
}
            
for
arg
in
known_extra_args
:
                
if
hasattr
(
metric
arg
)
:
                    
extra
[
arg
]
=
getattr
(
metric
arg
)
            
if
len
(
extra
)
:
                
metric_arg_list
.
append
(
extra
)
            
dict_cat
.
append
(
metric_arg_list
)
    
json
.
dump
(
jog_data
output_fd
sort_keys
=
True
default
=
encode
indent
=
2
)
