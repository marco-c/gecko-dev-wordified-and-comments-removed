import
copy
import
errno
import
hashlib
import
json
import
logging
import
os
import
re
import
subprocess
import
typing
from
collections
import
defaultdict
from
itertools
import
dropwhile
from
pathlib
import
Path
import
mozpack
.
path
as
mozpath
import
toml
import
tomlkit
from
looseversion
import
LooseVersion
from
mozboot
.
util
import
MINIMUM_RUST_VERSION
from
mozbuild
.
base
import
BuildEnvironmentNotFoundException
MozbuildObject
if
typing
.
TYPE_CHECKING
:
    
import
datetime
TomlItem
=
typing
.
Union
[
    
str
    
list
[
"
TomlItem
"
]
    
dict
[
str
"
TomlItem
"
]
    
bool
    
int
    
float
    
"
datetime
.
datetime
"
    
"
datetime
.
date
"
    
"
datetime
.
time
"
]
CARGO_CONFIG_TEMPLATE
=
"
"
"
\
#
This
file
contains
vendoring
instructions
for
cargo
.
#
It
was
generated
by
mach
vendor
rust
.
#
Please
do
not
edit
.
{
config
}
#
Take
advantage
of
the
fact
that
cargo
will
treat
lines
starting
with
#
#
as
comments
to
add
preprocessing
directives
.
This
file
can
thus
by
copied
#
as
-
is
to
topsrcdir
/
.
cargo
/
config
.
toml
with
no
preprocessing
to
be
used
there
#
(
for
e
.
g
.
independent
tasks
building
rust
code
)
or
be
preprocessed
by
#
the
build
system
to
produce
a
.
cargo
/
config
.
toml
with
the
right
content
.
#
define
REPLACE_NAME
{
replace_name
}
#
define
VENDORED_DIRECTORY
{
directory
}
#
We
explicitly
exclude
the
following
section
when
preprocessing
because
#
it
would
overlap
with
the
preprocessed
[
source
.
"
REPLACE_NAME
"
]
and
#
cargo
would
fail
.
#
ifndef
REPLACE_NAME
[
source
.
{
replace_name
}
]
directory
=
"
{
directory
}
"
#
endif
#
Thankfully
REPLACE_NAME
is
unlikely
to
be
a
legitimate
source
so
#
cargo
will
ignore
it
when
it
'
s
here
verbatim
.
#
filter
substitution
[
source
.
"
REPLACE_NAME
"
]
directory
=
"
top_srcdir
/
VENDORED_DIRECTORY
"
"
"
"
CARGO_LOCK_NOTICE
=
"
"
"
NOTE
:
cargo
vendor
may
have
made
changes
to
your
Cargo
.
lock
.
To
restore
your
Cargo
.
lock
to
the
HEAD
version
run
git
checkout
-
-
Cargo
.
lock
or
hg
revert
Cargo
.
lock
.
"
"
"
PACKAGES_WE_DONT_WANT
=
{
    
"
icu
"
:
"
Use
the
specific
ICU4X
crate
(
crates
whose
name
starts
with
icu_
)
instead
of
the
metacrate
.
"
    
"
rust_icu
"
:
"
Use
ICU4X
(
crates
whose
name
starts
with
icu_
)
instead
"
    
"
unic
"
:
"
Use
ICU4X
(
crates
whose
name
starts
with
icu_
)
instead
"
    
"
unicode
-
canonical
-
combining
-
class
"
:
"
Use
icu_normalizer
instead
"
    
"
unicode
-
case
-
mapping
"
:
"
Use
icu_casemap
instead
"
    
"
unicode
-
bidi
-
mirroring
"
:
"
Use
icu_properties
instead
"
    
"
unicode
-
ccc
"
:
"
Use
icu_normalizer
instead
"
    
"
unicode
-
general
-
category
"
:
"
Use
icu_properties
instead
"
    
"
unicode
-
id
"
:
"
Use
icu_properties
instead
"
    
"
unicode
-
id
-
start
"
:
"
Use
icu_properties
instead
"
    
"
unicode
-
joining
-
type
"
:
"
Use
icu_properties
instead
"
    
"
unicode
-
linebreak
"
:
"
Use
icu_segmenter
instead
"
    
"
unicode
-
normalization
"
:
"
Use
icu_normalizer
instead
"
    
"
unicode
-
properties
"
:
"
Use
icu_properties
instead
"
    
"
unicode
-
script
"
:
"
Use
icu_properties
instead
"
    
"
unicode
-
segmentation
"
:
"
Use
icu_segmenter
instead
"
    
"
unicode
-
xid
"
:
"
Use
icu_properties
instead
"
    
"
unicode_categories
"
:
"
Use
icu_properties
instead
"
    
"
unicode_names
"
:
"
Avoid
including
data
for
Unicode
character
names
"
    
"
unicode_names2
"
:
"
Avoid
including
data
for
Unicode
character
names
"
    
"
feruca
"
:
"
Use
icu_collator
instead
"
    
"
idna_mapping
"
:
"
Make
sure
to
use
a
version
of
idna_adapter
that
uses
ICU4X
"
    
"
unic
-
bidi
"
:
"
Use
unicode
-
bidi
instead
"
    
"
unic
-
idna
"
:
"
Use
idna
instead
"
    
"
unic
-
normal
"
:
"
Use
icu_normalizer
instead
"
    
"
unic
-
segment
"
:
"
Use
icu_segmenter
instead
"
    
"
unic
-
ucd
"
:
"
Use
icu_properties
instead
"
    
"
num
-
format
"
:
"
Use
icu_decimal
instead
"
    
"
encoding
"
:
"
Use
encoding_rs
instead
"
}
PREFIXES_WE_DONT_WANT
=
{
    
"
unicode
-
"
:
"
Use
ICU4X
(
crates
whose
name
starts
with
icu_
)
instead
"
    
"
unic
-
"
:
"
Use
ICU4X
(
crates
whose
name
starts
with
icu_
)
instead
"
    
"
rust_icu_
"
:
"
Use
ICU4X
(
crates
whose
name
starts
with
icu_
)
instead
"
    
"
unicode_
"
:
"
Use
ICU4X
(
crates
whose
name
starts
with
icu_
)
instead
"
}
ALLOWED_DESPITE_PREFIX
=
{
    
"
unicode
-
bidi
"
    
"
unicode
-
bidi
-
ffi
"
    
"
unicode
-
ident
"
    
"
unicode
-
width
"
    
"
unic
-
langid
"
    
"
unic
-
langid
-
ffi
"
    
"
unic
-
langid
-
impl
"
}
SEEN_ALLOWED_DESPITE_PREFIX
=
set
(
)
PACKAGES_WE_ALWAYS_WANT_AN_OVERRIDE_OF
=
[
    
"
autocfg
"
    
"
cmake
"
    
"
vcpkg
"
    
"
windows
"
    
"
windows
-
targets
"
]
def
dont_want_package
(
name
)
:
    
