import
json
import
os
from
collections
import
MutableMapping
from
six
import
iteritems
iterkeys
itervalues
string_types
binary_type
text_type
from
.
import
vcs
from
.
item
import
(
ConformanceCheckerTest
ManifestItem
ManualTest
RefTest
SupportFile
                   
TestharnessTest
VisualTest
WebDriverSpecTest
CrashTest
)
from
.
log
import
get_logger
from
.
sourcefile
import
SourceFile
from
.
utils
import
from_os_path
to_os_path
MYPY
=
False
if
MYPY
:
    
from
logging
import
Logger
    
from
typing
import
Any
    
from
typing
import
Container
    
from
typing
import
Dict
    
from
typing
import
IO
    
from
typing
import
Iterable
    
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
try
:
    
import
ujson
    
fast_json
=
ujson
except
ImportError
:
    
fast_json
=
json
CURRENT_VERSION
=
7
class
ManifestError
(
Exception
)
:
    
pass
class
ManifestVersionMismatch
(
ManifestError
)
:
    
pass
item_classes
=
{
"
testharness
"
:
TestharnessTest
                
"
reftest
"
:
RefTest
                
"
crashtest
"
:
CrashTest
                
"
manual
"
:
ManualTest
                
"
wdspec
"
:
WebDriverSpecTest
                
"
conformancechecker
"
:
ConformanceCheckerTest
                
"
visual
"
:
VisualTest
                
"
support
"
:
SupportFile
}
if
MYPY
:
    
TypeDataType
=
MutableMapping
[
Text
Set
[
ManifestItem
]
]
else
:
    
TypeDataType
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
manifest
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
manifest
=
manifest
        
self
.
type_cls
=
type_cls
        
self
.
json_data
=
{
}
        
self
.
tests_root
=
None
        
self
.
data
=
{
}
    
def
__getitem__
(
self
key
)
:
        
if
key
not
in
self
.
data
and
self
.
json_data
is
not
None
:
            
self
.
load
(
key
)
        
return
self
.
data
[
key
]
    
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
data
)
or
bool
(
self
.
json_data
)
    
def
__len__
(
self
)
:
        
rv
=
len
(
self
.
data
)
        
if
self
.
json_data
is
not
None
:
            
rv
+
=
len
(
self
.
json_data
)
        
return
rv
    
def
__delitem__
(
self
key
)
:
        
if
key
in
self
.
data
:
            
del
self
.
data
[
key
]
        
elif
self
.
json_data
is
not
None
:
            
del
self
.
json_data
[
from_os_path
(
key
)
]
        
else
:
            
raise
KeyError
    
def
__setitem__
(
self
key
value
)
:
        
if
self
.
json_data
is
not
None
:
            
path
=
from_os_path
(
key
)
            
if
path
in
self
.
json_data
:
                
del
self
.
json_data
[
path
]
        
self
.
data
[
key
]
=
value
    
def
__contains__
(
self
key
)
:
        
self
.
load_all
(
)
        
return
key
in
self
.
data
    
def
__iter__
(
self
)
:
        
self
.
load_all
(
)
        
return
self
.
data
.
__iter__
(
)
    
def
itervalues
(
self
)
:
        
self
.
load_all
(
)
        
return
itervalues
(
self
.
data
)
    
def
iteritems
(
self
)
:
        
self
.
load_all
(
)
        
return
iteritems
(
self
.
data
)
    
def
values
(
self
)
:
        
return
list
(
self
.
itervalues
(
)
)
    
def
items
(
self
)
:
        
return
list
(
self
.
iteritems
(
)
)
    
def
load
(
self
key
)
:
        
"
"
"
Load
a
specific
Item
given
a
path
"
"
"
        
if
self
.
json_data
is
not
None
:
            
data
=
set
(
)
            
path
=
from_os_path
(
key
)
            
for
test
in
self
.
json_data
.
get
(
path
[
]
)
:
                
manifest_item
=
self
.
type_cls
.
from_json
(
self
.
manifest
path
test
)
                
data
.
add
(
manifest_item
)
            
try
:
                
del
self
.
json_data
[
path
]
            
except
KeyError
:
                
pass
            
self
.
data
[
key
]
=
data
        
else
:
            
raise
ValueError
    
def
load_all
(
self
)
:
        
"
"
"
Load
all
test
items
in
this
class
"
"
"
        
if
self
.
json_data
is
not
None
:
            
