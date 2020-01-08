def
_assign_slots
(
obj
args
)
:
    
for
i
attr
in
enumerate
(
obj
.
__slots__
)
:
        
setattr
(
obj
attr
args
[
i
]
)
class
Longhand
(
object
)
:
    
__slots__
=
[
"
name
"
"
method
"
"
id
"
"
flags
"
"
pref
"
]
    
def
__init__
(
self
*
args
)
:
        
_assign_slots
(
self
args
)
    
staticmethod
    
def
type
(
)
:
        
return
"
longhand
"
class
Shorthand
(
object
)
:
    
__slots__
=
[
"
name
"
"
method
"
"
id
"
"
flags
"
"
pref
"
"
subprops
"
]
    
def
__init__
(
self
*
args
)
:
        
_assign_slots
(
self
args
)
    
staticmethod
    
def
type
(
)
:
        
return
"
shorthand
"
class
Alias
(
object
)
:
    
__slots__
=
[
"
name
"
"
method
"
"
alias_id
"
"
prop_id
"
"
flags
"
"
pref
"
]
    
def
__init__
(
self
*
args
)
:
        
_assign_slots
(
self
args
)
    
staticmethod
    
def
type
(
)
:
        
return
"
alias
"
<
%
!
def
order_key
(
prop
)
:
    
if
prop
.
name
.
startswith
(
"
-
"
)
:
        
return
prop
.
name
[
prop
.
name
.
find
(
"
-
"
1
)
+
1
:
]
    
return
prop
.
name
def
is_internal
(
prop
)
:
    
if
not
prop
.
gecko_pref
and
not
prop
.
enabled_in_content
(
)
:
        
return
True
    
OTHER_INTERNALS
=
[
        
"
-
moz
-
context
-
properties
"
        
"
-
moz
-
control
-
character
-
visibility
"
    
]
    
return
prop
.
name
in
OTHER_INTERNALS
def
method
(
prop
)
:
    
if
prop
.
name
=
=
"
float
"
:
        
return
"
CssFloat
"
    
if
prop
.
name
.
startswith
(
"
-
x
-
"
)
:
        
return
prop
.
camel_case
[
1
:
]
    
return
prop
.
camel_case
SERIALIZED_PREDEFINED_TYPES
=
[
    
"
Appearance
"
    
"
Clear
"
    
"
Color
"
    
"
Content
"
    
"
CounterIncrement
"
    
"
CounterReset
"
    
"
Float
"
    
"
FontFamily
"
    
"
FontFeatureSettings
"
    
"
FontLanguageOverride
"
    
"
FontSize
"
    
"
FontSizeAdjust
"
    
"
FontStretch
"
    
"
FontStyle
"
    
"
FontSynthesis
"
    
"
FontVariant
"
    
"
FontVariantAlternates
"
    
"
FontVariantEastAsian
"
    
"
FontVariantLigatures
"
    
"
FontVariantNumeric
"
    
"
FontVariationSettings
"
    
"
FontWeight
"
    
"
Integer
"
    
"
Length
"
    
"
LengthOrPercentage
"
    
"
NonNegativeLength
"
    
"
NonNegativeLengthOrPercentage
"
    
"
ListStyleType
"
    
"
Opacity
"
    
"
url
:
:
ImageUrlOrNone
"
]
def
serialized_by_servo
(
prop
)
:
    
if
"
GETCS_NEEDS_LAYOUT_FLUSH
"
in
prop
.
flags
:
        
return
False
    
if
prop
.
type
(
)
=
=
"
shorthand
"
:
        
return
False
    
if
prop
.
keyword
and
prop
.
name
!
=
"
-
moz
-
osx
-
font
-
smoothing
"
:
        
return
True
    
if
prop
.
predefined_type
in
SERIALIZED_PREDEFINED_TYPES
:
        
return
True
    
return
False
def
exposed_on_getcs
(
prop
)
:
    
if
prop
.
type
(
)
=
=
"
longhand
"
:
        
return
not
is_internal
(
prop
)
    
if
prop
.
type
(
)
=
=
"
shorthand
"
:
        
return
"
SHORTHAND_IN_GETCS
"
in
prop
.
flags
def
flags
(
prop
)
:
    
result
=
[
]
    
if
prop
.
explicitly_enabled_in_chrome
(
)
:
        
result
.
append
(
"
EnabledInUASheetsAndChrome
"
)
    
elif
prop
.
explicitly_enabled_in_ua_sheets
(
)
:
        
result
.
append
(
"
EnabledInUASheets
"
)
    
if
is_internal
(
prop
)
:
        
result
.
append
(
"
Internal
"
)
    
if
prop
.
enabled_in
=
=
"
"
:
        
result
.
append
(
"
Inaccessible
"
)
    
if
"
GETCS_NEEDS_LAYOUT_FLUSH
"
in
prop
.
flags
:
        
result
.
append
(
"
GetCSNeedsLayoutFlush
"
)
    
if
"
CAN_ANIMATE_ON_COMPOSITOR
"
in
prop
.
flags
:
        
result
.
append
(
"
CanAnimateOnCompositor
"
)
    
if
exposed_on_getcs
(
prop
)
:
        
result
.
append
(
"
ExposedOnGetCS
"
)
    
if
serialized_by_servo
(
prop
)
:
        
result
.
append
(
"
SerializedByServo
"
)
    
if
prop
.
type
(
)
=
=
"
longhand
"
and
prop
.
logical
:
        
result
.
append
(
"
IsLogical
"
)
    
return
"
"
.
join
(
'
"
{
}
"
'
.
format
(
flag
)
for
flag
in
result
)
def
pref
(
prop
)
:
    
if
prop
.
gecko_pref
:
        
return
'
"
'
+
prop
.
gecko_pref
+
'
"
'
    
return
'
"
"
'
def
sub_properties
(
prop
)
:
    
return
"
"
.
join
(
'
"
{
}
"
'
.
format
(
p
.
ident
)
for
p
in
prop
.
sub_properties
)
%
>
data
=
[
    
%
for
prop
in
sorted
(
data
.
longhands
key
=
order_key
)
:
    
Longhand
(
"
{
prop
.
name
}
"
"
{
method
(
prop
)
}
"
"
{
prop
.
ident
}
"
[
{
flags
(
prop
)
}
]
{
pref
(
prop
)
}
)
    
%
endfor
    
%
for
prop
in
sorted
(
data
.
shorthands
key
=
order_key
)
:
    
Shorthand
(
"
{
prop
.
name
}
"
"
{
prop
.
camel_case
}
"
"
{
prop
.
ident
}
"
[
{
flags
(
prop
)
}
]
{
pref
(
prop
)
}
              
[
{
sub_properties
(
prop
)
}
]
)
    
%
endfor
    
%
for
prop
in
sorted
(
data
.
all_aliases
(
)
key
=
lambda
x
:
x
.
name
)
:
    
Alias
(
"
{
prop
.
name
}
"
"
{
prop
.
camel_case
}
"
"
{
prop
.
ident
}
"
"
{
prop
.
original
.
ident
}
"
[
]
{
pref
(
prop
)
}
)
    
%
endfor
]