if
reason
:
=
PACKAGES_WE_DONT_WANT
.
get
(
name
)
:
        
return
reason
    
if
name
in
ALLOWED_DESPITE_PREFIX
:
        
SEEN_ALLOWED_DESPITE_PREFIX
.
add
(
name
)
        
return
None
    
for
prefix
reason
in
PREFIXES_WE_DONT_WANT
.
items
(
)
:
        
if
name
.
startswith
(
prefix
)
:
            
return
reason
class
VendorRust
(
MozbuildObject
)
:
    
def
__init__
(
self
*
args
*
*
kwargs
)
:
        
super
(
)
.
__init__
(
*
args
*
*
kwargs
)
        
self
.
_issues
=
[
]
    
def
serialize_issues_json
(
self
)
:
        
return
json
.
dumps
(
{
            
"
Cargo
.
lock
"
:
[
                
{
                    
"
path
"
:
"
Cargo
.
lock
"
                    
"
column
"
:
None
                    
"
line
"
:
None
                    
"
level
"
:
"
error
"
if
level
=
=
logging
.
ERROR
else
"
warning
"
                    
"
message
"
:
msg
                
}
                
for
(
level
msg
)
in
self
.
_issues
            
]
        
}
)
    
def
generate_diff_stream
(
self
)
:
        
return
self
.
repository
.
diff_stream
(
)
    
def
log
(
self
level
action
params
format_str
)
:
        
if
level
>
=
logging
.
WARNING
:
            
self
.
_issues
.
append
(
(
level
format_str
.
format
(
*
*
params
)
)
)
        
super
(
)
.
log
(
level
action
params
format_str
)
    
def
get_cargo_path
(
self
)
:
        
try
:
            
return
self
.
substs
[
"
CARGO
"
]
        
except
(
BuildEnvironmentNotFoundException
KeyError
)
:
            
if
"
MOZ_AUTOMATION
"
in
os
.
environ
:
                
cargo
=
os
.
path
.
join
(
                    
os
.
environ
[
"
MOZ_FETCHES_DIR
"
]
"
rustc
"
"
bin
"
"
cargo
"
                
)
                
assert
os
.
path
.
exists
(
cargo
)
                
return
cargo
            
from
mozfile
import
which
            
cargo
=
which
(
"
cargo
"
)
            
if
not
cargo
:
                
raise
OSError
(
                    
errno
.
ENOENT
                    
(
                        
"
Could
not
find
'
cargo
'
on
your
PATH
.
"
                        
"
Hint
:
have
you
run
mach
build
or
mach
configure
?
"
                    
)
                
)
            
return
cargo
    
def
cargo_version
(
self
cargo
)
:
        
out
=
(
            
subprocess
.
check_output
(
[
cargo
"
-
-
version
"
]
)
            
.
splitlines
(
)
[
0
]
            
.
decode
(
"
UTF
-
8
"
)
        
)
        
if
not
out
.
startswith
(
"
cargo
"
)
:
            
raise
RuntimeError
(
"
Unexpected
cargo
-
-
version
output
"
)
        
return
LooseVersion
(
out
.
split
(
)
[
1
]
)
    
def
check_cargo_version
(
self
cargo
)
:
        
"
"
"
        
Ensure
that
Cargo
is
new
enough
.
        
"
"
"
        
try
:
            
version
=
self
.
cargo_version
(
cargo
)
        
except
RuntimeError
:
            
return
False
        
minimum_rust_version
=
MINIMUM_RUST_VERSION
        
if
LooseVersion
(
"
1
.
85
.
0
"
)
>
=
MINIMUM_RUST_VERSION
:
            
minimum_rust_version
=
"
1
.
85
.
0
"
        
if
version
<
minimum_rust_version
:
            
self
.
log
(
                
logging
.
ERROR
                
"
cargo_version
"
                
{
}
                
f
"
Cargo
>
=
{
minimum_rust_version
}
required
(
install
Rust
{
minimum_rust_version
}
or
newer
)
"
            
)
            
return
False
        
self
.
log
(
logging
.
DEBUG
"
cargo_version
"
{
}
"
cargo
is
new
enough
"
)
        
return
True
    
def
has_modified_files
(
self
)
:
        
"
"
"
        
