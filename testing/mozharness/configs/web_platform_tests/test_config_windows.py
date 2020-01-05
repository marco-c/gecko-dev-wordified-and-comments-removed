import
os
import
sys
config
=
{
    
"
exes
"
:
{
        
'
python
'
:
sys
.
executable
        
'
virtualenv
'
:
[
sys
.
executable
'
c
:
/
mozilla
-
source
/
cedar
/
python
/
virtualenv
/
virtualenv
.
py
'
]
        
'
hg
'
:
'
c
:
/
mozilla
-
build
/
hg
/
hg
'
        
'
mozinstall
'
:
[
'
%
s
/
build
/
venv
/
scripts
/
python
'
%
os
.
getcwd
(
)
                       
'
%
s
/
build
/
venv
/
scripts
/
mozinstall
-
script
.
py
'
%
os
.
getcwd
(
)
]
    
}
    
"
default_actions
"
:
[
        
'
clobber
'
        
'
download
-
and
-
extract
'
        
'
create
-
virtualenv
'
        
'
pull
'
        
'
install
'
        
'
run
-
tests
'
    
]
    
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
    
"
pip_index
"
:
False
}
