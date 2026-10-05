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
configured
tree
.
generate_file
is
the
GENERATED_FILES
entry
point
the
build
uses
so
the
document
is
produced
from
the
objdir
that
built
the
product
by
the
same
build
graph
that
produces
everything
else
.
mach
sbom
calls
generate
(
)
which
is
also
how
an
unconfigured
tree
gets
the
moz
.
yaml
-
only
subset
.
"
"
"
import
os
import
sys
class
SbomError
(
Exception
)
:
    
"
"
"
A
condition
that
must
not
silently
shrink
the
document
.
"
"
"
def
_source_revision_and_time
(
repo
)
:
    
from
mozbuild
.
vendor
.
sbom_cyclonedx
import
utc_timestamp
    
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
            
raise
SbomError
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
    
return
source_revision
utc_timestamp
(
commit_time
)
def
_serialize
(
records
version
repo
log
*
*
bom_arguments
)
:
    
"
"
"
Sort
the
records
and
return
the
CycloneDX
document
as
a
JSON
string
.
"
"
"
    
from
mozbuild
.
vendor
.
sbom_cyclonedx
import
build_bom
to_json
    
source_revision
timestamp
=
_source_revision_and_time
(
repo
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
    
document
=
to_json
(
        
build_bom
(
            
records
            
version
            
source_revision
            
timestamp
            
unrecognized
=
unrecognized
            
*
*
bom_arguments
        
)
    
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
    
return
document
def
_product_identity
(
topsrcdir
substs
product_name
version
)
:
    
"
"
"
Default
the
root
component
'
s
name
and
version
from
the
configuration
.
"
"
"
    
if
product_name
is
None
:
        
product_name
=
substs
.
get
(
"
MOZ_APP_BASENAME
"
)
or
"
Firefox
"
    
if
version
is
None
:
        
version
=
substs
.
get
(
"
MOZ_APP_VERSION_DISPLAY
"
)
or
substs
.
get
(
"
MOZ_APP_VERSION
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
    
return
product_name
version
def
build_tooling_document
(
    
topsrcdir
repo
substs
=
None
version
=
None
product_name
=
None
log
=
None
)
:
    
"
"
"
Return
the
SBOM
of
what
builds
and
tests
the
product
as
a
JSON
string
.
    
The
product
document
describes
what
ships
;
this
one
describes
the
    
third
-
party
code
the
tree
runs
to
get
there
which
ships
in
nothing
but
is
    
as
much
a
supply
-
chain
input
.
The
build
does
not
generate
it
.
    
"
"
"
    
from
mozbuild
.
vendor
.
sbom_npm
import
npm_records
    
from
mozbuild
.
vendor
.
sbom_python
import
python_records
    
log
=
log
or
(
lambda
message
:
None
)
    
records
dependencies
=
npm_records
(
topsrcdir
dev
=
True
)
    
log
(
f
"
{
len
(
records
)
}
npm
packages
that
only
build
the
bundles
.
"
)
    
packages
python_edges
=
python_records
(
topsrcdir
)
    
records
.
extend
(
packages
)
    
dependencies
.
update
(
python_edges
)
    
log
(
f
"
{
len
(
packages
)
}
vendored
Python
packages
.
"
)
    
product_name
version
=
_product_identity
(
        
topsrcdir
substs
or
{
}
product_name
version
    
)
    
return
_serialize
(
        
records
        
version
        
repo
        
log
        
product_name
=
product_name
        
dependencies
=
dependencies
        
build_tooling
=
True
    
)
def
build_gradle_document
(
    
runtime_dependencies
repo
product_name
version
=
None
log
=
None
)
:
    
"
"
"
Return
the
SBOM
of
a
Gradle
application
'
s
runtime
closure
as
a
JSON
string
.
"
"
"
    
from
mozbuild
.
vendor
.
sbom_gradle
import
GradleSbomError
gradle_records
    
log
=
log
or
(
lambda
message
:
None
)
    
try
:
        
records
edges
gradle_version
=
gradle_records
(
runtime_dependencies
)
    
except
GradleSbomError
as
error
:
        
raise
SbomError
(
str
(
error
)
)
    
version
=
version
or
gradle_version
    
if
not
version
:
        
raise
SbomError
(
f
"
{
runtime_dependencies
}
names
no
version
;
pass
one
.
"
)
    
document
=
_serialize
(
        
records
version
repo
log
product_name
=
product_name
dependencies
=
edges
    
)
    
log
(
f
"
{
len
(
records
)
}
Maven
packages
in
{
product_name
}
{
version
}
.
"
)
    
return
document
def
build_document
(
    
topsrcdir
    
topobjdir
    
repo
    
substs
=
None
    
version
=
None
    
product_name
=
None
    
strict
=
False
    
log
=
None
)
:
    
"
"
"
Return
the
SBOM
as
a
JSON
string
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
substs
    
is
empty
for
an
unconfigured
tree
.
Raises
SbomError
where
strict
    
asks
for
a
hard
failure
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
        
components_for_unmatched
        
load_license_notices
        
merge_license_notices
        
unattached_notices
    
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
sbom_gradle
import
(
        
RUNTIME_DEPENDENCIES
        
GradleSbomError
        
gradle_records
    
)
    
from
mozbuild
.
vendor
.
sbom_npm
import
npm_records
upgrade_manifest_purls
    
from
mozbuild
.
vendor
.
sbom_python
import
VENDOR_DIR
as
PYTHON_VENDOR_DIR
    
substs
=
substs
or
{
}
    
log
=
log
or
(
lambda
message
:
None
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
        
raise
SbomError
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
    
records
=
[
        
record
        
for
record
in
records
        
if
not
record
[
"
bom_ref
"
]
.
startswith
(
PYTHON_VENDOR_DIR
+
"
/
"
)
    
]
    
kinds
=
collect_dependency_kinds
(
topsrcdir
topobjdir
substs
.
get
(
"
CARGO
"
)
log
=
log
)
    
crates
dependencies
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
    
packages
npm_edges
=
npm_records
(
topsrcdir
)
    
records
.
extend
(
packages
)
    
dependencies
.
update
(
npm_edges
)
    
upgraded
=
upgrade_manifest_purls
(
records
topsrcdir
)
    
log
(
        
f
"
{
len
(
packages
)
}
npm
packages
bundled
into
the
product
"
        
"
(
dev
-
only
dependencies
excluded
)
;
"
        
f
"
{
upgraded
}
vendored
manifest
(
s
)
given
a
pkg
:
npm
purl
.
"
    
)
    
maven
=
[
]
    
if
substs
.
get
(
"
MOZ_BUILD_APP
"
)
=
=
"
mobile
/
android
"
:
        
try
:
            
maven
maven_edges
_
=
gradle_records
(
                
os
.
path
.
join
(
topobjdir
RUNTIME_DEPENDENCIES
)
            
)
        
except
GradleSbomError
as
error
:
            
if
strict
:
                
raise
SbomError
(
str
(
error
)
)
            
log
(
f
"
{
error
}
;
build
the
tree
for
the
Maven
dependencies
.
"
)
        
else
:
            
records
.
extend
(
maven
)
            
dependencies
.
update
(
maven_edges
)
            
log
(
f
"
{
len
(
maven
)
}
Maven
packages
in
GeckoView
'
s
runtime
closure
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
        
records
.
extend
(
            
components_for_unmatched
(
                
records
                
notices
                
lambda
path
:
os
.
path
.
isfile
(
os
.
path
.
join
(
topsrcdir
path
)
)
            
)
        
)
        
product_notices
=
unattached_notices
(
records
notices
)
    
else
:
        
product_notices
=
[
]
        
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
    
product_name
version
=
_product_identity
(
topsrcdir
substs
product_name
version
)
    
document
=
_serialize
(
        
records
        
version
        
repo
        
log
        
product_notices
=
product_notices
        
product_name
=
product_name
        
dependencies
=
dependencies
    
)
    
log
(
        
f
"
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
packages
)
}
npm
packages
{
len
(
maven
)
}
Maven
packages
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
.
"
    
)
    
return
document
def
generate
(
    
topsrcdir
    
topobjdir
    
repo
    
substs
=
None
    
output
=
None
    
version
=
None
    
product_name
=
None
    
strict
=
False
    
gradle_runtime_dependencies
=
None
    
build_tooling
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
    
With
gradle_runtime_dependencies
the
document
describes
that
Gradle
    
application
rather
than
the
tree
;
with
build_tooling
what
builds
and
    
tests
the
tree
rather
than
what
it
ships
.
    
"
"
"
    
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
    
try
:
        
if
gradle_runtime_dependencies
and
build_tooling
:
            
raise
SbomError
(
                
"
-
-
gradle
-
runtime
-
dependencies
and
-
-
build
-
tooling
each
"
                
"
describe
a
different
document
.
"
            
)
        
if
strict
and
(
gradle_runtime_dependencies
or
build_tooling
)
:
            
raise
SbomError
(
                
"
-
-
strict
applies
to
the
manifests
the
product
document
reads
.
"
            
)
        
if
build_tooling
:
            
document
=
build_tooling_document
(
                
topsrcdir
                
repo
                
substs
=
substs
                
version
=
version
                
product_name
=
product_name
                
log
=
log
            
)
        
elif
gradle_runtime_dependencies
:
            
if
not
product_name
:
                
raise
SbomError
(
"
A
Gradle
application
'
s
SBOM
needs
a
product
name
.
"
)
            
document
=
build_gradle_document
(
                
gradle_runtime_dependencies
                
repo
                
product_name
                
version
=
version
                
log
=
log
            
)
        
else
:
            
document
=
build_document
(
                
topsrcdir
                
topobjdir
                
repo
                
substs
=
substs
                
version
=
version
                
product_name
=
product_name
                
strict
=
strict
                
log
=
log
            
)
    
except
SbomError
as
error
:
        
log
(
str
(
error
)
)
        
return
1
    
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
the
SBOM
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
generate_file
(
output
)
:
    
"
"
"
GENERATED_FILES
entry
point
wired
up
from
the
top
-
level
moz
.
build
.
    
Strict
:
a
moz
.
yaml
the
SBOM
cannot
parse
is
a
hole
in
the
document
and
a
    
build
that
ships
one
should
fail
rather
than
describe
less
than
it
ships
.
    
"
"
"
    
import
buildconfig
    
from
mozversioncontrol
import
get_repository_object
    
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
    
output
.
write
(
        
build_document
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
            
substs
=
buildconfig
.
substs
            
strict
=
True
            
log
=
log
        
)
    
)
