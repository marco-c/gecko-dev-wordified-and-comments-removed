"
"
"
WebSocket
utilities
.
"
"
"
from
__future__
import
absolute_import
import
array
import
errno
import
logging
import
os
import
re
import
six
from
six
.
moves
import
map
from
six
.
moves
import
range
import
socket
import
struct
import
zlib
try
:
    
from
mod_pywebsocket
import
fast_masking
except
ImportError
:
    
pass
def
prepend_message_to_exception
(
message
exc
)
:
    
"
"
"
Prepend
message
to
the
exception
.
"
"
"
    
exc
.
args
=
(
message
+
str
(
exc
)
)
    
return
def
__translate_interp
(
interp
cygwin_path
)
:
    
"
"
"
Translate
interp
program
path
for
Win32
python
to
run
cygwin
program
    
(
e
.
g
.
perl
)
.
Note
that
it
doesn
'
t
support
path
that
contains
space
    
which
is
typically
true
for
Unix
where
#
!
-
script
is
written
.
    
For
Win32
python
cygwin_path
is
a
directory
of
cygwin
binaries
.
    
Args
:
      
interp
:
interp
command
line
      
cygwin_path
:
directory
name
of
cygwin
binary
or
None
    
Returns
:
      
translated
interp
command
line
.
    
"
"
"
    
if
not
cygwin_path
:
        
return
interp
    
m
=
re
.
match
(
'
^
[
^
]
*
/
(
[
^
]
+
)
(
.
*
)
?
'
interp
)
    
if
m
:
        
cmd
=
os
.
path
.
join
(
cygwin_path
m
.
group
(
1
)
)
        
return
cmd
+
m
.
group
(
2
)
    
return
interp
def
get_script_interp
(
script_path
cygwin_path
=
None
)
:
    
r
"
"
"
Get
#
!
-
interpreter
command
line
from
the
script
.
    
It
also
fixes
command
path
.
When
Cygwin
Python
is
used
e
.
g
.
in
WebKit
    
it
could
run
"
/
usr
/
bin
/
perl
-
wT
hello
.
pl
"
.
    
When
Win32
Python
is
used
e
.
g
.
in
Chromium
it
couldn
'
t
.
So
fix
    
"
/
usr
/
bin
/
perl
"
to
"
<
cygwin_path
>
\
perl
.
exe
"
.
    
Args
:
      
script_path
:
pathname
of
the
script
      
cygwin_path
:
directory
name
of
cygwin
binary
or
None
    
Returns
:
      
#
!
-
interpreter
command
line
or
None
if
it
is
not
#
!
-
script
.
    
"
"
"
    
fp
=
open
(
script_path
)
    
line
=
fp
.
readline
(
)
    
fp
.
close
(
)
    
m
=
re
.
match
(
'
^
#
!
(
.
*
)
'
line
)
    
if
m
:
        
return
__translate_interp
(
m
.
group
(
1
)
cygwin_path
)
    
return
None
def
wrap_popen3_for_win
(
cygwin_path
)
:
    
"
"
"
Wrap
popen3
to
support
#
!
-
script
on
Windows
.
    
Args
:
      
cygwin_path
:
path
for
cygwin
binary
if
command
path
is
needed
to
be
                    
translated
.
None
if
no
translation
required
.
    
"
"
"
    
__orig_popen3
=
os
.
popen3
    
def
__wrap_popen3
(
cmd
mode
=
'
t
'
bufsize
=
-
1
)
:
        
cmdline
=
cmd
.
split
(
'
'
)
        
interp
=
get_script_interp
(
cmdline
[
0
]
cygwin_path
)
        
if
interp
:
            
cmd
=
interp
+
'
'
+
cmd
        
return
__orig_popen3
(
cmd
mode
bufsize
)
    
os
.
popen3
=
__wrap_popen3
def
hexify
(
s
)
:
    
return
'
'
.
join
(
[
'
%
02x
'
%
x
for
x
in
six
.
iterbytes
(
s
)
]
)
def
get_class_logger
(
o
)
:
    
"
"
"
Return
the
logging
class
information
.
"
"
"
    
return
logging
.
getLogger
(
'
%
s
.
%
s
'
%
                             
(
o
.
__class__
.
__module__
o
.
__class__
.
__name__
)
)
def
pack_byte
(
b
)
:
    
"
"
"
Pack
an
integer
to
network
-
ordered
byte
"
"
"
    
return
struct
.
pack
(
'
!
B
'
b
)
class
NoopMasker
(
object
)
:
    
"
"
"
A
NoOp
masking
object
.
    
This
has
the
same
interface
as
RepeatedXorMasker
but
just
returns
    
the
string
passed
in
without
making
any
change
.
    
