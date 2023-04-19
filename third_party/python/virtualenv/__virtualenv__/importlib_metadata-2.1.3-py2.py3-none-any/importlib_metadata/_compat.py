from
__future__
import
absolute_import
unicode_literals
import
io
import
abc
import
sys
import
email
if
sys
.
version_info
>
(
3
)
:
    
import
builtins
    
from
configparser
import
ConfigParser
    
import
contextlib
    
FileNotFoundError
=
builtins
.
FileNotFoundError
    
IsADirectoryError
=
builtins
.
IsADirectoryError
    
NotADirectoryError
=
builtins
.
NotADirectoryError
    
PermissionError
=
builtins
.
PermissionError
    
map
=
builtins
.
map
    
from
itertools
import
filterfalse
else
:
    
from
backports
.
configparser
import
ConfigParser
    
from
itertools
import
imap
as
map
    
from
itertools
import
ifilterfalse
as
filterfalse
    
import
contextlib2
as
contextlib
    
FileNotFoundError
=
IOError
OSError
    
IsADirectoryError
=
IOError
OSError
    
NotADirectoryError
=
IOError
OSError
    
PermissionError
=
IOError
OSError
str
=
type
(
'
'
)
suppress
=
contextlib
.
suppress
if
sys
.
version_info
>
(
3
5
)
:
    
import
pathlib
else
:
    
import
pathlib2
as
pathlib
try
:
    
ModuleNotFoundError
=
builtins
.
FileNotFoundError
except
(
NameError
AttributeError
)
:
    
ModuleNotFoundError
=
ImportError
if
sys
.
version_info
>
=
(
3
)
:
    
from
importlib
.
abc
import
MetaPathFinder
else
:
    
class
MetaPathFinder
(
object
)
:
        
__metaclass__
=
abc
.
ABCMeta
__metaclass__
=
type
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
MetaPathFinder
'
'
ModuleNotFoundError
'
    
'
pathlib
'
'
ConfigParser
'
'
map
'
'
suppress
'
'
FileNotFoundError
'
    
'
NotADirectoryError
'
'
email_message_from_string
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
(
            
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
def
py2_message_from_string
(
text
)
:
    
io_buffer
=
io
.
StringIO
(
text
)
    
return
email
.
message_from_file
(
io_buffer
)
email_message_from_string
=
(
    
py2_message_from_string
    
if
sys
.
version_info
<
(
3
)
else
    
email
.
message_from_string
    
)
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
def
unique_everseen
(
iterable
)
:
    
"
List
unique
elements
preserving
order
.
Remember
all
elements
ever
seen
.
"
    
seen
=
set
(
)
    
seen_add
=
seen
.
add
    
for
element
in
filterfalse
(
seen
.
__contains__
iterable
)
:
        
seen_add
(
element
)
        
yield
element
unique_ordered
=
(
    
unique_everseen
if
sys
.
version_info
<
(
3
7
)
else
dict
.
fromkeys
)
