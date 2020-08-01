#
-
*
-
coding
=
utf
-
8
-
*
-
from
__future__
import
absolute_import
print_function
unicode_literals
import
os
import
resolvelib
from
.
.
internals
.
candidates
import
find_candidates
from
.
.
internals
.
dependencies
import
get_dependencies
from
.
.
internals
.
utils
import
(
    
filter_sources
get_allow_prereleases
identify_requirment
strip_extras
)
PROTECTED_PACKAGE_NAMES
=
{
"
pip
"
"
setuptools
"
}
class
BasicProvider
(
resolvelib
.
AbstractProvider
)
:
    
"
"
"
Provider
implementation
to
interface
with
requirementslib
.
Requirement
.
    
"
"
"
    
def
__init__
(
self
root_requirements
sources
                 
requires_python
allow_prereleases
)
:
        
self
.
sources
=
sources
        
self
.
requires_python
=
requires_python
        
self
.
allow_prereleases
=
bool
(
allow_prereleases
)
        
self
.
invalid_candidates
=
set
(
)
        
self
.
fetched_dependencies
=
{
None
:
{
            
self
.
identify
(
r
)
:
r
for
r
in
root_requirements
        
}
}
        
self
.
collected_requires_pythons
=
{
None
:
"
"
}
    
def
identify
(
self
dependency
)
:
        
return
identify_requirment
(
dependency
)
    
def
get_preference
(
self
resolution
candidates
information
)
:
        
return
len
(
candidates
)
    
def
find_matches
(
self
requirement
)
:
        
sources
=
filter_sources
(
requirement
self
.
sources
)
        
candidates
=
find_candidates
(
            
requirement
sources
self
.
requires_python
            
get_allow_prereleases
(
requirement
self
.
allow_prereleases
)
        
)
        
return
candidates
    
def
is_satisfied_by
(
self
requirement
candidate
)
:
        
if
not
requirement
.
is_named
:
            
return
True
        
if
not
candidate
.
is_named
:
            
return
True
        
if
not
requirement
.
specifiers
:
            
return
True
        
candidate_line
=
candidate
.
as_line
(
include_hashes
=
False
)
        
if
candidate_line
in
self
.
invalid_candidates
:
            
return
False
        
try
:
            
version
=
candidate
.
get_specifier
(
)
.
version
        
except
(
TypeError
ValueError
)
:
            
print
(
'
ignoring
invalid
version
from
{
!
r
}
'
.
format
(
candidate_line
)
)
            
self
.
invalid_candidates
.
add
(
candidate_line
)
            
return
False
        
return
requirement
.
as_ireq
(
)
.
specifier
.
contains
(
version
)
    
def
get_dependencies
(
self
candidate
)
:
        
sources
=
filter_sources
(
candidate
self
.
sources
)
        
try
:
            
dependencies
requires_python
=
get_dependencies
(
                
candidate
sources
=
sources
            
)
        
except
Exception
as
e
:
            
if
os
.
environ
.
get
(
"
PASSA_NO_SUPPRESS_EXCEPTIONS
"
)
:
                
raise
            
print
(
"
failed
to
get
dependencies
for
{
0
!
r
}
:
{
1
}
"
.
format
(
                
candidate
.
as_line
(
include_hashes
=
False
)
e
            
)
)
            
dependencies
=
[
]
            
requires_python
=
"
"
        
dependencies
=
[
            
dependency
for
dependency
in
dependencies
            
if
dependency
.
normalized_name
not
in
PROTECTED_PACKAGE_NAMES
        
]
        
if
candidate
.
extras
:
            
dependencies
.
append
(
strip_extras
(
candidate
)
)
        
candidate_key
=
self
.
identify
(
candidate
)
        
self
.
fetched_dependencies
[
candidate_key
]
=
{
            
self
.
identify
(
r
)
:
r
for
r
in
dependencies
        
}
        
self
.
collected_requires_pythons
[
candidate_key
]
=
requires_python
        
return
dependencies
class
PinReuseProvider
(
BasicProvider
)
:
    
"
"
"
A
provider
that
reuses
preferred
pins
if
possible
.
    
This
is
used
to
implement
"
add
"
"
remove
"
and
"
only
-
if
-
needed
upgrade
"
    
where
already
-
pinned
candidates
in
Pipfile
.
lock
should
be
preferred
.
    
"
"
"
    
def
__init__
(
self
preferred_pins
*
args
*
*
kwargs
)
:
        
super
(
PinReuseProvider
self
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
        
self
.
preferred_pins
=
preferred_pins
    
def
find_matches
(
self
requirement
)
:
        
candidates
=
super
(
PinReuseProvider
self
)
.
find_matches
(
requirement
)
        
try
:
            
candidates
.
append
(
self
.
preferred_pins
[
self
.
identify
(
requirement
)
]
)
        
except
KeyError
:
            
pass
        
return
candidates
class
EagerUpgradeProvider
(
PinReuseProvider
)
:
    
"
"
"
A
specialized
provider
to
handle
an
"
eager
"
upgrade
strategy
.
    
An
eager
upgrade
tries
to
upgrade
not
only
packages
specified
but
also
    
their
dependencies
(
recursively
)
.
This
contrasts
to
the
"
only
-
if
-
needed
"
    
default
which
only
promises
to
upgrade
the
specified
package
and
    
prevents
touching
anything
else
if
at
all
possible
.
    
The
provider
is
implemented
as
to
keep
track
of
all
dependencies
of
the
    
specified
packages
to
upgrade
and
free
their
pins
when
it
has
a
chance
.
    
"
"
"
    
def
__init__
(
self
tracked_names
*
args
*
*
kwargs
)
:
        
super
(
EagerUpgradeProvider
self
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
        
self
.
tracked_names
=
set
(
tracked_names
)
        
for
name
in
tracked_names
:
            
self
.
preferred_pins
.
pop
(
name
None
)
        
for
pin
in
self
.
preferred_pins
.
values
(
)
:
            
pin
.
_preferred_by_provider
=
True
    
def
is_satisfied_by
(
self
requirement
candidate
)
:
        
if
(
self
.
identify
(
requirement
)
in
self
.
tracked_names
and
                
getattr
(
candidate
"
_preferred_by_provider
"
False
)
)
:
            
return
False
        
return
super
(
EagerUpgradeProvider
self
)
.
is_satisfied_by
(
            
requirement
candidate
        
)
    
def
get_dependencies
(
self
candidate
)
:
        
dependencies
=
super
(
EagerUpgradeProvider
self
)
.
get_dependencies
(
            
candidate
        
)
        
if
self
.
identify
(
candidate
)
in
self
.
tracked_names
:
            
for
dependency
in
dependencies
:
                
name
=
self
.
identify
(
dependency
)
                
self
.
tracked_names
.
add
(
name
)
                
self
.
preferred_pins
.
pop
(
name
None
)
        
return
dependencies
    
def
get_preference
(
self
resolution
candidates
information
)
:
        
name
=
self
.
identify
(
candidates
[
0
]
)
        
if
name
in
self
.
tracked_names
:
            
return
-
1
        
return
len
(
candidates
)
