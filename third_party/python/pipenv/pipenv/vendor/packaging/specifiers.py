from
__future__
import
absolute_import
division
print_function
import
abc
import
functools
import
itertools
import
re
from
.
_compat
import
string_types
with_metaclass
from
.
_typing
import
MYPY_CHECK_RUNNING
from
.
version
import
Version
LegacyVersion
parse
if
MYPY_CHECK_RUNNING
:
    
from
typing
import
(
        
List
        
Dict
        
Union
        
Iterable
        
Iterator
        
Optional
        
Callable
        
Tuple
        
FrozenSet
    
)
    
ParsedVersion
=
Union
[
Version
LegacyVersion
]
    
UnparsedVersion
=
Union
[
Version
LegacyVersion
str
]
    
CallableOperator
=
Callable
[
[
ParsedVersion
str
]
bool
]
class
InvalidSpecifier
(
ValueError
)
:
    
"
"
"
    
An
invalid
specifier
was
found
users
should
refer
to
PEP
440
.
    
"
"
"
class
BaseSpecifier
(
with_metaclass
(
abc
.
ABCMeta
object
)
)
:
    
abc
.
abstractmethod
    
def
__str__
(
self
)
:
        
"
"
"
        
Returns
the
str
representation
of
this
Specifier
like
object
.
This
        
should
be
representative
of
the
Specifier
itself
.
        
"
"
"
    
abc
.
abstractmethod
    
def
__hash__
(
self
)
:
        
"
"
"
        
Returns
a
hash
value
for
this
Specifier
like
object
.
        
"
"
"
    
abc
.
abstractmethod
    
def
__eq__
(
self
other
)
:
        
"
"
"
        
Returns
a
boolean
representing
whether
or
not
the
two
Specifier
like
        
objects
are
equal
.
        
"
"
"
    
abc
.
abstractmethod
    
def
__ne__
(
self
other
)
:
        
"
"
"
        
Returns
a
boolean
representing
whether
or
not
the
two
Specifier
like
        
objects
are
not
equal
.
        
"
"
"
    
abc
.
abstractproperty
    
def
prereleases
(
self
)
:
        
"
"
"
        
Returns
whether
or
not
pre
-
releases
as
a
whole
are
allowed
by
this
        
specifier
.
        
"
"
"
    
prereleases
.
setter
    
def
prereleases
(
self
value
)
:
        
"
"
"
        
Sets
whether
or
not
pre
-
releases
as
a
whole
are
allowed
by
this
        
specifier
.
        
"
"
"
    
abc
.
abstractmethod
    
def
contains
(
self
item
prereleases
=
None
)
:
        
"
"
"
        
Determines
if
the
given
item
is
contained
within
this
specifier
.
        
"
"
"
    
abc
.
abstractmethod
    
def
filter
(
self
iterable
prereleases
=
None
)
:
        
"
"
"
        
Takes
an
iterable
of
items
and
filters
them
so
that
only
items
which
        
are
contained
within
this
specifier
are
allowed
in
it
.
        
"
"
"
class
_IndividualSpecifier
(
BaseSpecifier
)
:
    
_operators
=
{
}
    
def
__init__
(
self
spec
=
"
"
prereleases
=
None
)
:
        
match
=
self
.
_regex
.
search
(
spec
)
        
if
not
match
:
            
raise
InvalidSpecifier
(
"
Invalid
specifier
:
'
{
0
}
'
"
.
format
(
spec
)
)
        
self
.
_spec
=
(
            
match
.
group
(
"
operator
"
)
.
strip
(
)
            
match
.
group
(
"
version
"
)
.
strip
(
)
        
)
        
self
.
_prereleases
=
prereleases
    
def
__repr__
(
self
)
:
        
pre
=
(
            
"
prereleases
=
{
0
!
r
}
"
.
format
(
self
.
prereleases
)
            
if
self
.
_prereleases
is
not
None
            
else
"
"
        
)
        
return
"
<
{
0
}
(
{
1
!
r
}
{
2
}
)
>
"
.
format
(
self
.
__class__
.
__name__
str
(
self
)
pre
)
    
def
__str__
(
self
)
:
        
return
"
{
0
}
{
1
}
"
.
format
(
*
self
.
_spec
)
    
def
__hash__
(
self
)
:
        
return
hash
(
self
.
_spec
)
    
def
__eq__
(
self
other
)
:
        
if
isinstance
(
other
string_types
)
:
            
try
:
                
other
=
self
.
__class__
(
str
(
other
)
)
            