Ensure
that
there
aren
'
t
any
uncommitted
changes
to
files
        
in
the
working
copy
since
we
'
re
going
to
change
some
state
        
on
the
user
.
Allow
changes
to
Cargo
.
{
toml
lock
}
since
that
'
s
        
likely
to
be
a
common
use
case
.
        
"
"
"
        
modified
=
[
            
f
            
for
f
in
self
.
repository
.
get_changed_files
(
"
M
"
)
            
if
os
.
path
.
basename
(
f
)
not
in
(
"
Cargo
.
toml
"
"
Cargo
.
lock
"
)
            
and
not
f
.
startswith
(
"
supply
-
chain
/
"
)
        
]
        
if
modified
:
            
self
.
log
(
                
logging
.
ERROR
                
"
modified_files
"
                
{
}
                
"
"
"
You
have
uncommitted
changes
to
the
following
files
:
{
files
}
Please
commit
or
stash
these
changes
before
vendoring
or
re
-
run
with
-
-
ignore
-
modified
.
"
"
"
.
format
(
files
=
"
\
n
"
.
join
(
sorted
(
modified
)
)
)
            
)
        
return
modified
    
def
_ensure_cargo
(
self
)
:
        
"
"
"
        
Ensures
all
the
necessary
cargo
bits
are
installed
.
        
Returns
the
path
to
cargo
if
successful
None
otherwise
.
        
"
"
"
        
cargo
=
self
.
get_cargo_path
(
)
        
if
not
self
.
check_cargo_version
(
cargo
)
:
            
return
None
        
return
cargo
    
RUNTIME_LICENSE_WHITELIST
=
[
        
"
Apache
-
2
.
0
"
        
"
Apache
-
2
.
0
WITH
LLVM
-
exception
"
        
"
CC0
-
1
.
0
"
        
"
ISC
"
        
"
MIT
"
        
"
MPL
-
2
.
0
"
        
"
Unicode
-
3
.
0
"
        
"
Unicode
-
DFS
-
2016
"
        
"
Unlicense
"
        
"
Zlib
"
    
]
    
BUILDTIME_LICENSE_WHITELIST
=
{
        
"
BSD
-
3
-
Clause
"
:
[
            
"
bindgen
"
            
"
fuchsia
-
zircon
"
            
"
fuchsia
-
zircon
-
sys
"
            
"
fuchsia
-
cprng
"
            
"
glsl
"
            
"
instant
"
        
]
    
}
    
RUNTIME_LICENSE_PACKAGE_WHITELIST
=
{
        
"
BSD
-
2
-
Clause
"
:
[
            
"
arrayref
"
            
"
mach
"
            
"
qlog
"
        
]
        
"
BSD
-
3
-
Clause
"
:
[
            
"
subtle
"
            
"
uritemplate
-
next
"
        
]
    
}
    
ICU4X_LICENSE_SHA256
=
(
        
"
853f87c96f3d249f200fec6db1114427bc8bdf4afddc93c576956d78152ce978
"
    
)
    
RUNTIME_LICENSE_FILE_PACKAGE_WHITELIST
=
{
        
"
deque
"
:
"
6485b8ed310d3f0340bf1ad1f47645069ce4069dcc6bb46c7d5c6faf41de1fdb
"
        
"
fuchsia
-
cprng
"
:
"
03b114f53e6587a398931762ee11e2395bfdba252a329940e2c8c9e81813845b
"
        
"
icu_calendar
"
:
ICU4X_LICENSE_SHA256
        
"
icu_calendar_data
"
:
ICU4X_LICENSE_SHA256
        
"
icu_collections
"
:
ICU4X_LICENSE_SHA256
        
"
icu_locid
"
:
ICU4X_LICENSE_SHA256
        
"
icu_locid_transform
"
:
ICU4X_LICENSE_SHA256
        
"
icu_locid_transform_data
"
:
ICU4X_LICENSE_SHA256
        
"
icu_properties
"
:
ICU4X_LICENSE_SHA256
        
"
icu_properties_data
"
:
ICU4X_LICENSE_SHA256
        
"
icu_provider
"
:
ICU4X_LICENSE_SHA256
        
"
icu_provider_adapters
"
:
ICU4X_LICENSE_SHA256
        
"
icu_provider_macros
"
:
ICU4X_LICENSE_SHA256
        
"
icu_segmenter
"
:
ICU4X_LICENSE_SHA256
        
"
litemap
"
:
ICU4X_LICENSE_SHA256
        
"
tinystr
"
:
ICU4X_LICENSE_SHA256
        
"
writeable
"
:
ICU4X_LICENSE_SHA256
        
"
yoke
"
:
ICU4X_LICENSE_SHA256
        
"
yoke
-
derive
"
:
ICU4X_LICENSE_SHA256
        
"
zerofrom
"
:
ICU4X_LICENSE_SHA256
        
"
zerofrom
-
derive
"
:
ICU4X_LICENSE_SHA256
        
"
zerovec
"
:
ICU4X_LICENSE_SHA256
        
"
zerovec
-
derive
"
:
ICU4X_LICENSE_SHA256
    
}
    
staticmethod
    
def
runtime_license
(
package
license_string
)
:
        
"
"
"
Cargo
docs
say
:
        
-
-
-
        
https
:
/
/
doc
.
rust
-
lang
.
org
/
cargo
/
reference
/
manifest
.
html
        
This
is
an
SPDX
2
.
1
license
expression
for
this
package
.
Currently
        
crates
.
io
will
validate
the
license
provided
against
a
whitelist
of
        
known
license
and
exception
identifiers
from
the
SPDX
license
list
        
