import
os
import
re
import
shutil
import
sys
import
tempfile
from
xml
.
etree
import
ElementTree
from
collections
import
namedtuple
from
typing
import
Dict
from
devil
.
utils
import
cmd_helper
from
pylib
import
constants
sys
.
path
.
append
(
os
.
path
.
join
(
os
.
path
.
dirname
(
__file__
)
'
.
.
'
'
.
.
'
'
gyp
'
)
)
from
util
import
build_utils
DEXDUMP_PATH
=
os
.
path
.
join
(
constants
.
ANDROID_SDK_TOOLS
'
dexdump
'
)
Annotations
=
namedtuple
(
'
Annotations
'
                         
[
'
classAnnotations
'
'
methodsAnnotations
'
]
)
def
Dump
(
apk_path
)
:
  
"
"
"
Dumps
class
and
method
information
from
a
APK
into
a
dict
via
dexdump
.
  
Args
:
    
apk_path
:
An
absolute
path
to
an
APK
file
to
dump
.
  
Returns
:
    
A
dict
in
the
following
format
:
      
{
        
<
package_name
>
:
{
          
'
classes
'
:
{
            
<
class_name
>
:
{
              
'
methods
'
:
[
<
method_1
>
<
method_2
>
]
              
'
superclass
'
:
<
string
>
              
'
is_abstract
'
:
<
boolean
>
              
'
annotations
'
:
<
Annotations
>
            
}
          
}
        
}
      
}
  
"
"
"
  
try
:
    
dexfile_dir
=
tempfile
.
mkdtemp
(
)
    
parsed_dex_files
=
[
]
    
for
dex_file
in
build_utils
.
ExtractAll
(
apk_path
                                           
dexfile_dir
                                           
pattern
=
'
*
classes
*
.
dex
'
)
:
      
output_xml
=
cmd_helper
.
GetCmdOutput
(
          
[
DEXDUMP_PATH
'
-
a
'
'
-
j
'
'
-
l
'
'
xml
'
dex_file
]
)
      
BAD_XML_CHARS
=
re
.
compile
(
          
u
'
[
\
x00
-
\
x08
\
x0b
-
\
x0c
\
x0e
-
\
x1f
\
x7f
-
\
x84
\
x86
-
\
x9f
'
+
          
u
'
\
ud800
-
\
udfff
\
ufdd0
-
\
ufddf
\
ufffe
-
\
uffff
]
'
)
      
clean_xml
=
BAD_XML_CHARS
.
sub
(
u
'
\
ufffd
'
output_xml
)
      
clean_xml
=
clean_xml
.
replace
(
'
<
init
>
'
'
constructor
'
)
      
annotations
=
_ParseAnnotations
(
clean_xml
)
      
parsed_dex_files
.
append
(
          
_ParseRootNode
(
ElementTree
.
fromstring
(
clean_xml
.
encode
(
'
utf
-
8
'
)
)
                         
annotations
)
)
    
return
parsed_dex_files
  
finally
:
    
shutil
.
rmtree
(
dexfile_dir
)
def
_ParseAnnotations
(
dexRaw
:
str
)
-
>
Dict
[
int
Annotations
]
:
  
"
"
"
Parse
XML
strings
and
return
a
list
of
Annotations
mapped
to
  
classes
by
index
.
  
Annotations
are
written
to
the
dex
dump
as
human
readable
blocks
of
text
  
The
only
prescription
is
that
they
appear
before
the
class
in
our
xml
file
  
They
are
not
required
to
be
nested
within
the
package
as
our
classes
  
It
is
simpler
to
parse
for
all
the
annotations
and
then
associate
them
  
back
to
the
  
classes
  
Example
:
  
Class
#
12
annotations
:
  
Annotations
on
class
    
VISIBILITY_RUNTIME
Ldalvik
/
annotation
/
EnclosingClass
;
value
=
.
.
.
  
Annotations
on
method
#
512
'
example
'
    
VISIBILITY_SYSTEM
Ldalvik
/
annotation
/
Signature
;
value
=
.
.
.
  
"
"
"
  
annotationsBlockMatcher
=
re
.
compile
(
u
'
^
Class
#
.
*
annotations
:
'
)
  
classIndexMatcher
=
re
.
compile
(
u
'
(
?
<
=
#
)
[
0
-
9
]
*
'
)
  
methodMatcher
=
re
.
compile
(
u
"
(
?
<
=
'
)
[
^
'
]
*
"
)
  
annotationMatcher
=
re
.
compile
(
u
'
[
^
/
]
*
(
?
=
;
)
'
)
  
annotations
=
{
}
  
currentAnnotationsForClass
=
None
  
currentAnnotationsBlock
:
Dict
[
str
None
]
=
None
  
for
line
in
dexRaw
.
splitlines
(
)
:
    
if
currentAnnotationsForClass
is
None
:
      
if
annotationsBlockMatcher
.
match
(
line
)
:
        
currentClassIndex
=
int
(
classIndexMatcher
.
findall
(
line
)
[
0
]
)
        
currentAnnotationsForClass
=
Annotations
(
classAnnotations
=
{
}
                                                 
methodsAnnotations
=
{
}
)
        
annotations
[
currentClassIndex
]
=
currentAnnotationsForClass
    
else
:
      