for
path
value
in
iteritems
(
self
.
json_data
)
:
                
key
=
to_os_path
(
path
)
                
if
key
in
self
.
data
:
                    
continue
                
data
=
set
(
)
                
for
test
in
self
.
json_data
.
get
(
path
[
]
)
:
                    
manifest_item
=
self
.
type_cls
.
from_json
(
self
.
manifest
path
test
)
                    
data
.
add
(
manifest_item
)
                
self
.
data
[
key
]
=
data
            
self
.
json_data
=
None
    
def
set_json
(
self
tests_root
data
)
:
        
if
not
isinstance
(
data
dict
)
:
            
raise
ValueError
(
"
Got
a
%
s
expected
a
dict
"
%
(
type
(
data
)
)
)
        
self
.
tests_root
=
tests_root
        
self
.
json_data
=
data
    
def
to_json
(
self
)
:
        
data
=
{
            
from_os_path
(
path
)
:
            
[
t
for
t
in
sorted
(
test
.
to_json
(
)
for
test
in
tests
)
]
            
for
path
tests
in
iteritems
(
self
.
data
)
        
}
        
if
self
.
json_data
is
not
None
:
            
if
not
data
:
                
return
self
.
json_data
            
data
.
update
(
self
.
json_data
)
        
return
data
    
def
paths
(
self
)
:
        
"
"
"
Get
a
list
of
all
paths
containing
items
of
this
type
        
without
actually
constructing
all
the
items
"
"
"
        
rv
=
set
(
iterkeys
(
self
.
data
)
)
        
if
self
.
json_data
:
            
rv
|
=
{
to_os_path
(
item
)
for
item
in
iterkeys
(
self
.
json_data
)
}
        
return
rv
if
MYPY
:
    
ManifestDataType
=
Dict
[
Any
TypeData
]
else
:
    
ManifestDataType
=
dict
class
ManifestData
(
ManifestDataType
)
:
    
def
__init__
(
self
manifest
)
:
        
"
"
"
Dictionary
subclass
containing
a
TypeData
instance
for
each
test
type
        
keyed
by
type
name
"
"
"
        
self
.
initialized
=
False
        
for
key
value
in
iteritems
(
item_classes
)
:
            
self
[
key
]
=
TypeData
(
manifest
value
)
        
self
.
initialized
=
True
        
self
.
json_obj
=
None
    
def
__setitem__
(
self
key
value
)
:
        
if
self
.
initialized
:
            
raise
AttributeError
        
dict
.
__setitem__
(
self
key
value
)
    
def
paths
(
self
)
:
        
"
"
"
Get
a
list
of
all
paths
containing
test
items
        
without
actually
constructing
all
the
items
"
"
"
        
rv
=
set
(
)
        
for
item_data
in
itervalues
(
self
)
:
            
rv
|
=
set
(
item_data
.
paths
(
)
)
        
return
rv
class
Manifest
(
object
)
:
    
def
__init__
(
self
tests_root
=
None
url_base
=
"
/
"
)
:
        
assert
url_base
is
not
None
        
self
.
_path_hash
=
{
}
        
self
.
_data
=
ManifestData
(
self
)
        
self
.
tests_root
=
tests_root
        
self
.
url_base
=
url_base
    
def
__iter__
(
self
)
:
        
return
self
.
itertypes
(
)
    
def
itertypes
(
self
*
types
)
:
        
for
item_type
in
(
types
or
sorted
(
self
.
_data
.
keys
(
)
)
)
:
            
for
path
in
sorted
(
self
.
_data
[
item_type
]
)
:
                
tests
=
self
.
_data
[
item_type
]
[
path
]
                
yield
item_type
path
tests
    
def
iterpath
(
self
path
)
:
        
for
type_tests
in
self
.
_data
.
values
(
)
:
            
i
=
type_tests
.
get
(
path
set
(
)
)
            
assert
i
is
not
None
            
for
test
in
i
:
                
yield
test
    
def
iterdir
(
self
dir_name
)
:
        
if
not
dir_name
.
endswith
(
os
.
path
.
sep
)
:
            
dir_name
=
dir_name
+
os
.
path
.
sep
        
for
type_tests
in
self
.
_data
.
values
(
)
:
            
for
path
tests
in
type_tests
.
iteritems
(
)
:
                
if
path
.
startswith
(
dir_name
)
:
                    
for
test
in
tests
:
                        
yield
test
    
def
update
(
self
tree
)
:
        
