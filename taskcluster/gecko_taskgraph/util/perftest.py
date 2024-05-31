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
            
"
chrome
-
m
"
            
"
cstm
-
car
-
m
"
        
)
    
)
:
        
return
True
    
return
False
