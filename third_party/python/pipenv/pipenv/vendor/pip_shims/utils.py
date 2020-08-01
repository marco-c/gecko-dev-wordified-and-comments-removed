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
"
"
"
Shared
utility
functions
which
are
not
specific
to
any
particular
module
.
"
"
"
from
__future__
import
absolute_import
import
contextlib
import
copy
import
inspect
import
sys
from
functools
import
wraps
import
packaging
.
version
import
six
from
.
environment
import
MYPY_RUNNING
six
.
add_move
(
    
six
.
MovedAttribute
(
"
Callable
"
"
collections
"
"
collections
.
abc
"
)
)
from
six
.
moves
import
Callable
if
MYPY_RUNNING
:
    
from
types
import
ModuleType
    
from
typing
import
(
        
Any
        
Dict
        
Iterator
        
List
        
Optional
        
Sequence
        
Tuple
        
Type
        
TypeVar
        
Union
    
)
    
TShimmedPath
=
TypeVar
(
"
TShimmedPath
"
)
    
TShimmedPathCollection
=
TypeVar
(
"
TShimmedPathCollection
"
)
    
TShim
=
Union
[
TShimmedPath
TShimmedPathCollection
]
    
TShimmedFunc
=
Union
[
TShimmedPath
TShimmedPathCollection
Callable
Type
]
STRING_TYPES
=
(
str
)
if
sys
.
version_info
<
(
3
0
)
:
    
STRING_TYPES
=
STRING_TYPES
+
(
unicode
)
class
BaseMethod
(
Callable
)
:
    
def
__init__
(
self
func_base
name
*
args
*
*
kwargs
)
:
        
self
.
func
=
func_base
        
self
.
__name__
=
self
.
__qualname__
=
name
    
def
__call__
(
self
*
args
*
*
kwargs
)
:
        
return
self
.
func
(
*
args
*
*
kwargs
)
class
BaseClassMethod
(
Callable
)
:
    
def
__init__
(
self
func_base
name
*
args
*
*
kwargs
)
:
        
self
.
func
=
func_base
        
self
.
__name__
=
self
.
__qualname__
=
name
    
def
__call__
(
self
cls
*
args
*
*
kwargs
)
:
        
return
self
.
func
(
*
args
*
*
kwargs
)
def
make_method
(
fn
)
:
    
wraps
(
fn
)
    
def
method_creator
(
*
args
*
*
kwargs
)
:
        
return
BaseMethod
(
fn
*
args
*
*
kwargs
)
    
return
method_creator
def
make_classmethod
(
fn
)
:
    
wraps
(
fn
)
    
def
classmethod_creator
(
*
args
*
*
kwargs
)
:
        
return
classmethod
(
BaseClassMethod
(
fn
*
args
*
*
kwargs
)
)
    
return
classmethod_creator
def
memoize
(
obj
)
:
    
cache
=
obj
.
cache
=
{
}
    
wraps
(
obj
)
    
def
memoizer
(
*
args
*
*
kwargs
)
:
        
key
=
str
(
args
)
+
str
(
kwargs
)
        
if
key
not
in
cache
:
            
cache
[
key
]
=
obj
(
*
args
*
*
kwargs
)
        
return
cache
[
key
]
    
return
memoizer
memoize
def
_parse
(
version
)
:
    
if
isinstance
(
version
STRING_TYPES
)
:
        
return
tuple
(
(
int
(
i
)
for
i
in
version
.
split
(
"
.
"
)
)
)
    
return
version
memoize
def
parse_version
(
version
)
:
    
if
not
isinstance
(
version
STRING_TYPES
)
:
        
raise
TypeError
(
"
Can
only
derive
versions
from
string
got
{
0
!
r
}
"
.
format
(
version
)
)
    
return
packaging
.
version
.
parse
(
version
)
memoize
def
split_package
(
module
subimport
=
None
)
:
    
"
"
"
    
Used
to
determine
what
target
to
import
.
    
Either
splits
off
the
final
segment
or
uses
the
provided
sub
-
import
to
return
a
    
2
-
tuple
of
the
import
path
and
the
target
module
or
sub
-
path
.
    
:
param
str
module
:
A
package
to
import
from
    
:
param
Optional
[
str
]
subimport
:
A
class
function
or
subpackage
to
import
    
:
return
:
A
2
-
tuple
of
the
corresponding
import
package
and
sub
-
import
path
    
:
rtype
:
Tuple
[
str
str
]
    
:
Example
:
    
>
>
>
from
pip_shims
.
utils
import
split_package
    
>
>
>
split_package
(
"
pip
.
_internal
.
req
.
req_install
"
subimport
=
"
InstallRequirement
"
)
    
(
"
pip
.
_internal
.
req
.
req_install
"
"
InstallRequirement
"
)
    
