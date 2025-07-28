import
argparse
import
subprocess
as
sp
import
sys
parser
=
argparse
.
ArgumentParser
(
)
parser
.
add_argument
(
"
-
-
javadoc
"
)
parser
.
add_argument
(
"
-
-
doclet
-
jar
"
)
parser
.
add_argument
(
"
-
-
java
-
root
"
)
parser
.
add_argument
(
"
-
-
out
-
dir
"
)
parser
.
add_argument
(
"
-
-
expected
"
)
parser
.
add_argument
(
"
-
-
expected
-
map
"
)
args
=
parser
.
parse_args
(
)
output
=
args
.
out_dir
+
"
/
api
.
txt
"
sp
.
check_call
(
    
[
        
args
.
javadoc
        
"
-
doclet
"
        
"
org
.
mozilla
.
doclet
.
ApiDoclet
"
        
"
-
docletpath
"
        
args
.
doclet_jar
        
"
-
subpackages
"
        
"
org
.
mozilla
.
test
"
        
"
-
sourcepath
"
        
args
.
java_root
        
"
-
root
-
dir
"
        
args
.
java_root
        
"
-
skip
-
class
-
regex
"
        
"
TestSkippedClass
:
^
org
.
mozilla
.
test
.
TestClass
.
TestSkippedClass2
"
        
"
-
output
"
        
output
    
]
)
result
=
sp
.
call
(
    
[
        
"
python3
"
        
"
.
.
/
apilint
/
src
/
main
/
resources
/
diff
.
py
"
        
"
-
-
existing
"
        
args
.
expected
        
"
-
-
local
"
        
output
    
]
)
result_map
=
sp
.
call
(
    
[
        
"
python3
"
        
"
.
.
/
apilint
/
src
/
main
/
resources
/
diff
.
py
"
        
"
-
-
existing
"
        
args
.
expected_map
        
"
-
-
local
"
        
output
+
"
.
map
"
    
]
)
if
result
!
=
0
or
result_map
!
=
0
:
    
print
(
"
"
)
    
print
(
"
ERROR
:
Doclet
output
differs
from
expected
.
"
)
    
sys
.
exit
(
1
)
