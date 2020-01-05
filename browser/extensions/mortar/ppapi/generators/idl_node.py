"
"
"
Nodes
for
PPAPI
IDL
AST
"
"
"
import
sys
from
idl_log
import
ErrOut
InfoOut
WarnOut
from
idl_propertynode
import
IDLPropertyNode
from
idl_release
import
IDLRelease
IDLReleaseMap
class
IDLAttribute
(
object
)
:
  
def
__init__
(
self
name
value
)
:
    
self
.
cls
=
'
ExtAttribute
'
    
self
.
name
=
name
    
self
.
value
=
value
  
def
__str__
(
self
)
:
    
return
'
%
s
=
%
s
'
%
(
self
.
name
self
.
value
)
class
IDLNode
(
IDLRelease
)
:
  
NamedSet
=
set
(
[
'
Enum
'
'
EnumItem
'
'
File
'
'
Function
'
'
Interface
'
                  
'
Member
'
'
Param
'
'
Struct
'
'
Type
'
'
Typedef
'
]
)
  
def
__init__
(
self
cls
filename
lineno
pos
children
=
None
)
:
    
IDLRelease
.
__init__
(
self
None
None
)
    
self
.
cls
=
cls
    
self
.
lineno
=
lineno
    
self
.
pos
=
pos
    
self
.
_filename
=
filename
    
self
.
_deps
=
{
}
    
self
.
errors
=
0
    
self
.
namespace
=
None
    
self
.
typelist
=
None
    
self
.
parent
=
None
    
self
.
_property_node
=
IDLPropertyNode
(
)
    
self
.
_unique_releases
=
None
    
self
.
releases
=
None
    
self
.
first_release
=
None
    
self
.
_children
=
[
]
    
if
children
:
      
for
child
in
children
:
        
if
child
.
cls
=
=
'
ExtAttribute
'
:
          
self
.
SetProperty
(
child
.
name
child
.
value
)
        
else
:
          
self
.
AddChild
(
child
)
  
def
__str__
(
self
)
:
    
name
=
self
.
GetName
(
)
    
if
name
is
None
:
      
name
=
'
'
    
return
'
%
s
(
%
s
)
'
%
(
self
.
cls
name
)
  
def
Location
(
self
)
:
    
"
"
"
Return
a
file
and
line
number
for
where
this
node
was
defined
.
"
"
"
    
return
'
%
s
(
%
d
)
'
%
(
self
.
_filename
self
.
lineno
)
  
def
Error
(
self
msg
)
:
    
"
"
"
Log
an
error
for
this
object
.
"
"
"
    
self
.
errors
+
=
1
    
ErrOut
.
LogLine
(
self
.
_filename
self
.
lineno
0
'
%
s
%
s
'
%
                   
(
str
(
self
)
msg
)
)
    
filenode
=
self
.
GetProperty
(
'
FILE
'
)
    
if
filenode
:
      
errcnt
=
filenode
.
GetProperty
(
'
ERRORS
'
)
      
if
not
errcnt
:
        
errcnt
=
0
      
filenode
.
SetProperty
(
'
ERRORS
'
errcnt
+
1
)
  
def
Warning
(
self
msg
)
:
    
"
"
"
Log
a
warning
for
this
object
.
"
"
"
    
WarnOut
.
LogLine
(
self
.
_filename
self
.
lineno
0
'
%
s
%
s
'
%
                    
(
str
(
self
)
msg
)
)
  
def
GetName
(
self
)
:
    
return
self
.
GetProperty
(
'
NAME
'
)
  
def
Dump
(
self
depth
=
0
comments
=
False
out
=
sys
.
stdout
)
:
    
"
"
"
Dump
this
object
and
its
children
"
"
"
    
if
self
.
cls
in
[
'
Comment
'
'
Copyright
'
]
:
      
is_comment
=
True
    
else
:
      
is_comment
=
False
    
if
not
comments
and
is_comment
:
      
return
    
tab
=
'
'
.
rjust
(
depth
*
2
)
    
if
is_comment
:
      
out
.
write
(
'
%
sComment
\
n
'
%
tab
)
      
for
line
in
self
.
GetName
(
)
.
split
(
'
\
n
'
)
:
        
out
.
write
(
'
%
s
"
%
s
"
\
n
'
%
(
tab
line
)
)
    
