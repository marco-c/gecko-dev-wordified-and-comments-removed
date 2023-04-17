#
coding
:
utf
-
8
from
__future__
import
absolute_import
division
print_function
unicode_literals
import
copy
from
functools
import
partial
from
itertools
import
chain
count
groupby
from
pip
.
_internal
.
req
.
constructors
import
install_req_from_line
from
pip
.
_internal
.
req
.
req_tracker
import
update_env_context_manager
from
.
import
click
from
.
logging
import
log
from
.
utils
import
(
    
UNSAFE_PACKAGES
    
format_requirement
    
format_specifier
    
is_pinned_requirement
    
is_url_requirement
    
key_from_ireq
)
green
=
partial
(
click
.
style
fg
=
"
green
"
)
magenta
=
partial
(
click
.
style
fg
=
"
magenta
"
)
class
RequirementSummary
(
object
)
:
    
"
"
"
    
Summary
of
a
requirement
'
s
properties
for
comparison
purposes
.
    
"
"
"
    
def
__init__
(
self
ireq
)
:
        
self
.
req
=
ireq
.
req
        
self
.
key
=
key_from_ireq
(
ireq
)
        
self
.
extras
=
frozenset
(
ireq
.
extras
)
        
self
.
specifier
=
ireq
.
specifier
    
def
__eq__
(
self
other
)
:
        
return
(
            
self
.
key
=
=
other
.
key
            
and
self
.
specifier
=
=
other
.
specifier
            
and
self
.
extras
=
=
other
.
extras
        
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
(
self
.
key
self
.
specifier
self
.
extras
)
)
    
def
__str__
(
self
)
:
        
return
repr
(
(
self
.
key
str
(
self
.
specifier
)
sorted
(
self
.
extras
)
)
)
def
combine_install_requirements
(
repository
ireqs
)
:
    
"
"
"
    
Return
a
single
install
requirement
that
reflects
a
combination
of
    
all
the
inputs
.
    
"
"
"
    
source_ireqs
=
[
]
    
for
ireq
in
ireqs
:
        
source_ireqs
.
extend
(
getattr
(
ireq
"
_source_ireqs
"
[
ireq
]
)
)
    
if
len
(
source_ireqs
)
=
=
1
:
        
return
source_ireqs
[
0
]
    
combined_ireq
=
copy
.
deepcopy
(
source_ireqs
[
0
]
)
    
repository
.
copy_ireq_dependencies
(
source_ireqs
[
0
]
combined_ireq
)
    
for
ireq
in
source_ireqs
[
1
:
]
:
        
combined_ireq
.
req
.
specifier
&
=
ireq
.
req
.
specifier
        
if
combined_ireq
.
constraint
:
            
repository
.
copy_ireq_dependencies
(
ireq
combined_ireq
)
        
combined_ireq
.
constraint
&
=
ireq
.
constraint
        
combined_ireq
.
extras
=
tuple
(
            
sorted
(
set
(
tuple
(
combined_ireq
.
extras
)
+
tuple
(
ireq
.
extras
)
)
)
        
)
    
if
len
(
source_ireqs
)
>
1
:
        
if
any
(
ireq
.
comes_from
is
None
for
ireq
in
source_ireqs
)
:
            
combined_ireq
.
comes_from
=
None
        
else
:
            
combined_ireq
.
comes_from
=
min
(
                
(
ireq
.
comes_from
for
ireq
in
source_ireqs
)
                
key
=
lambda
x
:
(
len
(
str
(
x
)
)
str
(
x
)
)
            
)
        
combined_ireq
.
_source_ireqs
=
source_ireqs
    
return
combined_ireq
class
Resolver
(
object
)
:
    
def
__init__
(
        
self
        
constraints
        
repository
        
cache
        
prereleases
=
False
        
clear_caches
=
False
        
allow_unsafe
=
False
    
)
:
        
"
"
"
        
