#
coding
:
utf
-
8
from
__future__
import
(
absolute_import
division
print_function
                        
unicode_literals
)
import
sys
from
collections
import
deque
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
throw
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
type
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
type
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
        
if
not
self
.
_exit_callbacks
:
            
return
        
def
_invoke_next_callback
(
exc_details
)
:
            
cb
=
self
.
_exit_callbacks
.
popleft
(
)
            
if
not
self
.
_exit_callbacks
:
                
return
cb
(
*
exc_details
)
            
try
:
                
suppress_exc
=
_invoke_next_callback
(
exc_details
)
            
except
:
                
suppress_exc
=
cb
(
*
sys
.
exc_info
(
)
)
                
if
not
suppress_exc
:
                    
raise
            
else
:
                
if
suppress_exc
:
                    
exc_details
=
(
None
None
None
)
                
suppress_exc
=
cb
(
*
exc_details
)
or
suppress_exc
            
return
suppress_exc
        
return
_invoke_next_callback
(
exc_details
)
