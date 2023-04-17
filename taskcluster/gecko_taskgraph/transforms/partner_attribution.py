"
"
"
Transform
the
partner
attribution
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
from
collections
import
defaultdict
import
json
import
logging
from
gecko_taskgraph
.
transforms
.
base
import
TransformSequence
from
gecko_taskgraph
.
util
.
partners
import
(
    
apply_partner_priority
    
check_if_partners_enabled
    
get_partner_config_by_kind
    
generate_attribution_code
)
log
=
logging
.
getLogger
(
__name__
)
transforms
=
TransformSequence
(
)
transforms
.
add
(
check_if_partners_enabled
)
transforms
.
add
(
apply_partner_priority
)
transforms
.
add
def
add_command_arguments
(
config
tasks
)
:
    
enabled_partners
=
config
.
params
.
get
(
"
release_partners
"
)
    
dependencies
=
{
}
    
fetches
=
defaultdict
(
set
)
    
attributions
=
[
]
    
release_artifacts
=
[
]
    
attribution_config
=
get_partner_config_by_kind
(
config
config
.
kind
)
    
for
partner_config
in
attribution_config
.
get
(
"
configs
"
[
]
)
:
        
if
enabled_partners
and
partner_config
[
"
campaign
"
]
not
in
enabled_partners
:
            
continue
        
attribution_code
=
generate_attribution_code
(
            
attribution_config
[
"
defaults
"
]
partner_config
        
)
        
for
platform
in
partner_config
[
"
platforms
"
]
:
            
stage_platform
=
platform
.
replace
(
"
-
shippable
"
"
"
)
            
for
locale
in
partner_config
[
"
locales
"
]
:
                
if
locale
=
=
"
en
-
US
"
:
                    
upstream_label
=
"
repackage
-
signing
-
{
platform
}
/
opt
"
.
format
(
                        
platform
=
platform
                    
)
                    
upstream_artifact
=
"
target
.
installer
.
exe
"
                
else
:
                    
upstream_label
=
(
                        
"
repackage
-
signing
-
l10n
-
{
locale
}
-
{
platform
}
/
opt
"
.
format
(
                            
locale
=
locale
platform
=
platform
                        
)
                    
)
                    
upstream_artifact
=
"
{
locale
}
/
target
.
installer
.
exe
"
.
format
(
                        
locale
=
locale
                    
)
                
if
upstream_label
not
in
config
.
kind_dependencies_tasks
:
                    
raise
Exception
(
f
"
Can
'
t
find
upstream
task
for
{
platform
}
{
locale
}
"
)
                
upstream
=
config
.
kind_dependencies_tasks
[
upstream_label
]
                
dependencies
.
update
(
{
upstream
.
label
:
upstream
.
label
}
)
                
fetches
[
upstream_label
]
.
add
(
(
upstream_artifact
stage_platform
locale
)
)
                
artifact_part
=
"
{
platform
}
/
{
locale
}
/
target
.
installer
.
exe
"
.
format
(
                    
platform
=
stage_platform
locale
=
locale
                
)
                
artifact
=
(
                    
"
releng
/
partner
/
{
partner
}
/
{
sub_partner
}
/
{
artifact_part
}
"
.
format
(
                        
partner
=
partner_config
[
"
campaign
"
]
                        
sub_partner
=
partner_config
[
"
content
"
]
                        
artifact_part
=
artifact_part
                    
)
                
)
                
attributions
.
append
(
                    
{
                        
"
input
"
:
f
"
/
builds
/
worker
/
fetches
/
{
artifact_part
}
"
                        
"
output
"
:
f
"
/
builds
/
worker
/
artifacts
/
{
artifact
}
"
                        
"
attribution
"
:
attribution_code
                    
}
                
)
                
release_artifacts
.
append
(
artifact
)
    
if
not
attributions
:
        
return
    
for
task
in
tasks
:
        
worker
=
task
.
get
(
"
worker
"
{
}
)
        
worker
[
"
chain
-
of
-
trust
"
]
=
True
        
task
.
setdefault
(
"
dependencies
"
{
}
)
.
update
(
dependencies
)
        
task
.
setdefault
(
"
fetches
"
{
}
)
        
for
upstream_label
upstream_artifacts
in
fetches
.
items
(
)
:
            
task
[
"
fetches
"
]
[
upstream_label
]
=
[
                
{
                    
"
artifact
"
:
upstream_artifact
                    
"
dest
"
:
"
{
platform
}
/
{
locale
}
"
.
format
(
                        
platform
=
platform
locale
=
locale
                    
)
                    
"
extract
"
:
False
                    
"
verify
-
hash
"
:
True
                
}
                
for
upstream_artifact
platform
locale
in
upstream_artifacts
            
]
        
worker
.
setdefault
(
"
env
"
{
}
)
[
"
ATTRIBUTION_CONFIG
"
]
=
json
.
dumps
(
            
attributions
sort_keys
=
True
        
)
        
worker
[
"
artifacts
"
]
=
[
            
{
                
"
name
"
:
"
releng
/
partner
"
                
"
path
"
:
"
/
builds
/
worker
/
artifacts
/
releng
/
partner
"
                
"
type
"
:
"
directory
"
            
}
        
]
        
task
[
"
release
-
artifacts
"
]
=
release_artifacts
        
task
[
"
label
"
]
=
config
.
kind
        
yield
task
