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
All
Any
Extra
Optional
Required
from
voluptuous
.
validators
import
Length
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
Length
(
max
=
100
)
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
signing
"
)
:
{
        
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
        
Required
(
"
hardened
-
sign
-
config
"
)
:
optionally_keyed_by
(
            
"
hardened
-
signing
-
type
"
            
[
                
{
                    
Optional
(
"
deep
"
)
:
bool
                    
Optional
(
"
runtime
"
)
:
bool
                    
Optional
(
"
force
"
)
:
bool
                    
Optional
(
"
requirements
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
str
                    
)
                    
Optional
(
"
entitlements
"
)
:
optionally_keyed_by
(
                        
"
build
-
platform
"
"
project
"
str
                    
)
                    
Required
(
"
globs
"
)
:
[
str
]
                
}
            
]
        
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
        
Optional
(
"
run
"
)
:
{
            
Optional
(
"
use
-
caches
"
)
:
Any
(
bool
[
str
]
)
        
}
        
Required
(
"
repositories
"
)
:
All
(
            
{
                
str
:
{
                    
Required
(
"
name
"
)
:
str
                    
Optional
(
"
project
-
regex
"
)
:
str
                    
Optional
(
"
ssh
-
secret
-
name
"
)
:
str
                    
Extra
:
str
                
}
            
}
            
Length
(
min
=
1
)
        
)
    
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
"
level
"
{
str
:
str
}
)
}
)
