import
re
import
sys
def
GetDefaultTryConfigs
(
bots
=
None
)
:
  
"
"
"
Returns
a
list
of
(
'
bot
'
set
(
[
'
tests
'
]
)
optionally
filtered
by
[
bots
]
.
  
For
WebRTC
purposes
we
always
return
an
empty
list
of
tests
since
we
want
  
to
run
all
tests
by
default
on
all
our
trybots
.
  
"
"
"
  
return
{
'
tryserver
.
libyuv
'
:
dict
(
(
bot
[
]
)
for
bot
in
bots
)
}
def
GetPreferredTryMasters
(
project
change
)
:
  
files
=
change
.
LocalPaths
(
)
  
bots
=
[
    
'
win
'
    
'
win_rel
'
    
'
win_x64_rel
'
    
'
win_x64_gn
'
    
'
win_x64_gn_rel
'
    
'
win_clang
'
    
'
win_clang_rel
'
    
'
win_x64_clang_rel
'
    
'
mac
'
    
'
mac_rel
'
    
'
mac_gn
'
    
'
mac_gn_rel
'
    
'
mac_asan
'
    
'
ios
'
    
'
ios_rel
'
    
'
ios_arm64
'
    
'
ios_arm64_rel
'
    
'
linux
'
    
'
linux_rel
'
    
'
linux_gn
'
    
'
linux_gn_rel
'
    
'
linux_memcheck
'
    
'
linux_tsan2
'
    
'
linux_asan
'
    
'
linux_msan
'
    
'
linux_ubsan
'
    
'
linux_ubsan_vptr
'
    
'
android
'
    
'
android_rel
'
    
'
android_clang
'
    
'
android_arm64
'
    
'
android_mips
'
    
'
android_x64
'
    
'
android_x86
'
    
'
android_gn
'
    
'
android_gn_rel
'
  
]
  
if
not
files
or
all
(
re
.
search
(
r
'
[
\
\
/
]
OWNERS
'
f
)
for
f
in
files
)
:
    
return
{
}
  
return
GetDefaultTryConfigs
(
bots
)
