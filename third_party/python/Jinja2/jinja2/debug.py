import
sys
from
types
import
CodeType
from
.
import
TemplateSyntaxError
from
.
_compat
import
PYPY
from
.
utils
import
internal_code
from
.
utils
import
missing
def
rewrite_traceback_stack
(
source
=
None
)
:
    
"
"
"
Rewrite
the
current
exception
to
replace
any
tracebacks
from
    
within
compiled
template
code
with
tracebacks
that
look
like
they
    
came
from
the
template
source
.
    
This
must
be
called
within
an
except
block
.
    
:
param
exc_info
:
A
:
meth
:
sys
.
exc_info
tuple
.
If
not
provided
        
the
current
exc_info
is
used
.
    
:
param
source
:
For
TemplateSyntaxError
the
original
source
if
        
known
.
    
:
return
:
A
:
meth
:
sys
.
exc_info
tuple
that
can
be
re
-
raised
.
    
"
"
"
    
exc_type
exc_value
tb
=
sys
.
exc_info
(
)
    
if
isinstance
(
exc_value
TemplateSyntaxError
)
and
not
exc_value
.
translated
:
        
exc_value
.
translated
=
True
        
exc_value
.
source
=
source
        
try
:
            
exc_value
.
with_traceback
(
None
)
        
except
AttributeError
:
            
pass
        
tb
=
fake_traceback
(
            
exc_value
None
exc_value
.
filename
or
"
<
unknown
>
"
exc_value
.
lineno
        
)
    
else
:
        
tb
=
tb
.
tb_next
    
stack
=
[
]
    
while
tb
is
not
None
:
        
if
tb
.
tb_frame
.
f_code
in
internal_code
:
            
tb
=
tb
.
tb_next
            
continue
        
template
=
tb
.
tb_frame
.
f_globals
.
get
(
"
__jinja_template__
"
)
        
if
template
is
not
None
:
            
lineno
=
template
.
get_corresponding_lineno
(
tb
.
tb_lineno
)
            
fake_tb
=
fake_traceback
(
exc_value
tb
template
.
filename
lineno
)
            
stack
.
append
(
fake_tb
)
        
else
:
            
stack
.
append
(
tb
)
        
tb
=
tb
.
tb_next
    
tb_next
=
None
    
for
tb
in
reversed
(
stack
)
:
        
tb_next
=
tb_set_next
(
tb
tb_next
)
    
return
exc_type
exc_value
tb_next
def
fake_traceback
(
exc_value
tb
filename
lineno
)
:
    
"
"
"
Produce
a
new
traceback
object
that
looks
like
it
came
from
the
    
template
source
instead
of
the
compiled
code
.
The
filename
line
    
number
and
location
name
will
point
to
the
template
and
the
local
    
variables
will
be
the
current
template
context
.
    
:
param
exc_value
:
The
original
exception
to
be
re
-
raised
to
create
        
the
new
traceback
.
    
:
param
tb
:
The
original
traceback
to
get
the
local
variables
and
        
code
info
from
.
    
:
param
filename
:
The
template
filename
.
    
:
param
lineno
:
The
line
number
in
the
template
source
.
    
"
"
"
    
if
tb
is
not
None
:
        
locals
=
get_template_locals
(
tb
.
tb_frame
.
f_locals
)
        
locals
.
pop
(
"
__jinja_exception__
"
None
)
    
else
:
        
locals
=
{
}
    
globals
=
{
        
"
__name__
"
:
filename
        
"
__file__
"
:
filename
        
"
__jinja_exception__
"
:
exc_value
    
}
    
code
=
compile
(
"
\
n
"
*
(
lineno
-
1
)
+
"
raise
__jinja_exception__
"
filename
"
exec
"
)
    
try
:
        
location
=
"
template
"
        
if
tb
is
not
None
:
            
function
=
tb
.
tb_frame
.
f_code
.
co_name
            
if
function
=
=
"
root
"
:
                
location
=
"
top
-
level
template
code
"
            
elif
function
.
startswith
(
"
block_
"
)
:
                
location
=
'
block
"
%
s
"
'
%
function
[
6
:
]
        
