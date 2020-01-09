"
"
"
Classes
for
describing
settings
and
groups
of
settings
.
"
"
"
from
__future__
import
absolute_import
from
collections
import
OrderedDict
from
.
predicates
import
Predicate
try
:
    
from
typing
import
Tuple
Set
List
Dict
Any
Union
TYPE_CHECKING
    
BoolOrPresetOrDict
=
Union
[
'
BoolSetting
'
'
Preset
'
Dict
[
'
Setting
'
Any
]
]
    
if
TYPE_CHECKING
:
        
from
.
predicates
import
PredLeaf
PredNode
PredKey
except
ImportError
:
    
pass
class
Setting
(
object
)
:
    
"
"
"
    
A
named
setting
variable
that
can
be
configured
externally
to
Cranelift
.
    
Settings
are
normally
not
named
when
they
are
created
.
They
get
their
name
    
from
the
extract_names
method
.
    
"
"
"
    
def
__init__
(
self
doc
)
:
        
self
.
name
=
None
        
self
.
__doc__
=
doc
        
self
.
byte_offset
=
None
        
self
.
descriptor_index
=
None
        
self
.
group
=
SettingGroup
.
append
(
self
)
    
def
__str__
(
self
)
:
        
return
'
{
}
.
{
}
'
.
format
(
self
.
group
.
name
self
.
name
)
    
def
default_byte
(
self
)
:
        
raise
NotImplementedError
(
"
default_byte
is
an
abstract
method
"
)
    
def
byte_for_value
(
self
value
)
:
        
"
"
"
Get
the
setting
byte
value
that
corresponds
to
value
"
"
"
        
raise
NotImplementedError
(
"
byte_for_value
is
an
abstract
method
"
)
    
def
byte_mask
(
self
)
:
        
"
"
"
Get
a
mask
of
bits
in
our
byte
that
are
relevant
to
this
setting
.
"
"
"
        
return
0xff
class
BoolSetting
(
Setting
)
:
    
"
"
"
    
A
named
setting
with
a
boolean
on
/
off
value
.
    
:
param
doc
:
Documentation
string
.
    
:
param
default
:
The
default
value
of
this
setting
.
    
"
"
"
    
def
__init__
(
self
doc
default
=
False
)
:
        
super
(
BoolSetting
self
)
.
__init__
(
doc
)
        
self
.
default
=
default
        
self
.
bit_offset
=
None
    
def
default_byte
(
self
)
:
        
"
"
"
        
Get
the
default
value
of
this
setting
as
a
byte
that
can
be
bitwise
        
or
'
ed
with
the
other
booleans
sharing
the
same
byte
.
        
"
"
"
        
if
self
.
default
:
            
return
1
<
<
self
.
bit_offset
        
else
:
            
return
0
    
def
byte_for_value
(
self
value
)
:
        
if
value
:
            
return
1
<
<
self
.
bit_offset
        
else
:
            
return
0
    
def
byte_mask
(
self
)
:
        
return
1
<
<
self
.
bit_offset
    
def
predicate_context
(
self
)
:
        
"
"
"
        
Return
the
context
where
this
setting
can
be
evaluated
as
a
(
leaf
)
        
predicate
.
        
"
"
"
        
return
self
.
group
    
def
predicate_key
(
self
)
:
        
assert
self
.
name
"
Can
'
t
compute
key
before
setting
is
named
"
        
return
(
'
setting
'
self
.
group
.
name
self
.
name
)
    
def
predicate_leafs
(
self
leafs
)
:
        
leafs
.
add
(
self
)
    
def
rust_predicate
(
self
prec
)
:
        
"
"
"
        
Return
the
Rust
code
to
compute
the
value
of
this
setting
.
        
The
emitted
code
assumes
that
the
setting
group
exists
as
a
local
        
variable
.
        
"
"
"
        
return
'
{
}
.
{
}
(
)
'
.
format
(
self
.
group
.
name
self
.
name
)
class
NumSetting
(
Setting
)
:
    
"
"
"
    
A
named
setting
with
an
integral
value
in
the
range
0
-
-
255
.
    
:
param
doc
:
Documentation
string
.
    
:
param
default
:
The
default
value
of
this
setting
.
    
"
"
"
    
def
__init__
(
self
doc
default
=
0
)
:
        
super
(
NumSetting
self
)
.
__init__
(
doc
)
        
assert
default
=
=
int
(
default
)
        
assert
default
>
=
0
and
default
<
=
255
        
self
.
default
=
default
    
def
default_byte
(
self
)
:
        
return
self
.
default
    
def
byte_for_value
(
self
value
)
:
        
assert
isinstance
(
value
int
)
"
NumSetting
must
be
set
to
an
int
"
        
assert
value
>
=
0
and
value
<
=
255
        
return
value
class
EnumSetting
(
Setting
)
:
    
