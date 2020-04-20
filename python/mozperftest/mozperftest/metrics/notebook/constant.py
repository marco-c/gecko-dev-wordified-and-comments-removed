import
os
from
pathlib
import
Path
from
types
import
MappingProxyType
from
.
customtransforms
import
custom_single_json_retriever
class
Constant
(
object
)
:
    
"
"
"
A
singleton
class
to
store
all
constants
.
    
"
"
"
    
__instance
=
None
    
def
__new__
(
cls
*
args
*
*
kw
)
:
        
if
cls
.
__instance
is
None
:
            
cls
.
__instance
=
object
.
__new__
(
cls
*
args
*
*
kw
)
        
return
cls
.
__instance
    
def
__init__
(
self
)
:
        
self
.
__here
=
Path
(
os
.
path
.
dirname
(
os
.
path
.
abspath
(
__file__
)
)
)
        
self
.
__predefined_transformers
=
{
            
"
SingleJsonRetriever
"
:
custom_single_json_retriever
.
SingleJsonRetriever
        
}
    
property
    
def
predefined_transformers
(
self
)
:
        
return
MappingProxyType
(
self
.
__predefined_transformers
)
.
copy
(
)
    
property
    
def
here
(
self
)
:
        
return
self
.
__here
