"
"
"
Generator
for
C
style
prototypes
and
definitions
"
"
"
import
glob
import
os
import
sys
from
idl_log
import
ErrOut
InfoOut
WarnOut
from
idl_node
import
IDLNode
from
idl_ast
import
IDLAst
from
idl_option
import
GetOption
Option
ParseOptions
from
idl_parser
import
ParseFiles
Option
(
'
cgen_debug
'
'
Debug
generate
.
'
)
class
CGenError
(
Exception
)
:
  
def
__init__
(
self
msg
)
:
    
self
.
value
=
msg
  
def
__str__
(
self
)
:
    
return
repr
(
self
.
value
)
def
CommentLines
(
lines
tabs
=
0
)
:
  
tab
=
'
'
*
tabs
  
out
=
'
%
s
/
*
'
%
tab
+
(
'
\
n
%
s
*
'
%
tab
)
.
join
(
lines
)
  
if
not
lines
[
-
1
]
:
    
out
+
=
'
/
\
n
'
  
else
:
    
out
+
=
'
*
/
\
n
'
  
return
out
def
Comment
(
node
prefix
=
None
tabs
=
0
)
:
  
comment
=
node
.
GetName
(
)
  
lines
=
comment
.
split
(
'
\
n
'
)
  
if
prefix
:
    
prefix_lines
=
prefix
.
split
(
'
\
n
'
)
    
if
prefix_lines
[
0
]
=
=
'
*
'
and
lines
[
0
]
=
=
'
*
'
:
      
lines
=
prefix_lines
+
lines
[
1
:
]
    
else
:
      
lines
=
prefix_lines
+
lines
;
  
return
CommentLines
(
lines
tabs
)
def
GetNodeComments
(
node
tabs
=
0
)
:
  
comment_txt
=
'
'
  
for
doc
in
node
.
GetListOf
(
'
Comment
'
)
:
    
comment_txt
+
=
Comment
(
doc
tabs
=
tabs
)
  
return
comment_txt
class
CGen
(
object
)
:
  
TypeMap
=
{
    
'
Array
'
:
{
      
'
in
'
:
'
const
%
s
'
      
'
inout
'
:
'
%
s
'
      
'
out
'
:
'
%
s
*
'
      
'
store
'
:
'
%
s
'
      
'
return
'
:
'
%
s
'
      
'
ref
'
:
'
%
s
*
'
    
}
    
'
Callspec
'
:
{
      
'
in
'
:
'
%
s
'
      
'
inout
'
:
'
%
s
'
      
'
out
'
:
'
%
s
'
      
'
store
'
:
'
%
s
'
      
'
return
'
:
'
%
s
'
    
}
    
'
Enum
'
:
{
      
'
in
'
:
'
%
s
'
      
'
inout
'
:
'
%
s
*
'
      
'
out
'
:
'
%
s
*
'
      
'
store
'
:
'
%
s
'
      
'
return
'
:
'
%
s
'
    
}
    
'
Interface
'
:
{
      
'
in
'
:
'
const
%
s
*
'
      
'
inout
'
:
'
%
s
*
'
      
'
out
'
:
'
%
s
*
*
'
      
'
return
'
:
'
%
s
*
'
      
'
store
'
:
'
%
s
*
'
    
}
    
'
Struct
'
:
{
      
'
in
'
:
'
const
%
s
*
'
      
'
inout
'
:
'
%
s
*
'
      
'
out
'
:
'
%
s
*
'
      
'
return
'
:
'
%
s
*
'
      
'
store
'
:
'
%
s
'
      
'
ref
'
:
'
%
s
*
'
    
}
    
'
blob_t
'
:
{
      
'
in
'
:
'
const
%
s
'
      
'
inout
'
:
'
%
s
'
      
'
out
'
:
'
%
s
'
      
'
return
'
:
'
%
s
'
      
'
store
'
:
'
%
s
'
    
}
    
'
mem_t
'
:
{
      
'
in
'
:
'
const
%
s
'
      
'
inout
'
:
'
%
s
'
      
'
out
'
:
'
%
s
'
      
'
return
'
:
'
%
s
'
      
'
store
'
:
'
%
s
'
    
}
    
'
mem_ptr_t
'
:
{
      
'
in
'
:
'
const
%
s
'
      
'
inout
'
:
'
%
s
'
      
'
out
'
:
'
%
s
'
      
'
return
'
:
'
%
s
'
      
'
store
'
:
'
%
s
'
    
}
    
'
str_t
'
:
{
      
'
in
'
:
'
const
%
s
'
      
'
inout
'
:
'
%
s
'
      
'
out
'
:
'
%
s
'
      
'
return
'
:
'
const
%
s
'
      
'
store
'
:
'
%
s
'
    
}
    
'
cstr_t
'
:
{
      
'
in
'
:
'
%
s
'
      
'
inout
'
:
'
%
s
*
'
      
'
out
'
:
'
%
s
*
'
      
'
return
'
:
'
%
s
'
      
'
store
'
:
'
%
s
'
    
}
    
'
TypeValue
'
:
{
      
'
in
'
:
'
%
s
'
      
'
constptr_in
'
:
'
const
%
s
*
'
      
'
inout
'
:
'
%
s
*
'
      
'
out
'
:
'
%
s
*
'
      
'
return
'
:
'
%
s
'
      
'
store
'
:
'
%
s
'
    
}
  
}
  