except
InvalidSpecifier
:
                
return
NotImplemented
        
elif
not
isinstance
(
other
self
.
__class__
)
:
            
return
NotImplemented
        
return
self
.
_spec
=
=
other
.
_spec
    
def
__ne__
(
self
other
)
:
        
if
isinstance
(
other
string_types
)
:
            
try
:
                
other
=
self
.
__class__
(
str
(
other
)
)
            
except
InvalidSpecifier
:
                
return
NotImplemented
        
elif
not
isinstance
(
other
self
.
__class__
)
:
            
return
NotImplemented
        
return
self
.
_spec
!
=
other
.
_spec
    
def
_get_operator
(
self
op
)
:
        
operator_callable
=
getattr
(
            
self
"
_compare_
{
0
}
"
.
format
(
self
.
_operators
[
op
]
)
        
)
        
return
operator_callable
    
def
_coerce_version
(
self
version
)
:
        
if
not
isinstance
(
version
(
LegacyVersion
Version
)
)
:
            
version
=
parse
(
version
)
        
return
version
    
property
    
def
operator
(
self
)
:
        
return
self
.
_spec
[
0
]
    
property
    
def
version
(
self
)
:
        
return
self
.
_spec
[
1
]
    
property
    
def
prereleases
(
self
)
:
        
return
self
.
_prereleases
    
prereleases
.
setter
    
def
prereleases
(
self
value
)
:
        
self
.
_prereleases
=
value
    
def
__contains__
(
self
item
)
:
        
return
self
.
contains
(
item
)
    
def
contains
(
self
item
prereleases
=
None
)
:
        
if
prereleases
is
None
:
            
prereleases
=
self
.
prereleases
        
normalized_item
=
self
.
_coerce_version
(
item
)
        
if
normalized_item
.
is_prerelease
and
not
prereleases
:
            
return
False
        
operator_callable
=
self
.
_get_operator
(
self
.
operator
)
        
return
operator_callable
(
normalized_item
self
.
version
)
    
def
filter
(
self
iterable
prereleases
=
None
)
:
        
yielded
=
False
        
found_prereleases
=
[
]
        
kw
=
{
"
prereleases
"
:
prereleases
if
prereleases
is
not
None
else
True
}
        
for
version
in
iterable
:
            
parsed_version
=
self
.
_coerce_version
(
version
)
            
if
self
.
contains
(
parsed_version
*
*
kw
)
:
                
if
parsed_version
.
is_prerelease
and
not
(
                    
prereleases
or
self
.
prereleases
                
)
:
                    
found_prereleases
.
append
(
version
)
                
else
:
                    
yielded
=
True
                    
yield
version
        
if
not
yielded
and
found_prereleases
:
            
for
version
in
found_prereleases
:
                
yield
version
class
LegacySpecifier
(
_IndividualSpecifier
)
:
    
_regex_str
=
r
"
"
"
        
(
?
P
<
operator
>
(
=
=
|
!
=
|
<
=
|
>
=
|
<
|
>
)
)
        
\
s
*
        
(
?
P
<
version
>
            
[
^
;
\
s
)
]
*
#
Since
this
is
a
"
legacy
"
specifier
and
the
version
                      
#
string
can
be
just
about
anything
we
match
everything
                      
#
except
for
whitespace
a
semi
-
colon
for
marker
support
                      
#
a
closing
paren
since
versions
can
be
enclosed
in
                      
#
them
and
a
comma
since
it
'
s
a
version
separator
.
        
)
        
"
"
"
    
_regex
=
re
.
compile
(
r
"
^
\
s
*
"
+
_regex_str
+
r
"
\
s
*
"
re
.
VERBOSE
|
re
.
IGNORECASE
)
    
_operators
=
{
        
"
=
=
"
:
"
equal
"
        
"
!
=
"
:
"
not_equal
"
        
"
<
=
"
:
"
less_than_equal
"
        
"
>
=
"
:
"
greater_than_equal
"
        
"
<
"
:
"
less_than
"
        
"
>
"
:
"
greater_than
"
    
}
    
def
_coerce_version
(
self
version
)
:
        
if
not
isinstance
(
version
LegacyVersion
)
:
            
version
=
LegacyVersion
(
str
(
version
)
)
        
return
version
    
def
_compare_equal
(
self
prospective
spec
)
:
        
return
prospective
=
=
self
.
_coerce_version
(
spec
)
    
def
_compare_not_equal
(
self
prospective
spec
)
:
        
