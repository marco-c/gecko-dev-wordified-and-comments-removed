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
android34
-
x86_64
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
x86_64
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
on
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
3072
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
800x1280
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
platform
-
tools
"
    
}
    
"
bogomips_minimum
"
:
3000
    
"
android_version
"
:
34
    
"
is_emulator
"
:
True
}
