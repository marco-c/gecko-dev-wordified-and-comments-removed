import
json
import
os
import
re
KEY_XRE
=
"
{
xre
}
"
DEFAULT_DURATION
=
100
.
0
class
Allowlist
:
    
PRE_PROFILE
=
"
"
    
def
__init__
(
        
self
        
test_name
        
paths
        
path_substitutions
        
name_substitutions
        
event_sources
=
None
        
init_with
=
None
    
)
:
        
self
.
test_name
=
test_name
        
self
.
listmap
=
init_with
if
init_with
else
{
}
        
self
.
dependent_libs
=
(
            
self
.
load_dependent_libs
(
)
if
init_with
and
KEY_XRE
in
paths
else
{
}
        
)
        
self
.
paths
=
paths
        
self
.
path_substitutions
=
path_substitutions
        
self
.
name_substitutions
=
name_substitutions
        
self
.
expected_event_sources
=
event_sources
or
[
]
    
def
load
(
self
filename
)
:
        
if
not
self
.
load_dependent_libs
(
)
:
            
return
False
        
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
fHandle
:
                
temp
=
json
.
load
(
fHandle
)
            
for
allowlist_name
in
temp
:
                
self
.
listmap
[
allowlist_name
.
lower
(
)
]
=
temp
[
allowlist_name
]
        
except
IOError
as
e
:
            
print
(
"
%
s
:
%
s
"
%
(
e
.
filename
e
.
strerror
)
)
            
return
False
        
return
True
    
def
sanitize_filename
(
self
filename
)
:
        
filename
=
filename
.
lower
(
)
        
filename
.
replace
(
"
(
x86
)
"
"
"
)
        
for
path
subst
in
self
.
path_substitutions
.
items
(
)
:
            
parts
=
filename
.
split
(
path
)
            
if
len
(
parts
)
>
=
2
:
                
if
self
.
PRE_PROFILE
=
=
"
"
and
subst
=
=
"
{
profile
}
"
:
                    
fname
=
self
.
sanitize_filename
(
parts
[
0
]
)
                    
self
.
listmap
[
fname
]
=
{
}
                    
self
.
listmap
[
fname
]
=
{
}
                    
if
not
fname
.
endswith
(
"
~
1
"
)
:
                        
dirs
=
fname
.
split
(
"
\
\
"
)
                        
dirs
[
-
1
]
=
"
%
s
~
1
"
%
(
dirs
[
-
1
]
[
:
6
]
)
                        
diter
=
2
                        
while
diter
<
len
(
dirs
)
:
                            
self
.
listmap
[
"
\
\
"
.
join
(
dirs
[
:
diter
]
)
]
=
{
}
                            
diter
=
diter
+
1
                        
self
.
PRE_PROFILE
=
fname
                
filename
=
"
%
s
%
s
"
%
(
subst
path
.
join
(
parts
[
1
:
]
)
)
        
for
old_name
new_name
in
self
.
name_substitutions
.
items
(
)
:
            
if
isinstance
(
old_name
re
.
Pattern
)
:
                
filename
=
re
.
sub
(
old_name
new_name
filename
)
            
else
:
                
parts
=
filename
.
split
(
old_name
)
                
if
len
(
parts
)
>
=
2
:
                    
filename
=
"
%
s
%
s
"
%
(
parts
[
0
]
new_name
)
        
return
filename
.
strip
(
"
/
\
\
\
\
t
"
)
    
def
check
(
self
test
file_name_index
event_source_index
=
None
)
:
        
errors
=
{
}
        
for
row_key
in
test
.
keys
(
)
:
            
filename
=
self
.
sanitize_filename
(
row_key
[
file_name_index
]
)
            
if
filename
in
self
.
listmap
:
                
if
(
                    
"
ignore
"
in
self
.
listmap
[
filename
]
                    
and
self
.
listmap
[
filename
]
[
"
ignore
"
]
                
)
:
                    
continue
            
elif
filename
in
self
.
dependent_libs
:
                
continue
            
elif
(
                
event_source_index
is
not
None
                
and
row_key
[
event_source_index
]
in
self
.
expected_event_sources
            
)
:
                
continue
            
else
:
                
if
filename
not
in
errors
:
                    
errors
[
filename
]
=
[
]
                
errors
[
filename
]
.
append
(
test
[
row_key
]
)
        
return
errors
    
def
checkDuration
(
self
test
file_name_index
file_duration_index
)
:
        
errors
=
{
}
        
for
idx
(
row_key
row_value
)
in
enumerate
(
test
.
items
(
)
)
:
            
if
row_value
[
file_duration_index
]
>
DEFAULT_DURATION
:
                
filename
=
self
.
sanitize_filename
(
row_key
[
file_name_index
]
)
                
if
(
                    
filename
in
self
.
listmap
                    
and
"
ignoreduration
"
in
self
.
listmap
[
filename
]
                
)
:
                    
if
(
                        
row_value
[
file_duration_index
]
                        
<
=
self
.
listmap
[
filename
]
[
"
ignoreduration
"
]
                    
)
:
                        
continue
                
if
filename
not
in
errors
:
                    
errors
[
filename
]
=
[
]
                
errors
[
filename
]
.
append
(
                    
"
Duration
%
s
>
%
s
"
%
(
row_value
[
file_duration_index
]
)
                    
DEFAULT_DURATION
                
)
        
return
errors
    
def
filter
(
self
test
file_name_index
)
:
        
for
row_key
in
test
.
keys
(
)
:
            
filename
=
self
.
sanitize_filename
(
row_key
[
file_name_index
]
)
            
if
filename
in
self
.
listmap
:
                
if
(
                    
"
ignore
"
in
self
.
listmap
[
filename
]
                    
and
self
.
listmap
[
filename
]
[
"
ignore
"
]
                
)
:
                    
del
test
[
row_key
]
                    
continue
            
elif
filename
in
self
.
dependent_libs
:
                
del
test
[
row_key
]
                
continue
    
staticmethod
    
def
get_error_strings
(
errors
)
:
        
error_strs
=
[
]
        
for
filename
data
in
errors
.
items
(
)
:
            
for
datum
in
data
:
                
error_strs
.
append
(
                    
"
File
'
%
s
'
was
accessed
and
we
were
not
"
                    
"
expecting
it
:
%
r
"
%
(
filename
datum
)
                
)
        
return
error_strs
    
def
print_errors
(
self
error_strs
)
:
        
for
error_msg
in
error_strs
:
            
print
(
"
TEST
-
UNEXPECTED
-
FAIL
|
%
s
|
%
s
"
%
(
self
.
test_name
error_msg
)
)
    
def
load_dependent_libs
(
self
)
:
        
filename
=
"
%
s
%
sdependentlibs
.
list
"
%
(
self
.
paths
[
KEY_XRE
]
os
.
path
.
sep
)
        
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
                
libs
=
f
.
readlines
(
)
            
self
.
dependent_libs
=
{
                
"
%
s
%
s
%
s
"
%
(
KEY_XRE
os
.
path
.
sep
lib
.
strip
(
)
)
:
{
"
ignore
"
:
True
}
                
for
lib
in
libs
            
}
            
return
True
        
except
IOError
as
e
:
            
print
(
"
%
s
:
%
s
"
%
(
e
.
filename
e
.
strerror
)
)
            
return
False