return
prospective
!
=
self
.
_coerce_version
(
spec
)
    
def
_compare_less_than_equal
(
self
prospective
spec
)
:
        
return
prospective
<
=
self
.
_coerce_version
(
spec
)
    
def
_compare_greater_than_equal
(
self
prospective
spec
)
:
        
return
prospective
>
=
self
.
_coerce_version
(
spec
)
    
def
_compare_less_than
(
self
prospective
spec
)
:
        
return
prospective
<
self
.
_coerce_version
(
spec
)
    
def
_compare_greater_than
(
self
prospective
spec
)
:
        
return
prospective
>
self
.
_coerce_version
(
spec
)
def
_require_version_compare
(
    
fn
)
:
    
functools
.
wraps
(
fn
)
    
def
wrapped
(
self
prospective
spec
)
:
        
if
not
isinstance
(
prospective
Version
)
:
            
return
False
        
return
fn
(
self
prospective
spec
)
    
return
wrapped
class
Specifier
(
_IndividualSpecifier
)
:
    
_regex_str
=
r
"
"
"
        
(
?
P
<
operator
>
(
~
=
|
=
=
|
!
=
|
<
=
|
>
=
|
<
|
>
|
=
=
=
)
)
        
(
?
P
<
version
>
            
(
?
:
                
#
The
identity
operators
allow
for
an
escape
hatch
that
will
                
#
do
an
exact
string
match
of
the
version
you
wish
to
install
.
                
#
This
will
not
be
parsed
by
PEP
440
and
we
cannot
determine
                
#
any
semantic
meaning
from
it
.
This
operator
is
discouraged
                
#
but
included
entirely
as
an
escape
hatch
.
                
(
?
<
=
=
=
=
)
#
Only
match
for
the
identity
operator
                
\
s
*
                
[
^
\
s
]
*
#
We
just
match
everything
except
for
whitespace
                          
#
since
we
are
only
testing
for
strict
identity
.
            
)
            
|
            
(
?
:
                
#
The
(
non
)
equality
operators
allow
for
wild
card
and
local
                
#
versions
to
be
specified
so
we
have
to
define
these
two
                
#
operators
separately
to
enable
that
.
                
(
?
<
=
=
=
|
!
=
)
#
Only
match
for
equals
and
not
equals
                
\
s
*
                
v
?
                
(
?
:
[
0
-
9
]
+
!
)
?
#
epoch
                
[
0
-
9
]
+
(
?
:
\
.
[
0
-
9
]
+
)
*
#
release
                
(
?
:
#
pre
release
                    
[
-
_
\
.
]
?
                    
(
a
|
b
|
c
|
rc
|
alpha
|
beta
|
pre
|
preview
)
                    
[
-
_
\
.
]
?
                    
[
0
-
9
]
*
                
)
?
                
(
?
:
#
post
release
                    
(
?
:
-
[
0
-
9
]
+
)
|
(
?
:
[
-
_
\
.
]
?
(
post
|
rev
|
r
)
[
-
_
\
.
]
?
[
0
-
9
]
*
)
                
)
?
                
#
You
cannot
use
a
wild
card
and
a
dev
or
local
version
                
#
together
so
group
them
with
a
|
and
make
them
optional
.
                
(
?
:
                    
(
?
:
[
-
_
\
.
]
?
dev
[
-
_
\
.
]
?
[
0
-
9
]
*
)
?
#
dev
release
                    
(
?
:
\
+
[
a
-
z0
-
9
]
+
(
?
:
[
-
_
\
.
]
[
a
-
z0
-
9
]
+
)
*
)
?
#
local
                    
|
                    
\
.
\
*
#
Wild
card
syntax
of
.
*
                
)
?
            
)
            
|
            
(
?
:
                
#
The
compatible
operator
requires
at
least
two
digits
in
the
                
#
release
segment
.
                
(
?
<
=
~
=
)
#
Only
match
for
the
compatible
operator
                
\
s
*
                
v
?
                
(
?
:
[
0
-
9
]
+
!
)
?
#
epoch
                
[
0
-
9
]
+
(
?
:
\
.
[
0
-
9
]
+
)
+
#
release
(
We
have
a
+
instead
of
a
*
)
                
(
?
:
#
pre
release
                    
[
-
_
\
.
]
?
                    
(
a
|
b
|
c
|
rc
|
alpha
|
beta
|
pre
|
preview
)
                    
[
-
_
\
.
]
?
                    
[
0
-
9
]
*
                
)
?
                
(
?
:
#
post
release
                    
(
?
:
-
[
0
-
9
]
+
)
|
(
?
:
[
-
_
\
.
]
?
(
post
|
rev
|
r
)
[
-
_
\
.
]
?
[
0
-
9
]
*
)
                
)
?
                
(
?
:
[
-
_
\
.
]
?
dev
[
-
_
\
.
]
?
[
0
-
9
]
*
)
?
#
dev
release
            
)
            
|
            
(
?
:
                
#
All
other
operators
only
allow
a
sub
set
of
what
the
                
#
(
non
)
equality
operators
do
.
Specifically
they
do
not
allow
                
#
local
versions
to
be
specified
nor
do
they
allow
the
prefix
                
#
matching
wild
cards
.
                
(
?
<
!
=
=
|
!
=
|
~
=
)
#
We
have
special
cases
for
these
                                      
#
operators
so
we
want
to
make
sure
they
                                      
#
don
'
t
match
here
.
                
\
s
*
                
v
?
                
(
?
:
[
0
-
9
]
+
!
)
?
#
epoch
                
[
0
-
9
]
+
(
?
:
\
.
[
0
-
9
]
+
)
*
#
release
                
(
?
:
#
pre
release
                    
[
-
_
\
.
]
?
                    
(
a
|
b
|
c
|
rc
|
alpha
|
beta
|
pre
|
preview
)
                    
[
-
_
\
.
]
?
                    
[
0
-
9
]
*
                
)
?
                
(
?
:
#
post
release
                    
(
?
:
-
[
0
-
9
]
+
)
|
(
?
:
[
-
_
\
.
]
?
(
post
|
rev
|
r
)
[
-
_
\
.
]
?
[
0
-
9
]
*
)
                
)
?
                
(
?
:
[
-
_
\
.
]
?
dev
[
-
_
\
.
]
?
[
0
-
9
]
*
)
?
#
dev
release
            
)
        
)
        
