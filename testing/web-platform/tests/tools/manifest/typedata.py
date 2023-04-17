from
collections
.
abc
import
MutableMapping
MYPY
=
False
if
MYPY
:
    
from
typing
import
Any
    
from
typing
import
Dict
    
from
typing
import
Iterator
    
from
typing
import
List
    
from
typing
import
Optional
    
from
typing
import
Set
    
from
typing
import
Text
    
from
typing
import
Tuple
    
from
typing
import
Type
    
from
typing
import
Union
    
from
.
import
item
    
from
.
import
manifest
if
MYPY
:
    
TypeDataType
=
MutableMapping
[
Tuple
[
Text
.
.
.
]
Set
[
item
.
ManifestItem
]
]
    
PathHashType
=
MutableMapping
[
Tuple
[
Text
.
.
.
]
Text
]
else
:
    
TypeDataType
=
MutableMapping
    
PathHashType
=
MutableMapping
class
TypeData
(
TypeDataType
)
:
    
def
__init__
(
self
m
type_cls
)
:
        
"
"
"
Dict
-
like
object
containing
the
TestItems
for
each
test
type
.
        
Loading
an
actual
Item
class
for
each
test
is
unnecessarily
        
slow
so
this
class
allows
lazy
-
loading
of
the
test
        
items
.
When
the
manifest
is
loaded
we
store
the
raw
json
        
corresponding
to
the
test
type
and
only
create
an
Item
        
subclass
when
the
test
is
accessed
.
In
order
to
remain
        
API
-
compatible
with
consumers
that
depend
on
getting
an
Item
        
from
iteration
we
do
egerly
load
all
items
when
iterating
        
over
the
class
.
"
"
"
        
self
.
_manifest
=
m
        
self
.
_type_cls
=
type_cls
        
self
.
_json_data
=
{
}
        
self
.
_data
=
{
}
        
self
.
_hashes
=
{
}
        
self
.
hashes
=
PathHash
(
self
)
    
def
_delete_node
(
self
data
key
)
:
        
"
"
"
delete
a
path
from
a
Dict
data
with
a
given
key
"
"
"
        
path
=
[
]
        
node
=
data
        
for
pathseg
in
key
[
:
-
1
]
:
            
path
.
append
(
(
node
pathseg
)
)
            
node
=
node
[
pathseg
]
            
if
not
isinstance
(
node
dict
)
:
                
raise
KeyError
(
key
)
        
del
node
[
key
[
-
1
]
]
        
while
path
:
            
node
pathseg
=
path
.
pop
(
)
            
if
len
(
node
[
pathseg
]
)
=
=
0
:
                
del
node
[
pathseg
]
            
else
:
                
break
    
def
__getitem__
(
self
key
)
:
        
node
=
self
.
_data
        
for
pathseg
in
key
:
            
if
isinstance
(
node
dict
)
and
pathseg
in
node
:
                
node
=
node
[
pathseg
]
            
else
:
                
break
        
else
:
            
if
isinstance
(
node
set
)
:
                
return
node
            
else
:
                
raise
KeyError
(
key
)
        
node
=
self
.
_json_data
        
found
=
False
        
for
pathseg
in
key
:
            
if
isinstance
(
node
dict
)
and
pathseg
in
node
:
                
node
=
node
[
pathseg
]
            
else
:
                
break
        
else
:
            
found
=
True
        
if
not
found
:
            
raise
KeyError
(
key
)
        
if
not
isinstance
(
node
list
)
:
            
raise
KeyError
(
key
)
        
self
.
_hashes
[
key
]
=
node
[
0
]
        
data
=
set
(
)
        
path
=
"
/
"
.
join
(
key
)
        
for
test
in
node
[
1
:
]
:
            
manifest_item
=
self
.
_type_cls
.
from_json
(
self
.
_manifest
path
test
)
            
data
.
add
(
manifest_item
)
        
node
=
self
.
_data
        
assert
isinstance
(
node
dict
)
        
