"
"
"
Reader
for
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
from
typing
import
TYPE_CHECKING
from
.
.
helpers
import
NO_EXTENSIONS
if
TYPE_CHECKING
or
NO_EXTENSIONS
:
    
from
.
reader_py
import
(
        
WebSocketDataQueue
as
WebSocketDataQueuePython
        
WebSocketReader
as
WebSocketReaderPython
    
)
    
WebSocketReader
=
WebSocketReaderPython
    
WebSocketDataQueue
=
WebSocketDataQueuePython
else
:
    
try
:
        
from
.
reader_c
import
(
            
WebSocketDataQueue
as
WebSocketDataQueueCython
            
WebSocketReader
as
WebSocketReaderCython
        
)
        
WebSocketReader
=
WebSocketReaderCython
        
WebSocketDataQueue
=
WebSocketDataQueueCython
    
except
ImportError
:
        
from
.
reader_py
import
(
            
WebSocketDataQueue
as
WebSocketDataQueuePython
            
WebSocketReader
as
WebSocketReaderPython
        
)
        
WebSocketReader
=
WebSocketReaderPython
        
WebSocketDataQueue
=
WebSocketDataQueuePython
