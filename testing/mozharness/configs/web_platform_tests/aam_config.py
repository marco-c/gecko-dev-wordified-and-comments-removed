import
os
config
=
{
    
"
virtualenv_modules
"
:
[
        
"
PyGObject
;
sys_platform
=
=
'
linux
'
"
    
]
    
"
find_links
"
:
[
        
os
.
path
.
abspath
(
os
.
environ
.
get
(
"
MOZ_FETCHES_DIR
"
)
)
        
"
https
:
/
/
pypi
.
pub
.
build
.
mozilla
.
org
/
pub
/
"
    
]
}
