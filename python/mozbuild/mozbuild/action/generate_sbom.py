"
"
"
Generate
a
CycloneDX
software
bill
of
materials
for
the
tree
.
generate
(
)
is
shared
by
mach
sbom
and
by
the
py_action
the
build
'
s
sbom
step
runs
so
the
document
a
build
uploads
is
the
one
the
command
produces
.
"
"
"
import
argparse
import
os
import
sys
def
generate
(
topsrcdir
topobjdir
repo
output
=
None
version
=
None
strict
=
False
)
:
    
"
"
"
Write
the
SBOM
to
output
or
to
stdout
.
Returns
a
process
exit
code
.
    
topobjdir
may
name
a
directory
that
holds
no
licenses
.
json
in
which
    
case
the
document
is
built
from
the
moz
.
yaml
manifests
alone
.
    
"
"
"
    
from
mozbuild
.
vendor
.
sbom
import
(
        
collect_records
        
load_license_notices
        
merge_license_notices
    
)
    
from
mozbuild
.
vendor
.
sbom_cargo
import
collect_dependency_kinds
crate_records
    
from
mozbuild
.
vendor
.
sbom_cyclonedx
import
build_bom
to_json
utc_timestamp
    
def
log
(
message
)
:
        
print
(
message
file
=
sys
.
stderr
)
    
records
errors
=
collect_records
(
repo
topsrcdir
log
=
log
)
    
if
errors
and
strict
:
        
log
(
f
"
{
len
(
errors
)
}
manifest
(
s
)
failed
to
load
.
"
)
        
return
1
    
kinds
=
collect_dependency_kinds
(
topsrcdir
topobjdir
)
    
crates
_
=
crate_records
(
topsrcdir
kinds
=
kinds
)
    
records
.
extend
(
crates
)
    
if
kinds
:
        
shipped
=
sum
(
1
for
c
in
crates
if
{
"
normal
"
"
build
"
}
&
set
(
c
[
"
kinds
"
]
)
)
        
dev_only
=
sum
(
1
for
c
in
crates
if
c
[
"
kinds
"
]
=
=
[
"
dev
"
]
)
        
log
(
            
f
"
{
len
(
crates
)
}
crates
:
{
shipped
}
built
into
the
product
"
            
f
"
{
dev_only
}
test
-
only
"
            
f
"
{
len
(
crates
)
-
shipped
-
dev_only
}
not
reached
by
cargo
metadata
.
"
        
)
    
else
:
        
log
(
            
"
cargo
metadata
unavailable
;
crate
dependency
kinds
not
collected
.
"
        
)
    
notices
=
load_license_notices
(
os
.
path
.
join
(
topobjdir
"
licenses
.
json
"
)
)
    
if
notices
:
        
merge_license_notices
(
records
notices
)
    
else
:
        
log
(
            
"
licenses
.
json
not
found
;
run
.
/
mach
build
-
backend
for
license
data
.
"
        
)
    
if
version
is
None
:
        
with
open
(
            
os
.
path
.
join
(
topsrcdir
"
browser
"
"
config
"
"
version_display
.
txt
"
)
            
encoding
=
"
utf
-
8
"
        
)
as
version_file
:
            
version
=
version_file
.
read
(
)
.
strip
(
)
    
source_revision
=
repo
.
head_rev
    
source_date_epoch
=
os
.
environ
.
get
(
"
SOURCE_DATE_EPOCH
"
)
    
if
source_date_epoch
:
        
try
:
            
commit_time
=
int
(
source_date_epoch
)
        
except
ValueError
:
            
log
(
                
"
SOURCE_DATE_EPOCH
must
be
an
integer
number
of
seconds
since
"
                
f
"
the
epoch
not
{
source_date_epoch
!
r
}
.
"
            
)
            
return
1
    
else
:
        
commit_time
=
repo
.
get_commit_time
(
)
or
0
    
timestamp
=
utc_timestamp
(
commit_time
)
    
unrecognized
=
[
]
    
records
.
sort
(
key
=
lambda
record
:
record
[
"
bom_ref
"
]
)
    
bom
=
build_bom
(
        
records
version
source_revision
timestamp
unrecognized
=
unrecognized
    
)
    
document
=
to_json
(
bom
)
    
if
unrecognized
:
        
log
(
            
f
"
{
len
(
unrecognized
)
}
license
value
(
s
)
are
neither
an
SPDX
id
nor
"
            
"
an
expression
and
are
recorded
as
free
text
:
"
            
f
"
{
'
'
.
join
(
sorted
(
set
(
unrecognized
)
)
)
}
.
"
        
)
    
if
output
:
        
with
open
(
output
"
w
"
encoding
=
"
utf
-
8
"
newline
=
"
\
n
"
)
as
output_file
:
            
output_file
.
write
(
document
)
        
log
(
            
f
"
Wrote
{
len
(
records
)
}
components
(
{
len
(
crates
)
}
crates
"
            
f
"
{
len
(
notices
)
}
license
notices
)
to
{
output
}
.
"
        
)
    
else
:
        
sys
.
stdout
.
write
(
document
)
    
return
0
def
main
(
argv
)
:
    
import
buildconfig
    
from
mozversioncontrol
import
get_repository_object
    
parser
=
argparse
.
ArgumentParser
(
description
=
__doc__
)
    
parser
.
add_argument
(
"
output
"
help
=
"
Write
the
SBOM
here
.
"
)
    
parser
.
add_argument
(
        
"
-
-
strict
"
        
action
=
"
store_true
"
        
help
=
"
Exit
non
-
zero
if
any
moz
.
yaml
fails
to
load
.
"
    
)
    
args
=
parser
.
parse_args
(
argv
)
    
return
generate
(
        
buildconfig
.
topsrcdir
        
buildconfig
.
topobjdir
        
get_repository_object
(
buildconfig
.
topsrcdir
)
        
output
=
args
.
output
        
strict
=
args
.
strict
    
)
if
__name__
=
=
"
__main__
"
:
    
sys
.
exit
(
main
(
sys
.
argv
[
1
:
]
)
)
