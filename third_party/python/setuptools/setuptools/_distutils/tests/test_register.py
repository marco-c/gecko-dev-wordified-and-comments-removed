"
"
"
Tests
for
distutils
.
command
.
register
.
"
"
"
import
getpass
import
os
import
pathlib
import
urllib
from
distutils
.
command
import
register
as
register_module
from
distutils
.
command
.
register
import
register
from
distutils
.
errors
import
DistutilsSetupError
from
distutils
.
tests
.
test_config
import
BasePyPIRCCommandTestCase
import
pytest
try
:
    
import
docutils
except
ImportError
:
    
docutils
=
None
PYPIRC_NOPASSWORD
=
"
"
"
\
[
distutils
]
index
-
servers
=
    
server1
[
server1
]
username
:
me
"
"
"
WANTED_PYPIRC
=
"
"
"
\
[
distutils
]
index
-
servers
=
    
pypi
[
pypi
]
username
:
tarek
password
:
password
"
"
"
class
Inputs
:
    
"
"
"
Fakes
user
inputs
.
"
"
"
    
def
__init__
(
self
*
answers
)
:
        
self
.
answers
=
answers
        
self
.
index
=
0
    
def
__call__
(
self
prompt
=
'
'
)
:
        
try
:
            
return
self
.
answers
[
self
.
index
]
        
finally
:
            
self
.
index
+
=
1
class
FakeOpener
:
    
"
"
"
Fakes
a
PyPI
server
"
"
"
    
def
__init__
(
self
)
:
        
self
.
reqs
=
[
]
    
def
__call__
(
self
*
args
)
:
        
return
self
    
def
open
(
self
req
data
=
None
timeout
=
None
)
:
        
self
.
reqs
.
append
(
req
)
        
return
self
    
def
read
(
self
)
:
        
return
b
'
xxx
'
    
def
getheader
(
self
name
default
=
None
)
:
        
return
{
            
'
content
-
type
'
:
'
text
/
plain
;
charset
=
utf
-
8
'
        
}
.
get
(
name
.
lower
(
)
default
)
pytest
.
fixture
(
autouse
=
True
)
def
autopass
(
monkeypatch
)
:
    
monkeypatch
.
setattr
(
getpass
'
getpass
'
lambda
prompt
:
'
password
'
)
pytest
.
fixture
(
autouse
=
True
)
def
fake_opener
(
monkeypatch
request
)
:
    
opener
=
FakeOpener
(
)
    
monkeypatch
.
setattr
(
urllib
.
request
'
build_opener
'
opener
)
    
monkeypatch
.
setattr
(
urllib
.
request
'
_opener
'
None
)
    
request
.
instance
.
conn
=
opener
class
TestRegister
(
BasePyPIRCCommandTestCase
)
:
    
def
_get_cmd
(
self
metadata
=
None
)
:
        
if
metadata
is
None
:
            
metadata
=
{
                
'
url
'
:
'
xxx
'
                
'
author
'
:
'
xxx
'
                
'
author_email
'
:
'
xxx
'
                
'
name
'
:
'
xxx
'
                
'
version
'
:
'
xxx
'
                
'
long_description
'
:
'
xxx
'
            
}
        
pkg_info
dist
=
self
.
create_dist
(
*
*
metadata
)
        
return
register
(
dist
)
    
def
test_create_pypirc
(
self
)
:
        
cmd
=
self
.
_get_cmd
(
)
        
assert
not
os
.
path
.
exists
(
self
.
rc
)
        
inputs
=
Inputs
(
'
1
'
'
tarek
'
'
y
'
)
        
register_module
.
input
=
inputs
.
__call__
        
try
:
            
cmd
.
run
(
)
        
finally
:
            
del
register_module
.
input
        
assert
pathlib
.
Path
(
self
.
rc
)
.
read_text
(
encoding
=
'
utf
-
8
'
)
=
=
WANTED_PYPIRC
        
def
_no_way
(
prompt
=
'
'
)
:
            
raise
AssertionError
(
prompt
)
        
register_module
.
input
=
_no_way
        
cmd
.
show_response
=
True
        
cmd
.
run
(
)
        
assert
len
(
self
.
conn
.
reqs
)
=
=
2
        
req1
=
dict
(
self
.
conn
.
reqs
[
0
]
.
headers
)
        
req2
=
dict
(
self
.
conn
.
reqs
[
1
]
.
headers
)
        
assert
req1
[
'
Content
-
length
'
]
=
=
'
1358
'
        
assert
req2
[
'
Content
-
length
'
]
=
=
'
1358
'
        
assert
b
'
xxx
'
in
self
.
conn
.
reqs
[
1
]
.
data
    
def
test_password_not_in_file
(
self
)
:
        
self
.
write_file
(
self
.
rc
PYPIRC_NOPASSWORD
)
        
cmd
=
self
.
_get_cmd
(
)
        
cmd
.
_set_config
(
)
        
cmd
.
finalize_options
(
)
        
cmd
.
send_metadata
(
)
        
assert
cmd
.
distribution
.
password
=
=
'
password
'
    
def
test_registering
(
self
)
:
        
cmd
=
self
.
_get_cmd
(
)
        
inputs
=
Inputs
(
'
2
'
'
tarek
'
'
tarek
ziade
.
org
'
)
        
register_module
.
input
=
inputs
.
__call__
        
try
:
            
cmd
.
run
(
)
        
finally
:
            
del
register_module
.
input
        
assert
len
(
self
.
conn
.
reqs
)
=
=
1
        
