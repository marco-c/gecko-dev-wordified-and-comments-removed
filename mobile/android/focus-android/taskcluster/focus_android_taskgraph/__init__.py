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
parameters
"
        
"
job
"
        
"
worker_types
"
        
"
routes
"
        
"
target_tasks
"
        
"
release_promotion
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
