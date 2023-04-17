import
sys
__all__
=
[
'
install
'
'
NullFinder
'
'
PyPy_repr
'
]
def
install
(
cls
)
:
    
"
"
"
    
Class
decorator
for
installation
on
sys
.
meta_path
.
    
Adds
the
backport
DistributionFinder
to
sys
.
meta_path
and
    
attempts
to
disable
the
finder
functionality
of
the
stdlib
    
DistributionFinder
.
    
"
"
"
    
sys
.
meta_path
.
append
(
cls
(
)
)
    
disable_stdlib_finder
(
)
    
return
cls
def
disable_stdlib_finder
(
)
:
    
"
"
"
    
Give
the
backport
primacy
for
discovering
path
-
based
distributions
    
by
monkey
-
patching
the
stdlib
O_O
.
    
See
#
91
for
more
background
for
rationale
on
this
sketchy
    
behavior
.
    
"
"
"
    
def
matches
(
finder
)
:
        
return
getattr
(
            
finder
'
__module__
'
None
        
)
=
=
'
_frozen_importlib_external
'
and
hasattr
(
finder
'
find_distributions
'
)
    
for
finder
in
filter
(
matches
sys
.
meta_path
)
:
        
del
finder
.
find_distributions
class
NullFinder
:
    
"
"
"
    
A
"
Finder
"
(
aka
"
MetaClassFinder
"
)
that
never
finds
any
modules
    
but
may
find
distributions
.
    
"
"
"
    
staticmethod
    
def
find_spec
(
*
args
*
*
kwargs
)
:
        
return
None
    
find_module
=
find_spec
class
PyPy_repr
:
    
"
"
"
    
Override
repr
for
EntryPoint
objects
on
PyPy
to
avoid
__iter__
access
.
    
Ref
#
97
#
102
.
    
"
"
"
    
affected
=
hasattr
(
sys
'
pypy_version_info
'
)
    
def
__compat_repr__
(
self
)
:
        
def
make_param
(
name
)
:
            
value
=
getattr
(
self
name
)
            
return
'
{
name
}
=
{
value
!
r
}
'
.
format
(
*
*
locals
(
)
)
        
params
=
'
'
.
join
(
map
(
make_param
self
.
_fields
)
)
        
return
'
EntryPoint
(
{
params
}
)
'
.
format
(
*
*
locals
(
)
)
    
if
affected
:
        
__repr__
=
__compat_repr__
    
del
affected
