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
manifestparser
"
PACKAGE_VERSION
=
"
2
.
1
.
0
"
DEPS
=
[
    
"
mozlog
>
=
6
.
0
"
    
"
six
>
=
1
.
13
.
0
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
Library
to
create
and
manage
test
manifests
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
    
]
    
keywords
=
"
mozilla
manifests
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
    
zip_safe
=
False
    
packages
=
[
"
manifestparser
"
]
    
install_requires
=
DEPS
    
entry_points
=
"
"
"
      
[
console_scripts
]
      
manifestparser
=
manifestparser
.
cli
:
main
      
"
"
"
)
