"
"
"
certifi
.
py
~
~
~
~
~
~
~
~
~
~
This
module
returns
the
installation
location
of
cacert
.
pem
or
its
contents
.
"
"
"
import
sys
if
sys
.
version_info
>
=
(
3
11
)
:
    
from
importlib
.
resources
import
as_file
files
    
_CACERT_CTX
=
None
    
_CACERT_PATH
=
None
    
def
where
(
)
-
>
str
:
        
global
_CACERT_CTX
        
global
_CACERT_PATH
        
if
_CACERT_PATH
is
None
:
            
_CACERT_CTX
=
as_file
(
files
(
"
certifi
"
)
.
joinpath
(
"
cacert
.
pem
"
)
)
            
_CACERT_PATH
=
str
(
_CACERT_CTX
.
__enter__
(
)
)
        
return
_CACERT_PATH
    
def
contents
(
)
-
>
str
:
        
return
files
(
"
certifi
"
)
.
joinpath
(
"
cacert
.
pem
"
)
.
read_text
(
encoding
=
"
ascii
"
)
elif
sys
.
version_info
>
=
(
3
7
)
:
    
from
importlib
.
resources
import
path
as
get_path
read_text
    
_CACERT_CTX
=
None
    
_CACERT_PATH
=
None
    
def
where
(
)
-
>
str
:
        
global
_CACERT_CTX
        
global
_CACERT_PATH
        
if
_CACERT_PATH
is
None
:
            
_CACERT_CTX
=
get_path
(
"
certifi
"
"
cacert
.
pem
"
)
            
_CACERT_PATH
=
str
(
_CACERT_CTX
.
__enter__
(
)
)
        
return
_CACERT_PATH
    
def
contents
(
)
-
>
str
:
        
return
read_text
(
"
certifi
"
"
cacert
.
pem
"
encoding
=
"
ascii
"
)
else
:
    
import
os
    
import
types
    
from
typing
import
Union
    
Package
=
Union
[
types
.
ModuleType
str
]
    
Resource
=
Union
[
str
"
os
.
PathLike
"
]
    
def
read_text
(
        
package
:
Package
        
resource
:
Resource
        
encoding
:
str
=
'
utf
-
8
'
        
errors
:
str
=
'
strict
'
    
)
-
>
str
:
        
with
open
(
where
(
)
encoding
=
encoding
)
as
data
:
            
return
data
.
read
(
)
    
def
where
(
)
-
>
str
:
        
f
=
os
.
path
.
dirname
(
__file__
)
        
return
os
.
path
.
join
(
f
"
cacert
.
pem
"
)
    
def
contents
(
)
-
>
str
:
        
return
read_text
(
"
certifi
"
"
cacert
.
pem
"
encoding
=
"
ascii
"
)
