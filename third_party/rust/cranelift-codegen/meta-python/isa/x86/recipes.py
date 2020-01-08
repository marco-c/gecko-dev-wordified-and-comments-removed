"
"
"
x86
Encoding
recipes
.
"
"
"
from
__future__
import
absolute_import
from
cdsl
.
isa
import
EncRecipe
from
cdsl
.
predicates
import
IsSignedInt
IsEqual
Or
from
cdsl
.
predicates
import
IsZero32BitFloat
IsZero64BitFloat
from
cdsl
.
registers
import
RegClass
from
base
.
formats
import
Unary
UnaryIeee32
UnaryIeee64
UnaryImm
UnaryBool
from
base
.
formats
import
Binary
BinaryImm
from
base
.
formats
import
MultiAry
NullAry
from
base
.
formats
import
Trap
Call
CallIndirect
Store
Load
from
base
.
formats
import
IntCompare
IntCompareImm
FloatCompare
from
base
.
formats
import
IntCond
FloatCond
from
base
.
formats
import
IntSelect
IntCondTrap
FloatCondTrap
from
base
.
formats
import
Jump
Branch
BranchInt
BranchFloat
from
base
.
formats
import
Ternary
FuncAddr
UnaryGlobalValue
from
base
.
formats
import
RegMove
RegSpill
RegFill
CopySpecial
from
base
.
formats
import
LoadComplex
StoreComplex
from
base
.
formats
import
StackLoad
from
.
registers
import
GPR
ABCD
FPR
GPR_DEREF_SAFE
GPR_ZERO_DEREF_SAFE
from
.
registers
import
GPR8
FPR8
GPR8_DEREF_SAFE
GPR8_ZERO_DEREF_SAFE
FLAG
from
.
registers
import
StackGPR32
StackFPR32
from
.
defs
import
supported_floatccs
from
.
settings
import
use_sse41
try
:
    
from
typing
import
Tuple
Dict
Sequence
Any
    
from
cdsl
.
instructions
import
InstructionFormat
    
from
cdsl
.
isa
import
ConstraintSeq
BranchRange
PredNode
OperandConstraint
except
ImportError
:
    
pass
OPCODE_PREFIX
=
{
        
(
)
:
(
'
Op1
'
0b0000
)
        
(
0x66
)
:
(
'
Mp1
'
0b0001
)
        
(
0xf3
)
:
(
'
Mp1
'
0b0010
)
        
(
0xf2
)
:
(
'
Mp1
'
0b0011
)
        
(
0x0f
)
:
(
'
Op2
'
0b0100
)
        
(
0x66
0x0f
)
:
(
'
Mp2
'
0b0101
)
        
(
0xf3
0x0f
)
:
(
'
Mp2
'
0b0110
)
        
(
0xf2
0x0f
)
:
(
'
Mp2
'
0b0111
)
        
(
0x0f
0x38
)
:
(
'
Op3
'
0b1000
)
        
(
0x66
0x0f
0x38
)
:
(
'
Mp3
'
0b1001
)
        
(
0xf3
0x0f
0x38
)
:
(
'
Mp3
'
0b1010
)
        
(
0xf2
0x0f
0x38
)
:
(
'
Mp3
'
0b1011
)
        
(
0x0f
0x3a
)
:
(
'
Op3
'
0b1100
)
        
(
0x66
0x0f
0x3a
)
:
(
'
Mp3
'
0b1101
)
        
(
0xf3
0x0f
0x3a
)
:
(
'
Mp3
'
0b1110
)
        
(
0xf2
0x0f
0x3a
)
:
(
'
Mp3
'
0b1111
)
        
}
def
decode_ops
(
ops
rrr
=
0
w
=
0
)
:
    
"
"
"
    
Given
a
sequence
of
opcode
bytes
compute
the
recipe
name
prefix
and
    
encoding
bits
.
    
"
"
"
    
assert
rrr
<
=
0b111
    
assert
w
<
=
1
    
name
mmpp
=
OPCODE_PREFIX
[
ops
[
:
-
1
]
]
    
op
=
ops
[
-
1
]
    
assert
op
<
=
256
    
return
(
name
op
|
(
mmpp
<
<
8
)
|
(
rrr
<
<
12
)
|
(
w
<
<
15
)
)
def
replace_put_op
(
emit
prefix
)
:
    
"
"
"
    
Given
a
snippet
of
Rust
code
(
or
None
)
replace
the
PUT_OP
macro
with
the
    
corresponding
put_
*
function
from
the
binemit
.
rs
module
.
    
"
"
"
    
if
emit
is
None
:
        
return
None
    
else
:
        
return
emit
.
replace
(
'
PUT_OP
'
'
put_
'
+
prefix
.
lower
(
)
)
NOREX_MAP
=
{
        
GPR
:
GPR8
        
GPR_DEREF_SAFE
:
GPR8_DEREF_SAFE
        
GPR_ZERO_DEREF_SAFE
:
GPR8_ZERO_DEREF_SAFE
        
FPR
:
FPR8
    
}
def
map_regs_norex
(
regs
)
:
    
return
tuple
(
NOREX_MAP
.
get
(
rc
rc
)
if
isinstance
(
rc
RegClass
)
else
rc
                 
for
rc
in
regs
)
class
TailRecipe
:
    
"
"
"
    
Generate
encoding
recipes
on
demand
.
    
x86
encodings
are
somewhat
orthogonal
with
the
opcode
representation
on
    
one
side
and
the
ModR
/
M
SIB
and
immediate
fields
on
the
other
side
.
    
A
TailRecipe
represents
the
part
of
an
encoding
that
follow
the
opcode
.
    
It
is
used
to
generate
full
encoding
recipes
on
demand
when
combined
with
    
an
opcode
.
    
The
arguments
are
the
same
as
for
an
EncRecipe
except
for
size
which
    
does
not
include
the
size
of
the
opcode
.
    
The
when_prefixed
parameter
specifies
a
recipe
that
should
be
substituted
    
for
this
one
when
a
REX
(
or
VEX
)
prefix
is
present
.
This
is
relevant
for
    
recipes
that
can
only
access
the
ABCD
registers
without
a
REX
prefix
but
    
are
able
to
access
all
registers
with
a
prefix
.
    
The
requires_prefix
parameter
indicates
that
the
recipe
can
'
t
be
used
    
without
a
REX
prefix
.
    
The
emit
parameter
contains
Rust
code
to
actually
emit
an
encoding
like
    
EncRecipe
does
it
.
Additionally
the
text
PUT_OP
is
substituted
with
    
the
proper
put_
*
function
from
the
x86
/
binemit
.
rs
module
.
    
"
"
"
    
def
__init__
(
            
self
            
name
            
format
            
size
            
ins
            
outs
            
branch_range
=
None
            
clobbers_flags
=
True
            
instp
=
None
            
isap
=
None
            
when_prefixed
=
None
            
requires_prefix
=
False
            
emit
=
None
            
)
:
        
self
.
name
=
name
        
self
.
format
=
format
        
self
.
size
=
size
        
self
.
ins
=
ins
        
self
.
outs
=
outs
        
self
.
branch_range
=
branch_range
        
self
.
clobbers_flags
=
clobbers_flags
        
self
.
instp
=
instp
        
self
.
isap
=
isap
        
self
.
when_prefixed
=
when_prefixed
        
self
.
requires_prefix
=
requires_prefix
        
self
.
emit
=
emit
        
self
.
recipes
=
dict
(
)
    
def
__call__
(
self
*
ops
*
*
kwargs
)
:
        
"
"
"
        
Create
an
encoding
recipe
and
encoding
bits
for
the
opcode
bytes
in
        
ops
.
        
"
"
"
        
assert
not
self
.
requires_prefix
"
Tail
recipe
requires
REX
prefix
.
"
        
rrr
=
kwargs
.
get
(
'
rrr
'
0
)
        
w
=
kwargs
.
get
(
'
w
'
0
)
        
name
bits
=
decode_ops
(
ops
rrr
w
)
        
size
=
len
(
ops
)
+
self
.
size
        
branch_range
=
None
        
if
self
.
branch_range
is
not
None
:
            
branch_range
=
(
size
self
.
branch_range
)
        
if
name
not
in
self
.
recipes
:
            
recipe
=
EncRecipe
(
                
name
+
self
.
name
                
self
.
format
                
size
                
ins
=
self
.
ins
                
outs
=
self
.
outs
                
branch_range
=
branch_range
                
clobbers_flags
=
self
.
clobbers_flags
                
instp
=
self
.
instp
                
isap
=
self
.
isap
                
emit
=
replace_put_op
(
self
.
emit
name
)
)
            
recipe
.
ins
=
map_regs_norex
(
recipe
.
ins
)
            
recipe
.
outs
=
map_regs_norex
(
recipe
.
outs
)
            
self
.
recipes
[
name
]
=
recipe
        
return
(
self
.
recipes
[
name
]
bits
)
    
def
rex
(
self
*
ops
*
*
kwargs
)
:
        
"
"
"
        
Create
a
REX
encoding
recipe
and
encoding
bits
for
the
opcode
bytes
in
        
ops
.
        
The
recipe
will
always
generate
a
REX
prefix
whether
it
is
required
or
        
not
.
For
instructions
that
don
'
t
require
a
REX
prefix
two
encodings
        
should
be
added
:
One
with
REX
and
one
without
.
        
"
"
"
        
if
self
.
when_prefixed
:
            
return
self
.
when_prefixed
.
rex
(
*
ops
*
*
kwargs
)
        
rrr
=
kwargs
.
get
(
'
rrr
'
0
)
        
w
=
kwargs
.
get
(
'
w
'
0
)
        
name
bits
=
decode_ops
(
ops
rrr
w
)
        
name
=
'
Rex
'
+
name
        
size
=
1
+
len
(
ops
)
+
self
.
size
        
branch_range
=
None
        
if
self
.
branch_range
is
not
None
:
            
branch_range
=
(
size
self
.
branch_range
)
        
if
name
not
in
self
.
recipes
:
            
recipe
=
EncRecipe
(
                
name
+
self
.
name
                
self
.
format
                
size
                
ins
=
self
.
ins
                
outs
=
self
.
outs
                
branch_range
=
branch_range
                
clobbers_flags
=
self
.
clobbers_flags
                
instp
=
self
.
instp
                
isap
=
self
.
isap
                
emit
=
replace_put_op
(
self
.
emit
name
)
)
            
