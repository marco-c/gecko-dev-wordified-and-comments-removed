"
"
"
Transforms
for
release
tasks
"
"
"
def
run_on_releases
(
config
jobs
)
:
    
"
"
"
    
Filter
out
jobs
with
run
-
on
-
releases
set
and
that
don
'
t
match
the
    
release_type
paramater
.
    
"
"
"
    
for
job
in
jobs
:
        
release_type
=
config
.
params
[
"
release_type
"
]
        
run_on_release_types
=
job
.
pop
(
"
run
-
on
-
releases
"
None
)
        
if
run_on_release_types
is
None
or
release_type
in
run_on_release_types
:
            
yield
job
