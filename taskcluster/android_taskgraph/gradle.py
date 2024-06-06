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
        
shipping_product
=
attributes
.
get
(
"
shipping
-
product
"
"
"
)
        
if
shipping_product
:
            
return
shipping_product
    
return
gradle_project