RemapName
=
{
  
'
blob_t
'
:
'
void
*
*
'
  
'
float_t
'
:
'
float
'
  
'
double_t
'
:
'
double
'
  
'
handle_t
'
:
'
int
'
  
'
mem_t
'
:
'
void
*
'
  
'
mem_ptr_t
'
:
'
void
*
*
'
  
'
str_t
'
:
'
char
*
'
  
'
cstr_t
'
:
'
const
char
*
'
  
'
interface_t
'
:
'
const
void
*
'
  
}
  
for
gltype
in
[
'
GLbitfield
'
'
GLboolean
'
'
GLbyte
'
'
GLclampf
'
                 
'
GLclampx
'
'
GLenum
'
'
GLfixed
'
'
GLfloat
'
'
GLint
'
                 
'
GLintptr
'
'
GLshort
'
'
GLsizei
'
'
GLsizeiptr
'
                 
'
GLubyte
'
'
GLuint
'
'
GLushort
'
]
:
    
ptrtype
=
gltype
+
'
_ptr_t
'
    
TypeMap
[
ptrtype
]
=
{
      
'
in
'
:
'
const
%
s
'
      
'
inout
'
:
'
%
s
'
      
'
out
'
:
'
%
s
'
      
'
return
'
:
'
const
%
s
'
      
'
store
'
:
'
%
s
'
    
}
    
RemapName
[
ptrtype
]
=
'
%
s
*
'
%
gltype
  
def
__init__
(
self
)
:
    
self
.
dbg_depth
=
0
  
def
Log
(
self
txt
)
:
    
if
not
GetOption
(
'
cgen_debug
'
)
:
return
    
tabs
=
'
'
*
self
.
dbg_depth
    
print
'
%
s
%
s
'
%
(
tabs
txt
)
  
def
LogEnter
(
self
txt
)
:
    
if
txt
:
self
.
Log
(
txt
)
    
self
.
dbg_depth
+
=
1
  
def
LogExit
(
self
txt
)
:
    
self
.
dbg_depth
-
=
1
    
if
txt
:
self
.
Log
(
txt
)
  
def
GetDefine
(
self
name
value
)
:
    
out
=
'
#
define
%
s
%
s
'
%
(
name
value
)
    
if
len
(
out
)
>
80
:
      
out
=
'
#
define
%
s
\
\
\
n
%
s
'
%
(
name
value
)
    
return
'
%
s
\
n
'
%
out
  
def
GetMacroHelper
(
self
node
)
:
    
macro
=
node
.
GetProperty
(
'
macro
'
)
    
if
macro
:
return
macro
    
name
=
node
.
GetName
(
)
    
name
=
name
.
upper
(
)
    
return
"
%
s_INTERFACE
"
%
name
  
def
GetInterfaceMacro
(
self
node
version
=
None
)
:
    
name
=
self
.
GetMacroHelper
(
node
)
    
if
version
is
None
:
      
return
name
    
return
'
%
s_
%
s
'
%
(
name
str
(
version
)
.
replace
(
'
.
'
'
_
'
)
)
  
def
GetInterfaceString
(
self
node
version
=
None
)
:
    
name
=
node
.
GetProperty
(
'
iname
'
)
    
if
not
name
:
      
name
=
node
.
GetName
(
)
      
if
name
.
endswith
(
'
_Dev
'
)
:
        
