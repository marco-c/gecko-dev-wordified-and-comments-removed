class
InternalError
(
Exception
)
:
    
pass
class
RustCallStatus
(
ctypes
.
Structure
)
:
    
"
"
"
    
Error
runtime
.
    
"
"
"
    
_fields_
=
[
        
(
"
code
"
ctypes
.
c_int8
)
        
(
"
error_buf
"
RustBuffer
)
    
]
    
CALL_SUCCESS
=
0
    
CALL_ERROR
=
1
    
CALL_PANIC
=
2
    
def
__str__
(
self
)
:
        
if
self
.
code
=
=
RustCallStatus
.
CALL_SUCCESS
:
            
return
"
RustCallStatus
(
CALL_SUCCESS
)
"
        
elif
self
.
code
=
=
RustCallStatus
.
CALL_ERROR
:
            
return
"
RustCallStatus
(
CALL_ERROR
)
"
        
elif
self
.
code
=
=
RustCallStatus
.
CALL_PANIC
:
            
return
"
RustCallStatus
(
CALL_PANIC
)
"
        
else
:
            
return
"
RustCallStatus
(
<
invalid
code
>
)
"
def
rust_call
(
fn
*
args
)
:
    
return
rust_call_with_error
(
None
fn
*
args
)
def
rust_call_with_error
(
error_ffi_converter
fn
*
args
)
:
    
call_status
=
RustCallStatus
(
code
=
RustCallStatus
.
CALL_SUCCESS
error_buf
=
RustBuffer
(
0
0
None
)
)
    
args_with_error
=
args
+
(
ctypes
.
byref
(
call_status
)
)
    
result
=
fn
(
*
args_with_error
)
    
if
call_status
.
code
=
=
RustCallStatus
.
CALL_SUCCESS
:
        
return
result
    
elif
call_status
.
code
=
=
RustCallStatus
.
CALL_ERROR
:
        
if
error_ffi_converter
is
None
:
            
call_status
.
error_buf
.
free
(
)
            
raise
InternalError
(
"
rust_call_with_error
:
CALL_ERROR
but
error_ffi_converter
is
None
"
)
        
else
:
            
raise
error_ffi_converter
.
lift
(
call_status
.
error_buf
)
    
elif
call_status
.
code
=
=
RustCallStatus
.
CALL_PANIC
:
        
if
call_status
.
error_buf
.
len
>
0
:
            
msg
=
FfiConverterString
.
lift
(
call_status
.
error_buf
)
        
else
:
            
msg
=
"
Unknown
rust
panic
"
        
raise
InternalError
(
msg
)
    
else
:
        
raise
InternalError
(
"
Invalid
RustCallStatus
code
:
{
}
"
.
format
(
            
call_status
.
code
)
)
FOREIGN_CALLBACK_T
=
ctypes
.
CFUNCTYPE
(
ctypes
.
c_int
ctypes
.
c_ulonglong
ctypes
.
c_ulong
RustBuffer
ctypes
.
POINTER
(
RustBuffer
)
)
