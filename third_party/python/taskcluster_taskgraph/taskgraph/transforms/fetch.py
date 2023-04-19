import
os
import
re
import
attr
from
voluptuous
import
Extra
Optional
Required
import
taskgraph
from
.
.
util
import
path
from
.
.
util
.
cached_tasks
import
add_optimization
from
.
.
util
.
schema
import
Schema
validate_schema
from
.
.
util
.
treeherder
import
join_symbol
from
.
base
import
TransformSequence
CACHE_TYPE
=
"
content
.
v1
"
FETCH_SCHEMA
=
Schema
(
    
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
job
-
from
"
)
:
str
        
Required
(
"
description
"
)
:
str
        
Optional
(
"
docker
-
image
"
)
:
object
        
Optional
(
            
"
fetch
-
alias
"
            
description
=
"
An
alias
that
can
be
used
instead
of
the
real
fetch
job
name
in
"
            
"
fetch
stanzas
for
jobs
.
"
        
)
:
str
        
Optional
(
            
"
artifact
-
prefix
"
            
description
=
"
The
prefix
of
the
taskcluster
artifact
being
uploaded
.
"
            
"
Defaults
to
public
/
;
if
it
starts
with
something
other
than
"
            
"
public
/
the
artifact
will
require
scopes
to
access
.
"
        
)
:
str
        
Optional
(
"
attributes
"
)
:
{
str
:
object
}
        
Required
(
"
fetch
"
)
:
{
            
Required
(
"
type
"
)
:
str
            
Extra
:
object
        
}
    
}
)
fetch_builders
=
{
}
attr
.
s
(
frozen
=
True
)
class
FetchBuilder
:
    
schema
=
attr
.
ib
(
type
=
Schema
)
    
builder
=
attr
.
ib
(
)
def
fetch_builder
(
name
schema
)
:
    
schema
=
Schema
(
{
Required
(
"
type
"
)
:
name
}
)
.
extend
(
schema
)
    
def
wrap
(
func
)
:
        
fetch_builders
[
name
]
=
FetchBuilder
(
schema
func
)
        
return
func
    
return
wrap
transforms
=
TransformSequence
(
)
transforms
.
add_validate
(
FETCH_SCHEMA
)
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
"
fetch
"
]
[
"
type
"
]
        
name
=
job
[
"
name
"
]
        
fetch
=
job
.
pop
(
"
fetch
"
)
        
if
typ
not
in
fetch_builders
:
            
raise
Exception
(
f
"
Unknown
fetch
type
{
typ
}
in
fetch
{
name
}
"
)
        
validate_schema
(
fetch_builders
[
typ
]
.
schema
fetch
f
"
In
task
.
fetch
{
name
!
r
}
:
"
)
        
job
.
update
(
configure_fetch
(
config
typ
name
fetch
)
)
        
yield
job
def
configure_fetch
(
config
typ
name
fetch
)
:
    
if
typ
not
in
fetch_builders
:
        
raise
Exception
(
f
"
No
fetch
type
{
typ
}
in
fetch
{
name
}
"
)
    
validate_schema
(
fetch_builders
[
typ
]
.
schema
fetch
f
"
In
task
.
fetch
{
name
!
r
}
:
"
)
    
return
fetch_builders
[
typ
]
.
builder
(
config
name
fetch
)
transforms
.
add
def
make_task
(
config
jobs
)
:
    
if
config
.
params
[
"
level
"
]
=
=
"
3
"
:
        
expires
=
"
1000
years
"
    
else
:
        
expires
=
"
28
days
"
    
for
job
in
jobs
:
        
name
=
job
[
"
name
"
]
        
artifact_prefix
=
job
.
get
(
"
artifact
-
prefix
"
"
public
"
)
        
env
=
job
.
get
(
"
env
"
{
}
)
        
env
.
update
(
{
"
UPLOAD_DIR
"
:
"
/
builds
/
worker
/
artifacts
"
}
)
        
attributes
=
job
.
get
(
"
attributes
"
{
}
)
        
attributes
[
"
fetch
-
artifact
"
]
=
path
.
join
(
artifact_prefix
job
[
"
artifact_name
"
]
)
        
alias
=
job
.
get
(
"
fetch
-
alias
"
)
        
if
alias
:
            
attributes
[
"
fetch
-
alias
"
]
=
alias
        
task
=
{
            
"
attributes
"
:
attributes
            
"
name
"
:
name
            
"
description
"
:
job
[
"
description
"
]
            
"
expires
-
after
"
:
expires
            
"
label
"
:
"
fetch
-
%
s
"
%
name
            
"
run
-
on
-
projects
"
:
[
]
            
"
run
"
:
{
                
"
using
"
:
"
run
-
task
"
                
"
checkout
"
:
False
                
"
command
"
:
job
[
"
command
"
]
            
}
            
"
worker
-
type
"
:
"
images
"
            
"
worker
"
:
{
                
"
chain
-
of
-
trust
"
:
True
                
"
docker
-
image
"
:
job
.
get
(
"
docker
-
image
"
{
"
in
-
tree
"
:
"
fetch
"
}
)
                
"
env
"
:
env
                
"
max
-
run
-
time
"
:
900
                
"
artifacts
"
:
[
                    
{
                        
"
type
"
:
"
directory
"
                        
"
name
"
:
artifact_prefix
                        
"
path
"
:
"
/
builds
/
worker
/
artifacts
"
                    
}
                
]
            
}
        
}
        