self
.
recipes
[
name
]
=
recipe
        
return
(
self
.
recipes
[
name
]
bits
)
    
staticmethod
    
def
check_names
(
globs
)
:
        
for
name
obj
in
globs
.
items
(
)
:
            
if
isinstance
(
obj
TailRecipe
)
:
                
assert
name
=
=
obj
.
name
"
Mismatched
TailRecipe
name
:
"
+
name
def
floatccs
(
iform
)
:
    
"
"
"
    
Return
an
instruction
predicate
that
checks
in
iform
.
cond
is
one
of
the
    
directly
supported
floating
point
condition
codes
.
    
"
"
"
    
return
Or
(
*
(
IsEqual
(
iform
.
cond
cc
)
for
cc
in
supported_floatccs
)
)
null
=
EncRecipe
(
'
null
'
Unary
size
=
0
ins
=
GPR
outs
=
0
emit
=
'
'
)
trap
=
TailRecipe
(
        
'
trap
'
Trap
size
=
0
ins
=
(
)
outs
=
(
)
        
emit
=
'
'
'
        
sink
.
trap
(
code
func
.
srclocs
[
inst
]
)
;
        
PUT_OP
(
bits
BASE_REX
sink
)
;
        
'
'
'
)
trapif
=
EncRecipe
(
        
'
trapif
'
IntCondTrap
size
=
4
ins
=
FLAG
.
rflags
outs
=
(
)
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
/
/
Jump
over
a
2
-
byte
ud2
.
        
sink
.
put1
(
0x70
|
(
icc2opc
(
cond
.
inverse
(
)
)
as
u8
)
)
;
        
sink
.
put1
(
2
)
;
        
/
/
ud2
.
        
sink
.
trap
(
code
func
.
srclocs
[
inst
]
)
;
        
sink
.
put1
(
0x0f
)
;
        
sink
.
put1
(
0x0b
)
;
        
'
'
'
)
trapff
=
EncRecipe
(
        
'
trapff
'
FloatCondTrap
size
=
4
ins
=
FLAG
.
rflags
outs
=
(
)
        
clobbers_flags
=
False
        
instp
=
floatccs
(
FloatCondTrap
)
        
emit
=
'
'
'
        
/
/
Jump
over
a
2
-
byte
ud2
.
        
sink
.
put1
(
0x70
|
(
fcc2opc
(
cond
.
inverse
(
)
)
as
u8
)
)
;
        
sink
.
put1
(
2
)
;
        
/
/
ud2
.
        
sink
.
trap
(
code
func
.
srclocs
[
inst
]
)
;
        
sink
.
put1
(
0x0f
)
;
        
sink
.
put1
(
0x0b
)
;
        
'
'
'
)
rr
=
TailRecipe
(
        
'
rr
'
Binary
size
=
1
ins
=
(
GPR
GPR
)
outs
=
0
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
in_reg0
in_reg1
)
sink
)
;
        
modrm_rr
(
in_reg0
in_reg1
sink
)
;
        
'
'
'
)
rrx
=
TailRecipe
(
        
'
rrx
'
Binary
size
=
1
ins
=
(
GPR
GPR
)
outs
=
0
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
in_reg1
in_reg0
)
sink
)
;
        
modrm_rr
(
in_reg1
in_reg0
sink
)
;
        
'
'
'
)
fa
=
TailRecipe
(
        
'
fa
'
Binary
size
=
1
ins
=
(
FPR
FPR
)
outs
=
0
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
in_reg1
in_reg0
)
sink
)
;
        
modrm_rr
(
in_reg1
in_reg0
sink
)
;
        
'
'
'
)
fax
=
TailRecipe
(
        
'
fax
'
Binary
size
=
1
ins
=
(
FPR
FPR
)
outs
=
1
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
in_reg0
in_reg1
)
sink
)
;
        
modrm_rr
(
in_reg0
in_reg1
sink
)
;
        
'
'
'
)
ur
=
TailRecipe
(
        
'
ur
'
Unary
size
=
1
ins
=
GPR
outs
=
0
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex1
(
in_reg0
)
sink
)
;
        
modrm_r_bits
(
in_reg0
bits
sink
)
;
        
'
'
'
)
umr
=
TailRecipe
(
        
'
umr
'
Unary
size
=
1
ins
=
GPR
outs
=
GPR
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
out_reg0
in_reg0
)
sink
)
;
        
modrm_rr
(
out_reg0
in_reg0
sink
)
;
        
'
'
'
)
rfumr
=
TailRecipe
(
        
'
rfumr
'
Unary
size
=
1
ins
=
FPR
outs
=
GPR
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
out_reg0
in_reg0
)
sink
)
;
        
modrm_rr
(
out_reg0
in_reg0
sink
)
;
        
'
'
'
)
urm
=
TailRecipe
(
        
'
urm
'
Unary
size
=
1
ins
=
GPR
outs
=
GPR
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
in_reg0
out_reg0
)
sink
)
;
        
modrm_rr
(
in_reg0
out_reg0
sink
)
;
        
'
'
'
)
urm_noflags
=
TailRecipe
(
        
'
urm_noflags
'
Unary
size
=
1
ins
=
GPR
outs
=
GPR
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
in_reg0
out_reg0
)
sink
)
;
        
modrm_rr
(
in_reg0
out_reg0
sink
)
;
        
'
'
'
)
urm_noflags_abcd
=
TailRecipe
(
        
'
urm_noflags_abcd
'
Unary
size
=
1
ins
=
ABCD
outs
=
GPR
        
when_prefixed
=
urm_noflags
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
in_reg0
out_reg0
)
sink
)
;
        
modrm_rr
(
in_reg0
out_reg0
sink
)
;
        
'
'
'
)
furm
=
TailRecipe
(
        
'
furm
'
Unary
size
=
1
ins
=
FPR
outs
=
FPR
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
in_reg0
out_reg0
)
sink
)
;
        
modrm_rr
(
in_reg0
out_reg0
sink
)
;
        
'
'
'
)
frurm
=
TailRecipe
(
        
'
frurm
'
Unary
size
=
1
ins
=
GPR
outs
=
FPR
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
in_reg0
out_reg0
)
sink
)
;
        
modrm_rr
(
in_reg0
out_reg0
sink
)
;
        
'
'
'
)
rfurm
=
TailRecipe
(
        
'
rfurm
'
Unary
size
=
1
ins
=
FPR
outs
=
GPR
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
in_reg0
out_reg0
)
sink
)
;
        
modrm_rr
(
in_reg0
out_reg0
sink
)
;
        
'
'
'
)
furmi_rnd
=
TailRecipe
(
        
'
furmi_rnd
'
Unary
size
=
2
ins
=
FPR
outs
=
FPR
        
isap
=
use_sse41
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
in_reg0
out_reg0
)
sink
)
;
        
modrm_rr
(
in_reg0
out_reg0
sink
)
;
        
sink
.
put1
(
match
opcode
{
            
Opcode
:
:
Nearest
=
>
0b00
            
Opcode
:
:
Floor
=
>
0b01
            
Opcode
:
:
Ceil
=
>
0b10
            
Opcode
:
:
Trunc
=
>
0b11
            
x
=
>
panic
!
(
"
{
}
unexpected
for
furmi_rnd
"
opcode
)
        
}
)
;
        
'
'
'
)
rmov
=
TailRecipe
(
        
'
rmov
'
RegMove
size
=
1
ins
=
GPR
outs
=
(
)
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
dst
src
)
sink
)
;
        
modrm_rr
(
dst
src
sink
)
;
        
'
'
'
)
frmov
=
TailRecipe
(
        
'
frmov
'
RegMove
size
=
1
ins
=
FPR
outs
=
(
)
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
src
dst
)
sink
)
;
        
modrm_rr
(
src
dst
sink
)
;
        
'
'
'
)
rc
=
TailRecipe
(
        
'
rc
'
Binary
size
=
1
ins
=
(
GPR
GPR
.
rcx
)
outs
=
0
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex1
(
in_reg0
)
sink
)
;
        
modrm_r_bits
(
in_reg0
bits
sink
)
;
        
'
'
'
)
div
=
TailRecipe
(
        
'
div
'
Ternary
size
=
1
        
ins
=
(
GPR
.
rax
GPR
.
rdx
GPR
)
outs
=
(
GPR
.
rax
GPR
.
rdx
)
        
emit
=
'
'
'
        
sink
.
trap
(
TrapCode
:
:
IntegerDivisionByZero
func
.
srclocs
[
inst
]
)
;
        
PUT_OP
(
bits
rex1
(
in_reg2
)
sink
)
;
        
modrm_r_bits
(
in_reg2
bits
sink
)
;
        
'
'
'
)
mulx
=
TailRecipe
(
        
'
mulx
'
Binary
size
=
1
        
ins
=
(
GPR
.
rax
GPR
)
outs
=
(
GPR
.
rax
GPR
.
rdx
)
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex1
(
in_reg1
)
sink
)
;
        
modrm_r_bits
(
in_reg1
bits
sink
)
;
        
'
'
'
)
r_ib
=
TailRecipe
(
        
'
r_ib
'
BinaryImm
size
=
2
ins
=
GPR
outs
=
0
        
instp
=
IsSignedInt
(
BinaryImm
.
imm
8
)
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex1
(
in_reg0
)
sink
)
;
        
modrm_r_bits
(
in_reg0
bits
sink
)
;
        
let
imm
:
i64
=
imm
.
into
(
)
;
        
sink
.
put1
(
imm
as
u8
)
;
        
'
'
'
)
r_id
=
TailRecipe
(
        
'
r_id
'
BinaryImm
size
=
5
ins
=
GPR
outs
=
0
        
instp
=
IsSignedInt
(
BinaryImm
.
imm
32
)
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex1
(
in_reg0
)
sink
)
;
        
modrm_r_bits
(
in_reg0
bits
sink
)
;
        
let
imm
:
i64
=
imm
.
into
(
)
;
        
sink
.
put4
(
imm
as
u32
)
;
        
