"
"
"
contextlib2
-
backports
and
enhancements
to
the
contextlib
module
"
"
"
import
abc
import
sys
import
warnings
from
collections
import
deque
from
functools
import
wraps
__all__
=
[
"
contextmanager
"
"
closing
"
"
nullcontext
"
           
"
AbstractContextManager
"
           
"
ContextDecorator
"
"
ExitStack
"
           
"
redirect_stdout
"
"
redirect_stderr
"
"
suppress
"
]
__all__
+
=
[
"
ContextStack
"
]
if
sys
.
version_info
[
:
2
]
>
=
(
3
4
)
:
    
_abc_ABC
=
abc
.
ABC
else
:
    
_abc_ABC
=
abc
.
ABCMeta
(
'
ABC
'
(
object
)
{
'
__slots__
'
:
(
)
}
)
def
_classic_mro
(
C
result
)
:
    
if
C
in
result
:
        
return
    
result
.
append
(
C
)
    
for
B
in
C
.
__bases__
:
        
_classic_mro
(
B
result
)
    
return
result
def
_check_methods
(
C
*
methods
)
:
    
try
:
        
mro
=
C
.
__mro__
    
except
AttributeError
:
        
mro
=
tuple
(
_classic_mro
(
C
[
]
)
)
    
for
method
in
methods
:
        
for
B
in
mro
:
            
if
method
in
B
.
__dict__
:
                
if
B
.
__dict__
[
method
]
is
None
:
                    
return
NotImplemented
                
break
        
else
:
            
return
NotImplemented
    
return
True
class
AbstractContextManager
(
_abc_ABC
)
:
    
"
"
"
An
abstract
base
class
for
context
managers
.
"
"
"
    
def
__enter__
(
self
)
:
        
"
"
"
Return
self
upon
entering
the
runtime
context
.
"
"
"
        
return
self
    
abc
.
abstractmethod
    
def
__exit__
(
self
exc_type
exc_value
traceback
)
:
        
"
"
"
Raise
any
exception
triggered
within
the
runtime
context
.
"
"
"
        
return
None
    
classmethod
    
def
__subclasshook__
(
cls
C
)
:
        
"
"
"
Check
whether
subclass
is
considered
a
subclass
of
this
ABC
.
"
"
"
        
if
cls
is
AbstractContextManager
:
            
return
_check_methods
(
C
"
__enter__
"
"
__exit__
"
)
        
return
NotImplemented
class
ContextDecorator
(
object
)
:
    
"
"
"
A
base
class
or
mixin
that
enables
context
managers
to
work
as
decorators
.
"
"
"
    
def
refresh_cm
(
self
)
:
        
"
"
"
Returns
the
context
manager
used
to
actually
wrap
the
call
to
the
        
decorated
function
.
        
The
default
implementation
just
returns
*
self
*
.
        
Overriding
this
method
allows
otherwise
one
-
shot
context
managers
        
like
_GeneratorContextManager
to
support
use
as
decorators
via
        
implicit
recreation
.
        
DEPRECATED
:
refresh_cm
was
never
added
to
the
standard
library
'
s
                    
ContextDecorator
API
        
"
"
"
        
warnings
.
warn
(
"
refresh_cm
was
never
added
to
the
standard
library
"
                      
DeprecationWarning
)
        
return
self
.
_recreate_cm
(
)
    
def
_recreate_cm
(
self
)
:
        
"
"
"
Return
a
recreated
instance
of
self
.
        
Allows
an
otherwise
one
-
shot
context
manager
like
        
_GeneratorContextManager
to
support
use
as
        
a
decorator
via
implicit
recreation
.
        
This
is
a
private
interface
just
for
_GeneratorContextManager
.
        
See
issue
#
11647
for
details
.
        
"
"
"
        
return
self
    
def
__call__
(
self
func
)
:
        
wraps
(
func
)
        
def
inner
(
*
args
*
*
kwds
)
:
            
with
self
.
_recreate_cm
(
)
:
                
return
func
(
*
args
*
*
kwds
)
        
return
inner
class
_GeneratorContextManager
(
ContextDecorator
)
:
    
"
"
"
Helper
for
contextmanager
decorator
.
"
"
"
    
