from
importlib
import
import_module
from
taskgraph
.
config
import
validate_graph_config
from
taskgraph
.
util
import
schema
schema
.
EXCEPTED_SCHEMA_IDENTIFIERS
.
extend
(
    
[
        
"
bitrise
"
    
]
)
def
register
(
graph_config
)
:
    
_import_modules
(
        
[
            
"
actions
"
            
"
config
"
            
"
worker_types
"
        
]
    
)
    
validate_graph_config
(
graph_config
.
_config
)
def
_import_modules
(
modules
)
:
    
for
module
in
modules
:
        
import_module
(
f
"
.
{
module
}
"
package
=
__name__
)
