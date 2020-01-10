from
__future__
import
absolute_import
unicode_literals
from
mozbuild
.
shellutil
import
quote
as
shell_quote
import
os
import
re
from
voluptuous
import
(
    
Any
    
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
        
{
            
'
type
'
:
'
chromium
-
fetch
'
            
Required
(
'
script
'
)
:
basestring
            
Required
(
'
platform
'
)
:
basestring
            
Optional
(
'
revision
'
)
:
basestring
            
Required
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
        
{
            
'
type
'
:
'
git
'
            
Required
(
'
repo
'
)
:
basestring
            
Required
(
'
revision
'
)
:
basestring
            
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
            
Optional
(
'
path
-
prefix
'
)
:
basestring
        
}
    
)
}
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
        
if
'
fetch
'
not
in
job
:
            
continue
        
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
        
elif
typ
=
=
'
chromium
-
fetch
'
:
            
yield
create_chromium_fetch_task
(
config
job
)
        
elif
typ
=
=
'
git
'
:
            
yield
create_git_fetch_task
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
def
create_git_fetch_task
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
    
path_prefix
=
fetch
.
get
(
'
path
-
prefix
'
)
    
if
not
path_prefix
:
        
path_prefix
=
fetch
[
'
repo
'
]
.
rstrip
(
'
/
'
)
.
rsplit
(
'
/
'
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
'
{
}
.
tar
.
zst
'
.
format
(
path_prefix
)
    
if
not
re
.
match
(
r
'
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
'
fetch
[
'
revision
'
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
git
-
checkout
-
archive
'
        
'
-
-
path
-
prefix
'
        
path_prefix
        
fetch
[
'
repo
'
]
        
fetch
[
'
revision
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
revision
'
]
path_prefix
artifact_name
]
        
)
    
return
task
def
create_chromium_fetch_task
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
    
workdir
=
'
/
builds
/
worker
'
    
platform
=
fetch
.
get
(
'
platform
'
)
    
revision
=
fetch
.
get
(
'
revision
'
)
    
args
=
'
-
-
platform
'
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
'
-
-
revision
'
+
shell_quote
(
revision
)
    
cmd
=
[
        
'
bash
'
        
'
-
c
'
        
'
cd
{
}
&
&
'
        
'
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
'
.
format
(
            
workdir
fetch
[
'
script
'
]
args
        
)
    
]
    
env
=
{
        
'
UPLOAD_DIR
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
cmd
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
        
)
    
return
task
