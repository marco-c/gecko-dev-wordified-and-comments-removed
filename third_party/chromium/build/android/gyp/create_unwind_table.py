"
"
"
Creates
a
table
of
unwind
information
in
Android
Chrome
'
s
bespoke
format
.
"
"
"
import
abc
import
argparse
import
collections
import
enum
import
json
import
logging
import
re
import
struct
import
subprocess
import
sys
from
typing
import
(
Dict
Iterable
List
NamedTuple
Sequence
TextIO
Tuple
                    
Union
)
from
util
import
build_utils
_STACK_CFI_INIT_REGEX
=
re
.
compile
(
    
r
'
^
STACK
CFI
INIT
(
[
0
-
9a
-
f
]
+
)
(
[
0
-
9a
-
f
]
+
)
(
.
+
)
'
)
_STACK_CFI_REGEX
=
re
.
compile
(
r
'
^
STACK
CFI
(
[
0
-
9a
-
f
]
+
)
(
.
+
)
'
)
class
AddressCfi
(
NamedTuple
)
:
  
"
"
"
Record
representing
CFI
for
an
address
within
a
function
.
  
Represents
the
Call
Frame
Information
required
to
unwind
from
an
address
in
a
  
function
.
  
Attributes
:
      
address
:
The
address
.
      
unwind_instructions
:
The
unwind
instructions
for
the
address
.
  
"
"
"
  
address
:
int
  
unwind_instructions
:
str
class
FunctionCfi
(
NamedTuple
)
:
  
"
"
"
Record
representing
CFI
for
a
function
.
  
Note
:
address_cfi
[
0
]
.
address
is
the
start
address
of
the
function
.
  
Attributes
:
      
size
:
The
function
size
in
bytes
.
      
address_cfi
:
The
CFI
at
each
address
in
the
function
.
  
"
"
"
  
size
:
int
  
address_cfi
:
Tuple
[
AddressCfi
.
.
.
]
def
FilterToNonTombstoneCfi
(
stream
:
TextIO
)
-
>
Iterable
[
str
]
:
  
"
"
"
Generates
non
-
tombstone
STACK
CFI
lines
from
the
stream
.
  
STACK
CFI
functions
with
address
0
correspond
are
a
'
tombstone
'
record
  
associated
with
dead
code
and
can
be
ignored
.
See
  
https
:
/
/
bugs
.
llvm
.
org
/
show_bug
.
cgi
?
id
=
47148
#
c2
.
  
Args
:
      
stream
:
A
file
object
.
  
Returns
:
      
An
iterable
over
the
non
-
tombstone
STACK
CFI
lines
in
the
stream
.
  
"
"
"
  
in_tombstone_function
=
False
  
for
line
in
stream
:
    
if
not
line
.
startswith
(
'
STACK
CFI
'
)
:
      
continue
    
if
line
.
startswith
(
'
STACK
CFI
INIT
0
'
)
:
      
in_tombstone_function
=
True
    
elif
line
.
startswith
(
'
STACK
CFI
INIT
'
)
:
      
in_tombstone_function
=
False
    
if
not
in_tombstone_function
:
      
yield
line
def
ReadFunctionCfi
(
stream
:
TextIO
)
-
>
Iterable
[
FunctionCfi
]
:
  
"
"
"
Generates
FunctionCfi
records
from
the
stream
.
  
Args
:
      
stream
:
A
file
object
.
  
Returns
:
      
An
iterable
over
FunctionCfi
corresponding
to
the
non
-
tombstone
STACK
CFI
      
lines
in
the
stream
.
  
"
"
"
  
current_function_address
=
None
  
current_function_size
=
None
  
current_function_address_cfi
=
[
]
  
for
line
in
FilterToNonTombstoneCfi
(
stream
)
:
    
cfi_init_match
=
_STACK_CFI_INIT_REGEX
.
search
(
line
)
    
if
cfi_init_match
:
      
assert
current_function_address
!
=
0
      
if
(
current_function_address
is
not
None
          
and
current_function_size
is
not
None
)
:
        
yield
FunctionCfi
(
current_function_size
                          
tuple
(
current_function_address_cfi
)
)
      
current_function_address
=
int
(
cfi_init_match
.
group
(
1
)
16
)
      
current_function_size
=
int
(
cfi_init_match
.
group
(
2
)
16
)
      
current_function_address_cfi
=
[
          
AddressCfi
(
int
(
cfi_init_match
.
group
(
1
)
16
)
cfi_init_match
.
group
(
3
)
)
      
]
    
else
:
      
cfi_match
=
_STACK_CFI_REGEX
.
search
(
line
)
      
assert
cfi_match
      
current_function_address_cfi
.
append
(
          
AddressCfi
(
int
(
cfi_match
.
group
(
1
)
16
)
cfi_match
.
group
(
2
)
)
)
  
assert
current_function_address
is
not
None
  
assert
current_function_size
is
not
None
  
