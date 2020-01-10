def
main
(
request
response
)
:
    
token
=
request
.
GET
.
first
(
"
token
"
None
)
    
is_query
=
request
.
GET
.
first
(
"
query
"
None
)
is
not
None
    
with
request
.
server
.
stash
.
lock
:
      
value
=
request
.
server
.
stash
.
take
(
token
)
      
count
=
0
      
if
value
is
not
None
:
        
count
=
int
(
value
)
      
if
is_query
:
        
request
.
server
.
stash
.
put
(
token
count
)
      
else
:
        
count
+
=
1
        
request
.
server
.
stash
.
put
(
token
count
)
    
headers
=
[
]
    
if
is_query
:
      
headers
=
[
(
"
Count
"
count
)
]
    
return
(
200
headers
"
"
)