name
=
'
%
s
(
Dev
)
'
%
name
[
:
-
4
]
    
if
version
is
None
:
      
return
name
    
return
"
%
s
;
%
s
"
%
(
name
version
)
  
def
GetArraySpec
(
self
node
)
:
    
assert
(
node
.
cls
=
=
'
Array
'
)
    
fixed
=
node
.
GetProperty
(
'
FIXED
'
)
    
if
fixed
:
      
return
'
[
%
s
]
'
%
fixed
    
else
:
      
return
'
[
]
'
  
def
GetTypeName
(
self
node
release
prefix
=
'
'
)
:
    
self
.
LogEnter
(
'
GetTypeName
of
%
s
rel
=
%
s
'
%
(
node
release
)
)
    
if
node
.
IsA
(
'
Member
'
'
Param
'
'
Typedef
'
)
:
      
typeref
=
node
.
GetType
(
release
)
    
else
:
      
typeref
=
node
    
if
typeref
is
None
:
      
node
.
Error
(
'
No
type
at
release
%
s
.
'
%
release
)
      
raise
CGenError
(
'
No
type
for
%
s
'
%
node
)
    
if
typeref
.
IsA
(
'
Type
'
)
:
      
name
=
CGen
.
RemapName
.
get
(
typeref
.
GetName
(
)
None
)
      
if
name
is
None
:
name
=
typeref
.
GetName
(
)
      
name
=
'
%
s
%
s
'
%
(
prefix
name
)
    
elif
typeref
.
IsA
(
'
Interface
'
)
:
      
rel
=
typeref
.
first_release
[
release
]
      
name
=
'
struct
%
s
%
s
'
%
(
prefix
self
.
GetStructName
(
typeref
rel
True
)
)
    
elif
typeref
.
IsA
(
'
Struct
'
)
:
      
if
typeref
.
GetProperty
(
'
union
'
)
:
        
name
=
'
union
%
s
%
s
'
%
(
prefix
typeref
.
GetName
(
)
)
      
else
:
        
name
=
'
struct
%
s
%
s
'
%
(
prefix
typeref
.
GetName
(
)
)
    
elif
typeref
.
IsA
(
'
Enum
'
'
Typedef
'
)
:
      
if
not
typeref
.
LastRelease
(
release
)
:
        
first
=
node
.
first_release
[
release
]
        
ver
=
'
_
'
+
node
.
GetVersion
(
first
)
.
replace
(
'
.
'
'
_
'
)
      
else
:
        
ver
=
'
'
      
if
typeref
.
GetProperty
(
'
notypedef
'
)
:
        
name
=
'
enum
%
s
%
s
%
s
'
%
(
prefix
typeref
.
GetName
(
)
ver
)
      
else
:
        
name
=
'
%
s
%
s
%
s
'
%
(
prefix
typeref
.
GetName
(
)
ver
)
    
else
:
      
raise
RuntimeError
(
'
Getting
name
of
non
-
type
%
s
.
'
%
node
)
    
self
.
LogExit
(
'
GetTypeName
%
s
is
%
s
'
%
(
node
name
)
)
    
return
name
  
def
GetRootTypeMode
(
self
node
release
mode
)
:
    
self
.
LogEnter
(
'
GetRootType
of
%
s
'
%
node
)
    
if
node
.
GetOneOf
(
'
Array
'
)
:
      
rootType
=
'
Array
'
    
elif
node
.
GetOneOf
(
'
Callspec
'
)
:
      
rootType
mode
=
self
.
GetRootTypeMode
(
node
.
GetType
(
release
)
release
                                            
'
return
'
)
    
elif
node
.
IsA
(
'
Member
'
'
Param
'
'
Typedef
'
)
:
      
rootType
mode
=
self
.
GetRootTypeMode
(
node
.
GetType
(
release
)
                                            
release
mode
)
    
elif
node
.
IsA
(
'
Enum
'
)
:
      
rootType
=
node
.
cls
    
elif
node
.
IsA
(
'
Interface
'
'
Struct
'
)
:
      
if
mode
=
=
'
return
'
:
        
if
node
.
GetProperty
(
'
returnByValue
'
)
:
          
rootType
=
'
TypeValue
'
        
else
:
          
rootType
=
node
.
cls
      
else
:
        
if
node
.
GetProperty
(
'
passByValue
'
)
:
          
