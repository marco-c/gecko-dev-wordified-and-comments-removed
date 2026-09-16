"
"
"
!
!
!
ALL
SYMBOLS
IN
HERE
ARE
INTERNAL
.
Everything
might
change
without
any
notice
.
"
"
"
from
itertools
import
zip_longest
from
typing
import
TYPE_CHECKING
Any
Optional
if
TYPE_CHECKING
:
    
from
packageurl
import
PackageURL
class
ComparableTuple
(
tuple
[
Optional
[
Any
]
.
.
.
]
)
:
    
"
"
"
    
Allows
comparison
of
tuples
allowing
for
None
values
.
    
"
"
"
    
def
__lt__
(
self
other
:
Any
)
-
>
bool
:
        
for
s
o
in
zip_longest
(
self
other
)
:
            
if
s
=
=
o
:
                
continue
            
if
s
is
None
:
                
return
False
            
if
o
is
None
:
                
return
True
            
return
bool
(
s
<
o
)
        
return
False
    
def
__gt__
(
self
other
:
Any
)
-
>
bool
:
        
for
s
o
in
zip_longest
(
self
other
)
:
            
if
s
=
=
o
:
                
continue
            
if
s
is
None
:
                
return
True
            
if
o
is
None
:
                
return
False
            
return
bool
(
s
>
o
)
        
return
False
class
ComparableDict
(
ComparableTuple
)
:
    
"
"
"
    
Allows
comparison
of
dictionaries
allowing
for
missing
/
None
values
.
    
"
"
"
    
def
__new__
(
cls
d
:
dict
[
Any
Any
]
)
-
>
'
ComparableDict
'
:
        
return
super
(
)
.
__new__
(
cls
sorted
(
d
.
items
(
)
)
)
class
ComparablePackageURL
(
ComparableTuple
)
:
    
"
"
"
    
Allows
comparison
of
PackageURL
allowing
for
qualifiers
.
    
"
"
"
    
def
__new__
(
cls
p
:
'
PackageURL
'
)
-
>
'
ComparablePackageURL
'
:
        
return
super
(
)
.
__new__
(
cls
(
            
p
.
type
            
p
.
namespace
            
p
.
version
            
ComparableDict
(
p
.
qualifiers
)
if
isinstance
(
p
.
qualifiers
dict
)
else
p
.
qualifiers
            
p
.
subpath
        
)
)
