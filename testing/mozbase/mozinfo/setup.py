from
__future__
import
absolute_import
from
setuptools
import
setup
PACKAGE_VERSION
=
"
1
.
0
.
0
"
deps
=
[
"
mozfile
>
=
0
.
12
"
]
setup
(
    
name
=
"
mozinfo
"
    
version
=
PACKAGE_VERSION
    
description
=
"
Library
to
get
system
information
for
use
in
Mozilla
testing
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
        
"
Development
Status
:
:
5
-
Production
/
Stable
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
Testing
Team
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
mozinfo
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
    
entry_points
=
"
"
"
      
#
-
*
-
Entry
points
:
-
*
-
      
[
console_scripts
]
      
mozinfo
=
mozinfo
:
main
      
"
"
"
)
