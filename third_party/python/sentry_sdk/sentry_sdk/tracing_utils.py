import
re
import
contextlib
import
json
import
math
from
numbers
import
Real
from
decimal
import
Decimal
import
sentry_sdk
from
sentry_sdk
.
consts
import
OP
from
sentry_sdk
.
utils
import
(
    
capture_internal_exceptions
    
Dsn
    
logger
    
safe_str
    
to_base64
    
to_string
    
from_base64
)
from
sentry_sdk
.
_compat
import
PY2
iteritems
from
sentry_sdk
.
_types
import
MYPY
if
PY2
:
    
from
collections
import
Mapping
    
from
urllib
import
quote
unquote
else
:
    
from
collections
.
abc
import
Mapping
    
from
urllib
.
parse
import
quote
unquote
if
MYPY
:
    
import
typing
    
from
typing
import
Generator
    
from
typing
import
Optional
    
from
typing
import
Any
    
from
typing
import
Dict
    
from
typing
import
Union
SENTRY_TRACE_REGEX
=
re
.
compile
(
    
"
^
[
\
t
]
*
"
    
"
(
[
0
-
9a
-
f
]
{
32
}
)
?
"
    
"
-
?
(
[
0
-
9a
-
f
]
{
16
}
)
?
"
    
"
-
?
(
[
01
]
)
?
"
    
"
[
\
t
]
*
"
)
base64_stripped
=
(
    
"
(
[
a
-
zA
-
Z0
-
9
+
/
]
{
4
}
)
*
"
    
"
(
[
a
-
zA
-
Z0
-
9
+
/
]
{
2
3
}
)
?
"
)
tracestate_entry
=
"
[
^
=
]
+
=
[
^
=
]
+
"
TRACESTATE_ENTRIES_REGEX
=
re
.
compile
(
    
"
^
(
{
te
}
)
+
"
    
"
(
|
)
"
.
format
(
te
=
tracestate_entry
)
)
SENTRY_TRACESTATE_ENTRY_REGEX
=
re
.
compile
(
    
"
(
?
:
^
|
.
+
)
"
    
"
(
sentry
=
[
^
]
*
)
"
    
"
(
?
:
.
+
|
)
"
)
class
EnvironHeaders
(
Mapping
)
:
    
def
__init__
(
        
self
        
environ
        
prefix
=
"
HTTP_
"
    
)
:
        
self
.
environ
=
environ
        
self
.
prefix
=
prefix
    
def
__getitem__
(
self
key
)
:
        
return
self
.
environ
[
self
.
prefix
+
key
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
.
upper
(
)
]
    
def
__len__
(
self
)
:
        
return
sum
(
1
for
_
in
iter
(
self
)
)
    
def
__iter__
(
self
)
:
        
for
k
in
self
.
environ
:
            
if
not
isinstance
(
k
str
)
:
                
continue
            
k
=
k
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
.
upper
(
)
            
if
not
k
.
startswith
(
self
.
prefix
)
:
                
continue
            
yield
k
[
len
(
self
.
prefix
)
:
]
def
has_tracing_enabled
(
options
)
:
    
"
"
"
    
Returns
True
if
either
traces_sample_rate
or
traces_sampler
is
    
defined
False
otherwise
.
    
"
"
"
    
return
bool
(
        
options
.
get
(
"
traces_sample_rate
"
)
is
not
None
        
or
options
.
get
(
"
traces_sampler
"
)
is
not
None
    
)
def
is_valid_sample_rate
(
rate
)
:
    
"
"
"
    
Checks
the
given
sample
rate
to
make
sure
it
is
valid
type
and
value
(
a
    
boolean
or
a
number
between
0
and
1
inclusive
)
.
    
"
"
"
    
if
not
isinstance
(
rate
(
Real
Decimal
)
)
or
math
.
isnan
(
rate
)
:
        
logger
.
warning
(
            
"
[
Tracing
]
Given
sample
rate
is
invalid
.
Sample
rate
must
be
a
boolean
or
a
number
between
0
and
1
.
Got
{
rate
}
of
type
{
type
}
.
"
.
format
(
                
rate
=
rate
type
=
type
(
rate
)
            
)
        
)
        
return
False
    
rate
=
float
(
rate
)
    
if
rate
<
0
or
rate
>
1
:
        
logger
.
warning
(
            
"
[
Tracing
]
Given
sample
rate
is
invalid
.
Sample
rate
must
be
between
0
and
1
.
Got
{
rate
}
.
"
.
format
(
                
rate
=
rate
            
)
        
)
        
return
False
    
