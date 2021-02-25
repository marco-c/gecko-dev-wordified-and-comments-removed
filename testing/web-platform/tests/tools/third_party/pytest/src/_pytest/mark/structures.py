import
collections
.
abc
import
inspect
import
typing
import
warnings
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
Iterable
from
typing
import
Iterator
from
typing
import
List
from
typing
import
Mapping
from
typing
import
NamedTuple
from
typing
import
Optional
from
typing
import
Sequence
from
typing
import
Set
from
typing
import
Tuple
from
typing
import
TypeVar
from
typing
import
Union
import
attr
from
.
.
_code
import
getfslineno
from
.
.
compat
import
ascii_escaped
from
.
.
compat
import
final
from
.
.
compat
import
NOTSET
from
.
.
compat
import
NotSetType
from
.
.
compat
import
overload
from
.
.
compat
import
TYPE_CHECKING
from
_pytest
.
config
import
Config
from
_pytest
.
outcomes
import
fail
from
_pytest
.
warning_types
import
PytestUnknownMarkWarning
if
TYPE_CHECKING
:
    
from
typing
import
Type
    
from
.
.
nodes
import
Node
EMPTY_PARAMETERSET_OPTION
=
"
empty_parameter_set_mark
"
def
istestfunc
(
func
)
-
>
bool
:
    
return
(
        
hasattr
(
func
"
__call__
"
)
        
and
getattr
(
func
"
__name__
"
"
<
lambda
>
"
)
!
=
"
<
lambda
>
"
    
)
def
get_empty_parameterset_mark
(
    
config
:
Config
argnames
:
Sequence
[
str
]
func
)
-
>
"
MarkDecorator
"
:
    
from
.
.
nodes
import
Collector
    
fs
lineno
=
getfslineno
(
func
)
    
reason
=
"
got
empty
parameter
set
%
r
function
%
s
at
%
s
:
%
d
"
%
(
        
argnames
        
func
.
__name__
        
fs
        
lineno
    
)
    
requested_mark
=
config
.
getini
(
EMPTY_PARAMETERSET_OPTION
)
    
if
requested_mark
in
(
"
"
None
"
skip
"
)
:
        
mark
=
MARK_GEN
.
skip
(
reason
=
reason
)
    
elif
requested_mark
=
=
"
xfail
"
:
        
mark
=
MARK_GEN
.
xfail
(
reason
=
reason
run
=
False
)
    
elif
requested_mark
=
=
"
fail_at_collect
"
:
        
f_name
=
func
.
__name__
        
_
lineno
=
getfslineno
(
func
)
        
raise
Collector
.
CollectError
(
            
"
Empty
parameter
set
in
'
%
s
'
at
line
%
d
"
%
(
f_name
lineno
+
1
)
        
)
    
else
:
        
raise
LookupError
(
requested_mark
)
    
return
mark
class
ParameterSet
(
    
NamedTuple
(
        
"
ParameterSet
"
        
[
            
(
"
values
"
Sequence
[
Union
[
object
NotSetType
]
]
)
            
(
"
marks
"
"
typing
.
Collection
[
Union
[
MarkDecorator
Mark
]
]
"
)
            
(
"
id
"
Optional
[
str
]
)
        
]
    
)
)
:
    
classmethod
    
def
param
(
        
cls
        
*
values
:
object
        
marks
:
"
Union
[
MarkDecorator
typing
.
Collection
[
Union
[
MarkDecorator
Mark
]
]
]
"
=
(
)
        
id
:
Optional
[
str
]
=
None
    
)
-
>
"
ParameterSet
"
:
        
if
isinstance
(
marks
MarkDecorator
)
:
            
marks
=
(
marks
)
        
else
:
            
assert
isinstance
(
marks
(
collections
.
abc
.
Sequence
set
)
)
        
if
id
is
not
None
:
            
if
not
isinstance
(
id
str
)
:
                
