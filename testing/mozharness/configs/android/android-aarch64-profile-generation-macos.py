config
=
{
    
"
emulator_avd_name
"
:
"
mozemulator
-
arm64
"
    
"
emulator_process_name
"
:
"
qemu
-
system
-
aarch64
"
    
"
emulator_extra_args
"
:
[
        
"
-
gpu
"
        
"
swiftshader_indirect
"
        
"
-
skip
-
adb
-
auth
"
        
"
-
verbose
"
        
"
-
show
-
kernel
"
        
"
-
ranchu
"
        
"
-
selinux
"
        
"
permissive
"
        
"
-
memory
"
        
"
4096
"
        
"
-
cores
"
        
"
4
"
        
"
-
skin
"
        
"
1080x1920
"
        
"
-
no
-
snapstorage
"
        
"
-
no
-
snapshot
"
        
"
-
prop
"
        
"
ro
.
test_harness
=
true
"
    
]
    
"
exes
"
:
{
        
"
adb
"
:
"
%
(
abs_sdk_dir
)
s
/
platform
-
tools
/
adb
"
    
}
    
"
env
"
:
{
        
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
:
%
(
abs_sdk_dir
)
s
/
emulator
:
%
(
abs_sdk_dir
)
s
/
tools
:
%
(
abs_sdk_dir
)
s
/
tools
/
bin
:
%
(
abs_sdk_dir
)
s
/
platform
-
tools
"
    
}
    
"
bogomips_minimum
"
:
0
    
"
android_version
"
:
34
    
"
os_version
"
:
"
14
"
    
"
is_emulator
"
:
True
}
