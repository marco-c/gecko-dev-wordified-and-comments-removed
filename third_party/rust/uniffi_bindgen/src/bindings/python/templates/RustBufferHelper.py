class
FfiConverterPrimitive
:
    
classmethod
    
def
lift
(
cls
value
)
:
        
return
value
    
classmethod
    
def
lower
(
cls
value
)
:
        
return
value
class
FfiConverterRustBuffer
:
    
classmethod
    
def
lift
(
cls
rbuf
)
:
        
with
rbuf
.
consumeWithStream
(
)
as
stream
:
            
return
cls
.
read
(
stream
)
    
classmethod
    
def
lower
(
cls
value
)
:
        
with
RustBuffer
.
allocWithBuilder
(
)
as
builder
:
            
cls
.
write
(
value
builder
)
            
return
builder
.
finalize
(
)
