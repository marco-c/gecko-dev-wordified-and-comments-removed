#
-
*
-
coding
:
utf
-
8
-
*
-
"
"
"
hpack
/
huffman_decoder
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
An
implementation
of
a
bitwise
prefix
tree
specially
built
for
decoding
Huffman
-
coded
content
where
we
already
know
the
Huffman
table
.
"
"
"
from
.
compat
import
to_byte
decode_hex
class
HuffmanEncoder
(
object
)
:
    
"
"
"
    
Encodes
a
string
according
to
the
Huffman
encoding
table
defined
in
the
    
HPACK
specification
.
    
"
"
"
    
def
__init__
(
self
huffman_code_list
huffman_code_list_lengths
)
:
        
self
.
huffman_code_list
=
huffman_code_list
        
self
.
huffman_code_list_lengths
=
huffman_code_list_lengths
    
def
encode
(
self
bytes_to_encode
)
:
        
"
"
"
        
Given
a
string
of
bytes
encodes
them
according
to
the
HPACK
Huffman
        
specification
.
        
"
"
"
        
if
not
bytes_to_encode
:
            
return
b
'
'
        
final_num
=
0
        
final_int_len
=
0
        
for
char
in
bytes_to_encode
:
            
byte
=
to_byte
(
char
)
            
bin_int_len
=
self
.
huffman_code_list_lengths
[
byte
]
            
bin_int
=
self
.
huffman_code_list
[
byte
]
&
(
                
2
*
*
(
bin_int_len
+
1
)
-
1
            
)
            
final_num
<
<
=
bin_int_len
            
final_num
|
=
bin_int
            
final_int_len
+
=
bin_int_len
        
bits_to_be_padded
=
(
8
-
(
final_int_len
%
8
)
)
%
8
        
final_num
<
<
=
bits_to_be_padded
        
final_num
|
=
(
1
<
<
bits_to_be_padded
)
-
1
        
final_num
=
hex
(
final_num
)
[
2
:
]
.
rstrip
(
'
L
'
)
        
final_num
=
'
0
'
+
final_num
if
len
(
final_num
)
%
2
!
=
0
else
final_num
        
total_bytes
=
(
final_int_len
+
bits_to_be_padded
)
/
/
8
        
expected_digits
=
total_bytes
*
2
        
if
len
(
final_num
)
!
=
expected_digits
:
            
missing_digits
=
expected_digits
-
len
(
final_num
)
            
final_num
=
(
'
0
'
*
missing_digits
)
+
final_num
        
return
decode_hex
(
final_num
)