rootType
=
'
TypeValue
'
        
else
:
          
rootType
=
node
.
cls
    
elif
node
.
IsA
(
'
Type
'
)
:
      
if
node
.
GetName
(
)
in
CGen
.
TypeMap
:
        
rootType
=
node
.
GetName
(
)
      
else
:
        
rootType
=
'
TypeValue
'
    
else
:
      
raise
RuntimeError
(
'
Getting
root
type
of
non
-
type
%
s
.
'
%
node
)
    
self
.
LogExit
(
'
RootType
is
"
%
s
"
'
%
rootType
)
    
return
rootType
mode
  
def
GetTypeByMode
(
self
node
release
mode
)
:
    
self
.
LogEnter
(
'
GetTypeByMode
of
%
s
mode
=
%
s
release
=
%
s
'
%
                  
(
node
mode
release
)
)
    
name
=
self
.
GetTypeName
(
node
release
)
    
ntype
mode
=
self
.
GetRootTypeMode
(
node
release
mode
)
    
out
=
CGen
.
TypeMap
[
ntype
]
[
mode
]
%
name
    
self
.
LogExit
(
'
GetTypeByMode
%
s
=
%
s
'
%
(
node
out
)
)
    
return
out
  
def
GetParamMode
(
self
node
)
:
    
self
.
Log
(
'
GetParamMode
for
%
s
'
%
node
)
    
if
node
.
GetProperty
(
'
in
'
)
:
return
'
in
'
    
if
node
.
GetProperty
(
'
out
'
)
:
return
'
out
'
    
if
node
.
GetProperty
(
'
inout
'
)
:
return
'
inout
'
    
if
node
.
GetProperty
(
'
constptr_in
'
)
:
return
'
constptr_in
'
    
return
'
return
'
  
def
GetComponents
(
self
node
release
mode
)
:
    
self
.
LogEnter
(
'
GetComponents
mode
%
s
for
%
s
%
s
'
%
(
mode
node
release
)
)
    
rtype
=
self
.
GetTypeByMode
(
node
release
mode
)
    
arrayspec
=
[
self
.
GetArraySpec
(
array
)
for
array
in
node
.
GetListOf
(
'
Array
'
)
]
    
if
mode
=
=
'
out
'
and
len
(
arrayspec
)
=
=
1
and
arrayspec
[
0
]
=
=
'
[
]
'
:
      
rtype
+
=
'
*
'
      
del
arrayspec
[
0
]
    
if
node
.
IsA
(
'
Enum
'
'
Interface
'
'
Struct
'
)
:
      
rname
=
node
.
GetName
(
)
    
else
:
      
rname
=
node
.
GetType
(
release
)
.
GetName
(
)
    
if
rname
in
CGen
.
RemapName
:
      
rname
=
CGen
.
RemapName
[
rname
]
    
if
'
%
'
in
rtype
:
      
rtype
=
rtype
%
rname
    
name
=
node
.
GetName
(
)
    
callnode
=
node
.
GetOneOf
(
'
Callspec
'
)
    
if
callnode
:
      
callspec
=
[
]
      
for
param
in
callnode
.
GetListOf
(
'
Param
'
)
:
        
if
not
param
.
IsRelease
(
release
)
:
          
continue
        
mode
=
self
.
GetParamMode
(
param
)
        
ptype
pname
parray
pspec
=
self
.
GetComponents
(
param
release
mode
)
        
if
node
.
GetName
(
)
=
=
'
GetDirContents
'
and
pname
=
=
'
contents
'
:
          
ptype
+
=
'
*
'
        
callspec
.
append
(
(
ptype
pname
parray
pspec
)
)
    
else
:
      
callspec
=
None
    
self
.
LogExit
(
'
GetComponents
:
%
s
%
s
%
s
%
s
'
%
                 
(
rtype
name
arrayspec
callspec
)
)
    
return
(
rtype
name
arrayspec
callspec
)
  
def
Compose
(
self
rtype
name
arrayspec
callspec
prefix
func_as_ptr
              
include_name
unsized_as_ptr
)
:
    
self
.
LogEnter
(
'
Compose
:
%
s
%
s
'
%
(
rtype
name
)
)
    
arrayspec
=
'
'
.
join
(
arrayspec
)
    
if
unsized_as_ptr
and
arrayspec
[
-
2
:
]
=
=
'
[
]
'
:
      
