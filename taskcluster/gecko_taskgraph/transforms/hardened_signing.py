"
"
"
Transform
the
signing
task
into
an
actual
task
description
.
"
"
"
import
copy
from
taskgraph
.
transforms
.
base
import
TransformSequence
from
taskgraph
.
util
.
dependencies
import
get_primary_dependency
from
taskgraph
.
util
.
keyed_by
import
evaluate_keyed_by
from
gecko_taskgraph
.
util
.
attributes
import
release_level
transforms
=
TransformSequence
(
)
PROVISIONING_PROFILE_FILENAMES
=
{
    
"
firefox
"
:
"
orgmozillafirefox
.
provisionprofile
"
    
"
devedition
"
:
"
orgmozillafirefoxdeveloperedition
.
provisionprofile
"
    
"
nightly
"
:
"
orgmozillanightly
.
provisionprofile
"
}
transforms
.
add
def
add_hardened_sign_config
(
config
jobs
)
:
    
for
job
in
jobs
:
        
if
(
            
"
signing
"
not
in
config
.
kind
            
or
"
macosx
"
not
in
job
[
"
attributes
"
]
[
"
build_platform
"
]
        
)
:
            
yield
job
            
continue
        
dep_job
=
get_primary_dependency
(
config
job
)
        
assert
dep_job
        
project_level
=
release_level
(
config
.
params
[
"
project
"
]
)
        
is_shippable
=
dep_job
.
attributes
.
get
(
"
shippable
"
False
)
        
hardened_signing_type
=
"
developer
"
        
if
project_level
=
=
"
production
"
and
is_shippable
:
            
hardened_signing_type
=
"
production
"
        
hardened_sign_config
=
evaluate_keyed_by
(
            
copy
.
deepcopy
(
config
.
graph_config
[
"
mac
-
signing
"
]
[
"
hardened
-
sign
-
config
"
]
)
            
"
hardened
-
sign
-
config
"
            
{
"
hardened
-
signing
-
type
"
:
hardened_signing_type
}
        
)
        
if
not
isinstance
(
hardened_sign_config
list
)
:
            
raise
Exception
(
"
hardened
-
sign
-
config
must
be
a
list
"
)
        
for
sign_cfg
in
hardened_sign_config
:
            
if
isinstance
(
sign_cfg
.
get
(
"
entitlements
"
)
dict
)
:
                
sign_cfg
[
"
entitlements
"
]
=
evaluate_keyed_by
(
                    
sign_cfg
[
"
entitlements
"
]
                    
"
entitlements
"
                    
{
                        
"
build
-
platform
"
:
dep_job
.
attributes
.
get
(
"
build_platform
"
)
                        
"
project
"
:
config
.
params
[
"
project
"
]
                    
}
                
)
            
if
"
entitlements
"
in
sign_cfg
and
not
sign_cfg
.
get
(
                
"
entitlements
"
"
"
            
)
.
startswith
(
"
http
"
)
:
                
sign_cfg
[
"
entitlements
"
]
=
config
.
params
.
file_url
(
                    
sign_cfg
[
"
entitlements
"
]
                
)
        
job
[
"
worker
"
]
[
"
hardened
-
sign
-
config
"
]
=
hardened_sign_config
        
job
[
"
worker
"
]
[
"
mac
-
behavior
"
]
=
"
mac_sign_and_pkg_hardened
"
        
yield
job
transforms
.
add
def
add_provisioning_profile_config
(
config
jobs
)
:
    
for
job
in
jobs
:
        
dep_job
=
get_primary_dependency
(
config
job
)
        
assert
dep_job
        
if
(
            
"
signing
"
in
config
.
kind
            
and
"
macosx
"
in
job
[
"
attributes
"
]
[
"
build_platform
"
]
            
and
release_level
(
config
.
params
[
"
project
"
]
)
=
=
"
production
"
            
and
dep_job
.
attributes
.
get
(
"
shippable
"
False
)
        
)
:
            
if
"
devedition
"
in
dep_job
.
attributes
.
get
(
"
build_platform
"
"
"
)
:
                
filename
=
PROVISIONING_PROFILE_FILENAMES
[
"
devedition
"
]
            
elif
config
.
params
[
"
project
"
]
=
=
"
mozilla
-
central
"
:
                
filename
=
PROVISIONING_PROFILE_FILENAMES
[
"
nightly
"
]
            
else
:
                
filename
=
PROVISIONING_PROFILE_FILENAMES
[
"
firefox
"
]
            
job
[
"
worker
"
]
[
"
provisioning
-
profile
-
config
"
]
=
[
                
{
                    
"
profile_name
"
:
filename
                    
"
target_path
"
:
"
/
Contents
/
embedded
.
provisionprofile
"
                
}
            
]
        
yield
job