'
'
'
)
u_id
=
TailRecipe
(
        
'
u_id
'
UnaryImm
size
=
5
ins
=
(
)
outs
=
GPR
        
instp
=
IsSignedInt
(
UnaryImm
.
imm
32
)
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex1
(
out_reg0
)
sink
)
;
        
modrm_r_bits
(
out_reg0
bits
sink
)
;
        
let
imm
:
i64
=
imm
.
into
(
)
;
        
sink
.
put4
(
imm
as
u32
)
;
        
'
'
'
)
pu_id
=
TailRecipe
(
        
'
pu_id
'
UnaryImm
size
=
4
ins
=
(
)
outs
=
GPR
        
emit
=
'
'
'
        
/
/
The
destination
register
is
encoded
in
the
low
bits
of
the
opcode
.
        
/
/
No
ModR
/
M
.
        
PUT_OP
(
bits
|
(
out_reg0
&
7
)
rex1
(
out_reg0
)
sink
)
;
        
let
imm
:
i64
=
imm
.
into
(
)
;
        
sink
.
put4
(
imm
as
u32
)
;
        
'
'
'
)
pu_id_bool
=
TailRecipe
(
        
'
pu_id_bool
'
UnaryBool
size
=
4
ins
=
(
)
outs
=
GPR
        
emit
=
'
'
'
        
/
/
The
destination
register
is
encoded
in
the
low
bits
of
the
opcode
.
        
/
/
No
ModR
/
M
.
        
PUT_OP
(
bits
|
(
out_reg0
&
7
)
rex1
(
out_reg0
)
sink
)
;
        
let
imm
:
u32
=
if
imm
{
1
}
else
{
0
}
;
        
sink
.
put4
(
imm
)
;
        
'
'
'
)
pu_iq
=
TailRecipe
(
        
'
pu_iq
'
UnaryImm
size
=
8
ins
=
(
)
outs
=
GPR
        
emit
=
'
'
'
        
PUT_OP
(
bits
|
(
out_reg0
&
7
)
rex1
(
out_reg0
)
sink
)
;
        
let
imm
:
i64
=
imm
.
into
(
)
;
        
sink
.
put8
(
imm
as
u64
)
;
        
'
'
'
)
f32imm_z
=
TailRecipe
(
    
'
f32imm_z
'
UnaryIeee32
size
=
1
ins
=
(
)
outs
=
FPR
    
instp
=
IsZero32BitFloat
(
UnaryIeee32
.
imm
)
    
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
out_reg0
out_reg0
)
sink
)
;
        
modrm_rr
(
out_reg0
out_reg0
sink
)
;
    
'
'
'
)
f64imm_z
=
TailRecipe
(
    
'
f64imm_z
'
UnaryIeee64
size
=
1
ins
=
(
)
outs
=
FPR
    
instp
=
IsZero64BitFloat
(
UnaryIeee64
.
imm
)
    
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
out_reg0
out_reg0
)
sink
)
;
        
modrm_rr
(
out_reg0
out_reg0
sink
)
;
    
'
'
'
)
pushq
=
TailRecipe
(
    
'
pushq
'
Unary
size
=
0
ins
=
GPR
outs
=
(
)
    
emit
=
'
'
'
    
sink
.
trap
(
TrapCode
:
:
StackOverflow
func
.
srclocs
[
inst
]
)
;
    
PUT_OP
(
bits
|
(
in_reg0
&
7
)
rex1
(
in_reg0
)
sink
)
;
    
'
'
'
)
popq
=
TailRecipe
(
    
'
popq
'
NullAry
size
=
0
ins
=
(
)
outs
=
GPR
    
emit
=
'
'
'
    
PUT_OP
(
bits
|
(
out_reg0
&
7
)
rex1
(
out_reg0
)
sink
)
;
    
'
'
'
)
copysp
=
TailRecipe
(
        
'
copysp
'
CopySpecial
size
=
1
ins
=
(
)
outs
=
(
)
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
dst
src
)
sink
)
;
        
modrm_rr
(
dst
src
sink
)
;
        
'
'
'
)
adjustsp
=
TailRecipe
(
    
'
adjustsp
'
Unary
size
=
1
ins
=
(
GPR
)
outs
=
(
)
    
emit
=
'
'
'
    
PUT_OP
(
bits
rex2
(
RU
:
:
rsp
.
into
(
)
in_reg0
)
sink
)
;
    
modrm_rr
(
RU
:
:
rsp
.
into
(
)
in_reg0
sink
)
;
    
'
'
'
)
adjustsp_ib
=
TailRecipe
(
    
'
adjustsp_ib
'
UnaryImm
size
=
2
ins
=
(
)
outs
=
(
)
    
instp
=
IsSignedInt
(
UnaryImm
.
imm
8
)
    
emit
=
'
'
'
    
PUT_OP
(
bits
rex1
(
RU
:
:
rsp
.
into
(
)
)
sink
)
;
    
modrm_r_bits
(
RU
:
:
rsp
.
into
(
)
bits
sink
)
;
    
let
imm
:
i64
=
imm
.
into
(
)
;
    
sink
.
put1
(
imm
as
u8
)
;
    
'
'
'
)
adjustsp_id
=
TailRecipe
(
    
'
adjustsp_id
'
UnaryImm
size
=
5
ins
=
(
)
outs
=
(
)
    
instp
=
IsSignedInt
(
UnaryImm
.
imm
32
)
    
emit
=
'
'
'
    
PUT_OP
(
bits
rex1
(
RU
:
:
rsp
.
into
(
)
)
sink
)
;
    
modrm_r_bits
(
RU
:
:
rsp
.
into
(
)
bits
sink
)
;
    
let
imm
:
i64
=
imm
.
into
(
)
;
    
sink
.
put4
(
imm
as
u32
)
;
    
'
'
'
)
fnaddr4
=
TailRecipe
(
        
'
fnaddr4
'
FuncAddr
size
=
4
ins
=
(
)
outs
=
GPR
        
emit
=
'
'
'
        
PUT_OP
(
bits
|
(
out_reg0
&
7
)
rex1
(
out_reg0
)
sink
)
;
        
sink
.
reloc_external
(
Reloc
:
:
Abs4
                            
&
func
.
dfg
.
ext_funcs
[
func_ref
]
.
name
                            
0
)
;
        
sink
.
put4
(
0
)
;
        
'
'
'
)
fnaddr8
=
TailRecipe
(
        
'
fnaddr8
'
FuncAddr
size
=
8
ins
=
(
)
outs
=
GPR
        
emit
=
'
'
'
        
PUT_OP
(
bits
|
(
out_reg0
&
7
)
rex1
(
out_reg0
)
sink
)
;
        
sink
.
reloc_external
(
Reloc
:
:
Abs8
                            
&
func
.
dfg
.
ext_funcs
[
func_ref
]
.
name
                            
0
)
;
        
sink
.
put8
(
0
)
;
        
'
'
'
)
allones_fnaddr4
=
TailRecipe
(
        
'
allones_fnaddr4
'
FuncAddr
size
=
4
ins
=
(
)
outs
=
GPR
        
emit
=
'
'
'
        
PUT_OP
(
bits
|
(
out_reg0
&
7
)
rex1
(
out_reg0
)
sink
)
;
        
sink
.
reloc_external
(
Reloc
:
:
Abs4
                            
&
func
.
dfg
.
ext_funcs
[
func_ref
]
.
name
                            
0
)
;
        
/
/
Write
the
immediate
as
!
0
for
the
benefit
of
BaldrMonkey
.
        
sink
.
put4
(
!
0
)
;
        
'
'
'
)
allones_fnaddr8
=
TailRecipe
(
        
'
allones_fnaddr8
'
FuncAddr
size
=
8
ins
=
(
)
outs
=
GPR
        
emit
=
'
'
'
        
PUT_OP
(
bits
|
(
out_reg0
&
7
)
rex1
(
out_reg0
)
sink
)
;
        
sink
.
reloc_external
(
Reloc
:
:
Abs8
                            
&
func
.
dfg
.
ext_funcs
[
func_ref
]
.
name
                            
0
)
;
        
/
/
Write
the
immediate
as
!
0
for
the
benefit
of
BaldrMonkey
.
        
sink
.
put8
(
!
0
)
;
        
'
'
'
)
pcrel_fnaddr8
=
TailRecipe
(
        
'
pcrel_fnaddr8
'
FuncAddr
size
=
5
ins
=
(
)
outs
=
GPR
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
0
out_reg0
)
sink
)
;
        
modrm_riprel
(
out_reg0
sink
)
;
        
/
/
The
addend
adjusts
for
the
difference
between
the
end
of
the
        
/
/
instruction
and
the
beginning
of
the
immediate
field
.
        
sink
.
reloc_external
(
Reloc
:
:
X86PCRel4
                            
&
func
.
dfg
.
ext_funcs
[
func_ref
]
.
name
                            
-
4
)
;
        
sink
.
put4
(
0
)
;
        
'
'
'
)
got_fnaddr8
=
TailRecipe
(
        
'
got_fnaddr8
'
FuncAddr
size
=
5
ins
=
(
)
outs
=
GPR
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
0
out_reg0
)
sink
)
;
        
modrm_riprel
(
out_reg0
sink
)
;
        
/
/
The
addend
adjusts
for
the
difference
between
the
end
of
the
        
/
/
instruction
and
the
beginning
of
the
immediate
field
.
        
sink
.
reloc_external
(
Reloc
:
:
X86GOTPCRel4
                            
&
func
.
dfg
.
ext_funcs
[
func_ref
]
.
name
                            
-
4
)
;
        
sink
.
put4
(
0
)
;
        
