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
django_filters
class
PackageURLFilter
(
django_filters
.
CharFilter
)
:
    
"
"
"
    
Filter
by
an
exact
Package
URL
string
.
    
The
special
"
EMPTY
"
value
allows
retrieval
of
objects
with
an
empty
Package
URL
.
    
This
filter
depends
on
for_package_url
and
empty_package_url
    
methods
to
be
available
on
the
Model
Manager
    
see
for
example
PackageURLQuerySetMixin
.
    
When
exact_match_only
is
True
the
filter
will
match
only
exact
Package
URL
strings
.
    
"
"
"
    
is_empty
=
"
EMPTY
"
    
exact_match_only
=
False
    
help_text
=
(
        
'
Match
Package
URL
.
Use
"
EMPTY
"
as
value
to
retrieve
objects
with
empty
Package
URL
.
'
    
)
    
def
__init__
(
self
*
args
*
*
kwargs
)
:
        
self
.
exact_match_only
=
kwargs
.
pop
(
"
exact_match_only
"
False
)
        
kwargs
.
setdefault
(
"
help_text
"
self
.
help_text
)
        
super
(
)
.
__init__
(
*
args
*
*
kwargs
)
    
def
filter
(
self
qs
value
)
:
        
none_values
=
(
[
]
(
)
{
}
"
"
None
)
        
if
value
in
none_values
:
            
return
qs
        
if
self
.
distinct
:
            
qs
=
qs
.
distinct
(
)
        
if
value
=
=
self
.
is_empty
:
            
return
qs
.
empty_package_url
(
)
        
return
qs
.
for_package_url
(
value
exact_match
=
self
.
exact_match_only
)
