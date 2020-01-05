from
__future__
import
absolute_import
print_function
unicode_literals
class
TransformConfig
(
object
)
:
    
"
"
"
A
container
for
configuration
affecting
transforms
.
The
config
    
argument
to
transforms
is
an
instance
of
this
class
possibly
with
    
additional
kind
-
specific
attributes
beyond
those
set
here
.
"
"
"
    
def
__init__
(
self
kind
path
config
params
)
:
        
self
.
kind
=
kind
        
self
.
path
=
path
        
self
.
config
=
config
        
self
.
params
=
params
class
TransformSequence
(
object
)
:
    
"
"
"
    
Container
for
a
sequence
of
transforms
.
Each
transform
is
represented
as
a
    
callable
taking
(
config
items
)
and
returning
a
generator
which
will
yield
    
transformed
items
.
The
resulting
sequence
has
the
same
interface
.
    
This
is
convenient
to
use
in
a
file
full
of
transforms
as
it
provides
a
    
decorator
transforms
.
add
that
will
add
the
decorated
function
to
the
    
sequence
.
    
"
"
"
    
def
__init__
(
self
transforms
=
None
)
:
        
self
.
transforms
=
transforms
or
[
]
    
def
__call__
(
self
config
items
)
:
        
for
xform
in
self
.
transforms
:
            
items
=
xform
(
config
items
)
            
if
items
is
None
:
                
raise
Exception
(
"
Transform
{
}
is
not
a
generator
"
.
format
(
xform
)
)
        
return
items
    
def
__repr__
(
self
)
:
        
return
'
\
n
'
.
join
(
            
[
'
TransformSequence
(
[
'
]
+
            
[
repr
(
x
)
for
x
in
self
.
transforms
]
+
            
[
'
]
)
'
]
)
    
def
add
(
self
func
)
:
        
self
.
transforms
.
append
(
func
)
        
return
func