"
"
"
Update
the
manifest
given
an
iterable
of
items
that
make
up
the
updated
manifest
.
        
The
iterable
must
either
generate
tuples
of
the
form
(
SourceFile
True
)
for
paths
        
that
are
to
be
updated
or
(
path
False
)
for
items
that
are
not
to
be
updated
.
This
        
unusual
API
is
designed
as
an
optimistaion
meaning
that
SourceFile
items
need
not
be
        
constructed
in
the
case
we
are
not
updating
a
path
but
the
absence
of
an
item
from
        
the
iterator
may
be
used
to
remove
defunct
entries
from
the
manifest
.
"
"
"
        
seen_files
=
set
(
)
        
changed
=
False
        
path_hash
=
self
.
_path_hash
        
data
=
self
.
_data
        
prev_files
=
data
.
paths
(
)
        
for
source_file
update
in
tree
:
            
if
not
update
:
                
assert
isinstance
(
source_file
(
binary_type
text_type
)
)
                
rel_path
=
source_file
                
seen_files
.
add
(
rel_path
)
                
assert
rel_path
in
path_hash
                
old_hash
old_type
=
path_hash
[
rel_path
]
            
else
:
                
assert
not
isinstance
(
source_file
bytes
)
                
rel_path
=
source_file
.
rel_path
                
seen_files
.
add
(
rel_path
)
                
file_hash
=
source_file
.
hash
                
is_new
=
rel_path
not
in
path_hash
                
hash_changed
=
False
                
if
not
is_new
:
                    
old_hash
old_type
=
path_hash
[
rel_path
]
                    
if
old_hash
!
=
file_hash
:
                        
hash_changed
=
True
                
if
is_new
or
hash_changed
:
                    
new_type
manifest_items
=
source_file
.
manifest_items
(
)
                    
data
[
new_type
]
[
rel_path
]
=
set
(
manifest_items
)
                    
path_hash
[
rel_path
]
=
(
file_hash
new_type
)
                    
if
hash_changed
and
new_type
!
=
old_type
:
                        
del
data
[
old_type
]
[
rel_path
]
                    
changed
=
True
        
deleted
=
prev_files
-
seen_files
        
if
deleted
:
            
changed
=
True
            
for
rel_path
in
deleted
:
                
if
rel_path
in
path_hash
:
                    
_
old_type
=
path_hash
[
rel_path
]
                    
del
path_hash
[
rel_path
]
                    
try
:
                        
del
data
[
old_type
]
[
rel_path
]
                    
except
KeyError
:
                        
pass
                
else
:
                    
for
test_data
in
itervalues
(
data
)
:
                        
if
rel_path
in
test_data
:
                            
del
test_data
[
rel_path
]
        
return
changed
    
def
to_json
(
self
)
:
        
out_items
=
{
            
test_type
:
type_paths
.
to_json
(
)
            
for
test_type
type_paths
in
iteritems
(
self
.
_data
)
if
type_paths
        
}
        
rv
=
{
"
url_base
"
:
self
.
url_base
              
"
paths
"
:
{
from_os_path
(
k
)
:
v
for
k
v
in
iteritems
(
self
.
_path_hash
)
}
              
"
items
"
:
out_items
              
"
version
"
:
CURRENT_VERSION
}
        
return
rv
    
classmethod
    
def
from_json
(
cls
tests_root
obj
types
=
None
)
:
        
version
=
obj
.
get
(
"
version
"
)
        
if
version
!
=
CURRENT_VERSION
:
            
raise
ManifestVersionMismatch
        
self
=
cls
(
tests_root
url_base
=
obj
.
get
(
"
url_base
"
"
/
"
)
)
        
if
not
hasattr
(
obj
"
items
"
)
and
hasattr
(
obj
"
paths
"
)
:
            
raise
ManifestError
        
self
.
_path_hash
=
{
to_os_path
(
k
)
:
v
for
k
v
in
iteritems
(
obj
[
"
paths
"
]
)
}
        
if
"
reftest_node
"
in
obj
[
"
items
"
]
:
            
for
path
in
obj
[
"
items
"
]
[
"
reftest_node
"
]
:
                
os_path
=
to_os_path
(
path
)
                
old_hash
old_type
=
self
.
_path_hash
[
os_path
]
                
self
.
_path_hash
[
os_path
]
=
(
old_hash
"
reftest
"
)
        
