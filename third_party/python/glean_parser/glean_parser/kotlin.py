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
Kotlin
code
for
metrics
.
"
"
"
from
collections
import
OrderedDict
import
enum
import
json
from
pathlib
import
Path
from
typing
import
Any
Dict
List
Union
from
.
import
metrics
from
.
import
pings
from
.
import
util
def
kotlin_datatypes_filter
(
value
:
util
.
JSONType
)
-
>
str
:
    
"
"
"
    
A
Jinja2
filter
that
renders
Kotlin
literals
.
    
Based
on
Python
'
s
JSONEncoder
but
overrides
:
      
-
lists
to
use
listOf
      
-
dicts
to
use
mapOf
      
-
sets
to
use
setOf
      
-
enums
to
use
the
like
-
named
Kotlin
enum
    
"
"
"
    
class
KotlinEncoder
(
json
.
JSONEncoder
)
:
        
def
iterencode
(
self
value
)
:
            
if
isinstance
(
value
list
)
:
                
yield
"
listOf
(
"
                
first
=
True
                
for
subvalue
in
value
:
                    
if
not
first
:
                        
yield
"
"
                    
yield
from
self
.
iterencode
(
subvalue
)
                    
first
=
False
                
yield
"
)
"
            
elif
isinstance
(
value
dict
)
:
                
yield
"
mapOf
(
"
                
first
=
True
                
for
key
subvalue
in
value
.
items
(
)
:
                    
if
not
first
:
                        
yield
"
"
                    
yield
from
self
.
iterencode
(
key
)
                    
yield
"
to
"
                    
yield
from
self
.
iterencode
(
subvalue
)
                    
first
=
False
                
yield
"
)
"
            
elif
isinstance
(
value
enum
.
Enum
)
:
                
yield
(
value
.
__class__
.
__name__
+
"
.
"
+
util
.
Camelize
(
value
.
name
)
)
            
elif
isinstance
(
value
set
)
:
                
yield
"
setOf
(
"
                
first
=
True
                
for
subvalue
in
sorted
(
list
(
value
)
)
:
                    
if
not
first
:
                        
yield
"
"
                    
yield
from
self
.
iterencode
(
subvalue
)
                    
first
=
False
                
yield
"
)
"
            
else
:
                
yield
from
super
(
)
.
iterencode
(
value
)
    
return
"
"
.
join
(
KotlinEncoder
(
)
.
iterencode
(
value
)
)
def
type_name
(
obj
:
Union
[
metrics
.
Metric
pings
.
Ping
]
)
-
>
str
:
    
"
"
"
    
Returns
the
Kotlin
type
to
use
for
a
given
metric
or
ping
object
.
    
"
"
"
    
generate_enums
=
getattr
(
obj
"
_generate_enums
"
[
]
)
    
if
len
(
generate_enums
)
:
        
template_args
=
[
]
        
for
member
suffix
in
generate_enums
:
            
if
len
(
getattr
(
obj
member
)
)
:
                
template_args
.
append
(
util
.
camelize
(
obj
.
name
)
+
suffix
)
            
else
:
                
if
suffix
=
=
"
Keys
"
:
                    
template_args
.
append
(
"
NoExtraKeys
"
)
                
else
:
                    
template_args
.
append
(
"
No
"
+
suffix
)
        
return
"
{
}
<
{
}
>
"
.
format
(
class_name
(
obj
.
type
)
"
"
.
join
(
template_args
)
)
    
return
class_name
(
obj
.
type
)
def
class_name
(
obj_type
:
str
)
-
>
str
:
    
"
"
"
    
Returns
the
Kotlin
class
name
for
a
given
metric
or
ping
type
.
    
"
"
"
    
if
obj_type
=
=
"
ping
"
:
        
return
"
PingType
"
    
if
obj_type
.
startswith
(
"
labeled_
"
)
:
        
obj_type
=
obj_type
[
8
:
]
    
return
util
.
Camelize
(
obj_type
)
+
"
MetricType
"
def
output_gecko_lookup
(
    
objs
:
metrics
.
ObjectTree
output_dir
:
Path
options
:
Dict
[
str
Any
]
=
{
}
)
-
>
None
:
    
"
"
"
    
Given
a
tree
of
objects
generate
a
Kotlin
map
between
Gecko
histograms
and
    
Glean
SDK
metric
types
.
    
:
param
objects
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
output_dir
:
Path
to
an
output
directory
to
write
to
.
    
:
param
options
:
options
dictionary
with
the
following
optional
keys
:
        
-
namespace
:
The
package
namespace
to
declare
at
the
top
of
the
          
generated
files
.
Defaults
to
GleanMetrics
.
        
-
glean_namespace
:
The
package
namespace
of
the
glean
library
itself
.
          
This
is
where
glean
objects
will
be
imported
from
in
the
generated
          