>
>
>
split_package
(
"
pip
.
_internal
.
cli
.
base_command
"
)
    
(
"
pip
.
_internal
.
cli
"
"
base_command
"
)
    
"
"
"
    
package
=
None
    
if
subimport
:
        
package
=
subimport
    
else
:
        
module
_
package
=
module
.
rpartition
(
"
.
"
)
    
return
module
package
def
get_method_args
(
target_method
)
:
    
"
"
"
    
Returns
the
arguments
for
a
callable
.
    
:
param
Callable
target_method
:
A
callable
to
retrieve
arguments
for
    
:
return
:
A
2
-
tuple
of
the
original
callable
and
its
resulting
arguments
    
:
rtype
:
Tuple
[
Callable
Optional
[
inspect
.
Arguments
]
]
    
"
"
"
    
inspected_args
=
None
    
try
:
        
inspected_args
=
inspect
.
getargs
(
target_method
.
__code__
)
    
except
AttributeError
:
        
target_func
=
getattr
(
target_method
"
__func__
"
None
)
        
if
target_func
is
not
None
:
            
inspected_args
=
inspect
.
getargs
(
target_func
.
__code__
)
    
else
:
        
target_func
=
target_method
    
return
target_func
inspected_args
def
set_default_kwargs
(
basecls
method
*
args
*
*
default_kwargs
)
:
    
target_method
=
getattr
(
basecls
method
None
)
    
if
target_method
is
None
:
        
return
basecls
    
target_func
inspected_args
=
get_method_args
(
target_method
)
    
if
inspected_args
is
not
None
:
        
pos_args
=
inspected_args
.
args
    
else
:
        
pos_args
=
[
]
    
if
not
any
(
arg
in
pos_args
for
arg
in
list
(
default_kwargs
.
keys
(
)
)
)
:
        
return
basecls
    
prepended_defaults
=
tuple
(
)
    
for
arg
in
args
:
        
prepended_defaults
+
=
(
arg
)
    
for
arg
in
pos_args
:
        
if
arg
in
default_kwargs
:
            
prepended_defaults
=
prepended_defaults
+
(
default_kwargs
[
arg
]
)
    
if
not
prepended_defaults
:
        
return
basecls
    
if
six
.
PY2
and
inspect
.
ismethod
(
target_method
)
:
        
new_defaults
=
prepended_defaults
+
target_func
.
__defaults__
        
target_method
.
__func__
.
__defaults__
=
new_defaults
    
else
:
        
new_defaults
=
prepended_defaults
+
target_method
.
__defaults__
        
target_method
.
__defaults__
=
new_defaults
    
setattr
(
basecls
method
target_method
)
    
return
basecls
def
ensure_function
(
parent
funcname
func
)
:
    
"
"
"
Given
a
module
a
function
name
and
a
function
object
attaches
the
given
    
function
to
the
module
and
ensures
it
is
named
properly
according
to
the
provided
    
argument
    
:
param
Any
parent
:
The
parent
to
attack
the
function
to
    
:
param
str
funcname
:
The
name
to
give
the
function
    
:
param
Callable
func
:
The
function
to
rename
and
attach
to
*
*
parent
*
*
    
:
returns
:
The
function
with
its
name
qualname
etc
set
to
mirror
*
*
parent
*
*
    
:
rtype
:
Callable
    
"
"
"
    
qualname
=
funcname
    
if
parent
is
None
:
        
parent
=
__module__
    
parent_is_module
=
inspect
.
ismodule
(
parent
)
    
parent_is_class
=
inspect
.
isclass
(
parent
)
    
module
=
None
    
if
parent_is_module
:
        
module
=
parent
.
__name__
    
elif
parent_is_class
:
        
qualname
=
"
{
0
}
.
{
1
}
"
.
format
(
parent
.
__name__
qualname
)
        
module
=
getattr
(
parent
"
__module__
"
None
)
    
else
:
        
module
=
getattr
(
parent
"
__module__
"
None
)
    
try
:
        
func
.
__name__
=
funcname
    
except
AttributeError
:
        
if
getattr
(
func
"
__func__
"
None
)
is
not
None
:
            
func
=
func
.
__func__
        
func
.
__name__
=
funcname
    
func
.
__qualname__
=
qualname
    
func
.
__module__
=
module
    
return
func
def
add_mixin_to_class
(
basecls
mixins
)
:
    
"
"
"
    
Given
a
class
adds
the
provided
mixin
classes
as
base
classes
and
gives
a
new
class
    
:
param
Type
basecls
:
An
initial
class
to
generate
a
new
class
from
    
:
param
List
[
Type
]
mixins
:
A
list
of
mixins
to
add
as
base
classes
    
:
return
:
A
new
class
with
the
provided
mixins
as
base
classes
    
