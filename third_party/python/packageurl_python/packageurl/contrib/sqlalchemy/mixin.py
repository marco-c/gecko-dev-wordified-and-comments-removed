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
sqlalchemy
import
String
from
sqlalchemy
.
orm
import
Mapped
from
sqlalchemy
.
orm
import
declarative_mixin
from
sqlalchemy
.
orm
import
mapped_column
from
packageurl
import
PackageURL
declarative_mixin
class
PackageURLMixin
:
    
"
"
"
    
SQLAlchemy
declarative
mixin
class
for
Package
URL
"
purl
"
fields
support
.
    
"
"
"
    
type
:
Mapped
[
str
]
=
mapped_column
(
        
String
(
16
)
        
nullable
=
False
        
comment
=
(
            
"
A
short
code
to
identify
the
type
of
this
package
.
"
            
"
For
example
:
gem
for
a
Rubygem
docker
for
a
container
"
            
"
pypi
for
a
Python
Wheel
or
Egg
maven
for
a
Maven
Jar
"
            
"
deb
for
a
Debian
package
etc
.
"
        
)
    
)
    
namespace
:
Mapped
[
str
]
=
mapped_column
(
        
String
(
255
)
        
nullable
=
True
        
comment
=
(
            
"
Package
name
prefix
such
as
Maven
groupid
Docker
image
owner
"
            
"
GitHub
user
or
organization
etc
.
"
        
)
    
)
    
name
:
Mapped
[
str
]
=
mapped_column
(
String
(
100
)
nullable
=
False
comment
=
"
Name
of
the
package
.
"
)
    
version
:
Mapped
[
str
]
=
mapped_column
(
        
String
(
100
)
nullable
=
True
comment
=
"
Version
of
the
package
.
"
    
)
    
qualifiers
:
Mapped
[
str
]
=
mapped_column
(
        
String
(
1024
)
        
nullable
=
True
        
comment
=
(
            
"
Extra
qualifying
data
for
a
package
such
as
the
name
of
an
OS
"
            
"
architecture
distro
etc
.
"
        
)
    
)
    
subpath
:
Mapped
[
str
]
=
mapped_column
(
        
String
(
200
)
        
nullable
=
True
        
comment
=
"
Extra
subpath
within
a
package
relative
to
the
package
root
.
"
    
)
    
property
    
def
package_url
(
self
)
-
>
str
:
        
"
"
"
        
Return
the
Package
URL
"
purl
"
string
.
        
Returns
        
-
-
-
-
-
-
-
        
str
        
"
"
"
        
try
:
            
package_url
=
self
.
get_package_url
(
)
        
except
ValueError
:
            
return
"
"
        
return
str
(
package_url
)
    
def
get_package_url
(
self
)
-
>
PackageURL
:
        
"
"
"
        
Get
the
PackageURL
instance
.
        
Returns
        
-
-
-
-
-
-
-
        
PackageURL
        
"
"
"
        
return
PackageURL
(
            
self
.
type
            
self
.
namespace
            
self
.
name
            
self
.
version
            
self
.
qualifiers
            
self
.
subpath
        
)
    
def
set_package_url
(
self
package_url
:
PackageURL
)
-
>
None
:
        
"
"
"
        
Set
or
update
the
PackageURL
object
attributes
.
        
Parameters
        
-
-
-
-
-
-
-
-
-
-
        
package_url
:
PackageURL
            
The
PackageURL
object
to
set
get
attributes
from
.
        
"
"
"
        
if
not
isinstance
(
package_url
PackageURL
)
:
            
package_url
=
PackageURL
.
from_string
(
package_url
)
        
package_url_dict
=
package_url
.
to_dict
(
encode
=
True
empty
=
"
"
)
        
for
key
value
in
package_url_dict
.
items
(
)
:
            
setattr
(
self
key
value
)
