import
asyncio
import
json
import
secrets
import
websockets
from
connect4
import
PLAYER1
PLAYER2
Connect4
JOIN
=
{
}
WATCH
=
{
}
async
def
error
(
websocket
message
)
:
    
"
"
"
    
Send
an
error
message
.
    
"
"
"
    
event
=
{
        
"
type
"
:
"
error
"
        
"
message
"
:
message
    
}
    
await
websocket
.
send
(
json
.
dumps
(
event
)
)
async
def
replay
(
websocket
game
)
:
    
"
"
"
    
Send
previous
moves
.
    
"
"
"
    
for
player
column
row
in
game
.
moves
.
copy
(
)
:
        
event
=
{
            
"
type
"
:
"
play
"
            
"
player
"
:
player
            
"
column
"
:
column
            
"
row
"
:
row
        
}
        
await
websocket
.
send
(
json
.
dumps
(
event
)
)
async
def
play
(
websocket
game
player
connected
)
:
    
"
"
"
    
Receive
and
process
moves
from
a
player
.
    
"
"
"
    
async
for
message
in
websocket
:
        
event
=
json
.
loads
(
message
)
        
assert
event
[
"
type
"
]
=
=
"
play
"
        
column
=
event
[
"
column
"
]
        
try
:
            
row
=
game
.
play
(
player
column
)
        
except
RuntimeError
as
exc
:
            
await
error
(
websocket
str
(
exc
)
)
            
continue
        
event
=
{
            
"
type
"
:
"
play
"
            
"
player
"
:
player
            
"
column
"
:
column
            
"
row
"
:
row
        
}
        
websockets
.
broadcast
(
connected
json
.
dumps
(
event
)
)
        
if
game
.
winner
is
not
None
:
            
event
=
{
                
"
type
"
:
"
win
"
                
"
player
"
:
game
.
winner
            
}
            
websockets
.
broadcast
(
connected
json
.
dumps
(
event
)
)
async
def
start
(
websocket
)
:
    
"
"
"
    
Handle
a
connection
from
the
first
player
:
start
a
new
game
.
    
"
"
"
    
game
=
Connect4
(
)
    
connected
=
{
websocket
}
    
join_key
=
secrets
.
token_urlsafe
(
12
)
    
JOIN
[
join_key
]
=
game
connected
    
watch_key
=
secrets
.
token_urlsafe
(
12
)
    
WATCH
[
watch_key
]
=
game
connected
    
try
:
        
event
=
{
            
"
type
"
:
"
init
"
            
"
join
"
:
join_key
            
"
watch
"
:
watch_key
        
}
        
await
websocket
.
send
(
json
.
dumps
(
event
)
)
        
await
play
(
websocket
game
PLAYER1
connected
)
    
finally
:
        
del
JOIN
[
join_key
]
        
del
WATCH
[
watch_key
]
async
def
join
(
websocket
join_key
)
:
    
"
"
"
    
Handle
a
connection
from
the
second
player
:
join
an
existing
game
.
    
"
"
"
    
try
:
        
game
connected
=
JOIN
[
join_key
]
    
except
KeyError
:
        
await
error
(
websocket
"
Game
not
found
.
"
)
        
return
    
connected
.
add
(
websocket
)
    
try
:
        
await
replay
(
websocket
game
)
        
await
play
(
websocket
game
PLAYER2
connected
)
    
finally
:
        
connected
.
remove
(
websocket
)
async
def
watch
(
websocket
watch_key
)
:
    
"
"
"
    
Handle
a
connection
from
a
spectator
:
watch
an
existing
game
.
    
"
"
"
    
try
:
        
game
connected
=
WATCH
[
watch_key
]
    
except
KeyError
:
        
await
error
(
websocket
"
Game
not
found
.
"
)
        
return
    
connected
.
add
(
websocket
)
    
try
:
        
await
replay
(
websocket
game
)
        
await
websocket
.
wait_closed
(
)
    
finally
:
        
connected
.
remove
(
websocket
)
async
def
handler
(
websocket
)
:
    
"
"
"
    
Handle
a
connection
and
dispatch
it
according
to
who
is
connecting
.
    
"
"
"
    
message
=
await
websocket
.
recv
(
)
    
event
=
json
.
loads
(
message
)
    
assert
event
[
"
type
"
]
=
=
"
init
"
    
if
"
join
"
in
event
:
        
await
join
(
websocket
event
[
"
join
"
]
)
    
elif
"
watch
"
in
event
:
        
await
watch
(
websocket
event
[
"
watch
"
]
)
    
else
:
        
await
start
(
websocket
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
handler
"
"
8001
)
:
        
await
asyncio
.
Future
(
)
if
__name__
=
=
"
__main__
"
:
    
asyncio
.
run
(
main
(
)
)
