__version__
=
"
3
.
10
.
11
"
from
typing
import
TYPE_CHECKING
Tuple
from
.
import
hdrs
as
hdrs
from
.
client
import
(
    
BaseConnector
    
ClientConnectionError
    
ClientConnectionResetError
    
ClientConnectorCertificateError
    
ClientConnectorDNSError
    
ClientConnectorError
    
ClientConnectorSSLError
    
ClientError
    
ClientHttpProxyError
    
ClientOSError
    
ClientPayloadError
    
ClientProxyConnectionError
    
ClientRequest
    
ClientResponse
    
ClientResponseError
    
ClientSession
    
ClientSSLError
    
ClientTimeout
    
ClientWebSocketResponse
    
ConnectionTimeoutError
    
ContentTypeError
    
Fingerprint
    
InvalidURL
    
InvalidUrlClientError
    
InvalidUrlRedirectClientError
    
NamedPipeConnector
    
NonHttpUrlClientError
    
NonHttpUrlRedirectClientError
    
RedirectClientError
    
RequestInfo
    
ServerConnectionError
    
ServerDisconnectedError
    
ServerFingerprintMismatch
    
ServerTimeoutError
    
SocketTimeoutError
    
TCPConnector
    
TooManyRedirects
    
UnixConnector
    
WSServerHandshakeError
    
request
)
from
.
cookiejar
import
CookieJar
as
CookieJar
DummyCookieJar
as
DummyCookieJar
from
.
formdata
import
FormData
as
FormData
from
.
helpers
import
BasicAuth
ChainMapProxy
ETag
from
.
http
import
(
    
HttpVersion
as
HttpVersion
    
HttpVersion10
as
HttpVersion10
    
HttpVersion11
as
HttpVersion11
    
WebSocketError
as
WebSocketError
    
WSCloseCode
as
WSCloseCode
    
WSMessage
as
WSMessage
    
WSMsgType
as
WSMsgType
)
from
.
multipart
import
(
    
BadContentDispositionHeader
as
BadContentDispositionHeader
    
BadContentDispositionParam
as
BadContentDispositionParam
    
BodyPartReader
as
BodyPartReader
    
MultipartReader
as
MultipartReader
    
MultipartWriter
as
MultipartWriter
    
content_disposition_filename
as
content_disposition_filename
    
parse_content_disposition
as
parse_content_disposition
)
from
.
payload
import
(
    
PAYLOAD_REGISTRY
as
PAYLOAD_REGISTRY
    
AsyncIterablePayload
as
AsyncIterablePayload
    
BufferedReaderPayload
as
BufferedReaderPayload
    
BytesIOPayload
as
BytesIOPayload
    
BytesPayload
as
BytesPayload
    
IOBasePayload
as
IOBasePayload
    
JsonPayload
as
JsonPayload
    
Payload
as
Payload
    
StringIOPayload
as
StringIOPayload
    
StringPayload
as
StringPayload
    
TextIOPayload
as
TextIOPayload
    
get_payload
as
get_payload
    
payload_type
as
payload_type
)
from
.
payload_streamer
import
streamer
as
streamer
from
.
resolver
import
(
    
AsyncResolver
as
AsyncResolver
    
DefaultResolver
as
DefaultResolver
    
ThreadedResolver
as
ThreadedResolver
)
from
.
streams
import
(
    
EMPTY_PAYLOAD
as
EMPTY_PAYLOAD
    
DataQueue
as
DataQueue
    
EofStream
as
EofStream
    
FlowControlDataQueue
as
FlowControlDataQueue
    
StreamReader
as
StreamReader
)
from
.
tracing
import
(
    
TraceConfig
as
TraceConfig
    
TraceConnectionCreateEndParams
as
TraceConnectionCreateEndParams
    
TraceConnectionCreateStartParams
as
TraceConnectionCreateStartParams
    
TraceConnectionQueuedEndParams
as
TraceConnectionQueuedEndParams
    
TraceConnectionQueuedStartParams
as
TraceConnectionQueuedStartParams
    
TraceConnectionReuseconnParams
as
TraceConnectionReuseconnParams
    
TraceDnsCacheHitParams
as
TraceDnsCacheHitParams
    
TraceDnsCacheMissParams
as
TraceDnsCacheMissParams
    
TraceDnsResolveHostEndParams
as
TraceDnsResolveHostEndParams
    
TraceDnsResolveHostStartParams
as
TraceDnsResolveHostStartParams
    
TraceRequestChunkSentParams
as
TraceRequestChunkSentParams
    
TraceRequestEndParams
as
TraceRequestEndParams
    
TraceRequestExceptionParams
as
TraceRequestExceptionParams
    
TraceRequestHeadersSentParams
as
TraceRequestHeadersSentParams
    
TraceRequestRedirectParams
as
TraceRequestRedirectParams
    
TraceRequestStartParams
as
TraceRequestStartParams
    
TraceResponseChunkReceivedParams
as
TraceResponseChunkReceivedParams
)
if
TYPE_CHECKING
:
    