raise
TypeError
(
                    
"
Expected
id
to
be
a
string
got
{
}
:
{
!
r
}
"
.
format
(
type
(
id
)
id
)
                
)
            
id
=
ascii_escaped
(
id
)
        
return
cls
(
values
marks
id
)
    
classmethod
    
def
extract_from
(
        
cls
        
parameterset
:
Union
[
"
ParameterSet
"
Sequence
[
object
]
object
]
        
force_tuple
:
bool
=
False
    
)
-
>
"
ParameterSet
"
:
        
"
"
"
Extract
from
an
object
or
objects
.
        
:
param
parameterset
:
            
A
legacy
style
parameterset
that
may
or
may
not
be
a
tuple
            
and
may
or
may
not
be
wrapped
into
a
mess
of
mark
objects
.
        
:
param
force_tuple
:
            
Enforce
tuple
wrapping
so
single
argument
tuple
values
            
don
'
t
get
decomposed
and
break
tests
.
        
"
"
"
        
if
isinstance
(
parameterset
cls
)
:
            
return
parameterset
        
if
force_tuple
:
            
return
cls
.
param
(
parameterset
)
        
else
:
            
return
cls
(
parameterset
marks
=
[
]
id
=
None
)
    
staticmethod
    
def
_parse_parametrize_args
(
        
argnames
:
Union
[
str
List
[
str
]
Tuple
[
str
.
.
.
]
]
        
argvalues
:
Iterable
[
Union
[
"
ParameterSet
"
Sequence
[
object
]
object
]
]
        
*
args
        
*
*
kwargs
    
)
-
>
Tuple
[
Union
[
List
[
str
]
Tuple
[
str
.
.
.
]
]
bool
]
:
        
if
not
isinstance
(
argnames
(
tuple
list
)
)
:
            
argnames
=
[
x
.
strip
(
)
for
x
in
argnames
.
split
(
"
"
)
if
x
.
strip
(
)
]
            
force_tuple
=
len
(
argnames
)
=
=
1
        
else
:
            
force_tuple
=
False
        
return
argnames
force_tuple
    
staticmethod
    
def
_parse_parametrize_parameters
(
        
argvalues
:
Iterable
[
Union
[
"
ParameterSet
"
Sequence
[
object
]
object
]
]
        
force_tuple
:
bool
    
)
-
>
List
[
"
ParameterSet
"
]
:
        
return
[
            
ParameterSet
.
extract_from
(
x
force_tuple
=
force_tuple
)
for
x
in
argvalues
        
]
    
classmethod
    
def
_for_parametrize
(
        
cls
        
argnames
:
Union
[
str
List
[
str
]
Tuple
[
str
.
.
.
]
]
        
argvalues
:
Iterable
[
Union
[
"
ParameterSet
"
Sequence
[
object
]
object
]
]
        
func
        
config
:
Config
        
nodeid
:
str
    
)
-
>
Tuple
[
Union
[
List
[
str
]
Tuple
[
str
.
.
.
]
]
List
[
"
ParameterSet
"
]
]
:
        
argnames
force_tuple
=
cls
.
_parse_parametrize_args
(
argnames
argvalues
)
        
parameters
=
cls
.
_parse_parametrize_parameters
(
argvalues
force_tuple
)
        
del
argvalues
        
if
parameters
:
            
for
param
in
parameters
:
                
if
len
(
param
.
values
)
!
=
len
(
argnames
)
:
                    
msg
=
(
                        
'
{
nodeid
}
:
in
"
parametrize
"
the
number
of
names
(
{
names_len
}
)
:
\
n
'
                        
"
{
names
}
\
n
"
                        
"
must
be
equal
to
the
number
of
values
(
{
values_len
}
)
:
\
n
"
                        
"
{
values
}
"
                    
)
                    
