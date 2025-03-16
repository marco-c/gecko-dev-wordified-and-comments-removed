import
argparse
import
json
def
compute_differences
(
)
:
    
data_old
=
None
    
data_new
=
None
    
with
open
(
"
IdnaTestV2
-
old
.
json
"
"
r
"
)
as
file_handle
:
        
data_old
=
json
.
load
(
file_handle
)
    
with
open
(
"
IdnaTestV2
-
new
.
json
"
"
r
"
)
as
file_handle
:
        
data_new
=
json
.
load
(
file_handle
)
    
added_tests
=
[
]
    
changed_tests
=
[
]
    
removed_tests
=
[
]
    
for
old_test
in
data_old
:
        
if
isinstance
(
old_test
str
)
:
            
continue
        
found
=
None
        
for
new_test
in
data_new
:
            
if
isinstance
(
new_test
str
)
:
                
continue
            
if
old_test
[
"
input
"
]
=
=
new_test
[
"
input
"
]
:
                
found
=
new_test
                
break
        
if
not
found
:
            
if
"
?
"
not
in
old_test
[
"
input
"
]
:
                
removed_tests
.
append
(
old_test
)
        
elif
old_test
[
"
output
"
]
!
=
found
[
"
output
"
]
and
old_test
[
"
output
"
]
:
            
changed_tests
.
append
(
{
"
input
"
:
old_test
[
"
input
"
]
"
output_old
"
:
old_test
[
"
output
"
]
"
output_new
"
:
found
[
"
output
"
]
}
)
    
for
new_test
in
data_new
:
        
if
isinstance
(
new_test
str
)
:
            
continue
        
found
=
False
        
for
old_test
in
data_old
:
            
if
isinstance
(
old_test
str
)
:
                
continue
            
if
new_test
[
"
input
"
]
=
=
old_test
[
"
input
"
]
:
                
found
=
True
                
break
        
if
not
found
:
            
added_tests
.
append
(
new_test
)
    
return
{
"
added
"
:
added_tests
"
changed
"
:
changed_tests
"
removed
"
:
removed_tests
}
def
main
(
)
:
    
parser
=
argparse
.
ArgumentParser
(
epilog
=
"
Thanks
for
caring
about
IDNA
!
"
)
    
group
=
parser
.
add_mutually_exclusive_group
(
required
=
True
)
    
group
.
add_argument
(
"
-
-
differences
"
action
=
"
store_true
"
help
=
"
Output
the
differences
"
)
    
group
.
add_argument
(
"
-
-
removed
"
action
=
"
store_true
"
help
=
"
Output
the
removed
tests
only
"
)
    
args
=
parser
.
parse_args
(
)
    
differences
=
compute_differences
(
)
    
output
=
None
    
if
args
.
differences
:
        
output
=
differences
    
elif
args
.
removed
:
        
output
=
differences
[
"
removed
"
]
    
print
(
json
.
dumps
(
output
sort_keys
=
True
allow_nan
=
False
indent
=
2
separators
=
(
'
'
'
:
'
)
)
)
main
(
)