for
pathseg
in
key
[
:
-
1
]
:
            
node
=
node
.
setdefault
(
pathseg
{
}
)
            
assert
isinstance
(
node
dict
)
        
assert
key
[
-
1
]
not
in
node
        
node
[
key
[
-
1
]
]
=
data
        
self
.
_delete_node
(
self
.
_json_data
key
)
        
return
data
    
def
__setitem__
(
self
key
value
)
:
        
try
:
            
self
.
_delete_node
(
self
.
_json_data
key
)
        
except
KeyError
:
            
pass
        
node
=
self
.
_data
        
for
i
pathseg
in
enumerate
(
key
[
:
-
1
]
)
:
            
node
=
node
.
setdefault
(
pathseg
{
}
)
            
if
not
isinstance
(
node
dict
)
:
                
raise
KeyError
(
"
%
r
is
a
child
of
a
test
(
%
r
)
"
%
(
key
key
[
:
i
+
1
]
)
)
        
node
[
key
[
-
1
]
]
=
value
    
def
__delitem__
(
self
key
)
:
        
try
:
            
self
.
_delete_node
(
self
.
_data
key
)
        
except
KeyError
:
            
self
.
_delete_node
(
self
.
_json_data
key
)
        
else
:
            
try
:
                
del
self
.
_hashes
[
key
]
            
except
KeyError
:
                
pass
    
def
__iter__
(
self
)
:
        
"
"
"
Iterator
over
keys
in
the
TypeData
in
codepoint
order
"
"
"
        
data_node
=
self
.
_data
        
json_node
=
self
.
_json_data
        
path
=
tuple
(
)
        
stack
=
[
(
data_node
json_node
path
)
]
        
while
stack
:
            
data_node
json_node
path
=
stack
.
pop
(
)
            
if
isinstance
(
data_node
set
)
or
isinstance
(
json_node
list
)
:
                
assert
data_node
is
None
or
json_node
is
None
                
yield
path
            
else
:
                
assert
data_node
is
None
or
isinstance
(
data_node
dict
)
                
assert
json_node
is
None
or
isinstance
(
json_node
dict
)
                
keys
=
set
(
)
                
if
data_node
is
not
None
:
                    
keys
|
=
set
(
iter
(
data_node
)
)
                
if
json_node
is
not
None
:
                    
keys
|
=
set
(
iter
(
json_node
)
)
                
for
key
in
sorted
(
keys
reverse
=
True
)
:
                    
stack
.
append
(
(
data_node
.
get
(
key
)
if
data_node
is
not
None
else
None
                                  
json_node
.
get
(
key
)
if
json_node
is
not
None
else
None
                                  
path
+
(
key
)
)
)
    
def
__len__
(
self
)
:
        
count
=
0
        
stack
=
[
self
.
_data
]
        
while
stack
:
            
v
=
stack
.
pop
(
)
            
if
isinstance
(
v
set
)
:
                
count
+
=
1
            
else
:
                
stack
.
extend
(
v
.
values
(
)
)
        
stack
=
[
self
.
_json_data
]
        
while
stack
:
            
v
=
stack
.
pop
(
)
            
if
isinstance
(
v
list
)
:
                
count
+
=
1
            
else
:
                
stack
.
extend
(
v
.
values
(
)
)
        
return
count
    
def
__nonzero__
(
self
)
:
        
return
bool
(
self
.
_data
)
or
bool
(
self
.
_json_data
)
    
__bool__
=
__nonzero__
    
def
__contains__
(
self
key
)
:
        
node
=
self
.
_data
        
for
pathseg
in
key
:
            
if
pathseg
in
node
:
                
node
=
node
[
pathseg
]
            
else
:
                
break
        
else
:
            
return
bool
(
isinstance
(
node
set
)
)
        
node
=
self
.
_json_data
        
for
pathseg
in
key
:
            
if
pathseg
in
node
:
                
node
=
node
[
pathseg
]
            
else
:
                
break
        
