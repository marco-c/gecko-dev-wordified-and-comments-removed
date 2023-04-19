import
os
import
re
import
attr
import
taskgraph
from
mozbuild
.
shellutil
import
quote
as
shell_quote
from
mozpack
import
path
as
mozpath
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
validate_schema
from
taskgraph
.
util
.
treeherder
import
join_symbol
from
voluptuous
import
Any
Extra
Optional
Required
import
gecko_taskgraph
from
.
.
util
.
cached_tasks
import
add_optimization
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
mozpath
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
        
task_expires
=
"
2
days
"
if
attributes
.
get
(
"
cached_task
"
)
is
False
else
expires
        
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
task_expires
            
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
treeherder
"
:
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
                        
"
expires
-
after
"
:
task_expires
                    
}
                
]
            
}
        
}
        
if
job
.
get
(
"
secret
"
None
)
:
            
task
[
"
scopes
"
]
=
[
"
secrets
:
get
:
"
+
job
.
get
(
"
secret
"
)
]
            
task
[
"
worker
"
]
[
"
taskcluster
-
proxy
"
]
=
True
        
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
            
gecko_taskgraph
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
"
r
"
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
Any
(
"
revision
"
"
branch
"
)
)
:
str
        
Optional
(
"
include
-
dot
-
git
"
)
:
bool
        
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
        
Optional
(
"
ssh
-
key
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
"
revision
"
in
fetch
and
"
branch
"
in
fetch
:
        
raise
Exception
(
"
revision
and
branch
cannot
be
used
in
the
same
context
"
)
    
revision_or_branch
=
None
    
if
"
revision
"
in
fetch
:
        
revision_or_branch
=
fetch
[
"
revision
"
]
        
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
    
else
:
        
revision_or_branch
=
fetch
[
"
branch
"
]
    
args
=
[
        
"
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
        
revision_or_branch
        
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
    
ssh_key
=
fetch
.
get
(
"
ssh
-
key
"
)
    
if
ssh_key
:
        
args
.
append
(
"
-
-
ssh
-
key
-
secret
"
)
        
args
.
append
(
ssh_key
)
    
digest_data
=
[
revision_or_branch
path_prefix
artifact_name
]
    
if
fetch
.
get
(
"
include
-
dot
-
git
"
False
)
:
        
args
.
append
(
"
-
-
include
-
dot
-
git
"
)
        
digest_data
.
append
(
"
.
git
"
)
    
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
digest_data
        
"
secret
"
:
ssh_key
    
}
fetch_builder
(
    
"
chromium
-
fetch
"
    
schema
=
{
        
Required
(
"
script
"
)
:
str
        
Required
(
"
platform
"
)
:
str
        
Optional
(
"
revision
"
)
:
str
        
Required
(
"
artifact
-
name
"
)
:
str
    
}
)
def
create_chromium_fetch_task
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
    
workdir
=
"
/
builds
/
worker
"
    
platform
=
fetch
.
get
(
"
platform
"
)
    
revision
=
fetch
.
get
(
"
revision
"
)
    
args
=
"
-
-
platform
"
+
shell_quote
(
platform
)
    
if
revision
:
        
args
+
=
"
-
-
revision
"
+
shell_quote
(
revision
)
    
cmd
=
[
        
"
bash
"
        
"
-
c
"
        
"
cd
{
}
&
&
"
"
/
usr
/
bin
/
python3
{
}
{
}
"
.
format
(
workdir
fetch
[
"
script
"
]
args
)
    
]
    
return
{
        
"
command
"
:
cmd
        
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
            
f
"
revision
=
{
revision
}
"
            
f
"
platform
=
{
platform
}
"
            
f
"
artifact_name
=
{
artifact_name
}
"
        
]
    
}
