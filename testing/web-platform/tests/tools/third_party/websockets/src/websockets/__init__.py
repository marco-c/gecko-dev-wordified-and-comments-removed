from
__future__
import
annotations
import
typing
from
.
imports
import
lazy_import
from
.
version
import
version
as
__version__
__all__
=
[
    
"
ClientProtocol
"
    
"
Headers
"
    
"
HeadersLike
"
    
"
MultipleValuesError
"
    
"
AbortHandshake
"
    
"
ConnectionClosed
"
    
"
ConnectionClosedError
"
    
"
ConnectionClosedOK
"
    
"
DuplicateParameter
"
    
"
InvalidHandshake
"
    
"
InvalidHeader
"
    
"
InvalidHeaderFormat
"
    
"
InvalidHeaderValue
"
    
"
InvalidMessage
"
    
"
InvalidOrigin
"
    
"
InvalidParameterName
"
    
"
InvalidParameterValue
"
    
"
InvalidState
"
    
"
InvalidStatus
"
    
"
InvalidStatusCode
"
    
"
InvalidUpgrade
"
    
"
InvalidURI
"
    
"
NegotiationError
"
    
"
PayloadTooBig
"
    
"
ProtocolError
"
    
"
RedirectHandshake
"
    
"
SecurityError
"
    
"
WebSocketException
"
    
"
WebSocketProtocolError
"
    
"
BasicAuthWebSocketServerProtocol
"
    
"
basic_auth_protocol_factory
"
    
"
WebSocketClientProtocol
"
    
"
connect
"
    
"
unix_connect
"
    
"
WebSocketCommonProtocol
"
    
"
broadcast
"
    
"
WebSocketServer
"
    
"
WebSocketServerProtocol
"
    
"
serve
"
    
"
unix_serve
"
    
"
ServerProtocol
"
    
"
Data
"
    
"
ExtensionName
"
    
"
ExtensionParameter
"
    
"
LoggerLike
"
    
"
StatusLike
"
    
"
Origin
"
    
"
Subprotocol
"
]
if
typing
.
TYPE_CHECKING
:
    
from
.
client
import
ClientProtocol
    
from
.
datastructures
import
Headers
HeadersLike
MultipleValuesError
    
from
.
exceptions
import
(
        
AbortHandshake
        
ConnectionClosed
        
ConnectionClosedError
        
ConnectionClosedOK
        
DuplicateParameter
        
InvalidHandshake
        
InvalidHeader
        
InvalidHeaderFormat
        
InvalidHeaderValue
        
InvalidMessage
        
InvalidOrigin
        
InvalidParameterName
        
InvalidParameterValue
        
InvalidState
        
InvalidStatus
        
InvalidStatusCode
        
InvalidUpgrade
        
InvalidURI
        
NegotiationError
        
PayloadTooBig
        
ProtocolError
        
RedirectHandshake
        
SecurityError
        
WebSocketException
        
WebSocketProtocolError
    
)
    
from
.
legacy
.
auth
import
(
        
BasicAuthWebSocketServerProtocol
        
basic_auth_protocol_factory
    
)
    
from
.
legacy
.
client
import
WebSocketClientProtocol
connect
unix_connect
    
from
.
legacy
.
protocol
import
WebSocketCommonProtocol
broadcast
    
from
.
legacy
.
server
import
(
        
WebSocketServer
        
WebSocketServerProtocol
        
serve
        
unix_serve
    
)
    
from
.
server
import
ServerProtocol
    
from
.
typing
import
(
        
Data
        
ExtensionName
        
ExtensionParameter
        
LoggerLike
        
Origin
        
StatusLike
        
Subprotocol
    
)
else
:
    
lazy_import
(
        
globals
(
)
        
aliases
=
{
            
"
ClientProtocol
"
:
"
.
client
"
            
"
Headers
"
:
"
.
datastructures
"
            
"
HeadersLike
"
:
"
.
datastructures
"
            
"
MultipleValuesError
"
:
"
.
datastructures
"
            
"
AbortHandshake
"
:
"
.
exceptions
"
            
"
ConnectionClosed
"
:
"
.
exceptions
"
            
"
ConnectionClosedError
"
:
"
.
exceptions
"
            
"
ConnectionClosedOK
"
:
"
.
exceptions
"
            
"
DuplicateParameter
"
:
"
.
exceptions
"
            
"
InvalidHandshake
"
:
"
.
exceptions
"
            
"
InvalidHeader
"
:
"
.
exceptions
"
            
"
InvalidHeaderFormat
"
:
"
.
exceptions
"
            
"
InvalidHeaderValue
"
:
"
.
exceptions
"
            
"
InvalidMessage
"
:
"
.
exceptions
"
            
"
InvalidOrigin
"
:
"
.
exceptions
"
            
"
InvalidParameterName
"
:
"
.
exceptions
"
            
"
InvalidParameterValue
"
:
"
.
exceptions
"
            
"
InvalidState
"
:
"
.
exceptions
"
            
"
InvalidStatus
"
:
"
.
exceptions
"
            
"
InvalidStatusCode
"
:
"
.
exceptions
"
            
"
InvalidUpgrade
"
:
"
.
exceptions
"
            
"
InvalidURI
"
:
"
.
exceptions
"
            
"
NegotiationError
"
:
"
.
exceptions
"
            
"
PayloadTooBig
"
:
"
.
exceptions
"
            
"
ProtocolError
"
:
"
.
exceptions
"
            
"
RedirectHandshake
"
:
"
.
exceptions
"
            
"
SecurityError
"
:
"
.
exceptions
"
            
"
WebSocketException
"
:
"
.
exceptions
"
            
"
WebSocketProtocolError
"
:
"
.
exceptions
"
            
"
BasicAuthWebSocketServerProtocol
"
:
"
.
legacy
.
auth
"
            
"
basic_auth_protocol_factory
"
:
"
.
legacy
.
auth
"
            
"
WebSocketClientProtocol
"
:
"
.
legacy
.
client
"
            
"
connect
"
:
"
.
legacy
.
client
"
            
"
unix_connect
"
:
"
.
legacy
.
client
"
            
"
WebSocketCommonProtocol
"
:
"
.
legacy
.
protocol
"
            
"
broadcast
"
:
"
.
legacy
.
protocol
"
            
"
WebSocketServer
"
:
"
.
legacy
.
server
"
            
"
WebSocketServerProtocol
"
:
"
.
legacy
.
server
"
            
"
serve
"
:
"
.
legacy
.
server
"
            
"
unix_serve
"
:
"
.
legacy
.
server
"
            
"
ServerProtocol
"
:
"
.
server
"
            
"
Data
"
:
"
.
typing
"
            
"
ExtensionName
"
:
"
.
typing
"
            
"
ExtensionParameter
"
:
"
.
typing
"
            
"
LoggerLike
"
:
"
.
typing
"
            
"
Origin
"
:
"
.
typing
"
            
"
StatusLike
"
:
"
typing
"
            
"
Subprotocol
"
:
"
.
typing
"
        
}
        
deprecated_aliases
=
{
            
"
framing
"
:
"
.
legacy
"
            
"
handshake
"
:
"
.
legacy
"
            
"
parse_uri
"
:
"
.
uri
"
            
"
WebSocketURI
"
:
"
.
uri
"
        
}
    
)
