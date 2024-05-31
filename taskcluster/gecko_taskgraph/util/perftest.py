def
is_external_browser
(
label
)
:
    
if
any
(
        
external_browser
in
label
        
for
external_browser
in
(
            
"
safari
"
            
"
chrome
"
            
"
custom
-
car
"
        
)
    
)
:
        
return
True
    
return
False
