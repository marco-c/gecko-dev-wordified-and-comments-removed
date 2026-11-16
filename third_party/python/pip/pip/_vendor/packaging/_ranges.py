"
"
"
Private
version
-
range
helpers
used
by
:
mod
:
packaging
.
specifiers
.
"
"
"
from
__future__
import
annotations
import
enum
import
functools
from
typing
import
(
    
TYPE_CHECKING
    
Any
    
Final
)
from
.
version
import
InvalidVersion
Version
if
TYPE_CHECKING
:
    
from
collections
.
abc
import
Callable
Iterable
Iterator
Sequence
    
from
typing
import
Union
    
_BoundaryOrderSuffix
=
tuple
[
int
int
int
Union
[
int
float
]
int
int
]
    
_BoundaryOrderKey
=
tuple
[
int
tuple
[
int
.
.
.
]
_BoundaryOrderSuffix
float
]
__all__
=
[
    
"
FULL_RANGE
"
    
"
bounds_for_spec
"
    
"
coerce_version
"
    
"
filter_by_ranges
"
    
"
intersect_ranges
"
    
"
intersect_specifier_bounds
"
    
"
least_version_above
"
    
"
matches_bounds_only
"
    
"
range_is_empty
"
    
"
ranges_are_prerelease_only
"
    
"
resolve_prereleases
"
    
"
standard_ranges
"
    
"
wildcard_ranges
"
]
MIN_VERSION
:
Final
[
Version
]
=
Version
(
"
0
.
dev0
"
)
MIN_RELEASE
:
Final
[
Version
]
=
Version
(
"
0
"
)
_BOUNDARY_INF
:
Final
[
float
]
=
float
(
"
inf
"
)
class
BoundaryKind
(
enum
.
Enum
)
:
    
"
"
"
Where
a
boundary
marker
sits
in
the
version
ordering
.
"
"
"
    
AFTER_LOCALS
=
enum
.
auto
(
)
    
AFTER_POSTS
=
enum
.
auto
(
)
functools
.
total_ordering
class
BoundaryVersion
:
    
"
"
"
A
point
on
the
version
line
between
two
real
PEP
440
versions
.
    
Relative
to
a
base
version
V
:
:
        
V
<
V
+
local
<
AFTER_LOCALS
(
V
)
<
V
.
post0
<
AFTER_POSTS
(
V
)
    
AFTER_LOCALS
is
the
upper
bound
of
<
=
V
=
=
V
!
=
V
(
no
    
local
)
and
the
lower
bound
of
the
upper
-
side
range
of
!
=
V
.
    
AFTER_POSTS
is
the
lower
bound
of
>
V
(
V
final
or
pre
-
release
)
    
excluding
V
'
s
post
-
releases
per
PEP
440
.
    
"
"
"
    
__slots__
=
(
        
"
_cached_dev
"
        
"
_cached_epoch
"
        
"
_cached_post
"
        
"
_cached_pre
"
        
"
_cached_trimmed_release
"
        
"
kind
"
        
"
version
"
    
)
    
def
__init__
(
self
version
:
Version
kind
:
BoundaryKind
)
-
>
None
:
        
self
.
version
=
version
        
self
.
kind
=
kind
        
self
.
_cached_trimmed_release
=
trim_release
(
version
.
release
)
        
self
.
_cached_epoch
=
version
.
epoch
        
self
.
_cached_pre
=
version
.
pre
        
self
.
_cached_post
=
version
.
post
        
self
.
_cached_dev
=
version
.
dev
    
def
_is_family
(
self
other
:
Version
)
-
>
bool
:
        
"
"
"
Is
other
a
version
that
this
boundary
sorts
above
?
"
"
"
        
if
other
.
epoch
!
=
self
.
_cached_epoch
:
            
return
False
        
other_release
=
other
.
release
        
trimmed_release
=
self
.
_cached_trimmed_release
        
trimmed_length
=
len
(
trimmed_release
)
        
if
len
(
other_release
)
<
trimmed_length
:
            
return
False
        
if
other_release
[
:
trimmed_length
]
!
=
trimmed_release
:
            
return
False
        
for
i
in
range
(
trimmed_length
len
(
other_release
)
)
:
            
if
other_release
[
i
]
!
=
0
:
                
return
False
        
if
other
.
pre
!
=
self
.
_cached_pre
:
            
return
False
        
if
self
.
kind
=
=
BoundaryKind
.
AFTER_LOCALS
:
            
