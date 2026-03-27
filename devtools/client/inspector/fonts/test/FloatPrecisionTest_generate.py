"
"
"
Generate
FloatPrecisionTest
.
ttf
a
minimal
variable
font
with
unusual
floating
point
precision
on
all
axes
to
test
font
variation
axis
rounding
behavior
.
Run
this
script
with
:
>
.
/
mach
python
-
m
pip
install
fonttools
>
.
/
mach
python
devtools
/
client
/
inspector
/
fonts
/
test
/
FloatPrecisionTest_generate
.
py
"
"
"
import
os
import
shutil
from
fontTools
.
designspaceLib
import
(
    
AxisDescriptor
    
DesignSpaceDocument
    
InstanceDescriptor
    
SourceDescriptor
)
from
fontTools
.
fontBuilder
import
FontBuilder
from
fontTools
.
pens
.
ttGlyphPen
import
TTGlyphPen
from
fontTools
.
varLib
import
build
as
varLib_build
FAMILY_NAME
=
"
FloatPrecisionTest
"
def
create_base_font
(
name
width
=
600
)
:
    
"
"
"
Create
a
simple
base
font
with
minimal
glyph
set
.
    
This
creates
a
"
master
"
font
that
will
be
used
as
one
of
the
sources
    
for
building
a
variable
font
.
The
width
parameter
allows
us
to
create
    
different
masters
with
different
glyph
widths
.
    
"
"
"
    
fb
=
FontBuilder
(
unitsPerEm
=
1000
isTTF
=
True
)
    
fb
.
setupNameTable
(
{
        
"
familyName
"
:
FAMILY_NAME
        
"
styleName
"
:
name
    
}
)
    
glyphOrder
=
[
"
.
notdef
"
"
A
"
]
    
def
draw_notdef
(
pen
)
:
        
pen
.
moveTo
(
(
50
0
)
)
        
pen
.
lineTo
(
(
50
700
)
)
        
pen
.
lineTo
(
(
450
700
)
)
        
pen
.
lineTo
(
(
450
0
)
)
        
pen
.
closePath
(
)
    
def
draw_A
(
pen
)
:
        
pen
.
moveTo
(
(
100
0
)
)
        
pen
.
lineTo
(
(
100
700
)
)
        
pen
.
lineTo
(
(
width
-
100
700
)
)
        
pen
.
lineTo
(
(
width
-
100
0
)
)
        
pen
.
closePath
(
)
    
fb
.
setupGlyphOrder
(
glyphOrder
)
    
fb
.
setupCharacterMap
(
{
ord
(
"
A
"
)
:
"
A
"
}
)
    
pen
=
TTGlyphPen
(
None
)
    
draw_notdef
(
pen
)
    
notdef_glyph
=
pen
.
glyph
(
)
    
pen
=
TTGlyphPen
(
None
)
    
draw_A
(
pen
)
    
a_glyph
=
pen
.
glyph
(
)
    
fb
.
setupGlyf
(
{
"
.
notdef
"
:
notdef_glyph
"
A
"
:
a_glyph
}
)
    
fb
.
setupHorizontalMetrics
(
{
        
"
.
notdef
"
:
(
500
50
)
        
"
A
"
:
(
width
100
)
    
}
)
    
fb
.
setupHorizontalHeader
(
ascent
=
800
descent
=
-
200
)
    
fb
.
setupOS2
(
        
sTypoAscender
=
800
sTypoDescender
=
-
200
usWinAscent
=
800
usWinDescent
=
200
    
)
    
fb
.
setupPost
(
)
    
fb
.
setupHead
(
)
    
return
fb
.
font
def
create_precision_test_font
(
)
:
    
"
"
"
Create
variable
font
with
floating
point
precision
issues
.
    
This
function
generates
a
variable
font
specifically
designed
to
test
    
how
the
font
inspector
handles
unusual
floating
point
precision
in
    
font
variation
axes
.
The
axis
values
have
many
decimal
places
that
    
can
expose
rounding
errors
or
precision
issues
in
the
UI
.
    
"
"
"
    