'
'
'
)
gvaddr4
=
TailRecipe
(
        
'
gvaddr4
'
UnaryGlobalValue
size
=
4
ins
=
(
)
outs
=
GPR
        
emit
=
'
'
'
        
PUT_OP
(
bits
|
(
out_reg0
&
7
)
rex1
(
out_reg0
)
sink
)
;
        
sink
.
reloc_external
(
Reloc
:
:
Abs4
                            
&
func
.
global_values
[
global_value
]
.
symbol_name
(
)
                            
0
)
;
        
sink
.
put4
(
0
)
;
        
'
'
'
)
gvaddr8
=
TailRecipe
(
        
'
gvaddr8
'
UnaryGlobalValue
size
=
8
ins
=
(
)
outs
=
GPR
        
emit
=
'
'
'
        
PUT_OP
(
bits
|
(
out_reg0
&
7
)
rex1
(
out_reg0
)
sink
)
;
        
sink
.
reloc_external
(
Reloc
:
:
Abs8
                            
&
func
.
global_values
[
global_value
]
.
symbol_name
(
)
                            
0
)
;
        
sink
.
put8
(
0
)
;
        
'
'
'
)
pcrel_gvaddr8
=
TailRecipe
(
        
'
pcrel_gvaddr8
'
UnaryGlobalValue
size
=
5
ins
=
(
)
outs
=
GPR
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
0
out_reg0
)
sink
)
;
        
modrm_rm
(
5
out_reg0
sink
)
;
        
/
/
The
addend
adjusts
for
the
difference
between
the
end
of
the
        
/
/
instruction
and
the
beginning
of
the
immediate
field
.
        
sink
.
reloc_external
(
Reloc
:
:
X86PCRel4
                            
&
func
.
global_values
[
global_value
]
.
symbol_name
(
)
                            
-
4
)
;
        
sink
.
put4
(
0
)
;
        
'
'
'
)
got_gvaddr8
=
TailRecipe
(
        
'
got_gvaddr8
'
UnaryGlobalValue
size
=
5
ins
=
(
)
outs
=
GPR
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
0
out_reg0
)
sink
)
;
        
modrm_rm
(
5
out_reg0
sink
)
;
        
/
/
The
addend
adjusts
for
the
difference
between
the
end
of
the
        
/
/
instruction
and
the
beginning
of
the
immediate
field
.
        
sink
.
reloc_external
(
Reloc
:
:
X86GOTPCRel4
                            
&
func
.
global_values
[
global_value
]
.
symbol_name
(
)
                            
-
4
)
;
        
sink
.
put4
(
0
)
;
        