This
class
resolves
a
given
set
of
constraints
(
a
collection
of
        
InstallRequirement
objects
)
by
consulting
the
given
Repository
and
the
        
DependencyCache
.
        
"
"
"
        
self
.
our_constraints
=
set
(
constraints
)
        
self
.
their_constraints
=
set
(
)
        
self
.
repository
=
repository
        
self
.
dependency_cache
=
cache
        
self
.
prereleases
=
prereleases
        
self
.
clear_caches
=
clear_caches
        
self
.
allow_unsafe
=
allow_unsafe
        
self
.
unsafe_constraints
=
set
(
)
    
property
    
def
constraints
(
self
)
:
        
return
set
(
            
self
.
_group_constraints
(
chain
(
self
.
our_constraints
self
.
their_constraints
)
)
        
)
    
def
resolve_hashes
(
self
ireqs
)
:
        
"
"
"
        
Finds
acceptable
hashes
for
all
of
the
given
InstallRequirements
.
        
"
"
"
        
log
.
debug
(
"
"
)
        
log
.
debug
(
"
Generating
hashes
:
"
)
        
with
self
.
repository
.
allow_all_wheels
(
)
log
.
indentation
(
)
:
            
return
{
ireq
:
self
.
repository
.
get_hashes
(
ireq
)
for
ireq
in
ireqs
}
    
def
resolve
(
self
max_rounds
=
10
)
:
        
"
"
"
        
Finds
concrete
package
versions
for
all
the
given
InstallRequirements
        
and
their
recursive
dependencies
.
The
end
result
is
a
flat
list
of
        
(
name
version
)
tuples
.
(
Or
an
editable
package
.
)
        
Resolves
constraints
one
round
at
a
time
until
they
don
'
t
change
        
anymore
.
Protects
against
infinite
loops
by
breaking
out
after
a
max
        
number
rounds
.
        
"
"
"
        
if
self
.
clear_caches
:
            
self
.
dependency_cache
.
clear
(
)
            
self
.
repository
.
clear_caches
(
)
        
with
update_env_context_manager
(
PIP_EXISTS_ACTION
=
str
(
"
i
"
)
)
:
            
for
current_round
in
count
(
start
=
1
)
:
                
if
current_round
>
max_rounds
:
                    
raise
RuntimeError
(
                        
"
No
stable
configuration
of
concrete
packages
"
                        
"
could
be
found
for
the
given
constraints
after
"
                        
"
{
max_rounds
}
rounds
of
resolving
.
\
n
"
                        
"
This
is
likely
a
bug
.
"
.
format
(
max_rounds
=
max_rounds
)
                    
)
                
log
.
debug
(
"
"
)
                
log
.
debug
(
magenta
(
"
{
:
^
60
}
"
.
format
(
"
ROUND
{
}
"
.
format
(
current_round
)
)
)
)
                
with
self
.
repository
.
freshen_build_caches
(
)
:
                    
has_changed
best_matches
=
self
.
_resolve_one_round
(
)
                    
log
.
debug
(
"
-
"
*
60
)
                    
log
.
debug
(
                        
"
Result
of
round
{
}
:
{
}
"
.
format
(
                            
current_round
                            
"
not
stable
"
if
has_changed
else
"
stable
done
"
                        
)
                    
)
                
if
not
has_changed
:
                    
break
        
results
=
{
req
for
req
in
best_matches
if
not
req
.
constraint
}
        
self
.
unsafe_constraints
=
set
(
)
        
if
not
self
.
allow_unsafe
:
            
reverse_dependencies
=
self
.
reverse_dependencies
(
results
)
            
for
req
in
results
.
copy
(
)
:
                
required_by
=
reverse_dependencies
.
get
(
req
.
name
.
lower
(
)
[
]
)
                
if
req
.
name
in
UNSAFE_PACKAGES
or
(
                    
required_by
and
all
(
name
in
UNSAFE_PACKAGES
for
name
in
required_by
)
                
)
:
                    
self
.
unsafe_constraints
.
add
(
req
)
                    
