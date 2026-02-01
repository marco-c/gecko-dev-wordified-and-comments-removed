"
"
"
WebSocket
protocol
versions
13
and
8
.
"
"
"
import
asyncio
import
random
from
functools
import
partial
from
typing
import
Any
Final
Optional
Union
from
.
.
base_protocol
import
BaseProtocol
from
.
.
client_exceptions
import
ClientConnectionResetError
from
.
.
compression_utils
import
ZLibBackend
ZLibCompressor
from
.
helpers
import
(
    
MASK_LEN
    
MSG_SIZE
    
PACK_CLOSE_CODE
    
PACK_LEN1
    
PACK_LEN2
    
PACK_LEN3
    
PACK_RANDBITS
    
websocket_mask
)
from
.
models
import
WS_DEFLATE_TRAILING
WSMsgType
DEFAULT_LIMIT
:
Final
[
int
]
=
2
*
*
16
WEBSOCKET_MAX_SYNC_CHUNK_SIZE
=
5
*
1024
class
WebSocketWriter
:
    
"
"
"
WebSocket
writer
.
    
The
writer
is
responsible
for
sending
messages
to
the
client
.
It
is
    
created
by
the
protocol
when
a
connection
is
established
.
The
writer
    
should
avoid
implementing
any
application
logic
and
should
only
be
    
concerned
with
the
low
-
level
details
of
the
WebSocket
protocol
.
    
"
"
"
    
def
__init__
(
        
self
        
protocol
:
BaseProtocol
        
transport
:
asyncio
.
Transport
        
*
        
use_mask
:
bool
=
False
        
limit
:
int
=
DEFAULT_LIMIT
        
random
:
random
.
Random
=
random
.
Random
(
)
        
compress
:
int
=
0
        
notakeover
:
bool
=
False
    
)
-
>
None
:
        
"
"
"
Initialize
a
WebSocket
writer
.
"
"
"
        
self
.
protocol
=
protocol
        
self
.
transport
=
transport
        
self
.
use_mask
=
use_mask
        
self
.
get_random_bits
=
partial
(
random
.
getrandbits
32
)
        
self
.
compress
=
compress
        
self
.
notakeover
=
notakeover
        
self
.
_closing
=
False
        
self
.
_limit
=
limit
        
self
.
_output_size
=
0
        
self
.
_compressobj
:
Any
=
None
    
async
def
send_frame
(
        
self
message
:
bytes
opcode
:
int
compress
:
Optional
[
int
]
=
None
    
)
-
>
None
:
        
"
"
"
Send
a
frame
over
the
websocket
with
message
as
its
payload
.
"
"
"
        
if
self
.
_closing
and
not
(
opcode
&
WSMsgType
.
CLOSE
)
:
            
raise
ClientConnectionResetError
(
"
Cannot
write
to
closing
transport
"
)
        
rsv
=
0
        
if
(
compress
or
self
.
compress
)
and
opcode
<
8
:
            
rsv
=
0x40
            
if
compress
:
                
compressobj
=
self
.
_make_compress_obj
(
compress
)
            
else
:
                
if
not
self
.
_compressobj
:
                    
self
.
_compressobj
=
self
.
_make_compress_obj
(
self
.
compress
)
                
compressobj
=
self
.
_compressobj
            
message
=
(
                
await
compressobj
.
compress
(
message
)
                
+
compressobj
.
flush
(
                    
ZLibBackend
.
Z_FULL_FLUSH
                    
if
self
.
notakeover
                    
else
ZLibBackend
.
Z_SYNC_FLUSH
                
)
            
)
.
removesuffix
(
WS_DEFLATE_TRAILING
)
        
msg_length
=
len
(
message
)
        
use_mask
=
self
.
use_mask
        
mask_bit
=
0x80
if
use_mask
else
0
        
first_byte
=
0x80
|
rsv
|
opcode
        
if
msg_length
<
126
:
            
header
=
PACK_LEN1
(
first_byte
msg_length
|
mask_bit
)
            
header_len
=
2
        
elif
msg_length
<
65536
:
            
header
=
PACK_LEN2
(
first_byte
126
|
mask_bit
msg_length
)
            
header_len
=
4
        
else
:
            
header
=
PACK_LEN3
(
first_byte
127
|
mask_bit
msg_length
)
            
header_len
=
10
        
if
self
.
transport
.
is_closing
(
)
:
            
raise
ClientConnectionResetError
(
"
Cannot
write
to
closing
transport
"
)
        
if
use_mask
:
            
mask
=
PACK_RANDBITS
(
self
.
get_random_bits
(
)
)
            
message
=
bytearray
(
message
)
            
websocket_mask
(
mask
message
)
            
self
.
transport
.
write
(
header
+
mask
+
message
)
            
self
.
_output_size
+
=
MASK_LEN
        
elif
msg_length
>
MSG_SIZE
:
            
self
.
transport
.
write
(
header
)
            
self
.
transport
.
write
(
message
)
        
else
:
            
self
.
transport
.
write
(
header
+
message
)
        
self
.
_output_size
+
=
header_len
+
msg_length
        
if
self
.
_output_size
>
self
.
_limit
:
            
self
.
_output_size
=
0
            
if
self
.
protocol
.
_paused
:
                
await
self
.
protocol
.
_drain_helper
(
)
    
def
_make_compress_obj
(
self
compress
:
int
)
-
>
ZLibCompressor
:
        
return
ZLibCompressor
(
            
level
=
ZLibBackend
.
Z_BEST_SPEED
            
wbits
=
-
compress
            
max_sync_chunk_size
=
WEBSOCKET_MAX_SYNC_CHUNK_SIZE
        
)
    
async
def
close
(
self
code
:
int
=
1000
message
:
Union
[
bytes
str
]
=
b
"
"
)
-
>
None
:
        
"
"
"
Close
the
websocket
sending
the
specified
code
and
message
.
"
"
"
        
if
isinstance
(
message
str
)
:
            
message
=
message
.
encode
(
"
utf
-
8
"
)
        
try
:
            
await
self
.
send_frame
(
                
PACK_CLOSE_CODE
(
code
)
+
message
opcode
=
WSMsgType
.
CLOSE
            
)
        
finally
:
            
self
.
_closing
=
True
