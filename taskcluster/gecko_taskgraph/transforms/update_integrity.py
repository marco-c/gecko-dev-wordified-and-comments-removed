import
shlex
import
urllib
.
parse
import
requests
from
mozilla_version
.
gecko
import
GeckoVersion
from
mozrelease
.
paths
import
getNightlyDir
getReleaseInstallerPath
getReleasesDir
from
mozrelease
.
platforms
import
buildPlatform2ftp
updatePlatform2ftp
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
schema
import
resolve_keyed_by
transforms
=
TransformSequence
(
)
transforms
.
add
def
skip_for_non_nightly
(
config
jobs
)
:
    
"
"
"
Don
'
t
generate
any
jobs
unless
running
as
a
nightly
.
Other
code
in
this
transform
depends
on
nightly
-
specific
parameters
being
set
.
"
"
"
    
if
not
config
.
params
[
"
release_history
"
]
:
        
return
    
yield
from
jobs
transforms
.
add
def
add_build_target
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
.
startswith
(
"
linux64
-
aarch64
"
)
:
            
build_target
=
"
Linux_aarch64
-
gcc3
"
        
elif
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
.
startswith
(
"
linux64
"
)
:
            
build_target
=
"
Linux_x86_64
-
gcc3
"
        
elif
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
.
startswith
(
"
mac
"
)
:
            
build_target
=
"
Darwin_x86_64
-
gcc3
-
u
-
i386
-
x86_64
"
        
elif
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
.
startswith
(
"
win32
"
)
:
            
build_target
=
"
WINNT_x86
-
msvc
"
        
elif
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
.
startswith
(
"
win64
-
aarch64
"
)
:
            
build_target
=
"
WINNT_aarch64
-
msvc
-
aarch64
"
        
elif
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
.
startswith
(
"
win64
"
)
:
            
build_target
=
"
WINNT_x86_64
-
msvc
"
        
else
:
            
raise
Exception
(
"
couldn
'
t
detect
build
target
"
)
        
job
[
"
attributes
"
]
[
"
build_target
"
]
=
build_target
        
yield
job
transforms
.
add
def
skip_for_new_locales_and_platforms
(
config
jobs
)
:
    
"
"
"
Don
'
t
generate
any
jobs
for
newly
added
locales
or
platforms
that
don
'
t
have
from
releases
to
test
.
"
"
"
    
for
job
in
jobs
:
        
locale
=
job
[
"
attributes
"
]
.
get
(
"
locale
"
"
en
-
US
"
)
        
build_target
=
job
[
"
attributes
"
]
[
"
build_target
"
]
        
if
locale
not
in
config
.
params
[
"
release_history
"
]
.
get
(
build_target
{
}
)
:
            
continue
        
yield
job
transforms
.
add
def
resolve_keys
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
        
for
key
in
(
            
"
cert
-
overrides
"
            
"
fetches
.
toolchain
"
            
"
archive
-
prefix
"
            
"
last
-
watershed
"
        
)
:
            
resolve_keyed_by
(
                
job
                
key
                
job
[
"
name
"
]
                
*
*
{
                    
"
build
-
platform
"
:
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
                    
"
release
-
type
"
:
config
.
params
[
"
release_type
"
]
                    
"
locale
"
:
job
[
"
attributes
"
]
.
get
(
"
locale
"
"
en
-
US
"
)
                    
"
shipping
-
product
"
:
job
[
"
attributes
"
]
[
"
shipping_product
"
]
                
}
            
)
        
yield
job
transforms
.
add
def
set_treeherder
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
        
th
=
job
.
setdefault
(
"
treeherder
"
{
}
)
        
attrs
=
job
[
"
attributes
"
]
        
attrs
[
"
locale
"
]
=
attrs
.
get
(
"
locale
"
"
en
-
US
"
)
        
th
[
"
platform
"
]
=
f
"
{
attrs
[
'
build_platform
'
]
}
/
{
attrs
[
'
build_type
'
]
}
"
        
th
[
"
symbol
"
]
=
th
[
"
symbol
"
]
.
format
(
*
*
attrs
)
        
