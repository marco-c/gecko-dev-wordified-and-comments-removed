from
__future__
import
absolute_import
from
setuptools
import
setup
find_packages
import
sys
version
=
'
0
.
6
'
deps
=
[
'
httplib2
=
=
0
.
9
.
2
'
        
'
mozfile
>
=
1
.
2
'
        
'
mozhttpd
=
=
0
.
7
'
        
'
mozinfo
>
=
0
.
10
'
        
'
mozinstall
=
=
1
.
16
'
        
'
mozprocess
=
=
0
.
26
'
        
'
mozprofile
~
=
2
.
1
'
        
'
mozrunner
~
=
7
.
2
'
        
'
mozversion
=
=
1
.
5
'
        
]
assert
sys
.
version_info
[
0
]
=
=
2
assert
sys
.
version_info
[
1
]
>
=
6
setup
(
name
=
'
tps
'
      
version
=
version
      
description
=
'
run
automated
multi
-
profile
sync
tests
'
      
long_description
=
"
"
"
\
"
"
"
      
classifiers
=
[
'
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
'
                   
'
Programming
Language
:
:
Python
:
:
2
:
:
Only
'
                   
]
      
keywords
=
'
'
      
author
=
'
Mozilla
Automation
and
Tools
team
'
      
author_email
=
'
tools
lists
.
mozilla
.
org
'
      
url
=
'
https
:
/
/
developer
.
mozilla
.
org
/
en
-
US
/
docs
/
TPS
'
      
license
=
'
MPL
2
.
0
'
      
packages
=
find_packages
(
exclude
=
[
'
ez_setup
'
'
examples
'
'
tests
'
]
)
      
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
      
runtps
=
tps
.
cli
:
main
      
"
"
"
      
data_files
=
[
        
(
'
tps
'
[
'
config
/
config
.
json
.
in
'
]
)
      
]
      
)
