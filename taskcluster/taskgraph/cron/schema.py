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
basestring
        
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
basestring
            
'
target
-
tasks
-
method
'
:
basestring
            
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
basestring
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