'
'
'
)
spaddr4_id
=
TailRecipe
(
        
'
spaddr4_id
'
StackLoad
size
=
6
ins
=
(
)
outs
=
GPR
        
emit
=
'
'
'
        
let
sp
=
StackRef
:
:
sp
(
stack_slot
&
func
.
stack_slots
)
;
        
let
base
=
stk_base
(
sp
.
base
)
;
        
PUT_OP
(
bits
rex2
(
out_reg0
base
)
sink
)
;
        
modrm_sib_disp8
(
out_reg0
sink
)
;
        
sib_noindex
(
base
sink
)
;
        
let
imm
:
i32
=
offset
.
into
(
)
;
        
sink
.
put4
(
sp
.
offset
.
checked_add
(
imm
)
.
unwrap
(
)
as
u32
)
;
        
'
'
'
)
spaddr8_id
=
TailRecipe
(
        
'
spaddr8_id
'
StackLoad
size
=
6
ins
=
(
)
outs
=
GPR
        
emit
=
'
'
'
        
let
sp
=
StackRef
:
:
sp
(
stack_slot
&
func
.
stack_slots
)
;
        
let
base
=
stk_base
(
sp
.
base
)
;
        
PUT_OP
(
bits
rex2
(
base
out_reg0
)
sink
)
;
        
modrm_sib_disp32
(
out_reg0
sink
)
;
        
sib_noindex
(
base
sink
)
;
        
let
imm
:
i32
=
offset
.
into
(
)
;
        
sink
.
put4
(
sp
.
offset
.
checked_add
(
imm
)
.
unwrap
(
)
as
u32
)
;
        
'
'
'
)
st
=
TailRecipe
(
        
'
st
'
Store
size
=
1
ins
=
(
GPR
GPR_ZERO_DEREF_SAFE
)
outs
=
(
)
        
instp
=
IsEqual
(
Store
.
offset
0
)
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
if
!
flags
.
notrap
(
)
{
            
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
        
}
        
PUT_OP
(
bits
rex2
(
in_reg1
in_reg0
)
sink
)
;
        
modrm_rm
(
in_reg1
in_reg0
sink
)
;
        
'
'
'
)
stWithIndex
=
TailRecipe
(
    
'
stWithIndex
'
StoreComplex
size
=
2
    
ins
=
(
GPR
GPR_ZERO_DEREF_SAFE
GPR_DEREF_SAFE
)
    
outs
=
(
)
    
instp
=
IsEqual
(
StoreComplex
.
offset
0
)
    
clobbers_flags
=
False
    
emit
=
'
'
'
    
if
!
flags
.
notrap
(
)
{
        
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
    
}
    
PUT_OP
(
bits
rex3
(
in_reg1
in_reg0
in_reg2
)
sink
)
;
    
modrm_sib
(
in_reg0
sink
)
;
    
sib
(
0
in_reg2
in_reg1
sink
)
;
    
'
'
'
)
st_abcd
=
TailRecipe
(
        
'
st_abcd
'
Store
size
=
1
ins
=
(
ABCD
GPR
)
outs
=
(
)
        
instp
=
IsEqual
(
Store
.
offset
0
)
        
when_prefixed
=
st
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
if
!
flags
.
notrap
(
)
{
            
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
        
}
        
PUT_OP
(
bits
rex2
(
in_reg1
in_reg0
)
sink
)
;
        
modrm_rm
(
in_reg1
in_reg0
sink
)
;
        
'
'
'
)
stWithIndex_abcd
=
TailRecipe
(
    
'
stWithIndex_abcd
'
StoreComplex
size
=
2
    
ins
=
(
ABCD
GPR_ZERO_DEREF_SAFE
GPR_DEREF_SAFE
)
    
outs
=
(
)
    
instp
=
IsEqual
(
StoreComplex
.
offset
0
)
    
clobbers_flags
=
False
    
emit
=
'
'
'
    
if
!
flags
.
notrap
(
)
{
        
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
    
}
    
PUT_OP
(
bits
rex3
(
in_reg1
in_reg0
in_reg2
)
sink
)
;
    
modrm_sib
(
in_reg0
sink
)
;
    
sib
(
0
in_reg2
in_reg1
sink
)
;
    
'
'
'
)
fst
=
TailRecipe
(
        
'
fst
'
Store
size
=
1
ins
=
(
FPR
GPR_ZERO_DEREF_SAFE
)
outs
=
(
)
        
instp
=
IsEqual
(
Store
.
offset
0
)
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
if
!
flags
.
notrap
(
)
{
            
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
        
}
        
PUT_OP
(
bits
rex2
(
in_reg1
in_reg0
)
sink
)
;
        
modrm_rm
(
in_reg1
in_reg0
sink
)
;
        
'
'
'
)
fstWithIndex
=
TailRecipe
(
        
'
fstWithIndex
'
StoreComplex
size
=
2
        
ins
=
(
FPR
GPR_ZERO_DEREF_SAFE
GPR_DEREF_SAFE
)
outs
=
(
)
        
instp
=
IsEqual
(
StoreComplex
.
offset
0
)
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
if
!
flags
.
notrap
(
)
{
            
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
        
}
        
PUT_OP
(
bits
rex3
(
in_reg1
in_reg0
in_reg2
)
sink
)
;
        
modrm_sib
(
in_reg0
sink
)
;
        
sib
(
0
in_reg2
in_reg1
sink
)
;
        
'
'
'
)
stDisp8
=
TailRecipe
(
        
'
stDisp8
'
Store
size
=
2
ins
=
(
GPR
GPR_DEREF_SAFE
)
outs
=
(
)
        
instp
=
IsSignedInt
(
Store
.
offset
8
)
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
if
!
flags
.
notrap
(
)
{
            
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
        
}
        
PUT_OP
(
bits
rex2
(
in_reg1
in_reg0
)
sink
)
;
        
modrm_disp8
(
in_reg1
in_reg0
sink
)
;
        
let
offset
:
i32
=
offset
.
into
(
)
;
        
sink
.
put1
(
offset
as
u8
)
;
        
'
'
'
)
stWithIndexDisp8
=
TailRecipe
(
    
'
stWithIndexDisp8
'
StoreComplex
size
=
3
    
ins
=
(
GPR
GPR
GPR_DEREF_SAFE
)
    
outs
=
(
)
    
instp
=
IsSignedInt
(
StoreComplex
.
offset
8
)
    
clobbers_flags
=
False
    
emit
=
'
'
'
    
if
!
flags
.
notrap
(
)
{
        
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
    
}
    
PUT_OP
(
bits
rex3
(
in_reg1
in_reg0
in_reg2
)
sink
)
;
    
modrm_sib_disp8
(
in_reg0
sink
)
;
    
sib
(
0
in_reg2
in_reg1
sink
)
;
    
let
offset
:
i32
=
offset
.
into
(
)
;
    
sink
.
put1
(
offset
as
u8
)
;
    
'
'
'
)
stDisp8_abcd
=
TailRecipe
(
        
'
stDisp8_abcd
'
Store
size
=
2
ins
=
(
ABCD
GPR
)
outs
=
(
)
        
instp
=
IsSignedInt
(
Store
.
offset
8
)
        
when_prefixed
=
stDisp8
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
if
!
flags
.
notrap
(
)
{
            
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
        
}
        
PUT_OP
(
bits
rex2
(
in_reg1
in_reg0
)
sink
)
;
        
modrm_disp8
(
in_reg1
in_reg0
sink
)
;
        
let
offset
:
i32
=
offset
.
into
(
)
;
        
sink
.
put1
(
offset
as
u8
)
;
        
'
'
'
)
stWithIndexDisp8_abcd
=
TailRecipe
(
    
'
stWithIndexDisp8_abcd
'
StoreComplex
size
=
3
    
ins
=
(
ABCD
GPR
GPR_DEREF_SAFE
)
    
outs
=
(
)
    
instp
=
IsSignedInt
(
StoreComplex
.
offset
8
)
    
clobbers_flags
=
False
    
emit
=
'
'
'
    
if
!
flags
.
notrap
(
)
{
        
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
    
}
    
PUT_OP
(
bits
rex3
(
in_reg1
in_reg0
in_reg2
)
sink
)
;
    
modrm_sib_disp8
(
in_reg0
sink
)
;
    
sib
(
0
in_reg2
in_reg1
sink
)
;
    
let
offset
:
i32
=
offset
.
into
(
)
;
    
sink
.
put1
(
offset
as
u8
)
;
    
'
'
'
)
fstDisp8
=
TailRecipe
(
        
'
fstDisp8
'
Store
size
=
2
ins
=
(
FPR
GPR_DEREF_SAFE
)
outs
=
(
)
        
instp
=
IsSignedInt
(
Store
.
offset
8
)
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
if
!
flags
.
notrap
(
)
{
            
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
        
}
        
PUT_OP
(
bits
rex2
(
in_reg1
in_reg0
)
sink
)
;
        
modrm_disp8
(
in_reg1
in_reg0
sink
)
;
        
let
offset
:
i32
=
offset
.
into
(
)
;
        
sink
.
put1
(
offset
as
u8
)
;
        
'
'
'
)
fstWithIndexDisp8
=
TailRecipe
(
    
'
fstWithIndexDisp8
'
StoreComplex
size
=
3
    
ins
=
(
FPR
GPR
GPR_DEREF_SAFE
)
    
outs
=
(
)
    
instp
=
IsSignedInt
(
StoreComplex
.
offset
8
)
    
clobbers_flags
=
False
    
emit
=
'
'
'
    
if
!
flags
.
notrap
(
)
{
        
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
    
}
    
PUT_OP
(
bits
rex3
(
in_reg1
in_reg0
in_reg2
)
sink
)
;
    
modrm_sib_disp8
(
in_reg0
sink
)
;
    
sib
(
0
in_reg2
in_reg1
sink
)
;
    
let
offset
:
i32
=
offset
.
into
(
)
;
    
sink
.
put1
(
offset
as
u8
)
;
    
'
'
'
)
stDisp32
=
TailRecipe
(
        
'
stDisp32
'
Store
size
=
5
ins
=
(
GPR
GPR_DEREF_SAFE
)
outs
=
(
)
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
if
!
flags
.
notrap
(
)
{
            
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
        
}
        
PUT_OP
(
bits
rex2
(
in_reg1
in_reg0
)
sink
)
;
        
modrm_disp32
(
in_reg1
in_reg0
sink
)
;
        
let
offset
:
i32
=
offset
.
into
(
)
;
        
sink
.
put4
(
offset
as
u32
)
;
        
'
'
'
)
stWithIndexDisp32
=
TailRecipe
(
    
'
stWithIndexDisp32
'
StoreComplex
size
=
6
    
ins
=
(
GPR
GPR
GPR_DEREF_SAFE
)
    
outs
=
(
)
    
instp
=
IsSignedInt
(
StoreComplex
.
offset
32
)
    
clobbers_flags
=
False
    
emit
=
'
'
'
    
if
!
flags
.
notrap
(
)
{
        
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
    
}
    
PUT_OP
(
bits
rex3
(
in_reg1
in_reg0
in_reg2
)
sink
)
;
    
modrm_sib_disp32
(
in_reg0
sink
)
;
    
sib
(
0
in_reg2
in_reg1
sink
)
;
    
let
offset
:
i32
=
offset
.
into
(
)
;
    
sink
.
put4
(
offset
as
u32
)
;
    
'
'
'
)
stDisp32_abcd
=
TailRecipe
(
        
'
stDisp32_abcd
'
Store
size
=
5
ins
=
(
ABCD
GPR
)
outs
=
(
)
        
when_prefixed
=
stDisp32
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
if
!
flags
.
notrap
(
)
{
            
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
        
}
        
PUT_OP
(
bits
rex2
(
in_reg1
in_reg0
)
sink
)
;
        
modrm_disp32
(
in_reg1
in_reg0
sink
)
;
        
let
offset
:
i32
=
offset
.
into
(
)
;
        
sink
.
put4
(
offset
as
u32
)
;
        
'
'
'
)
stWithIndexDisp32_abcd
=
TailRecipe
(
    
'
stWithIndexDisp32_abcd
'
StoreComplex
size
=
6
    
ins
=
(
ABCD
GPR
GPR_DEREF_SAFE
)
    
outs
=
(
)
    
instp
=
IsSignedInt
(
StoreComplex
.
offset
32
)
    
clobbers_flags
=
False
    
emit
=
'
'
'
    
if
!
flags
.
notrap
(
)
{
        
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
    
}
    
PUT_OP
(
bits
rex3
(
in_reg1
in_reg0
in_reg2
)
sink
)
;
    
modrm_sib_disp32
(
in_reg0
sink
)
;
    
sib
(
0
in_reg2
in_reg1
sink
)
;
    
let
offset
:
i32
=
offset
.
into
(
)
;
    
sink
.
put4
(
offset
as
u32
)
;
    
'
'
'
)
fstDisp32
=
TailRecipe
(
        
'
fstDisp32
'
Store
size
=
5
ins
=
(
FPR
GPR_DEREF_SAFE
)
outs
=
(
)
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
if
!
flags
.
notrap
(
)
{
            
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
        
}
        
PUT_OP
(
bits
rex2
(
in_reg1
in_reg0
)
sink
)
;
        
modrm_disp32
(
in_reg1
in_reg0
sink
)
;
        
let
offset
:
i32
=
offset
.
into
(
)
;
        
sink
.
put4
(
offset
as
u32
)
;
        
'
'
'
)
fstWithIndexDisp32
=
TailRecipe
(
    
'
fstWithIndexDisp32
'
StoreComplex
size
=
6
    
ins
=
(
FPR
GPR
GPR_DEREF_SAFE
)
    
outs
=
(
)
    
instp
=
IsSignedInt
(
StoreComplex
.
offset
32
)
    
clobbers_flags
=
False
    
emit
=
'
'
'
    
if
!
flags
.
notrap
(
)
{
        
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
    
}
    
PUT_OP
(
bits
rex3
(
in_reg1
in_reg0
in_reg2
)
sink
)
;
    
modrm_sib_disp32
(
in_reg0
sink
)
;
    
sib
(
0
in_reg2
in_reg1
sink
)
;
    
let
offset
:
i32
=
offset
.
into
(
)
;
    
sink
.
put4
(
offset
as
u32
)
;
    
'
'
'
)
spillSib32
=
TailRecipe
(
        
'
spillSib32
'
Unary
size
=
6
ins
=
GPR
outs
=
StackGPR32
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
sink
.
trap
(
TrapCode
:
:
StackOverflow
func
.
srclocs
[
inst
]
)
;
        
let
base
=
stk_base
(
out_stk0
.
base
)
;
        
PUT_OP
(
bits
rex2
(
base
in_reg0
)
sink
)
;
        
modrm_sib_disp32
(
in_reg0
sink
)
;
        
sib_noindex
(
base
sink
)
;
        
sink
.
put4
(
out_stk0
.
offset
as
u32
)
;
        
'
'
'
)
fspillSib32
=
TailRecipe
(
        
'
fspillSib32
'
Unary
size
=
6
ins
=
FPR
outs
=
StackFPR32
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
sink
.
trap
(
TrapCode
:
:
StackOverflow
func
.
srclocs
[
inst
]
)
;
        
let
base
=
stk_base
(
out_stk0
.
base
)
;
        
PUT_OP
(
bits
rex2
(
base
in_reg0
)
sink
)
;
        
modrm_sib_disp32
(
in_reg0
sink
)
;
        
sib_noindex
(
base
sink
)
;
        
sink
.
put4
(
out_stk0
.
offset
as
u32
)
;
        
'
'
'
)
regspill32
=
TailRecipe
(
        
'
regspill32
'
RegSpill
size
=
6
ins
=
GPR
outs
=
(
)
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
sink
.
trap
(
TrapCode
:
:
StackOverflow
func
.
srclocs
[
inst
]
)
;
        
let
dst
=
StackRef
:
:
sp
(
dst
&
func
.
stack_slots
)
;
        
let
base
=
stk_base
(
dst
.
base
)
;
        
PUT_OP
(
bits
rex2
(
base
src
)
sink
)
;
        
modrm_sib_disp32
(
src
sink
)
;
        
sib_noindex
(
base
sink
)
;
        
sink
.
put4
(
dst
.
offset
as
u32
)
;
        
'
'
'
)
fregspill32
=
TailRecipe
(
        
'
fregspill32
'
RegSpill
size
=
6
ins
=
FPR
outs
=
(
)
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
sink
.
trap
(
TrapCode
:
:
StackOverflow
func
.
srclocs
[
inst
]
)
;
        
let
dst
=
StackRef
:
:
sp
(
dst
&
func
.
stack_slots
)
;
        
let
base
=
stk_base
(
dst
.
base
)
;
        
PUT_OP
(
bits
rex2
(
base
src
)
sink
)
;
        
modrm_sib_disp32
(
src
sink
)
;
        
sib_noindex
(
base
sink
)
;
        
sink
.
put4
(
dst
.
offset
as
u32
)
;
        
'
'
'
)
ld
=
TailRecipe
(
        
'
ld
'
Load
size
=
1
ins
=
(
GPR_ZERO_DEREF_SAFE
)
outs
=
(
GPR
)
        
instp
=
IsEqual
(
Load
.
offset
0
)
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
if
!
flags
.
notrap
(
)
{
            
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
        
}
        
PUT_OP
(
bits
rex2
(
in_reg0
out_reg0
)
sink
)
;
        
modrm_rm
(
in_reg0
out_reg0
sink
)
;
        
'
'
'
)
ldWithIndex
=
TailRecipe
(
    
'
ldWithIndex
'
LoadComplex
size
=
2
    
ins
=
(
GPR_ZERO_DEREF_SAFE
GPR_DEREF_SAFE
)
    
outs
=
(
GPR
)
    
instp
=
IsEqual
(
LoadComplex
.
offset
0
)
    
clobbers_flags
=
False
    
emit
=
'
'
'
    
if
!
flags
.
notrap
(
)
{
        
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
    
}
    
PUT_OP
(
bits
rex3
(
in_reg0
out_reg0
in_reg1
)
sink
)
;
    
modrm_sib
(
out_reg0
sink
)
;
    
sib
(
0
in_reg1
in_reg0
sink
)
;
    
'
'
'
)
fld
=
TailRecipe
(
        
'
fld
'
Load
size
=
1
ins
=
(
GPR_ZERO_DEREF_SAFE
)
outs
=
(
FPR
)
        
instp
=
IsEqual
(
Load
.
offset
0
)
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
if
!
flags
.
notrap
(
)
{
            
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
        
}
        
PUT_OP
(
bits
rex2
(
in_reg0
out_reg0
)
sink
)
;
        
modrm_rm
(
in_reg0
out_reg0
sink
)
;
        
'
'
'
)
fldWithIndex
=
TailRecipe
(
    
'
fldWithIndex
'
LoadComplex
size
=
2
    
ins
=
(
GPR_ZERO_DEREF_SAFE
GPR_DEREF_SAFE
)
    
outs
=
(
FPR
)
    
instp
=
IsEqual
(
LoadComplex
.
offset
0
)
    
clobbers_flags
=
False
    
emit
=
'
'
'
    
if
!
flags
.
notrap
(
)
{
        
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
    
}
    
PUT_OP
(
bits
rex3
(
in_reg0
out_reg0
in_reg1
)
sink
)
;
    
modrm_sib
(
out_reg0
sink
)
;
    
sib
(
0
in_reg1
in_reg0
sink
)
;
    
'
'
'
)
ldDisp8
=
TailRecipe
(
        
'
ldDisp8
'
Load
size
=
2
ins
=
(
GPR_DEREF_SAFE
)
outs
=
(
GPR
)
        
instp
=
IsSignedInt
(
Load
.
offset
8
)
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
if
!
flags
.
notrap
(
)
{
            
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
        
}
        
PUT_OP
(
bits
rex2
(
in_reg0
out_reg0
)
sink
)
;
        
modrm_disp8
(
in_reg0
out_reg0
sink
)
;
        
let
offset
:
i32
=
offset
.
into
(
)
;
        
sink
.
put1
(
offset
as
u8
)
;
        
'
'
'
)
ldWithIndexDisp8
=
TailRecipe
(
    
'
ldWithIndexDisp8
'
LoadComplex
size
=
3
    
ins
=
(
GPR
GPR_DEREF_SAFE
)
    
outs
=
(
GPR
)
    
instp
=
IsSignedInt
(
LoadComplex
.
offset
8
)
    
clobbers_flags
=
False
    
emit
=
'
'
'
    
if
!
flags
.
notrap
(
)
{
        
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
    
}
    
PUT_OP
(
bits
rex3
(
in_reg0
out_reg0
in_reg1
)
sink
)
;
    
modrm_sib_disp8
(
out_reg0
sink
)
;
    
sib
(
0
in_reg1
in_reg0
sink
)
;
    
let
offset
:
i32
=
offset
.
into
(
)
;
    
sink
.
put1
(
offset
as
u8
)
;
    
'
'
'
)
fldDisp8
=
TailRecipe
(
        
'
fldDisp8
'
Load
size
=
2
ins
=
(
GPR_DEREF_SAFE
)
outs
=
(
FPR
)
        
instp
=
IsSignedInt
(
Load
.
offset
8
)
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
if
!
flags
.
notrap
(
)
{
            
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
        
}
        
PUT_OP
(
bits
rex2
(
in_reg0
out_reg0
)
sink
)
;
        
modrm_disp8
(
in_reg0
out_reg0
sink
)
;
        
let
offset
:
i32
=
offset
.
into
(
)
;
        
sink
.
put1
(
offset
as
u8
)
;
        
'
'
'
)
fldWithIndexDisp8
=
TailRecipe
(
    
'
fldWithIndexDisp8
'
LoadComplex
size
=
3
    
ins
=
(
GPR
GPR_DEREF_SAFE
)
    
outs
=
(
FPR
)
    
instp
=
IsSignedInt
(
LoadComplex
.
offset
8
)
    
clobbers_flags
=
False
    
emit
=
'
'
'
    
if
!
flags
.
notrap
(
)
{
        
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
    
}
    
PUT_OP
(
bits
rex3
(
in_reg0
out_reg0
in_reg1
)
sink
)
;
    
modrm_sib_disp8
(
out_reg0
sink
)
;
    
sib
(
0
in_reg1
in_reg0
sink
)
;
    
let
offset
:
i32
=
offset
.
into
(
)
;
    
sink
.
put1
(
offset
as
u8
)
;
    
'
'
'
)
ldDisp32
=
TailRecipe
(
        
'
ldDisp32
'
Load
size
=
5
ins
=
(
GPR_DEREF_SAFE
)
outs
=
(
GPR
)
        
instp
=
IsSignedInt
(
Load
.
offset
32
)
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
if
!
flags
.
notrap
(
)
{
            
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
        
}
        
PUT_OP
(
bits
rex2
(
in_reg0
out_reg0
)
sink
)
;
        
modrm_disp32
(
in_reg0
out_reg0
sink
)
;
        
let
offset
:
i32
=
offset
.
into
(
)
;
        
sink
.
put4
(
offset
as
u32
)
;
        
'
'
'
)
ldWithIndexDisp32
=
TailRecipe
(
    
'
ldWithIndexDisp32
'
LoadComplex
size
=
6
    
ins
=
(
GPR
GPR_DEREF_SAFE
)
    
outs
=
(
GPR
)
    
instp
=
IsSignedInt
(
LoadComplex
.
offset
32
)
    
clobbers_flags
=
False
    
emit
=
'
'
'
    
if
!
flags
.
notrap
(
)
{
        
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
    
}
    
PUT_OP
(
bits
rex3
(
in_reg0
out_reg0
in_reg1
)
sink
)
;
    
modrm_sib_disp32
(
out_reg0
sink
)
;
    
sib
(
0
in_reg1
in_reg0
sink
)
;
    
let
offset
:
i32
=
offset
.
into
(
)
;
    
sink
.
put4
(
offset
as
u32
)
;
    
'
'
'
)
fldDisp32
=
TailRecipe
(
        
'
fldDisp32
'
Load
size
=
5
ins
=
(
GPR_DEREF_SAFE
)
outs
=
(
FPR
)
        
instp
=
IsSignedInt
(
Load
.
offset
32
)
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
if
!
flags
.
notrap
(
)
{
            
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
        
}
        
PUT_OP
(
bits
rex2
(
in_reg0
out_reg0
)
sink
)
;
        
modrm_disp32
(
in_reg0
out_reg0
sink
)
;
        
let
offset
:
i32
=
offset
.
into
(
)
;
        
sink
.
put4
(
offset
as
u32
)
;
        
'
'
'
)
fldWithIndexDisp32
=
TailRecipe
(
    
'
fldWithIndexDisp32
'
LoadComplex
size
=
6
    
ins
=
(
GPR
GPR_DEREF_SAFE
)
    
outs
=
(
FPR
)
    
instp
=
IsSignedInt
(
LoadComplex
.
offset
32
)
    
clobbers_flags
=
False
    
emit
=
'
'
'
    
if
!
flags
.
notrap
(
)
{
        
sink
.
trap
(
TrapCode
:
:
HeapOutOfBounds
func
.
srclocs
[
inst
]
)
;
    
}
    
PUT_OP
(
bits
rex3
(
in_reg0
out_reg0
in_reg1
)
sink
)
;
    
modrm_sib_disp32
(
out_reg0
sink
)
;
    
sib
(
0
in_reg1
in_reg0
sink
)
;
    
let
offset
:
i32
=
offset
.
into
(
)
;
    
sink
.
put4
(
offset
as
u32
)
;
    
'
'
'
)
fillSib32
=
TailRecipe
(
        
'
fillSib32
'
Unary
size
=
6
ins
=
StackGPR32
outs
=
GPR
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
let
base
=
stk_base
(
in_stk0
.
base
)
;
        
PUT_OP
(
bits
rex2
(
base
out_reg0
)
sink
)
;
        
modrm_sib_disp32
(
out_reg0
sink
)
;
        
sib_noindex
(
base
sink
)
;
        
sink
.
put4
(
in_stk0
.
offset
as
u32
)
;
        
'
'
'
)
ffillSib32
=
TailRecipe
(
        
'
ffillSib32
'
Unary
size
=
6
ins
=
StackFPR32
outs
=
FPR
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
let
base
=
stk_base
(
in_stk0
.
base
)
;
        
PUT_OP
(
bits
rex2
(
base
out_reg0
)
sink
)
;
        
modrm_sib_disp32
(
out_reg0
sink
)
;
        
sib_noindex
(
base
sink
)
;
        
sink
.
put4
(
in_stk0
.
offset
as
u32
)
;
        
'
'
'
)
regfill32
=
TailRecipe
(
        
'
regfill32
'
RegFill
size
=
6
ins
=
StackGPR32
outs
=
(
)
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
let
src
=
StackRef
:
:
sp
(
src
&
func
.
stack_slots
)
;
        
let
base
=
stk_base
(
src
.
base
)
;
        
PUT_OP
(
bits
rex2
(
base
dst
)
sink
)
;
        
modrm_sib_disp32
(
dst
sink
)
;
        
sib_noindex
(
base
sink
)
;
        
sink
.
put4
(
src
.
offset
as
u32
)
;
        
'
'
'
)
fregfill32
=
TailRecipe
(
        
'
fregfill32
'
RegFill
size
=
6
ins
=
StackFPR32
outs
=
(
)
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
let
src
=
StackRef
:
:
sp
(
src
&
func
.
stack_slots
)
;
        
let
base
=
stk_base
(
src
.
base
)
;
        
PUT_OP
(
bits
rex2
(
base
dst
)
sink
)
;
        
modrm_sib_disp32
(
dst
sink
)
;
        
sib_noindex
(
base
sink
)
;
        
sink
.
put4
(
src
.
offset
as
u32
)
;
        
'
'
'
)
call_id
=
TailRecipe
(
        
'
call_id
'
Call
size
=
4
ins
=
(
)
outs
=
(
)
        
emit
=
'
'
'
        
sink
.
trap
(
TrapCode
:
:
StackOverflow
func
.
srclocs
[
inst
]
)
;
        
PUT_OP
(
bits
BASE_REX
sink
)
;
        
/
/
The
addend
adjusts
for
the
difference
between
the
end
of
the
        
/
/
instruction
and
the
beginning
of
the
immediate
field
.
        
sink
.
reloc_external
(
Reloc
:
:
X86CallPCRel4
                            
&
func
.
dfg
.
ext_funcs
[
func_ref
]
.
name
                            
-
4
)
;
        
sink
.
put4
(
0
)
;
        
'
'
'
)
call_plt_id
=
TailRecipe
(
        
'
call_plt_id
'
Call
size
=
4
ins
=
(
)
outs
=
(
)
        
emit
=
'
'
'
        
sink
.
trap
(
TrapCode
:
:
StackOverflow
func
.
srclocs
[
inst
]
)
;
        
PUT_OP
(
bits
BASE_REX
sink
)
;
        
sink
.
reloc_external
(
Reloc
:
:
X86CallPLTRel4
                            
&
func
.
dfg
.
ext_funcs
[
func_ref
]
.
name
                            
-
4
)
;
        
sink
.
put4
(
0
)
;
        
'
'
'
)
call_r
=
TailRecipe
(
        
'
call_r
'
CallIndirect
size
=
1
ins
=
GPR
outs
=
(
)
        
emit
=
'
'
'
        
sink
.
trap
(
TrapCode
:
:
StackOverflow
func
.
srclocs
[
inst
]
)
;
        
PUT_OP
(
bits
rex1
(
in_reg0
)
sink
)
;
        
modrm_r_bits
(
in_reg0
bits
sink
)
;
        
'
'
'
)
ret
=
TailRecipe
(
        
'
ret
'
MultiAry
size
=
0
ins
=
(
)
outs
=
(
)
        
emit
=
'
'
'
        
PUT_OP
(
bits
BASE_REX
sink
)
;
        
'
'
'
)
jmpb
=
TailRecipe
(
        
'
jmpb
'
Jump
size
=
1
ins
=
(
)
outs
=
(
)
        
branch_range
=
8
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
PUT_OP
(
bits
BASE_REX
sink
)
;
        
disp1
(
destination
func
sink
)
;
        
'
'
'
)
jmpd
=
TailRecipe
(
        
'
jmpd
'
Jump
size
=
4
ins
=
(
)
outs
=
(
)
        
branch_range
=
32
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
PUT_OP
(
bits
BASE_REX
sink
)
;
        
disp4
(
destination
func
sink
)
;
        
'
'
'
)
brib
=
TailRecipe
(
        
'
brib
'
BranchInt
size
=
1
ins
=
FLAG
.
rflags
outs
=
(
)
        
branch_range
=
8
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
PUT_OP
(
bits
|
icc2opc
(
cond
)
BASE_REX
sink
)
;
        
disp1
(
destination
func
sink
)
;
        
'
'
'
)
brid
=
TailRecipe
(
        
'
brid
'
BranchInt
size
=
4
ins
=
FLAG
.
rflags
outs
=
(
)
        
branch_range
=
32
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
PUT_OP
(
bits
|
icc2opc
(
cond
)
BASE_REX
sink
)
;
        
disp4
(
destination
func
sink
)
;
        
'
'
'
)
brfb
=
TailRecipe
(
        
'
brfb
'
BranchFloat
size
=
1
ins
=
FLAG
.
rflags
outs
=
(
)
        
branch_range
=
8
        
clobbers_flags
=
False
        
instp
=
floatccs
(
BranchFloat
)
        
emit
=
'
'
'
        
PUT_OP
(
bits
|
fcc2opc
(
cond
)
BASE_REX
sink
)
;
        
disp1
(
destination
func
sink
)
;
        
'
'
'
)
brfd
=
TailRecipe
(
        
'
brfd
'
BranchFloat
size
=
4
ins
=
FLAG
.
rflags
outs
=
(
)
        
branch_range
=
32
        
clobbers_flags
=
False
        
instp
=
floatccs
(
BranchFloat
)
        
emit
=
'
'
'
        
PUT_OP
(
bits
|
fcc2opc
(
cond
)
BASE_REX
sink
)
;
        
disp4
(
destination
func
sink
)
;
        
'
'
'
)
seti
=
TailRecipe
(
        
'
seti
'
IntCond
size
=
1
ins
=
FLAG
.
rflags
outs
=
GPR
        
requires_prefix
=
True
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
PUT_OP
(
bits
|
icc2opc
(
cond
)
rex1
(
out_reg0
)
sink
)
;
        
modrm_r_bits
(
out_reg0
bits
sink
)
;
        
'
'
'
)
seti_abcd
=
TailRecipe
(
        
'
seti_abcd
'
IntCond
size
=
1
ins
=
FLAG
.
rflags
outs
=
ABCD
        
when_prefixed
=
seti
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
PUT_OP
(
bits
|
icc2opc
(
cond
)
rex1
(
out_reg0
)
sink
)
;
        
modrm_r_bits
(
out_reg0
bits
sink
)
;
        
'
'
'
)
setf
=
TailRecipe
(
        
'
setf
'
FloatCond
size
=
1
ins
=
FLAG
.
rflags
outs
=
GPR
        
requires_prefix
=
True
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
PUT_OP
(
bits
|
fcc2opc
(
cond
)
rex1
(
out_reg0
)
sink
)
;
        
modrm_r_bits
(
out_reg0
bits
sink
)
;
        
'
'
'
)
setf_abcd
=
TailRecipe
(
        
'
setf_abcd
'
FloatCond
size
=
1
ins
=
FLAG
.
rflags
outs
=
ABCD
        
when_prefixed
=
setf
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
PUT_OP
(
bits
|
fcc2opc
(
cond
)
rex1
(
out_reg0
)
sink
)
;
        
modrm_r_bits
(
out_reg0
bits
sink
)
;
        
'
'
'
)
cmov
=
TailRecipe
(
        
'
cmov
'
IntSelect
size
=
1
ins
=
(
FLAG
.
rflags
GPR
GPR
)
outs
=
2
        
requires_prefix
=
False
        
clobbers_flags
=
False
        
emit
=
'
'
'
        
PUT_OP
(
bits
|
icc2opc
(
cond
)
rex2
(
in_reg1
in_reg2
)
sink
)
;
        
modrm_rr
(
in_reg1
in_reg2
sink
)
;
        
'
'
'
)
bsf_and_bsr
=
TailRecipe
(
        
'
bsf_and_bsr
'
Unary
size
=
1
ins
=
GPR
outs
=
(
GPR
FLAG
.
rflags
)
        
requires_prefix
=
False
        
clobbers_flags
=
True
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
in_reg0
out_reg0
)
sink
)
;
        