"
"
"
    
_regex
=
re
.
compile
(
r
"
^
\
s
*
"
+
_regex_str
+
r
"
\
s
*
"
re
.
VERBOSE
|
re
.
IGNORECASE
)
    
_operators
=
{
        
"
~
=
"
:
"
compatible
"
        
"
=
=
"
:
"
equal
"
        
"
!
=
"
:
"
not_equal
"
        
"
<
=
"
:
"
less_than_equal
"
        
"
>
=
"
:
"
greater_than_equal
"
        
"
<
"
:
"
less_than
"
        
"
>
"
:
"
greater_than
"
        
"
=
=
=
"
:
"
arbitrary
"
    
}
    
_require_version_compare
    
def
_compare_compatible
(
self
prospective
spec
)
:
        
prefix
=
"
.
"
.
join
(
            
list
(
                
itertools
.
takewhile
(
                    
lambda
x
:
(
not
x
.
startswith
(
"
post
"
)
and
not
x
.
startswith
(
"
dev
"
)
)
                    
_version_split
(
spec
)
                
)
            
)
[
:
-
1
]
        
)
        
prefix
+
=
"
.
*
"
        
return
self
.
_get_operator
(
"
>
=
"
)
(
prospective
spec
)
and
self
.
_get_operator
(
"
=
=
"
)
(
            
prospective
prefix
        
)
    
_require_version_compare
    
def
_compare_equal
(
self
prospective
spec
)
:
        
if
spec
.
endswith
(
"
.
*
"
)
:
            
prospective
=
Version
(
prospective
.
public
)
            
split_spec
=
_version_split
(
spec
[
:
-
2
]
)
            
split_prospective
=
_version_split
(
str
(
prospective
)
)
            
shortened_prospective
=
split_prospective
[
:
len
(
split_spec
)
]
            
padded_spec
padded_prospective
=
_pad_version
(
                
split_spec
shortened_prospective
            
)
            
return
padded_prospective
=
=
padded_spec
        
else
:
            
spec_version
=
Version
(
spec
)
            
if
not
spec_version
.
local
:
                
prospective
=
Version
(
prospective
.
public
)
            
return
prospective
=
=
spec_version
    
_require_version_compare
    
def
_compare_not_equal
(
self
prospective
spec
)
:
        
return
not
self
.
_compare_equal
(
prospective
spec
)
    
_require_version_compare
    
def
_compare_less_than_equal
(
self
prospective
spec
)
:
        
return
prospective
<
=
Version
(
spec
)
    
_require_version_compare
    
def
_compare_greater_than_equal
(
self
prospective
spec
)
:
        
