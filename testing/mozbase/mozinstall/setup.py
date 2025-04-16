import
os
from
setuptools
import
setup
try
:
    
here
=
os
.
path
.
dirname
(
os
.
path
.
abspath
(
__file__
)
)
    
description
=
open
(
os
.
path
.
join
(
here
"
README
.
md
"
)
)
.
read
(
)
except
OSError
:
    
description
=
None
PACKAGE_VERSION
=
"
2
.
1
.
0
"
deps
=
[
    
"
mozinfo
>
=
0
.
7
"
    
"
mozfile
>
=
1
.
0
"
    
"
requests
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
"
mozInstall
"
    
version
=
PACKAGE_VERSION
    
description
=
"
package
for
installing
and
uninstalling
Mozilla
applications
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
Environment
:
:
Console
"
        
"
Intended
Audience
:
:
Developers
"
        
"
License
:
:
OSI
Approved
:
:
Mozilla
Public
License
2
.
0
(
MPL
2
.
0
)
"
        
"
Natural
Language
:
:
English
"
        
"
Operating
System
:
:
OS
Independent
"
        
"
Topic
:
:
Software
Development
:
:
Libraries
:
:
Python
Modules
"
        
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
2
.
0
"
    
packages
=
[
"
mozinstall
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
      
mozinstall
=
mozinstall
:
install_cli
      
mozuninstall
=
mozinstall
:
uninstall_cli
      
moz_add_to_system
=
mozinstall
:
install_cli
      
moz_remove_from_system
=
mozinstall
:
uninstall_cli
      
"
"
"
)