else
:
      
ver
=
IDLRelease
.
__str__
(
self
)
      
if
self
.
releases
:
        
release_list
=
'
:
'
      
else
:
        
release_list
=
'
:
undefined
'
      
out
.
write
(
'
%
s
%
s
%
s
%
s
\
n
'
%
(
tab
self
ver
release_list
)
)
    
if
self
.
typelist
:
      
out
.
write
(
'
%
s
Typelist
:
%
s
\
n
'
%
(
tab
self
.
typelist
.
GetReleases
(
)
[
0
]
)
)
    
properties
=
self
.
_property_node
.
GetPropertyList
(
)
    
if
properties
:
      
out
.
write
(
'
%
s
Properties
\
n
'
%
tab
)
      
for
p
in
properties
:
        
if
is_comment
and
p
=
=
'
NAME
'
:
          
continue
        
out
.
write
(
'
%
s
%
s
:
%
s
\
n
'
%
(
tab
p
self
.
GetProperty
(
p
)
)
)
    
for
child
in
self
.
_children
:
      
child
.
Dump
(
depth
+
1
comments
=
comments
out
=
out
)
  
def
IsA
(
self
*
typelist
)
:
    
"
"
"
Check
if
node
is
of
a
given
type
.
"
"
"
    
return
self
.
cls
in
typelist
  
def
GetListOf
(
self
*
keys
)
:
    
"
"
"
Get
a
list
of
objects
for
the
given
key
(
s
)
.
"
"
"
    
out
=
[
]
    
for
child
in
self
.
_children
:
      
if
child
.
cls
in
keys
:
        
out
.
append
(
child
)
    
return
out
  
def
GetOneOf
(
self
*
keys
)
:
    
"
"
"
Get
an
object
for
the
given
key
(
s
)
.
"
"
"
    
out
=
self
.
GetListOf
(
*
keys
)
    
if
out
:
      
return
out
[
0
]
    
return
None
  
def
SetParent
(
self
parent
)
:
    
self
.
_property_node
.
AddParent
(
parent
)
    
self
.
parent
=
parent
  
def
AddChild
(
self
node
)
:
    
node
.
SetParent
(
self
)
    
self
.
_children
.
append
(
node
)
  
def
GetChildren
(
self
)
:
    
return
self
.
_children
  
def
GetType
(
self
release
)
:
    
if
not
self
.
typelist
:
      
return
None
    
return
self
.
typelist
.
FindRelease
(
release
)
  
def
GetDeps
(
self
release
visited
=
None
)
:
    
visited
=
visited
or
set
(
)
    
if
not
self
.
IsRelease
(
release
)
or
self
.
IsA
(
'
Comment
'
'
Copyright
'
)
:
      
return
set
(
[
]
)
    
deps
=
self
.
_deps
.
get
(
release
None
)
    
if
deps
is
not
None
:
      
return
deps
    
if
self
in
visited
:
      
return
set
(
[
self
]
)
    
visited
|
=
set
(
[
self
]
)
    
deps
=
set
(
[
self
]
)
    
for
child
in
self
.
GetChildren
(
)
:
      
deps
|
=
child
.
GetDeps
(
release
visited
)
      
visited
|
=
set
(
deps
)
    
typeref
=
self
.
GetType
(
release
)
    
if
typeref
:
      
deps
|
=
typeref
.
GetDeps
(
release
visited
)
    
self
.
_deps
[
release
]
=
deps
    
return
deps
  
def
GetVersion
(
self
release
)
:
    
filenode
=
self
.
GetProperty
(
'
FILE
'
)
    
if
not
filenode
:
      
return
None
    
return
filenode
.
release_map
.
GetVersion
(
release
)
  
def
GetUniqueReleases
(
self
releases
)
:
    
"
"
"
Return
the
unique
set
of
first
releases
corresponding
to
input
    
Since
we
are
returning
the
corresponding
'
first
'
version
for
a
    
release
we
may
return
a
release
version
prior
to
the
one
in
the
list
.
"
"
"
    
my_min
my_max
=
self
.
GetMinMax
(
releases
)
    
if
my_min
>
releases
[
-
1
]
or
my_max
<
releases
[
0
]
:
      
return
[
]
    
out
=
set
(
)
    