return
True
contextlib
.
contextmanager
def
record_sql_queries
(
    
hub
    
cursor
    
query
    
params_list
    
paramstyle
    
executemany
)
:
    
if
hub
.
client
and
hub
.
client
.
options
[
"
_experiments
"
]
.
get
(
        
"
record_sql_params
"
False
    
)
:
        
if
not
params_list
or
params_list
=
=
[
None
]
:
            
params_list
=
None
        
if
paramstyle
=
=
"
pyformat
"
:
            
paramstyle
=
"
format
"
    
else
:
        
params_list
=
None
        
paramstyle
=
None
    
query
=
_format_sql
(
cursor
query
)
    
data
=
{
}
    
if
params_list
is
not
None
:
        
data
[
"
db
.
params
"
]
=
params_list
    
if
paramstyle
is
not
None
:
        
data
[
"
db
.
paramstyle
"
]
=
paramstyle
    
if
executemany
:
        
data
[
"
db
.
executemany
"
]
=
True
    
with
capture_internal_exceptions
(
)
:
        
hub
.
add_breadcrumb
(
message
=
query
category
=
"
query
"
data
=
data
)
    
with
hub
.
start_span
(
op
=
OP
.
DB
description
=
query
)
as
span
:
        
for
k
v
in
data
.
items
(
)
:
            
span
.
set_data
(
k
v
)
        
yield
span
def
maybe_create_breadcrumbs_from_span
(
hub
span
)
:
    
if
span
.
op
=
=
OP
.
DB_REDIS
:
        
hub
.
add_breadcrumb
(
            
message
=
span
.
description
type
=
"
redis
"
category
=
"
redis
"
data
=
span
.
_tags
        
)
    
elif
span
.
op
=
=
OP
.
HTTP_CLIENT
:
        
hub
.
add_breadcrumb
(
type
=
"
http
"
category
=
"
httplib
"
data
=
span
.
_data
)
    
elif
span
.
op
=
=
"
subprocess
"
:
        
hub
.
add_breadcrumb
(
            
type
=
"
subprocess
"
            
category
=
"
subprocess
"
            
message
=
span
.
description
            
data
=
span
.
_data
        
)
def
extract_sentrytrace_data
(
header
)
:
    
"
"
"
    
Given
a
sentry
-
trace
header
string
return
a
dictionary
of
data
.
    
"
"
"
    
if
not
header
:
        
return
None
    
if
header
.
startswith
(
"
00
-
"
)
and
header
.
endswith
(
"
-
00
"
)
:
        
header
=
header
[
3
:
-
3
]
    
match
=
SENTRY_TRACE_REGEX
.
match
(
header
)
    
if
not
match
:
        
return
None
    
trace_id
parent_span_id
sampled_str
=
match
.
groups
(
)
    
parent_sampled
=
None
    
if
trace_id
:
        
trace_id
=
"
{
:
032x
}
"
.
format
(
int
(
trace_id
16
)
)
    
if
parent_span_id
:
        
parent_span_id
=
"
{
:
016x
}
"
.
format
(
int
(
parent_span_id
16
)
)
    
if
sampled_str
:
        
parent_sampled
=
sampled_str
!
=
"
0
"
    
return
{
        
"
trace_id
"
:
trace_id
        
"
parent_span_id
"
:
parent_span_id
        
"
parent_sampled
"
:
parent_sampled
    
}
def
extract_tracestate_data
(
header
)
:
    
"
"
"
    
Extracts
the
sentry
tracestate
value
and
any
third
-
party
data
from
the
given
    
tracestate
header
returning
a
dictionary
of
data
.
    
"
"
"
    
sentry_entry
=
third_party_entry
=
None
    
before
=
after
=
"
"
    
if
header
:
        
sentry_match
=
SENTRY_TRACESTATE_ENTRY_REGEX
.
search
(
header
)
        
if
sentry_match
:
            
sentry_entry
=
sentry_match
.
group
(
1
)
            
before
after
=
map
(
lambda
s
:
s
.
strip
(
"
"
)
header
.
split
(
sentry_entry
)
)
            
sentry_value
=
sentry_entry
.
replace
(
"
sentry
=
"
"
"
)
            
if
not
re
.
search
(
"
^
{
b64
}
"
.
format
(
b64
=
base64_stripped
)
sentry_value
)
:
                
sentry_entry
=
None
        
else
:
            
after
=
header
        
third_party_entry
=
(
            
"
"
.
join
(
filter
(
TRACESTATE_ENTRIES_REGEX
.
search
[
before
after
]
)
)
or
None
        
)
    
return
{
        
"
sentry_tracestate
"
:
sentry_entry
        
"
third_party_tracestate
"
:
third_party_entry
    
}
def
compute_tracestate_value
(
data
)
:
    
