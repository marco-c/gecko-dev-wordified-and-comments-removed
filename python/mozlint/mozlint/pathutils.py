from
__future__
import
unicode_literals
import
os
from
mozpack
import
path
as
mozpath
from
mozpack
.
files
import
FileFinder
class
FilterPath
(
object
)
:
    
"
"
"
Helper
class
to
make
comparing
and
matching
file
paths
easier
.
"
"
"
    
def
__init__
(
self
path
exclude
=
None
)
:
        
self
.
path
=
os
.
path
.
normpath
(
path
)
        
self
.
_finder
=
None
        
self
.
exclude
=
exclude
    
property
    
def
finder
(
self
)
:
        
if
self
.
_finder
:
            
return
self
.
_finder
        
self
.
_finder
=
FileFinder
(
            
self
.
path
find_executables
=
False
ignore
=
self
.
exclude
)
        
return
self
.
_finder
    
property
    
def
exists
(
self
)
:
        
return
os
.
path
.
exists
(
self
.
path
)
    
property
    
def
isfile
(
self
)
:
        
return
os
.
path
.
isfile
(
self
.
path
)
    
property
    
def
isdir
(
self
)
:
        
return
os
.
path
.
isdir
(
self
.
path
)
    
def
join
(
self
*
args
)
:
        
return
FilterPath
(
os
.
path
.
join
(
self
*
args
)
)
    
def
match
(
self
patterns
)
:
        
return
any
(
mozpath
.
match
(
self
.
path
pattern
.
path
)
for
pattern
in
patterns
)
    
def
contains
(
self
other
)
:
        
"
"
"
Return
True
if
other
is
a
subdirectory
of
self
or
equals
self
.
"
"
"
        
if
isinstance
(
other
FilterPath
)
:
            
other
=
other
.
path
        
a
=
os
.
path
.
abspath
(
self
.
path
)
        
b
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
abspath
(
other
)
)
        
if
b
.
startswith
(
a
)
:
            
return
True
        
return
False
    
def
__repr__
(
self
)
:
        
return
repr
(
self
.
path
)
def
filterpaths
(
paths
linter
*
*
lintargs
)
:
    
"
"
"
Filters
a
list
of
paths
.
    
Given
a
list
of
paths
and
a
linter
definition
plus
extra
    
arguments
return
the
set
of
paths
that
should
be
linted
.
    
:
param
paths
:
A
starting
list
of
paths
to
possibly
lint
.
    
:
param
linter
:
A
linter
definition
.
    
:
param
lintargs
:
Extra
arguments
passed
to
the
linter
.
    
:
returns
:
A
list
of
file
paths
to
lint
.
    
"
"
"
    
include
=
linter
.
get
(
'
include
'
[
]
)
    
exclude
=
lintargs
.
get
(
'
exclude
'
[
]
)
    
exclude
.
extend
(
linter
.
get
(
'
exclude
'
[
]
)
)
    
if
not
lintargs
.
get
(
'
use_filters
'
True
)
or
(
not
include
and
not
exclude
)
:
        
return
paths
    
include
=
map
(
FilterPath
include
or
[
]
)
    
exclude
=
map
(
FilterPath
exclude
or
[
]
)
    
includepaths
=
[
p
for
p
in
include
if
p
.
exists
]
    
excludepaths
=
[
p
for
p
in
exclude
if
p
.
exists
]
    
includeglobs
=
[
p
for
p
in
include
if
not
p
.
exists
]
    
excludeglobs
=
[
p
for
p
in
exclude
if
not
p
.
exists
]
    
keep
=
set
(
)
    
discard
=
set
(
)
    
for
path
in
map
(
FilterPath
paths
)
:
        
for
inc
in
includepaths
:
            
excs
=
[
e
for
e
in
excludepaths
if
inc
.
contains
(
e
)
]
            
if
path
.
contains
(
inc
)
:
                
keep
.
add
(
inc
)
                
discard
.
update
(
excs
)
            
elif
inc
.
contains
(
path
)
:
                
if
not
any
(
e
.
contains
(
path
)
for
e
in
excs
)
:
                    
keep
.
add
(
path
)
        
if
path
.
isfile
:
            
if
not
path
.
match
(
includeglobs
)
:
                
continue
            
elif
path
.
match
(
excludeglobs
)
:
                
continue
            
keep
.
add
(
path
)
        
elif
path
.
isdir
:
            
path
.
exclude
=
excludeglobs
            
for
pattern
in
includeglobs
:
                
for
p
f
in
path
.
finder
.
find
(
pattern
.
path
)
:
                    
keep
.
add
(
path
.
join
(
p
)
)
    
lintargs
[
'
exclude
'
]
=
[
f
.
path
for
f
in
discard
]
    
return
[
f
.
path
for
f
in
keep
]
