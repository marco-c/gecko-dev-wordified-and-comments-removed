import
hashlib
def
main
(
request
response
)
:
  
if
b
'
key
'
in
request
.
GET
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
  
else
:
    
return
(
400
[
]
b
'
'
)
  
stash_key
=
hashlib
.
md5
(
key
)
.
hexdigest
(
)
  
headers
=
request
.
server
.
stash
.
take
(
stash_key
)
  
if
headers
is
None
:
    
return
(
204
[
]
b
'
'
)
  
return
(
200
[
]
headers
)