req
=
self
.
conn
.
reqs
[
0
]
        
headers
=
dict
(
req
.
headers
)
        
assert
headers
[
'
Content
-
length
'
]
=
=
'
608
'
        
assert
b
'
tarek
'
in
req
.
data
    
def
test_password_reset
(
self
)
:
        
cmd
=
self
.
_get_cmd
(
)
        
inputs
=
Inputs
(
'
3
'
'
tarek
ziade
.
org
'
)
        
register_module
.
input
=
inputs
.
__call__
        
try
:
            
cmd
.
run
(
)
        
finally
:
            
del
register_module
.
input
        
assert
len
(
self
.
conn
.
reqs
)
=
=
1
        
req
=
self
.
conn
.
reqs
[
0
]
        
headers
=
dict
(
req
.
headers
)
        
assert
headers
[
'
Content
-
length
'
]
=
=
'
290
'
        
assert
b
'
tarek
'
in
req
.
data
    
def
test_strict
(
self
)
:
        
pytest
.
importorskip
(
'
docutils
'
)
        
cmd
=
self
.
_get_cmd
(
{
}
)
        
cmd
.
ensure_finalized
(
)
        
cmd
.
strict
=
True
        
with
pytest
.
raises
(
DistutilsSetupError
)
:
            
cmd
.
run
(
)
        
metadata
=
{
            
'
url
'
:
'
xxx
'
            
'
author
'
:
'
xxx
'
            
'
author_email
'
:
'
x
x
'
            
'
name
'
:
'
xxx
'
            
'
version
'
:
'
xxx
'
            
'
long_description
'
:
'
title
\
n
=
=
\
n
\
ntext
'
        
}
        
cmd
=
self
.
_get_cmd
(
metadata
)
        
cmd
.
ensure_finalized
(
)
        
cmd
.
strict
=
True
        
with
pytest
.
raises
(
DistutilsSetupError
)
:
            
cmd
.
run
(
)
        
metadata
[
'
long_description
'
]
=
'
title
\
n
=
=
=
=
=
\
n
\
ntext
'
        
cmd
=
self
.
_get_cmd
(
metadata
)
        
cmd
.
ensure_finalized
(
)
        
cmd
.
strict
=
True
        
inputs
=
Inputs
(
'
1
'
'
tarek
'
'
y
'
)
        
register_module
.
input
=
inputs
.
__call__
        
try
:
            
cmd
.
run
(
)
        
finally
:
            
del
register_module
.
input
        
cmd
=
self
.
_get_cmd
(
)
        
cmd
.
ensure_finalized
(
)
        
inputs
=
Inputs
(
'
1
'
'
tarek
'
'
y
'
)
        
register_module
.
input
=
inputs
.
__call__
        
try
:
            
cmd
.
run
(
)
        
finally
:
            
del
register_module
.
input
        
metadata
=
{
            
'
url
'
:
'
xxx
'
            
'
author
'
:
'
\
u00c9ric
'
            
'
author_email
'
:
'
xxx
'
            
'
name
'
:
'
xxx
'
            
'
version
'
:
'
xxx
'
            
'
description
'
:
'
Something
about
esszet
\
u00df
'
            
'
long_description
'
:
'
More
things
about
esszet
\
u00df
'
        
}
        
cmd
=
self
.
_get_cmd
(
metadata
)
        
cmd
.
ensure_finalized
(
)
        
cmd
.
strict
=
True
        
inputs
=
Inputs
(
'
1
'
'
tarek
'
'
y
'
)
        
register_module
.
input
=
inputs
.
__call__
        
try
:
            
cmd
.
run
(
)
        
finally
:
            
del
register_module
.
input
    
def
test_register_invalid_long_description
(
self
monkeypatch
)
:
        
pytest
.
importorskip
(
'
docutils
'
)
        
description
=
'
:
funkie
:
str
'
        
metadata
=
{
            
'
url
'
:
'
xxx
'
            
'
author
'
:
'
xxx
'
            
'
author_email
'
:
'
xxx
'
            
'
name
'
:
'
xxx
'
            
'
version
'
:
'
xxx
'
            
'
long_description
'
:
description
        
}
        
cmd
=
self
.
_get_cmd
(
metadata
)
        
cmd
.
ensure_finalized
(
)
        
cmd
.
strict
=
True
        
inputs
=
Inputs
(
'
2
'
'
tarek
'
'
tarek
ziade
.
org
'
)
        
monkeypatch
.
setattr
(
register_module
'
input
'
inputs
raising
=
False
)
        
with
pytest
.
raises
(
DistutilsSetupError
)
:
            
cmd
.
run
(
)
    
def
test_list_classifiers
(
self
caplog
)
:
        
cmd
=
self
.
_get_cmd
(
)
        
cmd
.
list_classifiers
=
True
        
cmd
.
run
(
)
        
assert
caplog
.
messages
=
=
[
'
running
check
'
'
xxx
'
]
    
def
test_show_response
(
self
caplog
)
:
        
cmd
=
self
.
_get_cmd
(
)
        
inputs
=
Inputs
(
'
1
'
'
tarek
'
'
y
'
)
        
register_module
.
input
=
inputs
.
__call__
        
cmd
.
show_response
=
True
        
try
:
            
cmd
.
run
(
)
        
finally
:
            
del
register_module
.
input
        
assert
caplog
.
messages
[
3
]
=
=
75
*
'
-
'
+
'
\
nxxx
\
n
'
+
75
*
'
-
'
