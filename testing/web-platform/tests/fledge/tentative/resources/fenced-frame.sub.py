def
main
(
request
response
)
:
    
response
.
status
=
(
200
b
"
OK
"
)
    
response
.
headers
.
set
(
b
"
Content
-
Type
"
b
"
text
/
html
"
)
    
response
.
headers
.
set
(
b
"
Supports
-
Loading
-
Mode
"
b
"
fenced
-
frame
"
)
    
return
"
"
"
        
<
!
DOCTYPE
html
>
        
<
html
>
        
<
body
>
        
<
script
>
        
{
{
GET
[
script
]
}
}
        
<
/
script
>
        
<
/
body
>
        
<
/
html
>
     
"
"
"
