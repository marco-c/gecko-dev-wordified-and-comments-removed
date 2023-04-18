import
re
import
os
import
itertools
from
collections
import
defaultdict
MYPY
=
False
if
MYPY
:
    
from
typing
import
Any
    
from
typing
import
Dict
    
from
typing
import
Iterable
    
from
typing
import
List
    
from
typing
import
MutableMapping
    
from
typing
import
Optional
    
from
typing
import
Pattern
    
from
typing
import
Tuple
    
from
typing
import
TypeVar
    
from
typing
import
Union
    
from
typing
import
cast
    
T
=
TypeVar
(
'
T
'
)
end_space
=
re
.
compile
(
r
"
(
[
^
\
\
]
\
s
)
*
"
)
def
fnmatch_translate
(
pat
)
:
    
parts
=
[
]
    
seq
=
None
    
i
=
0
    
any_char
=
b
"
[
^
/
]
"
    
if
pat
[
0
:
1
]
=
=
b
"
/
"
:
        
parts
.
append
(
b
"
^
"
)
        
pat
=
pat
[
1
:
]
    
else
:
        
parts
.
append
(
b
"
^
(
?
:
.
*
/
)
?
"
)
    
name_pattern
=
True
    
if
pat
[
-
1
:
]
=
=
b
"
/
"
:
        
pat
=
pat
[
:
-
1
]
        
suffix
=
b
"
(
?
:
/
|
)
"
    
else
:
        
suffix
=
b
"
"
    
while
i
<
len
(
pat
)
:
        
c
=
pat
[
i
:
i
+
1
]
        
if
c
=
=
b
"
\
\
"
:
            
if
i
<
len
(
pat
)
-
1
:
                
i
+
=
1
                
c
=
pat
[
i
:
i
+
1
]
                
parts
.
append
(
re
.
escape
(
c
)
)
            
else
:
                
raise
ValueError
        
elif
seq
is
not
None
:
            
if
c
=
=
b
"
]
"
:
                
seq
=
None
                
