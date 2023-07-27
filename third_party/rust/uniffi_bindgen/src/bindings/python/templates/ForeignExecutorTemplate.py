{
{
self
.
add_import
(
"
asyncio
"
)
}
}
class
{
{
ffi_converter_name
}
}
:
    
_pointer_manager
=
UniFfiPointerManager
(
)
    
classmethod
    
def
lower
(
cls
eventloop
)
:
        
if
not
isinstance
(
eventloop
asyncio
.
BaseEventLoop
)
:
            
raise
TypeError
(
"
uniffi_executor_callback
:
Expected
EventLoop
instance
"
)
        
return
cls
.
_pointer_manager
.
new_pointer
(
eventloop
)
    
classmethod
    
def
write
(
cls
eventloop
buf
)
:
        
buf
.
writeCSizeT
(
cls
.
lower
(
eventloop
)
)
    
classmethod
    
def
read
(
cls
buf
)
:
        
return
cls
.
lift
(
buf
.
readCSizeT
(
)
)
    
classmethod
    
def
lift
(
cls
value
)
:
        
return
cls
.
_pointer_manager
.
lookup
(
value
)
UNIFFI_FOREIGN_EXECUTOR_CALLBACK_T
def
uniffi_executor_callback
(
eventloop_address
delay
task_ptr
task_data
)
:
    
if
task_ptr
is
None
:
        
{
{
ffi_converter_name
}
}
.
_pointer_manager
.
release_pointer
(
eventloop_address
)
    
else
:
        
eventloop
=
{
{
ffi_converter_name
}
}
.
_pointer_manager
.
lookup
(
eventloop_address
)
        
callback
=
UNIFFI_RUST_TASK
(
task_ptr
)
        
if
delay
=
=
0
:
            
eventloop
.
call_soon_threadsafe
(
callback
task_data
)
        
else
:
            
eventloop
.
call_soon_threadsafe
(
eventloop
.
call_later
delay
/
1000
.
0
callback
task_data
)
_UniFFILib
.
uniffi_foreign_executor_callback_set
(
uniffi_executor_callback
)