:
rtype
:
Type
[
basecls
*
mixins
]
    
"
"
"
    
if
not
any
(
mixins
)
:
        
return
basecls
    
base_dict
=
basecls
.
__dict__
.
copy
(
)
    
class_tuple
=
(
basecls
)
    
for
mixin
in
mixins
:
        
if
not
mixin
:
            
continue
        
mixin_dict
=
mixin
.
__dict__
.
copy
(
)
        
base_dict
.
update
(
mixin_dict
)
        
class_tuple
=
class_tuple
+
(
mixin
)
    
base_dict
.
update
(
basecls
.
__dict__
)
    
return
type
(
basecls
.
__name__
class_tuple
base_dict
)
def
fallback_is_file_url
(
link
)
:
    
return
link
.
url
.
lower
(
)
.
startswith
(
"
file
:
"
)
def
fallback_is_artifact
(
self
)
:
    
return
not
getattr
(
self
"
is_vcs
"
False
)
def
fallback_is_vcs
(
self
)
:
    
return
not
getattr
(
self
"
is_artifact
"
True
)
def
resolve_possible_shim
(
target
)
:
    
if
target
is
None
:
        
return
target
    
if
getattr
(
target
"
shim
"
None
)
:
        
return
target
.
shim
(
)
    
return
target
contextlib
.
contextmanager
def
nullcontext
(
*
args
*
*
kwargs
)
:
    
try
:
        
yield
    
finally
:
        
pass
def
has_property
(
target
name
)
:
    
if
getattr
(
target
name
None
)
is
not
None
:
        
return
True
    
return
False
def
apply_alias
(
imported
target
*
aliases
)
:
    
"
"
"
    
Given
a
target
with
attributes
point
non
-
existant
aliases
at
the
first
existing
one
    
:
param
Union
[
ModuleType
Type
]
imported
:
A
Module
or
Class
base
    
:
param
Any
target
:
The
target
which
is
a
member
of
*
*
imported
*
*
and
will
have
aliases
    
:
param
str
aliases
:
A
list
of
aliases
the
first
found
attribute
will
be
the
basis
        
for
all
non
-
existant
names
which
will
be
created
as
pointers
    
:
return
:
The
original
target
    
:
rtype
:
Any
    
"
"
"
    
base_value
=
None
    
applied_aliases
=
set
(
)
    
unapplied_aliases
=
set
(
)
    
for
alias
in
aliases
:
        
if
has_property
(
target
alias
)
:
            
base_value
=
getattr
(
target
alias
)
            
applied_aliases
.
add
(
alias
)
        
else
:
            
unapplied_aliases
.
add
(
alias
)
    
is_callable
=
inspect
.
ismethod
(
base_value
)
or
inspect
.
isfunction
(
base_value
)
    
for
alias
in
unapplied_aliases
:
        
if
is_callable
:
            
func_copy
=
copy
.
deepcopy
(
base_value
)
            
alias_value
=
ensure_function
(
imported
alias
func_copy
)
        
else
:
            
alias_value
=
base_value
        
setattr
(
target
alias
alias_value
)
    
return
target
def
suppress_setattr
(
obj
attr
value
filter_none
=
False
)
:
    
"
"
"
    
Set
an
attribute
suppressing
any
exceptions
and
skipping
the
attempt
on
failure
.
    
:
param
Any
obj
:
Object
to
set
the
attribute
on
    
:
param
str
attr
:
The
attribute
name
to
set
    
:
param
Any
value
:
The
value
to
set
the
attribute
to
    
:
param
bool
filter_none
:
[
description
]
defaults
to
False
    
:
return
:
Nothing
    
:
rtype
:
None
    
:
Example
:
    
>
>
>
class
MyClass
(
object
)
:
    
.
.
.
def
__init__
(
self
name
)
:
    
.
.
.
self
.
name
=
name
    
.
.
.
self
.
parent
=
None
    
.
.
.
def
__repr__
(
self
)
:
    
.
.
.
return
"
<
{
0
!
r
}
instance
(
name
=
{
1
!
r
}
parent
=
{
2
!
r
}
)
>
"
.
format
(
    
.
.
.
self
.
__class__
.
__name__
self
.
name
self
.
parent
    
.
.
.
)
    
.
.
.
def
__str__
(
self
)
:
    
.
.
.
return
self
.
name
    
>
>
>
me
=
MyClass
(
"
Dan
"
)
    
>
>
>
dad
=
MyClass
(
"
John
"
)
    
>
>
>
grandfather
=
MyClass
(
"
Joe
"
)
    
>
>
>
suppress_setattr
(
dad
"
parent
"
grandfather
)
    
>
>
>
dad
    
<
'
MyClass
'
instance
(
name
=
'
John
'
parent
=
<
'
MyClass
'
instance
(
name
=
'
Joe
'
parent
=
None
    
)
>
)
>
    