prefix
+
=
'
*
'
      
arrayspec
=
arrayspec
[
:
-
2
]
    
if
not
include_name
:
      
name
=
prefix
+
arrayspec
    
else
:
      
name
=
prefix
+
name
+
arrayspec
    
if
callspec
is
None
:
      
out
=
'
%
s
%
s
'
%
(
rtype
name
)
    
else
:
      
params
=
[
]
      
for
ptype
pname
parray
pspec
in
callspec
:
        
params
.
append
(
self
.
Compose
(
ptype
pname
parray
pspec
'
'
True
                                   
include_name
=
True
                                   
unsized_as_ptr
=
unsized_as_ptr
)
)
      
if
func_as_ptr
:
        
name
=
'
(
*
%
s
)
'
%
name
      
if
not
params
:
        
params
=
[
'
void
'
]
      
out
=
'
%
s
%
s
(
%
s
)
'
%
(
rtype
name
'
'
.
join
(
params
)
)
    
self
.
LogExit
(
'
Exit
Compose
:
%
s
'
%
out
)
    
return
out
  
def
GetSignature
(
self
node
release
mode
prefix
=
'
'
func_as_ptr
=
True
                   
include_name
=
True
include_version
=
False
)
:
    
self
.
LogEnter
(
'
GetSignature
%
s
%
s
as
func
=
%
s
'
%
                  
(
node
mode
func_as_ptr
)
)
    
rtype
name
arrayspec
callspec
=
self
.
GetComponents
(
node
release
mode
)
    
if
include_version
:
      
name
=
self
.
GetStructName
(
node
release
True
)
    
unsized_as_ptr
=
not
callspec
    
out
=
self
.
Compose
(
rtype
name
arrayspec
callspec
prefix
                       
func_as_ptr
include_name
unsized_as_ptr
)
    
self
.
LogExit
(
'
Exit
GetSignature
:
%
s
'
%
out
)
    
return
out
  
def
DefineTypedef
(
self
node
releases
prefix
=
'
'
comment
=
False
)
:
    
__pychecker__
=
'
unusednames
=
comment
'
    
build_list
=
node
.
GetUniqueReleases
(
releases
)
    
out
=
'
typedef
%
s
;
\
n
'
%
self
.
GetSignature
(
node
build_list
[
-
1
]
'
return
'
                                              
prefix
True
                                              
include_version
=
False
)
    
for
index
rel
in
enumerate
(
build_list
[
:
-
1
]
)
:
      
out
+
=
'
\
n
'
      
out
+
=
'
typedef
%
s
;
\
n
'
%
self
.
GetSignature
(
node
rel
'
return
'
                                                 
prefix
True
                                                 
include_version
=
True
)
    
self
.
Log
(
'
DefineTypedef
:
%
s
'
%
out
)
    
return
out
  
def
DefineEnum
(
self
node
releases
prefix
=
'
'
comment
=
False
)
:
    
__pychecker__
=
'
unusednames
=
comment
releases
'
    
self
.
LogEnter
(
'
DefineEnum
%
s
'
%
node
)
    
name
=
'
%
s
%
s
'
%
(
prefix
node
.
GetName
(
)
)
    
notypedef
=
node
.
GetProperty
(
'
notypedef
'
)
    
unnamed
=
node
.
GetProperty
(
'
unnamed
'
)
    
if
unnamed
:
      