if
parts
[
-
1
]
=
=
b
"
[
"
:
                    
parts
=
parts
[
:
-
1
]
                
elif
parts
[
-
1
]
=
=
b
"
^
"
and
parts
[
-
2
]
=
=
b
"
[
"
:
                    
raise
ValueError
                
else
:
                    
parts
.
append
(
c
)
            
elif
c
=
=
b
"
-
"
:
                
parts
.
append
(
c
)
            
elif
c
=
=
b
"
[
"
:
                
raise
ValueError
            
else
:
                
parts
.
append
(
re
.
escape
(
c
)
)
        
elif
c
=
=
b
"
[
"
:
            
parts
.
append
(
b
"
[
"
)
            
if
i
<
len
(
pat
)
-
1
and
pat
[
i
+
1
:
i
+
2
]
in
(
b
"
!
"
b
"
^
"
)
:
                
parts
.
append
(
b
"
^
"
)
                
i
+
=
1
            
seq
=
i
        
elif
c
=
=
b
"
*
"
:
            
if
i
<
len
(
pat
)
-
1
and
pat
[
i
+
1
:
i
+
2
]
=
=
b
"
*
"
:
                
if
i
>
0
and
pat
[
i
-
1
:
i
]
!
=
b
"
/
"
:
                    
raise
ValueError
                
parts
.
append
(
b
"
.
*
"
)
                
i
+
=
1
                
if
i
<
len
(
pat
)
-
1
and
pat
[
i
+
1
:
i
+
2
]
!
=
b
"
/
"
:
                    
raise
ValueError
            
else
:
                
parts
.
append
(
any_char
+
b
"
*
"
)
        
elif
c
=
=
b
"
?
"
:
            
parts
.
append
(
any_char
)
        
elif
c
=
=
b
"
/
"
and
not
seq
:
            
name_pattern
=
False
            
parts
.
append
(
c
)
        
else
:
            
parts
.
append
(
re
.
escape
(
c
)
)
        
i
+
=
1
    
if
name_pattern
:
        
parts
[
0
]
=
b
"
^
"
    
if
seq
is
not
None
:
        
raise
ValueError
    
parts
.
append
(
suffix
)
    
try
:
        
return
name_pattern
re
.
compile
(
b
"
"
.
join
(
parts
)
)
    
except
Exception
:
        
raise
ValueError
pattern_re
=
re
.
compile
(
br
"
.
*
[
\
*
\
[
\
?
]
"
)
def
parse_line
(
line
)
:
    
line
=
line
.
rstrip
(
)
    
if
not
line
or
line
[
0
:
1
]
=
=
b
"
#
"
:
        
return
None
    
invert
=
line
[
0
:
1
]
=
=
b
"
!
"
    
if
invert
:
        
line
=
line
[
1
:
]
    
dir_only
=
line
[
-
1
:
]
=
=
b
"
/
"
    
if
dir_only
:
        
line
=
line
[
:
-
1
]
    
if
not
invert
and
not
pattern_re
.
match
(
line
)
:
        
literal
=
True
        
pattern
=
tuple
(
line
.
rsplit
(
b
"
/
"
1
)
)
    
else
:
        
pattern
=
fnmatch_translate
(
line
)
        
literal
=
False
    
return
invert
dir_only
literal
pattern
class
PathFilter
:
    
def
__init__
(
self
root
extras
=
None
cache
=
None
)
:
        
if
root
:
            
ignore_path
=
os
.
path
.
join
(
root
b
"
.
gitignore
"
)
        
else
:
            
ignore_path
=
None
        
if
not
ignore_path
and
not
extras
:
            
self
.
trivial
=
True
            
return
        
self
.
trivial
=
False
        
self
.
literals_file
=
defaultdict
(
dict
)
        
self
.
literals_dir
=
defaultdict
(
dict
)
        
self
.
patterns_file
=
[
]
        
self
.
patterns_dir
=
[
]
        
if
cache
is
None
:
            
cache
=
{
}
        
self
.
cache
=
cache
        
if
extras
is
None
:
            
extras
=
[
]
        
if
ignore_path
and
os
.
path
.
exists
(
ignore_path
)
:
            
args
=
ignore_path
extras
        
else
:
            
args
=
None
extras
        
self
.
_read_ignore
(
*
args
)
    
def
_read_ignore
(
self
ignore_path
extras
)
:
        
if
ignore_path
is
not
None
:
            
with
open
(
ignore_path
"
rb
"
)
as
f
:
                
for
line
in
f
:
                    
self
.
_read_line
(
line
)
        
for
line
in
extras
:
            
self
.
_read_line
(
line
)
    
def
_read_line
(
self
line
)
:
        
parsed
=
parse_line
(
line
)
        
if
not
parsed
:
            
return
        
invert
dir_only
literal
rule
=
parsed
        
if
invert
:
            
assert
not
literal
            
if
MYPY
:
                
rule
=
cast
(
Tuple
[
bool
Pattern
[
bytes
]
]
rule
)
            
if
not
dir_only
:
                
rules_iter
=
itertools
.
chain
(
                    
itertools
.
chain
(
*
(
item
.
items
(
)
for
item
in
self
.
literals_dir
.
values
(
)
)
)
                    
itertools
.
chain
(
*
(
item
.
items
(
)
for
item
in
self
.
literals_file
.
values
(
)
)
)
                    
self
.
patterns_dir
                    
self
.
patterns_file
)
            
else
:
                
rules_iter
=
itertools
.
chain
(
                    
itertools
.
chain
(
*
(
item
.
items
(
)
for
item
in
self
.
literals_dir
.
values
(
)
)
)
                    
self
.
patterns_dir
)
            
for
rules
in
rules_iter
:
                
rules
[
1
]
.
append
(
rule
)
        
else
:
            
if
literal
:
                
if
MYPY
:
                    
rule
=
cast
(
Tuple
[
bytes
.
.
.
]
rule
)
                
if
len
(
rule
)
=
=
1
:
                    
dir_name
pattern
=
None
rule
[
0
]
                
else
:
                    
dir_name
pattern
=
rule
                
self
.
literals_dir
[
dir_name
]
[
pattern
]
=
[
]
                
if
not
dir_only
:
                    
self
.
literals_file
[
dir_name
]
[
pattern
]
=
[
]
            
else
:
                
if
MYPY
:
                    
rule
=
cast
(
Tuple
[
bool
Pattern
[
bytes
]
]
rule
)
                
self
.
patterns_dir
.
append
(
(
rule
[
]
)
)
                
if
not
dir_only
:
                    
self
.
patterns_file
.
append
(
(
rule
[
]
)
)
    
def
filter
(
self
               
iterator
               
)
:
        
empty
=
{
}
        
for
dirpath
dirnames
filenames
in
iterator
:
            
orig_dirpath
=
dirpath
            
path_sep
=
os
.
path
.
sep
.
encode
(
)
            
if
path_sep
!
=
b
"
/
"
:
                
dirpath
=
dirpath
.
replace
(
path_sep
b
"
/
"
)
            
keep_dirs
=
[
]
            
keep_files
=
[
]
            
for
iter_items
literals
patterns
target
suffix
in
[
                    
(
dirnames
self
.
literals_dir
self
.
patterns_dir
keep_dirs
b
"
/
"
)
                    
(
filenames
self
.
literals_file
self
.
patterns_file
keep_files
b
"
"
)
]
:
                
for
item
in
iter_items
:
                    
name
=
item
[
0
]
                    
if
dirpath
:
                        
path
=
b
"
%
s
/
%
s
"
%
(
dirpath
name
)
+
suffix
                    
else
:
                        
path
=
name
+
suffix
                    
if
path
in
self
.
cache
:
                        
if
not
self
.
cache
[
path
]
:
                            
target
.
append
(
item
)
                        
continue
                    
for
rule_dir
in
[
None
dirpath
if
dirpath
!
=
b
"
.
"
else
b
"
"
]
:
                        
if
name
in
literals
.
get
(
rule_dir
empty
)
:
                            
exclude
=
literals
[
rule_dir
]
[
name
]
                            
if
not
any
(
rule
.
match
(
name
if
name_only
else
path
)
                                       
for
name_only
rule
in
exclude
)
:
                                
self
.
cache
[
path
]
=
True
                                
break
                    
else
:
                        
for
(
component_only
pattern
)
exclude
in
patterns
:
                            
if
component_only
:
                                
match
=
pattern
.
match
(
name
)
                            
else
:
                                
match
=
pattern
.
match
(
path
)
                            
if
match
:
                                
if
not
any
(
rule
.
match
(
name
if
name_only
else
path
)
                                           
for
name_only
rule
in
exclude
)
:
                                    
self
.
cache
[
path
]
=
True
                                    
break
                        
else
:
                            
self
.
cache
[
path
]
=
False
                            
target
.
append
(
item
)
            
dirnames
[
:
]
=
keep_dirs
            
assert
not
any
(
b
"
.
git
"
=
=
name
for
name
_
in
dirnames
)
            
yield
orig_dirpath
dirnames
keep_files
    
def
__call__
(
self
                 
iterator
                 
)
:
        
if
self
.
trivial
:
            
return
iterator
        
return
self
.
filter
(
iterator
)
def
has_ignore
(
dirpath
)
:
    
return
os
.
path
.
exists
(
os
.
path
.
join
(
dirpath
b
"
.
gitignore
"
)
)