fail
(
                        
msg
.
format
(
                            
nodeid
=
nodeid
                            
values
=
param
.
values
                            
names
=
argnames
                            
names_len
=
len
(
argnames
)
                            
values_len
=
len
(
param
.
values
)
                        
)
                        
pytrace
=
False
                    
)
        
else
:
            
mark
=
get_empty_parameterset_mark
(
config
argnames
func
)
            
parameters
.
append
(
                
ParameterSet
(
values
=
(
NOTSET
)
*
len
(
argnames
)
marks
=
[
mark
]
id
=
None
)
            
)
        
return
argnames
parameters
final
attr
.
s
(
frozen
=
True
)
class
Mark
:
    
name
=
attr
.
ib
(
type
=
str
)
    
args
=
attr
.
ib
(
type
=
Tuple
[
Any
.
.
.
]
)
    
kwargs
=
attr
.
ib
(
type
=
Mapping
[
str
Any
]
)
    
_param_ids_from
=
attr
.
ib
(
type
=
Optional
[
"
Mark
"
]
default
=
None
repr
=
False
)
    
_param_ids_generated
=
attr
.
ib
(
        
type
=
Optional
[
Sequence
[
str
]
]
default
=
None
repr
=
False
    
)
    
def
_has_param_ids
(
self
)
-
>
bool
:
        
return
"
ids
"
in
self
.
kwargs
or
len
(
self
.
args
)
>
=
4
    
def
combined_with
(
self
other
:
"
Mark
"
)
-
>
"
Mark
"
:
        
"
"
"
Return
a
new
Mark
which
is
a
combination
of
this
        
Mark
and
another
Mark
.
        
Combines
by
appending
args
and
merging
kwargs
.
        
:
param
Mark
other
:
The
mark
to
combine
with
.
        
:
rtype
:
Mark
        
"
"
"
        
assert
self
.
name
=
=
other
.
name
        
param_ids_from
=
None
        
if
self
.
name
=
=
"
parametrize
"
:
            
if
other
.
_has_param_ids
(
)
:
                
param_ids_from
=
other
            
elif
self
.
_has_param_ids
(
)
:
                
param_ids_from
=
self
        
return
Mark
(
            
self
.
name
            
self
.
args
+
other
.
args
            
dict
(
self
.
kwargs
*
*
other
.
kwargs
)
            
param_ids_from
=
param_ids_from
        
)
_Markable
=
TypeVar
(
"
_Markable
"
bound
=
Union
[
Callable
[
.
.
.
object
]
type
]
)
attr
.
s
class
MarkDecorator
:
    
"
"
"
A
decorator
for
applying
a
mark
on
test
functions
and
classes
.
    
MarkDecorators
are
created
with
pytest
.
mark
:
:
        
mark1
=
pytest
.
mark
.
NAME
#
Simple
MarkDecorator
        
mark2
=
pytest
.
mark
.
NAME
(
name1
=
value
)
#
Parametrized
MarkDecorator
    
and
can
then
be
applied
as
decorators
to
test
functions
:
:
        
mark2
        
def
test_function
(
)
:
            
pass
    
When
a
MarkDecorator
is
called
it
does
the
following
:
    
1
.
If
called
with
a
single
class
as
its
only
positional
argument
and
no
       
additional
keyword
arguments
it
attaches
the
mark
to
the
class
so
it
       
gets
applied
automatically
to
all
test
cases
found
in
that
class
.
    
2
.
If
called
with
a
single
function
as
its
only
positional
argument
and
       
no
additional
keyword
arguments
it
attaches
the
mark
to
the
function
       
containing
all
the
arguments
already
stored
internally
in
the
       
MarkDecorator
.
    
3
.
When
called
in
any
other
case
it
returns
a
new
MarkDecorator
instance
       
with
the
original
MarkDecorator
'
s
content
updated
with
the
arguments
       
passed
to
this
call
.
    
Note
:
The
rules
above
prevent
MarkDecorators
from
storing
only
a
single
    
function
or
class
reference
as
their
positional
argument
with
no
    
