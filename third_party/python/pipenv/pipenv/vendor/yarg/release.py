#
-
*
-
coding
:
utf
-
8
-
*
-
from
datetime
import
datetime
class
Release
(
object
)
:
    
"
"
"
    
A
release
file
from
PyPI
.
    
:
param
release_id
:
A
release
id
.
    
:
param
pypi_dict
:
A
dictionary
of
a
release
file
.
    
"
"
"
    
def
__init__
(
self
release_id
pypi_dict
)
:
        
self
.
_release
=
pypi_dict
        
self
.
_release
[
'
release_id
'
]
=
release_id
    
def
__repr__
(
self
)
:
        
return
"
<
Release
{
0
}
>
"
.
format
(
self
.
release_id
)
    
property
    
def
release_id
(
self
)
:
        
"
"
"
            
>
>
>
package
=
yarg
.
get
(
'
yarg
'
)
            
>
>
>
v
=
"
0
.
1
.
0
"
            
>
>
>
r
=
package
.
release
(
v
)
            
>
>
>
r
[
0
]
.
release_id
            
u
'
0
.
1
.
0
'
        
"
"
"
        
return
self
.
_release
[
'
release_id
'
]
    
property
    
def
uploaded
(
self
)
:
        
"
"
"
            
>
>
>
package
=
yarg
.
get
(
'
yarg
'
)
            
>
>
>
v
=
"
0
.
1
.
0
"
            
>
>
>
r
=
package
.
release
(
v
)
            
>
>
>
r
.
uploaded
            
datetime
.
datime
(
2014
8
7
21
26
19
)
        
"
"
"
        
return
datetime
.
strptime
(
self
.
_release
[
'
upload_time
'
]
                                 
'
%
Y
-
%
m
-
%
dT
%
H
:
%
M
:
%
S
'
)
    
property
    
def
python_version
(
self
)
:
        
"
"
"
            
>
>
>
package
=
yarg
.
get
(
'
yarg
'
)
            
>
>
>
v
=
"
0
.
1
.
0
"
            
>
>
>
r
=
package
.
release
(
v
)
            
>
>
>
r
.
python_version
            
u
'
2
.
7
'
        
"
"
"
        
return
self
.
_release
[
'
python_version
'
]
    
property
    
def
url
(
self
)
:
        
"
"
"
            
>
>
>
package
=
yarg
.
get
(
'
yarg
'
)
            
>
>
>
v
=
"
0
.
1
.
0
"
            
>
>
>
r
=
package
.
release
(
v
)
            
>
>
>
r
.
url
            
u
'
https
:
/
/
pypi
.
python
.
org
/
packages
/
2
.
7
/
y
/
yarg
/
yarg
.
.
.
'
        
"
"
"
        
return
self
.
_release
[
'
url
'
]
    
property
    
def
md5_digest
(
self
)
:
        
"
"
"
            
>
>
>
package
=
yarg
.
get
(
'
yarg
'
)
            
>
>
>
v
=
"
0
.
1
.
0
"
            
>
>
>
r
=
package
.
release
(
v
)
            
>
>
>
r
.
md5_digest
            
u
'
bec88e1c1765ca6177360e8f37b44c5c
'
        
"
"
"
        
return
self
.
_release
[
'
md5_digest
'
]
    
property
    
def
filename
(
self
)
:
        
"
"
"
            
>
>
>
package
=
yarg
.
get
(
'
yarg
'
)
            
>
>
>
v
=
"
0
.
1
.
0
"
            
>
>
>
r
=
package
.
release
(
v
)
            
>
>
>
r
.
filename
            
u
'
yarg
-
0
.
1
.
0
-
py27
-
none
-
any
.
whl
'
        
"
"
"
        
return
self
.
_release
[
'
filename
'
]
    
property
    
def
size
(
self
)
:
        
"
"
"
            
>
>
>
package
=
yarg
.
get
(
'
yarg
'
)
            
>
>
>
v
=
"
0
.
1
.
0
"
            
>
>
>
r
=
package
.
release
(
v
)
            
>
>
>
r
.
size
            
52941
        
"
"
"
        
return
self
.
_release
[
'
size
'
]
    
property
    
def
package_type
(
self
)
:
        
"
"
"
            
>
>
>
package
=
yarg
.
get
(
'
yarg
'
)
            
>
>
>
v
=
"
0
.
1
.
0
"
            
>
>
>
r
=
package
.
release
(
v
)
            
>
>
>
r
.
package_type
            
u
'
wheel
'
        
"
"
"
        
mapping
=
{
'
bdist_egg
'
:
u
'
egg
'
'
bdist_wheel
'
:
u
'
wheel
'
                   
'
sdist
'
:
u
'
source
'
}
        
ptype
=
self
.
_release
[
'
packagetype
'
]
        
if
ptype
in
mapping
.
keys
(
)
:
            
return
mapping
[
ptype
]
        
return
ptype
    
property
    
def
has_sig
(
self
)
:
        
"
"
"
            
>
>
>
package
=
yarg
.
get
(
'
yarg
'
)
            
>
>
>
v
=
"
0
.
1
.
0
"
            
>
>
>
r
=
package
.
release
(
v
)
            
>
>
>
r
.
has_sig
            
True
        
"
"
"
        
return
self
.
_release
[
'
has_sig
'
]
