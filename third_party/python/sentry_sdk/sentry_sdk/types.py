"
"
"
This
module
contains
type
definitions
for
the
Sentry
SDK
'
s
public
API
.
The
types
are
re
-
exported
from
the
internal
module
sentry_sdk
.
_types
.
Disclaimer
:
Since
types
are
a
form
of
documentation
type
definitions
may
change
in
minor
releases
.
Removing
a
type
would
be
considered
a
breaking
change
and
so
we
will
only
remove
type
definitions
in
major
releases
.
"
"
"
from
typing
import
TYPE_CHECKING
if
TYPE_CHECKING
:
    
from
sentry_sdk
.
_types
import
(
        
Breadcrumb
        
BreadcrumbHint
        
Event
        
EventDataCategory
        
Hint
        
Log
        
MonitorConfig
        
SamplingContext
    
)
else
:
    
from
typing
import
Any
    
Breadcrumb
=
Any
    
BreadcrumbHint
=
Any
    
Event
=
Any
    
EventDataCategory
=
Any
    
Hint
=
Any
    
Log
=
Any
    
MonitorConfig
=
Any
    
SamplingContext
=
Any
__all__
=
(
    
"
Breadcrumb
"
    
"
BreadcrumbHint
"
    
"
Event
"
    
"
EventDataCategory
"
    
"
Hint
"
    
"
Log
"
    
"
MonitorConfig
"
    
"
SamplingContext
"
)
