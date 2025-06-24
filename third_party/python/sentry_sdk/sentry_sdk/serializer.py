import
sys
import
math
from
datetime
import
datetime
from
sentry_sdk
.
utils
import
(
    
AnnotatedValue
    
capture_internal_exception
    
disable_capture_event
    
format_timestamp
    
safe_repr
    
strip_string
)
from
sentry_sdk
.
_compat
import
(
    
text_type
    
PY2
    
string_types
    
number_types
    
iteritems
    
binary_sequence_types
)
from
sentry_sdk
.
_types
import
TYPE_CHECKING
if
TYPE_CHECKING
:
    
from
types
import
TracebackType
    
from
typing
import
Any
    
from
typing
import
Callable
    
from
typing
import
ContextManager
    
from
typing
import
Dict
    
from
typing
import
List
    
from
typing
import
Optional
    
from
typing
import
Type
    
from
typing
import
Union
    
from
sentry_sdk
.
_types
import
NotImplementedType
Event
    
Span
=
Dict
[
str
Any
]
    
ReprProcessor
=
Callable
[
[
Any
Dict
[
str
Any
]
]
Union
[
NotImplementedType
str
]
]
    
Segment
=
Union
[
str
int
]
if
PY2
:
    
from
collections
import
Mapping
Sequence
Set
    
serializable_str_types
=
string_types
+
binary_sequence_types
else
:
    
from
collections
.
abc
import
Mapping
Sequence
Set
    
serializable_str_types
=
string_types
+
binary_sequence_types
MAX_EVENT_BYTES
=
10
*
*
6
MAX_DATABAG_DEPTH
=
5
MAX_DATABAG_BREADTH
=
10
CYCLE_MARKER
=
"
<
cyclic
>
"
global_repr_processors
=
[
]
def
add_global_repr_processor
(
processor
)
:
    
global_repr_processors
.
append
(
processor
)
class
Memo
(
object
)
:
    
__slots__
=
(
"
_ids
"
"
_objs
"
)
    
def
__init__
(
self
)
:
        
self
.
_ids
=
{
}
        
self
.
_objs
=
[
]
    
def
memoize
(
self
obj
)
:
        
self
.
_objs
.
append
(
obj
)
        
return
self
    
def
__enter__
(
self
)
:
        
obj
=
self
.
_objs
[
-
1
]
        
if
id
(
obj
)
in
self
.
_ids
:
            
return
True
        
else
:
            
self
.
_ids
[
id
(
obj
)
]
=
obj
            
return
False
    
def
__exit__
(
        
self
        
ty
        
value
        
tb
    
)
:
        
self
.
_ids
.
pop
(
id
(
self
.
_objs
.
pop
(
)
)
None
)
def
serialize
(
event
*
*
kwargs
)
:
    
memo
=
Memo
(
)
    
path
=
[
]
    
meta_stack
=
[
]
    
keep_request_bodies
=
(
        
kwargs
.
pop
(
"
max_request_body_size
"
None
)
=
=
"
always
"
    
)
    
max_value_length
=
kwargs
.
pop
(
"
max_value_length
"
None
)
    
def
_annotate
(
*
*
meta
)
:
        
while
len
(
meta_stack
)
<
=
len
(
path
)
:
            
try
:
                
segment
=
path
[
len
(
meta_stack
)
-
1
]
                
node
=
meta_stack
[
-
1
]
.
setdefault
(
text_type
(
segment
)
{
}
)
            
except
IndexError
:
                
node
=
{
}
            
meta_stack
.
append
(
node
)
        
meta_stack
[
-
1
]
.
setdefault
(
"
"
{
}
)
.
update
(
meta
)
    
def
_should_repr_strings
(
)
:
        
"
"
"
        
By
default
non
-
serializable
objects
are
going
through
        
safe_repr
(
)
.
For
certain
places
in
the
event
(
local
vars
)
we
        
want
to
repr
(
)
even
things
that
are
JSON
-
serializable
to
        
make
their
type
more
apparent
.
For
example
it
'
s
useful
to
        
see
the
difference
between
a
unicode
-
string
and
a
bytestring
        
when
viewing
a
stacktrace
.
        
For
container
-
types
we
still
don
'
t
do
anything
different
.
        
Generally
we
just
try
to
make
the
Sentry
UI
present
exactly
        
what
a
pretty
-
printed
repr
would
look
like
.
        
:
returns
:
True
if
we
are
somewhere
in
frame
variables
and
False
if
            
we
are
in
a
position
where
we
will
never
encounter
frame
variables
            
