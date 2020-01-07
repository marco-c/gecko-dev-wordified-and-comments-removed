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
import
xml
.
etree
.
ElementTree
import
requests
from
.
exceptions
import
HTTPError
def
_get
(
pypi_server
)
:
    
"
"
"
    
Query
the
PyPI
RSS
feed
and
return
a
list
    
of
XML
items
.
    
"
"
"
    
response
=
requests
.
get
(
pypi_server
)
    
if
response
.
status_code
>
=
300
:
        
raise
HTTPError
(
status_code
=
response
.
status_code
                        
reason
=
response
.
reason
)
    
if
hasattr
(
response
.
content
'
decode
'
)
:
        
tree
=
xml
.
etree
.
ElementTree
.
fromstring
(
response
.
content
.
decode
(
)
)
    
else
:
        
tree
=
xml
.
etree
.
ElementTree
.
fromstring
(
response
.
content
)
    
channel
=
tree
.
find
(
'
channel
'
)
    
return
channel
.
findall
(
'
item
'
)
def
newest_packages
(
        
pypi_server
=
"
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
pypi
?
%
3Aaction
=
packages_rss
"
)
:
    
"
"
"
    
Constructs
a
request
to
the
PyPI
server
and
returns
a
list
of
    
:
class
:
yarg
.
parse
.
Package
.
    
:
param
pypi_server
:
(
option
)
URL
to
the
PyPI
server
.
        
>
>
>
import
yarg
        
>
>
>
yarg
.
newest_packages
(
)
        
[
<
Package
yarg
>
<
Package
gray
>
<
Package
ragy
>
]
    
"
"
"
    
items
=
_get
(
pypi_server
)
    
i
=
[
]
    
for
item
in
items
:
        
i_dict
=
{
'
name
'
:
item
[
0
]
.
text
.
split
(
)
[
0
]
                  
'
url
'
:
item
[
1
]
.
text
                  
'
description
'
:
item
[
3
]
.
text
                  
'
date
'
:
item
[
4
]
.
text
}
        
i
.
append
(
Package
(
i_dict
)
)
    
return
i
def
latest_updated_packages
(
        
pypi_server
=
"
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
pypi
?
%
3Aaction
=
rss
"
)
:
    
"
"
"
    
Constructs
a
request
to
the
PyPI
server
and
returns
a
list
of
    
:
class
:
yarg
.
parse
.
Package
.
    
:
param
pypi_server
:
(
option
)
URL
to
the
PyPI
server
.
        
>
>
>
import
yarg
        
>
>
>
yarg
.
latest_updated_packages
(
)
        
[
<
Package
yarg
>
<
Package
gray
>
<
Package
ragy
>
]
    
"
"
"
    
items
=
_get
(
pypi_server
)
    
i
=
[
]
    
for
item
in
items
:
        
name
version
=
item
[
0
]
.
text
.
split
(
)
        
i_dict
=
{
'
name
'
:
name
                  
'
version
'
:
version
                  
'
url
'
:
item
[
1
]
.
text
                  
'
description
'
:
item
[
2
]
.
text
                  
'
date
'
:
item
[
3
]
.
text
}
        
i
.
append
(
Package
(
i_dict
)
)
    
return
i
class
Package
(
object
)
:
    
"
"
"
    
A
PyPI
package
generated
from
the
RSS
feed
information
.
    
:
param
pypi_dict
:
A
dictionary
retrieved
from
the
PyPI
server
.
    
"
"
"
    
def
__init__
(
self
pypi_dict
)
:
        
self
.
_content
=
pypi_dict
    
def
__repr__
(
self
)
:
        
return
"
<
Package
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
name
)
    
property
    
def
name
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
newest_packages
(
)
[
0
]
            
>
>
>
package
.
name
            
u
'
yarg
'
            
>
>
>
package
=
yarg
.
latest_updated_packages
(
)
[
0
]
            
>
>
>
package
.
name
            
u
'
yarg
'
        
"
"
"
        
return
self
.
_content
[
'
name
'
]
    
property
    
def
version
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
newest_packages
(
)
[
0
]
            
>
>
>
package
.
name
            
u
'
yarg
'
            
>
>
>
package
=
yarg
.
latest_updated_packages
(
)
[
0
]
            
>
>
>
package
.
name
            
u
'
yarg
'
        
"
"
"
        
if
'
version
'
not
in
self
.
_content
:
            
return
None
        
return
self
.
_content
[
'
version
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
        
This
is
only
available
for
:
meth
:
yarg
.
latest_updated_packages
for
        
:
meth
:
yarg
.
newest_packages
will
return
None
            
>
>
>
package
=
yarg
.
latest_updated_packages
(
)
[
0
]
            
>
>
>
package
.
url
            
u
'
http
:
/
/
pypi
.
python
.
org
/
pypi
/
yarg
'
        
"
"
"
        
return
self
.
_content
[
'
url
'
]
    
property
    
def
date
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
newest_packages
(
)
[
0
]
            
>
>
>
package
.
date
            
datetime
.
datetime
(
2014
8
9
8
40
20
)
            
>
>
>
package
=
yarg
.
latest_updated_packages
(
)
[
0
]
            
>
>
>
package
.
date
            
datetime
.
datetime
(
2014
8
9
8
40
20
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
_content
[
'
date
'
]
                                 
"
%
d
%
b
%
Y
%
H
:
%
M
:
%
S
%
Z
"
)
    
property
    
def
description
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
newest_packages
(
)
[
0
]
            
>
>
>
package
.
description
            
u
'
Some
random
summary
stuff
'
            
>
>
>
package
=
yarg
.
latest_updated_packages
(
)
[
0
]
            
>
>
>
package
.
description
            
u
'
Some
random
summary
stuff
'
        
"
"
"
        
return
self
.
_content
[
'
description
'
]
