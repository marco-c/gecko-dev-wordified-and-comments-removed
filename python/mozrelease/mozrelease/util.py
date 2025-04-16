from
yaml
.
loader
import
SafeLoader
class
UnicodeLoader
(
SafeLoader
)
:
    
def
construct_yaml_str
(
self
node
)
:
        
return
self
.
construct_scalar
(
node
)
UnicodeLoader
.
add_constructor
(
"
tag
:
yaml
.
org
2002
:
str
"
UnicodeLoader
.
construct_yaml_str
)
def
load
(
stream
)
:
    
"
"
"
    
Parse
the
first
YAML
document
in
a
stream
    
and
produce
the
corresponding
Python
object
.
    
"
"
"
    
loader
=
UnicodeLoader
(
stream
)
    
try
:
        
return
loader
.
get_single_data
(
)
    
finally
:
        
loader
.
dispose
(
)
