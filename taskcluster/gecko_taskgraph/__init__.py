import
os
from
taskgraph
import
config
as
taskgraph_config
from
taskgraph
import
morph
as
taskgraph_morph
from
taskgraph
.
util
import
schema
from
taskgraph
.
util
import
taskcluster
as
tc_util
from
gecko_taskgraph
.
config
import
graph_config_schema
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
taskgraph_config
.
graph_config_schema
=
graph_config_schema
taskgraph_morph
.
registered_morphs
=
[
]
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
        
"
profile_name
"
        
"
target_path
"
        
"
try_task_config
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
    
import
android_taskgraph
    
from
taskgraph
import
generator
    
from
gecko_taskgraph
import
(
        
morph
        
target_tasks
    
)
    
android_taskgraph
.
register
(
graph_config
)
    
from
gecko_taskgraph
.
parameters
import
register_parameters
    
from
gecko_taskgraph
.
util
import
dependencies
    
from
gecko_taskgraph
.
util
.
verify
import
verifications
    
generator
.
verifications
=
verifications
    
register_parameters
(
)
