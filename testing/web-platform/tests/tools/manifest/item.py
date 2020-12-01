import
os
.
path
from
inspect
import
isabstract
from
six
import
iteritems
with_metaclass
from
six
.
moves
.
urllib
.
parse
import
urljoin
urlparse
from
abc
import
ABCMeta
abstractproperty
from
.
utils
import
to_os_path
MYPY
=
False
if
MYPY
:
    
from
typing
import
Optional
    
from
typing
import
Text
    
from
typing
import
Dict
    
from
typing
import
Tuple
    
from
typing
import
List
    
from
typing
import
Union
    
from
typing
import
Type
    
from
typing
import
Any
    
from
typing
import
Sequence
    
from
typing
import
Hashable
    
from
.
manifest
import
Manifest
    
Fuzzy
=
Dict
[
Optional
[
Tuple
[
Text
Text
Text
]
]
List
[
int
]
]
    
PageRanges
=
Dict
[
Text
List
[
int
]
]
item_types
=
{
}
class
ManifestItemMeta
(
ABCMeta
)
:
    
"
"
"
Custom
metaclass
that
registers
all
the
subclasses
in
the
    
item_types
dictionary
according
to
the
value
of
their
item_type
    
attribute
and
otherwise
behaves
like
an
ABCMeta
.
"
"
"
    
def
__new__
(
cls
name
bases
attrs
)
:
        
rv
=
super
(
ManifestItemMeta
cls
)
.
__new__
(
cls
name
bases
attrs
)
        
if
not
isabstract
(
rv
)
:
            
assert
issubclass
(
rv
ManifestItem
)
            
assert
isinstance
(
rv
.
item_type
str
)
            
item_types
[
rv
.
item_type
]
=
rv
        
return
rv
class
ManifestItem
(
with_metaclass
(
ManifestItemMeta
)
)
:
    
__slots__
=
(
"
_tests_root
"
"
path
"
)
    
def
__init__
(
self
tests_root
path
)
:
        
self
.
_tests_root
=
tests_root
        
self
.
path
=
path
    
abstractproperty
    
def
id
(
self
)
:
        
"
"
"
The
test
'
s
id
(
usually
its
url
)
"
"
"
        
pass
    
abstractproperty
    
def
item_type
(
self
)
:
        
"
"
"
The
item
'
s
type
"
"
"
        
pass
    
property
    
def
path_parts
(
self
)
:
        
return
tuple
(
self
.
path
.
split
(
os
.
path
.
sep
)
)
    
def
key
(
self
)
:
        
"
"
"
A
unique
identifier
for
the
test
"
"
"
        
return
(
self
.
item_type
self
.
id
)
    
def
__eq__
(
self
other
)
:
        
if
not
hasattr
(
other
"
key
"
)
:
            
return
False
        
return
bool
(
self
.
key
(
)
=
=
other
.
key
(
)
)
    
def
__hash__
(
self
)
:
        
return
hash
(
self
.
key
(
)
)
    
def
__repr__
(
self
)
:
        
return
"
<
%
s
.
%
s
id
=
%
r
path
=
%
r
>
"
%
(
self
.
__module__
self
.
__class__
.
__name__
self
.
id
self
.
path
)
    
def
to_json
(
self
)
:
        
return
(
)
    
classmethod
    
def
from_json
(
cls
                  
manifest
                  
path
                  
obj
                  
)
:
        
path
=
to_os_path
(
path
)
        
tests_root
=
manifest
.
tests_root
        
assert
tests_root
is
not
None
        
return
cls
(
tests_root
path
)
class
URLManifestItem
(
ManifestItem
)
:
    
__slots__
=
(
"
url_base
"
"
_url
"
"
_extras
"
)
    
def
__init__
(
self
                 
tests_root
                 
path
                 
url_base
                 
url
                 
*
*
extras
                 
)
:
        
super
(
URLManifestItem
self
)
.
__init__
(
tests_root
path
)
        
assert
url_base
[
0
]
=
=
"
/
"
        
self
.
url_base
=
url_base
        
assert
url
is
None
or
url
[
0
]
!
=
"
/
"
        