return
other
.
post
=
=
self
.
_cached_post
and
other
.
dev
=
=
self
.
_cached_dev
        
return
other
.
dev
=
=
self
.
_cached_dev
or
other
.
post
is
not
None
    
def
_order_key
(
self
)
-
>
_BoundaryOrderKey
:
        
"
"
"
Sort
key
placing
this
boundary
just
above
the
versions
it
covers
.
        
It
extends
V
'
s
comparison
key
(
epoch
release
suffix
)
with
        
a
trailing
_BOUNDARY_INF
local
component
so
the
key
sorts
after
        
V
and
every
V
+
local
(
whose
keys
carry
a
real
finite
local
        
segment
)
.
suffix
is
the
6
-
int
comparison
suffix
        
(
pre_rank
pre_n
post_rank
post_n
dev_rank
dev_n
)
.
        
For
an
AFTER_POSTS
boundary
the
suffix
is
replaced
with
one
whose
        
post
number
is
_BOUNDARY_INF
so
the
key
also
sorts
after
every
        
V
.
postN
.
An
AFTER_LOCALS
boundary
uses
V
'
s
suffix
unchanged
.
        
"
"
"
        
version_key
=
self
.
version
.
_key
        
suffix
:
_BoundaryOrderSuffix
=
version_key
[
2
]
        
if
self
.
kind
=
=
BoundaryKind
.
AFTER_POSTS
:
            
suffix
=
(
suffix
[
0
]
suffix
[
1
]
1
_BOUNDARY_INF
1
0
)
        
return
version_key
[
0
]
version_key
[
1
]
suffix
_BOUNDARY_INF
    
def
__eq__
(
self
other
:
object
)
-
>
bool
:
        
if
isinstance
(
other
BoundaryVersion
)
:
            
return
self
.
_order_key
(
)
=
=
other
.
_order_key
(
)
        
return
NotImplemented
    
def
__lt__
(
self
other
:
BoundaryVersion
|
Version
)
-
>
bool
:
        
if
isinstance
(
other
BoundaryVersion
)
:
            
return
self
.
_order_key
(
)
<
other
.
_order_key
(
)
        
if
not
(
self
.
version
<
other
)
:
            
return
False
        
return
not
self
.
_is_family
(
other
)
    
def
__gt__
(
self
other
:
BoundaryVersion
|
Version
)
-
>
bool
:
        
if
isinstance
(
other
BoundaryVersion
)
:
            
return
self
.
_order_key
(
)
>
other
.
_order_key
(
)
        
if
self
.
version
>
=
other
:
            
return
True
        
return
self
.
_is_family
(
other
)
    
def
__hash__
(
self
)
-
>
int
:
        
