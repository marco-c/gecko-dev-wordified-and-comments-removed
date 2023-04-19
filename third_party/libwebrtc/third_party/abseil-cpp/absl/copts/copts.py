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
MSVC_BIG_WARNING_FLAGS
=
[
    
"
/
W3
"
]
LLVM_TEST_DISABLE_WARNINGS_FLAGS
=
[
    
"
-
Wno
-
c99
-
extensions
"
    
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
noreturn
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
null
-
conversion
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
shift
-
sign
-
overflow
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
zero
-
as
-
null
-
pointer
-
constant
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
COPT_VARS
=
{
    
"
ABSL_GCC_FLAGS
"
:
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
    
"
ABSL_GCC_TEST_FLAGS
"
:
[
        
"
-
Wno
-
conversion
-
null
"
        
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
    
"
ABSL_LLVM_FLAGS
"
:
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
conversion
"
        
"
-
DNOMINMAX
"
    
]
    
"
ABSL_LLVM_TEST_FLAGS
"
:
        
LLVM_TEST_DISABLE_WARNINGS_FLAGS
    
"
ABSL_CLANG_CL_FLAGS
"
:
        
(
MSVC_BIG_WARNING_FLAGS
+
MSVC_DEFINES
)
    
"
ABSL_CLANG_CL_TEST_FLAGS
"
:
        
LLVM_TEST_DISABLE_WARNINGS_FLAGS
    
"
ABSL_MSVC_FLAGS
"
:
        
MSVC_BIG_WARNING_FLAGS
+
MSVC_DEFINES
+
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
wd4800
"
        
]
    
"
ABSL_MSVC_TEST_FLAGS
"
:
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
    
"
ABSL_RANDOM_HWAES_ARM64_FLAGS
"
:
[
"
-
march
=
armv8
-
a
+
crypto
"
]
    
"
ABSL_RANDOM_HWAES_ARM32_FLAGS
"
:
[
"
-
mfpu
=
neon
"
]
    
"
ABSL_RANDOM_HWAES_X64_FLAGS
"
:
[
        
"
-
maes
"
        
"
-
msse4
.
1
"
    
]
    
"
ABSL_RANDOM_HWAES_MSVC_X64_FLAGS
"
:
[
]
}
