"
"
"
Python
source
expertise
for
coverage
.
py
"
"
"
import
os
.
path
import
types
import
zipimport
from
coverage
import
env
files
from
coverage
.
misc
import
contract
expensive
isolate_module
join_regex
from
coverage
.
misc
import
CoverageException
NoSource
from
coverage
.
parser
import
PythonParser
from
coverage
.
phystokens
import
source_token_lines
source_encoding
from
coverage
.
plugin
import
FileReporter
os
=
isolate_module
(
os
)
contract
(
returns
=
'
bytes
'
)
def
read_python_source
(
filename
)
:
    
"
"
"
Read
the
Python
source
text
from
filename
.
    
Returns
bytes
.
    
"
"
"
    
with
open
(
filename
"
rb
"
)
as
f
:
        
source
=
f
.
read
(
)
    
if
env
.
IRONPYTHON
:
        
source
=
bytes
(
source
)
    
return
source
.
replace
(
b
"
\
r
\
n
"
b
"
\
n
"
)
.
replace
(
b
"
\
r
"
b
"
\
n
"
)
contract
(
returns
=
'
unicode
'
)
def
get_python_source
(
filename
)
:
    
"
"
"
Return
the
source
code
as
unicode
.
"
"
"
    
base
ext
=
os
.
path
.
splitext
(
filename
)
    
if
ext
=
=
"
.
py
"
and
env
.
WINDOWS
:
        
exts
=
[
"
.
py
"
"
.
pyw
"
]
    
else
:
        
exts
=
[
ext
]
    
for
ext
in
exts
:
        
try_filename
=
base
+
ext
        
if
os
.
path
.
exists
(
try_filename
)
:
            
source
=
read_python_source
(
try_filename
)
            
break
        
source
=
get_zip_bytes
(
try_filename
)
        
if
source
is
not
None
:
            
break
    
else
:
        
exc_msg
=
"
No
source
for
code
:
'
%
s
'
.
\
n
"
%
(
filename
)
        
exc_msg
+
=
"
Aborting
report
output
consider
using
-
i
.
"
        
raise
NoSource
(
exc_msg
)
    
source
=
source
.
replace
(
b
'
\
f
'
b
'
'
)
    
source
=
source
.
decode
(
source_encoding
(
source
)
"
replace
"
)
    
if
source
and
source
[
-
1
]
!
=
'
\
n
'
:
        
source
+
=
'
\
n
'
    
return
source
contract
(
returns
=
'
bytes
|
None
'
)
def
get_zip_bytes
(
filename
)
:
    
"
"
"
Get
data
from
filename
if
it
is
a
zip
file
path
.
    
Returns
the
bytestring
data
read
from
the
zip
file
or
None
if
no
zip
file
    
could
be
found
or
filename
isn
'
t
in
it
.
The
data
returned
will
be
    
an
empty
string
if
the
file
is
empty
.
    
"
"
"
    
markers
=
[
'
.
zip
'
+
os
.
sep
'
.
egg
'
+
os
.
sep
'
.
pex
'
+
os
.
sep
]
    
for
marker
in
markers
:
        
if
marker
in
filename
:
            
parts
=
filename
.
split
(
marker
)
            
try
:
                
zi
=
zipimport
.
zipimporter
(
parts
[
0
]
+
marker
[
:
-
1
]
)
            
except
zipimport
.
ZipImportError
:
                
continue
            
try
:
                
data
=
zi
.
get_data
(
parts
[
1
]
)
            
except
IOError
:
                
continue
            
return
data
    
return
None
def
source_for_file
(
filename
)
:
    
"
"
"
Return
the
source
filename
for
filename
.
    
Given
a
file
name
being
traced
return
the
best
guess
as
to
the
source
    
file
to
attribute
it
to
.
    
"
"
"
    
if
filename
.
endswith
(
"
.
py
"
)
:
        
return
filename
    
elif
filename
.
endswith
(
(
"
.
pyc
"
"
.
pyo
"
)
)
:
        
py_filename
=
filename
[
:
-
1
]
        
if
os
.
path
.
exists
(
py_filename
)
:
            
return
py_filename
        
if
env
.
WINDOWS
:
            
pyw_filename
=
py_filename
+
"
w
"
            
if
os
.
path
.
exists
(
pyw_filename
)
:
                
return
pyw_filename
        
return
py_filename
    
elif
filename
.
endswith
(
"
py
.
class
"
)
:
        
return
filename
[
:
-
9
]
+
"
.
py
"
    
return
filename
def
source_for_morf
(
morf
)
:
    
