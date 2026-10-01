"
"
"
Compose
Cargo
commands
and
environments
for
Rust
build
edges
.
"
"
"
from
dataclasses
import
asdict
dataclass
fields
from
mozshellutil
import
split
as
shell_split
def
_as_str
(
v
)
:
    
if
v
is
None
:
        
return
"
"
    
if
isinstance
(
v
(
list
tuple
)
)
:
        
return
"
"
.
join
(
v
)
    
return
str
(
v
)
def
_as_list
(
v
)
:
    
if
v
is
None
:
        
return
[
]
    
if
isinstance
(
v
(
list
tuple
)
)
:
        
return
list
(
v
)
    
if
isinstance
(
v
str
)
:
        
return
v
.
split
(
)
    
return
[
str
(
v
)
]
def
_as_args
(
v
)
:
    
"
"
"
Split
a
configured
command
fragment
into
arguments
.
    
A
nargs
=
1
option
holds
the
whole
fragment
in
one
element
so
the
value
    
is
joined
before
it
is
split
.
    
"
"
"
    
return
shell_split
(
_as_str
(
v
)
)
def
_bool
(
v
)
:
    
if
v
is
None
:
        
return
False
    
if
isinstance
(
v
bool
)
:
        
return
v
    
return
str
(
v
)
.
strip
(
)
not
in
(
"
"
"
0
"
)
CARGO_CONFIG_KEYS
=
{
    
"
AR
"
:
_as_str
    
"
BINDGEN_EXTRA_CLANG_ARGS
"
:
_as_list
    
"
CARGO
"
:
_as_str
    
"
CARGOFLAGS
"
:
_as_args
    
"
CARGO_INCREMENTAL
"
:
_as_str
    
"
CARGO_PROFILE_DEV_OPT_LEVEL
"
:
_as_str
    
"
CARGO_PROFILE_RELEASE_OPT_LEVEL
"
:
_as_str
    
"
CC_KNOWN_WRAPPER_CUSTOM
"
:
_as_str
    
"
GLEAN_PARSER_VENV
"
:
_as_str
    
"
HOST_AR
"
:
_as_str
    
"
IPHONEOS_SDK_DIR
"
:
_as_str
    
"
MOZ_CARGO_BUILD_STD_ARGS
"
:
_as_list
    
"
MOZ_CARGO_CC
"
:
_as_list
    
"
MOZ_CARGO_CC_ENV_SUFFIX
"
:
_as_str
    
"
MOZ_CARGO_CFLAGS_BASE
"
:
_as_list
    
"
MOZ_CARGO_CFLAGS_FILTER
"
:
_as_list
    
"
MOZ_CARGO_CXX
"
:
_as_list
    
"
MOZ_CARGO_CXXFLAGS_BASE
"
:
_as_list
    
"
MOZ_CARGO_CXXFLAGS_FILTER
"
:
_as_list
    
"
MOZ_CARGO_DEFAULT_PROFILE_ARGS
"
:
_as_list
    
"
MOZ_CARGO_FROZEN_ARGS
"
:
_as_list
    
"
MOZ_CARGO_HOST_CC
"
:
_as_list
    
"
MOZ_CARGO_HOST_CC_ENV_SUFFIX
"
:
_as_str
    
"
MOZ_CARGO_HOST_CFLAGS_BASE
"
:
_as_list
    
"
MOZ_CARGO_HOST_CFLAGS_FILTER
"
:
_as_list
    
"
MOZ_CARGO_HOST_CXX
"
:
_as_list
    
"
MOZ_CARGO_HOST_CXXFLAGS_BASE
"
:
_as_list
    
"
MOZ_CARGO_HOST_CXXFLAGS_FILTER
"
:
_as_list
    
"
MOZ_CARGO_HOST_LD
"
:
_as_list
    
"
MOZ_CARGO_HOST_LDFLAGS
"
:
_as_list
    
"
MOZ_CARGO_HOST_LD_CXX
"
:
_as_list
    
"
MOZ_CARGO_HOST_LINKER
"
:
_as_str
    
"
MOZ_CARGO_HOST_LINKER_ENV_VAR
"
:
_as_str
    
"
MOZ_CARGO_HOST_TARGET_ARGS
"
:
_as_list
    
"
MOZ_CARGO_LD
"
:
_as_list
    
"
MOZ_CARGO_LDFLAGS_FILTER_OUT
"
:
_as_list
    
"
MOZ_CARGO_LD_CXX
"
:
_as_list
    
"
MOZ_CARGO_LINKER
"
:
_as_str
    
"
MOZ_CARGO_LINKER_ENV_VAR
"
:
_as_str
    
"
MOZ_CARGO_PROFILE_PREFIX
"
:
_as_str
    
"
MOZ_CARGO_PROGRAM_LDFLAGS_FILTER_OUT
"
:
_as_list
    
"
MOZ_CARGO_TARGET_ARGS
"
:
_as_list
    
"
MOZ_CLANG_NEWER_THAN_RUSTC_LLVM
"
:
_as_str
    
"
MOZ_CLANG_PATH
"
:
_as_str
    
"
MOZ_FOLD_LIBS
"
:
_as_str
    
"
MOZ_LIBCLANG_PATH
"
:
_as_str
    
"
MOZ_LTO_LDFLAGS
"
:
_as_list
    
"
MOZ_LTO_OBJECT_PATH
"
:
_bool
    
"
MOZ_RUSTC_BOOTSTRAP_DEFAULT
"
:
_as_str
    
"
MOZ_RUSTC_BOOTSTRAP_FORCE
"
:
_as_str
    
"
MOZ_RUSTC_WRAPPER
"
:
_as_str
    
"
MOZ_RUSTFLAGS_AFTER_EXTRA
"
:
_as_list
    
"
MOZ_RUSTFLAGS_CODEGEN
"
:
_as_list
    
"
MOZ_RUSTFLAGS_DEFAULT_LINKER_LIBRARIES
"
:
_as_list
    
"
MOZ_RUSTFLAGS_TARGET_COMMON
"
:
_as_list
    
"
MOZ_RUSTFLAGS_TARGET_LTOABLE
"
:
_as_list
    
"
MOZ_RUST_COREAUDIO_SDK_PATH
"
:
_as_str
    
"
MOZ_RUST_DEFAULT_FLAGS
"
:
_as_list
    
"
MOZ_RUST_LIBRARY_RUSTCFLAGS
"
:
_as_list
    
"
MOZ_RUST_PROGRAM_LDFLAGS
"
:
_as_list
    
"
MOZ_RUST_PROGRAM_RUSTCFLAGS
"
:
_as_list
    
"
MOZ_RUST_SANITIZER_OPTION_VARS
"
:
_as_list
    
"
PKG_CONFIG
"
:
_as_str
    
"
PKG_CONFIG_LIBDIR
"
:
_as_str
    
"
PKG_CONFIG_PATH
"
:
_as_str
    
"
PKG_CONFIG_SYSROOT_DIR
"
:
_as_str
    
"
PYTHON3
"
:
_as_str
    
"
RUSTC
"
:
_as_str
    
"
RUSTDOC
"
:
_as_str
    
"
RUSTDOCFLAGS
"
:
_as_str
    
"
RUSTFLAGS
"
:
_as_list
    
"
RUSTFMT
"
:
_as_str
    
"
RUST_LTO_CFLAGS
"
:
_as_list
    
"
RUST_LTO_ELIGIBLE
"
:
_bool
    
"
RUST_PGO_CFLAGS
"
:
_as_list
    
"
RUST_PGO_LDFLAGS
"
:
_as_list
    
"
RUST_SANCOV_FLAGS
"
:
_as_list
    
"
RUST_TARGET
"
:
_as_str
}
CARGO_SPEC_FILES
=
{
    
"
library
"
:
"
.
cargo
-
library
-
spec
.
json
"
    
"
host
-
library
"
:
"
.
cargo
-
host
-
library
-
spec
.
json
"
    
"
program
"
:
"
.
cargo
-
program
-
spec
.
json
"
    
"
host
-
program
"
:
"
.
cargo
-
host
-
program
-
spec
.
json
"
    
"
test
"
:
"
.
cargo
-
tests
-
spec
.
json
"
}
dataclass
class
CargoCommand
:
    
