from
pipenv
.
patched
.
notpip
.
_vendor
.
requests
.
models
import
CONTENT_CHUNK_SIZE
Response
from
pipenv
.
patched
.
notpip
.
_internal
.
utils
.
typing
import
MYPY_CHECK_RUNNING
if
MYPY_CHECK_RUNNING
:
    
from
typing
import
Iterator
def
response_chunks
(
response
chunk_size
=
CONTENT_CHUNK_SIZE
)
:
    
"
"
"
Given
a
requests
Response
provide
the
data
chunks
.
    
"
"
"
    
try
:
        
for
chunk
in
response
.
raw
.
stream
(
            
chunk_size
            
decode_content
=
False
        
)
:
            
yield
chunk
    
except
AttributeError
:
        
while
True
:
            
chunk
=
response
.
raw
.
read
(
chunk_size
)
            
if
not
chunk
:
                
break
            
yield
chunk
