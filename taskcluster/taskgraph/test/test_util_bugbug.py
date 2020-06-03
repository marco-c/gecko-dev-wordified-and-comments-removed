from
__future__
import
absolute_import
print_function
unicode_literals
import
mozunit
from
taskgraph
.
util
.
bugbug
import
(
    
BUGBUG_BASE_URL
    
push_schedules
)
def
test_group_translation
(
responses
)
:
    
branch
=
"
integration
/
autoland
"
    
rev
=
"
abcdef
"
    
query
=
"
/
push
/
{
}
/
{
}
/
schedules
"
.
format
(
branch
rev
)
    
url
=
BUGBUG_BASE_URL
+
query
    
responses
.
add
(
        
responses
.
GET
        
url
        
json
=
{
            
"
groups
"
:
{
                
"
dom
/
indexedDB
"
:
1
                
"
testing
/
web
-
platform
/
tests
/
IndexedDB
"
:
1
                
"
testing
/
web
-
platform
/
mozilla
/
tests
/
IndexedDB
"
:
1
            
}
        
}
        
status
=
200
    
)
    
assert
len
(
push_schedules
)
=
=
0
    
data
=
push_schedules
(
branch
rev
)
    
print
(
data
)
    
assert
sorted
(
data
[
"
groups
"
]
)
=
=
[
        
"
/
IndexedDB
"
        
"
/
_mozilla
/
IndexedDB
"
        
"
dom
/
indexedDB
"
    
]
    
assert
len
(
push_schedules
)
=
=
1
    
responses
.
reset
(
)
    
push_schedules
(
branch
rev
)
    
assert
len
(
push_schedules
)
=
=
1
if
__name__
=
=
'
__main__
'
:
    
mozunit
.
main
(
)