self
.
_url
=
url
        
self
.
_extras
=
extras
    
property
    
def
id
(
self
)
:
        
return
self
.
url
    
property
    
def
url
(
self
)
:
        
rel_url
=
self
.
_url
or
self
.
path
.
replace
(
os
.
path
.
sep
u
"
/
"
)
        
if
self
.
url_base
=
=
"
/
"
:
            
return
"
/
"
+
rel_url
        
return
urljoin
(
self
.
url_base
rel_url
)
    
property
    
def
https
(
self
)
:
        
flags
=
set
(
urlparse
(
self
.
url
)
.
path
.
rsplit
(
"
/
"
1
)
[
1
]
.
split
(
"
.
"
)
[
1
:
-
1
]
)
        
return
"
https
"
in
flags
or
"
serviceworker
"
in
flags
    
property
    
def
h2
(
self
)
:
        
flags
=
set
(
urlparse
(
self
.
url
)
.
path
.
rsplit
(
"
/
"
1
)
[
1
]
.
split
(
"
.
"
)
[
1
:
-
1
]
)
        
return
"
h2
"
in
flags
    
property
    
def
subdomain
(
self
)
:
        
flags
=
set
(
urlparse
(
self
.
url
)
.
path
.
rsplit
(
"
/
"
1
)
[
1
]
.
split
(
"
.
"
)
[
1
:
-
1
]
)
        
return
"
www
"
in
flags
    
def
to_json
(
self
)
:
        
rel_url
=
None
if
self
.
_url
=
=
self
.
path
.
replace
(
os
.
path
.
sep
u
"
/
"
)
else
self
.
_url
        
rv
=
(
rel_url
{
}
)
        
return
rv
    
classmethod
    
def
from_json
(
cls
                  
manifest
                  
path
                  
obj
                  
)
:
        
path
=
to_os_path
(
path
)
        
url
extras
=
obj
        
tests_root
=
manifest
.
tests_root
        
assert
tests_root
is
not
None
        
return
cls
(
tests_root
                   
path
                   
manifest
.
url_base
                   
url
                   
*
*
extras
)
class
TestharnessTest
(
URLManifestItem
)
:
    
__slots__
=
(
)
    
item_type
=
"
testharness
"
    
property
    
def
timeout
(
self
)
:
        
return
self
.
_extras
.
get
(
"
timeout
"
)
    
property
    
def
testdriver
(
self
)
:
        
return
self
.
_extras
.
get
(
"
testdriver
"
)
    
property
    
def
jsshell
(
self
)
:
        
return
self
.
_extras
.
get
(
"
jsshell
"
)
    
property
    
def
quic
(
self
)
:
        
return
self
.
_extras
.
get
(
"
quic
"
)
    
property
    
def
script_metadata
(
self
)
:
        
return
self
.
_extras
.
get
(
"
script_metadata
"
)
    
def
to_json
(
self
)
:
        
rv
=
super
(
TestharnessTest
self
)
.
to_json
(
)
        
if
self
.
timeout
is
not
None
:
            
rv
[
-
1
]
[
"
timeout
"
]
=
self
.
timeout
        
if
self
.
testdriver
:
            
rv
[
-
1
]
[
"
testdriver
"
]
=
self
.
testdriver
        
if
self
.
jsshell
:
            
rv
[
-
1
]
[
"
jsshell
"
]
=
True
        
if
self
.
quic
is
not
None
:
            
rv
[
-
1
]
[
"
quic
"
]
=
self
.
quic
        
if
self
.
script_metadata
:
            
rv
[
-
1
]
[
"
script_metadata
"
]
=
[
(
k
v
)
for
(
k
v
)
in
self
.
script_metadata
]
        
return
rv
class
RefTest
(
URLManifestItem
)
:
    
__slots__
=
(
"
references
"
)
    
item_type
=
"
reftest
"
    
def
__init__
(
self
                 
tests_root
                 
path
                 
url_base
                 
url
                 
references
=
None
                 
*
*
extras
                 
)
:
        
super
(
RefTest
self
)
.
__init__
(
tests_root
path
url_base
url
*
*
extras
)
        
