from
importlib
import
import_module
def
register
(
graph_config
)
:
    
"
"
"
    
Import
all
modules
that
are
siblings
of
this
one
triggering
decorators
in
    
the
process
.
    
"
"
"
    
_import_modules
(
        
[
            
"
job
"
            
"
parameters
"
            
"
release_promotion
"
            
"
routes
"
            
"
target_tasks
"
            
"
worker_types
"
        
]
    
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
"
.
{
}
"
.
format
(
module
)
package
=
__name__
)