2
.
4
.
Parentheses
are
not
currently
supported
.
        
Multiple
licenses
can
be
separated
with
a
/
although
that
usage
        
is
deprecated
.
Instead
use
a
license
expression
with
AND
and
OR
        
operators
to
get
more
explicit
semantics
.
        
-
-
-
        
But
I
have
no
idea
how
you
can
meaningfully
AND
licenses
so
        
we
will
abort
if
that
is
detected
.
We
'
ll
handle
/
and
OR
as
        
equivalent
and
approve
is
any
is
in
our
approved
list
.
"
"
"
        
if
(
            
license_string
=
=
"
(
Apache
-
2
.
0
OR
MIT
)
AND
BSD
-
3
-
Clause
"
            
and
package
=
=
"
encoding_rs
"
        
)
:
            
return
True
        
if
(
            
license_string
=
=
"
(
MIT
OR
Apache
-
2
.
0
)
AND
Unicode
-
DFS
-
2016
"
            
and
package
=
=
"
unicode
-
ident
"
        
)
:
            
return
True
        
if
re
.
search
(
r
"
\
s
+
AND
"
license_string
)
:
            
return
False
        
license_list
=
re
.
split
(
r
"
\
s
*
/
\
s
*
|
\
s
+
OR
\
s
+
"
license_string
)
        
for
license
in
license_list
:
            
if
license
in
VendorRust
.
RUNTIME_LICENSE_WHITELIST
:
                
return
True
            
if
package
in
VendorRust
.
RUNTIME_LICENSE_PACKAGE_WHITELIST
.
get
(
license
[
]
)
:
                
return
True
        
return
False
    
def
_check_licenses
(
self
vendor_dir
:
str
)
-
>
bool
:
        
def
verify_acceptable_license
(
package
:
str
license
:
str
)
-
>
bool
:
            
self
.
log
(
logging
.
DEBUG
"
package_license
"
{
}
f
"
has
license
{
license
}
"
)
            
if
not
self
.
runtime_license
(
package
license
)
:
                
if
license
not
in
self
.
BUILDTIME_LICENSE_WHITELIST
:
                    
self
.
log
(
                        
logging
.
ERROR
                        
"
package_license_error
"
                        
{
}
                        
f
"
"
"
Package
{
package
}
has
a
non
-
approved
license
:
{
license
}
.
    
Please
request
license
review
on
the
package
'
s
license
.
If
the
package
'
s
license
    
is
approved
please
add
it
to
the
whitelist
of
suitable
licenses
.
    
"
"
"
                    
)
                    
return
False
                
elif
package
not
in
self
.
BUILDTIME_LICENSE_WHITELIST
[
license
]
:
                    
self
.
log
(
                        
logging
.
ERROR
                        
"
package_license_error
"
                        
{
}
                        
f
"
"
"
Package
{
package
}
has
a
license
that
is
approved
for
build
-
time
dependencies
:
    
{
license
}
    
but
the
package
itself
is
not
whitelisted
as
being
a
build
-
time
only
package
.
    
If
your
package
is
build
-
time
only
please
add
it
to
the
whitelist
of
build
-
time
    
only
packages
.
Otherwise
you
need
to
request
license
review
on
the
package
'
s
license
.
    
If
the
package
'
s
license
is
approved
please
add
it
to
the
whitelist
of
suitable
licenses
.
    
"
"
"
                    
)
                    
return
False
            
return
True
        
def
check_package
(
package_name
:
str
)
-
>
bool
:
            
self
.
log
(
                
logging
.
DEBUG
                
"
package_check
"
                
{
}
                
f
"
Checking
license
for
{
package_name
}
"
            
)
            
toml_file
=
os
.
path
.
join
(
vendor_dir
package_name
"
Cargo
.
toml
"
)
            
with
open
(
toml_file
encoding
=
"
utf
-
8
"
)
as
fh
:
                
toml_data
=
toml
.
load
(
fh
)
            
package_entry
:
dict
[
str
TomlItem
]
=
toml_data
[
"
package
"
]
            
license
=
package_entry
.
get
(
"
license
"
None
)
            
license_file
=
package_entry
.
get
(
"
license
-
file
"
None
)
            
if
license
is
not
None
and
type
(
license
)
is
not
str
:
                
self
.
log
(
                    
logging
.
ERROR
                    
"
package_invalid_license_format
"
                    
{
}
                    
f
"
package
{
package_name
}
has
an
invalid
license
field
(
expected
a
string
)
"
                
)
                
return
False
            
if
license_file
is
not
None
and
type
(
license_file
)
is
not
str
:
                
self
.
log
(
                    
logging
.
ERROR
                    
"
package_invalid_license_format
"
                    
{
}
                    
f
"
package
{
package_name
}
has
an
invalid
license
-
file
field
(
expected
a
string
)
"
                
)
                
return
False
            
if
not
license
and
not
license_file
:
                
self
.
log
(
                    
logging
.
ERROR
                    
"
package_no_license
"
                    
{
}
                    
f
"
package
{
package_name
}
does
not
provide
a
license
"
                
)
                
return
False
            
if
license
and
license_file
:
                
self
.
log
(
                    
logging
.
ERROR
                    
"
package_many_licenses
"
                    
{
}
                    
f
"
package
{
package_name
}
provides
too
many
licenses
"
                
)
                
return
False
            
if
license
:
                
return
verify_acceptable_license
(
package_name
license
)
            
assert
license_file
is
not
None
            
self
.
log
(
                
logging
.
DEBUG
                
"
package_license_file
"
                
{
}
                
f
"
package
has
license
-
file
{
license_file
}
"
            
)
            
