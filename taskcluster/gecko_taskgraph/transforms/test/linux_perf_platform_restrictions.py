TALOS_DUAL_PLATFORM_TESTS
=
{
    
"
talos
-
chrome
"
    
"
talos
-
damp
-
inspector
"
    
"
talos
-
damp
-
webconsole
"
}
PERFTEST_DUAL_PLATFORM_TESTS
=
{
    
"
tr8ns
-
perf
-
base
"
    
"
tr8ns
-
perf
-
basememory
"
    
"
tr8ns
-
perf
-
tiny
"
}
def
restrict_tests_to_2404
(
config
tasks
)
:
    
"
"
"
    
Bug
2021939
-
Restrict
most
perf
tests
to
Ubuntu
24
.
04
by
dropping
linux1804
    
tasks
that
are
not
in
the
explicit
exception
lists
.
Tests
in
    
TALOS_DUAL_PLATFORM_TESTS
keep
both
platforms
.
    
"
"
"
    
for
task
in
tasks
:
        
if
"
linux1804
"
not
in
task
.
get
(
"
test
-
platform
"
"
"
)
:
            
yield
task
            
continue
        
test_name
=
task
.
get
(
"
test
-
name
"
"
"
)
        
if
task
.
get
(
"
suite
"
)
=
=
"
talos
"
:
            
if
test_name
in
TALOS_DUAL_PLATFORM_TESTS
:
                
yield
task
            
continue
        
yield
task
def
restrict_perftest_to_2404
(
config
jobs
)
:
    
"
"
"
    
Bug
2021939
-
Restrict
perftest
jobs
to
Ubuntu
24
.
04
.
Remove
linux1804
    
from
the
platform
list
of
each
job
.
Jobs
in
PERFTEST_DUAL_PLATFORM_TESTS
    
keep
both
platforms
.
    
"
"
"
    
for
job
in
jobs
:
        
platforms
=
job
.
get
(
"
platform
"
)
        
if
job
.
get
(
"
name
"
"
"
)
not
in
PERFTEST_DUAL_PLATFORM_TESTS
and
isinstance
(
            
platforms
list
        
)
:
            
filtered
=
[
p
for
p
in
platforms
if
"
linux1804
"
not
in
p
]
            
if
len
(
filtered
)
<
len
(
platforms
)
:
                
job
[
"
platform
"
]
=
filtered
        
yield
job