def
__init__
(
self
func
args
kwds
)
:
        
self
.
gen
=
func
(
*
args
*
*
kwds
)
        
self
.
func
self
.
args
self
.
kwds
=
func
args
kwds
        
doc
=
getattr
(
func
"
__doc__
"
None
)
        
if
doc
is
None
:
            
doc
=
type
(
self
)
.
__doc__
        
self
.
__doc__
=
doc
    
def
_recreate_cm
(
self
)
:
        
return
self
.
__class__
(
self
.
func
self
.
args
self
.
kwds
)
    
def
__enter__
(
self
)
:
        
try
:
            
return
next
(
self
.
gen
)
        
except
StopIteration
:
            
raise
RuntimeError
(
"
generator
didn
'
t
yield
"
)
    
def
__exit__
(
self
type
value
traceback
)
:
        
if
type
is
None
:
            
try
:
                
next
(
self
.
gen
)
            
except
StopIteration
:
                
return
            
else
:
                
raise
RuntimeError
(
"
generator
didn
'
t
stop
"
)
        
else
:
            
if
value
is
None
:
                
value
=
type
(
)
            
try
:
                
self
.
gen
.
throw
(
type
value
traceback
)
                
raise
RuntimeError
(
"
generator
didn
'
t
stop
after
throw
(
)
"
)
            
except
StopIteration
as
exc
:
                
return
exc
is
not
value
            
except
RuntimeError
as
exc
:
                
if
exc
is
value
:
                    
return
False
                
if
_HAVE_EXCEPTION_CHAINING
and
exc
.
__cause__
is
value
:
                    
return
False
                
raise
            
except
:
                
if
sys
.
exc_info
(
)
[
1
]
is
not
value
:
                    
raise
def
contextmanager
(
func
)
:
    
"
"
"
contextmanager
decorator
.
    
Typical
usage
:
        
contextmanager
        
def
some_generator
(
<
arguments
>
)
:
            
<
setup
>
            
try
:
                
yield
<
value
>
            
finally
:
                
<
cleanup
>
    
This
makes
this
:
        
with
some_generator
(
<
arguments
>
)
as
<
variable
>
:
            
<
body
>
    
equivalent
to
this
:
        
<
setup
>
        
try
:
            
<
variable
>
=
<
value
>
            
<
body
>
        
finally
:
            
<
cleanup
>
    
"
"
"
    
wraps
(
func
)
    
def
helper
(
*
args
*
*
kwds
)
:
        
return
_GeneratorContextManager
(
func
args
kwds
)
    
return
helper
class
closing
(
object
)
:
    
"
"
"
Context
to
automatically
close
something
at
the
end
of
a
block
.
    
Code
like
this
:
        
with
closing
(
<
module
>
.
open
(
<
arguments
>
)
)
as
f
:
            
<
block
>
    
is
equivalent
to
this
:
        
f
=
<
module
>
.
open
(
<
arguments
>
)
        
try
:
            
<
block
>
        
finally
:
            
f
.
close
(
)
    
"
"
"
    
def
__init__
(
self
thing
)
:
        
self
.
thing
=
thing
    
def
__enter__
(
self
)
:
        
return
self
.
thing
    
def
__exit__
(
self
*
exc_info
)
:
        
self
.
thing
.
close
(
)
class
_RedirectStream
(
object
)
:
    
_stream
=
None
    
def
__init__
(
self
new_target
)
:
        
self
.
_new_target
=
new_target
        
self
.
_old_targets
=
[
]
    
def
__enter__
(
self
)
:
        
self
.
_old_targets
.
append
(
getattr
(
sys
self
.
_stream
)
)
        
setattr
(
sys
self
.
_stream
self
.
_new_target
)
        
return
self
.
_new_target
    
def
__exit__
(
self
exctype
excinst
exctb
)
:
        
setattr
(
sys
self
.
_stream
self
.
_old_targets
.
pop
(
)
)
class
redirect_stdout
(
_RedirectStream
)
:
    
"
"
"
Context
manager
for
temporarily
redirecting
stdout
to
another
file
.
        
#
How
to
send
help
(
)
to
stderr
        
with
redirect_stdout
(
sys
.
stderr
)
:
            
help
(
dir
)
        
#
How
to
write
help
(
)
to
a
file
        