results
.
remove
(
req
)
        
return
results
    
def
_group_constraints
(
self
constraints
)
:
        
"
"
"
        
Groups
constraints
(
remember
InstallRequirements
!
)
by
their
key
name
        
and
combining
their
SpecifierSets
into
a
single
InstallRequirement
per
        
package
.
For
example
given
the
following
constraints
:
            
Django
<
1
.
9
>
=
1
.
4
.
2
            
django
~
=
1
.
5
            
Flask
~
=
0
.
7
        
This
will
be
combined
into
a
single
entry
per
package
:
            
django
~
=
1
.
5
<
1
.
9
>
=
1
.
4
.
2
            
flask
~
=
0
.
7
        
"
"
"
        
constraints
=
list
(
constraints
)
        
for
ireq
in
constraints
:
            
if
ireq
.
name
is
None
:
                
self
.
repository
.
get_dependencies
(
ireq
)
        
for
_
ireqs
in
groupby
(
            
sorted
(
constraints
key
=
(
lambda
x
:
(
key_from_ireq
(
x
)
not
x
.
editable
)
)
)
            
key
=
key_from_ireq
        
)
:
            
yield
combine_install_requirements
(
self
.
repository
ireqs
)
    
def
_resolve_one_round
(
self
)
:
        
"
"
"
        
Resolves
one
level
of
the
current
constraints
by
finding
the
best
        
match
for
each
package
in
the
repository
and
adding
all
requirements
        
for
those
best
package
versions
.
Some
of
these
constraints
may
be
new
        
or
updated
.
        
Returns
whether
new
constraints
appeared
in
this
round
.
If
no
        
constraints
were
added
or
changed
this
indicates
a
stable
        
configuration
.
        
"
"
"
        
constraints
=
sorted
(
self
.
constraints
key
=
key_from_ireq
)
        
log
.
debug
(
"
Current
constraints
:
"
)
        
with
log
.
indentation
(
)
:
            
for
constraint
in
constraints
:
                
log
.
debug
(
str
(
constraint
)
)
        
log
.
debug
(
"
"
)
        
log
.
debug
(
"
Finding
the
best
candidates
:
"
)
        
with
log
.
indentation
(
)
:
            
best_matches
=
{
self
.
get_best_match
(
ireq
)
for
ireq
in
constraints
}
        
log
.
debug
(
"
"
)
        
log
.
debug
(
"
Finding
secondary
dependencies
:
"
)
        
their_constraints
=
[
]
        
with
log
.
indentation
(
)
:
            
for
best_match
in
best_matches
:
                
their_constraints
.
extend
(
self
.
_iter_dependencies
(
best_match
)
)
        
theirs
=
set
(
self
.
_group_constraints
(
their_constraints
)
)
        
diff
=
{
RequirementSummary
(
t
)
for
t
in
theirs
}
-
{
            
RequirementSummary
(
t
)
for
t
in
self
.
their_constraints
        
}
        
removed
=
{
RequirementSummary
(
t
)
for
t
in
self
.
their_constraints
}
-
{
            
RequirementSummary
(
t
)
for
t
in
theirs
        
}
        
has_changed
=
len
(
diff
)
>
0
or
len
(
removed
)
>
0
        
if
has_changed
:
            
log
.
debug
(
"
"
)
            
log
.
debug
(
"
New
dependencies
found
in
this
round
:
"
)
            
with
log
.
indentation
(
)
:
                
for
new_dependency
in
sorted
(
diff
key
=
key_from_ireq
)
:
                    
log
.
debug
(
"
adding
{
}
"
.
format
(
new_dependency
)
)
            
log
.
debug
(
"
Removed
dependencies
in
this
round
:
"
)
            
with
log
.
indentation
(
)
:
                
for
removed_dependency
in
sorted
(
removed
key
=
key_from_ireq
)
:
                    
log
.
debug
(
"
removing
{
}
"
.
format
(
removed_dependency
)
)
        