yield
job
transforms
.
add
def
adjust_locale_watershed
(
config
jobs
)
:
    
"
"
"
Adjusts
the
last
-
watershed
for
locales
that
are
newer
than
the
last
    
general
watershed
.
eg
:
if
last
-
watershed
is
72
.
0
but
sco
didn
'
t
ship
    
91
.
0
it
will
be
adjusted
to
91
.
0
.
"
"
"
    
locale_history_cache
=
{
}
    
for
job
in
jobs
:
        
history_file
=
job
.
pop
(
"
locale
-
history
-
file
"
)
        
if
history_file
in
locale_history_cache
:
            
locale_history
=
locale_history_cache
[
history_file
]
        
else
:
            
req
=
requests
.
get
(
history_file
)
            
req
.
raise_for_status
(
)
            
locale_history
=
req
.
json
(
)
            
locale_history_cache
[
history_file
]
=
locale_history
        
last_watershed
=
job
[
"
last
-
watershed
"
]
        
locale
=
job
[
"
attributes
"
]
.
get
(
"
locale
"
"
en
-
US
"
)
        
channel
=
job
[
"
attributes
"
]
[
"
update
-
channel
"
]
        
if
channel
=
=
"
nightly
-
try
"
:
            
channel
=
"
nightly
"
        
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
            
yield
job
            
continue
        
if
not
locale_history
.
get
(
locale
{
}
)
.
get
(
"
first_release
"
{
}
)
.
get
(
channel
)
:
            
continue
        
first_release
=
locale_history
[
locale
]
[
"
first_release
"
]
[
channel
]
        
watershed_version
=
GeckoVersion
.
parse
(
last_watershed
[
"
version
"
]
)
        
first_version
=
GeckoVersion
.
parse
(
first_release
[
"
version
"
]
)
        
if
channel
=
=
"
nightly
"
:
            
if
(
                
watershed_version
<
=
first_version
                
and
last_watershed
[
"
buildid
"
]
<
first_release
[
"
buildid
"
]
            
)
:
                
job
[
"
last
-
watershed
"
]
=
first_release
        
elif
watershed_version
<
first_version
:
            
job
[
"
last
-
watershed
"
]
=
first_release
        
yield
job
transforms
.
add
def
add_to_installer
(
config
jobs
)
:
    
"
"
"
Adds
fetch
entries
for
the
"
to
"
installer
to
fetches
.
"
"
"
    
for
job
in
jobs
:
        
locale
=
job
[
"
attributes
"
]
.
get
(
"
locale
"
"
en
-
US
"
)
        
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
            
if
"
linux
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
:
                
job
[
"
fetches
"
]
[
"
build
-
signing
"
]
=
[
                    
{
"
artifact
"
:
"
target
.
tar
.
xz
"
"
extract
"
:
False
}
                
]
            
elif
"
mac
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
:
                
job
[
"
fetches
"
]
[
"
repackage
"
]
=
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
}
]
            
elif
"
win
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
:
                
job
[
"
fetches
"
]
[
"
repackage
"
]
=
[
{
"
artifact
"
:
"
target
.
installer
.
exe
"
}
]
            
else
:
                
raise
Exception
(
                    
"
unsupported
platform
:
{
job
[
'
attributes
'
]
[
'
build_platform
'
]
}
!
"
                
)
        
else
:
            
if
"
linux
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
:
                
job
[
"
fetches
"
]
[
"
shippable
-
l10n
-
signing
"
]
=
[
                    
{
"
artifact
"
:
f
"
{
locale
}
/
target
.
tar
.
xz
"
"
extract
"
:
False
}
                
]
            
elif
"
mac
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
:
                
job
[
"
fetches
"
]
[
"
repackage
-
l10n
"
]
=
[
                    
{
"
artifact
"
:
f
"
{
locale
}
/
target
.
dmg
"
}
                
]
            
elif
"
win
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
:
                
job
[
"
fetches
"
]
[
"
repackage
-
l10n
"
]
=
[
                    
{
"
artifact
"
:
f
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
}
                
]
            
else
:
                