code
.
    
"
"
"
    
template
=
util
.
get_jinja2_template
(
        
"
kotlin
.
geckoview
.
jinja2
"
        
filters
=
(
            
(
"
kotlin
"
kotlin_datatypes_filter
)
            
(
"
type_name
"
type_name
)
            
(
"
class_name
"
class_name
)
        
)
    
)
    
namespace
=
options
.
get
(
"
namespace
"
"
GleanMetrics
"
)
    
glean_namespace
=
options
.
get
(
"
glean_namespace
"
"
mozilla
.
components
.
service
.
glean
"
)
    
gecko_metrics
:
OrderedDict
[
        
str
OrderedDict
[
str
List
[
Dict
[
str
str
]
]
]
    
]
=
OrderedDict
(
)
    
SCALAR_LIKE_TYPES
=
[
"
boolean
"
"
string
"
"
quantity
"
]
    
for
category_key
category_val
in
objs
.
items
(
)
:
        
for
metric
in
category_val
.
values
(
)
:
            
if
isinstance
(
metric
pings
.
Ping
)
or
not
getattr
(
                
metric
"
gecko_datapoint
"
False
            
)
:
                
continue
            
type_category
=
"
histograms
"
            
if
metric
.
type
in
SCALAR_LIKE_TYPES
:
                
type_category
=
metric
.
type
            
elif
metric
.
type
=
=
"
labeled_counter
"
:
                
type_category
=
"
categoricals
"
            
gecko_metrics
.
setdefault
(
type_category
OrderedDict
(
)
)
            
gecko_metrics
[
type_category
]
.
setdefault
(
category_key
[
]
)
            
gecko_metrics
[
type_category
]
[
category_key
]
.
append
(
                
{
"
gecko_datapoint
"
:
metric
.
gecko_datapoint
"
name
"
:
metric
.
name
}
            
)
    
if
not
gecko_metrics
:
        
return
    
filepath
=
output_dir
/
"
GleanGeckoMetricsMapping
.
kt
"
    
with
filepath
.
open
(
"
w
"
encoding
=
"
utf
-
8
"
)
as
fd
:
        
fd
.
write
(
            
template
.
render
(
                
gecko_metrics
=
gecko_metrics
                
namespace
=
namespace
                
glean_namespace
=
glean_namespace
            
)
        
)
        
fd
.
write
(
"
\
n
"
)
def
output_kotlin
(
    
objs
:
metrics
.
ObjectTree
output_dir
:
Path
options
:
Dict
[
str
Any
]
=
{
}
)
-
>
None
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
Kotlin
code
to
output_dir
.
    
:
param
objects
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
output_dir
:
Path
to
an
output
directory
to
write
to
.
    
:
param
options
:
options
dictionary
with
the
following
optional
keys
:
        
-
namespace
:
The
package
namespace
to
declare
at
the
top
of
the
          
generated
files
.
Defaults
to
GleanMetrics
.
        
-
glean_namespace
:
The
package
namespace
of
the
glean
library
itself
.
          
This
is
where
glean
objects
will
be
imported
from
in
the
generated
          
code
.
    
"
"
"
    
template
=
util
.
get_jinja2_template
(
        
"
kotlin
.
jinja2
"
        
filters
=
(
            
(
"
kotlin
"
kotlin_datatypes_filter
)
            
(
"
type_name
"
type_name
)
            
(
"
class_name
"
class_name
)
        
)
    
)
    
namespace
=
options
.
get
(
"
namespace
"
"
GleanMetrics
"
)
    
glean_namespace
=
options
.
get
(
"
glean_namespace
"
"
mozilla
.
components
.
service
.
glean
"
)
    
for
category_key
category_val
in
objs
.
items
(
)
:
        
filename
=
util
.
Camelize
(
category_key
)
+
"
.
kt
"
        
filepath
=
output_dir
/
filename
        
obj_types
=
sorted
(
            
list
(
set
(
class_name
(
obj
.
type
)
for
obj
in
category_val
.
values
(
)
)
)
        
)
        
has_labeled_metrics
=
any
(
            
getattr
(
metric
"
labeled
"
False
)
for
metric
in
category_val
.
values
(
)
        
)
        
with
filepath
.
open
(
"
w
"
encoding
=
"
utf
-
8
"
)
as
fd
:
            
fd
.
write
(
                
template
.
render
(
                    
category_name
=
category_key
                    
objs
=
category_val
                    
obj_types
=
obj_types
                    
extra_args
=
util
.
extra_args
                    
namespace
=
namespace
                    
has_labeled_metrics
=
has_labeled_metrics
                    
glean_namespace
=
glean_namespace
                
)
            
)
            
fd
.
write
(
"
\
n
"
)
    
output_gecko_lookup
(
objs
output_dir
options
)