when
recursing
(
for
example
we
'
re
in
event
.
extra
)
.
None
if
we
            
are
not
(
yet
)
in
frame
variables
but
might
encounter
them
when
            
recursing
(
e
.
g
.
we
'
re
in
event
.
exception
)
        
"
"
"
        
try
:
            
p0
=
path
[
0
]
            
if
p0
=
=
"
stacktrace
"
and
path
[
1
]
=
=
"
frames
"
and
path
[
3
]
=
=
"
vars
"
:
                
return
True
            
if
(
                
p0
in
(
"
threads
"
"
exception
"
)
                
and
path
[
1
]
=
=
"
values
"
                
and
path
[
3
]
=
=
"
stacktrace
"
                
and
path
[
4
]
=
=
"
frames
"
                
and
path
[
6
]
=
=
"
vars
"
            
)
:
                
return
True
        
except
IndexError
:
            
return
None
        
return
False
    
def
_is_databag
(
)
:
        
"
"
"
        
A
databag
is
any
value
that
we
need
to
trim
.
        
:
returns
:
Works
like
_should_repr_strings
(
)
.
True
for
"
yes
"
            
False
for
:
"
no
"
None
for
"
maybe
soon
"
.
        
"
"
"
        
try
:
            
rv
=
_should_repr_strings
(
)
            
if
rv
in
(
True
None
)
:
                
return
rv
            
is_request_body
=
_is_request_body
(
)
            
if
is_request_body
in
(
True
None
)
:
                
return
is_request_body
            
p0
=
path
[
0
]
            
if
p0
=
=
"
breadcrumbs
"
and
path
[
1
]
=
=
"
values
"
:
                
path
[
2
]
                
return
True
            
if
p0
=
=
"
extra
"
:
                
return
True
        
except
IndexError
:
            
return
None
        
return
False
    
def
_is_request_body
(
)
:
        
try
:
            
if
path
[
0
]
=
=
"
request
"
and
path
[
1
]
=
=
"
data
"
:
                
return
True
        
except
IndexError
:
            
return
None
        
return
False
    
def
_serialize_node
(
        
obj
        
is_databag
=
None
        
is_request_body
=
None
        
should_repr_strings
=
None
        
segment
=
None
        
remaining_breadth
=
None
        
remaining_depth
=
None
    
)
:
        
if
segment
is
not
None
:
            
path
.
append
(
segment
)
        
try
:
            
with
memo
.
memoize
(
obj
)
as
result
:
                
if
result
:
                    
return
CYCLE_MARKER
                
return
_serialize_node_impl
(
                    
obj
                    
is_databag
=
is_databag
                    
is_request_body
=
is_request_body
                    
should_repr_strings
=
should_repr_strings
                    
remaining_depth
=
remaining_depth
                    
remaining_breadth
=
remaining_breadth
                
)
        
except
BaseException
:
            
capture_internal_exception
(
sys
.
exc_info
(
)
)
            
if
is_databag
:
                
return
"
<
failed
to
serialize
use
init
(
debug
=
True
)
to
see
error
logs
>
"
            
return
None
        
finally
:
            
if
segment
is
not
None
:
                
path
.
pop
(
)
                
del
meta_stack
[
len
(
path
)
+
1
:
]
    
def
_flatten_annotated
(
obj
)
:
        
if
isinstance
(
obj
AnnotatedValue
)
:
            
_annotate
(
*
*
obj
.
metadata
)
            
obj
=
obj
.
value
        
return
obj
    
def
_serialize_node_impl
(
        
obj
        
is_databag
        
is_request_body
        
should_repr_strings
        
remaining_depth
        
remaining_breadth
    
)
:
        
if
isinstance
(
obj
AnnotatedValue
)
:
            
should_repr_strings
=
False
        
if
should_repr_strings
is
None
:
            
should_repr_strings
=
_should_repr_strings
(
)
        
if
is_databag
is
None
:
            
is_databag
=
_is_databag
(
)
        
if
is_request_body
is
None
:
            
is_request_body
=
_is_request_body
(
)
        
if
is_databag
:
            
if
is_request_body
and
keep_request_bodies
:
                
remaining_depth
=
float
(
"
inf
"
)
                
remaining_breadth
=
float
(
"
inf
"
)
            
else
:
                
if
remaining_depth
is
None
:
                    
remaining_depth
=
MAX_DATABAG_DEPTH
                
if
remaining_breadth
is
None
:
                    
remaining_breadth
=
MAX_DATABAG_BREADTH
        
