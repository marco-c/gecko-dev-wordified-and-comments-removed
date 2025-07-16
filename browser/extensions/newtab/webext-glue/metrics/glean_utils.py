import
enum
import
json
import
sys
from
os
import
path
ROOT_PATH
=
path
.
abspath
(
    
path
.
join
(
        
path
.
dirname
(
__file__
)
        
path
.
pardir
        
path
.
pardir
        
path
.
pardir
        
path
.
pardir
        
path
.
pardir
    
)
)
GLEAN_BUILD_SCRIPTS_PATH
=
path
.
join
(
    
ROOT_PATH
"
toolkit
"
"
components
"
"
glean
"
"
build_scripts
"
"
glean_parser_ext
"
)
sys
.
path
.
append
(
GLEAN_BUILD_SCRIPTS_PATH
)
import
jog
from
glean_parser
.
metrics
import
Rate
def
output_file_with_key
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
    
in
a
format
similar
to
runtime
-
metrics
-
sample
.
json
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
    
jog
.
ensure_jog_support_for_args
(
)
    
output_data
=
{
"
metrics
"
:
{
}
"
pings
"
:
{
}
}
    
if
"
pings
"
in
objs
:
        
pings
=
objs
[
"
pings
"
]
        
for
ping_name
ping
in
pings
.
items
(
)
:
            
ping_data
=
{
}
            
for
arg
in
jog
.
known_ping_args
:
                
if
hasattr
(
ping
arg
)
:
                    
key
=
arg
                    
value
=
getattr
(
ping
arg
)
                    
ping_data
[
key
]
=
value
            
output_data
[
"
pings
"
]
[
ping_name
]
=
ping_data
    
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
jog
.
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
        
if
category
in
[
"
pings
"
"
tags
"
]
:
            
continue
        
output_data
[
"
metrics
"
]
[
category
]
=
{
}
        
for
metric_name
metric
in
metrics
.
items
(
)
:
            
metric_data
=
{
                
"
type
"
:
metric
.
typename
                
"
description
"
:
getattr
(
metric
"
description
"
"
"
)
                
"
lifetime
"
:
getattr
(
metric
"
lifetime
"
"
ping
"
)
.
name
.
lower
(
)
                
"
pings
"
:
getattr
(
metric
"
send_in_pings
"
[
]
)
                
"
disabled
"
:
getattr
(
metric
"
disabled
"
False
)
            
}
            
extra_args
=
{
}
            
for
arg
in
jog
.
known_extra_args
:
                
if
hasattr
(
metric
arg
)
:
                    
if
arg
=
=
"
extra_keys
"
:
                        
extra_args
[
"
allowed_extra_keys
"
]
=
list
(
                            
getattr
(
metric
arg
)
.
keys
(
)
                        
)
                    
else
:
                        
extra_args
[
arg
]
=
getattr
(
metric
arg
)
            
for
meta
in
jog
.
known_metadata
:
                
if
meta
in
metric
.
metadata
:
                    
extra_args
[
meta
]
=
metric
.
metadata
.
get
(
meta
)
            
if
extra_args
:
                
metric_data
[
"
extraArgs
"
]
=
extra_args
            
output_data
[
"
metrics
"
]
[
category
]
[
metric_name
]
=
metric_data
    
json
.
dump
(
output_data
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
