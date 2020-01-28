config
=
{
    
"
exes
"
:
{
}
    
"
env
"
:
{
        
"
DISPLAY
"
:
"
:
0
.
0
"
        
"
PATH
"
:
"
%
(
PATH
)
s
"
        
"
MINIDUMP_SAVEPATH
"
:
"
%
(
abs_work_dir
)
s
/
.
.
/
minidumps
"
    
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
verify
-
device
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
tooltool_cache
"
:
"
/
builds
/
tooltool_cache
"
    
"
download_tooltool
"
:
True
    
"
xpcshell_extra
"
:
"
-
-
remoteTestRoot
=
/
data
/
local
/
tests
"
}