obj
=
_flatten_annotated
(
obj
)
        
if
remaining_depth
is
not
None
and
remaining_depth
<
=
0
:
            
_annotate
(
rem
=
[
[
"
!
limit
"
"
x
"
]
]
)
            
if
is_databag
:
                
return
_flatten_annotated
(
                    
strip_string
(
safe_repr
(
obj
)
max_length
=
max_value_length
)
                
)
            
return
None
        
if
is_databag
and
global_repr_processors
:
            
hints
=
{
"
memo
"
:
memo
"
remaining_depth
"
:
remaining_depth
}
            
for
processor
in
global_repr_processors
:
                
result
=
processor
(
obj
hints
)
                
if
result
is
not
NotImplemented
:
                    
return
_flatten_annotated
(
result
)
        
sentry_repr
=
getattr
(
type
(
obj
)
"
__sentry_repr__
"
None
)
        
if
obj
is
None
or
isinstance
(
obj
(
bool
number_types
)
)
:
            
if
should_repr_strings
or
(
                
isinstance
(
obj
float
)
and
(
math
.
isinf
(
obj
)
or
math
.
isnan
(
obj
)
)
            
)
:
                
return
safe_repr
(
obj
)
            
else
:
                
return
obj
        
elif
callable
(
sentry_repr
)
:
            
return
sentry_repr
(
obj
)
        
elif
isinstance
(
obj
datetime
)
:
            
return
(
                
text_type
(
format_timestamp
(
obj
)
)
                
if
not
should_repr_strings
                
else
safe_repr
(
obj
)
            
)
        
elif
isinstance
(
obj
Mapping
)
:
            
obj
=
dict
(
iteritems
(
obj
)
)
            
rv_dict
=
{
}
            
i
=
0
            
for
k
v
in
iteritems
(
obj
)
:
                
if
remaining_breadth
is
not
None
and
i
>
=
remaining_breadth
:
                    
_annotate
(
len
=
len
(
obj
)
)
                    
break
                
str_k
=
text_type
(
k
)
                
v
=
_serialize_node
(
                    
v
                    
segment
=
str_k
                    
should_repr_strings
=
should_repr_strings
                    
is_databag
=
is_databag
                    
is_request_body
=
is_request_body
                    
remaining_depth
=
(
                        
remaining_depth
-
1
if
remaining_depth
is
not
None
else
None
                    
)
                    
remaining_breadth
=
remaining_breadth
                
)
                
rv_dict
[
str_k
]
=
v
                
i
+
=
1
            
return
rv_dict
        
elif
not
isinstance
(
obj
serializable_str_types
)
and
isinstance
(
            
obj
(
Set
Sequence
)
        
)
:
            
rv_list
=
[
]
            
for
i
v
in
enumerate
(
obj
)
:
                
if
remaining_breadth
is
not
None
and
i
>
=
remaining_breadth
:
                    
_annotate
(
len
=
len
(
obj
)
)
                    
break
                
rv_list
.
append
(
                    
_serialize_node
(
                        
v
                        
segment
=
i
                        
should_repr_strings
=
should_repr_strings
                        
is_databag
=
is_databag
                        
is_request_body
=
is_request_body
                        
remaining_depth
=
(
                            
remaining_depth
-
1
if
remaining_depth
is
not
None
else
None
                        
)
                        
remaining_breadth
=
remaining_breadth
                    
)
                
)
            
return
rv_list
        
if
should_repr_strings
:
            
obj
=
safe_repr
(
obj
)
        
else
:
            
if
isinstance
(
obj
bytes
)
or
isinstance
(
obj
bytearray
)
:
                
obj
=
obj
.
decode
(
"
utf
-
8
"
"
replace
"
)
            
if
not
isinstance
(
obj
string_types
)
:
                
obj
=
safe_repr
(
obj
)
        
is_span_description
=
(
            
len
(
path
)
=
=
3
and
path
[
0
]
=
=
"
spans
"
and
path
[
-
1
]
=
=
"
description
"
        
)
        
if
is_span_description
:
            
return
obj
        
return
_flatten_annotated
(
strip_string
(
obj
max_length
=
max_value_length
)
)
    
disable_capture_event
.
set
(
True
)
    
try
:
        
serialized_event
=
_serialize_node
(
event
*
*
kwargs
)
        
if
meta_stack
and
isinstance
(
serialized_event
dict
)
:
            
serialized_event
[
"
_meta
"
]
=
meta_stack
[
0
]
        
return
serialized_event
    
finally
:
        
disable_capture_event
.
set
(
False
)
