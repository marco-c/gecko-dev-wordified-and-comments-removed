import
concurrent
.
futures
import
pathlib
import
subprocess
import
sys
ARGS
=
sys
.
argv
SRC_PATH
=
pathlib
.
Path
(
ARGS
.
pop
(
)
)
assert
SRC_PATH
.
exists
(
)
"
gen_combos
.
py
[
-
-
flags
]
<
src
file
path
>
"
DIR
=
SRC_PATH
.
parent
def
cross_combine
(
*
args
)
:
    
args
=
list
(
args
)
    
def
cross_combine2
(
listA
listB
)
:
        
listC
=
[
]
        
for
a
in
listA
:
            
for
b
in
listB
:
                
c
=
dict
(
)
                
c
.
update
(
a
)
                
c
.
update
(
b
)
                
listC
.
append
(
c
)
        
return
listC
    
res
=
[
dict
(
)
]
    
while
True
:
        
try
:
            
next
=
args
.
pop
(
0
)
        
except
IndexError
:
            
break
        
res
=
cross_combine2
(
res
next
)
    
return
res
def
keyed_combiner
(
key
vals
)
:
    
res
=
[
]
    
for
v
in
vals
:
        
d
=
dict
(
)
        
d
[
key
]
=
v
        
res
.
append
(
d
)
    
return
res
def
eprint
(
*
args
*
*
kwargs
)
:
    
print
(
*
args
file
=
sys
.
stderr
*
*
kwargs
)
OGG
=
[
]
WEBM_CODECS
=
[
"
av1
"
"
vp9
"
]
if
"
-
-
all
"
in
ARGS
:
    
OGG
=
cross_combine
(
[
{
"
ext
"
:
"
ogg
"
}
]
keyed_combiner
(
"
vcodec
"
[
"
vp8
"
"
vp9
"
]
)
)
    
WEBM_CODECS
+
=
[
"
vp8
"
]
MP4
=
cross_combine
(
[
{
"
ext
"
:
"
mp4
"
}
]
keyed_combiner
(
"
vcodec
"
[
"
av1
"
"
h264
"
"
vp9
"
]
)
)
WEBM
=
cross_combine
(
[
{
"
ext
"
:
"
webm
"
}
]
keyed_combiner
(
"
vcodec
"
WEBM_CODECS
)
)
FORMAT_LIST
=
set
(
    
[
        
"
yuv420p
"
        
"
yuv420p10
"
        
"
gbrp
"
    
]
)
if
"
-
-
all
"
in
ARGS
:
    
FORMAT_LIST
|
=
set
(
        
[
            
"
yuv420p
"
            
"
yuv420p10
"
            
"
yuv420p12
"
            
"
yuv420p16be
"
            
"
yuv420p16le
"
            
"
yuv422p
"
            
"
yuv422p10
"
            
"
yuv422p12
"
            
"
yuv422p16be
"
            
"
yuv422p16le
"
            
"
yuv444p
"
            
"
yuv444p10
"
            
"
yuv444p12
"
            
"
yuv444p16be
"
            
"
yuv444p16le
"
            
"
yuv411p
"
            
"
yuv410p
"
            
"
yuyv422
"
            
"
uyvy422
"
            
"
rgb24
"
            
"
bgr24
"
            
"
rgb8
"
            
"
bgr8
"
            
"
rgb444be
"
            
"
rgb444le
"
            
"
bgr444be
"
            
"
bgr444le
"
            
"
gbrp
"
            
"
gbrp9be
"
            
"
gbrp9le
"
            
"
gbrp10be
"
            
"
gbrp10le
"
            
"
gbrp12be
"
            
"
gbrp12le
"
            
"
gbrp14be
"
            
"
gbrp14le
"
            
"
gbrp16be
"
            
"
gbrp16le
"
        
]
    
)
FORMATS
=
keyed_combiner
(
"
format
"
list
(
FORMAT_LIST
)
)
RANGE
=
keyed_combiner
(
"
range
"
[
"
tv
"
"
pc
"
]
)
CSPACE_LIST
=
set
(
    
[
        
"
bt709
"
    
]
)
if
"
-
-
all
"
in
ARGS
:
    