if
package_name
not
in
self
.
RUNTIME_LICENSE_FILE_PACKAGE_WHITELIST
:
                
self
.
log
(
                    
logging
.
ERROR
                    
"
package_license_file_unknown
"
                    
{
}
                    
f
"
"
"
Package
{
package_name
}
has
an
unreviewed
license
file
:
{
license_file
}
.
Please
request
review
on
the
provided
license
;
if
approved
the
package
can
be
added
to
the
whitelist
of
packages
whose
licenses
are
suitable
.
"
"
"
                
)
                
return
False
            
approved_hash
=
self
.
RUNTIME_LICENSE_FILE_PACKAGE_WHITELIST
[
package_name
]
            
with
open
(
                
os
.
path
.
join
(
vendor_dir
package_name
license_file
)
"
rb
"
            
)
as
license_buf
:
                
current_hash
=
hashlib
.
sha256
(
license_buf
.
read
(
)
)
.
hexdigest
(
)
            
if
current_hash
!
=
approved_hash
:
                
self
.
log
(
                    
logging
.
ERROR
                    
"
package_license_file_mismatch
"
                    
{
}
                    
f
"
"
"
Package
{
package_name
}
has
changed
its
license
file
:
{
license_file
}
(
hash
{
current_hash
}
)
.
Please
request
review
on
the
provided
license
;
if
approved
please
update
the
license
file
'
s
hash
.
"
"
"
                
)
                
return
False
            
return
True
        
results
=
[
            
check_package
(
p
)
            
for
p
in
os
.
listdir
(
vendor_dir
)
            
if
os
.
path
.
isdir
(
os
.
path
.
join
(
vendor_dir
p
)
)
        
]
        
return
all
(
results
)
    
def
_check_build_rust
(
self
cargo_lock
)
:
        
ret
=
True
        
crates
=
{
}
        
for
path
in
Path
(
self
.
topsrcdir
)
.
glob
(
"
build
/
rust
/
*
*
/
Cargo
.
toml
"
)
:
            
with
open
(
path
)
as
fh
:
                
cargo_toml
=
toml
.
load
(
fh
)
                
relative_path
=
path
.
relative_to
(
self
.
topsrcdir
)
                
package
=
cargo_toml
[
"
package
"
]
                
key
=
(
package
[
"
name
"
]
package
[
"
version
"
]
)
                
if
key
in
crates
:
                    
self
.
log
(
                        
logging
.
ERROR
                        
"
build_rust
"
                        
{
                            
"
path
"
:
crates
[
key
]
                            
"
path2
"
:
relative_path
                            
"
crate
"
:
key
[
0
]
                            
"
version
"
:
key
[
1
]
                        
}
                        
"
{
path
}
and
{
path2
}
both
contain
{
crate
}
{
version
}
"
                    
)
                    
ret
=
False
                
crates
[
key
]
=
relative_path
        
for
package
in
cargo_lock
[
"
package
"
]
:
            
key
=
(
package
[
"
name
"
]
package
[
"
version
"
]
)
            
if
key
in
crates
and
"
source
"
not
in
package
:
                
crates
.
pop
(
key
)
        
for
(
name
version
)
path
in
crates
.
items
(
)
:
            
self
.
log
(
                
logging
.
ERROR
                
"
build_rust
"
                
{
"
path
"
:
path
"
crate
"
:
name
"
version
"
:
version
}
                
"
{
crate
}
{
version
}
has
an
override
in
{
path
}
that
is
not
used
"
            
)
            
ret
=
False
        
return
ret
    
def
vendor
(
self
ignore_modified
=
False
force
=
False
)
:
        
from
mozbuild
.
mach_commands
import
cargo_vet
        
self
.
populate_logger
(
)
        
self
.
log_manager
.
enable_unstructured
(
)
        
if
not
ignore_modified
and
self
.
has_modified_files
(
)
:
            
return
False
        
cargo
=
self
.
_ensure_cargo
(
)
        
if
not
cargo
:
            
self
.
log
(
logging
.
ERROR
"
cargo_not_found
"
{
}
"
Cargo
was
not
found
.
"
)
            
return
False
        
relative_vendor_dir
=
"
third_party
/
rust
"
        
vendor_dir
=
mozpath
.
join
(
self
.
topsrcdir
relative_vendor_dir
)
        
res
=
subprocess
.
run
(
            
[
cargo
"
update
"
"
-
p
"
"
gkrust
"
]
cwd
=
self
.
topsrcdir
check
=
False
        
)
        
if
res
.
returncode
:
            
self
.
log
(
logging
.
ERROR
"
cargo_update_failed
"
{
}
"
Cargo
update
failed
.
"
)
            
return
False
        
with
open
(
os
.
path
.
join
(
self
.
topsrcdir
"
Cargo
.
lock
"
)
)
as
fh
:
            
cargo_lock
=
toml
.
load
(
fh
)
            
failed
=
False
            
for
package
in
cargo_lock
.
get
(
"
patch
"
{
}
)
.
get
(
"
unused
"
[
]
)
:
                
self
.
log
(
                    
logging
.
ERROR
                    
"
unused_patch
"
                    
{
"
crate
"
:
package
[
"
name
"
]
}
                    
"
"
"
Unused
patch
in
top
-
level
Cargo
.
toml
for
{
crate
}
.
"
"
"
                
)
                
failed
=
True
            
if
not
self
.
_check_build_rust
(
cargo_lock
)
:
                
failed
=
True
            
grouped
=
defaultdict
(
list
)
            
for
package
in
cargo_lock
[
"
package
"
]
:
                
