from
__future__
import
absolute_import
unicode_literals
import
attr
from
mozbuild
.
shellutil
import
quote
as
shell_quote
import
io
import
os
import
re
from
six
import
text_type
from
voluptuous
import
(
    
Optional
    
Required
    
Extra
    
Any
)
from
mozpack
import
path
as
mozpath
import
taskgraph
from
.
base
import
TransformSequence
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
text_type
        
Optional
(
"
job
-
from
"
)
:
text_type
        
Required
(
"
description
"
)
:
text_type
        
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
text_type
        
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
text_type
        
Optional
(
"
attributes
"
)
:
{
text_type
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
text_type
            
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
(
object
)
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
"
Unknown
fetch
type
{
}
in
fetch
{
}
"
.
format
(
typ
name
)
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
"
In
task
.
fetch
{
!
r
}
:
"
.
format
(
name
)
        
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
"
No
fetch
type
{
}
in
fetch
{
}
"
.
format
(
typ
name
)
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
"
In
task
.
fetch
{
!
r
}
:
"
.
format
(
name
)
    
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
"
{
}
-
"
.
format
(
config
.
kind
)
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
text_type
        
Required
(
"
sha256
"
)
:
text_type
        
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
text_type
            
Required
(
"
key
-
path
"
)
:
text_type
        
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
text_type
        
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
text_type
    
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
io
.
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
text_type
        
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
text_type
        
Optional
(
"
artifact
-
name
"
)
:
text_type
        
Optional
(
"
path
-
prefix
"
)
:
text_type
        
Optional
(
"
ssh
-
key
"
)
:
text_type
    
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
"
{
}
.
tar
.
zst
"
.
format
(
path_prefix
)
    
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
}
"
'
.
format
(
name
)
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
revision_or_branch
path_prefix
artifact_name
]
        
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
text_type
        
Required
(
"
platform
"
)
:
text_type
        
Optional
(
"
revision
"
)
:
text_type
        
Required
(
"
artifact
-
name
"
)
:
text_type
    
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
            
"
revision
=
{
}
"
.
format
(
revision
)
            
"
platform
=
{
}
"
.
format
(
platform
)
            
"
artifact_name
=
{
}
"
.
format
(
artifact_name
)
        
]
    
}