else
:
            
return
bool
(
isinstance
(
node
list
)
)
        
return
False
    
def
clear
(
self
)
:
        
self
.
_json_data
.
clear
(
)
        
self
.
_data
.
clear
(
)
        
self
.
_hashes
.
clear
(
)
    
def
set_json
(
self
json_data
)
:
        
"
"
"
Provide
the
object
with
a
raw
JSON
blob
        
Note
that
this
object
graph
is
assumed
to
be
owned
by
the
TypeData
        
object
after
the
call
so
the
caller
must
not
mutate
any
part
of
the
        
graph
.
        
"
"
"
        
if
self
.
_json_data
:
            
raise
ValueError
(
"
set_json
call
when
JSON
data
is
not
empty
"
)
        
self
.
_json_data
=
json_data
    
def
to_json
(
self
)
:
        
"
"
"
Convert
the
current
data
to
JSON
        
Note
that
the
returned
object
may
contain
references
to
the
internal
        
data
structures
and
is
only
guaranteed
to
be
valid
until
the
next
        
__getitem__
__setitem__
__delitem__
call
so
the
caller
must
not
        
mutate
any
part
of
the
returned
object
graph
.
        
"
"
"
        
json_rv
=
self
.
_json_data
.
copy
(
)
        
def
safe_sorter
(
element
)
:
            
"
"
"
key
function
to
sort
lists
with
None
values
.
"
"
"
            
if
element
and
not
element
[
0
]
:
                
return
(
"
"
element
[
1
]
)
            
else
:
                
return
element
        
stack
=
[
(
self
.
_data
json_rv
tuple
(
)
)
]
        
while
stack
:
            
data_node
json_node
par_full_key
=
stack
.
pop
(
)
            
for
k
v
in
data_node
.
items
(
)
:
                
full_key
=
par_full_key
+
(
k
)
                
if
isinstance
(
v
set
)
:
                    
assert
k
not
in
json_node
                    
json_node
[
k
]
=
[
self
.
_hashes
.
get
(
                        
full_key
)
]
+
[
t
for
t
in
sorted
(
(
test
.
to_json
(
)
for
test
in
v
)
key
=
safe_sorter
)
]
                
else
:
                    
json_node
[
k
]
=
json_node
.
get
(
k
{
}
)
.
copy
(
)
                    
stack
.
append
(
(
v
json_node
[
k
]
full_key
)
)
        
return
json_rv
class
PathHash
(
PathHashType
)
:
    
def
__init__
(
self
data
)
:
        
self
.
_data
=
data
    
def
__getitem__
(
self
k
)
:
        
if
k
not
in
self
.
_data
:
            
raise
KeyError
        
if
k
in
self
.
_data
.
_hashes
:
            
return
self
.
_data
.
_hashes
[
k
]
        
node
=
self
.
_data
.
_json_data
        
for
pathseg
in
k
:
            
if
pathseg
in
node
:
                
node
=
node
[
pathseg
]
            
else
:
                
break
        
else
:
            
return
node
[
0
]
        
assert
False
"
unreachable
"
        
raise
KeyError
    
def
__setitem__
(
self
k
v
)
:
        
if
k
not
in
self
.
_data
:
            
raise
KeyError
        
if
k
in
self
.
_data
.
_hashes
:
            
self
.
_data
.
_hashes
[
k
]
=
v
        
node
=
self
.
_data
.
_json_data
        
for
pathseg
in
k
:
            
if
pathseg
in
node
:
                
node
=
node
[
pathseg
]
            
else
:
                
break
        
else
:
            
node
[
0
]
=
v
            
return
        
self
.
_data
.
_hashes
[
k
]
=
v
    
def
__delitem__
(
self
k
)
:
        
raise
ValueError
(
"
keys
here
must
match
underlying
data
"
)
    
def
__iter__
(
self
)
:
        
return
iter
(
self
.
_data
)
    
def
__len__
(
self
)
:
        
return
len
(
self
.
_data
)