if
package
[
"
name
"
]
in
PACKAGES_WE_ALWAYS_WANT_AN_OVERRIDE_OF
:
                    
if
package
.
get
(
"
source
"
)
:
                        
self
.
log
(
                            
logging
.
ERROR
                            
"
non_overridden
"
                            
{
                                
"
crate
"
:
package
[
"
name
"
]
                                
"
version
"
:
package
[
"
version
"
]
                                
"
source
"
:
package
[
"
source
"
]
                            
}
                            
"
Crate
{
crate
}
v
{
version
}
must
be
overridden
but
isn
'
t
"
                            
"
and
comes
from
{
source
}
.
"
                        
)
                        
failed
=
True
                
elif
reason
:
=
dont_want_package
(
package
[
"
name
"
]
)
:
                    
self
.
log
(
                        
logging
.
ERROR
                        
"
undesirable
"
                        
{
                            
"
crate
"
:
package
[
"
name
"
]
                            
"
version
"
:
package
[
"
version
"
]
                            
"
reason
"
:
reason
                        
}
                        
"
Crate
{
crate
}
is
not
desirable
:
{
reason
}
"
                    
)
                    
failed
=
True
                
grouped
[
package
[
"
name
"
]
]
.
append
(
package
)
            
for
name
in
ALLOWED_DESPITE_PREFIX
:
                
if
name
not
in
SEEN_ALLOWED_DESPITE_PREFIX
:
                    
self
.
log
(
                        
logging
.
ERROR
                        
"
unused_allowed_despite_prefix
"
                        
{
"
crate
"
:
name
}
                        
"
ALLOWED_DESPITE_PREFIX
contains
{
crate
}
"
                        
"
but
that
crate
is
not
actually
used
(
anymore
?
)
.
"
                    
)
                    
failed
=
True
            
for
name
packages
in
grouped
.
items
(
)
:
                
num
=
len
(
[
                    
p
                    
for
p
in
packages
                    
if
all
(
d
.
split
(
)
[
0
]
!
=
name
for
d
in
p
.
get
(
"
dependencies
"
[
]
)
)
                
]
)
                
if
num
>
1
:
                    
self
.
log
(
                        
logging
.
ERROR
                        
"
duplicate_crate
"
                        
{
                            
"
crate
"
:
name
                            
"
num
"
:
num
                        
}
                        
"
There
are
{
num
}
different
versions
of
crate
{
crate
}
.
"
                        
"
Please
avoid
the
extra
duplication
.
"
                    
)
                    
failed
=
True
        
env
=
os
.
environ
.
copy
(
)
        
env
[
"
PATH
"
]
=
os
.
pathsep
.
join
(
(
            
str
(
Path
(
cargo
)
.
parent
)
            
os
.
environ
[
"
PATH
"
]
        
)
)
        
flags
=
[
"
-
-
output
-
format
=
json
"
]
        
if
"
MOZ_AUTOMATION
"
in
os
.
environ
:
            
flags
.
append
(
"
-
-
locked
"
)
            
flags
.
append
(
"
-
-
frozen
"
)
        
res
=
cargo_vet
(
            
self
            
flags
            
stdout
=
subprocess
.
PIPE
            
env
=
env
        
)
        
if
res
.
returncode
:
            
try
:
                
vet
=
json
.
loads
(
res
.
stdout
)
            
except
Exception
:
                
vet
=
{
}
            
logged_error
=
False
            
for
failure
in
vet
.
get
(
"
failures
"
[
]
)
:
                
failure
[
"
crate
"
]
=
failure
.
pop
(
"
name
"
)
                
self
.
log
(
                    
logging
.
ERROR
                    
"
cargo_vet_failed
"
                    
failure
                    
"
Missing
audit
for
{
crate
}
:
{
version
}
(
requires
{
missing_criteria
}
)
.
"
                    
"
Run
.
/
mach
cargo
vet
for
more
information
.
"
                
)
                
logged_error
=
True
            
for
key
in
vet
.
get
(
"
violations
"
{
}
)
.
keys
(
)
:
                
self
.
log
(
                    
logging
.
ERROR
                    
"
cargo_vet_failed
"
                    
{
"
key
"
:
key
}
                    
"
Violation
conflict
for
{
key
}
.
Run
.
/
mach
cargo
vet
for
more
information
.
"
                
)
                
logged_error
=
True
            
if
"
error
"
in
vet
:
                
error
=
vet
[
"
error
"
]
                
self
.
log
(
                    
logging
.
ERROR
                    
"
cargo_vet_failed
"
                    
error
                    
"
Vet
{
severity
}
:
{
message
}
"
                
)
                
if
"
help
"
in
error
:
                    
self
.
log
(
logging
.
INFO
"
cargo_vet_failed
"
error
"
help
:
{
help
}
"
)
                
for
cause
in
error
.
get
(
"
causes
"
[
]
)
:
                    
self
.
log
(
                        
logging
.
INFO
                        
"
cargo_vet_failed
"
                        
{
"
cause
"
:
cause
}
                        
"
cause
:
{
cause
}
"
                    
)
                
for
related
in
error
.
get
(
"
related
"
[
]
)
:
                    
self
.
log
(
                        
logging
.
INFO
                        
"
cargo_vet_failed
"
                        
related
                        
"
related
{
severity
}
:
{
message
}
"
                    
)
                
self
.
log
(
                    
logging
.
INFO
                    
"
cargo_vet_failed
"
                    
{
}
                    
"
Run
.
/
mach
cargo
vet
for
more
information
.
"
                
)
                
logged_error
=
True
            
if
not
logged_error
:
                