>
>
>
suppress_setattr
(
me
"
parent
"
dad
)
    
>
>
>
me
    
<
'
MyClass
'
instance
(
name
=
'
Dan
'
parent
=
<
'
MyClass
'
instance
(
name
=
'
John
'
parent
=
<
'
My
    
Class
'
instance
(
name
=
'
Joe
'
parent
=
None
)
>
)
>
)
>
    
>
>
>
suppress_setattr
(
me
"
grandparent
"
grandfather
)
    
>
>
>
me
    
<
'
MyClass
'
instance
(
name
=
'
Dan
'
parent
=
<
'
MyClass
'
instance
(
name
=
'
John
'
parent
=
<
'
My
    
Class
'
instance
(
name
=
'
Joe
'
parent
=
None
)
>
)
>
)
>
    
"
"
"
    
if
filter_none
and
value
is
None
:
        
pass
    
try
:
        
setattr
(
obj
attr
value
)
    
except
Exception
:
        
pass
def
get_allowed_args
(
fn_or_class
)
:
    
"
"
"
    
Given
a
callable
or
a
class
returns
the
arguments
and
default
kwargs
passed
in
.
    
:
param
Union
[
Callable
Type
]
fn_or_class
:
A
function
method
or
class
to
inspect
.
    
:
return
:
A
2
-
tuple
with
a
list
of
arguments
and
a
dictionary
of
keywords
mapped
to
        
default
values
.
    
:
rtype
:
Tuple
[
List
[
str
]
Dict
[
str
Any
]
]
    
"
"
"
    
try
:
        
signature
=
inspect
.
signature
(
fn_or_class
)
    
except
AttributeError
:
        
import
funcsigs
        
signature
=
funcsigs
.
signature
(
fn_or_class
)
    
args
=
[
]
    
kwargs
=
{
}
    
for
arg
param
in
signature
.
parameters
.
items
(
)
:
        
if
(
            
param
.
kind
in
(
param
.
POSITIONAL_OR_KEYWORD
param
.
POSITIONAL_ONLY
)
        
)
and
param
.
default
is
param
.
empty
:
            
args
.
append
(
arg
)
        
else
:
            
kwargs
[
arg
]
=
param
.
default
if
param
.
default
is
not
param
.
empty
else
None
    
return
args
kwargs
def
call_function_with_correct_args
(
fn
*
*
provided_kwargs
)
:
    
"
"
"
    
Determines
which
arguments
from
*
*
provided_kwargs
*
*
to
call
*
*
fn
*
*
and
calls
it
.
    
Consumes
a
list
of
allowed
arguments
(
e
.
g
.
from
:
func
:
~
inspect
.
getargs
(
)
)
and
    
uses
it
to
determine
which
of
the
arguments
in
the
provided
kwargs
should
be
passed
    
through
to
the
given
callable
.
    
:
param
Callable
fn
:
A
callable
which
has
some
dynamic
arguments
    
:
param
List
[
str
]
allowed_args
:
A
list
of
allowed
arguments
which
can
be
passed
to
        
the
supplied
function
    
:
return
:
The
result
of
calling
the
function
    
:
rtype
:
Any
    
"
"
"
    
args
=
[
]
    
kwargs
=
{
}
    
func_args
func_kwargs
=
get_allowed_args
(
fn
)
    
for
arg
in
func_args
:
        
args
.
append
(
provided_kwargs
[
arg
]
)
    
for
arg
in
func_kwargs
:
        
if
not
provided_kwargs
.
get
(
arg
)
:
            
continue
        
kwargs
[
arg
]
=
provided_kwargs
[
arg
]
    
return
fn
(
*
args
*
*
kwargs
)
def
filter_allowed_args
(
fn
*
*
provided_kwargs
)
:
    
"
"
"
    
Given
a
function
and
a
kwarg
mapping
return
only
those
kwargs
used
in
the
function
.
    
:
param
Callable
fn
:
A
function
to
inspect
    
:
param
Dict
[
str
Any
]
kwargs
:
A
mapping
of
kwargs
to
filter
    
:
return
:
A
new
filtered
kwarg
mapping
    
:
rtype
:
Tuple
[
List
[
Any
]
Dict
[
str
Any
]
]
    
"
"
"
    
args
=
[
]
    
kwargs
=
{
}
    
func_args
func_kwargs
=
get_allowed_args
(
fn
)
    
for
arg
in
func_args
:
        
if
arg
in
provided_kwargs
:
            
args
.
append
(
provided_kwargs
[
arg
]
)
    
for
arg
in
func_kwargs
:
        
if
arg
not
in
provided_kwargs
:
            
continue
        
kwargs
[
arg
]
=
provided_kwargs
[
arg
]
    
return
args
kwargs
