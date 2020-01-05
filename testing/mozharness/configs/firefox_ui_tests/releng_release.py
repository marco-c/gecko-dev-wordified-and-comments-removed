import
os
import
sys
import
mozharness
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
config
=
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
[
            
sys
.
executable
            
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
    
}
    
'
find_links
'
:
[
'
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
'
]
    
'
pip_index
'
:
False
    
'
download_minidump_stackwalk
'
:
True
    
'
download_symbols
'
:
'
ondemand
'
    
'
download_tooltool
'
:
True
}