"
"
"
Declarative
metadata
for
one
Cargo
build
edge
.
    
names
select
what
Cargo
builds
interpreted
by
kind
:
the
library
    
file
name
the
program
binary
names
or
the
test
package
names
.
    
rustflags
and
rustc_flags
hold
the
edge
'
s
own
additions
to
    
RUSTFLAGS
and
to
the
flags
after
-
-
.
lto
is
whether
a
library
    
uses
link
time
optimization
in
a
build
that
enables
it
for
Rust
libraries
.
    
"
"
"
    
kind
:
str
    
manifest_path
:
str
    
working_directory
:
str
    
names
:
tuple
=
(
)
    
features
:
tuple
=
(
)
    
cargo_profile_suffix
:
str
=
"
"
    
cargo_crate_type
:
str
=
"
"
    
lto
:
bool
=
True
    
computed_cflags
:
tuple
=
(
)
    
computed_cxxflags
:
tuple
=
(
)
    
computed_host_cflags
:
tuple
=
(
)
    
computed_host_cxxflags
:
tuple
=
(
)
    
link_flags
:
tuple
=
(
)
    
rustflags
:
tuple
=
(
)
    
rustc_flags
:
tuple
=
(
)
    
def
__post_init__
(
self
)
:
        
if
self
.
kind
not
in
CARGO_SPEC_FILES
:
            
raise
ValueError
(
f
"
Unknown
Rust
build
kind
:
{
self
.
kind
!
r
}
"
)
        
for
field
in
fields
(
self
)
:
            
if
field
.
type
is
tuple
:
                
setattr
(
self
field
.
name
tuple
(
getattr
(
self
field
.
name
)
)
)
dataclass
class
CargoInvocation
:
    
"
"
"
State
that
varies
per
Cargo
run
and
belongs
to
neither
an
edge
nor
configure
.
    
