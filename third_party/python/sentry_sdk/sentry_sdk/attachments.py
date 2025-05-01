import
os
import
mimetypes
from
sentry_sdk
.
_types
import
MYPY
from
sentry_sdk
.
envelope
import
Item
PayloadRef
if
MYPY
:
    
from
typing
import
Optional
Union
Callable
class
Attachment
(
object
)
:
    
def
__init__
(
        
self
        
bytes
=
None
        
filename
=
None
        
path
=
None
        
content_type
=
None
        
add_to_transactions
=
False
    
)
:
        
if
bytes
is
None
and
path
is
None
:
            
raise
TypeError
(
"
path
or
raw
bytes
required
for
attachment
"
)
        
if
filename
is
None
and
path
is
not
None
:
            
filename
=
os
.
path
.
basename
(
path
)
        
if
filename
is
None
:
            
raise
TypeError
(
"
filename
is
required
for
attachment
"
)
        
if
content_type
is
None
:
            
content_type
=
mimetypes
.
guess_type
(
filename
)
[
0
]
        
self
.
bytes
=
bytes
        
self
.
filename
=
filename
        
self
.
path
=
path
        
self
.
content_type
=
content_type
        
self
.
add_to_transactions
=
add_to_transactions
    
def
to_envelope_item
(
self
)
:
        
"
"
"
Returns
an
envelope
item
for
this
attachment
.
"
"
"
        
payload
=
None
        
if
self
.
bytes
is
not
None
:
            
if
callable
(
self
.
bytes
)
:
                
payload
=
self
.
bytes
(
)
            
else
:
                
payload
=
self
.
bytes
        
else
:
            
payload
=
PayloadRef
(
path
=
self
.
path
)
        
return
Item
(
            
payload
=
payload
            
type
=
"
attachment
"
            
content_type
=
self
.
content_type
            
filename
=
self
.
filename
        
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
Attachment
%
r
>
"
%
(
self
.
filename
)
