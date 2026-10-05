import
json
PUB_KEY_X
=
"
e8MHlRjtEdoDNghb9pYpIP
-
H
-
zxNYwqbWMthU2dPXdY
"
def
main
(
request
response
)
:
    
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
application
/
json
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
Access
-
Control
-
Allow
-
Origin
"
b
"
*
"
)
    
return
json
.
dumps
(
{
        
"
keys
"
:
[
{
            
"
kty
"
:
"
OKP
"
            
"
crv
"
:
"
Ed25519
"
            
"
x
"
:
PUB_KEY_X
            
"
kid
"
:
"
test_kid
"
            
"
use
"
:
"
sig
"
            
"
alg
"
:
"
EdDSA
"
        
}
]
    
}
)
