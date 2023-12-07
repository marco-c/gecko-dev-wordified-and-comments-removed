from
setuptools
import
find_packages
setup
entry_points
=
"
"
"
      
[
console_scripts
]
      
cp
-
creator
=
condprof
.
main
:
main
      
cp
-
client
=
condprof
.
client
:
main
      
"
"
"
setup
(
    
name
=
"
conditioned
-
profile
"
    
version
=
"
0
.
2
"
    
packages
=
find_packages
(
)
    
description
=
"
Firefox
Heavy
Profile
creator
"
    
include_package_data
=
True
    
data_files
=
[
        
(
            
"
condprof
"
            
[
                
"
condprof
/
customization
/
default
.
json
"
                
"
condprof
/
customization
/
youtube
.
json
"
                
"
condprof
/
customization
/
webext
.
json
"
            
]
        
)
    
]
    
zip_safe
=
False
    
install_requires
=
[
]
    
entry_points
=
entry_points
)