modrm_rr
(
in_reg0
out_reg0
sink
)
;
        
'
'
'
)
rcmp
=
TailRecipe
(
        
'
rcmp
'
Binary
size
=
1
ins
=
(
GPR
GPR
)
outs
=
FLAG
.
rflags
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
in_reg0
in_reg1
)
sink
)
;
        
modrm_rr
(
in_reg0
in_reg1
sink
)
;
        
'
'
'
)
fcmp
=
TailRecipe
(
        
'
fcmp
'
Binary
size
=
1
ins
=
(
FPR
FPR
)
outs
=
FLAG
.
rflags
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
in_reg1
in_reg0
)
sink
)
;
        
modrm_rr
(
in_reg1
in_reg0
sink
)
;
        
'
'
'
)
rcmp_ib
=
TailRecipe
(
        
'
rcmp_ib
'
BinaryImm
size
=
2
ins
=
GPR
outs
=
FLAG
.
rflags
        
instp
=
IsSignedInt
(
BinaryImm
.
imm
8
)
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex1
(
in_reg0
)
sink
)
;
        
modrm_r_bits
(
in_reg0
bits
sink
)
;
        
let
imm
:
i64
=
imm
.
into
(
)
;
        
sink
.
put1
(
imm
as
u8
)
;
        
