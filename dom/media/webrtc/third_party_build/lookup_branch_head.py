import
argparse
import
json
import
os
import
pathlib
import
sys
import
urllib
.
request
default_cache_path
=
"
.
moz
-
fast
-
forward
/
milestone
.
cache
"
def
fetch_branch_head_dict
(
)
:
    
milestone_url
=
(
        
"
https
:
/
/
chromiumdash
.
appspot
.
com
/
fetch_milestones
?
only_branched
=
true
"
    
)
    
uf
=
urllib
.
request
.
urlopen
(
milestone_url
)
    
html
=
uf
.
read
(
)
    
milestone_dict
=
json
.
loads
(
html
)
    
new_dict
=
{
}
    
for
row
in
milestone_dict
:
        
new_dict
[
row
[
"
milestone
"
]
]
=
row
[
"
webrtc_branch
"
]
    
return
new_dict
def
fetch_branch_schedule_dict
(
)
:
    
milestone_schedule_url
=
(
        
"
https
:
/
/
chromiumdash
.
appspot
.
com
/
fetch_milestone_schedule
?
offset
=
-
1
&
n
=
4
"
    
)
    
uf
=
urllib
.
request
.
urlopen
(
milestone_schedule_url
)
    
html
=
uf
.
read
(
)
    
schedule_dict
=
json
.
loads
(
html
)
    
new_dict
=
{
}
    
for
row
in
schedule_dict
[
"
mstones
"
]
:
        
new_dict
[
row
[
"
mstone
"
]
]
=
row
[
"
branch_point
"
]
    
return
new_dict
def
get_branch_date
(
milestone
)
:
    
milestone_dates
=
{
}
    
try
:
        
milestone_dates
=
fetch_branch_schedule_dict
(
)
    
except
Exception
:
        
pass
    
if
milestone
in
milestone_dates
:
        
return
milestone_dates
[
milestone
]
    
return
None
def
read_dict_from_cache
(
cache_path
)
:
    
if
cache_path
is
not
None
and
os
.
path
.
exists
(
cache_path
)
:
        
with
open
(
cache_path
)
as
ifile
:
            
return
json
.
loads
(
ifile
.
read
(
)
object_hook
=
jsonKeys2int
)
    
return
{
}
def
write_dict_to_cache
(
cache_path
milestones
)
:
    
with
open
(
cache_path
"
w
"
)
as
ofile
:
        
ofile
.
write
(
json
.
dumps
(
milestones
)
)
def
get_branch_head
(
milestone
cache_path
=
default_cache_path
)
:
    
milestones
=
read_dict_from_cache
(
cache_path
)
    
if
milestone
not
in
milestones
:
        
try
:
            
milestones
=
fetch_branch_head_dict
(
)
            
write_dict_to_cache
(
cache_path
milestones
)
        
except
Exception
:
            
pass
    
if
milestone
in
milestones
:
        
return
milestones
[
milestone
]
    
return
None
def
jsonKeys2int
(
x
)
:
    
if
isinstance
(
x
dict
)
:
        
return
{
int
(
k
)
:
v
for
k
v
in
x
.
items
(
)
}
    
return
x
if
__name__
=
=
"
__main__
"
:
    
parser
=
argparse
.
ArgumentParser
(
        
description
=
"
Get
libwebrtc
branch
-
head
for
given
chromium
milestone
"
    
)
    
parser
.
add_argument
(
        
"
milestone
"
type
=
int
help
=
"
integer
chromium
milestone
(
example
:
106
)
"
    
)
    
parser
.
add_argument
(
"
-
v
"
"
-
-
verbose
"
action
=
"
store_true
"
)
    
parser
.
add_argument
(
"
-
c
"
"
-
-
cache
"
type
=
pathlib
.
Path
help
=
"
path
to
cache
file
"
)
    
args
=
parser
.
parse_args
(
)
    
local_cache_path
=
args
.
cache
or
default_cache_path
    
branch_head
=
get_branch_head
(
args
.
milestone
local_cache_path
)
    
if
branch_head
is
None
:
        
sys
.
exit
(
f
"
error
:
chromium
milestone
'
{
args
.
milestone
}
'
is
not
found
.
"
)
    
if
args
.
verbose
:
        
print
(
f
"
chromium
milestone
{
args
.
milestone
}
uses
branch
-
heads
/
{
branch_head
}
"
)
    
else
:
        
print
(
branch_head
)
