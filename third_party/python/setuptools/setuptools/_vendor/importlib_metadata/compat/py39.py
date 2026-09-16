"
"
"
Compatibility
layer
with
Python
3
.
8
/
3
.
9
"
"
"
from
__future__
import
annotations
from
typing
import
TYPE_CHECKING
Any
if
TYPE_CHECKING
:
    
from
.
.
import
Distribution
EntryPoint
else
:
    
Distribution
=
EntryPoint
=
Any
from
.
.
_typing
import
md_none
def
normalized_name
(
dist
:
Distribution
)
-
>
str
|
None
:
    
"
"
"
    
Honor
name
normalization
for
distributions
that
don
'
t
provide
_normalized_name
.
    
"
"
"
    
try
:
        
return
dist
.
_normalized_name
    
except
AttributeError
:
        
from
.
.
import
Prepared
        
return
Prepared
.
normalize
(
            
getattr
(
dist
"
name
"
None
)
or
md_none
(
dist
.
metadata
)
[
'
Name
'
]
        
)
def
ep_matches
(
ep
:
EntryPoint
*
*
params
)
-
>
bool
:
    
"
"
"
    
Workaround
for
EntryPoint
objects
without
the
matches
method
.
    
"
"
"
    
try
:
        
return
ep
.
matches
(
*
*
params
)
    
except
AttributeError
:
        
from
.
.
import
EntryPoint
        
return
EntryPoint
(
ep
.
name
ep
.
value
ep
.
group
)
.
matches
(
*
*
params
)
