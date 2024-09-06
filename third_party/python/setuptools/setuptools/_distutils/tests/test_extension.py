"
"
"
Tests
for
distutils
.
extension
.
"
"
"
import
os
import
pathlib
import
warnings
from
distutils
.
extension
import
Extension
read_setup_file
import
pytest
from
.
compat
.
py38
import
check_warnings
class
TestExtension
:
    
def
test_read_setup_file
(
self
)
:
        
setup
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
dirname
(
__file__
)
'
Setup
.
sample
'
)
        
exts
=
read_setup_file
(
setup
)
        
names
=
[
ext
.
name
for
ext
in
exts
]
        
names
.
sort
(
)
        
wanted
=
[
            
'
_arraysurfarray
'
            
'
_camera
'
            
'
_numericsndarray
'
            
'
_numericsurfarray
'
            
'
base
'
            
'
bufferproxy
'
            
'
cdrom
'
            
'
color
'
            
'
constants
'
            
'
display
'
            
'
draw
'
            
'
event
'
            
'
fastevent
'
            
'
font
'
            
'
gfxdraw
'
            
'
image
'
            
'
imageext
'
            
'
joystick
'
            
'
key
'
            
'
mask
'
            
'
mixer
'
            
'
mixer_music
'
            
'
mouse
'
            
'
movie
'
            
'
overlay
'
            
'
pixelarray
'
            
'
pypm
'
            
'
rect
'
            
'
rwobject
'
            
'
scrap
'
            
'
surface
'
            
'
surflock
'
            
'
time
'
            
'
transform
'
        
]
        
assert
names
=
=
wanted
    
def
test_extension_init
(
self
)
:
        
with
pytest
.
raises
(
AssertionError
)
:
            
Extension
(
1
[
]
)
        
ext
=
Extension
(
'
name
'
[
]
)
        
assert
ext
.
name
=
=
'
name
'
        
with
pytest
.
raises
(
AssertionError
)
:
            
Extension
(
'
name
'
'
file
'
)
        
with
pytest
.
raises
(
AssertionError
)
:
            
Extension
(
'
name
'
[
'
file
'
1
]
)
        
ext
=
Extension
(
'
name
'
[
'
file1
'
'
file2
'
]
)
        
assert
ext
.
sources
=
=
[
'
file1
'
'
file2
'
]
        
ext
=
Extension
(
'
name
'
[
pathlib
.
Path
(
'
file1
'
)
pathlib
.
Path
(
'
file2
'
)
]
)
        
assert
ext
.
sources
=
=
[
'
file1
'
'
file2
'
]
        
for
attr
in
(
            
'
include_dirs
'
            
'
define_macros
'
            
'
undef_macros
'
            
'
library_dirs
'
            
'
libraries
'
            
'
runtime_library_dirs
'
            
'
extra_objects
'
            
'
extra_compile_args
'
            
'
extra_link_args
'
            
'
export_symbols
'
            
'
swig_opts
'
            
'
depends
'
        
)
:
            
assert
getattr
(
ext
attr
)
=
=
[
]
        
assert
ext
.
language
is
None
        
assert
ext
.
optional
is
None
        
with
check_warnings
(
)
as
w
:
            
warnings
.
simplefilter
(
'
always
'
)
            
ext
=
Extension
(
'
name
'
[
'
file1
'
'
file2
'
]
chic
=
True
)
        
assert
len
(
w
.
warnings
)
=
=
1
        
assert
str
(
w
.
warnings
[
0
]
.
message
)
=
=
"
Unknown
Extension
options
:
'
chic
'
"