for
rel
in
releases
:
      
remapped
=
self
.
first_release
[
rel
]
      
if
not
remapped
:
        
continue
      
out
|
=
set
(
[
remapped
]
)
    
self
.
_unique_releases
=
sorted
(
out
)
    
return
self
.
_unique_releases
  
def
LastRelease
(
self
release
)
:
    
if
self
.
_unique_releases
and
self
.
_unique_releases
[
-
1
]
>
release
:
      
return
False
    
return
True
  
def
GetRelease
(
self
version
)
:
    
filenode
=
self
.
GetProperty
(
'
FILE
'
)
    
if
not
filenode
:
      
return
None
    
return
filenode
.
release_map
.
GetRelease
(
version
)
  
def
_GetReleaseList
(
self
releases
visited
=
None
)
:
    
visited
=
visited
or
set
(
)
    
if
not
self
.
releases
:
      
if
self
.
IsA
(
'
Comment
'
'
Copyright
'
'
Label
'
)
:
        
self
.
releases
=
[
]
        
return
self
.
releases
      
my_min
my_max
=
self
.
GetMinMax
(
releases
)
      
if
my_max
!
=
releases
[
-
1
]
:
        
my_releases
=
set
(
[
my_min
my_max
]
)
      
else
:
        
my_releases
=
set
(
[
my_min
]
)
      
r
=
self
.
GetRelease
(
self
.
GetProperty
(
'
version
'
)
)
      
if
not
r
in
my_releases
:
        
my_releases
|
=
set
(
[
r
]
)
      
if
self
in
visited
:
        
return
[
my_min
]
      
visited
|
=
set
(
[
self
]
)
      
if
self
.
IsA
(
'
AST
'
'
File
'
)
:
        
my_releases
=
set
(
)
      
child_releases
=
set
(
)
      
cur_visits
=
visited
      
for
child
in
self
.
_children
:
        
child_releases
|
=
set
(
child
.
_GetReleaseList
(
releases
cur_visits
)
)
        
visited
|
=
set
(
child_releases
)
      
type_releases
=
set
(
)
      
if
self
.
typelist
:
        
type_list
=
self
.
typelist
.
GetReleases
(
)
        
for
typenode
in
type_list
:
          
type_releases
|
=
set
(
typenode
.
_GetReleaseList
(
releases
cur_visits
)
)
        
type_release_list
=
sorted
(
type_releases
)
        
if
my_min
<
type_release_list
[
0
]
:
          
type_node
=
type_list
[
0
]
          
self
.
Error
(
'
requires
%
s
in
%
s
which
is
undefined
at
%
s
.
'
%
(
              
type_node
type_node
.
_filename
my_min
)
)
      
for
rel
in
child_releases
|
type_releases
:
        
if
rel
>
=
my_min
and
rel
<
=
my_max
:
          
my_releases
|
=
set
(
[
rel
]
)
      
self
.
releases
=
sorted
(
my_releases
)
    
return
self
.
releases
  
def
BuildReleaseMap
(
self
releases
)
:
    
unique_list
=
self
.
_GetReleaseList
(
releases
)
    
_
my_max
=
self
.
GetMinMax
(
releases
)
    
self
.
first_release
=
{
}
    
last_rel
=
None
    
for
rel
in
releases
:
      
if
rel
in
unique_list
:
        
last_rel
=
rel
      
self
.
first_release
[
rel
]
=
last_rel
      
if
rel
=
=
my_max
:
        
last_rel
=
None
  
def
SetProperty
(
self
name
val
)
:
    
self
.
_property_node
.
SetProperty
(
name
val
)
  
def
GetProperty
(
self
name
)
:
    
return
self
.
_property_node
.
GetProperty
(
name
)
  
def
GetPropertyLocal
(
self
name
)
:
    
return
self
.
_property_node
.
GetPropertyLocal
(
name
)
  
def
NodeIsDevOnly
(
self
)
:
    
"
"
"
Returns
true
iff
a
node
is
only
in
dev
channel
.
"
"
"
    
return
self
.
GetProperty
(
'
dev_version
'
)
and
not
self
.
GetProperty
(
'
version
'
)
  
def
DevInterfaceMatchesStable
(
self
release
)
:
    