return
prospective
>
=
Version
(
spec
)
    
_require_version_compare
    
def
_compare_less_than
(
self
prospective
spec_str
)
:
        
spec
=
Version
(
spec_str
)
        
if
not
prospective
<
spec
:
            
return
False
        
if
not
spec
.
is_prerelease
and
prospective
.
is_prerelease
:
            
if
Version
(
prospective
.
base_version
)
=
=
Version
(
spec
.
base_version
)
:
                
return
False
        
return
True
    
_require_version_compare
    
def
_compare_greater_than
(
self
prospective
spec_str
)
:
        
spec
=
Version
(
spec_str
)
        
if
not
prospective
>
spec
:
            
return
False
        
if
not
spec
.
is_postrelease
and
prospective
.
is_postrelease
:
            
if
Version
(
prospective
.
base_version
)
=
=
Version
(
spec
.
base_version
)
:
                
return
False
        
if
prospective
.
local
is
not
None
:
            
if
Version
(
prospective
.
base_version
)
=
=
Version
(
spec
.
base_version
)
:
                
return
False
        
return
True
    
def
_compare_arbitrary
(
self
prospective
spec
)
:
        
return
str
(
prospective
)
.
lower
(
)
=
=
str
(
spec
)
.
lower
(
)
    
property
    
def
prereleases
(
self
)
:
        
if
self
.
_prereleases
is
not
None
:
            
return
self
.
_prereleases
        
operator
version
=
self
.
_spec
        
if
operator
in
[
"
=
=
"
"
>
=
"
"
<
=
"
"
~
=
"
"
=
=
=
"
]
:
            
if
operator
=
=
"
=
=
"
and
version
.
endswith
(
"
.
*
"
)
:
                
version
=
version
[
:
-
2
]
            
if
parse
(
version
)
.
is_prerelease
:
                
return
True
        
return
False
    
prereleases
.
setter
    
def
prereleases
(
self
value
)
:
        
self
.
_prereleases
=
value
_prefix_regex
=
re
.
compile
(
r
"
^
(
[
0
-
9
]
+
)
(
(
?
:
a
|
b
|
c
|
rc
)
[
0
-
9
]
+
)
"
)
def
_version_split
(
version
)
:
    
result
=
[
]
    
for
item
in
version
.
split
(
"
.
"
)
:
        
match
=
_prefix_regex
.
search
(
item
)
        
if
match
:
            
result
.
extend
(
match
.
groups
(
)
)
        
else
:
            
result
.
append
(
item
)
    
return
result
def
_pad_version
(
left
right
)
:
    
left_split
right_split
=
[
]
[
]
    
left_split
.
append
(
list
(
itertools
.
takewhile
(
lambda
x
:
x
.
isdigit
(
)
left
)
)
)
    
right_split
.
append
(
list
(
itertools
.
takewhile
(
lambda
x
:
x
.
isdigit
(
)
right
)
)
)
    
left_split
.
append
(
left
[
len
(
left_split
[
0
]
)
:
]
)
    
right_split
.
append
(
right
[
len
(
right_split
[
0
]
)
:
]
)
    
left_split
.
insert
(
1
[
"
0
"
]
*
max
(
0
len
(
right_split
[
0
]
)
-
len
(
left_split
[
0
]
)
)
)
    
right_split
.
insert
(
1
[
"
0
"
]
*
max
(
0
len
(
left_split
[
0
]
)
-
len
(
right_split
[
0
]
)
)
)
    
return
(
list
(
itertools
.
chain
(
*
left_split
)
)
list
(
itertools
.
chain
(
*
right_split
)
)
)
class
SpecifierSet
(
BaseSpecifier
)
:
    
def
__init__
(
self
specifiers
=
"
"
prereleases
=
None
)
:
        
split_specifiers
=
[
s
.
strip
(
)
for
s
in
specifiers
.
split
(
"
"
)
if
s
.
strip
(
)
]
        
parsed
=
set
(
)
        
for
specifier
in
split_specifiers
:
            
try
:
                
parsed
.
add
(
Specifier
(
specifier
)
)
            
except
InvalidSpecifier
:
                
parsed
.
add
(
LegacySpecifier
(
specifier
)
)
        
self
.
_specs
=
frozenset
(
parsed
)
        
self
.
_prereleases
=
prereleases
    
def
__repr__
(
self
)
:
        
pre
=
(
            
"
prereleases
=
{
0
!
r
}
"
.
format
(
self
.
prereleases
)
            
if
self
.
_prereleases
is
not
None
            
else
"
"
        
)
        
