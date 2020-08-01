from
__future__
import
absolute_import
import
errno
import
itertools
import
logging
import
os
.
path
import
tempfile
from
contextlib
import
contextmanager
from
pipenv
.
patched
.
notpip
.
_vendor
.
contextlib2
import
ExitStack
import
warnings
from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
misc
import
rmtree
from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
typing
import
MYPY_CHECK_RUNNING
from
pipenv
.
vendor
.
vistir
.
compat
import
finalize
ResourceWarning
if
MYPY_CHECK_RUNNING
:
    
from
typing
import
Any
Dict
Iterator
Optional
TypeVar
    
_T
=
TypeVar
(
'
_T
'
bound
=
'
TempDirectory
'
)
logger
=
logging
.
getLogger
(
__name__
)
_tempdir_manager
=
None
contextmanager
def
global_tempdir_manager
(
)
:
    
global
_tempdir_manager
    
with
ExitStack
(
)
as
stack
:
        
old_tempdir_manager
_tempdir_manager
=
_tempdir_manager
stack
        
try
:
            
yield
        
finally
:
            
_tempdir_manager
=
old_tempdir_manager
class
TempDirectoryTypeRegistry
(
object
)
:
    
"
"
"
Manages
temp
directory
behavior
    
"
"
"
    
def
__init__
(
self
)
:
        
self
.
_should_delete
=
{
}
    
def
set_delete
(
self
kind
value
)
:
        
"
"
"
Indicate
whether
a
TempDirectory
of
the
given
kind
should
be
        
auto
-
deleted
.
        
"
"
"
        
self
.
_should_delete
[
kind
]
=
value
    
def
get_delete
(
self
kind
)
:
        
"
"
"
Get
configured
auto
-
delete
flag
for
a
given
TempDirectory
type
        
default
True
.
        
"
"
"
        
return
self
.
_should_delete
.
get
(
kind
True
)
_tempdir_registry
=
None
contextmanager
def
tempdir_registry
(
)
:
    
"
"
"
Provides
a
scoped
global
tempdir
registry
that
can
be
used
to
dictate
    
whether
directories
should
be
deleted
.
    
"
"
"
    
global
_tempdir_registry
    
old_tempdir_registry
=
_tempdir_registry
    
_tempdir_registry
=
TempDirectoryTypeRegistry
(
)
    
try
:
        
yield
_tempdir_registry
    
finally
:
        
_tempdir_registry
=
old_tempdir_registry
class
TempDirectory
(
object
)
:
    
"
"
"
Helper
class
that
owns
and
cleans
up
a
temporary
directory
.
    
This
class
can
be
used
as
a
context
manager
or
as
an
OO
representation
of
a
    
temporary
directory
.
    
Attributes
:
        
path
            
Location
to
the
created
temporary
directory
        
delete
            
Whether
the
directory
should
be
deleted
when
exiting
            
(
when
used
as
a
contextmanager
)
    
Methods
:
        
cleanup
(
)
            
Deletes
the
temporary
directory
    
When
used
as
a
context
manager
if
the
delete
attribute
is
True
on
    
exiting
the
context
the
temporary
directory
is
deleted
.
    
"
"
"
    
def
__init__
(
        
self
        
path
=
None
        
delete
=
None
        
kind
=
"
temp
"
        
globally_managed
=
False
    
)
:
        
super
(
TempDirectory
self
)
.
__init__
(
)
        
if
path
is
not
None
and
delete
is
None
:
            
delete
=
False
        
if
path
is
None
:
            
path
=
self
.
_create
(
kind
)
        
self
.
_path
=
path
        
self
.
_deleted
=
False
        
self
.
delete
=
delete
        
self
.
kind
=
kind
        
self
.
_finalizer
=
None
        
if
self
.
_path
:
            
self
.
_register_finalizer
(
)
        
if
globally_managed
:
            
assert
_tempdir_manager
is
not
None
            
_tempdir_manager
.
enter_context
(
self
)
    
def
_register_finalizer
(
self
)
:
        
if
self
.
delete
and
self
.
_path
:
            
self
.
_finalizer
=
finalize
(
                
self
                
self
.
_cleanup
                
self
.
_path
                
warn_message
=
None
            
)
        
else
:
            
self
.
_finalizer
=
None
    
property
    
def
path
(
self
)
:
        
assert
not
self
.
_deleted
(
            
"
Attempted
to
access
deleted
path
:
{
}
"
.
format
(
self
.
_path
)
        
)
        
return
self
.
_path
    
def
__repr__
(
self
)
:
        
return
"
<
{
}
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
__class__
.
__name__
self
.
path
)
    
