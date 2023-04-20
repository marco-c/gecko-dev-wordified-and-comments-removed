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
"
mozinfo
"
"
mozlog
>
=
6
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
    
install_requires
=
deps
    
entry_points
=
{
        
"
console_scripts
"
:
[
            
"
mozproxy
=
mozproxy
.
driver
:
main
"
        
]
    
}
    
include_package_data
=
True
    
zip_safe
=
False
)