"
"
"
    
def
__init__
(
self
)
:
        
"
"
"
NoOp
.
"
"
"
        
pass
    
def
mask
(
self
s
)
:
        
"
"
"
NoOp
.
"
"
"
        
return
s
class
RepeatedXorMasker
(
object
)
:
    
"
"
"
A
masking
object
that
applies
XOR
on
the
string
.
    
Applies
XOR
on
the
byte
string
given
to
mask
method
with
the
masking
bytes
    
given
to
the
constructor
repeatedly
.
This
object
remembers
the
position
    
in
the
masking
bytes
the
last
mask
method
call
ended
and
resumes
from
    
that
point
on
the
next
mask
method
call
.
    
"
"
"
    
def
__init__
(
self
masking_key
)
:
        
self
.
_masking_key
=
masking_key
        
self
.
_masking_key_index
=
0
    
def
_mask_using_swig
(
self
s
)
:
        
"
"
"
Perform
the
mask
via
SWIG
.
"
"
"
        
masked_data
=
fast_masking
.
mask
(
s
self
.
_masking_key
                                        
self
.
_masking_key_index
)
        
self
.
_masking_key_index
=
(
(
self
.
_masking_key_index
+
len
(
s
)
)
%
                                   
len
(
self
.
_masking_key
)
)
        
return
masked_data
    
def
_mask_using_array
(
self
s
)
:
        
"
"
"
Perform
the
mask
via
python
.
"
"
"
        
if
isinstance
(
s
six
.
text_type
)
:
            
raise
Exception
(
                
'
Masking
Operation
should
not
process
unicode
strings
'
)
        
result
=
bytearray
(
s
)
        
masking_key
=
[
c
for
c
in
six
.
iterbytes
(
self
.
_masking_key
)
]
        
masking_key_size
=
len
(
masking_key
)
        
masking_key_index
=
self
.
_masking_key_index
        
for
i
in
range
(
len
(
result
)
)
:
            
result
[
i
]
^
=
masking_key
[
masking_key_index
]
            
masking_key_index
=
(
masking_key_index
+
1
)
%
masking_key_size
        
self
.
_masking_key_index
=
masking_key_index
        
return
bytes
(
result
)
    
if
'
fast_masking
'
in
globals
(
)
:
        
mask
=
_mask_using_swig
    
else
:
        
mask
=
_mask_using_array
class
_Deflater
(
object
)
:
    
def
__init__
(
self
window_bits
)
:
        
self
.
_logger
=
get_class_logger
(
self
)
        
window_bits
=
max
(
window_bits
9
)
        
self
.
_compress
=
zlib
.
compressobj
(
zlib
.
Z_DEFAULT_COMPRESSION
                                          
zlib
.
DEFLATED
-
window_bits
)
    
def
compress
(
self
bytes
)
:
        
compressed_bytes
=
self
.
_compress
.
compress
(
bytes
)
        
self
.
_logger
.
debug
(
'
Compress
input
%
r
'
bytes
)
        
self
.
_logger
.
debug
(
'
Compress
result
%
r
'
compressed_bytes
)
        
return
compressed_bytes
    
def
compress_and_flush
(
self
bytes
)
:
        
compressed_bytes
=
self
.
_compress
.
compress
(
bytes
)
        
compressed_bytes
+
=
self
.
_compress
.
flush
(
zlib
.
Z_SYNC_FLUSH
)
        
self
.
_logger
.
debug
(
'
Compress
input
%
r
'
bytes
)
        
self
.
_logger
.
debug
(
'
Compress
result
%
r
'
compressed_bytes
)
        
return
compressed_bytes
    
def
compress_and_finish
(
self
bytes
)
:
        
compressed_bytes
=
self
.
_compress
.
compress
(
bytes
)
        
compressed_bytes
+
=
self
.
_compress
.
flush
(
zlib
.
Z_FINISH
)
        
self
.
_logger
.
debug
(
'
Compress
input
%
r
'
bytes
)
        
self
.
_logger
.
debug
(
'
Compress
result
%
r
'
compressed_bytes
)
        
return
compressed_bytes
class
_Inflater
(
object
)
:
    
def
__init__
(
self
window_bits
)
:
        
self
.
_logger
=
get_class_logger
(
self
)
        
self
.
_window_bits
=
window_bits
        
self
.
_unconsumed
=
b
'
'
        
self
.
reset
(
)
    
def
decompress
(
self
size
)
:
        
if
not
(
size
=
=
-
1
or
size
>
0
)
:
            
raise
Exception
(
'
size
must
be
-
1
or
positive
'
)
        
data
=
b
'
'
        
while
True
:
            
