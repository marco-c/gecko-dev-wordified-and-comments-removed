import
asyncio
import
websockets
async
def
hello
(
websocket
)
:
    
greeting
=
f
"
Hello
{
websocket
.
username
}
!
"
    
await
websocket
.
send
(
greeting
)
async
def
main
(
)
:
    
async
with
websockets
.
serve
(
        
hello
"
localhost
"
8765
        
create_protocol
=
websockets
.
basic_auth_protocol_factory
(
            
realm
=
"
example
"
credentials
=
(
"
mary
"
"
p
ssw0rd
"
)
        
)
    
)
:
        
await
asyncio
.
Future
(
)
asyncio
.
run
(
main
(
)
)
