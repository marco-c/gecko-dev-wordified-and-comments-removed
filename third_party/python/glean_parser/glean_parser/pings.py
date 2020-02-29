#
-
*
-
coding
:
utf
-
8
-
*
-
"
"
"
Classes
for
managing
the
description
of
pings
.
"
"
"
import
sys
if
sys
.
version_info
<
(
3
6
)
:
    
import
pep487
    
base_object
=
pep487
.
PEP487Object
else
:
    
base_object
=
object
RESERVED_PING_NAMES
=
[
"
baseline
"
"
metrics
"
"
events
"
"
deletion_request
"
]
class
Ping
(
base_object
)
:
    
def
__init__
(
        
self
        
name
        
description
        
bugs
        
notification_emails
        
data_reviews
=
None
        
include_client_id
=
False
        
send_if_empty
=
False
        
reasons
=
None
        
_validated
=
False
    
)
:
        
from
.
import
parser
        
self
.
name
=
name
        
self
.
description
=
description
        
self
.
bugs
=
bugs
        
self
.
notification_emails
=
notification_emails
        
if
data_reviews
is
None
:
            
data_reviews
=
[
]
        
self
.
data_reviews
=
data_reviews
        
self
.
include_client_id
=
include_client_id
        
self
.
send_if_empty
=
send_if_empty
        
if
reasons
is
None
:
            
reasons
=
{
}
        
self
.
reasons
=
reasons
        
if
not
_validated
:
            
data
=
{
"
schema
"
:
parser
.
PINGS_ID
self
.
name
:
self
.
serialize
(
)
}
            
for
error
in
parser
.
validate
(
data
)
:
                
raise
ValueError
(
error
)
    
_generate_enums
=
[
(
"
reason_codes
"
"
ReasonCodes
"
)
]
    
property
    
def
type
(
self
)
:
        
return
"
ping
"
    
property
    
def
reason_codes
(
self
)
:
        
return
sorted
(
list
(
self
.
reasons
.
keys
(
)
)
)
    
def
serialize
(
self
)
:
        
"
"
"
        
Serialize
the
metric
back
to
JSON
object
model
.
        
"
"
"
        
d
=
self
.
__dict__
.
copy
(
)
        
del
d
[
"
name
"
]
        
return
d
