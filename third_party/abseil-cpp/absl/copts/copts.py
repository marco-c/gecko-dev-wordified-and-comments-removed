"
"
"
Abseil
compiler
options
.
This
is
the
source
of
truth
for
Abseil
compiler
options
.
To
modify
Abseil
compilation
options
:
  
(
1
)
Edit
the
appropriate
list
in
this
file
based
on
the
platform
the
flag
is
      
needed
on
.
  
(
2
)
Run
<
path_to_absl
>
/
copts
/
generate_copts
.
py
.
The
generated
copts
are
consumed
by
configure_copts
.
bzl
and
AbseilConfigureCopts
.
cmake
.
"
"
"
ABSL_GCC_FLAGS
=
[
    
"
-
Wall
"
    
"
-
Wextra
"
    
"
-
Wcast
-
qual
"
    
"
-
Wconversion
-
null
"
    
"
-
Wformat
-
security
"
    
"
-
Wmissing
-
declarations
"
    
"
-
Wnon
-
virtual
-
dtor
"
    
"
-
Woverlength
-
strings
"
    
"
-
Wpointer
-
arith
"
    
"
-
Wundef
"
    
"
-
Wunused
-
local
-
typedefs
"
    
"
-
Wunused
-
result
"
    
"
-
Wvarargs
"
    
"
-
Wvla
"
    
"
-
Wwrite
-
strings
"
    
"
-
DNOMINMAX
"
]
ABSL_GCC_TEST_ADDITIONAL_FLAGS
=
[
    
"
-
Wno
-
deprecated
-
declarations
"
    
"
-
Wno
-
missing
-
declarations
"
    
"
-
Wno
-
self
-
move
"
    
"
-
Wno
-
sign
-
compare
"
    
"
-
Wno
-
unused
-
function
"
    
"
-
Wno
-
unused
-
parameter
"
    
"
-
Wno
-
unused
-
private
-
field
"
]
ABSL_LLVM_FLAGS
=
[
    
"
-
Wall
"
    
"
-
Wextra
"
    
"
-
Wc
+
+
98
-
compat
-
extra
-
semi
"
    
"
-
Wcast
-
qual
"
    
"
-
Wconversion
"
    
"
-
Wdeprecated
-
pragma
"
    
"
-
Wfloat
-
overflow
-
conversion
"
    
"
-
Wfloat
-
zero
-
conversion
"
    
"
-
Wfor
-
loop
-
analysis
"
    
"
-
Wformat
-
security
"
    
"
-
Wgnu
-
redeclared
-
enum
"
    
"
-
Winfinite
-
recursion
"
    
"
-
Winvalid
-
constexpr
"
    
"
-
Wliteral
-
conversion
"
    
"
-
Wmissing
-
declarations
"
    
"
-
Wnullability
-
completeness
"
    
"
-
Woverlength
-
strings
"
    
"
-
Wpointer
-
arith
"
    
"
-
Wself
-
assign
"
    
"
-
Wshadow
-
all
"
    
"
-
Wshorten
-
64
-
to
-
32
"
    
"
-
Wsign
-
conversion
"
    
"
-
Wstring
-
conversion
"
    
"
-
Wtautological
-
overlap
-
compare
"
    
"
-
Wtautological
-
unsigned
-
zero
-
compare
"
    
"
-
Wthread
-
safety
"
    
"
-
Wundef
"
    
"
-
Wuninitialized
"
    
"
-
Wunreachable
-
code
"
    
"
-
Wunused
-
comparison
"
    
"
-
Wunused
-
local
-
typedefs
"
    
"
-
Wunused
-
result
"
    
"
-
Wvla
"
    
"
-
Wwrite
-
strings
"
    
"
-
Wno
-
float
-
conversion
"
    
"
-
Wno
-
implicit
-
float
-
conversion
"
    
"
-
Wno
-
implicit
-
int
-
float
-
conversion
"
    
"
-
Wno
-
unknown
-
warning
-
option
"
    
"
-
DNOMINMAX
"
]
ABSL_LLVM_TEST_ADDITIONAL_FLAGS
=
[
    
"
-
Wno
-
deprecated
-
declarations
"
    
"
-
Wno
-
implicit
-
int
-
conversion
"
    
"
-
Wno
-
missing
-
prototypes
"
    
"
-
Wno
-
missing
-
variable
-
declarations
"
    
"
-
Wno
-
shadow
"
    
"
-
Wno
-
shorten
-
64
-
to
-
32
"
    
"
-
Wno
-
sign
-
compare
"
    
"
-
Wno
-
sign
-
conversion
"
    
"
-
Wno
-
unreachable
-
code
-
loop
-
increment
"
    
"
-
Wno
-
unused
-
function
"
    
"
-
Wno
-
unused
-
member
-
function
"
    
"
-
Wno
-
unused
-
parameter
"
    
"
-
Wno
-
unused
-
private
-
field
"
    
"
-
Wno
-
unused
-
template
"
    
"
-
Wno
-
used
-
but
-
marked
-
unused
"
    
"
-
Wno
-
gnu
-
zero
-
variadic
-
macro
-
arguments
"
]
MSVC_BIG_WARNING_FLAGS
=
[
    
"
/
W3
"
]
MSVC_WARNING_FLAGS
=
[
    
"
/
bigobj
"
    
"
/
wd4005
"
    
"
/
wd4068
"
    
"
/
wd4180
"
    
"
/
wd4503
"
    
"
/
wd4800
"
]
MSVC_DEFINES
=
[
    
"
/
DNOMINMAX
"
    
"
/
DWIN32_LEAN_AND_MEAN
"
    
"
/
D_CRT_SECURE_NO_WARNINGS
"
    
"
/
D_SCL_SECURE_NO_WARNINGS
"
    
"
/
D_ENABLE_EXTENDED_ALIGNED_STORAGE
"
]
def
GccStyleFilterAndCombine
(
default_flags
test_flags
)
:
  