data
+
=
self
.
_decompress
.
decompress
(
self
.
_unconsumed
                                                
max
(
0
size
-
len
(
data
)
)
)
            
self
.
_unconsumed
=
self
.
_decompress
.
unconsumed_tail
            
if
self
.
_decompress
.
unused_data
:
                
self
.
_unconsumed
=
self
.
_decompress
.
unused_data
                
self
.
reset
(
)
                
if
size
>
=
0
and
len
(
data
)
=
=
size
:
                    
break
                
else
:
                    
continue
            
else
:
                
break
        
if
data
:
            
self
.
_logger
.
debug
(
'
Decompressed
%
r
'
data
)
        
return
data
    
def
append
(
self
data
)
:
        
self
.
_logger
.
debug
(
'
Appended
%
r
'
data
)
        
self
.
_unconsumed
+
=
data
    
def
reset
(
self
)
:
        
self
.
_logger
.
debug
(
'
Reset
'
)
        
self
.
_decompress
=
zlib
.
decompressobj
(
-
self
.
_window_bits
)
class
_RFC1979Deflater
(
object
)
:
    
"
"
"
A
compressor
class
that
applies
DEFLATE
to
given
byte
sequence
and
    
flushes
using
the
algorithm
described
in
the
RFC1979
section
2
.
1
.
    
"
"
"
    
def
__init__
(
self
window_bits
no_context_takeover
)
:
        
self
.
_deflater
=
None
        
if
window_bits
is
None
:
            
window_bits
=
zlib
.
MAX_WBITS
        
self
.
_window_bits
=
window_bits
        
self
.
_no_context_takeover
=
no_context_takeover
    
def
filter
(
self
bytes
end
=
True
bfinal
=
False
)
:
        
if
self
.
_deflater
is
None
:
            
self
.
_deflater
=
_Deflater
(
self
.
_window_bits
)
        
if
bfinal
:
            
result
=
self
.
_deflater
.
compress_and_finish
(
bytes
)
            
result
=
result
+
pack_byte
(
0
)
            
self
.
_deflater
=
None
            
return
result
        
result
=
self
.
_deflater
.
compress_and_flush
(
bytes
)
        
if
end
:
            
result
=
result
[
:
-
4
]
        
if
self
.
_no_context_takeover
and
end
:
            
self
.
_deflater
=
None
        
return
result
class
_RFC1979Inflater
(
object
)
:
    
"
"
"
A
decompressor
class
a
la
RFC1979
.
    
A
decompressor
class
for
byte
sequence
compressed
and
flushed
following
    
the
algorithm
described
in
the
RFC1979
section
2
.
1
.
    
"
"
"
    
def
__init__
(
self
window_bits
=
zlib
.
MAX_WBITS
)
:
        
self
.
_inflater
=
_Inflater
(
window_bits
)
    
def
filter
(
self
bytes
)
:
        
self
.
_inflater
.
append
(
bytes
+
b
'
\
x00
\
x00
\
xff
\
xff
'
)
        
return
self
.
_inflater
.
decompress
(
-
1
)
class
DeflateSocket
(
object
)
:
    
"
"
"
A
wrapper
class
for
socket
object
to
intercept
send
and
recv
to
perform
    
deflate
compression
and
decompression
transparently
.
    
"
"
"
    
_RECV_SIZE
=
4096
    
def
__init__
(
self
socket
)
:
        
self
.
_socket
=
socket
        
self
.
_logger
=
get_class_logger
(
self
)
        
self
.
_deflater
=
_Deflater
(
zlib
.
MAX_WBITS
)
        
self
.
_inflater
=
_Inflater
(
zlib
.
MAX_WBITS
)
    
def
recv
(
self
size
)
:
        
"
"
"
Receives
data
from
the
socket
specified
on
the
construction
up
        
to
the
specified
size
.
Once
any
data
is
available
returns
it
even
        
if
it
'
s
smaller
than
the
specified
size
.
        
"
"
"
        
if
size
<
=
0
:
            
raise
Exception
(
'
Non
-
positive
size
passed
'
)
        
while
True
:
            
data
=
self
.
_inflater
.
decompress
(
size
)
            
if
len
(
data
)
!
=
0
:
                
return
data
            
read_data
=
self
.
_socket
.
recv
(
DeflateSocket
.
_RECV_SIZE
)
            
if
not
read_data
:
                
return
b
'
'
            
self
.
_inflater
.
append
(
read_data
)
    
def
sendall
(
self
bytes
)
:
        
self
.
send
(
bytes
)
    
def
send
(
self
bytes
)
:
        
self
.
_socket
.
sendall
(
self
.
_deflater
.
compress_and_flush
(
bytes
)
)
        
return
len
(
bytes
)
