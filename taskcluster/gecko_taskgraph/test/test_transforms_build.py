import
pytest
from
mozunit
import
main
from
gecko_taskgraph
.
test
.
conftest
import
FakeParameters
from
gecko_taskgraph
.
transforms
.
build
import
collapse_unified_builds
mozconfig
def
unified_build
(
)
:
    
return
{
        
"
name
"
:
"
macosx64
-
shippable
/
opt
"
        
"
attributes
"
:
{
"
shippable
"
:
True
}
        
"
index
"
:
{
"
job
-
name
"
:
"
macosx64
-
opt
"
}
        
"
worker
"
:
{
"
env
"
:
{
}
"
max
-
run
-
time
"
:
1800
}
        
"
run
"
:
{
"
job
-
script
"
:
"
taskcluster
/
scripts
/
misc
/
unify
.
sh
"
}
        
"
dependencies
"
:
{
            
"
x64
"
:
"
build
-
macosx64
-
x64
-
shippable
/
opt
"
            
"
aarch64
"
:
"
build
-
macosx64
-
aarch64
-
shippable
/
opt
"
        
}
        
"
fetches
"
:
{
            
"
x64
"
:
[
{
"
artifact
"
:
"
target
.
dmg
"
"
dest
"
:
"
x64
"
}
]
            
"
aarch64
"
:
[
{
"
artifact
"
:
"
target
.
dmg
"
"
dest
"
:
"
aarch64
"
}
]
        
}
    
}
def
per_arch_build
(
arch
package_tests
=
True
)
:
    
env
=
{
"
MOZ_AUTOMATION_PACKAGE_TESTS
"
:
"
1
"
}
if
package_tests
else
{
}
    
return
{
        
"
name
"
:
f
"
macosx64
-
{
arch
}
-
shippable
/
opt
"
        
"
attributes
"
:
{
}
        
"
index
"
:
{
"
job
-
name
"
:
f
"
macosx64
-
{
arch
}
-
opt
"
}
        
"
worker
"
:
{
"
env
"
:
env
"
max
-
run
-
time
"
:
7200
}
        
"
run
"
:
{
"
config
"
:
[
"
builds
/
releng_base_mac_64_cross_builds
.
py
"
]
}
        
"
fetches
"
:
{
"
toolchain
"
:
[
"
linux64
-
clang
"
]
}
    
}
def
run
(
run_transform
use_artifact
package_tests
=
True
)
:
    
jobs
=
[
        
per_arch_build
(
"
x64
"
package_tests
)
        
per_arch_build
(
"
aarch64
"
package_tests
)
        
unified_build
(
)
    
]
    
params
=
FakeParameters
(
{
        
"
try_task_config
"
:
{
"
use
-
artifact
-
builds
"
:
use_artifact
}
    
}
)
    
return
list
(
        
run_transform
(
collapse_unified_builds
jobs
kind
=
"
build
"
params
=
params
)
    
)
[
-
1
]
def
test_collapse_unified_build
(
run_transform
)
:
    
job
=
run
(
run_transform
use_artifact
=
True
)
    
assert
"
dependencies
"
not
in
job
    
assert
"
job
-
script
"
not
in
job
[
"
run
"
]
    
assert
job
[
"
run
"
]
[
"
config
"
]
=
=
[
"
builds
/
releng_base_mac_64_cross_builds
.
py
"
]
    
assert
job
[
"
fetches
"
]
=
=
{
"
toolchain
"
:
[
"
linux64
-
clang
"
]
}
    
assert
job
[
"
worker
"
]
[
"
env
"
]
[
"
MOZ_AUTOMATION_PACKAGE_TESTS
"
]
=
=
"
1
"
    
assert
job
[
"
worker
"
]
[
"
max
-
run
-
time
"
]
=
=
7200
pytest
.
mark
.
parametrize
(
    
"
use_artifact
package_tests
"
    
(
        
pytest
.
param
(
False
True
id
=
"
artifact
-
builds
-
disabled
"
)
        
pytest
.
param
(
True
False
id
=
"
tests
-
not
-
packaged
"
)
    
)
)
def
test_unified_build_left_alone
(
run_transform
use_artifact
package_tests
)
:
    
job
=
run
(
run_transform
use_artifact
package_tests
)
    
assert
job
=
=
unified_build
(
)
def
mozconfig_job
(
name
script
=
"
mozharness
/
scripts
/
fx_desktop_build
.
py
"
*
*
run
)
:
    
return
{
        
"
name
"
:
name
        
"
attributes
"
:
{
}
        
"
worker
"
:
{
"
env
"
:
{
}
}
        
"
run
"
:
{
"
script
"
:
script
*
*
run
}
    
}
def
run_mozconfig
(
run_transform
job
release_type
=
"
nightly
"
)
:
    
params
=
FakeParameters
(
{
"
release_type
"
:
release_type
}
)
    