"
"
"
    
A
named
setting
with
an
enumerated
set
of
possible
values
.
    
The
default
value
is
always
the
first
enumerator
.
    
:
param
doc
:
Documentation
string
.
    
:
param
args
:
Tuple
of
unique
strings
representing
the
possible
values
.
    
"
"
"
    
def
__init__
(
self
doc
*
args
)
:
        
super
(
EnumSetting
self
)
.
__init__
(
doc
)
        
assert
len
(
args
)
>
0
"
EnumSetting
must
have
at
least
one
value
"
        
self
.
values
=
tuple
(
str
(
x
)
for
x
in
args
)
        
self
.
default
=
self
.
values
[
0
]
    
def
default_byte
(
self
)
:
        
return
0
    
def
byte_for_value
(
self
value
)
:
        
return
self
.
values
.
index
(
value
)
class
SettingGroup
(
object
)
:
    
"
"
"
    
A
group
of
settings
.
    
Whenever
a
:
class
:
Setting
object
is
created
it
is
added
to
the
currently
    
open
group
.
A
setting
group
must
be
closed
explicitly
before
another
can
be
    
opened
.
    
:
param
name
:
Short
mnemonic
name
for
setting
group
.
    
:
param
parent
:
Parent
settings
group
.
    
"
"
"
    
_current
=
None
    
def
__init__
(
self
name
parent
=
None
)
:
        
self
.
name
=
name
        
self
.
parent
=
parent
        
self
.
settings
=
[
]
        
self
.
named_predicates
=
OrderedDict
(
)
        
self
.
predicate_number
=
OrderedDict
(
)
        
self
.
presets
=
[
]
        
self
.
qual_mod
=
None
        
self
.
open
(
)
    
def
open
(
self
)
:
        
"
"
"
        
Open
this
setting
group
such
that
future
new
settings
are
added
to
this
        
group
.
        
"
"
"
        
assert
SettingGroup
.
_current
is
None
(
                
"
Can
'
t
open
{
}
since
{
}
is
already
open
"
                
.
format
(
self
SettingGroup
.
_current
)
)
        
SettingGroup
.
_current
=
self
    
def
close
(
self
globs
=
None
)
:
        
"
"
"
        
Close
this
setting
group
.
This
function
must
be
called
before
opening
        
another
setting
group
.
        
:
param
globs
:
Pass
in
globals
(
)
to
run
extract_names
on
all
            
settings
defined
in
the
module
.
        
"
"
"
        
assert
SettingGroup
.
_current
is
self
(
                
"
Can
'
t
close
{
}
the
open
setting
group
is
{
}
"
                
.
format
(
self
SettingGroup
.
_current
)
)
        
SettingGroup
.
_current
=
None
        
if
globs
:
            
named_predicates
=
[
]
            
for
name
obj
in
globs
.
items
(
)
:
                
if
isinstance
(
obj
Setting
)
:
                    
assert
obj
.
name
is
None
obj
.
name
                    
obj
.
name
=
name
                
if
isinstance
(
obj
Predicate
)
:
                    
named_predicates
.
append
(
(
name
obj
)
)
                
if
isinstance
(
obj
Preset
)
:
                    
assert
obj
.
name
is
None
obj
.
name
                    
obj
.
name
=
name
            
named_predicates
.
sort
(
key
=
lambda
x
:
x
[
0
]
)
            
for
(
name
obj
)
in
named_predicates
:
                
self
.
named_predicates
[
name
]
=
obj
        
self
.
layout
(
)
    
staticmethod
    
def
append
(
setting
)
:
        
g
=
SettingGroup
.
_current
        
assert
g
"
Open
a
setting
group
before
defining
settings
.
"
        
g
.
settings
.
append
(
setting
)
        
return
g
    
staticmethod
    
def
append_preset
(
preset
)
:
        
g
=
SettingGroup
.
_current
        
assert
g
"
Open
a
setting
group
before
defining
presets
.
"
        
g
.
presets
.
append
(
preset
)
        
return
g
    
def
number_predicate
(
self
pred
)
:
        
"
"
"
        
Make
sure
that
pred
has
an
assigned
number
and
will
be
included
in
        
this
group
'
s
bit
vector
.
        
The
numbered
predicates
include
:
        
-
BoolSetting
settings
that
belong
to
this
group
.
        
-
Predicate
instances
in
named_predicates
.
        
-
Predicate
instances
without
a
name
.
        
-
Settings
or
computed
predicates
that
belong
to
the
parent
group
but
          
need
to
be
accessible
by
number
in
this
group
.
        
The
numbered
predicates
are
referenced
by
the
encoding
tables
as
ISA
        
predicates
.
See
the
isap
field
on
Encoding
.
        
:
returns
:
The
assigned
predicate
number
in
this
group
.
        
"
"
"
        
if
pred
in
self
.
predicate_number
:
            