"
"
"
Get
the
source
filename
for
the
module
-
or
-
file
morf
.
"
"
"
    
if
hasattr
(
morf
'
__file__
'
)
and
morf
.
__file__
:
        
filename
=
morf
.
__file__
    
elif
isinstance
(
morf
types
.
ModuleType
)
:
        
raise
CoverageException
(
"
Module
{
}
has
no
file
"
.
format
(
morf
)
)
    
else
:
        
filename
=
morf
    
filename
=
source_for_file
(
files
.
unicode_filename
(
filename
)
)
    
return
filename
class
PythonFileReporter
(
FileReporter
)
:
    
"
"
"
Report
support
for
a
Python
file
.
"
"
"
    
def
__init__
(
self
morf
coverage
=
None
)
:
        
self
.
coverage
=
coverage
        
filename
=
source_for_morf
(
morf
)
        
super
(
PythonFileReporter
self
)
.
__init__
(
files
.
canonical_filename
(
filename
)
)
        
if
hasattr
(
morf
'
__name__
'
)
:
            
name
=
morf
.
__name__
.
replace
(
"
.
"
os
.
sep
)
            
if
os
.
path
.
basename
(
filename
)
.
startswith
(
'
__init__
.
'
)
:
                
name
+
=
os
.
sep
+
"
__init__
"
            
name
+
=
"
.
py
"
            
name
=
files
.
unicode_filename
(
name
)
        
else
:
            
name
=
files
.
relative_filename
(
filename
)
        
self
.
relname
=
name
        
self
.
_source
=
None
        
self
.
_parser
=
None
        
self
.
_excluded
=
None
    
def
__repr__
(
self
)
:
        
return
"
<
PythonFileReporter
{
!
r
}
>
"
.
format
(
self
.
filename
)
    
contract
(
returns
=
'
unicode
'
)
    
def
relative_filename
(
self
)
:
        
return
self
.
relname
    
property
    
def
parser
(
self
)
:
        
"
"
"
Lazily
create
a
:
class
:
PythonParser
.
"
"
"
        
if
self
.
_parser
is
None
:
            
self
.
_parser
=
PythonParser
(
                
filename
=
self
.
filename
                
exclude
=
self
.
coverage
.
_exclude_regex
(
'
exclude
'
)
            
)
            
self
.
_parser
.
parse_source
(
)
        
return
self
.
_parser
    
def
lines
(
self
)
:
        
"
"
"
Return
the
line
numbers
of
statements
in
the
file
.
"
"
"
        
return
self
.
parser
.
statements
    
def
excluded_lines
(
self
)
:
        
"
"
"
Return
the
line
numbers
of
statements
in
the
file
.
"
"
"
        
return
self
.
parser
.
excluded
    
def
translate_lines
(
self
lines
)
:
        
return
self
.
parser
.
translate_lines
(
lines
)
    
def
translate_arcs
(
self
arcs
)
:
        
return
self
.
parser
.
translate_arcs
(
arcs
)
    
expensive
    
def
no_branch_lines
(
self
)
:
        
no_branch
=
self
.
parser
.
lines_matching
(
            
join_regex
(
self
.
coverage
.
config
.
partial_list
)
            
join_regex
(
self
.
coverage
.
config
.
partial_always_list
)
            
)
        
return
no_branch
    
expensive
    
def
arcs
(
self
)
:
        
return
self
.
parser
.
arcs
(
)
    
expensive
    
def
exit_counts
(
self
)
:
        
return
self
.
parser
.
exit_counts
(
)
    
def
missing_arc_description
(
self
start
end
executed_arcs
=
None
)
:
        
return
self
.
parser
.
missing_arc_description
(
start
end
executed_arcs
)
    
contract
(
returns
=
'
unicode
'
)
    
def
source
(
self
)
:
        
if
self
.
_source
is
None
:
            
self
.
_source
=
get_python_source
(
self
.
filename
)
        
return
self
.
_source
    
def
should_be_python
(
self
)
:
        
"
"
"
Does
it
seem
like
this
file
should
contain
Python
?
        
This
is
used
to
decide
if
a
file
reported
as
part
of
the
execution
of
        
a
program
was
really
likely
to
have
contained
Python
in
the
first
        
place
.
        
"
"
"
        
_
ext
=
os
.
path
.
splitext
(
self
.
filename
)
        
if
ext
.
startswith
(
'
.
py
'
)
:
            
return
True
        
if
not
ext
:
            
return
True
        
return
False
    
def
source_token_lines
(
self
)
:
        
return
source_token_lines
(
self
.
source
(
)
)