color
is
always
never
or
empty
to
leave
Cargo
'
s
default
.
    
rustc_bootstrap
replaces
the
configured
RUSTC_BOOTSTRAP
default
.
    
"
"
"
    
verbose
:
bool
=
False
    
json_output
:
bool
=
False
    
color
:
str
=
"
"
    
extra_rustflags
:
tuple
=
(
)
    
cargo_rustcflags
:
tuple
=
(
)
    
cargo_extra_flags
:
tuple
=
(
)
    
rustc_bootstrap
:
str
=
"
"
    
classmethod
    
def
from_environ
(
cls
environ
)
:
        
color
=
"
"
        
if
_bool
(
environ
.
get
(
"
MACH_STDOUT_ISATTY
"
)
)
:
            
color
=
"
never
"
if
_bool
(
environ
.
get
(
"
NO_ANSI
"
)
)
else
"
always
"
        
return
cls
(
            
verbose
=
_bool
(
environ
.
get
(
"
BUILD_VERBOSE_LOG
"
)
)
            
json_output
=
_bool
(
environ
.
get
(
"
USE_CARGO_JSON_MESSAGE_FORMAT
"
)
)
            
color
=
color
            
extra_rustflags
=
tuple
(
(
environ
.
get
(
"
extra_rustflags
"
)
or
"
"
)
.
split
(
)
)
            
cargo_rustcflags
=
tuple
(
_as_args
(
environ
.
get
(
"
CARGO_RUSTCFLAGS
"
)
)
)
            
cargo_extra_flags
=
tuple
(
_as_args
(
environ
.
get
(
"
CARGO_EXTRA_FLAGS
"
)
)
)
            
rustc_bootstrap
=
environ
.
get
(
"
RUSTC_BOOTSTRAP
"
)
or
"
"
        
)
def
_copied
(
value
)
:
    
"
"
"
A
value
a
caller
may
extend
without
reaching
back
into
the
config
.
"
"
"
    
return
list
(
value
)
if
isinstance
(
value
list
)
else
value
class
CargoConfig
:
    
"
"
"
The
configure
substitutions
a
Cargo
command
may
read
.
    
Every
value
arrives
in
the
representation
CARGO_CONFIG_KEYS
declares
for
    
its
key
so
a
read
needs
no
conversion
and
a
key
the
substitutions
do
not
    
carry
reads
as
that
representation
'
s
empty
value
.
Reading
a
key
that
    
CARGO_CONFIG_KEYS
does
not
declare
raises
because
a
spec
only
carries
    
the
declared
ones
.
    
"
"
"
    
def
__init__
(
self
substs
)
:
        
self
.
_values
=
{
            
key
:
CARGO_CONFIG_KEYS
[
key
]
(
value
)
            
for
key
value
in
substs
.
items
(
)
            
if
key
in
CARGO_CONFIG_KEYS
        
}
    
def
_check
(
self
key
)
:
        
if
key
not
in
CARGO_CONFIG_KEYS
:
            
raise
KeyError
(
f
"
{
key
}
is
not
declared
in
CARGO_CONFIG_KEYS
"
)
    
def
__getitem__
(
self
key
)
:
        
self
.
_check
(
key
)
        
return
_copied
(
self
.
_values
[
key
]
)
    
def
__contains__
(
self
key
)
:
        
self
.
_check
(
key
)
        
return
key
in
self
.
_values
    
def
get
(
self
key
default
=
None
)
:
        
self
.
_check
(
key
)
        
if
key
not
in
self
.
_values
:
            
return
CARGO_CONFIG_KEYS
[
key
]
(
default
)
        
return
_copied
(
self
.
_values
[
key
]
)
def
cargo_spec
(
command
substs
topsrcdir
topobjdir
)
:
    
"
"
"
Everything
one
Rust
build
edge
needs
in
serializable
form
.
    
The
spec
is
the
only
input
the
run_cargo
action
reads
so
it
carries
    
every
configure
substitution
the
Cargo
commands
read
.
    
"
"
"
    
if
isinstance
(
substs
CargoConfig
)
:
        
raise
TypeError
(
            
"
cargo_spec
takes
the
raw
substitutions
because
loading
the
spec
"
            
"
converts
them
and
a
converted
value
cannot
be
converted
again
"
        
)
    
return
{
        
"
config
"
:
{
k
:
substs
[
k
]
for
k
in
sorted
(
CARGO_CONFIG_KEYS
)
if
k
in
substs
}
        
"
edge
"
:
asdict
(
command
)
        
"
topobjdir
"
:
topobjdir
        
"
topsrcdir
"
:
topsrcdir
    
}
def
load_cargo_spec
(
data
)
:
    
"
"
"
Return
the
command
substs
topsrcdir
and
topobjdir
held
in
a
spec
.
"
"
"
    
return
(
        
CargoCommand
(
*
*
data
[
"
edge
"
]
)
        
CargoConfig
(
data
[
"
config
"
]
)
        
data
[
"
topsrcdir
"
]
        
data
[
"
topobjdir
"
]
    
)