additional
keyword
or
positional
arguments
.
You
can
work
around
this
by
    
using
with_args
(
)
.
    
"
"
"
    
mark
=
attr
.
ib
(
type
=
Mark
validator
=
attr
.
validators
.
instance_of
(
Mark
)
)
    
property
    
def
name
(
self
)
-
>
str
:
        
"
"
"
Alias
for
mark
.
name
.
"
"
"
        
return
self
.
mark
.
name
    
property
    
def
args
(
self
)
-
>
Tuple
[
Any
.
.
.
]
:
        
"
"
"
Alias
for
mark
.
args
.
"
"
"
        
return
self
.
mark
.
args
    
property
    
def
kwargs
(
self
)
-
>
Mapping
[
str
Any
]
:
        
"
"
"
Alias
for
mark
.
kwargs
.
"
"
"
        
return
self
.
mark
.
kwargs
    
property
    
def
markname
(
self
)
-
>
str
:
        
return
self
.
name
    
def
__repr__
(
self
)
-
>
str
:
        
return
"
<
MarkDecorator
{
!
r
}
>
"
.
format
(
self
.
mark
)
    
def
with_args
(
self
*
args
:
object
*
*
kwargs
:
object
)
-
>
"
MarkDecorator
"
:
        
"
"
"
Return
a
MarkDecorator
with
extra
arguments
added
.
        
Unlike
calling
the
MarkDecorator
with_args
(
)
can
be
used
even
        
if
the
sole
argument
is
a
callable
/
class
.
        
:
rtype
:
MarkDecorator
        
"
"
"
        
mark
=
Mark
(
self
.
name
args
kwargs
)
        
return
self
.
__class__
(
self
.
mark
.
combined_with
(
mark
)
)
    
overload
    
def
__call__
(
self
arg
:
_Markable
)
-
>
_Markable
:
        
pass
    
overload
    
def
__call__
(
        
self
*
args
:
object
*
*
kwargs
:
object
    
)
-
>
"
MarkDecorator
"
:
        
pass
    
def
__call__
(
self
*
args
:
object
*
*
kwargs
:
object
)
:
        
"
"
"
Call
the
MarkDecorator
.
"
"
"
        
if
args
and
not
kwargs
:
            
func
=
args
[
0
]
            
is_class
=
inspect
.
isclass
(
func
)
            
if
len
(
args
)
=
=
1
and
(
istestfunc
(
func
)
or
is_class
)
:
                
store_mark
(
func
self
.
mark
)
                
return
func
        
return
self
.
with_args
(
*
args
*
*
kwargs
)
def
get_unpacked_marks
(
obj
)
-
>
List
[
Mark
]
:
    
"
"
"
Obtain
the
unpacked
marks
that
are
stored
on
an
object
.
"
"
"
    
mark_list
=
getattr
(
obj
"
pytestmark
"
[
]
)
    
if
not
isinstance
(
mark_list
list
)
:
        
mark_list
=
[
mark_list
]
    
return
normalize_mark_list
(
mark_list
)
def
normalize_mark_list
(
mark_list
:
Iterable
[
Union
[
Mark
MarkDecorator
]
]
)
-
>
List
[
Mark
]
:
    
"
"
"
Normalize
marker
decorating
helpers
to
mark
objects
.
    
:
type
List
[
Union
[
Mark
Markdecorator
]
]
mark_list
:
    
:
rtype
:
List
[
Mark
]
    
"
"
"
    
extracted
=
[
        
getattr
(
mark
"
mark
"
mark
)
for
mark
in
mark_list
    
]
    
for
mark
in
extracted
:
        
if
not
isinstance
(
mark
Mark
)
:
            
raise
TypeError
(
"
got
{
!
r
}
instead
of
Mark
"
.
format
(
mark
)
)
    
return
[
x
for
x
in
extracted
if
isinstance
(
x
Mark
)
]
def
store_mark
(
obj
mark
:
Mark
)
-
>
None
:
    
