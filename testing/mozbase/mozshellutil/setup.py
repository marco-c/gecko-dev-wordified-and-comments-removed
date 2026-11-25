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
setup
(
    
name
=
"
mozshellutil
"
    
version
=
PACKAGE_VERSION
    
description
=
"
Shell
command
line
parsing
utilities
for
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
:
:
Only
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
mozshellutil
"
]
    
include_package_data
=
True
    
zip_safe
=
False
    
python_requires
=
"
>
=
3
.
9
"
)
