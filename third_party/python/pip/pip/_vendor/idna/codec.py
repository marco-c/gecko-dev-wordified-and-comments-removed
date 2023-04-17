from
.
core
import
encode
decode
alabel
ulabel
IDNAError
import
codecs
import
re
from
typing
import
Tuple
Optional
_unicode_dots_re
=
re
.
compile
(
'
[
\
u002e
\
u3002
\
uff0e
\
uff61
]
'
)
class
Codec
(
codecs
.
Codec
)
:
    
def
encode
(
self
data
errors
=
'
strict
'
)
:
        
if
errors
!
=
'
strict
'
:
            
raise
IDNAError
(
'
Unsupported
error
handling
\
"
{
}
\
"
'
.
format
(
errors
)
)
        
if
not
data
:
            
return
b
"
"
0
        
return
encode
(
data
)
len
(
data
)
    
def
decode
(
self
data
errors
=
'
strict
'
)
:
        
if
errors
!
=
'
strict
'
:
            
raise
IDNAError
(
'
Unsupported
error
handling
\
"
{
}
\
"
'
.
format
(
errors
)
)
        
if
not
data
:
            
return
'
'
0
        
return
decode
(
data
)
len
(
data
)
class
IncrementalEncoder
(
codecs
.
BufferedIncrementalEncoder
)
:
    
def
_buffer_encode
(
self
data
errors
final
)
:
        
if
errors
!
=
'
strict
'
:
            
raise
IDNAError
(
'
Unsupported
error
handling
\
"
{
}
\
"
'
.
format
(
errors
)
)
        
if
not
data
:
            
return
"
"
0
        
labels
=
_unicode_dots_re
.
split
(
data
)
        
trailing_dot
=
'
'
        
if
labels
:
            
if
not
labels
[
-
1
]
:
                
trailing_dot
=
'
.
'
                
del
labels
[
-
1
]
            
elif
not
final
:
                
del
labels
[
-
1
]
                
if
labels
:
                    
trailing_dot
=
'
.
'
        
result
=
[
]
        
size
=
0
        
for
label
in
labels
:
            
result
.
append
(
alabel
(
label
)
)
            
if
size
:
                
size
+
=
1
            
size
+
=
len
(
label
)
        
result_str
=
'
.
'
.
join
(
result
)
+
trailing_dot
        
size
+
=
len
(
trailing_dot
)
        
return
result_str
size
class
IncrementalDecoder
(
codecs
.
BufferedIncrementalDecoder
)
:
    
def
_buffer_decode
(
self
data
errors
final
)
:
        
if
errors
!
=
'
strict
'
:
            
raise
IDNAError
(
'
Unsupported
error
handling
\
"
{
}
\
"
'
.
format
(
errors
)
)
        
if
not
data
:
            
return
(
'
'
0
)
        
labels
=
_unicode_dots_re
.
split
(
data
)
        
trailing_dot
=
'
'
        
if
labels
:
            
if
not
labels
[
-
1
]
:
                
trailing_dot
=
'
.
'
                
del
labels
[
-
1
]
            
elif
not
final
:
                
del
labels
[
-
1
]
                
if
labels
:
                    
trailing_dot
=
'
.
'
        
result
=
[
]
        
size
=
0
        
for
label
in
labels
:
            
result
.
append
(
ulabel
(
label
)
)
            
if
size
:
                
size
+
=
1
            
size
+
=
len
(
label
)
        
result_str
=
'
.
'
.
join
(
result
)
+
trailing_dot
        
size
+
=
len
(
trailing_dot
)
        
return
(
result_str
size
)
class
StreamWriter
(
Codec
codecs
.
StreamWriter
)
:
    
pass
class
StreamReader
(
Codec
codecs
.
StreamReader
)
:
    
pass
def
getregentry
(
)
:
    
return
codecs
.
CodecInfo
(
        
name
=
'
idna
'
        
encode
=
Codec
(
)
.
encode
        
decode
=
Codec
(
)
.
decode
        
incrementalencoder
=
IncrementalEncoder
        
incrementaldecoder
=
IncrementalDecoder
        
streamwriter
=
StreamWriter
        
streamreader
=
StreamReader
    
)