"
"
"
Store
a
Mark
on
an
object
.
    
This
is
used
to
implement
the
Mark
declarations
/
decorators
correctly
.
    
"
"
"
    
assert
isinstance
(
mark
Mark
)
mark
    
obj
.
pytestmark
=
get_unpacked_marks
(
obj
)
+
[
mark
]
if
TYPE_CHECKING
:
    
from
_pytest
.
fixtures
import
_Scope
    
class
_SkipMarkDecorator
(
MarkDecorator
)
:
        
overload
        
def
__call__
(
self
arg
:
_Markable
)
-
>
_Markable
:
            
.
.
.
        
overload
        
def
__call__
(
self
reason
:
str
=
.
.
.
)
-
>
"
MarkDecorator
"
:
            
.
.
.
    
class
_SkipifMarkDecorator
(
MarkDecorator
)
:
        
def
__call__
(
            
self
            
condition
:
Union
[
str
bool
]
=
.
.
.
            
*
conditions
:
Union
[
str
bool
]
            
reason
:
str
=
.
.
.
        
)
-
>
MarkDecorator
:
            
.
.
.
    
class
_XfailMarkDecorator
(
MarkDecorator
)
:
        
overload
        
def
__call__
(
self
arg
:
_Markable
)
-
>
_Markable
:
            
.
.
.
        
overload
        
def
__call__
(
            
self
            
condition
:
Union
[
str
bool
]
=
.
.
.
            
*
conditions
:
Union
[
str
bool
]
            
reason
:
str
=
.
.
.
            
run
:
bool
=
.
.
.
            
raises
:
Union
[
                
"
Type
[
BaseException
]
"
Tuple
[
"
Type
[
BaseException
]
"
.
.
.
]
            
]
=
.
.
.
            
strict
:
bool
=
.
.
.
        
)
-
>
MarkDecorator
:
            
.
.
.
    
class
_ParametrizeMarkDecorator
(
MarkDecorator
)
:
        
def
__call__
(
            
self
            
argnames
:
Union
[
str
List
[
str
]
Tuple
[
str
.
.
.
]
]
            
argvalues
:
Iterable
[
Union
[
ParameterSet
Sequence
[
object
]
object
]
]
            
*
            
indirect
:
Union
[
bool
Sequence
[
str
]
]
=
.
.
.
            
ids
:
Optional
[
                
Union
[
                    
Iterable
[
Union
[
None
str
float
int
bool
]
]
                    
Callable
[
[
Any
]
Optional
[
object
]
]
                
]
            
]
=
.
.
.
            
scope
:
Optional
[
_Scope
]
=
.
.
.
        
)
-
>
MarkDecorator
:
            
.
.
.
    
class
_UsefixturesMarkDecorator
(
MarkDecorator
)
:
        
def
__call__
(
            
self
*
fixtures
:
str
        
)
-
>
MarkDecorator
:
            
.
.
.
    
class
_FilterwarningsMarkDecorator
(
MarkDecorator
)
:
        
def
__call__
(
            
self
*
filters
:
str
        
)
-
>
MarkDecorator
:
            
.
.
.
final
class
MarkGenerator
:
    
"
"
"
Factory
for
:
class
:
MarkDecorator
objects
-
exposed
as
    
a
pytest
.
mark
singleton
instance
.
    
Example
:
:
         
import
pytest
         
pytest
.
mark
.
slowtest
         
def
test_function
(
)
:
            
pass
    
applies
a
'
slowtest
'
:
class
:
Mark
on
test_function
.
    
"
"
"
    
_config
=
None
    
_markers
=
set
(
)
    
if
TYPE_CHECKING
:
        
skip
=
_SkipMarkDecorator
(
Mark
(
"
skip
"
(
)
{
}
)
)
        
skipif
=
_SkipifMarkDecorator
(
Mark
(
"
skipif
"
(
)
{
}
)
)
        