out
=
'
enum
{
'
    
elif
notypedef
:
      
out
=
'
enum
%
s
{
'
%
name
    
else
:
      
out
=
'
typedef
enum
{
'
    
enumlist
=
[
]
    
for
child
in
node
.
GetListOf
(
'
EnumItem
'
)
:
      
value
=
child
.
GetProperty
(
'
VALUE
'
)
      
comment_txt
=
GetNodeComments
(
child
tabs
=
1
)
      
if
value
:
        
item_txt
=
'
%
s
%
s
=
%
s
'
%
(
prefix
child
.
GetName
(
)
value
)
      
else
:
        
item_txt
=
'
%
s
%
s
'
%
(
prefix
child
.
GetName
(
)
)
      
enumlist
.
append
(
'
%
s
%
s
'
%
(
comment_txt
item_txt
)
)
    
self
.
LogExit
(
'
Exit
DefineEnum
'
)
    
if
unnamed
or
notypedef
:
      
out
=
'
%
s
\
n
%
s
\
n
}
;
\
n
'
%
(
out
'
\
n
'
.
join
(
enumlist
)
)
    
else
:
      
out
=
'
%
s
\
n
%
s
\
n
}
%
s
;
\
n
'
%
(
out
'
\
n
'
.
join
(
enumlist
)
name
)
    
return
out
  
def
DefineMember
(
self
node
releases
prefix
=
'
'
comment
=
False
)
:
    
__pychecker__
=
'
unusednames
=
prefix
comment
'
    
release
=
releases
[
0
]
    
self
.
LogEnter
(
'
DefineMember
%
s
'
%
node
)
    
if
node
.
GetProperty
(
'
ref
'
)
:
      
out
=
'
%
s
;
'
%
self
.
GetSignature
(
node
release
'
ref
'
'
'
True
)
    
else
:
      
out
=
'
%
s
;
'
%
self
.
GetSignature
(
node
release
'
store
'
'
'
True
)
    
self
.
LogExit
(
'
Exit
DefineMember
'
)
    
return
out
  
def
GetStructName
(
self
node
release
include_version
=
False
)
:
    
suffix
=
'
'
    
if
include_version
:
      
ver_num
=
node
.
GetVersion
(
release
)
      
suffix
=
(
'
_
%
s
'
%
ver_num
)
.
replace
(
'
.
'
'
_
'
)
    
return
node
.
GetName
(
)
+
suffix
  
def
DefineStructInternals
(
self
node
release
                            
include_version
=
False
comment
=
True
)
:
    
channel
=
node
.
GetProperty
(
'
FILE
'
)
.
release_map
.
GetChannel
(
release
)
    
if
channel
=
=
'
dev
'
:
      
channel_comment
=
'
/
*
dev
*
/
'
    
else
:
      
channel_comment
=
'
'
    
out
=
'
'
    
if
node
.
GetProperty
(
'
union
'
)
:
      
out
+
=
'
union
%
s
{
%
s
\
n
'
%
(
          
self
.
GetStructName
(
node
release
include_version
)
channel_comment
)
    
else
:
      
out
+
=
'
struct
%
s
{
%
s
\
n
'
%
(
          
self
.
GetStructName
(
node
release
include_version
)
channel_comment
)
    
channel
=
node
.
GetProperty
(
'
FILE
'
)
.
release_map
.
GetChannel
(
release
)
    
members
=
[
]
    
for
child
in
node
.
GetListOf
(
'
Member
'
)
:
      
if
channel
=
=
'
stable
'
and
child
.
NodeIsDevOnly
(
)
:
        
continue
      
member
=
self
.
Define
(
child
[
release
]
tabs
=
1
comment
=
comment
)
      
if
not
member
:
        
continue
      
members
.
append
(
member
)
    
out
+
=
'
%
s
\
n
}
;
\
n
'
%
'
\
n
'
.
join
(
members
)
    
return
out
  
def
DefineUnversionedInterface
(
self
node
rel
)
:
    
out
=
'
\
n
'
    
if
node
.
GetProperty
(
'
force_struct_namespace
'
)
:
      
out
+
=
self
.
DefineStructInternals
(
node
rel
                                        
include_version
=
False
comment
=
True
)
    
else
:
      
out
+
=
'
typedef
struct
%
s
%
s
;
\
n
'
%
(
        
self
.
GetStructName
(
node
rel
include_version
=
True
)
        
self
.
GetStructName
(
node
rel
include_version
=
False
)
)
    
return
out
  
def
DefineStruct
(
self
node
releases
prefix
=
'
'
comment
=
False
)
:
    
__pychecker__
=
'
unusednames
=
comment
prefix
'
    
self
.
LogEnter
(
'
DefineStruct
%
s
'
%
node
)
    
out
=
'
'
    
build_list
=
node
.
GetUniqueReleases
(
releases
)
    
newest_stable
=
None
    
newest_dev
=
None
    
for
rel
in
build_list
:
      
channel
=
node
.
GetProperty
(
'
FILE
'
)
.
release_map
.
GetChannel
(
rel
)
      
if
channel
=
=
'
stable
'
:
        
newest_stable
=
rel
      
if
channel
=
=
'
dev
'
:
        
newest_dev
=
rel
    
last_rel
=
build_list
[
-
1
]
    
if
node
.
IsA
(
'
Struct
'
)
:
      
if
len
(
build_list
)
!
=
1
:
        
node
.
Error
(
'
Can
not
support
multiple
versions
of
node
.
'
)
      
assert
len
(
build_list
)
=
=
1
      
out
=
self
.
DefineStructInternals
(
node
last_rel
                                       
include_version
=
False
comment
=
True
)
    
if
node
.
IsA
(
'
Interface
'
)
:
      
out
=
self
.
DefineStructInternals
(
node
last_rel
                                       
include_version
=
True
comment
=
True
)
      
if
last_rel
=
=
newest_stable
:
        
out
+
=
self
.
DefineUnversionedInterface
(
node
last_rel
)
      
for
rel
in
build_list
[
0
:
-
1
]
:
        
channel
=
node
.
GetProperty
(
'
FILE
'
)
.
release_map
.
GetChannel
(
rel
)
        
if
channel
=
=
'
dev
'
and
rel
!
=
newest_dev
:
          
if
not
node
.
DevInterfaceMatchesStable
(
rel
)
:
            
continue
        
out
+
=
'
\
n
'
+
self
.
DefineStructInternals
(
node
rel
                                                 
include_version
=
True
                                                 
comment
=
False
)
        
if
rel
=
=
newest_stable
:
          
out
+
=
self
.
DefineUnversionedInterface
(
node
rel
)
    
self
.
LogExit
(
'
Exit
DefineStruct
'
)
    
return
out
  
def
Copyright
(
self
node
cpp_style
=
False
)
:
    
lines
=
node
.
GetName
(
)
.
split
(
'
\
n
'
)
    
if
cpp_style
:
      
return
'
/
/
'
+
'
\
n
/
/
'
.
join
(
filter
(
lambda
f
:
f
!
=
'
'
lines
)
)
+
'
\
n
'
    
return
CommentLines
(
lines
)
  
def
Indent
(
self
data
tabs
=
0
)
:
    
"
"
"
Handles
indentation
and
80
-
column
line
wrapping
.
"
"
"
    
tab
=
'
'
*
tabs
    
lines
=
[
]
    
for
line
in
data
.
split
(
'
\
n
'
)
:
      
line
=
tab
+
line
      
space_break
=
line
.
rfind
(
'
'
0
80
)
      
if
len
(
line
)
<
=
80
or
'
http
:
/
/
'
in
line
:
        
lines
.
append
(
line
.
rstrip
(
)
)
      
elif
not
'
(
'
in
line
and
space_break
>
=
0
:
        
lines
.
append
(
line
[
0
:
space_break
]
)
        
lines
.
append
(
'
'
+
line
[
space_break
+
1
:
]
)
      
else
:
        
left
=
line
.
rfind
(
'
(
'
)
+
1
        
args
=
line
[
left
:
]
.
split
(
'
'
)
        
orig_args
=
args
        
orig_left
=
left
        
while
args
[
0
]
[
0
]
=
=
'
)
'
:
          
left
=
line
.
rfind
(
'
(
'
0
left
-
1
)
+
1
          
if
left
=
=
0
:
            
args
=
orig_args
            
left
=
orig_left
            
break
          
args
=
line
[
left
:
]
.
split
(
'
'
)
        
line_max
=
0
        
for
arg
in
args
:
          
if
len
(
arg
)
>
line_max
:
line_max
=
len
(
arg
)
        
if
left
+
line_max
>
=
80
:
          
indent
=
'
%
s
'
%
tab
          
args
=
(
'
\
n
%
s
'
%
indent
)
.
join
(
[
arg
.
strip
(
)
for
arg
in
args
]
)
          
lines
.
append
(
'
%
s
\
n
%
s
%
s
'
%
(
line
[
:
left
]
indent
args
)
)
        
else
:
          
indent
=
'
'
*
(
left
-
1
)
          
args
=
(
'
\
n
%
s
'
%
indent
)
.
join
(
args
)
          
lines
.
append
(
'
%
s
%
s
'
%
(
line
[
:
left
]
args
)
)
    
return
'
\
n
'
.
join
(
lines
)
  
def
Define
(
self
node
releases
tabs
=
0
prefix
=
'
'
comment
=
False
)
:
    
unique
=
node
.
GetUniqueReleases
(
releases
)
    
if
not
unique
or
not
node
.
InReleases
(
releases
)
:
      
return
'
'
    
self
.
LogEnter
(
'
Define
%
s
tab
=
%
d
prefix
=
"
%
s
"
'
%
(
node
tabs
prefix
)
)
    
declmap
=
dict
(
{
      
'
Enum
'
:
CGen
.
DefineEnum
      
'
Function
'
:
CGen
.
DefineMember
      
'
Interface
'
:
CGen
.
DefineStruct
      
'
Member
'
:
CGen
.
DefineMember
      
'
Struct
'
:
CGen
.
DefineStruct
      
'
Typedef
'
:
CGen
.
DefineTypedef
    
}
)
    
out
=
'
'
    
func
=
declmap
.
get
(
node
.
cls
None
)
    
if
not
func
:
      
ErrOut
.
Log
(
'
Failed
to
define
%
s
named
%
s
'
%
(
node
.
cls
node
.
GetName
(
)
)
)
    
define_txt
=
func
(
self
node
releases
prefix
=
prefix
comment
=
comment
)
    
comment_txt
=
GetNodeComments
(
node
tabs
=
0
)
    
if
comment_txt
and
comment
:
      
out
+
=
comment_txt
    
out
+
=
define_txt
    
indented_out
=
self
.
Indent
(
out
tabs
)
    
self
.
LogExit
(
'
Exit
Define
'
)
    
return
indented_out
def
CleanString
(
instr
)
:
  
instr
=
instr
.
strip
(
)
  
instr
=
instr
.
split
(
)
  
return
'
'
.
join
(
instr
)
def
TestFile
(
filenode
)
:
  
cgen
=
CGen
(
)
  
errors
=
0
  
for
node
in
filenode
.
GetChildren
(
)
[
2
:
]
:
    
instr
=
node
.
GetOneOf
(
'
Comment
'
)
    
if
not
instr
:
continue
    
instr
.
Dump
(
)
    
instr
=
CleanString
(
instr
.
GetName
(
)
)
    
outstr
=
cgen
.
Define
(
node
releases
=
[
'
M14
'
]
)
    
if
GetOption
(
'
verbose
'
)
:
      
print
outstr
+
'
\
n
'
    
outstr
=
CleanString
(
outstr
)
    
if
instr
!
=
outstr
:
      
ErrOut
.
Log
(
'
Failed
match
of
\
n
>
>
%
s
<
<
\
nto
:
\
n
>
>
%
s
<
<
\
nFor
:
\
n
'
%
                 
(
instr
outstr
)
)
      
node
.
Dump
(
1
comments
=
True
)
      
errors
+
=
1
  
return
errors
def
TestFiles
(
filenames
)
:
  
if
not
filenames
:
    
idldir
=
os
.
path
.
split
(
sys
.
argv
[
0
]
)
[
0
]
    
idldir
=
os
.
path
.
join
(
idldir
'
test_cgen
'
'
*
.
idl
'
)
    
filenames
=
glob
.
glob
(
idldir
)
  
filenames
=
sorted
(
filenames
)
  
ast
=
ParseFiles
(
filenames
)
  
total_errs
=
0
  
for
filenode
in
ast
.
GetListOf
(
'
File
'
)
:
    
errs
=
TestFile
(
filenode
)
    
if
errs
:
      
ErrOut
.
Log
(
'
%
s
test
failed
with
%
d
error
(
s
)
.
'
%
                 
(
filenode
.
GetName
(
)
errs
)
)
      
total_errs
+
=
errs
  
if
total_errs
:
    
ErrOut
.
Log
(
'
Failed
generator
test
.
'
)
  
else
:
    
InfoOut
.
Log
(
'
Passed
generator
test
.
'
)
  
return
total_errs
def
main
(
args
)
:
  
filenames
=
ParseOptions
(
args
)
  
if
GetOption
(
'
test
'
)
:
    
return
TestFiles
(
filenames
)
  
ast
=
ParseFiles
(
filenames
)
  
cgen
=
CGen
(
)
  
for
f
in
ast
.
GetListOf
(
'
File
'
)
:
    
if
f
.
GetProperty
(
'
ERRORS
'
)
>
0
:
      
print
'
Skipping
%
s
'
%
f
.
GetName
(
)
      
continue
    
for
node
in
f
.
GetChildren
(
)
[
2
:
]
:
      
print
cgen
.
Define
(
node
ast
.
releases
comment
=
True
prefix
=
'
tst_
'
)
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
sys
.
argv
[
1
:
]
)
)