'
'
'
)
rcmp_id
=
TailRecipe
(
        
'
rcmp_id
'
BinaryImm
size
=
5
ins
=
GPR
outs
=
FLAG
.
rflags
        
instp
=
IsSignedInt
(
BinaryImm
.
imm
32
)
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex1
(
in_reg0
)
sink
)
;
        
modrm_r_bits
(
in_reg0
bits
sink
)
;
        
let
imm
:
i64
=
imm
.
into
(
)
;
        
sink
.
put4
(
imm
as
u32
)
;
        
'
'
'
)
rcmp_sp
=
TailRecipe
(
        
'
rcmp_sp
'
Unary
size
=
1
ins
=
GPR
outs
=
FLAG
.
rflags
        
emit
=
'
'
'
        
PUT_OP
(
bits
rex2
(
in_reg0
RU
:
:
rsp
.
into
(
)
)
sink
)
;
        
modrm_rr
(
in_reg0
RU
:
:
rsp
.
into
(
)
sink
)
;
        
'
'
'
)
tjccb
=
TailRecipe
(
        
'
tjccb
'
Branch
size
=
1
+
2
ins
=
GPR
outs
=
(
)
        
branch_range
=
8
        
emit
=
'
'
'
        
/
/
test
r
r
.
        
PUT_OP
(
(
bits
&
0xff00
)
|
0x85
rex2
(
in_reg0
in_reg0
)
sink
)
;
        
modrm_rr
(
in_reg0
in_reg0
sink
)
;
        
/
/
Jcc
instruction
.
        
sink
.
put1
(
bits
as
u8
)
;
        
disp1
(
destination
func
sink
)
;
        
'
'
'
)
tjccd
=
TailRecipe
(
        
'
tjccd
'
Branch
size
=
1
+
6
ins
=
GPR
outs
=
(
)
        
branch_range
=
32
        
emit
=
'
'
'
        
/
/
test
r
r
.
        
PUT_OP
(
(
bits
&
0xff00
)
|
0x85
rex2
(
in_reg0
in_reg0
)
sink
)
;
        
modrm_rr
(
in_reg0
in_reg0
sink
)
;
        
/
/
Jcc
instruction
.
        
sink
.
put1
(
0x0f
)
;
        
sink
.
put1
(
bits
as
u8
)
;
        
disp4
(
destination
func
sink
)
;
        
'
'
'
)
t8jccb
=
TailRecipe
(
        
'
t8jccb
'
Branch
size
=
1
+
2
ins
=
GPR
outs
=
(
)
        
branch_range
=
8
        
requires_prefix
=
True
        
emit
=
'
'
'
        
/
/
test8
r
r
.
        
PUT_OP
(
(
bits
&
0xff00
)
|
0x84
rex2
(
in_reg0
in_reg0
)
sink
)
;
        
modrm_rr
(
in_reg0
in_reg0
sink
)
;
        
/
/
Jcc
instruction
.
        
sink
.
put1
(
bits
as
u8
)
;
        
disp1
(
destination
func
sink
)
;
        
'
'
'
)
t8jccb_abcd
=
TailRecipe
(
        
'
t8jccb_abcd
'
Branch
size
=
1
+
2
ins
=
ABCD
outs
=
(
)
        
branch_range
=
8
        
when_prefixed
=
t8jccb
        
emit
=
'
'
'
        
/
/
test8
r
r
.
        
PUT_OP
(
(
bits
&
0xff00
)
|
0x84
rex2
(
in_reg0
in_reg0
)
sink
)
;
        
modrm_rr
(
in_reg0
in_reg0
sink
)
;
        
/
/
Jcc
instruction
.
        
sink
.
put1
(
bits
as
u8
)
;
        
disp1
(
destination
func
sink
)
;
        
'
'
'
)
t8jccd
=
TailRecipe
(
        
'
t8jccd
'
Branch
size
=
1
+
6
ins
=
GPR
outs
=
(
)
        
branch_range
=
32
        
requires_prefix
=
True
        
emit
=
'
'
'
        
/
/
test8
r
r
.
        
PUT_OP
(
(
bits
&
0xff00
)
|
0x84
rex2
(
in_reg0
in_reg0
)
sink
)
;
        
modrm_rr
(
in_reg0
in_reg0
sink
)
;
        
/
/
Jcc
instruction
.
        
sink
.
put1
(
0x0f
)
;
        
sink
.
put1
(
bits
as
u8
)
;
        
disp4
(
destination
func
sink
)
;
        
'
'
'
)
t8jccd_abcd
=
TailRecipe
(
        
'
t8jccd_abcd
'
Branch
size
=
1
+
6
ins
=
ABCD
outs
=
(
)
        
branch_range
=
32
        
when_prefixed
=
t8jccd
        
emit
=
'
'
'
        
/
/
test8
r
r
.
        
PUT_OP
(
(
bits
&
0xff00
)
|
0x84
rex2
(
in_reg0
in_reg0
)
sink
)
;
        
modrm_rr
(
in_reg0
in_reg0
sink
)
;
        
/
/
Jcc
instruction
.
        
sink
.
put1
(
0x0f
)
;
        
sink
.
put1
(
bits
as
u8
)
;
        
disp4
(
destination
func
sink
)
;
        
'
'
'
)
t8jccd_long
=
TailRecipe
(
        
'
t8jccd_long
'
Branch
size
=
5
+
6
ins
=
GPR
outs
=
(
)
        
branch_range
=
32
        
emit
=
'
'
'
        
/
/
test32
r
0xff
.
        
PUT_OP
(
(
bits
&
0xff00
)
|
0xf7
rex1
(
in_reg0
)
sink
)
;
        
modrm_r_bits
(
in_reg0
bits
sink
)
;
        
sink
.
put4
(
0xff
)
;
        
/
/
Jcc
instruction
.
        
sink
.
put1
(
0x0f
)
;
        
sink
.
put1
(
bits
as
u8
)
;
        
disp4
(
destination
func
sink
)
;
        
'
'
'
)
icscc
=
TailRecipe
(
        
'
icscc
'
IntCompare
size
=
1
+
3
ins
=
(
GPR
GPR
)
outs
=
ABCD
        
emit
=
'
'
'
        
/
/
Comparison
instruction
.
        
PUT_OP
(
bits
rex2
(
in_reg0
in_reg1
)
sink
)
;
        
modrm_rr
(
in_reg0
in_reg1
sink
)
;
        
/
/
setCC
instruction
no
REX
.
        
use
ir
:
:
condcodes
:
:
IntCC
:
:
*
;
        
let
setcc
=
match
cond
{
            
Equal
=
>
0x94
            
NotEqual
=
>
0x95
            
SignedLessThan
=
>
0x9c
            
SignedGreaterThanOrEqual
=
>
0x9d
            
SignedGreaterThan
=
>
0x9f
            
SignedLessThanOrEqual
=
>
0x9e
            
UnsignedLessThan
=
>
0x92
            
UnsignedGreaterThanOrEqual
=
>
0x93
            
UnsignedGreaterThan
=
>
0x97
            
UnsignedLessThanOrEqual
=
>
0x96
        
}
;
        
sink
.
put1
(
0x0f
)
;
        
sink
.
put1
(
setcc
)
;
        
modrm_rr
(
out_reg0
0
sink
)
;
        
'
'
'
)
icscc_ib
=
TailRecipe
(
        
'
icscc_ib
'
IntCompareImm
size
=
2
+
3
ins
=
GPR
outs
=
ABCD
        
instp
=
IsSignedInt
(
IntCompareImm
.
imm
8
)
        
emit
=
'
'
'
        
/
/
Comparison
instruction
.
        
PUT_OP
(
bits
rex1
(
in_reg0
)
sink
)
;
        
modrm_r_bits
(
in_reg0
bits
sink
)
;
        
let
imm
:
i64
=
imm
.
into
(
)
;
        
sink
.
put1
(
imm
as
u8
)
;
        
/
/
setCC
instruction
no
REX
.
        
use
ir
:
:
condcodes
:
:
IntCC
:
:
*
;
        
let
setcc
=
match
cond
{
            
Equal
=
>
0x94
            
NotEqual
=
>
0x95
            
SignedLessThan
=
>
0x9c
            
SignedGreaterThanOrEqual
=
>
0x9d
            
SignedGreaterThan
=
>
0x9f
            
SignedLessThanOrEqual
=
>
0x9e
            
UnsignedLessThan
=
>
0x92
            
UnsignedGreaterThanOrEqual
=
>
0x93
            
UnsignedGreaterThan
=
>
0x97
            
UnsignedLessThanOrEqual
=
>
0x96
        
}
;
        
sink
.
put1
(
0x0f
)
;
        
sink
.
put1
(
setcc
)
;
        
modrm_rr
(
out_reg0
0
sink
)
;
        
'
'
'
)
icscc_id
=
TailRecipe
(
        
'
icscc_id
'
IntCompareImm
size
=
5
+
3
ins
=
GPR
outs
=
ABCD
        
instp
=
IsSignedInt
(
IntCompareImm
.
imm
32
)
        
emit
=
'
'
'
        
/
/
Comparison
instruction
.
        
PUT_OP
(
bits
rex1
(
in_reg0
)
sink
)
;
        
modrm_r_bits
(
in_reg0
bits
sink
)
;
        
let
imm
:
i64
=
imm
.
into
(
)
;
        
sink
.
put4
(
imm
as
u32
)
;
        
/
/
setCC
instruction
no
REX
.
        
use
ir
:
:
condcodes
:
:
IntCC
:
:
*
;
        
let
setcc
=
match
cond
{
            
Equal
=
>
0x94
            
NotEqual
=
>
0x95
            
SignedLessThan
=
>
0x9c
            
SignedGreaterThanOrEqual
=
>
0x9d
            
SignedGreaterThan
=
>
0x9f
            
SignedLessThanOrEqual
=
>
0x9e
            
UnsignedLessThan
=
>
0x92
            
UnsignedGreaterThanOrEqual
=
>
0x93
            
UnsignedGreaterThan
=
>
0x97
            
UnsignedLessThanOrEqual
=
>
0x96
        
}
;
        
sink
.
put1
(
0x0f
)
;
        
sink
.
put1
(
setcc
)
;
        
modrm_rr
(
out_reg0
0
sink
)
;
        
'
'
'
)
fcscc
=
TailRecipe
(
        
'
fcscc
'
FloatCompare
size
=
1
+
3
ins
=
(
FPR
FPR
)
outs
=
ABCD
        
instp
=
floatccs
(
FloatCompare
)
        
emit
=
'
'
'
        
/
/
Comparison
instruction
.
        
PUT_OP
(
bits
rex2
(
in_reg1
in_reg0
)
sink
)
;
        
modrm_rr
(
in_reg1
in_reg0
sink
)
;
        
/
/
setCC
instruction
no
REX
.
        
use
ir
:
:
condcodes
:
:
FloatCC
:
:
*
;
        
let
setcc
=
match
cond
{
            
Ordered
=
>
0x9b
/
/
EQ
|
LT
|
GT
=
>
setnp
(
P
=
0
)
            
Unordered
=
>
0x9a
/
/
UN
=
>
setp
(
P
=
1
)
            
OrderedNotEqual
=
>
0x95
/
/
LT
|
GT
=
>
setne
(
Z
=
0
)
            
UnorderedOrEqual
=
>
0x94
/
/
UN
|
EQ
=
>
sete
(
Z
=
1
)
            
GreaterThan
=
>
0x97
/
/
GT
=
>
seta
(
C
=
0
&
Z
=
0
)
            
GreaterThanOrEqual
=
>
0x93
/
/
GT
|
EQ
=
>
setae
(
C
=
0
)
            
UnorderedOrLessThan
=
>
0x92
/
/
UN
|
LT
=
>
setb
(
C
=
1
)
            
UnorderedOrLessThanOrEqual
=
>
0x96
/
/
UN
|
LT
|
EQ
=
>
setbe
(
Z
=
1
|
C
=
1
)
            
Equal
|
/
/
EQ
            
NotEqual
|
/
/
UN
|
LT
|
GT
            
LessThan
|
/
/
LT
            
LessThanOrEqual
|
/
/
LT
|
EQ
            
UnorderedOrGreaterThan
|
/
/
UN
|
GT
            
UnorderedOrGreaterThanOrEqual
/
/
UN
|
GT
|
EQ
            
=
>
panic
!
(
"
{
}
not
supported
by
fcscc
"
cond
)
        
}
;
        
sink
.
put1
(
0x0f
)
;
        
sink
.
put1
(
setcc
)
;
        
modrm_rr
(
out_reg0
0
sink
)
;
        
'
'
'
)
TailRecipe
.
check_names
(
globals
(
)
)
