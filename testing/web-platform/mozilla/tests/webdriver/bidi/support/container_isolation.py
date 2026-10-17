import
pytest
container_isolation
=
pytest
.
mark
.
capabilities
(
{
    
"
moz
:
firefoxOptions
"
:
{
        
"
prefs
"
:
{
            
"
remote
.
experimental
.
dynamicstart
.
container
-
isolation
-
enabled
"
:
True
            
"
remote
.
experimental
.
dynamicstart
.
force
-
container
"
:
True
        
}
    
}
}
)
