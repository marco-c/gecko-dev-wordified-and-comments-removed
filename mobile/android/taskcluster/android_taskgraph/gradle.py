def
get_gradle_project
(
task
)
:
    
attributes
=
task
.
get
(
"
attributes
"
{
}
)
    
gradle_project
=
attributes
.
get
(
"
component
"
)
    
if
not
gradle_project
:
        
treeherder_group
=
attributes
.
get
(
"
treeherder
-
group
"
"
"
)
        
if
"
focus
"
in
treeherder_group
:
            
gradle_project
=
"
focus
"
        
elif
"
fenix
"
in
treeherder_group
:
            
gradle_project
=
"
fenix
"
        
else
:
            
gradle_project
=
None
    
return
gradle_project