return
self
.
predicate_number
[
pred
]
        
else
:
            
number
=
len
(
self
.
predicate_number
)
            
self
.
predicate_number
[
pred
]
=
number
            
return
number
    
def
layout
(
self
)
:
        
"
"
"
        
Compute
the
layout
of
the
byte
vector
used
to
represent
this
settings
        
group
.
        
The
byte
vector
contains
the
following
entries
in
order
:
        
1
.
Byte
-
sized
settings
like
NumSetting
and
EnumSetting
.
        
2
.
BoolSetting
settings
.
        
3
.
Precomputed
named
predicates
.
        
4
.
Other
numbered
predicates
including
anonymous
predicates
and
parent
           
predicates
that
need
to
be
accessible
by
number
.
        
Set
self
.
settings_size
to
the
length
of
the
byte
vector
prefix
that
        
contains
the
settings
.
All
bytes
after
that
are
computed
not
        
configured
.
        
Set
self
.
boolean_offset
to
the
beginning
of
the
numbered
predicates
        
2
.
in
the
list
above
.
        
Assign
byte_offset
and
bit_offset
fields
in
all
settings
.
        
After
calling
this
method
no
more
settings
can
be
added
but
        
additional
predicates
can
be
made
accessible
with
number_predicate
(
)
.
        
"
"
"
        
assert
len
(
self
.
predicate_number
)
=
=
0
"
Too
late
for
layout
"
        
byte_offset
=
0
        
for
s
in
self
.
settings
:
            
if
not
isinstance
(
s
BoolSetting
)
:
                
s
.
byte_offset
=
byte_offset
                
byte_offset
+
=
1
        
self
.
boolean_offset
=
byte_offset
        
for
s
in
self
.
settings
:
            
if
isinstance
(
s
BoolSetting
)
:
                
number
=
self
.
number_predicate
(
s
)
                
s
.
byte_offset
=
byte_offset
+
number
/
/
8
                
s
.
bit_offset
=
number
%
8
        
self
.
boolean_settings
=
len
(
self
.
predicate_number
)
        
self
.
settings_size
=
self
.
byte_size
(
)
        
for
name
pred
in
self
.
named_predicates
.
items
(
)
:
            
self
.
number_predicate
(
pred
)
    
def
byte_size
(
self
)
:
        
"
"
"
        
Compute
the
number
of
bytes
required
to
hold
all
settings
and
        
precomputed
predicates
.
        
This
is
the
size
of
the
byte
-
sized
settings
plus
all
the
numbered
        
predicate
bits
rounded
up
to
a
whole
number
of
bytes
.
        
"
"
"
        
return
self
.
boolean_offset
+
(
len
(
self
.
predicate_number
)
+
7
)
/
/
8
class
Preset
(
object
)
:
    
"
"
"
    
A
collection
of
setting
values
that
are
applied
at
once
.
    
A
Preset
represents
a
shorthand
notation
for
applying
a
number
of
    
settings
at
once
.
Example
:
        
nehalem
=
Preset
(
has_sse41
has_cmov
has_avx
=
0
)
    
Enabling
the
nehalem
setting
is
equivalent
to
enabling
has_sse41
and
    
has_cmov
while
disabling
the
has_avx
setting
.
    
"
"
"
    
def
__init__
(
self
*
args
)
:
        
self
.
name
=
None
        
self
.
values
=
list
(
)
        
for
arg
in
args
:
            
if
isinstance
(
arg
Preset
)
:
                
self
.
values
.
extend
(
arg
.
values
)
            
elif
isinstance
(
arg
dict
)
:
                
self
.
values
.
extend
(
arg
.
items
(
)
)
            
else
:
                
assert
isinstance
(
arg
BoolSetting
)
                
self
.
values
.
append
(
(
arg
True
)
)
        
self
.
group
=
SettingGroup
.
append_preset
(
self
)
        
self
.
descriptor_index
=
None
    
def
layout
(
self
)
:
        
"
"
"
        
Compute
a
list
of
(
mask
byte
)
pairs
that
incorporate
all
values
in
        
this
preset
.
        
The
list
will
have
an
entry
for
each
setting
byte
in
the
settings
        
group
.
        
"
"
"
        
lst
=
[
(
0
0
)
]
*
self
.
group
.
settings_size
        
for
s
v
in
self
.
values
:
            
ofs
=
s
.
byte_offset
            
s_mask
=
s
.
byte_mask
(
)
            
s_val
=
s
.
byte_for_value
(
v
)
            
assert
(
s_val
&
~
s_mask
)
=
=
0
            
l_mask
l_val
=
lst
[
ofs
]
            
l_mask
|
=
s_mask
            
l_val
=
(
l_val
&
~
s_mask
)
|
s_val
            
lst
[
ofs
]
=
(
l_mask
l_val
)
        
return
lst