"
"
"
    
Computes
a
new
tracestate
value
using
the
given
data
.
    
Note
:
Returns
just
the
base64
-
encoded
data
NOT
the
full
sentry
=
.
.
.
    
tracestate
entry
.
    
"
"
"
    
tracestate_json
=
json
.
dumps
(
data
default
=
safe_str
)
    
return
(
to_base64
(
tracestate_json
)
or
"
"
)
.
rstrip
(
"
=
"
)
def
compute_tracestate_entry
(
span
)
:
    
"
"
"
    
Computes
a
new
sentry
tracestate
for
the
span
.
Includes
the
sentry
=
.
    
Will
return
None
if
there
'
s
no
client
and
/
or
no
DSN
.
    
"
"
"
    
data
=
{
}
    
hub
=
span
.
hub
or
sentry_sdk
.
Hub
.
current
    
client
=
hub
.
client
    
scope
=
hub
.
scope
    
if
client
and
client
.
options
.
get
(
"
dsn
"
)
:
        
options
=
client
.
options
        
user
=
scope
.
_user
        
data
=
{
            
"
trace_id
"
:
span
.
trace_id
            
"
environment
"
:
options
[
"
environment
"
]
            
"
release
"
:
options
.
get
(
"
release
"
)
            
"
public_key
"
:
Dsn
(
options
[
"
dsn
"
]
)
.
public_key
        
}
        
if
user
and
(
user
.
get
(
"
id
"
)
or
user
.
get
(
"
segment
"
)
)
:
            
user_data
=
{
}
            
if
user
.
get
(
"
id
"
)
:
                
user_data
[
"
id
"
]
=
user
[
"
id
"
]
            
if
user
.
get
(
"
segment
"
)
:
                
user_data
[
"
segment
"
]
=
user
[
"
segment
"
]
            
data
[
"
user
"
]
=
user_data
        
if
span
.
containing_transaction
:
            
data
[
"
transaction
"
]
=
span
.
containing_transaction
.
name
        
return
"
sentry
=
"
+
compute_tracestate_value
(
data
)
    
return
None
def
reinflate_tracestate
(
encoded_tracestate
)
:
    
"
"
"
    
Given
a
sentry
tracestate
value
in
its
encoded
form
translate
it
back
into
    
a
dictionary
of
data
.
    
"
"
"
    
inflated_tracestate
=
None
    
if
encoded_tracestate
:
        
tracestate_json
=
from_base64
(
encoded_tracestate
+
"
=
=
"
)
        
try
:
            
assert
tracestate_json
is
not
None
            
inflated_tracestate
=
json
.
loads
(
tracestate_json
)
        
except
Exception
as
err
:
            
logger
.
warning
(
                
(
                    
"
Unable
to
attach
tracestate
data
to
envelope
header
:
{
err
}
"
                    
+
"
\
nTracestate
value
is
{
encoded_tracestate
}
"
                
)
.
format
(
err
=
err
encoded_tracestate
=
encoded_tracestate
)
            
)
    
return
inflated_tracestate
def
_format_sql
(
cursor
sql
)
:
    
real_sql
=
None
    
try
:
        
if
hasattr
(
cursor
"
mogrify
"
)
:
            
real_sql
=
cursor
.
mogrify
(
sql
)
            
if
isinstance
(
real_sql
bytes
)
:
                
real_sql
=
real_sql
.
decode
(
cursor
.
connection
.
encoding
)
    
except
Exception
:
        
real_sql
=
None
    
return
real_sql
or
to_string
(
sql
)
def
has_tracestate_enabled
(
span
=
None
)
:
    
client
=
(
(
span
and
span
.
hub
)
or
sentry_sdk
.
Hub
.
current
)
.
client
    
options
=
client
and
client
.
options
    
return
bool
(
options
and
options
[
"
_experiments
"
]
.
get
(
"
propagate_tracestate
"
)
)
def
has_custom_measurements_enabled
(
)
:
    
client
=
sentry_sdk
.
Hub
.
current
.
client
    
options
=
client
and
client
.
options
    
return
bool
(
options
and
options
[
"
_experiments
"
]
.
get
(
"
custom_measurements
"
)
)
class
Baggage
(
object
)
:
    
__slots__
=
(
"
sentry_items
"
"
third_party_items
"
"
mutable
"
)
    
SENTRY_PREFIX
=
"
sentry
-
"
    
SENTRY_PREFIX_REGEX
=
re
.
compile
(
"
^
sentry
-
"
)
    