AXIS_VALUES
=
{
        
"
Weight
"
:
{
            
"
minimum
"
:
300
.
3333282470703
            
"
default
"
:
400
.
6666717529297
            
"
maximum
"
:
699
.
4444580078125
        
}
        
"
Width
"
:
{
            
"
minimum
"
:
62
.
142856597900391
            
"
default
"
:
87
.
555557250976562
            
"
maximum
"
:
137
.
77777099609375
        
}
        
"
Slant
"
:
{
            
"
minimum
"
:
-
12
.
345678329467773
            
"
default
"
:
-
0
.
111111111111111
            
"
maximum
"
:
5
.
432109832763672
        
}
        
"
Optical
Size
"
:
{
            
"
minimum
"
:
8
.
888888359069824
            
"
default
"
:
14
.
285714149475098
            
"
maximum
"
:
96
.
969696044921875
        
}
    
}
    
AXES
=
[
        
(
"
Weight
"
"
wght
"
)
        
(
"
Width
"
"
wdth
"
)
        
(
"
Slant
"
"
slnt
"
)
        
(
"
Optical
Size
"
"
opsz
"
)
    
]
    
SOURCES
=
[
        
(
"
Light
"
"
minimum
"
400
)
        
(
"
Regular
"
"
default
"
600
)
        
(
"
Bold
"
"
maximum
"
800
)
    
]
    
INSTANCES
=
[
        
(
"
Regular
"
"
default
"
)
        
(
"
Bold
"
"
maximum
"
)
    
]
    
script_dir
=
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
abspath
(
__file__
)
)
    
tmp_masters
=
os
.
path
.
join
(
script_dir
"
tmp_masters
"
)
    
os
.
makedirs
(
tmp_masters
exist_ok
=
True
)
    
for
source_name
_
width
in
SOURCES
:
        
font
=
create_base_font
(
source_name
width
=
width
)
        
font
.
save
(
os
.
path
.
join
(
tmp_masters
f
"
{
source_name
}
.
ttf
"
)
)
    
doc
=
DesignSpaceDocument
(
)
    
for
axis_name
axis_tag
in
AXES
:
        
axis
=
AxisDescriptor
(
)
        
axis
.
name
=
axis_name
        
axis
.
tag
=
axis_tag
        
axis
.
minimum
=
AXIS_VALUES
[
axis_name
]
[
"
minimum
"
]
        
axis
.
default
=
AXIS_VALUES
[
axis_name
]
[
"
default
"
]
        
axis
.
maximum
=
AXIS_VALUES
[
axis_name
]
[
"
maximum
"
]
        
doc
.
addAxis
(
axis
)
    
for
source_name
location_type
_
in
SOURCES
:
        
source
=
SourceDescriptor
(
)
        
source
.
path
=
os
.
path
.
join
(
tmp_masters
f
"
{
source_name
}
.
ttf
"
)
        
source
.
familyName
=
FAMILY_NAME
        
source
.
styleName
=
source_name
        
source
.
location
=
{
            
axis_name
:
AXIS_VALUES
[
axis_name
]
[
location_type
]
            
for
axis_name
in
AXIS_VALUES
        
}
        
doc
.
addSource
(
source
)
    
for
instance_name
location_type
in
INSTANCES
:
        
instance
=
InstanceDescriptor
(
)
        
instance
.
familyName
=
FAMILY_NAME
        
instance
.
styleName
=
instance_name
        
instance
.
location
=
{
            
axis_name
:
AXIS_VALUES
[
axis_name
]
[
location_type
]
            
for
axis_name
in
AXIS_VALUES
        
}
        
doc
.
addInstance
(
instance
)
    
output_path
=
os
.
path
.
join
(
script_dir
"
FloatPrecisionTest
.
ttf
"
)
    
varfont
_
_
=
varLib_build
(
doc
)
    
varfont
.
save
(
output_path
)
    
shutil
.
rmtree
(
tmp_masters
)
    
print
(
f
"
Created
:
{
output_path
}
"
)
if
__name__
=
=
"
__main__
"
:
    
create_precision_test_font
(
)