if
line
.
startswith
(
u
'
Annotations
on
class
'
)
:
        
currentAnnotationsBlock
=
currentAnnotationsForClass
.
classAnnotations
      
elif
line
.
startswith
(
u
'
Annotations
on
method
'
)
:
        
method
=
methodMatcher
.
findall
(
line
)
[
0
]
        
currentAnnotationsBlock
=
{
}
        
currentAnnotationsForClass
.
methodsAnnotations
[
            
method
]
=
currentAnnotationsBlock
      
elif
line
.
startswith
(
u
'
Annotations
on
'
)
:
        
currentAnnotationsBlock
=
None
      
elif
currentAnnotationsBlock
is
not
None
and
line
.
strip
(
)
.
startswith
(
          
'
VISIBILITY_RUNTIME
'
)
:
        
annotation
=
annotationMatcher
.
findall
(
line
)
[
0
]
        
currentAnnotationsBlock
.
update
(
{
annotation
:
None
}
)
      
elif
not
line
.
strip
(
)
:
        
currentAnnotationsForClass
=
None
        
currentAnnotationsBlock
=
None
  
return
annotations
def
_ParseRootNode
(
root
annotations
:
Dict
[
int
Annotations
]
)
:
  
"
"
"
Parses
the
XML
output
of
dexdump
.
This
output
is
in
the
following
format
.
  
This
is
a
subset
of
the
information
contained
within
dexdump
output
.
  
<
api
>
    
<
package
name
=
"
foo
.
bar
"
>
      
<
class
name
=
"
Class
"
extends
=
"
foo
.
bar
.
SuperClass
"
>
        
<
field
name
=
"
Field
"
>
        
<
/
field
>
        
<
constructor
name
=
"
Method
"
>
          
<
parameter
name
=
"
Param
"
type
=
"
int
"
>
          
<
/
parameter
>
        
<
/
constructor
>
        
<
method
name
=
"
Method
"
>
          
<
parameter
name
=
"
Param
"
type
=
"
int
"
>
          
<
/
parameter
>
        
<
/
method
>
      
<
/
class
>
    
<
/
package
>
  
<
/
api
>
  
"
"
"
  
results
=
{
}
  
classCount
=
0
  
for
child
in
root
:
    
if
child
.
tag
=
=
'
package
'
:
      
package_name
=
child
.
attrib
[
'
name
'
]
      
parsed_node
classCount
=
_ParsePackageNode
(
child
classCount
                                                  
annotations
)
      
if
package_name
in
results
:
        
results
[
package_name
]
[
'
classes
'
]
.
update
(
parsed_node
[
'
classes
'
]
)
      
else
:
        
results
[
package_name
]
=
parsed_node
  
return
results
def
_ParsePackageNode
(
package_node
classCount
:
int
                      
annotations
:
Dict
[
int
Annotations
]
)
:
  
"
"
"
Parses
a
<
package
>
node
from
the
dexdump
xml
output
.
  
Returns
:
    
A
tuple
in
the
format
:
      
(
classes
:
{
        
'
classes
'
:
{
          
<
class_1
>
:
{
            
'
methods
'
:
[
<
method_1
>
<
method_2
>
]
            
'
superclass
'
:
<
string
>
            
'
is_abstract
'
:
<
boolean
>
            
'
annotations
'
:
<
Annotations
or
None
>
          
}
          
<
class_2
>
:
{
            
'
methods
'
:
[
<
method_1
>
<
method_2
>
]
            
'
superclass
'
:
<
string
>
            
'
is_abstract
'
:
<
boolean
>
            
'
annotations
'
:
<
Annotations
or
None
>
          
}
        
}
      
}
classCount
:
number
)
  
"
"
"
  
classes
=
{
}
  
for
child
in
package_node
:
    
if
child
.
tag
=
=
'
class
'
:
      
classes
[
child
.
attrib
[
'
name
'
]
]
=
_ParseClassNode
(
child
classCount
                                                      
annotations
)
      
classCount
+
=
1
  
return
(
{
'
classes
'
:
classes
}
classCount
)
def
_ParseClassNode
(
class_node
classIndex
:
int
                    
annotations
:
Dict
[
int
Annotations
]
)
:
  
"
"
"
Parses
a
<
class
>
node
from
the
dexdump
xml
output
.
  
Returns
:
    
A
dict
in
the
format
:
      
{
        
'
methods
'
:
[
<
method_1
>
<
method_2
>
]
        
'
superclass
'
:
<
string
>
        
'
is_abstract
'
:
<
boolean
>
      
}
  
"
"
"
  
methods
=
[
]
  
for
child
in
class_node
:
    
if
child
.
tag
=
=
'
method
'
and
child
.
attrib
[
'
visibility
'
]
=
=
'
public
'
:
      
methods
.
append
(
child
.
attrib
[
'
name
'
]
)
  
return
{
      
'
methods
'
:
      
methods
      
'
superclass
'
:
      
class_node
.
attrib
[
'
extends
'
]
      
'
is_abstract
'
:
      
class_node
.
attrib
.
get
(
'
abstract
'
)
=
=
'
true
'
      
'
annotations
'
:
      
annotations
.
get
(
classIndex
                      
Annotations
(
classAnnotations
=
{
}
methodsAnnotations
=
{
}
)
)
  
}
