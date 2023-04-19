"
"
"
Add
notifications
via
taskcluster
-
notify
for
release
tasks
"
"
"
from
string
import
Formatter
from
voluptuous
import
ALLOW_EXTRA
Any
Optional
Required
from
taskgraph
.
transforms
.
base
import
TransformSequence
from
taskgraph
.
util
.
schema
import
Schema
optionally_keyed_by
resolve_keyed_by
RELEASE_NOTIFICATIONS_SCHEMA
=
Schema
(
    
{
        
Optional
(
"
notifications
"
)
:
{
            
Required
(
"
emails
"
)
:
optionally_keyed_by
(
"
project
"
"
level
"
[
str
]
)
            
Required
(
"
subject
"
)
:
str
            
Optional
(
"
message
"
)
:
str
            
Optional
(
"
status
-
types
"
)
:
[
                
Any
(
                    
"
on
-
completed
"
                    
"
on
-
defined
"
                    
"
on
-
exception
"
                    
"
on
-
failed
"
                    
"
on
-
pending
"
                    
"
on
-
resolved
"
                    
"
on
-
running
"
                
)
            
]
        
}
    
}
    
extra
=
ALLOW_EXTRA
)
transforms
=
TransformSequence
(
)
transforms
.
add_validate
(
RELEASE_NOTIFICATIONS_SCHEMA
)
class
TitleCaseFormatter
(
Formatter
)
:
    
"
"
"
Support
title
formatter
for
strings
"
"
"
    
def
convert_field
(
self
value
conversion
)
:
        
if
conversion
=
=
"
t
"
:
            
return
str
(
value
)
.
title
(
)
        
super
(
)
.
convert_field
(
value
conversion
)
        
return
value
titleformatter
=
TitleCaseFormatter
(
)
transforms
.
add
def
add_notifications
(
config
jobs
)
:
    
for
job
in
jobs
:
        
label
=
"
{
}
-
{
}
"
.
format
(
config
.
kind
job
[
"
name
"
]
)
        
notifications
=
job
.
pop
(
"
notifications
"
None
)
        
if
notifications
:
            
resolve_keyed_by
(
                
notifications
                
"
emails
"
                
label
                
*
*
{
                    
"
level
"
:
config
.
params
[
"
level
"
]
                    
"
project
"
:
config
.
params
[
"
project
"
]
                
}
            
)
            
emails
=
notifications
[
"
emails
"
]
            
format_kwargs
=
dict
(
                
task
=
job
                
config
=
config
.
__dict__
            
)
            
subject
=
titleformatter
.
format
(
notifications
[
"
subject
"
]
*
*
format_kwargs
)
            
message
=
notifications
.
get
(
"
message
"
notifications
[
"
subject
"
]
)
            
message
=
titleformatter
.
format
(
message
*
*
format_kwargs
)
            
emails
=
[
email
.
format
(
*
*
format_kwargs
)
for
email
in
emails
]
            
status_types
=
notifications
.
get
(
"
status
-
types
"
[
"
on
-
completed
"
]
)
            
for
s
in
status_types
:
                
job
.
setdefault
(
"
routes
"
[
]
)
.
extend
(
                    
[
f
"
notify
.
email
.
{
email
}
.
{
s
}
"
for
email
in
emails
]
                
)
            
job
.
setdefault
(
"
extra
"
{
}
)
.
update
(
                
{
                    
"
notify
"
:
{
                        
"
email
"
:
{
                            
"
subject
"
:
subject
                            
"
content
"
:
message
                        
}
                    
}
                
}
            
)
        
yield
job
