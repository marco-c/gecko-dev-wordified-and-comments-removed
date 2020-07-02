import
gdb
def
get_header_ptr
(
value
ptr_t
)
:
    
return
value
[
'
header_
'
]
.
cast
(
ptr_t
)
def
get_header_length_and_flags
(
value
)
:
    
flags
=
value
[
'
header_
'
]
    
try
:
        
length
=
value
[
'
length_
'
]
    
except
gdb
.
error
:
        
length
=
flags
>
>
32
        
flags
=
flags
%
2
*
*
32
    
return
length
flags
