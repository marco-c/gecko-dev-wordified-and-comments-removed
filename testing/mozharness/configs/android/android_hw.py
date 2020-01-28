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
minidump_stackwalk_path
"
:
"
linux64
-
minidump_stackwalk
"
    
"
minidump_tooltool_manifest_path
"
:
"
config
/
tooltool
-
manifests
/
linux64
/
releng
.
manifest
"
    
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