DSC_KEYS
=
[
        
"
trace_id
"
        
"
public_key
"
        
"
sample_rate
"
        
"
release
"
        
"
environment
"
        
"
transaction
"
        
"
user_id
"
        
"
user_segment
"
    
]
    
def
__init__
(
        
self
        
sentry_items
        
third_party_items
=
"
"
        
mutable
=
True
    
)
:
        
self
.
sentry_items
=
sentry_items
        
self
.
third_party_items
=
third_party_items
        
self
.
mutable
=
mutable
    
classmethod
    
def
from_incoming_header
(
cls
header
)
:
        
"
"
"
        
freeze
if
incoming
header
already
has
sentry
baggage
        
"
"
"
        
sentry_items
=
{
}
        
third_party_items
=
"
"
        
mutable
=
True
        
if
header
:
            
for
item
in
header
.
split
(
"
"
)
:
                
if
"
=
"
not
in
item
:
                    
continue
                
with
capture_internal_exceptions
(
)
:
                    
item
=
item
.
strip
(
)
                    
key
val
=
item
.
split
(
"
=
"
)
                    
if
Baggage
.
SENTRY_PREFIX_REGEX
.
match
(
key
)
:
                        
baggage_key
=
unquote
(
key
.
split
(
"
-
"
)
[
1
]
)
                        
sentry_items
[
baggage_key
]
=
unquote
(
val
)
                        
mutable
=
False
                    
else
:
                        
third_party_items
+
=
(
"
"
if
third_party_items
else
"
"
)
+
item
        
return
Baggage
(
sentry_items
third_party_items
mutable
)
    
classmethod
    
def
populate_from_transaction
(
cls
transaction
)
:
        
"
"
"
        
Populate
fresh
baggage
entry
with
sentry_items
and
make
it
immutable
        
if
this
is
the
head
SDK
which
originates
traces
.
        
"
"
"
        
hub
=
transaction
.
hub
or
sentry_sdk
.
Hub
.
current
        
client
=
hub
.
client
        
sentry_items
=
{
}
        
if
not
client
:
            
return
Baggage
(
sentry_items
)
        
options
=
client
.
options
or
{
}
        
user
=
(
hub
.
scope
and
hub
.
scope
.
_user
)
or
{
}
        
sentry_items
[
"
trace_id
"
]
=
transaction
.
trace_id
        
if
options
.
get
(
"
environment
"
)
:
            
sentry_items
[
"
environment
"
]
=
options
[
"
environment
"
]
        
if
options
.
get
(
"
release
"
)
:
            
sentry_items
[
"
release
"
]
=
options
[
"
release
"
]
        
if
options
.
get
(
"
dsn
"
)
:
            
sentry_items
[
"
public_key
"
]
=
Dsn
(
options
[
"
dsn
"
]
)
.
public_key
        
if
(
            
transaction
.
name
            
and
transaction
.
source
not
in
LOW_QUALITY_TRANSACTION_SOURCES
        
)
:
            
sentry_items
[
"
transaction
"
]
=
transaction
.
name
        
if
user
.
get
(
"
segment
"
)
:
            
sentry_items
[
"
user_segment
"
]
=
user
[
"
segment
"
]
        
if
transaction
.
sample_rate
is
not
None
:
            
sentry_items
[
"
sample_rate
"
]
=
str
(
transaction
.
sample_rate
)
        
if
transaction
.
_baggage
and
transaction
.
_baggage
.
sentry_items
:
            
sentry_items
.
update
(
transaction
.
_baggage
.
sentry_items
)
        
return
Baggage
(
sentry_items
mutable
=
False
)
    
def
freeze
(
self
)
:
        
self
.
mutable
=
False
    
def
dynamic_sampling_context
(
self
)
:
        
header
=
{
}
        
for
key
in
Baggage
.
DSC_KEYS
:
            
item
=
self
.
sentry_items
.
get
(
key
)
            
if
item
:
                
header
[
key
]
=
item
        
return
header
    
def
serialize
(
self
include_third_party
=
False
)
:
        
items
=
[
]
        
for
key
val
in
iteritems
(
self
.
sentry_items
)
:
            
with
capture_internal_exceptions
(
)
:
                
item
=
Baggage
.
SENTRY_PREFIX
+
quote
(
key
)
+
"
=
"
+
quote
(
str
(
val
)
)
                
items
.
append
(
item
)
        
if
include_third_party
:
            
items
.
append
(
self
.
third_party_items
)
        
return
"
"
.
join
(
items
)
from
sentry_sdk
.
tracing
import
LOW_QUALITY_TRANSACTION_SOURCES
if
MYPY
:
    
from
sentry_sdk
.
tracing
import
Span
Transaction