self
.
their_constraints
=
theirs
        
return
has_changed
best_matches
    
def
get_best_match
(
self
ireq
)
:
        
"
"
"
        
Returns
a
(
pinned
or
editable
)
InstallRequirement
indicating
the
best
        
match
to
use
for
the
given
InstallRequirement
(
in
the
form
of
an
        
InstallRequirement
)
.
        
Example
:
        
Given
the
constraint
Flask
>
=
0
.
10
may
return
Flask
=
=
0
.
10
.
1
at
        
a
certain
moment
in
time
.
        
Pinned
requirements
will
always
return
themselves
i
.
e
.
            
Flask
=
=
0
.
10
.
1
=
>
Flask
=
=
0
.
10
.
1
        
"
"
"
        
if
ireq
.
editable
or
is_url_requirement
(
ireq
)
:
            
best_match
=
ireq
        
elif
is_pinned_requirement
(
ireq
)
:
            
best_match
=
ireq
        
elif
ireq
.
constraint
:
            
best_match
=
ireq
        
else
:
            
best_match
=
self
.
repository
.
find_best_match
(
                
ireq
prereleases
=
self
.
prereleases
            
)
        
log
.
debug
(
            
"
found
candidate
{
}
(
constraint
was
{
}
)
"
.
format
(
                
format_requirement
(
best_match
)
format_specifier
(
ireq
)
            
)
        
)
        
best_match
.
comes_from
=
ireq
.
comes_from
        
if
hasattr
(
ireq
"
_source_ireqs
"
)
:
            
best_match
.
_source_ireqs
=
ireq
.
_source_ireqs
        
return
best_match
    
def
_iter_dependencies
(
self
ireq
)
:
        
"
"
"
        
Given
a
pinned
url
or
editable
InstallRequirement
collects
all
the
        
secondary
dependencies
for
them
either
by
looking
them
up
in
a
local
        
cache
or
by
reaching
out
to
the
repository
.
        
Editable
requirements
will
never
be
looked
up
as
they
may
have
        
changed
at
any
time
.
        
"
"
"
        
if
ireq
.
constraint
:
            
return
        
if
ireq
.
editable
or
is_url_requirement
(
ireq
)
:
            
for
dependency
in
self
.
repository
.
get_dependencies
(
ireq
)
:
                
yield
dependency
            
return
        
elif
not
is_pinned_requirement
(
ireq
)
:
            
raise
TypeError
(
                
"
Expected
pinned
or
editable
requirement
got
{
}
"
.
format
(
ireq
)
            
)
        
if
ireq
not
in
self
.
dependency_cache
:
            
log
.
debug
(
                
"
{
}
not
in
cache
need
to
check
index
"
.
format
(
format_requirement
(
ireq
)
)
                
fg
=
"
yellow
"
            
)
            
dependencies
=
self
.
repository
.
get_dependencies
(
ireq
)
            
self
.
dependency_cache
[
ireq
]
=
sorted
(
str
(
ireq
.
req
)
for
ireq
in
dependencies
)
        
dependency_strings
=
self
.
dependency_cache
[
ireq
]
        
log
.
debug
(
            
"
{
:
25
}
requires
{
}
"
.
format
(
                
format_requirement
(
ireq
)
                
"
"
.
join
(
sorted
(
dependency_strings
key
=
lambda
s
:
s
.
lower
(
)
)
)
or
"
-
"
            
)
        
)
        
for
dependency_string
in
dependency_strings
:
            
yield
install_req_from_line
(
                
dependency_string
constraint
=
ireq
.
constraint
comes_from
=
ireq
            
)
    
def
reverse_dependencies
(
self
ireqs
)
:
        
non_editable
=
[
            
ireq
for
ireq
in
ireqs
if
not
(
ireq
.
editable
or
is_url_requirement
(
ireq
)
)
        
]
        
return
self
.
dependency_cache
.
reverse_dependencies
(
non_editable
)
