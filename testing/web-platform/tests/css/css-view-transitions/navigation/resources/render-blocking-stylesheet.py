import
time
def
main
(
request
response
)
:
    
key
=
request
.
GET
.
first
(
b
'
key
'
)
    
if
request
.
method
=
=
'
POST
'
:
        
request
.
server
.
stash
.
put
(
key
'
doResponse
'
)
        
return
'
done
'
    
else
:
        
poll_delay_sec
=
0
.
1
        
while
request
.
server
.
stash
.
take
(
key
)
is
None
:
            
time
.
sleep
(
poll_delay_sec
)
        
status
=
200
        
headers
=
[
(
'
Content
-
Type
'
'
text
/
css
'
)
]
        
body
=
'
'
        
return
(
status
headers
body
)