"
"
"
Returns
true
if
an
interface
has
an
equivalent
stable
version
.
"
"
"
    
assert
(
self
.
IsA
(
'
Interface
'
)
)
    
for
child
in
self
.
GetListOf
(
'
Member
'
)
:
      
unique
=
child
.
GetUniqueReleases
(
[
release
]
)
      
if
not
unique
or
not
child
.
InReleases
(
[
release
]
)
:
        
continue
      
if
child
.
NodeIsDevOnly
(
)
:
        
return
False
    
return
True
class
IDLFile
(
IDLNode
)
:
  
def
__init__
(
self
name
children
errors
=
0
)
:
    
attrs
=
[
IDLAttribute
(
'
NAME
'
name
)
             
IDLAttribute
(
'
ERRORS
'
errors
)
]
    
if
not
children
:
      
children
=
[
]
    
IDLNode
.
__init__
(
self
'
File
'
name
1
0
attrs
+
children
)
    
self
.
release_map
=
IDLReleaseMap
(
[
(
'
M13
'
1
.
0
'
stable
'
)
]
)
def
StringTest
(
)
:
  
errors
=
0
  
name_str
=
'
MyName
'
  
text_str
=
'
MyNode
(
%
s
)
'
%
name_str
  
name_node
=
IDLAttribute
(
'
NAME
'
name_str
)
  
node
=
IDLNode
(
'
MyNode
'
'
no
file
'
1
0
[
name_node
]
)
  
if
node
.
GetName
(
)
!
=
name_str
:
    
ErrOut
.
Log
(
'
GetName
returned
>
%
s
<
not
>
%
s
<
'
%
(
node
.
GetName
(
)
name_str
)
)
    
errors
+
=
1
  
if
node
.
GetProperty
(
'
NAME
'
)
!
=
name_str
:
    
ErrOut
.
Log
(
'
Failed
to
get
name
property
.
'
)
    
errors
+
=
1
  
if
str
(
node
)
!
=
text_str
:
    
ErrOut
.
Log
(
'
str
(
)
returned
>
%
s
<
not
>
%
s
<
'
%
(
str
(
node
)
text_str
)
)
    
errors
+
=
1
  
if
not
errors
:
    
InfoOut
.
Log
(
'
Passed
StringTest
'
)
  
return
errors
def
ChildTest
(
)
:
  
errors
=
0
  
child
=
IDLNode
(
'
child
'
'
no
file
'
1
0
)
  
parent
=
IDLNode
(
'
parent
'
'
no
file
'
1
0
[
child
]
)
  
if
child
.
parent
!
=
parent
:
    
ErrOut
.
Log
(
'
Failed
to
connect
parent
.
'
)
    
errors
+
=
1
  
if
[
child
]
!
=
parent
.
GetChildren
(
)
:
    
ErrOut
.
Log
(
'
Failed
GetChildren
.
'
)
    
errors
+
=
1
  
if
child
!
=
parent
.
GetOneOf
(
'
child
'
)
:
    
ErrOut
.
Log
(
'
Failed
GetOneOf
(
child
)
'
)
    
errors
+
=
1
  
if
parent
.
GetOneOf
(
'
bogus
'
)
:
    
ErrOut
.
Log
(
'
Failed
GetOneOf
(
bogus
)
'
)
    
errors
+
=
1
  
if
not
parent
.
IsA
(
'
parent
'
)
:
    
ErrOut
.
Log
(
'
Expecting
parent
type
'
)
    
errors
+
=
1
  
parent
=
IDLNode
(
'
parent
'
'
no
file
'
1
0
[
child
child
]
)
  
if
[
child
child
]
!
=
parent
.
GetChildren
(
)
:
    
ErrOut
.
Log
(
'
Failed
GetChildren2
.
'
)
    
errors
+
=
1
  
if
not
errors
:
    
InfoOut
.
Log
(
'
Passed
ChildTest
'
)
  
return
errors
def
Main
(
)
:
  
errors
=
StringTest
(
)
  
errors
+
=
ChildTest
(
)
  
if
errors
:
    
ErrOut
.
Log
(
'
IDLNode
failed
with
%
d
errors
.
'
%
errors
)
    
return
-
1
  
return
0
if
__name__
=
=
'
__main__
'
:
  
sys
.
exit
(
Main
(
)
)