if
"
treeherder
"
in
config
.
graph_config
:
            
task
[
"
treeherder
"
]
=
{
                
"
symbol
"
:
join_symbol
(
"
Fetch
"
name
)
                
"
kind
"
:
"
build
"
                
"
platform
"
:
"
fetch
/
opt
"
                
"
tier
"
:
1
            
}
        
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
"
label
"
]
.
replace
(
f
"
{
config
.
kind
}
-
"
"
"
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
job
[
"
digest_data
"
]
            
)
        
yield
task
fetch_builder
(
    
"
static
-
url
"
    
schema
=
{
        
Required
(
"
url
"
)
:
str
        
Required
(
"
sha256
"
)
:
str
        
Required
(
"
size
"
)
:
int
        
Optional
(
"
gpg
-
signature
"
)
:
{
            
Required
(
"
sig
-
url
"
)
:
str
            
Required
(
"
key
-
path
"
)
:
str
        
}
        
Optional
(
"
artifact
-
name
"
)
:
str
        
Optional
(
"
strip
-
components
"
)
:
int
        
Optional
(
"
add
-
prefix
"
)
:
str
        
Optional
(
"
headers
"
)
:
{
            
str
:
str
        
}
    
}
)
def
create_fetch_url_task
(
config
name
fetch
)
:
    
artifact_name
=
fetch
.
get
(
"
artifact
-
name
"
)
    
if
not
artifact_name
:
        
artifact_name
=
fetch
[
"
url
"
]
.
split
(
"
/
"
)
[
-
1
]
    
command
=
[
        
"
fetch
-
content
"
        
"
static
-
url
"
    
]
    
args
=
[
        
"
-
-
sha256
"
        
fetch
[
"
sha256
"
]
        
"
-
-
size
"
        
"
%
d
"
%
fetch
[
"
size
"
]
    
]
    
if
fetch
.
get
(
"
strip
-
components
"
)
:
        
args
.
extend
(
[
"
-
-
strip
-
components
"
"
%
d
"
%
fetch
[
"
strip
-
components
"
]
]
)
    
if
fetch
.
get
(
"
add
-
prefix
"
)
:
        
args
.
extend
(
[
"
-
-
add
-
prefix
"
fetch
[
"
add
-
prefix
"
]
]
)
    
command
.
extend
(
args
)
    
env
=
{
}
    
if
"
gpg
-
signature
"
in
fetch
:
        
sig_url
=
fetch
[
"
gpg
-
signature
"
]
[
"
sig
-
url
"
]
.
format
(
url
=
fetch
[
"
url
"
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
"
gpg
-
signature
"
]
[
"
key
-
path
"
]
)
        
with
open
(
key_path
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
"
FETCH_GPG_KEY
"
]
=
gpg_key
        
command
.
extend
(
            
[
                
"
-
-
gpg
-
sig
-
url
"
                
sig_url
                
"
-
-
gpg
-
key
-
env
"
                
"
FETCH_GPG_KEY
"
            
]
        
)
    
if
"
headers
"
in
fetch
:
        
for
k
v
in
fetch
[
"
headers
"
]
.
items
(
)
:
            
command
.
extend
(
[
"
-
H
"
f
"
{
k
}
:
{
v
}
"
]
)
    
command
.
extend
(
        
[
            
fetch
[
"
url
"
]
            
"
/
builds
/
worker
/
artifacts
/
%
s
"
%
artifact_name
        
]
    
)
    
return
{
        
"
command
"
:
command
        
"
artifact_name
"
:
artifact_name
        
"
env
"
:
env
        
"
digest_data
"
:
args
+
[
artifact_name
]
    
}
fetch_builder
(
    
"
git
"
    
schema
=
{
        
Required
(
"
repo
"
)
:
str
        
Required
(
"
revision
"
)
:
str
        
Optional
(
"
artifact
-
name
"
)
:
str
        
Optional
(
"
path
-
prefix
"
)
:
str
    
}
)
def
create_git_fetch_task
(
config
name
fetch
)
:
    
path_prefix
=
fetch
.
get
(
"
path
-
prefix
"
)
    
if
not
path_prefix
:
        
path_prefix
=
fetch
[
"
repo
"
]
.
rstrip
(
"
/
"
)
.
rsplit
(
"
/
"
1
)
[
-
1
]
    
artifact_name
=
fetch
.
get
(
"
artifact
-
name
"
)
    
if
not
artifact_name
:
        
artifact_name
=
f
"
{
path_prefix
}
.
tar
.
zst
"
    
if
not
re
.
match
(
r
"
[
0
-
9a
-
fA
-
F
]
{
40
}
"
fetch
[
"
revision
"
]
)
:
        
raise
Exception
(
f
'
Revision
is
not
a
sha1
in
fetch
task
"
{
name
}
"
'
)
    
args
=
[
        
"
fetch
-
content
"
        
"
git
-
checkout
-
archive
"
        
"
-
-
path
-
prefix
"
        
path_prefix
        
fetch
[
"
repo
"
]
        
fetch
[
"
revision
"
]
        
"
/
builds
/
worker
/
artifacts
/
%
s
"
%
artifact_name
    
]
    
return
{
        
"
command
"
:
args
        
"
artifact_name
"
:
artifact_name
        
"
digest_data
"
:
[
fetch
[
"
revision
"
]
path_prefix
artifact_name
]
    
}
