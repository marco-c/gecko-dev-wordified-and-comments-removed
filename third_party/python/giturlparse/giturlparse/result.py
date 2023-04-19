from
copy
import
copy
from
.
platforms
import
PLATFORMS
REQUIRED_ATTRIBUTES
=
(
    
"
domain
"
    
"
repo
"
)
class
GitUrlParsed
:
    
platform
=
None
    
def
__init__
(
self
parsed_info
)
:
        
self
.
_parsed
=
parsed_info
        
for
k
v
in
parsed_info
.
items
(
)
:
            
setattr
(
self
k
v
)
        
for
name
platform
in
PLATFORMS
:
            
if
name
=
=
self
.
platform
:
                
self
.
_platform_obj
=
platform
                
break
    
def
_valid_attrs
(
self
)
:
        
return
all
(
[
getattr
(
self
attr
None
)
for
attr
in
REQUIRED_ATTRIBUTES
]
)
    
property
    
def
valid
(
self
)
:
        
return
all
(
            
[
                
self
.
_valid_attrs
(
)
            
]
        
)
    
property
    
def
host
(
self
)
:
        
return
self
.
domain
    
property
    
def
resource
(
self
)
:
        
return
self
.
domain
    
property
    
def
name
(
self
)
:
        
return
self
.
repo
    
property
    
def
user
(
self
)
:
        
if
hasattr
(
self
"
_user
"
)
:
            
return
self
.
_user
        
return
self
.
owner
    
property
    
def
groups
(
self
)
:
        
if
self
.
groups_path
:
            
return
self
.
groups_path
.
split
(
"
/
"
)
        
else
:
            
return
[
]
    
def
format
(
self
protocol
)
:
        
"
"
"
Reformat
URL
to
protocol
.
"
"
"
        
items
=
copy
(
self
.
_parsed
)
        
items
[
"
port_slash
"
]
=
"
%
s
/
"
%
self
.
port
if
self
.
port
else
"
"
        
items
[
"
groups_slash
"
]
=
"
%
s
/
"
%
self
.
groups_path
if
self
.
groups_path
else
"
"
        
return
self
.
_platform_obj
.
FORMATS
[
protocol
]
%
items
    
property
    
def
normalized
(
self
)
:
        
"
"
"
Normalize
URL
.
"
"
"
        
return
self
.
format
(
self
.
protocol
)
    
property
    
def
url2ssh
(
self
)
:
        
return
self
.
format
(
"
ssh
"
)
    
property
    
def
url2http
(
self
)
:
        
return
self
.
format
(
"
http
"
)
    
property
    
def
url2https
(
self
)
:
        
return
self
.
format
(
"
https
"
)
    
property
    
def
url2git
(
self
)
:
        
return
self
.
format
(
"
git
"
)
    
property
    
def
urls
(
self
)
:
        
return
{
protocol
:
self
.
format
(
protocol
)
for
protocol
in
self
.
_platform_obj
.
PROTOCOLS
}
    
property
    
def
github
(
self
)
:
        
return
self
.
platform
=
=
"
github
"
    
property
    
def
bitbucket
(
self
)
:
        
return
self
.
platform
=
=
"
bitbucket
"
    
property
    
def
friendcode
(
self
)
:
        
return
self
.
platform
=
=
"
friendcode
"
    
property
    
def
assembla
(
self
)
:
        
return
self
.
platform
=
=
"
assembla
"
    
property
    
def
gitlab
(
self
)
:
        
return
self
.
platform
=
=
"
gitlab
"
    
property
    
def
data
(
self
)
:
        
return
dict
(
self
.
_parsed
)
