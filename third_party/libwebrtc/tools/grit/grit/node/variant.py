'
'
'
The
<
skeleton
>
element
.
'
'
'
from
__future__
import
print_function
from
grit
.
node
import
base
class
SkeletonNode
(
base
.
Node
)
:
  
'
'
'
A
<
skeleton
>
element
.
'
'
'
  
def
MandatoryAttributes
(
self
)
:
    
return
[
'
expr
'
'
variant_of_revision
'
'
file
'
]
  
def
DefaultAttributes
(
self
)
:
    
'
'
'
If
not
specified
'
encoding
'
will
actually
default
to
the
parent
node
'
s
    
encoding
.
    
'
'
'
    
return
{
'
encoding
'
:
'
'
}
  
def
_ContentType
(
self
)
:
    
if
'
file
'
in
self
.
attrs
:
      
return
self
.
_CONTENT_TYPE_NONE
    
else
:
      
return
self
.
_CONTENT_TYPE_CDATA
  
def
GetEncodingToUse
(
self
)
:
    
if
self
.
attrs
[
'
encoding
'
]
=
=
'
'
:
      
return
self
.
parent
.
attrs
[
'
encoding
'
]
    
else
:
      
return
self
.
attrs
[
'
encoding
'
]
  
def
GetInputPath
(
self
)
:
    
return
self
.
attrs
[
'
file
'
]