xfail
=
_XfailMarkDecorator
(
Mark
(
"
xfail
"
(
)
{
}
)
)
        
parametrize
=
_ParametrizeMarkDecorator
(
Mark
(
"
parametrize
"
(
)
{
}
)
)
        
usefixtures
=
_UsefixturesMarkDecorator
(
Mark
(
"
usefixtures
"
(
)
{
}
)
)
        
filterwarnings
=
_FilterwarningsMarkDecorator
(
Mark
(
"
filterwarnings
"
(
)
{
}
)
)
    
def
__getattr__
(
self
name
:
str
)
-
>
MarkDecorator
:
        
if
name
[
0
]
=
=
"
_
"
:
            
raise
AttributeError
(
"
Marker
name
must
NOT
start
with
underscore
"
)
        
if
self
.
_config
is
not
None
:
            
if
name
not
in
self
.
_markers
:
                
for
line
in
self
.
_config
.
getini
(
"
markers
"
)
:
                    
marker
=
line
.
split
(
"
:
"
)
[
0
]
.
split
(
"
(
"
)
[
0
]
.
strip
(
)
                    
self
.
_markers
.
add
(
marker
)
            
if
name
not
in
self
.
_markers
:
                
if
self
.
_config
.
option
.
strict_markers
:
                    
fail
(
                        
"
{
!
r
}
not
found
in
markers
configuration
option
"
.
format
(
name
)
                        
pytrace
=
False
                    
)
                
if
name
in
[
"
parameterize
"
"
parametrise
"
"
parameterise
"
]
:
                    
__tracebackhide__
=
True
                    
fail
(
"
Unknown
'
{
}
'
mark
did
you
mean
'
parametrize
'
?
"
.
format
(
name
)
)
                
warnings
.
warn
(
                    
"
Unknown
pytest
.
mark
.
%
s
-
is
this
a
typo
?
You
can
register
"
                    
"
custom
marks
to
avoid
this
warning
-
for
details
see
"
                    
"
https
:
/
/
docs
.
pytest
.
org
/
en
/
stable
/
mark
.
html
"
%
name
                    
PytestUnknownMarkWarning
                    
2
                
)
        
return
MarkDecorator
(
Mark
(
name
(
)
{
}
)
)
MARK_GEN
=
MarkGenerator
(
)
final
class
NodeKeywords
(
collections
.
abc
.
MutableMapping
)
:
    
def
__init__
(
self
node
:
"
Node
"
)
-
>
None
:
        
self
.
node
=
node
        
self
.
parent
=
node
.
parent
        
self
.
_markers
=
{
node
.
name
:
True
}
    
def
__getitem__
(
self
key
:
str
)
-
>
Any
:
        
try
:
            
return
self
.
_markers
[
key
]
        
except
KeyError
:
            
if
self
.
parent
is
None
:
                
raise
            
return
self
.
parent
.
keywords
[
key
]
    
def
__setitem__
(
self
key
:
str
value
:
Any
)
-
>
None
:
        
self
.
_markers
[
key
]
=
value
    
def
__delitem__
(
self
key
:
str
)
-
>
None
:
        
raise
ValueError
(
"
cannot
delete
key
in
keywords
dict
"
)
    
def
__iter__
(
self
)
-
>
Iterator
[
str
]
:
        
seen
=
self
.
_seen
(
)
        
return
iter
(
seen
)
    
def
_seen
(
self
)
-
>
Set
[
str
]
:
        
seen
=
set
(
self
.
_markers
)
        
if
self
.
parent
is
not
None
:
            
seen
.
update
(
self
.
parent
.
keywords
)
        
return
seen
    
def
__len__
(
self
)
-
>
int
:
        
return
len
(
self
.
_seen
(
)
)
    
def
__repr__
(
self
)
-
>
str
:
        
return
"
<
NodeKeywords
for
node
{
}
>
"
.
format
(
self
.
node
)
