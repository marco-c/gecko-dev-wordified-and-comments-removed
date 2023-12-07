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
_UNIFFI_RUST_TASK_CALLBACK_SUCCESS
=
0
_UNIFFI_RUST_TASK_CALLBACK_CANCELLED
=
1
_UNIFFI_FOREIGN_EXECUTOR_CALLBACK_SUCCESS
=
0
_UNIFFI_FOREIGN_EXECUTOR_CALLBACK_CANCELED
=
1
_UNIFFI_FOREIGN_EXECUTOR_CALLBACK_ERROR
=
2
class
{
{
ffi_converter_name
}
}
:
    
_pointer_manager
=
_UniffiPointerManager
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
_uniffi_executor_callback
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
write_c_size_t
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
read_c_size_t
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
_UNIFFI_FOREIGN_EXECUTOR_CALLBACK_T
def
_uniffi_executor_callback
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
        
return
_UNIFFI_FOREIGN_EXECUTOR_CALLBACK_SUCCESS
    
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
        
if
eventloop
.
is_closed
(
)
:
            
return
_UNIFFI_FOREIGN_EXECUTOR_CALLBACK_CANCELED
        
callback
=
_UNIFFI_RUST_TASK
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
                                           
_UNIFFI_FOREIGN_EXECUTOR_CALLBACK_SUCCESS
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
_UNIFFI_FOREIGN_EXECUTOR_CALLBACK_SUCCESS
)
        
return
_UNIFFI_FOREIGN_EXECUTOR_CALLBACK_SUCCESS
{
%
-
match
ci
.
ffi_foreign_executor_callback_set
(
)
%
}
{
%
-
when
Some
with
(
fn
)
%
}
_UniffiLib
.
{
{
fn
.
name
(
)
}
}
(
_uniffi_executor_callback
)
{
%
-
when
None
%
}
{
{
%
endmatch
%
}
