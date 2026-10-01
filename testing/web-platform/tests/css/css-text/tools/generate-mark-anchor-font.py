import
io
import
os
from
fontTools
.
fontBuilder
import
FontBuilder
from
fontTools
.
feaLib
.
builder
import
addOpenTypeFeatures
from
fontTools
.
pens
.
ttGlyphPen
import
TTGlyphPen
EM
=
1000
ASCENT
=
800
DESCENT
=
200
BOTTOM_BAR
=
(
0
200
)
MID_BAR
=
(
250
450
)
TOP_BAR
=
(
500
700
)
BASE_ANCHOR_X
=
0
FAMILY
=
"
mark
-
anchor
-
test
"
FEATURES
=
"
"
"
languagesystem
DFLT
dflt
;
languagesystem
latn
dflt
;
languagesystem
hebr
dflt
;
markClass
[
midbar
topbar
]
<
anchor
0
0
>
MARKS
;
feature
mark
{
    
pos
base
[
bottombar
space
]
<
anchor
%
d
0
>
mark
MARKS
;
}
mark
;
"
"
"
%
BASE_ANCHOR_X
def
bars
(
*
y_ranges
)
:
    
pen
=
TTGlyphPen
(
None
)
    
for
y_min
y_max
in
y_ranges
:
        
pen
.
moveTo
(
(
0
y_min
)
)
        
pen
.
lineTo
(
(
0
y_max
)
)
        
pen
.
lineTo
(
(
EM
y_max
)
)
        
pen
.
lineTo
(
(
EM
y_min
)
)
        
pen
.
closePath
(
)
    
return
pen
.
glyph
(
)
def
empty
(
)
:
    
return
TTGlyphPen
(
None
)
.
glyph
(
)
def
main
(
)
:
    
glyph_order
=
[
"
.
notdef
"
"
space
"
"
bottombar
"
"
midbar
"
"
topbar
"
                   
"
twobars
"
"
threebars
"
"
midbaronly
"
]
    
glyphs
=
{
        
"
.
notdef
"
:
empty
(
)
        
"
space
"
:
empty
(
)
        
"
bottombar
"
:
bars
(
BOTTOM_BAR
)
        
"
midbar
"
:
bars
(
MID_BAR
)
        
"
topbar
"
:
bars
(
TOP_BAR
)
        
"
twobars
"
:
bars
(
BOTTOM_BAR
MID_BAR
)
        
"
threebars
"
:
bars
(
BOTTOM_BAR
MID_BAR
TOP_BAR
)
        
"
midbaronly
"
:
bars
(
MID_BAR
)
    
}
    
metrics
=
{
        
"
.
notdef
"
:
(
EM
0
)
        
"
space
"
:
(
EM
0
)
        
"
bottombar
"
:
(
EM
0
)
        
"
midbar
"
:
(
0
0
)
        
"
topbar
"
:
(
0
0
)
        
"
twobars
"
:
(
EM
0
)
        
"
threebars
"
:
(
EM
0
)
        
"
midbaronly
"
:
(
EM
0
)
    
}
    
cmap
=
{
        
0x0020
:
"
space
"
        
0x0041
:
"
bottombar
"
        
0x0042
:
"
twobars
"
        
0x0043
:
"
threebars
"
        
0x0044
:
"
midbaronly
"
        
0x0300
:
"
topbar
"
        
0x0301
:
"
midbar
"
        
0x05D0
:
"
bottombar
"
        
0x05D1
:
"
twobars
"
        
0x05D2
:
"
threebars
"
        
0x05D3
:
"
midbaronly
"
    
}
    
fb
=
FontBuilder
(
EM
isTTF
=
True
)
    
fb
.
setupGlyphOrder
(
glyph_order
)
    
fb
.
setupCharacterMap
(
cmap
)
    
fb
.
setupGlyf
(
glyphs
)
    
fb
.
setupHorizontalMetrics
(
metrics
)
    
fb
.
setupHorizontalHeader
(
ascent
=
ASCENT
descent
=
-
DESCENT
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
FAMILY
        
"
styleName
"
:
"
Regular
"
        
"
uniqueFontIdentifier
"
:
"
%
s
;
Regular
;
web
-
platform
-
tests
"
%
FAMILY
        
"
fullName
"
:
FAMILY
        
"
version
"
:
"
1
.
000
"
        
"
psName
"
:
"
mark
-
anchor
-
test
-
Regular
"
        
"
manufacturer
"
:
"
web
-
platform
-
tests
"
        
"
licenseDescription
"
:
            
"
Generated
for
web
-
platform
-
tests
by
"
            
"
css
/
css
-
text
/
tools
/
generate
-
mark
-
anchor
-
font
.
py
.
"
            
"
Available
under
the
W3C
3
-
clause
BSD
license
.
"
    
}
)
    
fb
.
setupOS2
(
        
sTypoAscender
=
ASCENT
        
sTypoDescender
=
-
DESCENT
        
sTypoLineGap
=
0
        
usWinAscent
=
ASCENT
        
usWinDescent
=
DESCENT
        
sxHeight
=
TOP_BAR
[
1
]
        
sCapHeight
=
TOP_BAR
[
1
]
        
achVendID
=
"
NONE
"
        
fsType
=
0
    
)
    
fb
.
setupPost
(
isFixedPitch
=
0
)
    
addOpenTypeFeatures
(
fb
.
font
io
.
StringIO
(
FEATURES
)
)
    
out_dir
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
os
.
path
.
abspath
(
__file__
)
)
"
.
.
"
"
.
.
"
"
.
.
"
"
fonts
"
)
    
out
=
os
.
path
.
normpath
(
os
.
path
.
join
(
out_dir
"
%
s
.
ttf
"
%
FAMILY
)
)
    
fb
.
save
(
out
)
    
print
(
"
Wrote
%
s
"
%
out
)
if
__name__
=
=
"
__main__
"
:
    
main
(
)
