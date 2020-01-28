from
__future__
import
absolute_import
from
setuptools
import
setup
PACKAGE_NAME
=
"
mozproxy
"
PACKAGE_VERSION
=
"
1
.
0
"
deps
=
[
"
redo
"
]
setup
(
    
name
=
PACKAGE_NAME
    
version
=
PACKAGE_VERSION
    
description
=
"
Proxy
for
playback
"
    
long_description
=
"
see
https
:
/
/
firefox
-
source
-
docs
.
mozilla
.
org
/
mozbase
/
index
.
html
"
    
classifiers
=
[
        
"
Programming
Language
:
:
Python
:
:
2
.
7
"
        
"
Programming
Language
:
:
Python
:
:
3
.
5
"
    
]
    
keywords
=
"
mozilla
"
    
author
=
"
Mozilla
Automation
and
Tools
team
"
    
author_email
=
"
tools
lists
.
mozilla
.
org
"
    
url
=
"
https
:
/
/
wiki
.
mozilla
.
org
/
Auto
-
tools
/
Projects
/
Mozbase
"
    
license
=
"
MPL
"
    
packages
=
[
"
mozproxy
"
]
    
include_package_data
=
True
    
zip_safe
=
False
    
install_requires
=
deps
)
