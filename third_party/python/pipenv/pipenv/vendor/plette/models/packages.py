import
six
from
.
base
import
DataView
class
Package
(
DataView
)
:
    
"
"
"
A
package
requirement
specified
in
a
Pipfile
.
    
This
is
the
base
class
of
variants
appearing
in
either
[
packages
]
or
    
[
dev
-
packages
]
sections
of
a
Pipfile
.
    
"
"
"
    
__SCHEMA__
=
{
        
"
__package__
"
:
{
            
"
oneof_type
"
:
[
"
string
"
"
dict
"
]
        
}
    
}
    
classmethod
    
def
validate
(
cls
data
)
:
        
return
super
(
Package
cls
)
.
validate
(
{
"
__package__
"
:
data
}
)
    
def
__getattr__
(
self
key
)
:
        
if
isinstance
(
self
.
_data
six
.
string_types
)
:
            
if
key
=
=
"
version
"
:
                
return
self
.
_data
            
raise
AttributeError
(
key
)
        
try
:
            
return
self
.
_data
[
key
]
        
except
KeyError
:
            
pass
        
raise
AttributeError
(
key
)
    
def
__setattr__
(
self
key
value
)
:
        
if
key
=
=
"
_data
"
:
            
super
(
Package
self
)
.
__setattr__
(
key
value
)
        
elif
key
=
=
"
version
"
and
isinstance
(
self
.
_data
six
.
string_types
)
:
            
self
.
_data
=
value
        
else
:
            
self
.
_data
[
key
]
=
value