"
"
"
Merges
default_flags
and
test_flags
for
GCC
and
LLVM
.
  
Args
:
    
default_flags
:
A
list
of
default
compiler
flags
    
test_flags
:
A
list
of
flags
that
are
only
used
in
tests
  
Returns
:
    
A
combined
list
of
default_flags
and
test_flags
but
with
all
flags
of
the
    
form
'
-
Wwarning
'
removed
if
test_flags
contains
a
flag
of
the
form
    
'
-
Wno
-
warning
'
  
"
"
"
  
remove
=
set
(
[
"
-
W
"
+
f
[
5
:
]
for
f
in
test_flags
if
f
[
:
5
]
=
=
"
-
Wno
-
"
]
)
  
return
[
f
for
f
in
default_flags
if
f
not
in
remove
]
+
test_flags
COPT_VARS
=
{
    
"
ABSL_GCC_FLAGS
"
:
ABSL_GCC_FLAGS
    
"
ABSL_GCC_TEST_FLAGS
"
:
GccStyleFilterAndCombine
(
        
ABSL_GCC_FLAGS
ABSL_GCC_TEST_ADDITIONAL_FLAGS
    
)
    
"
ABSL_LLVM_FLAGS
"
:
ABSL_LLVM_FLAGS
    
"
ABSL_LLVM_TEST_FLAGS
"
:
GccStyleFilterAndCombine
(
        
ABSL_LLVM_FLAGS
ABSL_LLVM_TEST_ADDITIONAL_FLAGS
    
)
    
"
ABSL_CLANG_CL_FLAGS
"
:
MSVC_BIG_WARNING_FLAGS
+
MSVC_DEFINES
    
"
ABSL_CLANG_CL_TEST_FLAGS
"
:
(
        
MSVC_BIG_WARNING_FLAGS
+
MSVC_DEFINES
+
ABSL_LLVM_TEST_ADDITIONAL_FLAGS
    
)
    
"
ABSL_MSVC_FLAGS
"
:
(
        
MSVC_BIG_WARNING_FLAGS
+
MSVC_WARNING_FLAGS
+
MSVC_DEFINES
    
)
    
"
ABSL_MSVC_TEST_FLAGS
"
:
(
        
MSVC_BIG_WARNING_FLAGS
        
+
MSVC_WARNING_FLAGS
        
+
MSVC_DEFINES
        
+
[
            
"
/
wd4018
"
            
"
/
wd4101
"
            
"
/
wd4244
"
            
"
/
wd4267
"
            
"
/
wd4503
"
            
"
/
wd4996
"
            
"
/
DNOMINMAX
"
        
]
    
)
    
"
ABSL_MSVC_LINKOPTS
"
:
[
        
"
-
ignore
:
4221
"
    
]
}
