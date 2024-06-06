def
does_task_match_release_type
(
task
release_type
)
:
    
return
(
        
task
.
attributes
.
get
(
"
build
-
type
"
)
=
=
release_type
        
or
task
.
attributes
.
get
(
"
release
-
type
"
)
=
=
release_type
    
)
