import
json
import
pytoml
import
re
import
sys
import
six
import
voluptuous
import
voluptuous
.
humanize
from
voluptuous
import
Schema
Optional
Any
All
Required
Length
Range
Msg
Match
Text
=
Any
(
six
.
text_type
six
.
binary_type
)
id_regex
=
re
.
compile
(
r
"
^
[
a
-
z0
-
9
-
]
+
"
)
feature_schema
=
Schema
(
    
{
        
Match
(
id_regex
)
:
{
            
Required
(
"
title
"
)
:
All
(
Text
Length
(
min
=
1
)
)
            
Required
(
"
description
"
)
:
All
(
Text
Length
(
min
=
1
)
)
            
Required
(
"
bug
-
numbers
"
)
:
All
(
Length
(
min
=
1
)
[
All
(
int
Range
(
min
=
1
)
)
]
)
            
Required
(
"
restart
-
required
"
)
:
bool
            
Required
(
"
type
"
)
:
"
boolean
"
            
Optional
(
"
preference
"
)
:
Text
            
Optional
(
"
default
-
value
"
)
:
Any
(
                
bool
dict
            
)
            
Optional
(
"
is
-
public
"
)
:
Any
(
bool
dict
)
            
Optional
(
"
description
-
links
"
)
:
dict
        
}
    
}
)
EXIT_OK
=
0
EXIT_ERROR
=
1
def
main
(
output
*
filenames
)
:
    
features
=
{
}
    
errors
=
False
    
try
:
        
features
=
process_files
(
filenames
)
        
json
.
dump
(
features
output
sort_keys
=
True
)
    
except
ExceptionGroup
as
error_group
:
        
print
(
str
(
error_group
)
)
        
return
EXIT_ERROR
    
return
EXIT_OK
class
ExceptionGroup
(
Exception
)
:
    
def
__init__
(
self
errors
)
:
        
self
.
errors
=
errors
    
def
__str__
(
self
)
:
        
rv
=
[
"
There
were
errors
while
processing
feature
definitions
:
"
]
        
for
error
in
self
.
errors
:
            
s
=
"
\
n
"
.
join
(
"
"
+
line
for
line
in
str
(
error
)
.
split
(
"
\
n
"
)
)
            
s
=
"
*
"
+
s
[
4
:
]
            
rv
.
append
(
s
)
        
return
"
\
n
"
.
join
(
rv
)
class
FeatureGateException
(
Exception
)
:
    
def
__init__
(
self
message
filename
=
None
)
:
        
super
(
FeatureGateException
self
)
.
__init__
(
message
)
        
self
.
filename
=
filename
    
def
__str__
(
self
)
:
        
message
=
super
(
FeatureGateException
self
)
.
__str__
(
)
        
rv
=
[
"
In
"
]
        
if
self
.
filename
is
None
:
            
rv
.
append
(
"
unknown
file
:
"
)
        
else
:
            
rv
.
append
(
'
file
"
{
}
"
:
'
.
format
(
self
.
filename
)
)
        
rv
.
append
(
message
)
        
return
"
"
.
join
(
rv
)
    
def
__repr__
(
self
)
:
        
original
=
super
(
FeatureGateException
self
)
.
__repr__
(
)
        
with_comma
=
original
[
:
-
1
]
        
if
len
(
with_comma
)
>
0
and
with_comma
[
-
1
]
!
=
"
"
:
            
with_comma
=
with_comma
+
"
"
        
return
with_comma
+
"
filename
=
{
!
r
}
)
"
.
format
(
self
.
filename
)
def
process_files
(
filenames
)
:
    
features
=
{
}
    
errors
=
[
]
    
for
filename
in
filenames
:
        
try
:
            
with
open
(
filename
"
r
"
)
as
f
:
                
feature_data
=
pytoml
.
load
(
f
)
            
voluptuous
.
humanize
.
validate_with_humanized_errors
(
                
feature_data
feature_schema
            
)
            
