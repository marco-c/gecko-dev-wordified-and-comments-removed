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
mozperftest
"
PACKAGE_VERSION
=
"
0
.
2
"
deps
=
[
    
"
regex
"
    
"
jsonschema
"
    
"
mozlog
>
=
6
.
0
"
    
"
mozdevice
>
=
4
.
0
.
0
"
    
"
mozproxy
"
    
"
mozinfo
"
    
"
mozfile
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
Mozilla
'
s
mach
perftest
command
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
3
.
6
"
]
    
keywords
=
"
"
    
author
=
"
Mozilla
Performance
Test
Engineering
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
hg
.
mozilla
.
org
/
mozilla
-
central
/
file
/
tip
/
python
/
mozperftest
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
mozperftest
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