code_args
=
[
]
        
for
attr
in
(
            
"
argcount
"
            
"
posonlyargcount
"
            
"
kwonlyargcount
"
            
"
nlocals
"
            
"
stacksize
"
            
"
flags
"
            
"
code
"
            
"
consts
"
            
"
names
"
            
"
varnames
"
            
(
"
filename
"
filename
)
            
(
"
name
"
location
)
            
"
firstlineno
"
            
"
lnotab
"
            
"
freevars
"
            
"
cellvars
"
        
)
:
            
if
isinstance
(
attr
tuple
)
:
                
code_args
.
append
(
attr
[
1
]
)
                
continue
            
try
:
                
code_args
.
append
(
getattr
(
code
"
co_
"
+
attr
)
)
            
except
AttributeError
:
                
continue
        
code
=
CodeType
(
*
code_args
)
    
except
Exception
:
        
pass
    
try
:
        
exec
(
code
globals
locals
)
    
except
BaseException
:
        
return
sys
.
exc_info
(
)
[
2
]
.
tb_next
def
get_template_locals
(
real_locals
)
:
    
"
"
"
Based
on
the
runtime
locals
get
the
context
that
would
be
    
available
at
that
point
in
the
template
.
    
"
"
"
    
ctx
=
real_locals
.
get
(
"
context
"
)
    
if
ctx
:
        
data
=
ctx
.
get_all
(
)
.
copy
(
)
    
else
:
        
data
=
{
}
    
local_overrides
=
{
}
    
for
name
value
in
real_locals
.
items
(
)
:
        
if
not
name
.
startswith
(
"
l_
"
)
or
value
is
missing
:
            
continue
        
try
:
            
_
depth
name
=
name
.
split
(
"
_
"
2
)
            
depth
=
int
(
depth
)
        
except
ValueError
:
            
continue
        
cur_depth
=
local_overrides
.
get
(
name
(
-
1
)
)
[
0
]
        
if
cur_depth
<
depth
:
            
local_overrides
[
name
]
=
(
depth
value
)
    
for
name
(
_
value
)
in
local_overrides
.
items
(
)
:
        
if
value
is
missing
:
            
data
.
pop
(
name
None
)
        
else
:
            
data
[
name
]
=
value
    
return
data
if
sys
.
version_info
>
=
(
3
7
)
:
    
def
tb_set_next
(
tb
tb_next
)
:
        
tb
.
tb_next
=
tb_next
        
return
tb
elif
PYPY
:
    
try
:
        
import
tputil
    
except
ImportError
:
        
def
tb_set_next
(
tb
tb_next
)
:
            
return
tb
    
else
:
        
def
tb_set_next
(
tb
tb_next
)
:
            
def
controller
(
op
)
:
                
if
op
.
opname
=
=
"
__getattribute__
"
and
op
.
args
[
0
]
=
=
"
tb_next
"
:
                    
return
tb_next
                
return
op
.
delegate
(
)
            
return
tputil
.
make_proxy
(
controller
obj
=
tb
)
else
:
    
import
ctypes
    
class
_CTraceback
(
ctypes
.
Structure
)
:
        
_fields_
=
[
            
(
"
PyObject_HEAD
"
ctypes
.
c_byte
*
object
(
)
.
__sizeof__
(
)
)
            
(
"
tb_next
"
ctypes
.
py_object
)
        
]
    
def
tb_set_next
(
tb
tb_next
)
:
        
c_tb
=
_CTraceback
.
from_address
(
id
(
tb
)
)
        
if
tb
.
tb_next
is
not
None
:
            
c_tb_next
=
ctypes
.
py_object
(
tb
.
tb_next
)
            
c_tb
.
tb_next
=
ctypes
.
py_object
(
)
            
ctypes
.
pythonapi
.
Py_DecRef
(
c_tb_next
)
        
if
tb_next
is
not
None
:
            
c_tb_next
=
ctypes
.
py_object
(
tb_next
)
            
ctypes
.
pythonapi
.
Py_IncRef
(
c_tb_next
)
            
c_tb
.
tb_next
=
c_tb_next
        
return
tb