return
"
<
SpecifierSet
(
{
0
!
r
}
{
1
}
)
>
"
.
format
(
str
(
self
)
pre
)
    
def
__str__
(
self
)
:
        
return
"
"
.
join
(
sorted
(
str
(
s
)
for
s
in
self
.
_specs
)
)
    
def
__hash__
(
self
)
:
        
return
hash
(
self
.
_specs
)
    
def
__and__
(
self
other
)
:
        
if
isinstance
(
other
string_types
)
:
            
other
=
SpecifierSet
(
other
)
        
elif
not
isinstance
(
other
SpecifierSet
)
:
            
return
NotImplemented
        
specifier
=
SpecifierSet
(
)
        
specifier
.
_specs
=
frozenset
(
self
.
_specs
|
other
.
_specs
)
        
if
self
.
_prereleases
is
None
and
other
.
_prereleases
is
not
None
:
            
specifier
.
_prereleases
=
other
.
_prereleases
        
elif
self
.
_prereleases
is
not
None
and
other
.
_prereleases
is
None
:
            
specifier
.
_prereleases
=
self
.
_prereleases
        
elif
self
.
_prereleases
=
=
other
.
_prereleases
:
            
specifier
.
_prereleases
=
self
.
_prereleases
        
else
:
            
raise
ValueError
(
                
"
Cannot
combine
SpecifierSets
with
True
and
False
prerelease
"
                
"
overrides
.
"
            
)
        
return
specifier
    
def
__eq__
(
self
other
)
:
        
if
isinstance
(
other
(
string_types
_IndividualSpecifier
)
)
:
            
other
=
SpecifierSet
(
str
(
other
)
)
        
elif
not
isinstance
(
other
SpecifierSet
)
:
            
return
NotImplemented
        
return
self
.
_specs
=
=
other
.
_specs
    
def
__ne__
(
self
other
)
:
        
if
isinstance
(
other
(
string_types
_IndividualSpecifier
)
)
:
            
other
=
SpecifierSet
(
str
(
other
)
)
        
elif
not
isinstance
(
other
SpecifierSet
)
:
            
return
NotImplemented
        
return
self
.
_specs
!
=
other
.
_specs
    
def
__len__
(
self
)
:
        
return
len
(
self
.
_specs
)
    
def
__iter__
(
self
)
:
        
return
iter
(
self
.
_specs
)
    
property
    
def
prereleases
(
self
)
:
        
if
self
.
_prereleases
is
not
None
:
            
return
self
.
_prereleases
        
if
not
self
.
_specs
:
            
return
None
        
return
any
(
s
.
prereleases
for
s
in
self
.
_specs
)
    
prereleases
.
setter
    
def
prereleases
(
self
value
)
:
        
self
.
_prereleases
=
value
    
def
__contains__
(
self
item
)
:
        
return
self
.
contains
(
item
)
    
def
contains
(
self
item
prereleases
=
None
)
:
        
if
not
isinstance
(
item
(
LegacyVersion
Version
)
)
:
            
item
=
parse
(
item
)
        
if
prereleases
is
None
:
            
prereleases
=
self
.
prereleases
        
if
not
prereleases
and
item
.
is_prerelease
:
            
return
False
        
return
all
(
s
.
contains
(
item
prereleases
=
prereleases
)
for
s
in
self
.
_specs
)
    
def
filter
(
        
self
        
iterable
        
prereleases
=
None
    
)
:
        
if
prereleases
is
None
:
            
prereleases
=
self
.
prereleases
        
if
self
.
_specs
:
            
for
spec
in
self
.
_specs
:
                
iterable
=
spec
.
filter
(
iterable
prereleases
=
bool
(
prereleases
)
)
            
return
iterable
        
else
:
            
filtered
=
[
]
            
found_prereleases
=
[
]
            
for
item
in
iterable
:
                
if
not
isinstance
(
item
(
LegacyVersion
Version
)
)
:
                    
parsed_version
=
parse
(
item
)
                
else
:
                    
parsed_version
=
item
                
if
isinstance
(
parsed_version
LegacyVersion
)
:
                    
continue
                
if
parsed_version
.
is_prerelease
and
not
prereleases
:
                    
if
not
filtered
:
                        
found_prereleases
.
append
(
item
)
                
else
:
                    
filtered
.
append
(
item
)
            
if
not
filtered
and
found_prereleases
and
prereleases
is
None
:
                
return
found_prereleases
            
return
filtered
