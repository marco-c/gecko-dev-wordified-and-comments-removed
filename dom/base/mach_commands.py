from
mach
.
decorators
import
Command
Command
(
    
"
gen
-
use
-
counter
-
metrics
"
    
category
=
"
misc
"
    
description
=
"
Generate
a
Glean
use_counter_metrics
.
yaml
file
creating
metrics
definitions
for
every
use
counter
.
"
)
def
gen_use_counter_metrics
(
command_context
)
:
    
import
sys
    
from
os
import
path
    
sys
.
path
.
append
(
path
.
dirname
(
__file__
)
)
    
from
usecounters
import
gen_use_counter_metrics
    
return
gen_use_counter_metrics
(
)
