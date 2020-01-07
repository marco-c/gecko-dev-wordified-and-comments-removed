import
os
import
mozharness
from
mozharness
.
base
.
script
import
platform_name
external_tools_path
=
os
.
path
.
join
(
    
os
.
path
.
abspath
(
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
dirname
(
mozharness
.
__file__
)
)
)
    
'
external_tools
'
)
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
linux
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
os
.
path
.
join
(
external_tools_path
'
gittool
.
py
'
)
        
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
0
'
            
'
PATH
'
:
'
%
(
PATH
)
s
:
'
+
external_tools_path
        
}
    
}
    
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
os
.
path
.
join
(
external_tools_path
'
gittool
.
py
'
)
        
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
0
'
            
'
PATH
'
:
'
%
(
PATH
)
s
:
'
+
external_tools_path
        
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
os
.
path
.
join
(
external_tools_path
'
gittool
.
py
'
)
        
}
        
'
env
'
:
{
            
'
PATH
'
:
'
%
(
PATH
)
s
:
'
+
external_tools_path
        
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
os
.
path
.
join
(
external_tools_path
'
gittool
.
py
'
)
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
