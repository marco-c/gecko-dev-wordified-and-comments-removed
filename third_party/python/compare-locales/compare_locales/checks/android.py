from
__future__
import
absolute_import
from
__future__
import
unicode_literals
import
re
from
.
base
import
Checker
from
.
.
parser
.
android
import
textContent
class
AndroidChecker
(
Checker
)
:
    
pattern
=
re
.
compile
(
'
.
*
/
strings
.
*
\
\
.
xml
'
)
    
def
check
(
self
refEnt
l10nEnt
)
:
        
'
'
'
Given
the
reference
and
localized
Entities
performs
checks
.
        
This
is
a
generator
yielding
tuples
of
        
-
"
warning
"
or
"
error
"
depending
on
what
should
be
reported
        
-
tuple
of
line
column
info
for
the
error
within
the
string
        
-
description
string
to
be
shown
in
the
report
        
'
'
'
        
refNode
=
refEnt
.
node
        
l10nNode
=
l10nEnt
.
node
        
if
refNode
.
nodeName
!
=
l10nNode
.
nodeName
:
            
yield
(
"
error
"
0
"
Incompatible
resource
types
"
"
android
"
)
            
return
        
if
refNode
.
nodeName
!
=
"
string
"
:
            
yield
(
"
warning
"
0
"
Unsupported
resource
type
"
"
android
"
)
            
return
        
for
report_tuple
in
self
.
check_string
(
[
refNode
]
l10nNode
)
:
            
yield
report_tuple
    
def
check_string
(
self
refs
l10n
)
:
        
'
'
'
Check
a
single
string
literal
against
a
list
of
references
.
        
There
should
be
multiple
nodes
given
for
<
plurals
>
or
<
string
-
array
>
.
        
'
'
'
        
if
self
.
not_translatable
(
l10n
*
refs
)
:
            
yield
(
                
"
error
"
                
0
                
"
strings
must
be
translatable
"
                
"
android
"
            
)
            
return
        
l10nstring
=
textContent
(
l10n
)
        
for
report_tuple
in
check_apostrophes
(
l10nstring
)
:
            
yield
report_tuple
    
def
not_translatable
(
self
*
nodes
)
:
        
return
any
(
            
node
.
hasAttribute
(
"
translatable
"
)
            
and
node
.
getAttribute
(
"
translatable
"
)
=
=
"
false
"
            
for
node
in
nodes
        
)
silencer
=
re
.
compile
(
r
'
\
\
.
|
"
"
'
)
def
check_apostrophes
(
string
)
:
    
'
'
'
Check
Android
logic
for
quotes
and
apostrophes
.
    
If
you
have
an
apostrophe
(
'
)
in
your
string
you
must
either
escape
it
    
with
a
backslash
(
\
'
)
or
enclose
the
string
in
double
-
quotes
(
"
)
.
    
Unescaped
quotes
are
not
visually
shown
on
Android
but
they
'
re
    
also
harmless
so
we
'
re
not
checking
for
quotes
.
We
might
do
once
we
'
re
    
better
at
checking
for
inline
XML
which
is
full
of
quotes
.
    
Pairing
quotes
as
in
'
"
"
'
is
bad
though
so
report
errors
for
that
.
    
Mostly
because
it
'
s
hard
to
tell
if
a
string
is
consider
quoted
or
not
    
by
Android
in
the
end
.
    
https
:
/
/
developer
.
android
.
com
/
guide
/
topics
/
resources
/
string
-
resource
#
escaping_quotes
    
'
'
'
    
for
m
in
re
.
finditer
(
'
"
"
'
string
)
:
        
yield
(
            
"
error
"
            
m
.
start
(
)
            
"
Double
straight
quotes
not
allowed
"
            
"
android
"
        
)
    
string
=
silencer
.
sub
(
"
"
string
)
    
is_quoted
=
string
.
startswith
(
'
"
'
)
and
string
.
endswith
(
'
"
'
)
    
if
not
is_quoted
:
        
for
m
in
re
.
finditer
(
"
'
"
string
)
:
            
yield
(
                
"
error
"
                
m
.
start
(
)
                
"
Apostrophe
must
be
escaped
"
                
"
android
"
            
)
