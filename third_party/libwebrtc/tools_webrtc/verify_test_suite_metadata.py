"
"
"
Verifies
that
rtc_test_suite
targets
contribute
'
rtc_cc_test
'
metadata
.
This
ensures
that
rtc_test_suite
aggregates
valid
rtc_cc_test
targets
.
"
"
"
import
json
import
sys
def
main
(
)
:
    
if
len
(
sys
.
argv
)
!
=
3
:
        
print
(
"
Usage
:
verify_test_suite_metadata
.
py
<
metadata_map_json
>
"
              
"
<
output_stamp
>
"
)
        
return
1
    
map_path
=
sys
.
argv
[
1
]
    
output_stamp
=
sys
.
argv
[
2
]
    
try
:
        
with
open
(
map_path
'
r
'
encoding
=
'
utf
-
8
'
)
as
map_file
:
            
check_map
=
json
.
load
(
map_file
)
    
except
Exception
as
error
:
        
print
(
f
"
Error
reading
input
map
file
:
{
error
}
"
)
        
return
1
    
missing_unittests
=
[
]
    
for
item
in
check_map
:
        
label
=
item
[
'
label
'
]
        
output_file
=
item
[
'
output
'
]
        
try
:
            
with
open
(
output_file
'
r
'
encoding
=
'
utf
-
8
'
)
as
metadata_file
:
                
unittests
=
json
.
load
(
metadata_file
)
                
is_valid
=
any
(
m
.
get
(
'
label
'
)
=
=
label
for
m
in
unittests
)
                
if
not
is_valid
:
                    
missing_unittests
.
append
(
label
)
        
except
Exception
as
error
:
            
print
(
                
f
"
Error
reading
generated
metadata
file
for
{
label
}
:
{
error
}
"
)
            
return
1
    
if
missing_unittests
:
        
lines
=
[
            
"
Error
:
The
following
targets
in
rtc_test_suite
are
not
"
            
"
rtc_cc_test
targets
:
"
        
]
        
for
missing_test
in
sorted
(
missing_unittests
)
:
            
lines
.
append
(
f
"
{
missing_test
}
"
)
        
lines
.
append
(
            
"
\
nEnsure
these
targets
are
rtc_cc_test
targets
themselves
.
"
)
        
print
(
'
\
n
'
.
join
(
lines
)
)
        
return
1
    
with
open
(
output_stamp
'
w
'
encoding
=
'
utf
-
8
'
)
as
stamp_file
:
        
stamp_file
.
write
(
"
OK
"
)
    
return
0
if
__name__
=
=
'
__main__
'
:
    
sys
.
exit
(
main
(
)
)