with
open
(
'
help
.
txt
'
'
w
'
)
as
f
:
            
with
redirect_stdout
(
f
)
:
                
help
(
pow
)
    
"
"
"
    
_stream
=
"
stdout
"
class
redirect_stderr
(
_RedirectStream
)
:
    
"
"
"
Context
manager
for
temporarily
redirecting
stderr
to
another
file
.
"
"
"
    
_stream
=
"
stderr
"
class
suppress
(
object
)
:
    
"
"
"
Context
manager
to
suppress
specified
exceptions
    
After
the
exception
is
suppressed
execution
proceeds
with
the
next
    
statement
following
the
with
statement
.
         
with
suppress
(
FileNotFoundError
)
:
             
os
.
remove
(
somefile
)
         
#
Execution
still
resumes
here
if
the
file
was
already
removed
    
"
"
"
    
def
__init__
(
self
*
exceptions
)
:
        
self
.
_exceptions
=
exceptions
    
def
__enter__
(
self
)
:
        
pass
    
def
__exit__
(
self
exctype
excinst
exctb
)
:
        
return
exctype
is
not
None
and
issubclass
(
exctype
self
.
_exceptions
)
_HAVE_EXCEPTION_CHAINING
=
sys
.
version_info
[
0
]
>
=
3
if
_HAVE_EXCEPTION_CHAINING
:
    
def
_make_context_fixer
(
frame_exc
)
:
        
def
_fix_exception_context
(
new_exc
old_exc
)
:
            
while
1
:
                
exc_context
=
new_exc
.
__context__
                
if
exc_context
is
old_exc
:
                    
return
                
if
exc_context
is
None
or
exc_context
is
frame_exc
:
                    
break
                
new_exc
=
exc_context
            
new_exc
.
__context__
=
old_exc
        
return
_fix_exception_context
    
def
_reraise_with_existing_context
(
exc_details
)
:
        
try
:
            
fixed_ctx
=
exc_details
[
1
]
.
__context__
            
raise
exc_details
[
1
]
        
except
BaseException
:
            
exc_details
[
1
]
.
__context__
=
fixed_ctx
            
raise
else
:
    
def
_make_context_fixer
(
frame_exc
)
:
        
return
lambda
new_exc
old_exc
:
None
    
def
_reraise_with_existing_context
(
exc_details
)
:
        
exc_type
exc_value
exc_tb
=
exc_details
        
exec
(
"
raise
exc_type
exc_value
exc_tb
"
)
try
:
    
from
types
import
InstanceType
except
ImportError
:
    
_get_type
=
type
else
:
    
def
_get_type
(
obj
)
:
        
obj_type
=
type
(
obj
)
        
if
obj_type
is
InstanceType
:
            
return
obj
.
__class__
        
return
obj_type
class
ExitStack
(
object
)
:
    
"
"
"
Context
manager
for
dynamic
management
of
a
stack
of
exit
callbacks
    
For
example
:
        
with
ExitStack
(
)
as
stack
:
            
files
=
[
stack
.
enter_context
(
open
(
fname
)
)
for
fname
in
filenames
]
            
#
All
opened
files
will
automatically
be
closed
at
the
end
of
            
#
the
with
statement
even
if
attempts
to
open
files
later
            
#
in
the
list
raise
an
exception
    
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
_exit_callbacks
=
deque
(
)
    
def
pop_all
(
self
)
:
        
"
"
"
Preserve
the
context
stack
by
transferring
it
to
a
new
instance
"
"
"
        
new_stack
=
type
(
self
)
(
)
        
new_stack
.
_exit_callbacks
=
self
.
_exit_callbacks
        
self
.
_exit_callbacks
=
deque
(
)
        
return
new_stack
    
def
_push_cm_exit
(
self
cm
cm_exit
)
:
        
"
"
"
Helper
to
correctly
register
callbacks
to
__exit__
methods
"
"
"
        
def
_exit_wrapper
(
*
exc_details
)
:
            
return
cm_exit
(
cm
*
exc_details
)
        
_exit_wrapper
.
__self__
=
cm
        
self
.
push
(
_exit_wrapper
)
    
def
push
(
self
exit
)
:
        
