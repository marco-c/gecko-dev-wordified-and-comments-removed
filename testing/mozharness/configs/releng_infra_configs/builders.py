from
mozharness
.
base
.
script
import
platform_name
PYTHON_WIN32
=
'
c
:
/
mozilla
-
build
/
python27
/
python
.
exe
'
PLATFORM_CONFIG
=
{
    
'
linux64
'
:
{
        
'
exes
'
:
{
            
'
gittool
.
py
'
:
'
/
usr
/
local
/
bin
/
gittool
.
py
'
        
}
        
'
env
'
:
{
            
'
DISPLAY
'
:
'
:
2
'
        
}
    
}
    
'
macosx
'
:
{
        
'
exes
'
:
{
            
'
gittool
.
py
'
:
'
/
usr
/
local
/
bin
/
gittool
.
py
'
        
}
    
}
    
'
win32
'
:
{
        
"
exes
"
:
{
            
'
gittool
.
py
'
:
[
PYTHON_WIN32
'
c
:
/
builds
/
hg
-
shared
/
build
/
tools
/
buildfarm
/
utils
/
gittool
.
py
'
]
            
'
python
'
:
PYTHON_WIN32
        
}
    
}
}
config
=
PLATFORM_CONFIG
[
platform_name
(
)
]
config
.
update
(
{
    
"
find_links
"
:
[
        
"
http
:
/
/
pypi
.
pvt
.
build
.
mozilla
.
org
/
pub
"
        
"
http
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
"
    
]
    
'
pip_index
'
:
False
    
'
virtualenv_path
'
:
'
venv
'
}
)
