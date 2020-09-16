from
__future__
import
absolute_import
print_function
unicode_literals
from
datetime
import
datetime
from
textwrap
import
dedent
from
time
import
mktime
import
pytest
from
mozunit
import
main
from
taskgraph
.
util
.
backstop
import
(
    
is_backstop
    
BACKSTOP_INDEX
    
BACKSTOP_PUSH_INTERVAL
    
BACKSTOP_TIME_INTERVAL
)
from
taskgraph
.
util
.
taskcluster
import
get_index_url
pytest
.
fixture
(
scope
=
'
module
'
)
def
params
(
)
:
    
return
{
        
'
branch
'
:
'
integration
/
autoland
'
        
'
head_repository
'
:
'
https
:
/
/
hg
.
mozilla
.
org
/
integration
/
autoland
'
        
'
head_rev
'
:
'
abcdef
'
        
'
project
'
:
'
autoland
'
        
'
pushdate
'
:
mktime
(
datetime
.
now
(
)
.
timetuple
(
)
)
    
}
def
test_is_backstop
(
responses
params
)
:
    
url
=
get_index_url
(
        
BACKSTOP_INDEX
.
format
(
project
=
params
[
"
project
"
]
)
    
)
+
"
/
artifacts
/
public
/
parameters
.
yml
"
    
responses
.
add
(
        
responses
.
GET
        
url
        
status
=
404
    
)
    
params
[
"
pushlog_id
"
]
=
1
    
assert
is_backstop
(
params
)
    
responses
.
replace
(
        
responses
.
GET
        
url
        
body
=
dedent
(
"
"
"
        
pushdate
:
{
pushdate
}
        
"
"
"
.
format
(
pushdate
=
params
[
"
pushdate
"
]
)
)
        
status
=
200
    
)
    
params
[
'
pushlog_id
'
]
=
BACKSTOP_PUSH_INTERVAL
-
1
    
params
[
'
pushdate
'
]
+
=
1
    
assert
not
is_backstop
(
params
)
    
params
[
'
pushlog_id
'
]
=
BACKSTOP_PUSH_INTERVAL
    
params
[
'
pushdate
'
]
+
=
1
    
assert
is_backstop
(
params
)
    
params
[
'
pushlog_id
'
]
=
BACKSTOP_PUSH_INTERVAL
+
1
    
params
[
'
pushdate
'
]
+
=
BACKSTOP_TIME_INTERVAL
*
60
    
assert
is_backstop
(
params
)
    
params
[
'
project
'
]
=
'
try
'
    
assert
not
is_backstop
(
params
)
    
params
[
'
project
'
]
=
'
mozilla
-
central
'
    
params
[
'
pushdate
'
]
-
=
BACKSTOP_TIME_INTERVAL
*
60
    
assert
is_backstop
(
params
)
if
__name__
=
=
'
__main__
'
:
    
main
(
)