from
.
worker
import
(
        
GunicornUVLoopWebWorker
as
GunicornUVLoopWebWorker
        
GunicornWebWorker
as
GunicornWebWorker
    
)
__all__
:
Tuple
[
str
.
.
.
]
=
(
    
"
hdrs
"
    
"
BaseConnector
"
    
"
ClientConnectionError
"
    
"
ClientConnectionResetError
"
    
"
ClientConnectorCertificateError
"
    
"
ClientConnectorDNSError
"
    
"
ClientConnectorError
"
    
"
ClientConnectorSSLError
"
    
"
ClientError
"
    
"
ClientHttpProxyError
"
    
"
ClientOSError
"
    
"
ClientPayloadError
"
    
"
ClientProxyConnectionError
"
    
"
ClientResponse
"
    
"
ClientRequest
"
    
"
ClientResponseError
"
    
"
ClientSSLError
"
    
"
ClientSession
"
    
"
ClientTimeout
"
    
"
ClientWebSocketResponse
"
    
"
ConnectionTimeoutError
"
    
"
ContentTypeError
"
    
"
Fingerprint
"
    
"
InvalidURL
"
    
"
InvalidUrlClientError
"
    
"
InvalidUrlRedirectClientError
"
    
"
NonHttpUrlClientError
"
    
"
NonHttpUrlRedirectClientError
"
    
"
RedirectClientError
"
    
"
RequestInfo
"
    
"
ServerConnectionError
"
    
"
ServerDisconnectedError
"
    
"
ServerFingerprintMismatch
"
    
"
ServerTimeoutError
"
    
"
SocketTimeoutError
"
    
"
TCPConnector
"
    
"
TooManyRedirects
"
    
"
UnixConnector
"
    
"
NamedPipeConnector
"
    
"
WSServerHandshakeError
"
    
"
request
"
    
"
CookieJar
"
    
"
DummyCookieJar
"
    
"
FormData
"
    
"
BasicAuth
"
    
"
ChainMapProxy
"
    
"
ETag
"
    
"
HttpVersion
"
    
"
HttpVersion10
"
    
"
HttpVersion11
"
    
"
WSMsgType
"
    
"
WSCloseCode
"
    
"
WSMessage
"
    
"
WebSocketError
"
    
"
BadContentDispositionHeader
"
    
"
BadContentDispositionParam
"
    
"
BodyPartReader
"
    
"
MultipartReader
"
    
"
MultipartWriter
"
    
"
content_disposition_filename
"
    
"
parse_content_disposition
"
    
"
AsyncIterablePayload
"
    
"
BufferedReaderPayload
"
    
"
BytesIOPayload
"
    
"
BytesPayload
"
    
"
IOBasePayload
"
    
"
JsonPayload
"
    
"
PAYLOAD_REGISTRY
"
    
"
Payload
"
    
"
StringIOPayload
"
    
"
StringPayload
"
    
"
TextIOPayload
"
    
"
get_payload
"
    
"
payload_type
"
    
"
streamer
"
    
"
AsyncResolver
"
    
"
DefaultResolver
"
    
"
ThreadedResolver
"
    
"
DataQueue
"
    
"
EMPTY_PAYLOAD
"
    
"
EofStream
"
    
"
FlowControlDataQueue
"
    
"
StreamReader
"
    
"
TraceConfig
"
    
"
TraceConnectionCreateEndParams
"
    
"
TraceConnectionCreateStartParams
"
    
"
TraceConnectionQueuedEndParams
"
    
"
TraceConnectionQueuedStartParams
"
    
"
TraceConnectionReuseconnParams
"
    
"
TraceDnsCacheHitParams
"
    
"
TraceDnsCacheMissParams
"
    
"
TraceDnsResolveHostEndParams
"
    
"
TraceDnsResolveHostStartParams
"
    
"
TraceRequestChunkSentParams
"
    
"
TraceRequestEndParams
"
    
"
TraceRequestExceptionParams
"
    
"
TraceRequestHeadersSentParams
"
    
"
TraceRequestRedirectParams
"
    
"
TraceRequestStartParams
"
    
"
TraceResponseChunkReceivedParams
"
    
"
GunicornUVLoopWebWorker
"
    
"
GunicornWebWorker
"
)
def
__dir__
(
)
-
>
Tuple
[
str
.
.
.
]
:
    
return
__all__
+
(
"
__author__
"
"
__doc__
"
)
def
__getattr__
(
name
:
str
)
-
>
object
:
    
global
GunicornUVLoopWebWorker
GunicornWebWorker
    
if
name
in
(
"
GunicornUVLoopWebWorker
"
"
GunicornWebWorker
"
)
:
        
try
:
            
from
.
worker
import
GunicornUVLoopWebWorker
as
guv
GunicornWebWorker
as
gw
        
except
ImportError
:
            
return
None
        
GunicornUVLoopWebWorker
=
guv
        
GunicornWebWorker
=
gw
        
return
guv
if
name
=
=
"
GunicornUVLoopWebWorker
"
else
gw
    
raise
AttributeError
(
f
"
module
{
__name__
}
has
no
attribute
{
name
}
"
)