return
list
(
run_transform
(
mozconfig
[
job
]
params
=
params
)
)
[
0
]
pytest
.
mark
.
parametrize
(
    
"
name
run
expected
"
    
(
        
pytest
.
param
(
            
"
linux64
-
shippable
/
opt
"
            
{
"
mozconfig
-
variant
"
:
"
nightly
"
}
            
"
browser
/
config
/
mozconfigs
/
linux64
/
nightly
"
            
id
=
"
default
-
platform
"
        
)
        
pytest
.
param
(
            
"
win64
-
aarch64
-
shippable
/
opt
"
            
{
"
mozconfig
-
variant
"
:
"
nightly
"
}
            
"
browser
/
config
/
mozconfigs
/
win64
-
aarch64
/
nightly
"
            
id
=
"
longest
-
prefix
"
        
)
        
pytest
.
param
(
            
"
macosx64
-
aarch64
/
debug
"
            
{
                
"
mozconfig
-
variant
"
:
"
debug
"
                
"
extra
-
config
"
:
{
"
mozconfig_platform
"
:
"
macosx64
"
}
            
}
            
"
browser
/
config
/
mozconfigs
/
macosx64
/
debug
"
            
id
=
"
explicit
-
platform
-
overrides
-
default
"
        
)
        
pytest
.
param
(
            
"
android
-
x86_64
-
shippable
/
opt
"
            
{
"
mozconfig
-
variant
"
:
"
nightly
"
}
            
"
mobile
/
android
/
config
/
mozconfigs
/
android
-
x86_64
/
nightly
"
            
id
=
"
android
-
app
-
name
"
        
)
        
pytest
.
param
(
            
"
ios
-
sim
/
debug
"
            
{
"
mozconfig
-
variant
"
:
"
debug
"
"
extra
-
config
"
:
{
"
app_name
"
:
"
mobile
/
ios
"
}
}
            
"
mobile
/
ios
/
config
/
mozconfigs
/
ios
-
sim
/
debug
"
            
id
=
"
explicit
-
app
-
name
"
        
)
        
pytest
.
param
(
            
"
win64
-
aarch64
/
debug
"
            
{
                
"
mozconfig
-
variant
"
:
"
debug
"
                
"
extra
-
config
"
:
{
"
mozconfig_platform
"
:
"
win64
-
aarch64
"
}
            
}
            
"
browser
/
config
/
mozconfigs
/
win64
-
aarch64
/
debug
"
            
id
=
"
explicit
-
platform
-
matches
-
default
"
        
)
        
pytest
.
param
(
            
"
firefox
-
source
/
opt
"
            
{
                
"
extra
-
config
"
:
{
                    
"
src_mozconfig
"
:
"
browser
/
config
/
mozconfigs
/
linux64
/
source
"
                
}
            
}
            
"
browser
/
config
/
mozconfigs
/
linux64
/
source
"
            
id
=
"
src
-
mozconfig
"
        
)
        
pytest
.
param
(
            
"
linux64
-
shippable
/
opt
"
            
{
                
"
mozconfig
-
variant
"
:
{
                    
"
by
-
release
-
type
"
:
{
"
beta
"
:
"
beta
"
"
default
"
:
"
nightly
"
}
                
}
            
}
            
"
browser
/
config
/
mozconfigs
/
linux64
/
nightly
"
            
id
=
"
keyed
-
variant
"
        
)
    
)
)
def
test_mozconfig
(
run_transform
name
run
expected
)
:
    
job
=
run_mozconfig
(
run_transform
mozconfig_job
(
name
*
*
run
)
)
    
assert
job
[
"
worker
"
]
[
"
env
"
]
[
"
MOZCONFIG
"
]
=
=
expected
    
assert
"
mozconfig
-
variant
"
not
in
job
[
"
run
"
]
    
for
key
in
(
"
app_name
"
"
mozconfig_platform
"
"
mozconfig_variant
"
"
src_mozconfig
"
)
:
        
assert
key
not
in
job
[
"
run
"
]
.
get
(
"
extra
-
config
"
{
}
)
pytest
.
mark
.
parametrize
(
    
"
name
run
message
"
    
(
        
pytest
.
param
(
            
"
android
-
geckoview
-
docs
/
opt
"
            
{
"
mozconfig
-
variant
"
:
"
nightly
-
android
-
lints
"
}
            
"
needs
mozconfig_platform
"
            
id
=
"
unknown
-
platform
"
        
)
        
pytest
.
param
(
            
"
linux64
/
opt
"
{
}
"
needs
run
.
mozconfig
-
variant
"
id
=
"
missing
-
variant
"
        
)
        
pytest
.
param
(
            
"
linux64
/
opt
"
            
{
                
"
mozconfig
-
variant
"
:
"
nightly
"
                
"
config
-
paths
"
:
[
"
comm
/
testing
/
mozharness
/
configs
"
]
            
}
            
"
needs
app_name
"
            
id
=
"
config
-
paths
-
without
-
app
-
name
"
        
)
    
)
)
def
test_mozconfig_errors
(
run_transform
name
run
message
)
:
    
with
pytest
.
raises
(
Exception
match
=
message
)
:
        
run_mozconfig
(
run_transform
mozconfig_job
(
name
*
*
run
)
)
pytest
.
mark
.
parametrize
(
    
"
job
"
    
(
        
pytest
.
param
(
            
mozconfig_job
(
                
"
linux64
/
opt
"
                
script
=
"
mozharness
/
scripts
/
release
/
generate
-
checksums
.
py
"
                
*
*
{
"
mozconfig
-
variant
"
:
"
nightly
"
}
            
)
            
id
=
"
other
-
script
"
        
)
        
pytest
.
param
(
            
mozconfig_job
(
                
"
macosx64
-
shippable
/
opt
"
                
*
*
{
                    
"
job
-
script
"
:
"
taskcluster
/
scripts
/
misc
/
unify
.
sh
"
                    
"
mozconfig
-
variant
"
:
"
nightly
"
                
}
            
)
            
id
=
"
unify
"
        
)
    
)
)
def
test_mozconfig_not_a_build
(
run_transform
job
)
:
    
job
=
run_mozconfig
(
run_transform
job
)
    
assert
"
MOZCONFIG
"
not
in
job
[
"
worker
"
]
[
"
env
"
]
    
assert
"
mozconfig
-
variant
"
not
in
job
[
"
run
"
]
if
__name__
=
=
"
__main__
"
:
    
main
(
)
