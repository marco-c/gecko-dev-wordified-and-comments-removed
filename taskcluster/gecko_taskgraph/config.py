from
taskgraph
.
util
.
schema
import
Schema
optionally_keyed_by
from
voluptuous
import
Any
Optional
Required
graph_config_schema
=
Schema
(
    
{
        
Required
(
"
trust
-
domain
"
)
:
str
        
Required
(
"
project
-
repo
-
param
-
prefix
"
)
:
str
        
Required
(
"
product
-
dir
"
)
:
str
        
Required
(
"
treeherder
"
)
:
{
            
Required
(
"
group
-
names
"
)
:
{
str
:
str
}
        
}
        
Required
(
"
index
"
)
:
{
Required
(
"
products
"
)
:
[
str
]
}
        
Required
(
"
try
"
)
:
{
            
Required
(
"
ridealong
-
builds
"
)
:
{
str
:
[
str
]
}
        
}
        
Required
(
"
release
-
promotion
"
)
:
{
            
Required
(
"
products
"
)
:
[
str
]
            
Required
(
"
flavors
"
)
:
{
                
str
:
{
                    
Required
(
"
product
"
)
:
str
                    
Required
(
"
target
-
tasks
-
method
"
)
:
str
                    
Optional
(
"
is
-
rc
"
)
:
bool
                    
Optional
(
"
rebuild
-
kinds
"
)
:
[
str
]
                    
Optional
(
"
version
-
bump
"
)
:
bool
                    
Optional
(
"
partial
-
updates
"
)
:
bool
                
}
            
}
        
}
        
Required
(
"
merge
-
automation
"
)
:
{
            
Required
(
"
behaviors
"
)
:
{
                
str
:
{
                    
Optional
(
"
from
-
branch
"
)
:
str
                    
Required
(
"
to
-
branch
"
)
:
str
                    
Optional
(
"
from
-
repo
"
)
:
str
                    
Required
(
"
to
-
repo
"
)
:
str
                    
Required
(
"
version
-
files
"
)
:
[
                        
{
                            
Required
(
"
filename
"
)
:
str
                            
Optional
(
"
new
-
suffix
"
)
:
str
                            
Optional
(
"
version
-
bump
"
)
:
Any
(
"
major
"
"
minor
"
)
                        
}
                    
]
                    
Required
(
"
replacements
"
)
:
[
[
str
]
]
                    
Required
(
"
merge
-
old
-
head
"
)
:
bool
                    
Optional
(
"
base
-
tag
"
)
:
str
                    
Optional
(
"
end
-
tag
"
)
:
str
                    
Optional
(
"
fetch
-
version
-
from
"
)
:
str
                
}
            
}
        
}
        
Required
(
"
scriptworker
"
)
:
{
            
Required
(
"
scope
-
prefix
"
)
:
str
        
}
        
Required
(
"
task
-
priority
"
)
:
optionally_keyed_by
(
            
"
project
"
            
Any
(
                
"
highest
"
                
"
very
-
high
"
                
"
high
"
                
"
medium
"
                
"
low
"
                
"
very
-
low
"
                
"
lowest
"
            
)
        
)
        
Required
(
"
partner
-
urls
"
)
:
{
            
Required
(
"
release
-
partner
-
repack
"
)
:
optionally_keyed_by
(
                
"
release
-
product
"
"
release
-
level
"
"
release
-
type
"
Any
(
str
None
)
            
)
            
Optional
(
"
release
-
partner
-
attribution
"
)
:
optionally_keyed_by
(
                
"
release
-
product
"
"
release
-
level
"
"
release
-
type
"
Any
(
str
None
)
            
)
            
Required
(
"
release
-
eme
-
free
-
repack
"
)
:
optionally_keyed_by
(
                
"
release
-
product
"
"
release
-
level
"
"
release
-
type
"
Any
(
str
None
)
            
)
        
}
        
Required
(
"
workers
"
)
:
{
            
Required
(
"
aliases
"
)
:
{
                
str
:
{
                    
Required
(
"
provisioner
"
)
:
optionally_keyed_by
(
"
level
"
str
)
                    
Required
(
"
implementation
"
)
:
str
                    
Required
(
"
os
"
)
:
str
                    
Required
(
"
worker
-
type
"
)
:
optionally_keyed_by
(
                        
"
level
"
"
release
-
level
"
"
project
"
str
                    
)
                
}
            
}
        
}
        
Required
(
"
mac
-
notarization
"
)
:
{
            
Required
(
"
mac
-
entitlements
"
)
:
optionally_keyed_by
(
                
"
platform
"
"
release
-
level
"
str
            
)
            
Required
(
"
mac
-
requirements
"
)
:
optionally_keyed_by
(
"
platform
"
str
)
        
}
        
Required
(
"
taskgraph
"
)
:
{
            
Optional
(
                
"
register
"
                
description
=
"
Python
function
to
call
to
register
extensions
.
"
            
)
:
str
            
Optional
(
"
decision
-
parameters
"
)
:
str
        
}
        
Required
(
"
expiration
-
policy
"
)
:
optionally_keyed_by
(
"
project
"
{
str
:
str
}
)
    
}
)
