import
os
import
sys
import
unittest
import
mozunit
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
"
.
.
"
)
)
import
gen_static_components
from
gen_static_components
import
BackgroundTasksSelector
class
TestGenStaticComponents
(
unittest
.
TestCase
)
:
    
def
test_string
(
self
)
:
        
clas
=
{
            
"
cid
"
:
"
{
a8566880
-
0bc7
-
4822
-
adb9
-
748c9af5cce7
}
"
            
"
contract_ids
"
:
[
"
mozilla
.
org
/
dummy
-
class
;
1
"
]
            
"
jsm
"
:
"
resource
:
/
/
/
modules
/
DummyClass
.
jsm
"
            
"
js_name
"
:
"
dummyClass
"
            
"
constructor
"
:
"
DummyClassImpl
"
            
"
categories
"
:
{
                
"
dummy1
"
:
[
"
m
-
dummy1
"
"
m
-
dummy2
"
]
            
}
            
"
protocol_config
"
:
{
                
"
scheme
"
:
"
dummy
"
                
"
flags
"
:
[
]
            
}
        
}
        
substs
=
gen_static_components
.
gen_substs
(
[
{
"
Classes
"
:
[
clas
]
}
]
)
        
self
.
assertEqual
(
substs
[
"
category_count
"
]
1
)
        
self
.
assertEqual
(
            
[
s
.
strip
(
)
for
s
in
substs
[
"
categories
"
]
.
splitlines
(
)
]
            
[
                
'
{
{
0x0
}
/
*
"
dummy1
"
*
/
'
                
"
0
2
}
"
            
]
        
)
        
self
.
assertEqual
(
            
[
s
.
strip
(
)
for
s
in
substs
[
"
category_entries
"
]
.
splitlines
(
)
]
            
[
                
'
/
*
"
dummy1
"
*
/
'
                
'
{
{
0x7
}
/
*
"
m
-
dummy1
"
*
/
'
                
'
{
0x10
}
/
*
"
mozilla
.
org
/
dummy
-
class
;
1
"
*
/
'
                
"
Module
:
:
BackgroundTasksSelector
:
:
NO_TASKS
"
                
"
Module
:
:
ProcessSelector
:
:
ANY_PROCESS
}
"
                
'
{
{
0x2b
}
/
*
"
m
-
dummy2
"
*
/
'
                
'
{
0x10
}
/
*
"
mozilla
.
org
/
dummy
-
class
;
1
"
*
/
'
                
"
Module
:
:
BackgroundTasksSelector
:
:
NO_TASKS
"
                
"
Module
:
:
ProcessSelector
:
:
ANY_PROCESS
}
"
            
]
        
)
    
def
test_dict
(
self
)
:
        
clas
=
{
            
"
cid
"
:
"
{
a8566880
-
0bc7
-
4822
-
adb9
-
748c9af5cce7
}
"
            
"
contract_ids
"
:
[
"
mozilla
.
org
/
dummy
-
class
;
1
"
]
            
"
jsm
"
:
"
resource
:
/
/
/
modules
/
DummyClass
.
jsm
"
            
"
js_name
"
:
"
dummyClass
"
            
"
constructor
"
:
"
DummyClassImpl
"
            
"
categories
"
:
{
                
"
dummy1
"
:
{
                    
"
name
"
:
[
"
m
-
dummy1
"
"
m
-
dummy2
"
]
                
}
            
}
            
"
protocol_config
"
:
{
                
"
scheme
"
:
"
dummy
"
                
"
flags
"
:
[
]
            
}
        
}
        
substs
=
gen_static_components
.
gen_substs
(
[
{
"
Classes
"
:
[
clas
]
}
]
)
        
self
.
assertEqual
(
substs
[
"
category_count
"
]
1
)
        
self
.
assertEqual
(
            
[
s
.
strip
(
)
for
s
in
substs
[
"
categories
"
]
.
splitlines
(
)
]
            
[
                
'
{
{
0x0
}
/
*
"
dummy1
"
*
/
'
                
"
0
2
}
"
            
]
        
)
        
self
.
assertEqual
(
            
[
s
.
strip
(
)
for
s
in
substs
[
"
category_entries
"
]
.
splitlines
(
)
]
            
[
                
'
/
*
"
dummy1
"
*
/
'
                
'
{
{
0x7
}
/
*
"
m
-
dummy1
"
*
/
'
                
'
{
0x10
}
/
*
"
mozilla
.
org
/
dummy
-
class
;
1
"
*
/
'
                
"
Module
:
:
BackgroundTasksSelector
:
:
NO_TASKS
"
                
"
Module
:
:
ProcessSelector
:
:
ANY_PROCESS
}
"
                
'
{
{
0x2b
}
/
*
"
m
-
dummy2
"
*
/
'
                
'
{
0x10
}
/
*
"
mozilla
.
org
/
dummy
-
class
;
1
"
*
/
'
                
"
Module
:
:
BackgroundTasksSelector
:
:
NO_TASKS
"
                
"
Module
:
:
ProcessSelector
:
:
ANY_PROCESS
}
"
            
]
        
)
    
def
test_dict_with_selector
(
self
)
:
        
clas
=
{
            
"
cid
"
:
"
{
a8566880
-
0bc7
-
4822
-
adb9
-
748c9af5cce7
}
"
            
"
contract_ids
"
:
[
"
mozilla
.
org
/
dummy
-
class
;
1
"
]
            
"
jsm
"
:
"
resource
:
/
/
/
modules
/
DummyClass
.
jsm
"
            
"
js_name
"
:
"
dummyClass
"
            
"
constructor
"
:
"
DummyClassImpl
"
            
"
categories
"
:
{
                
"
dummy1
"
:
{
                    
"
name
"
:
[
"
m
-
dummy1
"
"
m
-
dummy2
"
]
                    
"
backgroundtasks
"
:
BackgroundTasksSelector
.
ALL_TASKS
                
}
            
}
            
"
protocol_config
"
:
{
                
"
scheme
"
:
"
dummy
"
                
"
flags
"
:
[
]
            
}
        
}
        
substs
=
gen_static_components
.
gen_substs
(
[
{
"
Classes
"
:
[
clas
]
}
]
)
        
self
.
assertEqual
(
substs
[
"
category_count
"
]
1
)
        
self
.
assertEqual
(
            
[
s
.
strip
(
)
for
s
in
substs
[
"
categories
"
]
.
splitlines
(
)
]
            
[
                
'
{
{
0x0
}
/
*
"
dummy1
"
*
/
'
                
"
0
2
}
"
            
]
        
)
        
self
.
assertEqual
(
            
[
s
.
strip
(
)
for
s
in
substs
[
"
category_entries
"
]
.
splitlines
(
)
]
            
[
                
'
/
*
"
dummy1
"
*
/
'
                
'
{
{
0x7
}
/
*
"
m
-
dummy1
"
*
/
'
                
'
{
0x10
}
/
*
"
mozilla
.
org
/
dummy
-
class
;
1
"
*
/
'
                
"
Module
:
:
BackgroundTasksSelector
:
:
ALL_TASKS
"
                
"
Module
:
:
ProcessSelector
:
:
ANY_PROCESS
}
"
                
'
{
{
0x2b
}
/
*
"
m
-
dummy2
"
*
/
'
                
'
{
0x10
}
/
*
"
mozilla
.
org
/
dummy
-
class
;
1
"
*
/
'
                
"
Module
:
:
BackgroundTasksSelector
:
:
ALL_TASKS
"
                
"
Module
:
:
ProcessSelector
:
:
ANY_PROCESS
}
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
    
mozunit
.
main
(
)
