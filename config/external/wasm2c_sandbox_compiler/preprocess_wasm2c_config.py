import
itertools
known_vars
=
[
    
"
#
cmakedefine
CMAKE_PROJECT_VERSION
"
    
"
#
cmakedefine01
HAVE_ALLOCA_H
"
    
"
#
cmakedefine01
HAVE_UNISTD_H
"
    
"
#
cmakedefine01
HAVE_SNPRINTF
"
    
"
#
cmakedefine01
HAVE_SSIZE_T
"
    
"
#
cmakedefine01
HAVE_STRCASECMP
"
    
"
#
cmakedefine01
HAVE_WIN32_VT100
"
    
"
#
cmakedefine01
COMPILER_IS_CLANG
"
    
"
#
cmakedefine01
COMPILER_IS_GNU
"
    
"
#
cmakedefine01
COMPILER_IS_MSVC
"
    
"
#
cmakedefine01
WITH_EXCEPTIONS
"
    
"
#
define
SIZEOF_SIZE_T
SIZEOF_SIZE_T
"
]
replaced_variables
=
"
"
"
#
include
"
mozilla
-
config
.
h
"
#
define
CMAKE_PROJECT_VERSION
"
Firefox
-
in
-
tree
-
version
"
/
/
mozilla
-
config
.
h
defines
the
following
which
is
used
/
/
-
HAVE_ALLOCA_H
/
/
-
HAVE_UNISTD_H
#
ifdef
_WIN32
  
/
/
Ignore
whatever
is
set
in
mozilla
-
config
.
h
wrt
alloca
because
it
is
  
/
/
wrong
when
cross
-
compiling
on
Windows
.
  
#
undef
HAVE_ALLOCA_H
  
/
*
Whether
ssize_t
is
defined
by
stddef
.
h
*
/
  
#
define
HAVE_SSIZE_T
0
  
/
*
Whether
strcasecmp
is
defined
by
strings
.
h
*
/
  
#
define
HAVE_STRCASECMP
0
  
/
*
Whether
ENABLE_VIRTUAL_TERMINAL_PROCESSING
is
defined
by
windows
.
h
*
/
  
#
define
HAVE_WIN32_VT100
1
#
else
  
#
define
HAVE_SSIZE_T
1
  
#
define
HAVE_STRCASECMP
1
  
#
define
HAVE_WIN32_VT100
0
#
endif
/
*
Whether
snprintf
is
defined
by
stdio
.
h
*
/
#
define
HAVE_SNPRINTF
1
#
if
defined
(
_MSC_VER
)
  
#
define
COMPILER_IS_GNU
0
  
#
define
COMPILER_IS_CLANG
0
  
#
define
COMPILER_IS_MSVC
1
#
elif
defined
(
__GNUC__
)
  
#
if
defined
(
__clang__
)
    
#
define
COMPILER_IS_GNU
0
    
#
define
COMPILER_IS_CLANG
1
    
#
define
COMPILER_IS_MSVC
0
  
#
else
    
#
define
COMPILER_IS_GNU
1
    
#
define
COMPILER_IS_CLANG
0
    
#
define
COMPILER_IS_MSVC
0
  
#
endif
#
else
  
#
error
"
Unknown
compiler
"
#
endif
#
define
WITH_EXCEPTIONS
0
#
if
SIZE_MAX
=
=
0xffffffffffffffff
  
#
define
SIZEOF_SIZE_T
8
#
elif
SIZE_MAX
=
=
0xffffffff
  
#
define
SIZEOF_SIZE_T
4
#
else
  
#
error
"
Unknown
size
of
size_t
"
#
endif
"
"
"
def
generate_config
(
output
config_h_in
)
:
    
file_config_h_in
=
open
(
config_h_in
"
r
"
)
    
lines
=
file_config_h_in
.
readlines
(
)
    
for
known_var
in
known_vars
:
        
lines
=
[
x
for
x
in
lines
if
not
x
.
startswith
(
known_var
)
]
    
remaining_vars
=
[
x
for
x
in
lines
if
x
.
startswith
(
"
#
cmakedefine
"
)
or
"
"
in
x
]
    
if
len
(
remaining_vars
)
>
0
:
        
raise
BaseException
(
"
Unknown
cmake
variables
:
"
+
str
(
remaining_vars
)
)
    
pos
=
lines
.
index
(
"
#
define
WABT_CONFIG_H_
\
n
"
)
    
skipped
=
itertools
.
takewhile
(
        
lambda
x
:
not
(
x
.
strip
(
)
)
or
x
.
startswith
(
"
#
include
"
)
lines
[
pos
+
1
:
]
    
)
    
pos
+
=
len
(
list
(
skipped
)
)
    
pre_include_lines
=
lines
[
0
:
pos
]
    
post_include_lines
=
lines
[
pos
:
]
    
output_str
=
(
        
"
"
.
join
(
pre_include_lines
)
        
+
"
\
n
"
        
+
replaced_variables
        
+
"
\
n
"
        
+
"
"
.
join
(
post_include_lines
)
    
)
    
output
.
write
(
output_str
)