raise
Exception
(
                    
"
unsupported
platform
:
{
job
[
'
attributes
'
]
[
'
build_platform
'
]
}
!
"
                
)
        
yield
job
transforms
.
add
def
add_additional_fetches_and_command
(
config
jobs
)
:
    
"
"
"
Adds
fetch
entries
for
the
"
from
"
installers
and
partial
MARs
.
"
"
"
    
for
job
in
jobs
:
        
build_platform
=
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
        
if
build_platform
.
startswith
(
"
linux
"
)
:
            
platform
=
"
linux
"
            
installer_suffix
=
"
tar
.
xz
"
        
elif
build_platform
.
startswith
(
"
mac
"
)
:
            
platform
=
"
mac
"
            
installer_suffix
=
"
dmg
"
        
elif
build_platform
.
startswith
(
"
win
"
)
:
            
platform
=
"
win
"
            
installer_suffix
=
"
installer
.
exe
"
        
else
:
            
raise
Exception
(
"
couldn
'
t
detect
platform
specific
variables
"
)
        
locale
=
job
[
"
attributes
"
]
.
get
(
"
locale
"
"
en
-
US
"
)
        
linux_locale
=
"
ja
"
if
locale
=
=
"
ja
-
JP
-
mac
"
else
locale
        
build_target
=
job
[
"
attributes
"
]
[
"
build_target
"
]
        
product
=
job
.
pop
(
"
product
"
)
        
brand
=
job
[
"
attributes
"
]
[
"
shipping_product
"
]
        
cmd
=
[
            
"
export
PATH
=
MOZ_FETCHES_DIR
/
dmg
:
PATH
&
&
"
            
"
/
builds
/
worker
/
fetches
/
marannon
/
marannon
"
            
"
tools
/
update
-
verify
/
release
/
common
/
check_updates
.
sh
"
            
platform
            
f
"
/
builds
/
worker
/
fetches
/
target
.
{
installer_suffix
}
"
            
"
/
builds
/
worker
/
fetches
/
target
.
complete
.
mar
"
            
"
/
builds
/
worker
/
fetches
"
            
locale
            
job
[
"
attributes
"
]
[
"
update
-
channel
"
]
            
product
            
"
/
builds
/
worker
/
artifacts
"
        
]
        
cert_overrides
=
job
.
pop
(
"
cert
-
overrides
"
)
        
if
cert_overrides
:
            
cmd
.
extend
(
[
                
"
-
-
cert
-
dir
"
                
"
tools
/
update
-
verify
/
release
/
mar_certs
"
            
]
)
            
for
override
in
cert_overrides
:
                
cmd
.
extend
(
[
"
-
-
cert
-
override
"
shlex
.
quote
(
override
)
]
)
        
archive_prefix
=
job
.
pop
(
"
archive
-
prefix
"
)
        
tested_identifiers
=
set
(
)
        
fetches
=
[
]
        
for
mar
info
in
config
.
params
[
"
release_history
"
]
[
build_target
]
[
locale
]
.
items
(
)
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
                
mar_prefix
=
"
"
            
else
:
                
mar_prefix
=
f
"
{
locale
}
/
"
            
fetches
.
append
(
{
"
artifact
"
:
f
"
{
mar_prefix
}
{
mar
}
"
}
)
            
if
"
nightly
"
in
info
[
"
mar_url
"
]
:
                
base_url
=
info
[
"
mar_url
"
]
.
split
(
"
.
complete
.
mar
"
)
[
0
]
                
identifier
=
info
[
"
buildid
"
]
                
linux64_info
=
config
.
params
[
"
release_history
"
]
[
"
Linux_x86_64
-
gcc3
"
]
[
                    
linux_locale
                
]
[
mar
]
                
from_installer_url
=
f
"
{
base_url
}
.
{
installer_suffix
}
"
                
linux64_installer_url
=
linux64_info
[
"
mar_url
"
]
.
replace
(
                    
"
.
complete
.
mar
"
"
.
tar
.
xz
"
                
)
            
else
:
                
identifier
=
info
[
"
previousVersion
"
]
                
from_installer_url
=
_get_release_installer_url
(
                    
brand
                    
product
                    
build_target
                    
locale
                    
info
[
"
previousVersion
"
]
                    
archive_prefix
                
)
                