CSPACE_LIST
|
=
set
(
        
[
            
"
bt709
"
            
"
bt2020
"
            
"
bt601
-
6
-
525
"
            
"
bt601
-
6
-
625
"
        
]
    
)
CSPACE_LIST
=
list
(
CSPACE_LIST
)
COMBOS
=
cross_combine
(
    
WEBM
+
MP4
+
OGG
    
FORMATS
    
RANGE
    
keyed_combiner
(
"
src_cspace
"
CSPACE_LIST
)
    
keyed_combiner
(
"
dst_cspace
"
CSPACE_LIST
)
)
print
(
f
"
{
len
(
COMBOS
)
}
combinations
.
.
.
"
)
todo
=
[
]
for
c
in
COMBOS
:
    
dst_name
=
"
.
"
.
join
(
        
[
            
SRC_PATH
.
name
            
c
[
"
src_cspace
"
]
            
c
[
"
dst_cspace
"
]
            
c
[
"
range
"
]
            
c
[
"
format
"
]
            
c
[
"
vcodec
"
]
            
c
[
"
ext
"
]
        
]
    
)
    
src_cspace
=
c
[
"
src_cspace
"
]
    
vf
=
f
"
scale
=
out_range
=
{
c
[
'
range
'
]
}
"
    
vf
+
=
f
"
colorspace
=
all
=
{
c
[
'
dst_cspace
'
]
}
"
    
vf
+
=
f
"
:
iall
=
{
src_cspace
}
"
    
args
=
[
        
"
ffmpeg
"
        
"
-
y
"
        
"
-
color_primaries
"
        
src_cspace
        
"
-
color_trc
"
        
src_cspace
        
"
-
colorspace
"
        
src_cspace
        
"
-
i
"
        
SRC_PATH
.
as_posix
(
)
        
"
-
bitexact
"
        
"
-
vf
"
        
vf
        
"
-
pix_fmt
"
        
c
[
"
format
"
]
        
"
-
vcodec
"
        
c
[
"
vcodec
"
]
        
"
-
crf
"
        
"
1
"
        
(
DIR
/
dst_name
)
.
as_posix
(
)
    
]
    
if
"
-
v
"
in
ARGS
or
"
-
vv
"
in
ARGS
:
        
print
(
"
"
+
"
"
.
join
(
args
)
)
    
else
:
        
print
(
"
"
+
args
[
-
1
]
)
    
todo
.
append
(
args
)
with
open
(
DIR
/
"
reftest
.
list
"
)
as
f
:
    
reftest_list_text
=
f
.
read
(
)
for
args
in
todo
:
    
vid_name
=
pathlib
.
Path
(
args
[
-
1
]
)
.
name
    
if
vid_name
not
in
reftest_list_text
:
        
print
(
f
"
WARNING
:
Not
in
reftest
.
list
:
{
vid_name
}
"
)
if
"
-
-
write
"
not
in
ARGS
:
    
print
(
"
Use
-
-
write
to
write
.
Exiting
.
.
.
"
)
    
sys
.
exit
(
0
)
def
run_cmd
(
args
)
:
    
dest
=
None
    
if
"
-
vv
"
not
in
ARGS
:
        
dest
=
subprocess
.
DEVNULL
    
try
:
        
subprocess
.
run
(
args
check
=
True
stderr
=
dest
)
    
except
FileNotFoundError
:
        
print
(
"
FileNotFoundError
is
ffmpeg
not
in
your
PATH
?
"
)
        
raise
with
concurrent
.
futures
.
ThreadPoolExecutor
(
)
as
pool
:
    
fs
=
[
]
    
for
cur_args
in
todo
:
        
f
=
pool
.
submit
(
run_cmd
cur_args
)
        
fs
.
append
(
f
)
    
done
=
0
    
for
f
in
concurrent
.
futures
.
as_completed
(
fs
)
:
        
f
.
result
(
)
        
done
+
=
1
        
sys
.
stdout
.
write
(
f
"
\
rEncoded
{
done
}
/
{
len
(
todo
)
}
"
)
