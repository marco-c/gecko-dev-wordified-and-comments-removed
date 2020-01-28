#
-
*
-
coding
:
utf
-
8
-
*
-
from
__future__
import
absolute_import
print_function
unicode_literals
from
six
import
text_type
from
voluptuous
import
Any
Required
All
Optional
from
taskgraph
.
util
.
schema
import
(
    
optionally_keyed_by
    
validate_schema
    
Schema
)
def
even_15_minutes
(
minutes
)
:
    
if
minutes
%
15
!
=
0
:
        
raise
ValueError
(
"
minutes
must
be
evenly
divisible
by
15
"
)
cron_yml_schema
=
Schema
(
{
    
'
jobs
'
:
[
{
        
Required
(
'
name
'
)
:
text_type
        
Required
(
'
job
'
)
:
{
            
Required
(
'
type
'
)
:
'
decision
-
task
'
            
Required
(
'
treeherder
-
symbol
'
)
:
text_type
            
Required
(
'
target
-
tasks
-
method
'
)
:
text_type
            
Optional
(
                
'
optimize
-
target
-
tasks
'
                
description
=
'
If
specified
this
indicates
whether
the
target
'
                            
'
tasks
are
eligible
for
optimization
.
Otherwise
'
                            
'
the
default
for
the
project
is
used
.
'
            
)
:
bool
            
Optional
(
                
'
include
-
push
-
tasks
'
                
description
=
'
Whether
tasks
from
the
on
-
push
graph
should
be
re
-
used
'
                            
'
in
the
cron
graph
.
'
            
)
:
bool
            
Optional
(
                
'
rebuild
-
kinds
'
                
description
=
'
Kinds
that
should
not
be
re
-
used
from
the
on
-
push
graph
.
'
            
)
:
[
text_type
]
        
}
        
'
run
-
on
-
projects
'
:
[
text_type
]
        
'
when
'
:
optionally_keyed_by
(
            
'
project
'
            
[
                
{
                    
'
hour
'
:
int
                    
'
minute
'
:
All
(
int
even_15_minutes
)
                    
'
day
'
:
int
                    
'
weekday
'
:
Any
(
'
Monday
'
'
Tuesday
'
'
Wednesday
'
'
Thursday
'
'
Friday
'
                                   
'
Saturday
'
'
Sunday
'
)
                
}
            
]
        
)
    
}
]
}
)
def
validate
(
cron_yml
)
:
    
validate_schema
(
cron_yml_schema
cron_yml
"
Invalid
.
cron
.
yml
:
"
)