def
__enter__
(
self
)
:
        
return
self
    
def
__exit__
(
self
exc
value
tb
)
:
        
if
self
.
delete
is
not
None
:
            
delete
=
self
.
delete
        
elif
_tempdir_registry
:
            
delete
=
_tempdir_registry
.
get_delete
(
self
.
kind
)
        
else
:
            
delete
=
True
        
if
delete
:
            
self
.
cleanup
(
)
    
def
_create
(
self
kind
)
:
        
"
"
"
Create
a
temporary
directory
and
store
its
path
in
self
.
path
        
"
"
"
        
path
=
os
.
path
.
realpath
(
            
tempfile
.
mkdtemp
(
prefix
=
"
pip
-
{
}
-
"
.
format
(
kind
)
)
        
)
        
logger
.
debug
(
"
Created
temporary
directory
:
{
}
"
.
format
(
path
)
)
        
return
path
    
classmethod
    
def
_cleanup
(
cls
name
warn_message
=
None
)
:
        
if
not
os
.
path
.
exists
(
name
)
:
            
return
        
try
:
            
rmtree
(
name
)
        
except
OSError
:
            
pass
        
else
:
            
if
warn_message
:
                
warnings
.
warn
(
warn_message
ResourceWarning
)
    
def
cleanup
(
self
)
:
        
"
"
"
Remove
the
temporary
directory
created
and
reset
state
        
"
"
"
        
if
getattr
(
self
.
_finalizer
"
detach
"
None
)
and
self
.
_finalizer
.
detach
(
)
:
            
if
os
.
path
.
exists
(
self
.
_path
)
:
                
self
.
_deleted
=
True
                
try
:
                    
rmtree
(
self
.
_path
)
                
except
OSError
:
                    
pass
class
AdjacentTempDirectory
(
TempDirectory
)
:
    
"
"
"
Helper
class
that
creates
a
temporary
directory
adjacent
to
a
real
one
.
    
Attributes
:
        
original
            
The
original
directory
to
create
a
temp
directory
for
.
        
path
            
After
calling
create
(
)
or
entering
contains
the
full
            
path
to
the
temporary
directory
.
        
delete
            
Whether
the
directory
should
be
deleted
when
exiting
            
(
when
used
as
a
contextmanager
)
    
"
"
"
    
LEADING_CHARS
=
"
-
~
.
=
%
0123456789
"
    
def
__init__
(
self
original
delete
=
None
)
:
        
self
.
original
=
original
.
rstrip
(
'
/
\
\
'
)
        
super
(
AdjacentTempDirectory
self
)
.
__init__
(
delete
=
delete
)
    
classmethod
    
def
_generate_names
(
cls
name
)
:
        
"
"
"
Generates
a
series
of
temporary
names
.
        
The
algorithm
replaces
the
leading
characters
in
the
name
        
with
ones
that
are
valid
filesystem
characters
but
are
not
        
valid
package
names
(
for
both
Python
and
pip
definitions
of
        
package
)
.
        
"
"
"
        
for
i
in
range
(
1
len
(
name
)
)
:
            
for
candidate
in
itertools
.
combinations_with_replacement
(
                    
cls
.
LEADING_CHARS
i
-
1
)
:
                
new_name
=
'
~
'
+
'
'
.
join
(
candidate
)
+
name
[
i
:
]
                
if
new_name
!
=
name
:
                    
yield
new_name
        
for
i
in
range
(
len
(
cls
.
LEADING_CHARS
)
)
:
            
for
candidate
in
itertools
.
combinations_with_replacement
(
                    
cls
.
LEADING_CHARS
i
)
:
                
new_name
=
'
~
'
+
'
'
.
join
(
candidate
)
+
name
                
if
new_name
!
=
name
:
                    
yield
new_name
    
def
_create
(
self
kind
)
:
        
root
name
=
os
.
path
.
split
(
self
.
original
)
        
for
candidate
in
self
.
_generate_names
(
name
)
:
            
path
=
os
.
path
.
join
(
root
candidate
)
            
try
:
                
os
.
mkdir
(
path
)
            
except
OSError
as
ex
:
                
if
ex
.
errno
!
=
errno
.
EEXIST
:
                    
raise
            
else
:
                
path
=
os
.
path
.
realpath
(
path
)
                
break
        
else
:
            
path
=
os
.
path
.
realpath
(
                
tempfile
.
mkdtemp
(
prefix
=
"
pip
-
{
}
-
"
.
format
(
kind
)
)
            
)
        
logger
.
debug
(
"
Created
temporary
directory
:
{
}
"
.
format
(
path
)
)
        
return
path
