from
urllib
.
parse
import
quote_plus
import
requests
from
mozbuild
.
vendor
.
host_base
import
BaseHost
def
taskcluster_indexed_artifact_url
(
index_name
artifact_path
)
:
    
artifact_path
=
quote_plus
(
artifact_path
)
    
return
(
        
"
https
:
/
/
firefox
-
ci
-
tc
.
services
.
mozilla
.
com
/
"
        
f
"
api
/
index
/
v1
/
task
/
{
index_name
}
/
artifacts
/
{
artifact_path
}
"
    
)
def
get_as_nightly_json
(
version
=
"
latest
"
)
:
    
r
=
requests
.
get
(
        
taskcluster_indexed_artifact_url
(
            
f
"
project
.
application
-
services
.
v2
.
nightly
.
{
version
}
"
            
"
public
/
build
/
nightly
.
json
"
        
)
    
)
    
r
.
raise_for_status
(
)
    
return
r
.
json
(
)
class
ASHost
(
BaseHost
)
:
    
def
upstream_tag
(
self
revision
)
:
        
if
revision
=
=
"
HEAD
"
:
            
index
=
"
latest
"
        
else
:
            
index
=
revision
        
json
=
get_as_nightly_json
(
index
)
        
return
json
[
"
version
"
]
json
[
"
commit
"
]
