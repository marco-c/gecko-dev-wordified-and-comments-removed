import
unittest
from
textwrap
import
dedent
from
gecko_taskgraph
.
util
import
yaml
from
mozunit
import
main
MockedOpen
class
TestYaml
(
unittest
.
TestCase
)
:
    
def
test_load
(
self
)
:
        
with
MockedOpen
(
            
{
                
"
/
dir1
/
dir2
/
foo
.
yml
"
:
dedent
(
                    
"
"
"
\
                    
prop
:
                        
-
val1
                    
"
"
"
                
)
            
}
        
)
:
            
self
.
assertEqual
(
                
yaml
.
load_yaml
(
"
/
dir1
/
dir2
"
"
foo
.
yml
"
)
{
"
prop
"
:
[
"
val1
"
]
}
            
)
    
def
test_key_order
(
self
)
:
        
with
MockedOpen
(
            
{
                
"
/
dir1
/
dir2
/
foo
.
yml
"
:
dedent
(
                    
"
"
"
\
                    
job
:
                        
foo
:
1
                        
bar
:
2
                        
xyz
:
3
                    
"
"
"
                
)
            
}
        
)
:
            
self
.
assertEqual
(
                
list
(
yaml
.
load_yaml
(
"
/
dir1
/
dir2
"
"
foo
.
yml
"
)
[
"
job
"
]
.
keys
(
)
)
                
[
"
foo
"
"
bar
"
"
xyz
"
]
            
)
if
__name__
=
=
"
__main__
"
:
    
main
(
)
