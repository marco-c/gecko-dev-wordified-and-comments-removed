"
"
"
Functions
for
generating
random
numbers
.
"
"
"
import
os
import
struct
from
rsa
import
common
transform
def
read_random_bits
(
nbits
:
int
)
-
>
bytes
:
    
"
"
"
Reads
'
nbits
'
random
bits
.
    
If
nbits
isn
'
t
a
whole
number
of
bytes
an
extra
byte
will
be
appended
with
    
only
the
lower
bits
set
.
    
"
"
"
    
nbytes
rbits
=
divmod
(
nbits
8
)
    
randomdata
=
os
.
urandom
(
nbytes
)
    
if
rbits
>
0
:
        
randomvalue
=
ord
(
os
.
urandom
(
1
)
)
        
randomvalue
>
>
=
8
-
rbits
        
randomdata
=
struct
.
pack
(
"
B
"
randomvalue
)
+
randomdata
    
return
randomdata
def
read_random_int
(
nbits
:
int
)
-
>
int
:
    
"
"
"
Reads
a
random
integer
of
approximately
nbits
bits
.
"
"
"
    
randomdata
=
read_random_bits
(
nbits
)
    
value
=
transform
.
bytes2int
(
randomdata
)
    
value
|
=
1
<
<
(
nbits
-
1
)
    
return
value
def
read_random_odd_int
(
nbits
:
int
)
-
>
int
:
    
"
"
"
Reads
a
random
odd
integer
of
approximately
nbits
bits
.
    
>
>
>
read_random_odd_int
(
512
)
&
1
    
1
    
"
"
"
    
value
=
read_random_int
(
nbits
)
    
return
value
|
1
def
randint
(
maxvalue
:
int
)
-
>
int
:
    
"
"
"
Returns
a
random
integer
x
with
1
<
=
x
<
=
maxvalue
    
May
take
a
very
long
time
in
specific
situations
.
If
maxvalue
needs
N
bits
    
to
store
the
closer
maxvalue
is
to
(
2
*
*
N
)
-
1
the
faster
this
function
    
is
.
    
"
"
"
    
bit_size
=
common
.
bit_size
(
maxvalue
)
    
tries
=
0
    
while
True
:
        
value
=
read_random_int
(
bit_size
)
        
if
value
<
=
maxvalue
:
            
break
        
if
tries
%
10
=
=
0
and
tries
:
            
bit_size
-
=
1
        
tries
+
=
1
    
return
value
