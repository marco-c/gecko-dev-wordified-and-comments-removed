"
"
"
Provides
classes
to
represent
module
version
numbers
(
one
class
for
each
style
of
version
numbering
)
.
There
are
currently
two
such
classes
implemented
:
StrictVersion
and
LooseVersion
.
Every
version
number
class
implements
the
following
interface
:
  
*
the
'
parse
'
method
takes
a
string
and
parses
it
to
some
internal
    
representation
;
if
the
string
is
an
invalid
version
number
    
'
parse
'
raises
a
ValueError
exception
  
*
the
class
constructor
takes
an
optional
string
argument
which
    
if
supplied
is
passed
to
'
parse
'
  
*
__str__
reconstructs
the
string
that
was
passed
to
'
parse
'
(
or
    
an
equivalent
string
-
-
ie
.
one
that
will
generate
an
equivalent
    
version
number
instance
)
  
*
__repr__
generates
Python
code
to
recreate
the
version
number
instance
  
*
_cmp
compares
the
current
instance
with
either
another
instance
    
of
the
same
class
or
a
string
(
which
will
be
parsed
to
an
instance
    
of
the
same
class
thus
must
follow
the
same
rules
)
"
"
"
import
sys
import
re
class
LooseVersion
:
    
"
"
"
Version
numbering
for
anarchists
and
software
realists
.
    
Implements
the
standard
interface
for
version
number
classes
as
    
described
above
.
A
version
number
consists
of
a
series
of
numbers
    
separated
by
either
periods
or
strings
of
letters
.
When
comparing
    
version
numbers
the
numeric
components
will
be
compared
    
numerically
and
the
alphabetic
components
lexically
.
The
following
    
are
all
valid
version
numbers
in
no
particular
order
:
        
1
.
5
.
1
        
1
.
5
.
2b2
        
161
        
3
.
10a
        
8
.
02
        
3
.
4j
        
1996
.
07
.
12
        
3
.
2
.
pl0
        
3
.
1
.
1
.
6
        
2g6
        
11g
        
0
.
960923
        
2
.
2beta29
        
1
.
13
+
+
        
5
.
5
.
kw
        
2
.
0b1pl0
    
In
fact
there
is
no
such
thing
as
an
invalid
version
number
under
    
this
scheme
;
the
rules
for
comparison
are
simple
and
predictable
    
but
may
not
always
give
the
results
you
want
(
for
some
definition
    
of
"
want
"
)
.
    
"
"
"
    
component_re
=
re
.
compile
(
r
"
(
\
d
+
|
[
a
-
z
]
+
|
\
.
)
"
re
.
VERBOSE
)
    
def
__init__
(
self
vstring
=
None
)
:
        
if
vstring
:
            
self
.
parse
(
vstring
)
    
def
__eq__
(
self
other
)
:
        
c
=
self
.
_cmp
(
other
)
        
if
c
is
NotImplemented
:
            
return
c
        
return
c
=
=
0
    
def
__lt__
(
self
other
)
:
        
c
=
self
.
_cmp
(
other
)
        
if
c
is
NotImplemented
:
            
return
c
        
return
c
<
0
    
def
__le__
(
self
other
)
:
        
c
=
self
.
_cmp
(
other
)
        
if
c
is
NotImplemented
:
            
return
c
        
return
c
<
=
0
    
def
__gt__
(
self
other
)
:
        
c
=
self
.
_cmp
(
other
)
        
if
c
is
NotImplemented
:
            
return
c
        
return
c
>
0
    
def
__ge__
(
self
other
)
:
        
c
=
self
.
_cmp
(
other
)
        
if
c
is
NotImplemented
:
            
return
c
        
return
c
>
=
0
    
def
parse
(
self
vstring
)
:
        
self
.
vstring
=
vstring
        
components
=
[
x
for
x
in
self
.
component_re
.
split
(
vstring
)
if
x
and
x
!
=
"
.
"
]
        
for
i
obj
in
enumerate
(
components
)
:
            
try
:
                
components
[
i
]
=
int
(
obj
)
            
except
ValueError
:
                
pass
        
self
.
version
=
components
    
def
__str__
(
self
)
:
        
return
self
.
vstring
    
def
__repr__
(
self
)
:
        
return
"
LooseVersion
(
'
%
s
'
)
"
%
str
(
self
)
    
def
_cmp
(
self
other
)
:
        
other
=
self
.
_coerce
(
other
)
        
if
other
is
NotImplemented
:
            
return
NotImplemented
        
if
self
.
version
=
=
other
.
version
:
            
return
0
        
if
self
.
version
<
other
.
version
:
            
return
-
1
        
if
self
.
version
>
other
.
version
:
            
return
1
    
staticmethod
    
def
_coerce
(
other
)
:
        
if
isinstance
(
other
LooseVersion
)
:
            
return
other
        
elif
isinstance
(
other
str
)
:
            
return
LooseVersion
(
other
)
        
elif
"
distutils
"
in
sys
.
modules
:
            
try
:
                
from
distutils
.
version
import
LooseVersion
as
deprecated
            
except
ImportError
:
                
return
NotImplemented
            
if
isinstance
(
other
deprecated
)
:
                
return
LooseVersion
(
str
(
other
)
)
        
return
NotImplemented