linux64_installer_url
=
_get_release_installer_url
(
                    
brand
                    
product
                    
"
Linux_x86_64
-
gcc3
"
                    
linux_locale
                    
info
[
"
previousVersion
"
]
                    
archive_prefix
                
)
            
cmd
.
append
(
"
-
-
from
"
)
            
cmd
.
append
(
                
shlex
.
quote
(
                    
f
"
{
identifier
}
|
{
from_installer_url
}
|
{
linux64_installer_url
}
|
{
mar
}
"
                
)
            
)
            
tested_identifiers
.
add
(
identifier
)
        
last_watershed
=
job
.
pop
(
"
last
-
watershed
"
)
        
if
config
.
params
[
"
release_type
"
]
=
=
"
nightly
"
:
            
watershed_identifier
=
last_watershed
[
"
buildid
"
]
            
if
watershed_identifier
not
in
tested_identifiers
:
                
nightly_dir
=
getNightlyDir
(
                    
product
                    
last_watershed
[
"
buildid
"
]
                    
locale
                    
config
.
params
[
"
project
"
]
                    
protocol
=
"
https
"
                    
server
=
archive_prefix
                
)
                
version
=
last_watershed
[
"
version
"
]
                
platform
=
buildPlatform2ftp
(
build_platform
)
                
linux_suffix
=
"
tar
.
xz
"
                
if
GeckoVersion
.
parse
(
version
)
<
GeckoVersion
.
parse
(
"
135
.
0a1
"
)
:
                    
installer_suffix
=
installer_suffix
.
replace
(
"
xz
"
"
bz2
"
)
                    
linux_suffix
=
"
tar
.
bz2
"
                
from_installer_url
=
f
"
{
nightly_dir
}
/
{
product
}
-
{
version
}
.
{
locale
}
.
{
platform
}
.
{
installer_suffix
}
"
                
linux64_installer_url
=
f
"
{
nightly_dir
}
/
{
product
}
-
{
version
}
.
{
linux_locale
}
.
linux
-
x86_64
.
{
linux_suffix
}
"
                
cmd
.
append
(
"
-
-
from
"
)
                
cmd
.
append
(
                    
shlex
.
quote
(
                        
f
"
{
watershed_identifier
}
|
{
from_installer_url
}
|
{
linux64_installer_url
}
"
                    
)
                
)
        
else
:
            
watershed_identifier
=
last_watershed
[
"
version
"
]
            
if
watershed_identifier
not
in
tested_identifiers
:
                
from_installer_url
=
_get_release_installer_url
(
                    
brand
                    
product
                    
build_target
                    
locale
                    
last_watershed
[
"
version
"
]
                    
archive_prefix
                
)
                
linux64_installer_url
=
_get_release_installer_url
(
                    
brand
                    
product
                    
"
Linux_x86_64
-
gcc3
"
                    
linux_locale
                    
last_watershed
[
"
version
"
]
                    
archive_prefix
                
)
                
cmd
.
append
(
"
-
-
from
"
)
                
cmd
.
append
(
                    
shlex
.
quote
(
                        
f
"
{
watershed_identifier
}
|
{
from_installer_url
}
|
{
linux64_installer_url
}
"
                    
)
                
)
        
job
[
"
fetches
"
]
[
"
partials
-
signing
"
]
=
fetches
        
job
[
"
run
"
]
[
"
command
"
]
=
"
"
.
join
(
cmd
)
        
yield
job
def
_get_release_installer_url
(
    
brand
product
build_target
locale
from_version
archive_prefix
)
:
    
ftp_platform
=
updatePlatform2ftp
(
build_target
)
    
releases_dir
=
getReleasesDir
(
        
brand
from_version
protocol
=
"
https
"
server
=
archive_prefix
    
)
    
path
=
urllib
.
parse
.
quote
(
        
getReleaseInstallerPath
(
            
product
product
.
capitalize
(
)
from_version
ftp_platform
locale
        
)
    
)
    
return
f
"
{
releases_dir
}
/
{
path
}
"
