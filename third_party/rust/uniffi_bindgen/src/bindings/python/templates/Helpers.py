class
InternalError
(
Exception
)
:
    
pass
class
_UniffiRustCallStatus
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
_UniffiRustBuffer
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
_UniffiRustCallStatus
.
CALL_SUCCESS
:
            
return
"
_UniffiRustCallStatus
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
_UniffiRustCallStatus
.
CALL_ERROR
:
            
return
"
_UniffiRustCallStatus
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
_UniffiRustCallStatus
.
CALL_PANIC
:
            
return
"
_UniffiRustCallStatus
(
CALL_PANIC
)
"
        
else
:
            
return
"
_UniffiRustCallStatus
(
<
invalid
code
>
)
"
def
_rust_call
(
fn
*
args
)
:
    
return
_rust_call_with_error
(
None
fn
*
args
)
def
_rust_call_with_error
(
error_ffi_converter
fn
*
args
)
:
    
call_status
=
_UniffiRustCallStatus
(
code
=
_UniffiRustCallStatus
.
CALL_SUCCESS
error_buf
=
_UniffiRustBuffer
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
    
_uniffi_check_call_status
(
error_ffi_converter
call_status
)
    
return
result
def
_uniffi_check_call_status
(
error_ffi_converter
call_status
)
:
    
if
call_status
.
code
=
=
_UniffiRustCallStatus
.
CALL_SUCCESS
:
        
pass
    
elif
call_status
.
code
=
=
_UniffiRustCallStatus
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
_rust_call_with_error
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
_UniffiRustCallStatus
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
_UniffiConverterString
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
_UniffiRustCallStatus
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
_UNIFFI_FOREIGN_CALLBACK_T
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
ctypes
.
POINTER
(
ctypes
.
c_char
)
ctypes
.
c_int
ctypes
.
POINTER
(
_UniffiRustBuffer
)
)
_UNIFFI_FUTURE_CONTINUATION_T
=
ctypes
.
CFUNCTYPE
(
None
ctypes
.
c_size_t
ctypes
.
c_int8
)
