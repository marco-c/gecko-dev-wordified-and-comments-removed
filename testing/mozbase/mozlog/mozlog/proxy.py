from
.
structuredlog
import
get_default_logger
class
ProxyLogger
(
object
)
:
    
"
"
"
    
A
ProxyLogger
behaves
like
a
    
:
class
:
mozlog
.
structuredlog
.
StructuredLogger
.
    
Each
method
and
attribute
access
will
be
forwarded
to
the
underlying
    
StructuredLogger
.
    
RuntimeError
will
be
raised
when
the
default
logger
is
not
yet
initialized
.
    
"
"
"
    
def
__init__
(
self
component
=
None
)
:
        
self
.
logger
=
None
        
self
.
_component
=
component
    
def
__getattr__
(
self
name
)
:
        
if
self
.
logger
is
None
:
            
self
.
logger
=
get_default_logger
(
component
=
self
.
_component
)
            
if
self
.
logger
is
None
:
                
raise
RuntimeError
(
"
Default
logger
is
not
initialized
!
"
)
        
return
getattr
(
self
.
logger
name
)
def
get_proxy_logger
(
component
=
None
)
:
    
"
"
"
    
Returns
a
:
class
:
ProxyLogger
for
the
given
component
.
    
"
"
"
    
return
ProxyLogger
(
component
)