self
.
log
(
                    
logging
.
ERROR
                    
"
cargo_vet_failed
"
                    
{
}
                    
"
Unknown
vet
error
.
Run
.
/
mach
cargo
vet
for
more
information
.
"
                
)
            
failed
=
True
        
if
failed
and
not
force
:
            
return
False
        
res
=
subprocess
.
run
(
            
[
cargo
"
vendor
"
vendor_dir
]
            
cwd
=
self
.
topsrcdir
            
stdout
=
subprocess
.
PIPE
            
check
=
False
        
)
        
if
res
.
returncode
:
            
self
.
log
(
logging
.
ERROR
"
cargo_vendor_failed
"
{
}
"
Cargo
vendor
failed
.
"
)
            
return
False
        
output
=
res
.
stdout
.
decode
(
"
UTF
-
8
"
)
        
config
=
"
\
n
"
.
join
(
            
dropwhile
(
lambda
l
:
not
l
.
startswith
(
"
[
"
)
output
.
splitlines
(
)
)
        
)
        
config
=
toml
.
loads
(
config
)
        
replaces
=
{
            
v
[
"
replace
-
with
"
]
for
v
in
config
[
"
source
"
]
.
values
(
)
if
"
replace
-
with
"
in
v
        
}
        
if
len
(
replaces
)
!
=
1
:
            
self
.
log
(
                
logging
.
ERROR
                
"
vendor_failed
"
                
dict
(
replaces
=
replaces
)
                
"
"
"
cargo
vendor
didn
'
t
output
a
unique
replace
-
with
.
Found
:
{
replaces
}
.
"
"
"
            
)
            
return
False
        
replace_name
=
replaces
.
pop
(
)
        
replace
=
config
[
"
source
"
]
.
pop
(
replace_name
)
        
replace
[
"
directory
"
]
=
mozpath
.
relpath
(
            
mozpath
.
normsep
(
os
.
path
.
normcase
(
replace
[
"
directory
"
]
)
)
            
mozpath
.
normsep
(
os
.
path
.
normcase
(
self
.
topsrcdir
)
)
        
)
        
cargo_config
=
os
.
path
.
join
(
self
.
topsrcdir
"
.
cargo
"
"
config
.
toml
.
in
"
)
        
with
open
(
cargo_config
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
fh
:
            
fh
.
write
(
                
CARGO_CONFIG_TEMPLATE
.
format
(
                    
config
=
toml
.
dumps
(
config
)
                    
replace_name
=
replace_name
                    
directory
=
replace
[
"
directory
"
]
                
)
            
)
        
def
recursive_sort
(
obj
)
:
            
if
isinstance
(
obj
tomlkit
.
items
.
Table
)
:
                
new_obj
=
obj
.
copy
(
)
                
body
=
[
(
k
recursive_sort
(
v
)
)
for
k
v
in
new_obj
.
value
.
body
]
                
for
n
(
k
v
)
in
enumerate
(
body
)
:
                    
if
k
is
None
or
v
.
is_aot
(
)
:
                        
break
                
else
:
                    
n
=
len
(
body
)
                
body
[
:
n
]
=
sorted
(
body
[
:
n
]
key
=
lambda
x
:
str
(
x
[
0
]
)
)
                
new_obj
.
value
.
body
[
:
]
=
body
                
return
new_obj
            
if
isinstance
(
obj
tomlkit
.
items
.
AoT
)
:
                
new_obj
=
copy
.
copy
(
obj
)
                
body
=
[
recursive_sort
(
v
)
for
v
in
new_obj
.
body
]
                
new_obj
.
body
[
:
]
=
body
                
return
new_obj
            
return
obj
        
cargo_version
=
self
.
cargo_version
(
cargo
)
        
if
cargo_version
>
=
"
1
.
89
"
:
            
for
package
in
cargo_lock
[
"
package
"
]
:
                
source
=
package
.
get
(
"
source
"
)
                
if
not
source
:
                    
continue
                
unlinked
=
[
]
                
modified
=
{
}
                
package_dir
=
Path
(
vendor_dir
)
/
package
[
"
name
"
]
                
with
(
package_dir
/
"
Cargo
.
toml
"
)
.
open
(
encoding
=
"
utf
-
8
"
)
as
fh
:
                    
toml_data
=
tomlkit
.
parse
(
fh
.
read
(
)
)
                
if
not
source
.
startswith
(
"
registry
+
"
)
:
                    
metadata
=
toml_data
.
get
(
"
package
"
{
}
)
.
get
(
"
metadata
"
{
}
)
                    
if
metadata
and
cargo_version
>
=
"
1
.
90
"
:
                        
with
(
package_dir
/
"
Cargo
.
toml
"
)
.
open
(
"
wb
"
)
as
fh
:
                            
toml_data
[
"
package
"
]
[
"
metadata
"
]
=
recursive_sort
(
metadata
)
                            
raw_data
=
tomlkit
.
dumps
(
toml_data
)
.
encode
(
"
utf
-
8
"
)
                            
modified
[
"
Cargo
.
toml
"
]
=
hashlib
.
sha256
(
                                
raw_data
                            
)
.
hexdigest
(
)
                            
fh
.
write
(
raw_data
)
                
else
:
                    
unlinked
+
=
[
"
Cargo
.
toml
.
orig
"
]
                    
cargo_package
=
toml_data
.
get
(
"
package
"
{
}
)
                    
if
readme
:
=
cargo_package
.
get
(
"
readme
"
)
:
                        
if
includes
:
=
cargo_package
.
get
(
"
include
"
)
:
                            
if
not
any
(
                                
mozpath
.
match
(
readme
include
.
removeprefix
(
"
/
"
)
)
                                
for
include
in
includes
                            
)
:
                                
try
:
                                    
(
package_dir
/
readme
)
.
unlink
(
)
                                    
unlinked
.
append
(
readme
)
                                
except
FileNotFoundError
:
                                    
pass
                    
for
path
in
package_dir
.
glob
(
"
*
*
/
.
*
"
)
:
                        
if
path
.
name
=
=
"
.
cargo
-
checksum
.
json
"
:
                            
continue
                        
if
path
.
is_dir
(
)
:
                            
for
root_path
dirs
files
in
os
.
walk
(
path
topdown
=
False
)
:
                                
root
=
Path
(
root_path
)
                                
for
name
in
files
:
                                    
to_unlink
=
root
/
name
                                    
try
:
                                        
to_unlink
.
unlink
(
)
                                        
unlinked
.
append
(
                                            
mozpath
.
normsep
(
                                                
str
(
to_unlink
.
relative_to
(
package_dir
)
)
                                            
)
                                        
)
                                    
except
FileNotFoundError
:
                                        
pass
                                
for
name
in
dirs
:
                                    
try
:
                                        
(
root
/
name
)
.
rmdir
(
)
                                    
except
OSError
:
                                        
pass
                        
else
:
                            
try
:
                                
path
.
unlink
(
)
                                
unlinked
.
append
(
                                    
mozpath
.
normsep
(
str
(
path
.
relative_to
(
package_dir
)
)
)
                                
)
                            
except
FileNotFoundError
:
                                
pass
                
checksum_json
=
package_dir
/
"
.
cargo
-
checksum
.
json
"
                
with
checksum_json
.
open
(
encoding
=
"
utf
-
8
"
)
as
fh
:
                    
checksum_data
=
json
.
load
(
fh
)
                
for
path
in
unlinked
:
                    
try
:
                        
del
checksum_data
[
"
files
"
]
[
path
]
                    
except
KeyError
:
                        
pass
                
for
path
sha256
in
modified
.
items
(
)
:
                    
checksum_data
[
"
files
"
]
[
path
]
=
sha256
                
with
checksum_json
.
open
(
mode
=
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
)
as
fh
:
                    
json
.
dump
(
checksum_data
fh
separators
=
(
"
"
"
:
"
)
)
        
if
not
self
.
_check_licenses
(
vendor_dir
)
and
not
force
:
            
self
.
log
(
                
logging
.
ERROR
                
"
license_check_failed
"
                
{
}
                
f
"
"
"
The
changes
from
mach
vendor
rust
will
NOT
be
added
to
version
control
.
{
CARGO_LOCK_NOTICE
}
"
"
"
            
)
            
self
.
repository
.
clean_directory
(
vendor_dir
)
            
return
False
        
self
.
repository
.
add_remove_files
(
vendor_dir
)
        
FILESIZE_LIMIT
=
100
*
1024
        
large_files
=
set
(
)
        
cumulative_added_size
=
0
        
for
f
in
self
.
repository
.
get_changed_files
(
"
A
"
)
:
            
path
=
mozpath
.
join
(
self
.
topsrcdir
f
)
            
size
=
os
.
stat
(
path
)
.
st_size
            
cumulative_added_size
+
=
size
            
if
size
>
FILESIZE_LIMIT
:
                
large_files
.
add
(
f
)
        
if
large_files
:
            
self
.
log
(
                
logging
.
ERROR
                
"
filesize_check
"
                
{
}
                
"
"
"
The
following
files
exceed
the
filesize
limit
of
{
size
}
:
{
files
}
If
you
can
'
t
reduce
the
size
of
these
files
talk
to
a
build
peer
(
on
the
#
build
channel
at
https
:
/
/
chat
.
mozilla
.
org
)
about
the
particular
large
files
you
are
adding
.
The
changes
from
mach
vendor
rust
will
NOT
be
added
to
version
control
.
{
notice
}
"
"
"
.
format
(
                    
files
=
"
\
n
"
.
join
(
sorted
(
large_files
)
)
                    
size
=
FILESIZE_LIMIT
                    
notice
=
CARGO_LOCK_NOTICE
                
)
            
)
            
if
not
force
:
                
self
.
repository
.
forget_add_remove_files
(
vendor_dir
)
                
self
.
repository
.
clean_directory
(
vendor_dir
)
                
return
False
        
SIZE_WARN_THRESHOLD
=
5
*
1024
*
1024
        
if
cumulative_added_size
>
=
SIZE_WARN_THRESHOLD
:
            
self
.
log
(
                
logging
.
WARN
                
"
filesize_check
"
                
{
}
                
f
"
"
"
Your
changes
add
{
cumulative_added_size
}
bytes
of
added
files
.
Please
consider
finding
ways
to
reduce
the
size
of
the
vendored
packages
.
For
instance
check
the
vendored
packages
for
unusually
large
test
or
benchmark
files
that
don
'
t
need
to
be
published
to
crates
.
io
and
submit
a
pull
request
upstream
to
ignore
those
files
when
publishing
.
"
"
"
            
)
        
if
"
MOZ_AUTOMATION
"
in
os
.
environ
:
            
changed
=
self
.
repository
.
get_changed_files
(
mode
=
"
staged
"
)
            
for
file
in
changed
:
                
self
.
log
(
                    
logging
.
ERROR
                    
"
vendor
-
change
"
                    
{
"
file
"
:
file
}
                    
"
File
was
modified
by
vendor
:
{
file
}
"
                
)
            
if
changed
:
                
return
False
        
return
True