return
hash
(
self
.
_order_key
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
f
"
{
self
.
__class__
.
__name__
}
(
{
self
.
version
!
r
}
{
self
.
kind
.
name
}
)
"
if
TYPE_CHECKING
:
    
_VersionOrBoundary
=
Union
[
Version
BoundaryVersion
None
]
functools
.
total_ordering
class
LowerBound
:
    
"
"
"
Lower
bound
of
a
version
range
.
    
A
version
*
v
*
of
None
means
unbounded
below
(
-
inf
)
.
    
At
equal
versions
[
v
sorts
before
(
v
because
an
inclusive
    
bound
starts
earlier
.
    
"
"
"
    
__slots__
=
(
"
_above
"
"
inclusive
"
"
version
"
)
    
def
__init__
(
self
version
:
_VersionOrBoundary
inclusive
:
bool
)
-
>
None
:
        
self
.
version
=
version
        
self
.
inclusive
=
inclusive
        
if
version
is
None
:
            
self
.
_above
:
Callable
[
[
Version
]
bool
]
|
None
=
None
        
elif
isinstance
(
version
BoundaryVersion
)
:
            
if
version
.
kind
=
=
BoundaryKind
.
AFTER_POSTS
:
                
self
.
_above
=
_make_above_after_posts
(
version
.
version
)
            
else
:
                
self
.
_above
=
_make_above_after_locals
(
version
.
version
)
        
elif
inclusive
:
            
self
.
_above
=
version
.
__le__
        
else
:
            
self
.
_above
=
version
.
__lt__
    
def
__eq__
(
self
other
:
object
)
-
>
bool
:
        
if
not
isinstance
(
other
LowerBound
)
:
            
return
NotImplemented
        
return
self
.
version
=
=
other
.
version
and
self
.
inclusive
=
=
other
.
inclusive
    
def
__lt__
(
self
other
:
LowerBound
)
-
>
bool
:
        
if
not
isinstance
(
other
LowerBound
)
:
            
return
NotImplemented
        
if
self
.
version
is
None
:
            
return
other
.
version
is
not
None
        
if
other
.
version
is
None
:
            
return
False
        
if
self
.
version
!
=
other
.
version
:
            
return
self
.
version
<
other
.
version
        
return
self
.
inclusive
and
not
other
.
inclusive
    
def
__hash__
(
self
)
-
>
int
:
        
return
hash
(
(
self
.
version
self
.
inclusive
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
        
bracket
=
"
[
"
if
self
.
inclusive
else
"
(
"
        
return
f
"
<
{
self
.
__class__
.
__name__
}
{
bracket
}
{
self
.
version
!
r
}
>
"
functools
.
total_ordering
class
UpperBound
:
    
"
"
"
Upper
bound
of
a
version
range
.
    
A
version
*
v
*
of
None
means
unbounded
above
(
+
inf
)
.
    
At
equal
versions
v
)
sorts
before
v
]
because
an
exclusive
    
bound
ends
earlier
.
    
"
"
"
    
__slots__
=
(
"
_below
"
"
inclusive
"
"
version
"
)
    
def
__init__
(
self
version
:
_VersionOrBoundary
inclusive
:
bool
)
-
>
None
:
        
self
.
version
=
version
        
self
.
inclusive
=
inclusive
        
if
version
is
None
:
            
self
.
_below
:
Callable
[
[
Version
]
bool
]
|
None
=
None
        
elif
isinstance
(
version
BoundaryVersion
)
:
            
if
version
.
kind
=
=
BoundaryKind
.
AFTER_LOCALS
:
                
self
.
_below
=
_make_below_after_locals
(
version
.
version
)
            
else
:
                
self
.
_below
=
version
.
__ge__
        
elif
inclusive
:
            
self
.
_below
=
version
.
__ge__
        
else
:
            
self
.
_below
=
version
.
__gt__
    
def
__eq__
(
self
other
:
object
)
-
>
bool
:
        
if
not
isinstance
(
other
UpperBound
)
:
            
return
NotImplemented
        
return
self
.
version
=
=
other
.
version
and
self
.
inclusive
=
=
other
.
inclusive
    
def
__lt__
(
self
other
:
UpperBound
)
-
>
bool
:
        
if
not
isinstance
(
other
UpperBound
)
:
            
return
NotImplemented
        
if
self
.
version
is
None
:
            
return
False
        
if
other
.
version
is
None
:
            
return
True
        
if
self
.
version
!
=
other
.
version
:
            
return
self
.
version
<
other
.
version
        
return
not
self
.
inclusive
and
other
.
inclusive
    
def
__hash__
(
self
)
-
>
int
:
        
return
hash
(
(
self
.
version
self
.
inclusive
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
        
bracket
=
"
]
"
if
self
.
inclusive
else
"
)
"
        
return
f
"
<
{
self
.
__class__
.
__name__
}
{
self
.
version
!
r
}
{
bracket
}
>
"
if
TYPE_CHECKING
:
    
Interval
=
tuple
[
LowerBound
UpperBound
]
NEG_INF
:
Final
[
LowerBound
]
=
LowerBound
(
None
False
)
POS_INF
:
Final
[
UpperBound
]
=
UpperBound
(
None
False
)
FULL_RANGE
:
Final
[
tuple
[
Interval
]
]
=
(
(
NEG_INF
POS_INF
)
)
def
trim_release
(
release
:
tuple
[
int
.
.
.
]
)
-
>
tuple
[
int
.
.
.
]
:
    
"
"
"
Strip
trailing
zeros
from
a
release
tuple
for
normalized
comparison
.
"
"
"
    
end
=
len
(
release
)
    
while
end
>
1
and
release
[
end
-
1
]
=
=
0
:
        
end
-
=
1
    
return
release
if
end
=
=
len
(
release
)
else
release
[
:
end
]
def
_next_prefix_dev0
(
version
:
Version
)
-
>
Version
:
    
"
"
"
Smallest
version
in
the
next
prefix
:
1
.
2
-
>
1
.
3
.
dev0
.
"
"
"
    
release
=
(
*
version
.
release
[
:
-
1
]
version
.
release
[
-
1
]
+
1
)
    
return
Version
.
from_parts
(
epoch
=
version
.
epoch
release
=
release
dev
=
0
)
def
_base_dev0
(
version
:
Version
)
-
>
Version
:
    
"
"
"
The
.
dev0
of
a
version
'
s
base
release
:
1
.
2
-
>
1
.
2
.
dev0
.
"
"
"
    
return
Version
.
from_parts
(
epoch
=
version
.
epoch
release
=
version
.
release
dev
=
0
)
def
coerce_version
(
version
:
Version
|
str
)
-
>
Version
|
None
:
    
if
not
isinstance
(
version
Version
)
:
        
try
:
            
version
=
Version
(
version
)
        
except
InvalidVersion
:
            
return
None
    
return
version
def
_make_above_after_posts
(
version
:
Version
)
-
>
Callable
[
[
Version
]
bool
]
:
    
"
"
"
Predicate
parsed
>
AFTER_POSTS
(
V
)
for
a
lower
bound
.
    
Per
PEP
440
>
V
excludes
V
'
s
post
-
releases
unless
V
is
itself
    
a
post
-
release
.
AFTER_POSTS
sits
above
V
and
every
V
.
postN
(
with
    
or
without
local
)
and
just
below
the
next
release
.
    
"
"
"
    
version_ge
=
version
.
__ge__
    
version_epoch
=
version
.
epoch
    
version_pre
=
version
.
pre
    
version_release_trimmed
=
trim_release
(
version
.
release
)
    
trimmed_length
=
len
(
version_release_trimmed
)
    
def
above
(
parsed
:
Version
)
-
>
bool
:
        
if
version_ge
(
parsed
)
:
            
return
False
        
if
parsed
.
epoch
!
=
version_epoch
:
            
return
True
        
parsed_release
=
parsed
.
release
        
if
len
(
parsed_release
)
<
trimmed_length
:
            
return
True
        
if
parsed_release
[
:
trimmed_length
]
!
=
version_release_trimmed
:
            
return
True
        
for
i
in
range
(
trimmed_length
len
(
parsed_release
)
)
:
            
if
parsed_release
[
i
]
!
=
0
:
                
return
True
        
if
parsed
.
pre
!
=
version_pre
:
            
return
True
        
return
False
    
return
above
def
_make_above_after_locals
(
version
:
Version
)
-
>
Callable
[
[
Version
]
bool
]
:
    
"
"
"
Predicate
parsed
>
AFTER_LOCALS
(
V
)
for
a
lower
bound
.
    
Used
by
the
upper
-
side
range
of
!
=
V
(
when
V
has
no
local
    
segment
)
.
AFTER_LOCALS
sits
above
V
and
every
V
+
local
but
    
just
below
V
.
post0
.
    
"
"
"
    
version_ge
=
version
.
__ge__
    
version_epoch
=
version
.
epoch
    
version_pre
=
version
.
pre
    
version_post
=
version
.
post
    
version_dev
=
version
.
dev
    
version_release_trimmed
=
trim_release
(
version
.
release
)
    
trimmed_length
=
len
(
version_release_trimmed
)
    
def
above
(
parsed
:
Version
)
-
>
bool
:
        
if
version_ge
(
parsed
)
:
            
return
False
        
if
parsed
.
epoch
!
=
version_epoch
:
            
return
True
        
parsed_release
=
parsed
.
release
        
if
len
(
parsed_release
)
<
trimmed_length
:
            
return
True
        
if
parsed_release
[
:
trimmed_length
]
!
=
version_release_trimmed
:
            
return
True
        
for
i
in
range
(
trimmed_length
len
(
parsed_release
)
)
:
            
if
parsed_release
[
i
]
!
=
0
:
                
return
True
        
if
parsed
.
pre
!
=
version_pre
:
            
return
True
        
if
parsed
.
post
!
=
version_post
:
            
return
True
        
return
parsed
.
dev
!
=
version_dev
    
return
above
def
_make_below_after_locals
(
version
:
Version
)
-
>
Callable
[
[
Version
]
bool
]
:
    
"
"
"
Predicate
parsed
<
=
AFTER_LOCALS
(
V
)
for
an
upper
bound
.
    
Used
by
<
=
V
=
=
V
!
=
V
(
no
local
)
.
parsed
is
at
or
    
below
the
boundary
when
it
is
at
or
below
V
cmpkey
-
wise
or
when
    
it
is
in
V
'
s
local
family
.
    
"
"
"
    
version_ge
=
version
.
__ge__
    
version_epoch
=
version
.
epoch
    
version_pre
=
version
.
pre
    
version_post
=
version
.
post
    
version_dev
=
version
.
dev
    
version_release_trimmed
=
trim_release
(
version
.
release
)
    
trimmed_length
=
len
(
version_release_trimmed
)
    
def
below
(
parsed
:
Version
)
-
>
bool
:
        
if
version_ge
(
parsed
)
:
            
return
True
        
if
parsed
.
epoch
!
=
version_epoch
:
            
return
False
        
parsed_release
=
parsed
.
release
        
if
len
(
parsed_release
)
<
trimmed_length
:
            
return
False
        
if
parsed_release
[
:
trimmed_length
]
!
=
version_release_trimmed
:
            
return
False
        
for
i
in
range
(
trimmed_length
len
(
parsed_release
)
)
:
            
if
parsed_release
[
i
]
!
=
0
:
                
return
False
        
if
parsed
.
pre
!
=
version_pre
:
            
return
False
        
if
parsed
.
post
!
=
version_post
:
            
return
False
        
return
parsed
.
dev
=
=
version_dev
    
return
below
def
least_version_above
(
boundary
:
BoundaryVersion
)
-
>
Version
|
None
:
    
"
"
"
Smallest
real
version
strictly
above
*
boundary
*
or
None
if
none
exists
.
"
"
"
    
base
=
boundary
.
version
    
if
boundary
.
kind
=
=
BoundaryKind
.
AFTER_LOCALS
:
        
if
base
.
dev
is
not
None
:
            
return
base
.
__replace__
(
dev
=
base
.
dev
+
1
local
=
None
)
        
next_post
=
(
base
.
post
+
1
)
if
base
.
post
is
not
None
else
0
        
return
base
.
__replace__
(
post
=
next_post
dev
=
0
local
=
None
)
    
if
base
.
pre
is
not
None
:
        
kind
number
=
base
.
pre
        
return
base
.
__replace__
(
pre
=
(
kind
number
+
1
)
post
=
None
dev
=
0
local
=
None
)
    
return
None
def
range_is_empty
(
lower
:
LowerBound
upper
:
UpperBound
)
-
>
bool
:
    
"
"
"
True
when
the
range
defined
by
*
lower
*
and
*
upper
*
contains
no
versions
.
    
A
boundary
lower
sits
just
below
the
next
real
version
so
an
ordered
pair
    
is
still
empty
when
the
upper
excludes
that
least
successor
:
    
(
AFTER_POSTS
(
1
.
0a1
)
1
.
0a2
.
dev0
)
holds
no
version
.
    
"
"
"
    
if
upper
.
version
is
None
:
        
return
False
    
if
lower
.
version
is
None
:
        
return
(
            
not
upper
.
inclusive
            
and
isinstance
(
upper
.
version
Version
)
            
and
upper
.
version
<
=
MIN_VERSION
        
)
    
if
isinstance
(
lower
.
version
BoundaryVersion
)
:
        
successor
=
least_version_above
(
lower
.
version
)
        
if
successor
is
not
None
:
            
if
upper
.
version
=
=
successor
:
                
return
not
upper
.
inclusive
            
return
upper
.
version
<
successor
    
if
lower
.
version
=
=
upper
.
version
:
        
return
not
(
lower
.
inclusive
and
upper
.
inclusive
)
    
return
lower
.
version
>
upper
.
version
def
intersect_ranges
(
    
left
:
Sequence
[
Interval
]
    
right
:
Sequence
[
Interval
]
)
-
>
list
[
Interval
]
:
    
"
"
"
Intersect
two
sorted
non
-
overlapping
range
lists
(
two
-
pointer
merge
)
.
"
"
"
    
result
:
list
[
Interval
]
=
[
]
    
left_index
=
right_index
=
0
    
while
left_index
<
len
(
left
)
and
right_index
<
len
(
right
)
:
        
left_lower
left_upper
=
left
[
left_index
]
        
right_lower
right_upper
=
right
[
right_index
]
        
lower
=
max
(
left_lower
right_lower
)
        
upper
=
min
(
left_upper
right_upper
)
        
if
not
range_is_empty
(
lower
upper
)
:
            
result
.
append
(
(
lower
upper
)
)
        
if
left_upper
<
right_upper
:
            
left_index
+
=
1
        
else
:
            
right_index
+
=
1
    
return
result
def
filter_by_ranges
(
    
ranges
:
Sequence
[
Interval
]
    
iterable
:
Iterable
[
Any
]
    
key
:
Callable
[
[
Any
]
Version
|
str
]
|
None
    
prereleases
:
bool
|
None
    
region
:
Sequence
[
Interval
]
=
(
)
)
-
>
Iterator
[
Any
]
:
    
"
"
"
Filter
*
iterable
*
against
precomputed
version
*
ranges
*
.
    
With
prereleases
=
None
the
PEP
440
default
applies
:
pre
-
releases
are
    
excluded
unless
no
final
matches
in
which
case
buffered
pre
-
releases
come
    
out
at
the
end
.
A
pre
-
release
inside
the
opt
-
in
region
is
the
exception
:
    
it
is
force
-
admitted
in
place
as
prereleases
=
True
would
yield
it
.
A
    
force
-
admitted
pre
-
release
is
not
a
final
so
it
never
suppresses
the
buffer
.
    
"
"
"
    
if
prereleases
is
None
:
        
prerelease_buffer
:
list
[
Any
]
=
[
]
        
found_final
=
False
        
if
len
(
ranges
)
=
=
1
:
            
lower
upper
=
ranges
[
0
]
            
above
=
lower
.
_above
            
below
=
upper
.
_below
            
for
item
in
iterable
:
                
parsed
=
coerce_version
(
item
if
key
is
None
else
key
(
item
)
)
                
if
parsed
is
None
:
                    
continue
                
if
above
is
not
None
and
not
above
(
parsed
)
:
                    
continue
                
if
below
is
not
None
and
not
below
(
parsed
)
:
                    
continue
                
if
not
parsed
.
is_prerelease
:
                    
found_final
=
True
                    
yield
item
                
elif
region
and
matches_bounds_only
(
region
parsed
)
:
                    
yield
item
                
elif
not
found_final
:
                    
prerelease_buffer
.
append
(
item
)
            
if
not
found_final
:
                
yield
from
prerelease_buffer
            
return
        
for
item
in
iterable
:
            
parsed
=
coerce_version
(
item
if
key
is
None
else
key
(
item
)
)
            
if
parsed
is
None
:
                
continue
            
for
lower
upper
in
ranges
:
                
above
=
lower
.
_above
                
if
above
is
not
None
and
not
above
(
parsed
)
:
                    
break
                
below
=
upper
.
_below
                
if
below
is
None
or
below
(
parsed
)
:
                    
if
not
parsed
.
is_prerelease
:
                        
found_final
=
True
                        
yield
item
                    
elif
region
and
matches_bounds_only
(
region
parsed
)
:
                        
yield
item
                    
elif
not
found_final
:
                        
prerelease_buffer
.
append
(
item
)
                    
break
        
if
not
found_final
:
            
yield
from
prerelease_buffer
        
return
    
exclude_prereleases
=
prereleases
is
False
    
if
len
(
ranges
)
=
=
1
:
        
lower
upper
=
ranges
[
0
]
        
above
=
lower
.
_above
        
below
=
upper
.
_below
        
for
item
in
iterable
:
            
parsed
=
coerce_version
(
item
if
key
is
None
else
key
(
item
)
)
            
if
parsed
is
None
:
                
continue
            
if
exclude_prereleases
and
parsed
.
is_prerelease
:
                
continue
            
if
above
is
not
None
and
not
above
(
parsed
)
:
                
continue
            
if
below
is
None
or
below
(
parsed
)
:
                
yield
item
        
return
    
for
item
in
iterable
:
        
parsed
=
coerce_version
(
item
if
key
is
None
else
key
(
item
)
)
        
if
parsed
is
None
:
            
continue
        
if
exclude_prereleases
and
parsed
.
is_prerelease
:
            
continue
        
for
lower
upper
in
ranges
:
            
above
=
lower
.
_above
            
if
above
is
not
None
and
not
above
(
parsed
)
:
                
break
            
below
=
upper
.
_below
            
if
below
is
None
or
below
(
parsed
)
:
                
yield
item
                
break
def
_nearest_release_above_prerelease
(
version
:
Version
)
-
>
Version
:
    
"
"
"
Smallest
non
-
pre
-
release
at
or
above
a
pre
-
release
*
version
*
.
"
"
"
    
if
version
.
pre
is
not
None
:
        
return
version
.
__replace__
(
pre
=
None
post
=
None
dev
=
None
local
=
None
)
    
return
version
.
__replace__
(
dev
=
None
local
=
None
)
def
_lowest_release_at_or_above
(
value
:
Version
|
BoundaryVersion
|
None
)
-
>
Version
:
    
"
"
"
Smallest
non
-
pre
-
release
version
at
or
above
*
value
*
.
    
None
is
the
-
inf
floor
whose
nearest
non
-
pre
-
release
is
    
:
data
:
MIN_RELEASE
.
    
"
"
"
    
if
value
is
None
:
        
return
MIN_RELEASE
    
if
isinstance
(
value
BoundaryVersion
)
:
        
inner_version
=
value
.
version
        
if
inner_version
.
is_prerelease
:
            
return
_nearest_release_above_prerelease
(
inner_version
)
        
next_post
=
(
inner_version
.
post
+
1
)
if
inner_version
.
post
is
not
None
else
0
        
return
inner_version
.
__replace__
(
post
=
next_post
local
=
None
)
    
if
not
value
.
is_prerelease
:
        
return
value
    
return
_nearest_release_above_prerelease
(
value
)
def
ranges_are_prerelease_only
(
ranges
:
Sequence
[
Interval
]
)
-
>
bool
:
    
"
"
"
True
when
every
range
in
*
ranges
*
contains
only
pre
-
releases
.
    
Used
to
detect
unsatisfiable
specifier
sets
when
prereleases
=
False
:
    
if
every
range
is
pre
-
release
-
only
every
contained
version
is
excluded
.
    
"
"
"
    
for
lower
upper
in
ranges
:
        
nearest
=
_lowest_release_at_or_above
(
lower
.
version
)
        
if
upper
.
version
is
None
or
nearest
<
upper
.
version
:
            
return
False
        
if
nearest
=
=
upper
.
version
and
upper
.
inclusive
:
            
return
False
    
return
True
def
wildcard_ranges
(
op
:
str
base
:
Version
)
-
>
list
[
Interval
]
:
    
"
"
"
Ranges
for
=
=
V
.
*
and
!
=
V
.
*
.
    
=
=
1
.
2
.
*
-
>
[
1
.
2
.
dev0
1
.
3
.
dev0
)
;
!
=
1
.
2
.
*
-
>
complement
.
    
"
"
"
    
lower
=
_base_dev0
(
base
)
    
upper
=
_next_prefix_dev0
(
base
)
    
if
op
=
=
"
=
=
"
:
        
return
[
(
LowerBound
(
lower
True
)
UpperBound
(
upper
False
)
)
]
    
return
[
        
(
NEG_INF
UpperBound
(
lower
False
)
)
        
(
LowerBound
(
upper
True
)
POS_INF
)
    
]
def
standard_ranges
(
op
:
str
version
:
Version
has_local
:
bool
)
-
>
list
[
Interval
]
:
    
"
"
"
Ranges
for
the
standard
PEP
440
operators
(
no
wildcard
no
=
=
=
)
.
    
*
has_local
*
indicates
whether
the
spec
string
included
a
+
local
    
segment
;
relevant
only
for
=
=
/
!
=
to
decide
whether
the
    
upper
bound
includes
V
'
s
local
family
.
    
"
"
"
    
if
op
=
=
"
>
=
"
:
        
return
[
(
LowerBound
(
version
True
)
POS_INF
)
]
    
if
op
=
=
"
<
=
"
:
        
return
[
            
(
                
NEG_INF
                
UpperBound
(
BoundaryVersion
(
version
BoundaryKind
.
AFTER_LOCALS
)
True
)
            
)
        
]
    
if
op
=
=
"
>
"
:
        
if
version
.
dev
is
not
None
:
            
lower_bound
=
version
.
__replace__
(
dev
=
version
.
dev
+
1
local
=
None
)
            
return
[
(
LowerBound
(
lower_bound
True
)
POS_INF
)
]
        
if
version
.
post
is
not
None
:
            
lower_bound
=
version
.
__replace__
(
post
=
version
.
post
+
1
dev
=
0
local
=
None
)
            
return
[
(
LowerBound
(
lower_bound
True
)
POS_INF
)
]
        
return
[
            
(
                
LowerBound
(
BoundaryVersion
(
version
BoundaryKind
.
AFTER_POSTS
)
False
)
                
POS_INF
            
)
        
]
    
if
op
=
=
"
<
"
:
        
bound
=
(
            
version
if
version
.
is_prerelease
else
version
.
__replace__
(
dev
=
0
local
=
None
)
        
)
        
if
bound
<
=
MIN_VERSION
:
            
return
[
]
        
return
[
(
NEG_INF
UpperBound
(
bound
False
)
)
]
    
after_locals
=
BoundaryVersion
(
version
BoundaryKind
.
AFTER_LOCALS
)
    
upper
=
version
if
has_local
else
after_locals
    
if
op
=
=
"
=
=
"
:
        
return
[
(
LowerBound
(
version
True
)
UpperBound
(
upper
True
)
)
]
    
if
op
=
=
"
!
=
"
:
        
return
[
            
(
NEG_INF
UpperBound
(
version
False
)
)
            
(
LowerBound
(
upper
False
)
POS_INF
)
        
]
    
if
op
=
=
"
~
=
"
:
        
prefix
=
version
.
__replace__
(
release
=
version
.
release
[
:
-
1
]
)
        
return
[
            
(
LowerBound
(
version
True
)
UpperBound
(
_next_prefix_dev0
(
prefix
)
False
)
)
        
]
    
raise
ValueError
(
f
"
Unknown
operator
:
{
op
!
r
}
"
)
def
bounds_for_spec
(
op
:
str
version_str
:
str
version
:
Version
)
-
>
list
[
Interval
]
:
    
"
"
"
Ranges
for
one
specifier
'
s
(
op
version_str
)
.
    
Dispatches
between
the
wildcard
and
standard
builders
.
version
is
the
    
parsed
version_str
(
its
base
without
the
trailing
.
*
for
    
wildcards
)
.
=
=
=
is
not
handled
here
;
its
match
is
a
literal
string
    
compared
in
:
mod
:
packaging
.
specifiers
.
    
"
"
"
    
if
version_str
.
endswith
(
"
.
*
"
)
:
        
return
wildcard_ranges
(
op
version
)
    
return
standard_ranges
(
op
version
"
+
"
in
version_str
)
def
intersect_specifier_bounds
(
    
per_specifier_ranges
:
Iterable
[
Sequence
[
Interval
]
]
)
-
>
Sequence
[
Interval
]
:
    
"
"
"
Intersect
each
specifier
'
s
ranges
into
a
single
sequence
.
    
Short
-
circuits
once
the
running
intersection
is
empty
since
no
later
    
specifier
can
revive
it
.
Callers
must
pass
at
least
one
specifier
.
    
"
"
"
    
result
:
Sequence
[
Interval
]
|
None
=
None
    
for
sub
in
per_specifier_ranges
:
        
if
result
is
None
:
            
result
=
sub
        
else
:
            
result
=
intersect_ranges
(
result
sub
)
            
if
not
result
:
                
break
    
if
result
is
None
:
        
raise
RuntimeError
(
"
intersect_specifier_bounds
called
with
no
specifiers
"
)
    
return
result
def
matches_bounds_only
(
ranges
:
Sequence
[
Interval
]
version
:
Version
)
-
>
bool
:
    
"
"
"
Whether
version
falls
within
any
of
ranges
.
    
The
pure
bounds
membership
test
for
a
single
already
-
parsed
version
with
    
no
pre
-
release
policy
applied
.
ranges
are
sorted
and
non
-
overlapping
    
so
a
version
below
one
range
'
s
lower
bound
is
below
every
later
range
too
.
    
"
"
"
    
for
lower
upper
in
ranges
:
        
above
=
lower
.
_above
        
if
above
is
not
None
and
not
above
(
version
)
:
            
return
False
        
below
=
upper
.
_below
        
if
below
is
None
or
below
(
version
)
:
            
return
True
    
return
False
def
resolve_prereleases
(
    
configured
:
bool
|
None
autodetected
:
bool
|
None
)
-
>
bool
|
None
:
    
"
"
"
Resolve
a
specifier
'
s
effective
default
pre
-
release
policy
.
    
An
explicit
configured
value
wins
;
otherwise
an
autodetected
True
    
propagates
and
anything
else
falls
back
to
the
PEP
440
default
(
None
)
.
    
"
"
"
    
if
configured
is
not
None
:
        
return
configured
    
if
autodetected
:
        
return
True
    
return
None
