from
gecko_taskgraph
.
util
.
copy_task
import
copy_task
def
merge_to
(
source
dest
)
:
    
"
"
"
    
Merge
dict
and
arrays
(
override
scalar
values
)
    
Keys
from
source
override
keys
from
dest
and
elements
from
lists
in
source
    
are
appended
to
lists
in
dest
.
    
:
param
dict
source
:
to
copy
from
    
:
param
dict
dest
:
to
copy
to
(
modified
in
place
)
    
"
"
"
    
for
key
value
in
source
.
items
(
)
:
        
if
(
            
isinstance
(
value
dict
)
            
and
len
(
value
)
=
=
1
            
and
list
(
value
)
[
0
]
.
startswith
(
"
by
-
"
)
        
)
:
            
dest
[
key
]
=
value
            
continue
        
if
type
(
value
)
!
=
type
(
dest
.
get
(
key
)
)
:
            
dest
[
key
]
=
value
            
continue
        
if
isinstance
(
value
dict
)
:
            
merge_to
(
value
dest
[
key
]
)
            
continue
        
if
isinstance
(
value
list
)
:
            
dest
[
key
]
=
dest
[
key
]
+
value
            
continue
        
dest
[
key
]
=
value
    
return
dest
def
merge
(
*
objects
)
:
    
"
"
"
    
Merge
the
given
objects
using
the
semantics
described
for
merge_to
with
    
objects
later
in
the
list
taking
precedence
.
From
an
inheritance
    
perspective
"
parents
"
should
be
listed
before
"
children
"
.
    
Returns
the
result
without
modifying
any
arguments
.
    
"
"
"
    
if
len
(
objects
)
=
=
1
:
        
return
copy_task
(
objects
[
0
]
)
    
return
merge_to
(
objects
[
-
1
]
merge
(
*
objects
[
:
-
1
]
)
)