yield
FunctionCfi
(
current_function_size
tuple
(
current_function_address_cfi
)
)
def
EncodeAsBytes
(
*
values
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
Encodes
the
argument
ints
as
bytes
.
  
This
function
validates
that
the
inputs
are
within
the
range
that
can
be
  
represented
as
bytes
.
  
Args
:
    
values
:
Integers
in
range
[
0
255
]
.
  
Returns
:
    
The
values
encoded
as
bytes
.
  
"
"
"
  
for
i
value
in
enumerate
(
values
)
:
    
if
not
0
<
=
value
<
=
255
:
      
raise
ValueError
(
'
value
=
%
d
out
of
bounds
at
byte
%
d
'
%
(
value
i
)
)
  
return
bytes
(
values
)
def
Uleb128Encode
(
value
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
Encodes
the
argument
int
to
ULEB128
format
.
  
Args
:
    
value
:
Unsigned
integer
.
  
Returns
:
    
The
values
encoded
as
ULEB128
bytes
.
  
"
"
"
  
if
value
<
0
:
    
raise
ValueError
(
f
'
Cannot
uleb128
encode
negative
value
(
{
value
}
)
.
'
)
  
uleb128_bytes
=
[
]
  
done
=
False
  
while
not
done
:
    
value
lowest_seven_bits
=
divmod
(
value
0x80
)
    
done
=
value
=
=
0
    
uleb128_bytes
.
append
(
lowest_seven_bits
|
(
0x80
if
not
done
else
0x00
)
)
  
return
EncodeAsBytes
(
*
uleb128_bytes
)
def
EncodeStackPointerUpdate
(
offset
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
Encodes
a
stack
pointer
update
as
arm
unwind
instructions
.
  
Args
:
    
offset
:
Offset
to
apply
on
stack
pointer
.
Should
be
in
range
[
-
0x204
inf
)
.
  
Returns
:
    
A
list
of
arm
unwind
instructions
as
bytes
.
  
"
"
"
  
assert
offset
%
4
=
=
0
  
abs_offset
=
abs
(
offset
)
  
instruction_code
=
0b01000000
if
offset
<
0
else
0b00000000
  
if
0x04
<
=
abs_offset
<
=
0x200
:
    
instructions
=
[
        
instruction_code
|
(
(
min
(
abs_offset
0x100
)
-
4
)
>
>
2
)
    
]
    
if
abs_offset
>
=
0x104
:
      
instructions
.
append
(
instruction_code
|
(
(
abs_offset
-
0x100
-
4
)
>
>
2
)
)
    
try
:
      
return
EncodeAsBytes
(
*
instructions
)
    
except
ValueError
as
e
:
      
raise
RuntimeError
(
'
offset
=
%
d
produced
out
of
range
value
'
%
                         
offset
)
from
e
  
else
:
    
assert
offset
>
0
offset
    
return
EncodeAsBytes
(
0b10110010
                         
)
+
Uleb128Encode
(
(
offset
-
0x204
)
>
>
2
)
def
EncodePop
(
registers
:
Sequence
[
int
]
)
-
>
bytes
:
  
"
"
"
Encodes
popping
of
a
sequence
of
registers
as
arm
unwind
instructions
.
  
Args
:
    
registers
:
Collection
of
target
registers
to
accept
values
popped
from
      
stack
.
Register
value
order
in
the
sequence
does
not
matter
.
Values
are
      
popped
based
on
register
index
order
.
  
Returns
:
    
A
list
of
arm
unwind
instructions
as
bytes
.
  
"
"
"
  
assert
all
(
      
r
in
range
(
4
16
)
      
for
r
in
registers
)
f
'
Can
only
pop
r4
~
r15
.
Registers
:
\
n
{
registers
}
.
'
  
assert
len
(
registers
)
>
0
'
Register
sequence
cannot
be
empty
.
'
  
instructions
:
List
[
int
]
=
[
]
  
pop_lr
=
14
in
registers
  
non_lr_registers
=
[
r
for
r
in
registers
if
r
!
=
14
]
  
non_lr_registers_continuous_from_r4
=
\
    
sorted
(
non_lr_registers
)
=
=
list
(
range
(
4
4
+
len
(
non_lr_registers
)
)
)
  
if
(
pop_lr
and
0
<
len
(
non_lr_registers
)
<
=
8
      
and
non_lr_registers_continuous_from_r4
)
:
    
instructions
.
append
(
0b10101000
                        
|
(
len
(
non_lr_registers
)
-
1
)
                        
)
  
else
:
    
register_bits
=
0
    
for
register
in
registers
:
      
register_bits
|
=
1
<
<
register
    
register_bits
=
register_bits
>
>
4
    
instructions
.
extend
(
[
        
0b10000000
|
(
register_bits
>
>
8
)
        
register_bits
&
0xff
    
]
)
  
return
EncodeAsBytes
(
*
instructions
)
class
UnwindType
(
enum
.
Enum
)
:
  
"
"
"
  
The
type
of
unwind
action
to
perform
.
  
"
"
"
  
RETURN_TO_LR
=
1
  
UPDATE_SP_AND_OR_POP_REGISTERS
=
2
  
RESTORE_SP_FROM_REGISTER
=
3
  
NO_ACTION
=
4
class
AddressUnwind
(
NamedTuple
)
:
  
"
"
"
Record
representing
unwind
information
for
an
address
within
a
function
.
  
Attributes
:
      
address_offset
:
The
offset
of
the
address
from
the
start
of
the
function
.
      
unwind_type
:
The
type
of
unwind
to
perform
from
the
address
.
      
sp_offset
:
The
offset
to
apply
to
the
stack
pointer
.
      
registers
:
The
registers
involved
in
the
unwind
.
  
"
"
"
  
address_offset
:
int
  
unwind_type
:
UnwindType
  
sp_offset
:
int
  
registers
:
Tuple
[
int
.
.
.
]
class
FunctionUnwind
(
NamedTuple
)
:
  
"
"
"
Record
representing
unwind
information
for
a
function
.
  
Attributes
:
      
address
:
The
address
of
the
function
.
      
size
:
The
function
size
in
bytes
.
      
address_unwind_info
:
The
unwind
info
at
each
address
in
the
function
.
  
"
"
"
  
address
:
int
  
size
:
int
  
address_unwinds
:
Tuple
[
AddressUnwind
.
.
.
]
def
EncodeAddressUnwind
(
address_unwind
:
AddressUnwind
)
-
>
bytes
:
  
"
"
"
Encodes
an
AddressUnwind
object
as
arm
unwind
instructions
.
  
Args
:
    
address_unwind
:
Record
representing
unwind
information
for
an
address
within
      
a
function
.
  
Returns
:
    
A
list
of
arm
unwind
instructions
as
bytes
.
  
"
"
"
  
if
address_unwind
.
unwind_type
=
=
UnwindType
.
RETURN_TO_LR
:
    
return
EncodeAsBytes
(
0b10110000
)
  
if
address_unwind
.
unwind_type
=
=
UnwindType
.
UPDATE_SP_AND_OR_POP_REGISTERS
:
    
return
(
(
EncodeStackPointerUpdate
(
address_unwind
.
sp_offset
)
             
if
address_unwind
.
sp_offset
else
b
'
'
)
+
            
(
EncodePop
(
address_unwind
.
registers
)
             
if
address_unwind
.
registers
else
b
'
'
)
)
  
if
address_unwind
.
unwind_type
=
=
UnwindType
.
RESTORE_SP_FROM_REGISTER
:
    
assert
len
(
address_unwind
.
registers
)
=
=
1
    
return
(
EncodeAsBytes
(
0b10010000
                          
|
address_unwind
.
registers
[
0
]
                          
)
+
            
(
EncodeStackPointerUpdate
(
address_unwind
.
sp_offset
)
             
if
address_unwind
.
sp_offset
else
b
'
'
)
)
  
if
address_unwind
.
unwind_type
=
=
UnwindType
.
NO_ACTION
:
    
return
b
'
'
  
assert
False
'
unknown
unwind
type
'
  
return
b
'
'
class
UnwindInstructionsParser
(
abc
.
ABC
)
:
  
"
"
"
Base
class
for
parsers
of
breakpad
unwind
instruction
sequences
.
  
Provides
regexes
matching
breakpad
instruction
sequences
understood
by
the
  
parser
and
parsing
of
the
sequences
from
the
regex
match
.
  
"
"
"
  
abc
.
abstractmethod
  
def
GetBreakpadInstructionsRegex
(
self
)
-
>
re
.
Pattern
:
    
pass
  
abc
.
abstractmethod
  
def
ParseFromMatch
(
self
address_offset
:
int
cfa_sp_offset
:
int
                     
match
:
re
.
Match
)
-
>
Tuple
[
AddressUnwind
int
]
:
    
"
"
"
Returns
the
regex
matching
the
breakpad
instructions
.
    
Args
:
      
address_offset
:
Offset
from
function
start
address
.
      
cfa_sp_offset
:
CFA
stack
pointer
offset
.
    
Returns
:
      
The
unwind
info
for
the
address
plus
the
new
cfa_sp_offset
.
    
"
"
"
class
NullParser
(
UnwindInstructionsParser
)
:
  
"
"
"
Translates
the
state
before
any
instruction
has
been
executed
.
"
"
"
  
regex
=
re
.
compile
(
r
'
^
\
.
cfa
:
sp
0
\
+
\
.
ra
:
lr
'
)
  
def
GetBreakpadInstructionsRegex
(
self
)
-
>
re
.
Pattern
:
    
return
self
.
regex
  
def
ParseFromMatch
(
self
address_offset
:
int
cfa_sp_offset
:
int
                     
match
:
re
.
Match
)
-
>
Tuple
[
AddressUnwind
int
]
:
    
return
AddressUnwind
(
address_offset
UnwindType
.
RETURN_TO_LR
0
(
)
)
0
class
PushOrSubSpParser
(
UnwindInstructionsParser
)
:
  
"
"
"
Translates
unwinds
from
push
or
sub
sp
#
constant
instructions
.
"
"
"
  
regex
=
re
.
compile
(
r
'
^
(
?
:
\
.
cfa
:
sp
(
\
d
+
)
\
+
?
)
?
'
                     
r
'
(
?
:
\
.
ra
:
\
.
cfa
(
-
\
d
+
)
\
+
\
^
?
)
?
'
                     
r
'
(
(
?
:
r
\
d
+
:
\
.
cfa
-
\
d
+
\
+
\
^
?
)
*
)
'
)
  
register_regex
=
re
.
compile
(
'
(
?
<
=
r
)
(
\
d
+
)
'
)
  
def
GetBreakpadInstructionsRegex
(
self
)
-
>
re
.
Pattern
:
    
return
self
.
regex
  
def
ParseFromMatch
(
self
address_offset
:
int
cfa_sp_offset
:
int
                     
match
:
re
.
Match
)
-
>
Tuple
[
AddressUnwind
int
]
:
    
new_cfa_sp_offset
ra_cfa_offset
=
(
int
(
group
)
if
group
else
None
                                        
for
group
in
match
.
groups
(
)
[
:
2
]
)
    
registers
=
sorted
(
[
        
int
(
register
)
        
for
register
in
self
.
register_regex
.
findall
(
match
.
group
(
3
)
)
        
if
int
(
register
)
in
range
(
4
16
)
    
]
+
                       
(
[
14
]
if
ra_cfa_offset
is
not
None
else
[
]
)
)
    
sp_offset
=
0
    
if
new_cfa_sp_offset
is
not
None
:
      
sp_offset
=
new_cfa_sp_offset
-
cfa_sp_offset
      
assert
sp_offset
%
4
=
=
0
      
if
sp_offset
>
=
len
(
registers
)
*
4
:
        
sp_offset
-
=
len
(
registers
)
*
4
    
return
AddressUnwind
(
address_offset
                         
UnwindType
.
UPDATE_SP_AND_OR_POP_REGISTERS
sp_offset
                         
tuple
(
registers
)
)
new_cfa_sp_offset
or
cfa_sp_offset
class
VPushParser
(
UnwindInstructionsParser
)
:
  
regex
=
re
.
compile
(
r
'
^
(
?
:
\
.
cfa
:
sp
(
\
d
+
)
\
+
)
?
'
                     
r
'
(
?
:
unnamed_register
\
d
+
:
\
.
cfa
-
\
d
+
\
+
\
^
?
)
+
'
)
  
def
GetBreakpadInstructionsRegex
(
self
)
-
>
re
.
Pattern
:
    
return
self
.
regex
  
def
ParseFromMatch
(
self
address_offset
:
int
cfa_sp_offset
:
int
                     
match
:
re
.
Match
)
-
>
Tuple
[
AddressUnwind
int
]
:
    
new_cfa_sp_offset
=
int
(
match
.
group
(
1
)
)
if
match
.
group
(
1
)
else
None
    
if
new_cfa_sp_offset
is
None
:
      
return
(
AddressUnwind
(
address_offset
UnwindType
.
NO_ACTION
0
                            
(
)
)
cfa_sp_offset
)
    
sp_offset
=
new_cfa_sp_offset
-
cfa_sp_offset
    
assert
sp_offset
%
4
=
=
0
    
return
AddressUnwind
(
address_offset
                         
UnwindType
.
UPDATE_SP_AND_OR_POP_REGISTERS
sp_offset
                         
(
)
)
new_cfa_sp_offset
class
StoreSpParser
(
UnwindInstructionsParser
)
:
  
regex
=
re
.
compile
(
r
'
^
\
.
cfa
:
r
(
\
d
+
)
(
\
d
+
)
\
+
'
)
  
def
GetBreakpadInstructionsRegex
(
self
)
-
>
re
.
Pattern
:
    
return
self
.
regex
  
def
ParseFromMatch
(
self
address_offset
:
int
cfa_sp_offset
:
int
                     
match
:
re
.
Match
)
-
>
Tuple
[
AddressUnwind
int
]
:
    
register
=
int
(
match
.
group
(
1
)
)
    
new_cfa_sp_offset
=
int
(
match
.
group
(
2
)
)
    
sp_offset
=
new_cfa_sp_offset
-
cfa_sp_offset
    
assert
sp_offset
%
4
=
=
0
    
return
AddressUnwind
(
address_offset
UnwindType
.
RESTORE_SP_FROM_REGISTER
                         
sp_offset
(
register
)
)
new_cfa_sp_offset
def
EncodeUnwindInstructionTable
(
complete_instruction_sequences
:
Iterable
[
bytes
]
                                 
)
-
>
Tuple
[
bytes
Dict
[
bytes
int
]
]
:
  
"
"
"
Encodes
the
unwind
instruction
table
.
  
Deduplicates
the
encoded
unwind
instruction
sequences
.
Generates
the
table
and
  
a
dictionary
mapping
a
function
to
its
starting
index
in
the
table
.
  
The
instruction
table
is
used
by
the
unwinder
to
provide
the
sequence
of
  
unwind
instructions
to
execute
for
each
function
separated
by
offset
  
into
the
function
.
  
Args
:
    
complete_instruction_sequences
:
An
iterable
of
encoded
unwind
instruction
      
sequences
.
The
sequences
represent
the
series
of
unwind
instructions
to
      
execute
corresponding
to
offsets
within
each
function
.
  
Returns
:
    
A
tuple
containing
:
    
-
The
unwind
instruction
table
as
bytes
.
    
-
The
mapping
from
the
instruction
sequence
to
the
offset
in
the
unwind
      
instruction
table
.
This
mapping
is
used
to
construct
the
function
offset
      
table
which
references
entries
in
the
unwind
instruction
table
.
  
"
"
"
  
ref_counts
:
Dict
[
bytes
int
]
=
collections
.
defaultdict
(
int
)
  
for
sequence
in
complete_instruction_sequences
:
    
ref_counts
[
sequence
]
+
=
1
  
def
ComputeScore
(
sequence
)
:
    
"
"
"
Score
for
each
sequence
is
computed
as
ref_count
/
size_of_sequence
.
    
According
to
greedy
algorithm
items
with
higher
value
/
space
cost
ratio
    
should
be
prioritized
.
Here
value
is
bytes
saved
in
the
function
offset
    
table
represetned
by
ref_count
.
Space
cost
is
the
space
taken
in
the
    
unwind
instruction
table
represented
by
size_of_sequence
.
    
Note
:
In
order
to
ensure
build
-
time
determinism
sequence
is
also
returned
    
to
resolve
sorting
order
when
scores
are
the
same
.
    
"
"
"
    
return
ref_counts
[
sequence
]
/
len
(
sequence
)
sequence
  
ordered_sequences
=
sorted
(
ref_counts
.
keys
(
)
key
=
ComputeScore
reverse
=
True
)
  
offsets
:
Dict
[
bytes
int
]
=
{
}
  
current_offset
=
0
  
for
sequence
in
ordered_sequences
:
    
offsets
[
sequence
]
=
current_offset
    
current_offset
+
=
len
(
sequence
)
  
return
b
'
'
.
join
(
ordered_sequences
)
offsets
class
EncodedAddressUnwind
(
NamedTuple
)
:
  
"
"
"
Record
representing
unwind
information
for
an
address
within
a
function
.
  
This
structure
represents
the
same
concept
as
AddressUnwind
.
The
only
  
difference
is
that
how
to
unwind
from
the
address
is
represented
as
  
encoded
ARM
unwind
instructions
.
  
Attributes
:
    
address_offset
:
The
offset
of
the
address
from
the
start
address
of
the
      
function
.
    
complete_instruction_sequence
:
The
full
ARM
unwind
instruction
sequence
to
      
unwind
from
the
address_offset
.
  
"
"
"
  
address_offset
:
int
  
complete_instruction_sequence
:
bytes
def
EncodeAddressUnwinds
(
address_unwinds
:
Tuple
[
AddressUnwind
.
.
.
]
                         
)
-
>
Tuple
[
EncodedAddressUnwind
.
.
.
]
:
  
"
"
"
Encodes
the
unwind
instructions
and
offset
for
the
addresses
within
a
  
function
.
  
Args
:
    
address_unwinds
:
A
tuple
of
unwind
state
for
addresses
within
a
function
.
  
Returns
:
    
The
encoded
unwind
instructions
and
offsets
for
the
addresses
within
a
    
function
ordered
by
decreasing
offset
.
  
"
"
"
  
sorted_address_unwinds
:
List
[
AddressUnwind
]
=
sorted
(
      
address_unwinds
      
key
=
lambda
address_unwind
:
address_unwind
.
address_offset
      
reverse
=
True
)
  
unwind_instructions
:
List
[
bytes
]
=
[
      
EncodeAddressUnwind
(
address_unwind
)
      
for
address_unwind
in
sorted_address_unwinds
  
]
  
complete_instruction_sequences
=
[
      
b
'
'
.
join
(
unwind_instructions
[
i
:
]
)
for
i
in
range
(
len
(
unwind_instructions
)
)
  
]
  
encoded_unwinds
:
List
[
EncodedAddressUnwind
]
=
[
]
  
for
address_unwind
sequence
in
zip
(
sorted_address_unwinds
                                      
complete_instruction_sequences
)
:
    
encoded_unwinds
.
append
(
        
EncodedAddressUnwind
(
address_unwind
.
address_offset
sequence
)
)
  
return
tuple
(
encoded_unwinds
)
class
EncodedFunctionUnwind
(
NamedTuple
)
:
  
"
"
"
Record
representing
unwind
information
for
a
function
.
  
This
structure
represents
the
same
concept
as
FunctionUnwind
but
with
  
some
differences
:
  
-
Attribute
address
is
split
into
2
attributes
:
page_number
and
    
page_offset
.
  
-
Attribute
size
is
dropped
.
  
-
Attribute
address_unwinds
becomes
a
collection
of
EncodedAddressUnwind
s
    
instead
of
a
collection
of
AddressUnwind
s
.
  
Attributes
:
    
page_number
:
The
upper
bits
(
17
~
31bits
)
of
byte
offset
from
text
section
      
start
.
    
page_offset
:
The
lower
bits
(
1
~
16bits
)
of
instruction
offset
from
text
      
section
start
.
    
address_unwinds
:
A
collection
of
EncodedAddressUnwind
s
.
  
"
"
"
  
page_number
:
int
  
page_offset
:
int
  
address_unwinds
:
Tuple
[
EncodedAddressUnwind
.
.
.
]
TRIVIAL_UNWIND
:
Tuple
[
EncodedAddressUnwind
.
.
.
]
=
EncodeAddressUnwinds
(
    
(
AddressUnwind
(
address_offset
=
0
                   
unwind_type
=
UnwindType
.
RETURN_TO_LR
                   
sp_offset
=
0
                   
registers
=
(
)
)
)
)
REFUSE_TO_UNWIND
:
Tuple
[
EncodedAddressUnwind
.
.
.
]
=
(
EncodedAddressUnwind
(
    
address_offset
=
0
    
complete_instruction_sequence
=
bytes
(
[
0b10000000
0b00000000
]
)
)
)
def
EncodeFunctionUnwinds
(
function_unwinds
:
Iterable
[
FunctionUnwind
]
                          
text_section_start_address
:
int
                          
)
-
>
Iterable
[
EncodedFunctionUnwind
]
:
  
"
"
"
Encodes
the
unwind
state
for
all
functions
defined
in
the
binary
.
  
This
function
  
-
sorts
the
collection
of
FunctionUnwind
s
by
address
.
  
-
fills
in
gaps
between
functions
with
trivial
unwind
.
  
-
fills
the
space
in
the
last
page
after
last
function
with
refuse
to
unwind
.
  
-
fills
the
space
in
the
first
page
before
the
first
function
with
refuse
    
to
unwind
.
  
Args
:
    
function_unwinds
:
An
iterable
of
function
unwind
states
.
    
text_section_start_address
:
The
address
of
.
text
section
in
ELF
file
.
  
Returns
:
    
The
encoded
function
unwind
states
with
no
gaps
between
functions
ordered
    
by
ascending
address
.
  
"
"
"
  
def
GetPageNumber
(
address
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
Calculates
the
page
number
.
    
Page
number
is
calculated
as
byte_offset_from_text_section_start
>
>
17
    
i
.
e
.
the
upper
bits
(
17
~
31bits
)
of
byte
offset
from
text
section
start
.
    
"
"
"
    
return
(
address
-
text_section_start_address
)
>
>
17
  
def
GetPageOffset
(
address
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
Calculates
the
page
offset
.
    
Page
offset
is
calculated
as
(
byte_offset_from_text_section_start
>
>
1
)
    
&
0xffff
i
.
e
.
the
lower
bits
(
1
~
16bits
)
of
instruction
offset
from
    
text
section
start
.
    
"
"
"
    
return
(
(
address
-
text_section_start_address
)
>
>
1
)
&
0xffff
  
sorted_function_unwinds
:
List
[
FunctionUnwind
]
=
sorted
(
      
function_unwinds
key
=
lambda
function_unwind
:
function_unwind
.
address
)
  
if
sorted_function_unwinds
[
0
]
.
address
>
text_section_start_address
:
    
yield
EncodedFunctionUnwind
(
page_number
=
0
                                
page_offset
=
0
                                
address_unwinds
=
REFUSE_TO_UNWIND
)
  
prev_func_end_address
:
int
=
sorted_function_unwinds
[
0
]
.
address
  
gaps
=
0
  
for
unwind
in
sorted_function_unwinds
:
    
assert
prev_func_end_address
<
=
unwind
.
address
(
        
'
Detected
overlap
between
functions
.
'
)
    
if
prev_func_end_address
<
unwind
.
address
:
      
gaps
+
=
1
      
yield
EncodedFunctionUnwind
(
GetPageNumber
(
prev_func_end_address
)
                                  
GetPageOffset
(
prev_func_end_address
)
                                  
TRIVIAL_UNWIND
)
    
yield
EncodedFunctionUnwind
(
GetPageNumber
(
unwind
.
address
)
                                
GetPageOffset
(
unwind
.
address
)
                                
EncodeAddressUnwinds
(
unwind
.
address_unwinds
)
)
    
prev_func_end_address
=
unwind
.
address
+
unwind
.
size
  
if
GetPageOffset
(
prev_func_end_address
)
!
=
0
:
    
yield
EncodedFunctionUnwind
(
GetPageNumber
(
prev_func_end_address
)
                                
GetPageOffset
(
prev_func_end_address
)
                                
REFUSE_TO_UNWIND
)
  
logging
.
info
(
'
%
d
/
%
d
gaps
between
functions
filled
with
trivial
unwind
.
'
gaps
               
len
(
sorted_function_unwinds
)
)
def
EncodeFunctionOffsetTable
(
    
encoded_address_unwind_sequences
:
Iterable
[
        
Tuple
[
EncodedAddressUnwind
.
.
.
]
]
    
unwind_instruction_table_offsets
:
Dict
[
bytes
int
]
)
-
>
Tuple
[
bytes
Dict
[
Tuple
[
EncodedAddressUnwind
.
.
.
]
int
]
]
:
  
"
"
"
Encodes
the
function
offset
table
.
  
The
function
offset
table
maps
local
instruction
offset
from
function
  
start
to
the
location
in
the
unwind
instruction
table
.
  
Args
:
    
encoded_address_unwind_sequences
:
An
iterable
of
encoded
address
unwind
      
sequences
.
    
unwind_instruction_table_offsets
:
The
offset
mapping
returned
from
      
EncodeUnwindInstructionTable
.
  
Returns
:
    
A
tuple
containing
:
    
-
The
function
offset
table
as
bytes
.
    
-
The
mapping
from
the
EncodedAddressUnwind
s
to
the
offset
in
the
function
      
offset
table
.
This
mapping
is
used
to
construct
the
function
table
which
      
references
entries
in
the
function
offset
table
.
  
"
"
"
  
function_offset_table
=
bytearray
(
)
  
offsets
:
Dict
[
Tuple
[
EncodedAddressUnwind
.
.
.
]
int
]
=
{
}
  
for
sequence
in
encoded_address_unwind_sequences
:
    
if
sequence
in
offsets
:
      
continue
    
offsets
[
sequence
]
=
len
(
function_offset_table
)
    
for
address_offset
complete_instruction_sequence
in
sequence
:
      
instruction_offset
=
address_offset
>
>
1
      
function_offset_table
+
=
(
          
Uleb128Encode
(
instruction_offset
)
+
Uleb128Encode
(
              
unwind_instruction_table_offsets
[
complete_instruction_sequence
]
)
)
  
return
bytes
(
function_offset_table
)
offsets
def
EncodePageTableAndFunctionTable
(
    
function_unwinds
:
Iterable
[
EncodedFunctionUnwind
]
    
function_offset_table_offsets
:
Dict
[
Tuple
[
EncodedAddressUnwind
.
.
.
]
int
]
)
-
>
Tuple
[
bytes
bytes
]
:
  
"
"
"
Encode
page
table
and
function
table
as
bytes
.
  
Page
table
:
  
A
table
that
contains
the
mapping
from
page_number
to
the
location
of
the
  
entry
for
the
first
function
on
the
page
in
the
function
table
.
  
Function
table
:
  
A
table
that
contains
the
mapping
from
page_offset
to
the
location
of
an
entry
  
in
the
function
offset
table
.
  
Args
:
    
function_unwinds
:
All
encoded
function
unwinds
in
the
module
.
    
function_offset_table_offsets
:
The
offset
mapping
returned
from
      
EncodeFunctionOffsetTable
.
  
Returns
:
    
A
tuple
containing
:
    
-
The
page
table
as
bytes
.
    
-
The
function
table
as
bytes
.
  
"
"
"
  
page_function_unwinds
:
Dict
[
      
int
List
[
EncodedFunctionUnwind
]
]
=
collections
.
defaultdict
(
list
)
  
for
function_unwind
in
function_unwinds
:
    
page_function_unwinds
[
function_unwind
.
page_number
]
.
append
(
function_unwind
)
  
raw_page_table
:
List
[
int
]
=
[
]
  
function_table
=
bytearray
(
)
  
for
page_number
same_page_function_unwinds
in
sorted
(
      
page_function_unwinds
.
items
(
)
key
=
lambda
item
:
item
[
0
]
)
:
    
assert
page_number
>
len
(
raw_page_table
)
-
1
    
number_of_empty_pages
=
page_number
-
len
(
raw_page_table
)
    
function_table_index
=
len
(
function_table
)
/
/
4
    
raw_page_table
.
extend
(
[
function_table_index
]
*
(
number_of_empty_pages
+
1
)
)
    
assert
page_number
=
=
len
(
raw_page_table
)
-
1
    
for
function_unwind
in
sorted
(
        
same_page_function_unwinds
        
key
=
lambda
function_unwind
:
function_unwind
.
page_offset
)
:
      
function_table
+
=
struct
.
pack
(
          
'
HH
'
function_unwind
.
page_offset
          
function_offset_table_offsets
[
function_unwind
.
address_unwinds
]
)
  
page_table
=
struct
.
pack
(
f
'
{
len
(
raw_page_table
)
}
I
'
*
raw_page_table
)
  
return
page_table
bytes
(
function_table
)
ALL_PARSERS
:
Tuple
[
UnwindInstructionsParser
.
.
.
]
=
(
    
NullParser
(
)
    
PushOrSubSpParser
(
)
    
StoreSpParser
(
)
    
VPushParser
(
)
)
def
ParseAddressCfi
(
address_cfi
:
AddressCfi
function_start_address
:
int
                    
parsers
:
Tuple
[
UnwindInstructionsParser
.
.
.
]
                    
prev_cfa_sp_offset
:
int
                    
)
-
>
Tuple
[
Union
[
AddressUnwind
None
]
bool
int
]
:
  
"
"
"
Parses
address
CFI
with
given
parsers
.
  
Args
:
    
address_cfi
:
The
CFI
for
an
address
in
the
function
.
    
function_start_address
:
The
start
address
of
the
function
.
    
parsers
:
Available
parsers
to
try
on
CFI
data
.
    
prev_cfa_sp_offset
:
Previous
CFA
stack
pointer
offset
.
  
Returns
:
    
A
tuple
containing
:
    
-
An
AddressUnwind
object
when
the
parse
is
successful
None
otherwise
.
    
-
Whether
the
address
is
in
function
epilogue
.
    
-
The
new
cfa_sp_offset
.
  
"
"
"
  
for
parser
in
parsers
:
    
match
=
parser
.
GetBreakpadInstructionsRegex
(
)
.
search
(
        
address_cfi
.
unwind_instructions
)
    
if
not
match
:
      
continue
    
address_unwind
cfa_sp_offset
=
parser
.
ParseFromMatch
(
        
address_cfi
.
address
-
function_start_address
prev_cfa_sp_offset
match
)
    
in_epilogue
=
(
        
prev_cfa_sp_offset
>
cfa_sp_offset
        
and
address_unwind
.
unwind_type
!
=
UnwindType
.
RESTORE_SP_FROM_REGISTER
)
    
return
(
address_unwind
if
not
in_epilogue
else
None
in_epilogue
            
cfa_sp_offset
)
  
return
None
False
prev_cfa_sp_offset
def
GenerateUnwinds
(
function_cfis
:
Iterable
[
FunctionCfi
]
                    
parsers
:
Tuple
[
UnwindInstructionsParser
.
.
.
]
                    
)
-
>
Iterable
[
FunctionUnwind
]
:
  
"
"
"
Generates
parsed
function
unwind
states
from
breakpad
CFI
data
.
  
This
function
parses
FunctionCfi
s
to
FunctionUnwind
s
using
  
UnwindInstructionParser
.
  
Args
:
    
function_cfis
:
An
iterable
of
function
CFI
data
.
    
parsers
:
Available
parsers
to
try
on
CFI
address
data
.
  
Returns
:
    
An
iterable
of
parsed
function
unwind
states
.
  
"
"
"
  
functions
=
0
  
addresses
=
0
  
handled_addresses
=
0
  
epilogues_seen
=
0
  
for
function_cfi
in
function_cfis
:
    
functions
+
=
1
    
address_unwinds
:
List
[
AddressUnwind
]
=
[
]
    
cfa_sp_offset
=
0
    
for
address_cfi
in
function_cfi
.
address_cfi
:
      
addresses
+
=
1
      
address_unwind
in_epilogue
cfa_sp_offset
=
ParseAddressCfi
(
          
address_cfi
function_cfi
.
address_cfi
[
0
]
.
address
parsers
          
cfa_sp_offset
)
      
if
address_unwind
:
        
handled_addresses
+
=
1
        
address_unwinds
.
append
(
address_unwind
)
        
continue
      
if
in_epilogue
:
        
epilogues_seen
+
=
1
        
break
      
logging
.
info
(
'
unrecognized
CFI
:
%
x
%
s
.
'
address_cfi
.
address
                   
address_cfi
.
unwind_instructions
)
    
if
address_unwinds
:
      
assert
address_unwinds
[
0
]
.
address_offset
=
=
0
      
assert
address_unwinds
[
0
]
.
unwind_type
=
=
UnwindType
.
RETURN_TO_LR
      
yield
FunctionUnwind
(
function_cfi
.
address_cfi
[
0
]
.
address
                           
function_cfi
.
size
tuple
(
address_unwinds
)
)
  
logging
.
info
(
'
%
d
functions
.
'
functions
)
  
logging
.
info
(
'
%
d
/
%
d
addresses
handled
.
'
handled_addresses
addresses
)
  
logging
.
info
(
'
epilogues_seen
:
%
d
.
'
epilogues_seen
)
def
EncodeUnwindInfo
(
page_table
:
bytes
function_table
:
bytes
                     
function_offset_table
:
bytes
                     
unwind_instruction_table
:
bytes
)
-
>
bytes
:
  
"
"
"
Encodes
all
unwind
tables
as
a
single
binary
.
  
Concats
all
unwind
table
binaries
together
and
attach
a
header
at
the
start
  
with
a
offset
-
size
pair
for
each
table
.
  
offset
:
The
offset
to
the
target
table
from
the
start
of
the
unwind
info
    
binary
in
bytes
.
  
size
:
The
declared
size
of
the
target
table
.
  
Both
offset
and
size
are
represented
as
32bit
integers
.
  
See
base
:
:
ChromeUnwindInfoHeaderAndroid
for
more
details
.
  
Args
:
    
page_table
:
The
page
table
as
bytes
.
    
function_table
:
The
function
table
as
bytes
.
    
function_offset_table
:
The
function
offset
table
as
bytes
.
    
unwind_instruction_table
:
The
unwind
instruction
table
as
bytes
.
  
Returns
:
    
A
single
binary
containing
    
-
A
header
that
points
to
the
location
of
each
table
.
    
-
All
unwind
tables
.
  
"
"
"
  
unwind_info_header
=
bytearray
(
)
  
unwind_info_header_size
=
4
*
2
*
4
  
unwind_info_body
=
bytearray
(
)
  
assert
len
(
page_table
)
%
4
=
=
0
(
      
'
Each
entry
in
the
page
table
should
be
4
-
byte
integer
.
'
)
  
assert
len
(
function_table
)
%
4
=
=
0
(
      
'
Each
entry
in
the
function
table
should
be
a
pair
of
2
2
-
byte
integers
.
'
)
  
for
table
in
page_table
function_table
:
    
offset
=
unwind_info_header_size
+
len
(
unwind_info_body
)
    
declared_size
=
len
(
table
)
/
/
4
    
unwind_info_header
+
=
struct
.
pack
(
'
II
'
offset
declared_size
)
    
unwind_info_body
+
=
table
  
for
table
in
function_offset_table
unwind_instruction_table
:
    
offset
=
unwind_info_header_size
+
len
(
unwind_info_body
)
    
declared_size
=
len
(
table
)
    
unwind_info_header
+
=
struct
.
pack
(
'
II
'
offset
declared_size
)
    
unwind_info_body
+
=
table
  
return
bytes
(
unwind_info_header
+
unwind_info_body
)
def
GenerateUnwindTables
(
    
encoded_function_unwinds_iterable
:
Iterable
[
EncodedFunctionUnwind
]
)
-
>
Tuple
[
bytes
bytes
bytes
bytes
]
:
  
"
"
"
Generates
all
unwind
tables
as
bytes
.
  
Args
:
    
encoded_function_unwinds_iterable
:
Encoded
function
unwinds
for
all
      
functions
in
the
ELF
binary
.
  
Returns
:
    
A
tuple
containing
:
    
-
The
page
table
as
bytes
.
    
-
The
function
table
as
bytes
.
    
-
The
function
offset
table
as
bytes
.
    
-
The
unwind
instruction
table
as
bytes
.
  
"
"
"
  
encoded_function_unwinds
:
List
[
EncodedFunctionUnwind
]
=
list
(
      
encoded_function_unwinds_iterable
)
  
complete_instruction_sequences
:
List
[
bytes
]
=
[
]
  
encoded_address_unwind_sequences
:
List
[
Tuple
[
EncodedAddressUnwind
.
.
.
]
]
=
[
]
  
for
encoded_function_unwind
in
encoded_function_unwinds
:
    
encoded_address_unwind_sequences
.
append
(
        
encoded_function_unwind
.
address_unwinds
)
    
for
address_unwind
in
encoded_function_unwind
.
address_unwinds
:
      
complete_instruction_sequences
.
append
(
          
address_unwind
.
complete_instruction_sequence
)
  
unwind_instruction_table
unwind_instruction_table_offsets
=
(
      
EncodeUnwindInstructionTable
(
complete_instruction_sequences
)
)
  
function_offset_table
function_offset_table_offsets
=
(
      
EncodeFunctionOffsetTable
(
encoded_address_unwind_sequences
                                
unwind_instruction_table_offsets
)
)
  
page_table
function_table
=
EncodePageTableAndFunctionTable
(
      
encoded_function_unwinds
function_offset_table_offsets
)
  
return
(
page_table
function_table
function_offset_table
          
unwind_instruction_table
)
def
ReadTextSectionStartAddress
(
readobj_path
:
str
libchrome_path
:
str
)
-
>
int
:
  
"
"
"
Reads
the
.
text
section
start
address
of
libchrome
ELF
.
  
Arguments
:
    
readobj_path
:
Path
to
llvm
-
obj
binary
.
    
libchrome_path
:
Path
to
libchrome
binary
.
  
Returns
:
    
The
text
section
start
address
as
a
number
.
  
"
"
"
  
proc
=
subprocess
.
Popen
(
      
[
readobj_path
'
-
-
sections
'
'
-
-
elf
-
output
-
style
=
JSON
'
libchrome_path
]
      
stdout
=
subprocess
.
PIPE
      
encoding
=
'
ascii
'
)
  
elfs
=
json
.
loads
(
proc
.
stdout
.
read
(
)
)
[
0
]
  
assert
len
(
elfs
)
=
=
1
  
sections
=
list
(
elfs
.
values
(
)
)
[
0
]
[
'
Sections
'
]
  
return
next
(
s
[
'
Section
'
]
[
'
Address
'
]
for
s
in
sections
              
if
s
[
'
Section
'
]
[
'
Name
'
]
[
'
Value
'
]
=
=
'
.
text
'
)
def
main
(
)
:
  
build_utils
.
InitLogging
(
'
CREATE_UNWIND_TABLE_DEBUG
'
)
  
parser
=
argparse
.
ArgumentParser
(
description
=
__doc__
)
  
parser
.
add_argument
(
'
-
-
input_path
'
                      
help
=
'
Path
to
the
unstripped
binary
.
'
                      
required
=
True
                      
metavar
=
'
FILE
'
)
  
parser
.
add_argument
(
'
-
-
output_path
'
                      
help
=
'
Path
to
unwind
info
binary
output
.
'
                      
required
=
True
                      
metavar
=
'
FILE
'
)
  
parser
.
add_argument
(
'
-
-
dump_syms_path
'
                      
required
=
True
                      
help
=
'
The
path
of
the
dump_syms
binary
.
'
                      
metavar
=
'
FILE
'
)
  
parser
.
add_argument
(
'
-
-
readobj_path
'
                      
required
=
True
                      
help
=
'
The
path
of
the
llvm
-
readobj
binary
.
'
                      
metavar
=
'
FILE
'
)
  
args
=
parser
.
parse_args
(
)
  
proc
=
subprocess
.
Popen
(
[
'
.
/
'
+
args
.
dump_syms_path
args
.
input_path
'
-
v
'
]
                          
stdout
=
subprocess
.
PIPE
                          
encoding
=
'
ascii
'
)
  
function_cfis
=
ReadFunctionCfi
(
proc
.
stdout
)
  
function_unwinds
=
GenerateUnwinds
(
function_cfis
parsers
=
ALL_PARSERS
)
  
encoded_function_unwinds
=
EncodeFunctionUnwinds
(
      
function_unwinds
      
ReadTextSectionStartAddress
(
args
.
readobj_path
args
.
input_path
)
)
  
(
page_table
function_table
function_offset_table
   
unwind_instruction_table
)
=
GenerateUnwindTables
(
encoded_function_unwinds
)
  
unwind_info
:
bytes
=
EncodeUnwindInfo
(
page_table
function_table
                                        
function_offset_table
                                        
unwind_instruction_table
)
  
if
proc
.
wait
(
)
:
    
logging
.
critical
(
'
dump_syms
exited
with
return
code
%
d
'
proc
.
returncode
)
    
sys
.
exit
(
proc
.
returncode
)
  
with
open
(
args
.
output_path
'
wb
'
)
as
f
:
    
f
.
write
(
unwind_info
)
  
return
0
if
__name__
=
=
'
__main__
'
:
  
sys
.
exit
(
main
(
)
)
