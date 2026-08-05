"
"
"
L10n
manifest
data
structures
and
helpers
.
The
l10n
manifest
is
written
during
configure
to
<
topobjdir
>
/
l10n
-
manifest
.
json
and
read
during
command
time
.
All
data
structures
of
interest
are
children
of
the
L10nManifest
class
.
jar
.
mn
entries
are
captured
with
AB_CD
=
MOZ_L10N_AB_CD_PLACEHOLDER
so
the
manifest
stays
locale
-
independent
and
are
resolved
during
staging
.
"
"
"
import
json
from
dataclasses
import
asdict
dataclass
field
from
pathlib
import
Path
MANIFEST_VERSION
=
1
MOZ_L10N_AB_CD_PLACEHOLDER
=
"
MOZ_L10N_AB_CD_PLACEHOLDER
"
dataclass
class
JarEntry
:
    
"
"
"
One
entry
inside
a
jar
.
mn
group
.
"
"
"
    
source
:
str
    
output
:
str
    
is_locale
:
bool
    
preprocess
:
bool
dataclass
class
JarSection
:
    
"
"
"
One
jar
.
mn
group
'
s
locale
-
aware
data
captured
for
any
locale
.
    
relativesrcdir
mirrors
jarinfo
.
relativesrcdir
and
drives
the
    
merge
-
tree
subdir
for
is_locale
entries
.
    
"
"
"
    
name
:
str
    
base
:
str
    
relativesrcdir
:
str
    
chrome_manifests
:
list
[
str
]
    
pp_includes
:
list
[
str
]
    
entries
:
list
[
JarEntry
]
dataclass
class
LocalizedFileGroup
:
    
"
"
"
One
LOCALIZED_FILES
/
LOCALIZED_PP_FILES
group
for
a
context
.
"
"
"
    
subpath
:
str
    
sources
:
list
[
str
]
dataclass
class
LocalizedGenScript
:
    
"
"
"
One
LOCALIZED_GENERATED_FILES
script
invocation
locale
-
templated
.
"
"
"
    
script
:
str
    
method
:
str
    
inputs
:
list
[
str
]
    
outputs
:
list
[
str
]
    
flags
:
list
[
str
]
    
force
:
bool
dataclass
class
L10nManifestContextData
:
    
"
"
"
Per
-
moz
.
build
-
context
l10n
data
.
"
"
"
    
relsrcdir
:
str
    
install_subdir
:
str
    
defines
:
dict
[
str
object
]
    
locale_pp_defines
:
dict
[
str
dict
[
str
str
]
]
    
jar_sections
:
list
[
JarSection
]
=
field
(
default_factory
=
list
)
    
localized_files
:
list
[
LocalizedFileGroup
]
=
field
(
default_factory
=
list
)
    
localized_pp_files
:
list
[
LocalizedFileGroup
]
=
field
(
default_factory
=
list
)
    
localized_generated_files
:
list
[
LocalizedGenScript
]
=
field
(
default_factory
=
list
)
dataclass
class
L10nManifest
:
    
"
"
"
topobjdir
l10n
manifest
.
"
"
"
    
version
:
int
    
moz_app_id
:
str
    
moz_app_version
:
str
    
moz_app_displayname
:
str
    
moz_build_app
:
str
    
contexts
:
list
[
L10nManifestContextData
]
=
field
(
default_factory
=
list
)
def
write_l10n_manifest
(
manifest
:
L10nManifest
path
:
Path
)
-
>
None
:
    
path
.
parent
.
mkdir
(
parents
=
True
exist_ok
=
True
)
    
with
path
.
open
(
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
f
:
        
json
.
dump
(
asdict
(
manifest
)
f
indent
=
2
sort_keys
=
True
)
def
load_l10n_manifest
(
path
:
Path
)
-
>
L10nManifest
:
    
with
path
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
f
:
        
raw
=
json
.
load
(
f
)
    
if
raw
.
get
(
"
version
"
)
!
=
MANIFEST_VERSION
:
        
raise
ValueError
(
            
f
"
Unsupported
l10n
manifest
version
:
{
raw
.
get
(
'
version
'
)
!
r
}
"
            
f
"
(
expected
{
MANIFEST_VERSION
}
)
"
        
)
    
contexts
=
[
        
L10nManifestContextData
(
            
relsrcdir
=
c
[
"
relsrcdir
"
]
            
install_subdir
=
c
[
"
install_subdir
"
]
            
defines
=
c
[
"
defines
"
]
            
locale_pp_defines
=
c
[
"
locale_pp_defines
"
]
            
jar_sections
=
[
                
JarSection
(
                    
name
=
s
[
"
name
"
]
                    
base
=
s
[
"
base
"
]
                    
relativesrcdir
=
s
[
"
relativesrcdir
"
]
                    
chrome_manifests
=
s
[
"
chrome_manifests
"
]
                    
pp_includes
=
s
[
"
pp_includes
"
]
                    
entries
=
[
JarEntry
(
*
*
e
)
for
e
in
s
[
"
entries
"
]
]
                
)
                
for
s
in
c
[
"
jar_sections
"
]
            
]
            
localized_files
=
[
LocalizedFileGroup
(
*
*
g
)
for
g
in
c
[
"
localized_files
"
]
]
            
localized_pp_files
=
[
                
LocalizedFileGroup
(
*
*
g
)
for
g
in
c
[
"
localized_pp_files
"
]
            
]
            
localized_generated_files
=
[
                
LocalizedGenScript
(
*
*
g
)
for
g
in
c
[
"
localized_generated_files
"
]
            
]
        
)
        
for
c
in
raw
[
"
contexts
"
]
    
]
    
return
L10nManifest
(
        
version
=
raw
[
"
version
"
]
        
moz_app_id
=
raw
[
"
moz_app_id
"
]
        
moz_app_version
=
raw
[
"
moz_app_version
"
]
        
moz_app_displayname
=
raw
[
"
moz_app_displayname
"
]
        
moz_build_app
=
raw
[
"
moz_build_app
"
]
        
contexts
=
contexts
    
)
def
build_l10n_manifest_from_substs
(
    
substs
:
dict
[
str
object
]
    
context_data_list
:
list
[
L10nManifestContextData
]
)
-
>
L10nManifest
:
    
return
L10nManifest
(
        
version
=
MANIFEST_VERSION
        
moz_app_id
=
substs
.
get
(
"
MOZ_APP_ID
"
)
or
"
"
        
moz_app_version
=
substs
.
get
(
"
MOZ_APP_VERSION
"
)
or
"
"
        
moz_app_displayname
=
substs
.
get
(
"
MOZ_APP_DISPLAYNAME
"
)
or
"
"
        
moz_build_app
=
substs
.
get
(
"
MOZ_BUILD_APP
"
)
or
"
"
        
contexts
=
list
(
context_data_list
)
    
)
