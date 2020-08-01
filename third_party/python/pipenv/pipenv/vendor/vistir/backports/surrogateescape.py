"
"
"
This
is
Victor
Stinner
'
s
pure
-
Python
implementation
of
PEP
383
:
the
"
surrogateescape
"
error
handler
of
Python
3
.
Source
:
misc
/
python
/
surrogateescape
.
py
in
https
:
/
/
bitbucket
.
org
/
haypo
/
misc
"
"
"
import
codecs
import
sys
import
six
FS_ERRORS
=
"
surrogateescape
"
def
u
(
text
)
:
    
if
six
.
PY3
:
        
return
text
    
else
:
        
return
text
.
decode
(
"
unicode_escape
"
)
def
b
(
data
)
:
    
if
six
.
PY3
:
        
return
data
.
encode
(
"
latin1
"
)
    
else
:
        
return
data
if
six
.
PY3
:
    
_unichr
=
chr
    
bytes_chr
=
lambda
code
:
bytes
(
(
code
)
)
else
:
    
_unichr
=
unichr
    
bytes_chr
=
chr
def
surrogateescape_handler
(
exc
)
:
    
"
"
"
    
Pure
Python
implementation
of
the
PEP
383
:
the
"
surrogateescape
"
error
    
handler
of
Python
3
.
Undecodable
bytes
will
be
replaced
by
a
Unicode
    
character
U
+
DCxx
on
decoding
and
these
are
translated
into
the
    
original
bytes
on
encoding
.
    
"
"
"
    
mystring
=
exc
.
object
[
exc
.
start
:
exc
.
end
]
    
try
:
        
if
isinstance
(
exc
UnicodeDecodeError
)
:
            
decoded
=
replace_surrogate_decode
(
mystring
)
        
elif
isinstance
(
exc
UnicodeEncodeError
)
:
            
decoded
=
replace_surrogate_encode
(
mystring
)
        
else
:
            
raise
exc
    
except
NotASurrogateError
:
        
raise
exc
    
return
(
decoded
exc
.
end
)
class
NotASurrogateError
(
Exception
)
:
    
pass
def
replace_surrogate_encode
(
mystring
)
:
    
"
"
"
    
Returns
a
(
unicode
)
string
not
the
more
logical
bytes
because
the
codecs
    
register_error
functionality
expects
this
.
    
"
"
"
    
decoded
=
[
]
    
for
ch
in
mystring
:
        
code
=
ord
(
ch
)
        
if
not
0xD800
<
=
code
<
=
0xDCFF
:
            
raise
NotASurrogateError
        
if
0xDC00
<
=
code
<
=
0xDC7F
:
            
decoded
.
append
(
_unichr
(
code
-
0xDC00
)
)
        
elif
code
<
=
0xDCFF
:
            
decoded
.
append
(
_unichr
(
code
-
0xDC00
)
)
        
else
:
            
raise
NotASurrogateError
    
return
str
(
)
.
join
(
decoded
)
def
replace_surrogate_decode
(
mybytes
)
:
    
"
"
"
    
Returns
a
(
unicode
)
string
    
"
"
"
    
decoded
=
[
]
    
for
ch
in
mybytes
:
        
if
isinstance
(
ch
int
)
:
            
code
=
ch
        
else
:
            
code
=
ord
(
ch
)
        
if
0x80
<
=
code
<
=
0xFF
:
            
decoded
.
append
(
_unichr
(
0xDC00
+
code
)
)
        
elif
code
<
=
0x7F
:
            
decoded
.
append
(
_unichr
(
code
)
)
        
else
:
            
raise
NotASurrogateError
    
return
str
(
)
.
join
(
decoded
)
def
encodefilename
(
fn
)
:
    
if
FS_ENCODING
=
=
"
ascii
"
:
        
encoded
=
[
]
        
for
index
ch
in
enumerate
(
fn
)
:
            
code
=
ord
(
ch
)
            
if
code
<
128
:
                
ch
=
bytes_chr
(
code
)
            
elif
0xDC80
<
=
code
<
=
0xDCFF
:
                
ch
=
bytes_chr
(
code
-
0xDC00
)
            
else
:
                
raise
UnicodeEncodeError
(
                    
FS_ENCODING
fn
index
index
+
1
"
ordinal
not
in
range
(
128
)
"
                
)
            
encoded
.
append
(
ch
)
        
return
bytes
(
)
.
join
(
encoded
)
    
elif
FS_ENCODING
=
=
"
utf
-
8
"
:
        
encoded
=
[
]
        
for
index
ch
in
enumerate
(
fn
)
:
            
code
=
ord
(
ch
)
            
if
0xD800
<
=
code
<
=
0xDFFF
:
                
if
0xDC80
<
=
code
<
=
0xDCFF
:
                    
ch
=
bytes_chr
(
code
-
0xDC00
)
                    
encoded
.
append
(
ch
)
                
else
:
                    
raise
UnicodeEncodeError
(
                        
FS_ENCODING
fn
index
index
+
1
"
surrogates
not
allowed
"
                    
)
            
else
:
                
ch_utf8
=
ch
.
encode
(
"
utf
-
8
"
)
                
encoded
.
append
(
ch_utf8
)
        
return
bytes
(
)
.
join
(
encoded
)
    
else
:
        
return
fn
.
encode
(
FS_ENCODING
FS_ERRORS
)
def
decodefilename
(
fn
)
:
    
return
fn
.
decode
(
FS_ENCODING
FS_ERRORS
)
FS_ENCODING
=
"
ascii
"
fn
=
b
(
"
[
abc
\
xff
]
"
)
encoded
=
u
(
"
[
abc
\
udcff
]
"
)
FS_ENCODING
=
codecs
.
lookup
(
FS_ENCODING
)
.
name
def
register_surrogateescape
(
)
:
    
"
"
"
    
Registers
the
surrogateescape
error
handler
on
Python
2
(
only
)
    
"
"
"
    
if
six
.
PY3
:
        
return
    
try
:
        
codecs
.
lookup_error
(
FS_ERRORS
)
    
except
LookupError
:
        
codecs
.
register_error
(
FS_ERRORS
surrogateescape_handler
)
if
__name__
=
=
"
__main__
"
:
    
pass
