import
os
from
taskgraph
.
util
import
taskcluster
as
tc_util
schema
GECKO
=
os
.
path
.
normpath
(
os
.
path
.
realpath
(
os
.
path
.
join
(
__file__
"
.
.
"
"
.
.
"
"
.
.
"
)
)
)
MAX_DEPENDENCIES
=
99
tc_util
.
PRODUCTION_TASKCLUSTER_ROOT_URL
=
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
"
schema
.
EXCEPTED_SCHEMA_IDENTIFIERS
.
extend
(
    
[
        
"
test_name
"
        
"
json_location
"
        
"
video_location
"
    
]
)
def
register
(
graph_config
)
:
    
"
"
"
Used
to
register
Gecko
specific
extensions
.
    
Args
:
        
graph_config
:
The
graph
configuration
object
.
    
"
"
"
    
from
gecko_taskgraph
.
parameters
import
register_parameters
    
from
gecko_taskgraph
import
(
        
target_tasks
    
)
    
register_parameters
(
)
