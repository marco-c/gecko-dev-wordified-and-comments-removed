from
__future__
import
absolute_import
unicode_literals
import
os
from
voluptuous
import
(
    
Any
    
Extra
    
Optional
    
Required
)
import
taskgraph
from
.
base
import
(
    
TransformSequence
)
from
.
.
util
.
cached_tasks
import
(
    
add_optimization
)
from
.
.
util
.
schema
import
(
    
Schema
    
validate_schema
)
from
.
.
util
.
treeherder
import
(
    
join_symbol
)
CACHE_TYPE
=
'
content
.
v1
'
transforms
=
TransformSequence
(
)
FETCH_SCHEMA
=
Schema
(
{
    
Required
(
'
name
'
)
:
basestring
    
Optional
(
'
job
-
from
'
)
:
basestring
    
Required
(
'
description
'
)
:
basestring
    
Required
(
'
fetch
'
)
:
Any
(
{
        
'
type
'
:
'
static
-
url
'
        
Required
(
'
url
'
)
:
basestring
        
Required
(
'
sha256
'
)
:
basestring
        
Required
(
'
size
'
)
:
int
        
Optional
(
'
gpg
-
signature
'
)
:
{
            
Required
(
'
sig
-
url
'
)
:
basestring
            
Required
(
'
key
-
path
'
)
:
basestring
        
}
        
Optional
(
'
artifact
-
name
'
)
:
basestring
    
}
)
}
)
transforms
.
add
def
validate
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
        
validate_schema
(
            
FETCH_SCHEMA
job
            
'
In
fetch
task
{
!
r
}
:
'
.
format
(
job
.
get
(
'
name
'
'
unknown
'
)
)
)
        
yield
job
transforms
.
add
def
process_fetch_job
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
        
typ
=
job
[
'
fetch
'
]
[
'
type
'
]
        
if
typ
=
=
'
static
-
url
'
:
            
yield
create_fetch_url_task
(
config
job
)
        
else
:
            
assert
False
def
make_base_task
(
config
name
description
command
)
:
    
if
config
.
params
[
'
level
'
]
=
=
'
3
'
:
        
expires
=
'
1000
years
'
    
else
:
        
expires
=
'
28
days
'
    
return
{
        
'
attributes
'
:
{
}
        
'
name
'
:
name
        
'
description
'
:
description
        
'
expires
-
after
'
:
expires
        
'
label
'
:
'
fetch
-
%
s
'
%
name
        
'
run
-
on
-
projects
'
:
[
]
        
'
treeherder
'
:
{
            
'
kind
'
:
'
build
'
            
'
platform
'
:
'
fetch
/
opt
'
            
'
tier
'
:
1
        
}
        
'
run
'
:
{
            
'
using
'
:
'
run
-
task
'
            
'
checkout
'
:
False
            
'
command
'
:
command
        
}
        
'
worker
-
type
'
:
'
aws
-
provisioner
-
v1
/
gecko
-
{
level
}
-
images
'
        
'
worker
'
:
{
            
'
chain
-
of
-
trust
'
:
True
            
'
docker
-
image
'
:
{
'
in
-
tree
'
:
'
fetch
'
}
            
'
env
'
:
{
}
            
'
max
-
run
-
time
'
:
900
        
}
    
}
def
create_fetch_url_task
(
config
job
)
:
    
name
=
job
[
'
name
'
]
    
fetch
=
job
[
'
fetch
'
]
    
artifact_name
=
fetch
.
get
(
'
artifact
-
name
'
)
    
if
not
artifact_name
:
        
artifact_name
=
fetch
[
'
url
'
]
.
split
(
'
/
'
)
[
-
1
]
    
args
=
[
        
'
/
builds
/
worker
/
bin
/
fetch
-
content
'
'
static
-
url
'
        
'
-
-
sha256
'
fetch
[
'
sha256
'
]
        
'
-
-
size
'
'
%
d
'
%
fetch
[
'
size
'
]
    
]
    
env
=
{
}
    
if
'
gpg
-
signature
'
in
fetch
:
        
sig_url
=
fetch
[
'
gpg
-
signature
'
]
[
'
sig
-
url
'
]
.
format
(
url
=
fetch
[
'
url
'
]
)
        
key_path
=
os
.
path
.
join
(
taskgraph
.
GECKO
fetch
[
'
gpg
-
signature
'
]
[
            
'
key
-
path
'
]
)
        
with
open
(
key_path
'
rb
'
)
as
fh
:
            
gpg_key
=
fh
.
read
(
)
        
env
[
'
FETCH_GPG_KEY
'
]
=
gpg_key
        
args
.
extend
(
[
            
'
-
-
gpg
-
sig
-
url
'
sig_url
            
'
-
-
gpg
-
key
-
env
'
'
FETCH_GPG_KEY
'
        
]
)
    
args
.
extend
(
[
        
fetch
[
'
url
'
]
'
/
builds
/
worker
/
artifacts
/
%
s
'
%
artifact_name
    
]
)
    
task
=
make_base_task
(
config
name
job
[
'
description
'
]
args
)
    
task
[
'
treeherder
'
]
[
'
symbol
'
]
=
join_symbol
(
'
Fetch
-
URL
'
name
)
    
task
[
'
worker
'
]
[
'
artifacts
'
]
=
[
{
        
'
type
'
:
'
directory
'
        
'
name
'
:
'
public
'
        
'
path
'
:
'
/
builds
/
worker
/
artifacts
'
    
}
]
    
task
[
'
worker
'
]
[
'
env
'
]
=
env
    
task
[
'
attributes
'
]
[
'
fetch
-
artifact
'
]
=
'
public
/
%
s
'
%
artifact_name
    
if
not
taskgraph
.
fast
:
        
cache_name
=
task
[
'
label
'
]
.
replace
(
'
{
}
-
'
.
format
(
config
.
kind
)
'
'
1
)
        
add_optimization
(
            
config
            
task
            
cache_type
=
CACHE_TYPE
            
cache_name
=
cache_name
            
digest_data
=
[
fetch
[
'
sha256
'
]
'
%
d
'
%
fetch
[
'
size
'
]
artifact_name
]
        
)
    
return
task
