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
        
"
-
moz
-
window
-
opacity
"
        
"
-
moz
-
window
-
transform
"
        
"
-
moz
-
window
-
transform
-
origin
"
    
]
    
return
prop
.
name
in
OTHER_INTERNALS
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
CSS_PROPERTY_ENABLED_IN_UA_SHEETS_AND_CHROME
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
CSS_PROPERTY_ENABLED_IN_UA_SHEETS
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
CSS_PROPERTY_INTERNAL
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
CSS_PROPERTY_PARSE_INACCESSIBLE
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
CSS_PROPERTY_GETCS_NEEDS_LAYOUT_FLUSH
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
CSS_PROPERTY_CAN_ANIMATE_ON_COMPOSITOR
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
%
>
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
    
(
        
"
{
prop
.
name
}
"
        
%
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
        
"
CssFloat
"
        
%
elif
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
        
"
{
prop
.
camel_case
[
1
:
]
}
"
        
%
else
:
        
"
{
prop
.
camel_case
}
"
        
%
endif
        
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
        
"
longhand
"
    
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
        
"
shorthand
"
    
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
        
(
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
)
        
[
]
        
{
pref
(
prop
)
}
        
"
alias
"
    
)
    
%
endfor
]