for
test_type
type_paths
in
iteritems
(
obj
[
"
items
"
]
)
:
            
if
test_type
in
(
"
reftest
"
"
reftest_node
"
)
:
                
if
types
and
"
reftest
"
not
in
types
:
                    
continue
                
if
self
.
_data
[
"
reftest
"
]
.
json_data
:
                    
self
.
_data
[
"
reftest
"
]
.
json_data
.
update
(
type_paths
)
                
else
:
                    
self
.
_data
[
"
reftest
"
]
.
set_json
(
tests_root
type_paths
)
                
continue
            
if
test_type
not
in
item_classes
:
                
raise
ManifestError
            
if
types
and
test_type
not
in
types
:
                
continue
            
self
.
_data
[
test_type
]
.
set_json
(
tests_root
type_paths
)
        
return
self
def
load
(
tests_root
manifest
types
=
None
)
:
    
logger
=
get_logger
(
)
    
logger
.
warning
(
"
Prefer
load_and_update
instead
"
)
    
return
_load
(
logger
tests_root
manifest
types
)
__load_cache
=
{
}
def
_load
(
logger
          
tests_root
          
manifest
          
types
=
None
          
allow_cached
=
True
          
)
:
    
manifest_path
=
(
manifest
if
isinstance
(
manifest
string_types
)
                     
else
manifest
.
name
)
    
if
allow_cached
and
manifest_path
in
__load_cache
:
        
return
__load_cache
[
manifest_path
]
    
if
isinstance
(
manifest
string_types
)
:
        
if
os
.
path
.
exists
(
manifest
)
:
            
logger
.
debug
(
"
Opening
manifest
at
%
s
"
%
manifest
)
        
else
:
            
logger
.
debug
(
"
Creating
new
manifest
at
%
s
"
%
manifest
)
        
try
:
            
with
open
(
manifest
"
rb
"
)
as
f
:
                
rv
=
Manifest
.
from_json
(
tests_root
                                        
fast_json
.
load
(
f
)
                                        
types
=
types
)
        
except
IOError
:
            
return
None
        
except
ValueError
:
            
logger
.
warning
(
"
%
r
may
be
corrupted
"
manifest
)
            
return
None
    
else
:
        
rv
=
Manifest
.
from_json
(
tests_root
                                
fast_json
.
load
(
manifest
)
                                
types
=
types
)
    
if
allow_cached
:
        
__load_cache
[
manifest_path
]
=
rv
    
return
rv
def
load_and_update
(
tests_root
                    
manifest_path
                    
url_base
                    
update
=
True
                    
rebuild
=
False
                    
metadata_path
=
None
                    
cache_root
=
None
                    
working_copy
=
True
                    
types
=
None
                    
write_manifest
=
True
                    
allow_cached
=
True
                    
)
:
    
logger
=
get_logger
(
)
    
manifest
=
None
    
if
not
rebuild
:
        
try
:
            
manifest
=
_load
(
logger
                             
tests_root
                             
manifest_path
                             
types
=
types
                             
allow_cached
=
allow_cached
)
        
except
ManifestVersionMismatch
:
            
logger
.
info
(
"
Manifest
version
changed
rebuilding
"
)
        
if
manifest
is
not
None
and
manifest
.
url_base
!
=
url_base
:
            
logger
.
info
(
"
Manifest
url
base
did
not
match
rebuilding
"
)
            
manifest
=
None
    
if
manifest
is
None
:
        
manifest
=
Manifest
(
tests_root
url_base
)
        
rebuild
=
True
        
update
=
True
    
if
rebuild
or
update
:
        
tree
=
vcs
.
get_tree
(
tests_root
manifest
manifest_path
cache_root
                            
working_copy
rebuild
)
        
changed
=
manifest
.
update
(
tree
)
        
if
write_manifest
and
changed
:
            
write
(
manifest
manifest_path
)
        
tree
.
dump_caches
(
)
    
return
manifest
def
write
(
manifest
manifest_path
)
:
    
dir_name
=
os
.
path
.
dirname
(
manifest_path
)
    
if
not
os
.
path
.
exists
(
dir_name
)
:
        
os
.
makedirs
(
dir_name
)
    
with
open
(
manifest_path
"
wb
"
)
as
f
:
        
json
.
dump
(
manifest
.
to_json
(
)
f
                  
sort_keys
=
True
indent
=
1
separators
=
(
'
'
'
:
'
)
)
        
f
.
write
(
"
\
n
"
)