for
feature_id
feature
in
feature_data
.
items
(
)
:
                
feature
[
"
id
"
]
=
feature_id
                
features
[
feature_id
]
=
expand_feature
(
feature
)
        
except
(
voluptuous
.
error
.
Error
IOError
FeatureGateException
)
as
e
:
            
errors
.
append
(
FeatureGateException
(
e
filename
)
)
        
except
pytoml
.
TomlError
as
e
:
            
errors
.
append
(
e
)
    
if
errors
:
        
raise
ExceptionGroup
(
errors
)
    
return
features
def
hyphens_to_camel_case
(
s
)
:
    
"
"
"
Convert
names
-
with
-
hyphens
to
namesInCamelCase
"
"
"
    
rv
=
"
"
    
for
part
in
s
.
split
(
"
-
"
)
:
        
if
rv
=
=
"
"
:
            
rv
=
part
.
lower
(
)
        
else
:
            
rv
+
=
part
[
0
]
.
upper
(
)
+
part
[
1
:
]
.
lower
(
)
    
return
rv
def
expand_feature
(
feature
)
:
    
"
"
"
Fill
in
default
values
for
optional
fields
"
"
"
    
key_changes
=
[
]
    
for
key
in
feature
.
keys
(
)
:
        
if
"
-
"
in
key
:
            
new_key
=
hyphens_to_camel_case
(
key
)
            
key_changes
.
append
(
(
key
new_key
)
)
    
for
(
old_key
new_key
)
in
key_changes
:
        
feature
[
new_key
]
=
feature
[
old_key
]
        
del
feature
[
old_key
]
    
if
feature
[
"
type
"
]
=
=
"
boolean
"
:
        
feature
.
setdefault
(
"
preference
"
"
features
.
{
}
.
enabled
"
.
format
(
feature
[
"
id
"
]
)
)
        
feature
.
setdefault
(
"
defaultValue
"
None
)
    
elif
"
preference
"
not
in
feature
:
        
raise
FeatureGateException
(
            
"
Features
of
type
{
}
must
specify
an
explicit
preference
name
"
.
format
(
                
feature
[
"
type
"
]
            
)
        
)
    
feature
.
setdefault
(
"
isPublic
"
False
)
    
try
:
        
for
key
in
[
"
defaultValue
"
"
isPublic
"
]
:
            
feature
[
key
]
=
process_configured_value
(
key
feature
[
key
]
)
    
except
FeatureGateException
as
e
:
        
raise
FeatureGateException
(
            
"
Error
when
processing
feature
{
}
:
{
}
"
.
format
(
feature
[
"
id
"
]
e
)
        
)
    
return
feature
def
process_configured_value
(
name
value
)
:
    
if
not
isinstance
(
value
dict
)
:
        
return
{
"
default
"
:
value
}
    
if
"
default
"
not
in
value
:
        
raise
FeatureGateException
(
            
"
Config
for
{
}
has
no
default
:
{
}
"
.
format
(
name
value
)
        
)
    
expected_keys
=
set
(
        
{
            
"
default
"
            
"
win
"
            
"
mac
"
            
"
linux
"
            
"
android
"
            
"
nightly
"
            
"
early_beta_or_earlier
"
            
"
beta
"
            
"
release
"
            
"
dev
-
edition
"
            
"
esr
"
            
"
thunderbird
"
        
}
    
)
    
for
key
in
value
.
keys
(
)
:
        
parts
=
[
p
.
strip
(
)
for
p
in
key
.
split
(
"
"
)
]
        
for
part
in
parts
:
            
if
part
not
in
expected_keys
:
                
raise
FeatureGateException
(
                    
"
Unexpected
target
{
}
expected
any
of
{
}
"
.
format
(
                        
part
expected_keys
                    
)
                
)
    
return
value
if
__name__
=
=
"
__main__
"
:
    
sys
.
exit
(
main
(
sys
.
stdout
*
sys
.
argv
[
1
:
]
)
)