if
references
is
None
:
            
self
.
references
=
[
]
        
else
:
            
self
.
references
=
references
    
property
    
def
timeout
(
self
)
:
        
return
self
.
_extras
.
get
(
"
timeout
"
)
    
property
    
def
viewport_size
(
self
)
:
        
return
self
.
_extras
.
get
(
"
viewport_size
"
)
    
property
    
def
dpi
(
self
)
:
        
return
self
.
_extras
.
get
(
"
dpi
"
)
    
property
    
def
fuzzy
(
self
)
:
        
fuzzy
=
self
.
_extras
.
get
(
"
fuzzy
"
{
}
)
        
if
not
isinstance
(
fuzzy
list
)
:
            
return
fuzzy
        
rv
=
{
}
        
for
k
v
in
fuzzy
:
            
if
k
is
None
:
                
key
=
None
            
else
:
                
assert
len
(
k
)
=
=
3
                
key
=
tuple
(
k
)
            
rv
[
key
]
=
v
        
return
rv
    
def
to_json
(
self
)
:
        
rel_url
=
None
if
self
.
_url
=
=
self
.
path
else
self
.
_url
        
rv
=
(
rel_url
self
.
references
{
}
)
        
extras
=
rv
[
-
1
]
        
if
self
.
timeout
is
not
None
:
            
extras
[
"
timeout
"
]
=
self
.
timeout
        
if
self
.
viewport_size
is
not
None
:
            
extras
[
"
viewport_size
"
]
=
self
.
viewport_size
        
if
self
.
dpi
is
not
None
:
            
extras
[
"
dpi
"
]
=
self
.
dpi
        
if
self
.
fuzzy
:
            
extras
[
"
fuzzy
"
]
=
list
(
iteritems
(
self
.
fuzzy
)
)
        
return
rv
    
classmethod
    
def
from_json
(
cls
                  
manifest
                  
path
                  
obj
                  
)
:
        
tests_root
=
manifest
.
tests_root
        
assert
tests_root
is
not
None
        
path
=
to_os_path
(
path
)
        
url
references
extras
=
obj
        
return
cls
(
tests_root
                   
path
                   
manifest
.
url_base
                   
url
                   
references
                   
*
*
extras
)
class
PrintRefTest
(
RefTest
)
:
    
__slots__
=
(
"
references
"
)
    
item_type
=
"
print
-
reftest
"
    
property
    
def
page_ranges
(
self
)
:
        
return
self
.
_extras
.
get
(
"
page_ranges
"
{
}
)
    
def
to_json
(
self
)
:
        
rv
=
super
(
PrintRefTest
self
)
.
to_json
(
)
        
if
self
.
page_ranges
:
            
rv
[
-
1
]
[
"
page_ranges
"
]
=
self
.
page_ranges
        
return
rv
class
ManualTest
(
URLManifestItem
)
:
    
__slots__
=
(
)
    
item_type
=
"
manual
"
class
ConformanceCheckerTest
(
URLManifestItem
)
:
    
__slots__
=
(
)
    
item_type
=
"
conformancechecker
"
class
VisualTest
(
URLManifestItem
)
:
    
__slots__
=
(
)
    
item_type
=
"
visual
"
class
CrashTest
(
URLManifestItem
)
:
    
__slots__
=
(
)
    
item_type
=
"
crashtest
"
    
property
    
def
timeout
(
self
)
:
        
return
None
class
WebDriverSpecTest
(
URLManifestItem
)
:
    
__slots__
=
(
)
    
item_type
=
"
wdspec
"
    
property
    
def
timeout
(
self
)
:
        
return
self
.
_extras
.
get
(
"
timeout
"
)
    
def
to_json
(
self
)
:
        
rv
=
super
(
WebDriverSpecTest
self
)
.
to_json
(
)
        
if
self
.
timeout
is
not
None
:
            
rv
[
-
1
]
[
"
timeout
"
]
=
self
.
timeout
        
return
rv
class
SupportFile
(
ManifestItem
)
:
    
__slots__
=
(
)
    
item_type
=
"
support
"
    
property
    
def
id
(
self
)
:
        
return
self
.
path