"
"
"
Registers
a
callback
with
the
standard
__exit__
method
signature
        
Can
suppress
exceptions
the
same
way
__exit__
methods
can
.
        
Also
accepts
any
object
with
an
__exit__
method
(
registering
a
call
        
to
the
method
instead
of
the
object
itself
)
        
"
"
"
        
_cb_type
=
_get_type
(
exit
)
        
try
:
            
exit_method
=
_cb_type
.
__exit__
        
except
AttributeError
:
            
self
.
_exit_callbacks
.
append
(
exit
)
        
else
:
            
self
.
_push_cm_exit
(
exit
exit_method
)
        
return
exit
    
def
callback
(
self
callback
*
args
*
*
kwds
)
:
        
"
"
"
Registers
an
arbitrary
callback
and
arguments
.
        
Cannot
suppress
exceptions
.
        
"
"
"
        
def
_exit_wrapper
(
exc_type
exc
tb
)
:
            
callback
(
*
args
*
*
kwds
)
        
_exit_wrapper
.
__wrapped__
=
callback
        
self
.
push
(
_exit_wrapper
)
        
return
callback
    
def
enter_context
(
self
cm
)
:
        
"
"
"
Enters
the
supplied
context
manager
        
If
successful
also
pushes
its
__exit__
method
as
a
callback
and
        
returns
the
result
of
the
__enter__
method
.
        
"
"
"
        
_cm_type
=
_get_type
(
cm
)
        
_exit
=
_cm_type
.
__exit__
        
result
=
_cm_type
.
__enter__
(
cm
)
        
self
.
_push_cm_exit
(
cm
_exit
)
        
return
result
    
def
close
(
self
)
:
        
"
"
"
Immediately
unwind
the
context
stack
"
"
"
        
self
.
__exit__
(
None
None
None
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
*
exc_details
)
:
        
received_exc
=
exc_details
[
0
]
is
not
None
        
frame_exc
=
sys
.
exc_info
(
)
[
1
]
        
_fix_exception_context
=
_make_context_fixer
(
frame_exc
)
        
suppressed_exc
=
False
        
pending_raise
=
False
        
while
self
.
_exit_callbacks
:
            
cb
=
self
.
_exit_callbacks
.
pop
(
)
            
try
:
                
if
cb
(
*
exc_details
)
:
                    
suppressed_exc
=
True
                    
pending_raise
=
False
                    
exc_details
=
(
None
None
None
)
            
except
:
                
new_exc_details
=
sys
.
exc_info
(
)
                
_fix_exception_context
(
new_exc_details
[
1
]
exc_details
[
1
]
)
                
pending_raise
=
True
                
exc_details
=
new_exc_details
        
if
pending_raise
:
            
_reraise_with_existing_context
(
exc_details
)
        
return
received_exc
and
suppressed_exc
class
ContextStack
(
ExitStack
)
:
    
"
"
"
Backwards
compatibility
alias
for
ExitStack
"
"
"
    
def
__init__
(
self
)
:
        
warnings
.
warn
(
"
ContextStack
has
been
renamed
to
ExitStack
"
                      
DeprecationWarning
)
        
super
(
ContextStack
self
)
.
__init__
(
)
    
def
register_exit
(
self
callback
)
:
        
return
self
.
push
(
callback
)
    
def
register
(
self
callback
*
args
*
*
kwds
)
:
        
return
self
.
callback
(
callback
*
args
*
*
kwds
)
    
def
preserve
(
self
)
:
        
return
self
.
pop_all
(
)
class
nullcontext
(
AbstractContextManager
)
:
    
"
"
"
Context
manager
that
does
no
additional
processing
.
    
Used
as
a
stand
-
in
for
a
normal
context
manager
when
a
particular
    
block
of
code
is
only
sometimes
used
with
a
normal
context
manager
:
    
cm
=
optional_cm
if
condition
else
nullcontext
(
)
    
with
cm
:
        
#
Perform
operation
using
optional_cm
if
condition
is
True
    
"
"
"
    
def
__init__
(
self
enter_result
=
None
)
:
        
self
.
enter_result
=
enter_result
    
def
__enter__
(
self
)
:
        
return
self
.
enter_result
    
def
__exit__
(
self
*
excinfo
)
:
        
pass
