import
functools
from
pathlib
import
Path
from
gecko_taskgraph
import
GECKO
def
load_sparse_profile
(
profile_path
topsrcdir
=
GECKO
)
:
    
"
"
"
Return
the
ordered
(
includes
excludes
)
pattern
lines
of
a
Mercurial
    
sparse
profile
following
%
include
directives
.
"
"
"
    
includes
=
[
]
    
excludes
=
[
]
    
def
parse
(
relpath
)
:
        
full_path
=
Path
(
topsrcdir
)
/
relpath
        
if
not
full_path
.
exists
(
)
:
            
raise
FileNotFoundError
(
                
f
"
Sparse
profile
'
{
full_path
.
stem
}
'
not
found
at
{
full_path
}
"
            
)
        
section
=
includes
        
for
raw_line
in
full_path
.
read_text
(
encoding
=
"
utf
-
8
"
)
.
splitlines
(
)
:
            
line
=
raw_line
.
strip
(
)
            
if
not
line
or
line
.
startswith
(
"
#
"
)
:
                
continue
            
if
line
.
startswith
(
"
%
include
"
)
:
                
parse
(
line
[
len
(
"
%
include
"
)
:
]
.
strip
(
)
)
            
elif
line
=
=
"
[
include
]
"
:
                
section
=
includes
            
elif
line
=
=
"
[
exclude
]
"
:
                
section
=
excludes
            
else
:
                
section
.
append
(
line
)
    
parse
(
profile_path
)
    
return
includes
excludes
functools
.
cache
def
_get_taskgraph_sparse_profile
(
)
:
    
"
"
"
    
Parse
the
taskgraph
sparse
profile
and
return
the
paths
and
globs
it
includes
.
    
"
"
"
    
includes
_
=
load_sparse_profile
(
"
build
/
sparse
-
profiles
/
taskgraph
"
)
    
paths
=
{
        
Path
(
line
[
len
(
"
path
:
"
)
:
]
.
strip
(
)
)
        
for
line
in
includes
        
if
line
.
startswith
(
"
path
:
"
)
    
}
    
globs
=
{
        
line
[
len
(
"
glob
:
"
)
:
]
.
strip
(
)
for
line
in
includes
if
line
.
startswith
(
"
glob
:
"
)
    
}
    
return
paths
globs
functools
.
cache
def
is_path_covered_by_taskgraph_sparse_profile
(
path
)
:
    
"
"
"
    
Check
if
a
given
path
would
be
included
in
the
taskgraph
sparse
checkout
.
    
"
"
"
    
profile_paths
profile_globs
=
_get_taskgraph_sparse_profile
(
)
    
path
=
Path
(
path
)
    
for
profile_path
in
profile_paths
:
        
if
path
=
=
profile_path
or
profile_path
in
path
.
parents
:
            
return
True
    
path_with_parent
=
Path
(
"
_
"
path
)
    
for
pattern
in
profile_globs
:
        
if
path_with_parent
.
match
(
pattern
)
:
            
return
True
    
return
False
