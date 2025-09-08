import
yaml
from
mozbuild
.
repackaging
.
desktop_file
import
generate_browser_desktop_entry
yaml
.
SafeDumper
.
org_represent_str
=
yaml
.
SafeDumper
.
represent_str
def
repr_str
(
dumper
data
)
:
    
if
"
\
n
"
in
data
:
        
return
dumper
.
represent_scalar
(
"
tag
:
yaml
.
org
2002
:
str
"
data
style
=
"
|
"
)
    
return
dumper
.
org_represent_str
(
data
)
yaml
.
add_representer
(
str
repr_str
Dumper
=
yaml
.
SafeDumper
)
class
SnapcraftTransform
:
    
EXPECTED_PARTS
=
[
        
"
rust
"
        
"
cbindgen
"
        
"
clang
"
        
"
dump
-
syms
"
        
"
hunspell
"
        
"
wasi
-
sdk
"
        
"
nodejs
"
        
"
mozconfig
"
        
"
firefox
"
        
"
firefox
-
langpacks
"
        
"
launcher
"
        
"
distribution
"
        
"
ffmpeg
"
        
"
apikeys
"
        
"
debug
-
symbols
"
    
]
    
PARTS_TO_KEEP
=
[
        
"
hunspell
"
        
"
firefox
-
langpacks
"
        
"
launcher
"
        
"
distribution
"
        
"
ffmpeg
"
    
]
    
def
__init__
(
self
source_file
appname
version
buildno
)
:
        
self
.
snap
=
self
.
parse
(
source_file
)
        
self
.
_appname
=
appname
        
self
.
_version
=
version
        
self
.
_buildno
=
buildno
    
def
repack
(
self
)
:
        
removed
=
self
.
keep_non_build_parts
(
)
        
self
.
add_firefox_repack
(
removed
)
        
self
.
fix_distribution
(
)
        
self
.
change_version
(
self
.
_version
self
.
_buildno
)
        
self
.
change_name
(
self
.
_appname
)
        
return
yaml
.
safe_dump
(
self
.
snap
sort_keys
=
False
)
    
def
assert_parts
(
self
snap
)
:
        
"
"
"
        
Make
sure
we
have
the
expected
parts
        
"
"
"
        
parts
=
list
(
snap
[
"
parts
"
]
.
keys
(
)
)
        
assert
parts
=
=
self
.
EXPECTED_PARTS
    
def
keep_non_build_parts
(
self
)
:
        
removed
=
{
}
        
parts_to_delete
=
[
            
key
for
key
in
self
.
snap
[
"
parts
"
]
if
key
not
in
self
.
PARTS_TO_KEEP
        
]
        
for
part
in
parts_to_delete
:
            
removed
[
part
]
=
self
.
snap
[
"
parts
"
]
[
part
]
            
del
self
.
snap
[
"
parts
"
]
[
part
]
        
removed_parts
=
list
(
removed
.
keys
(
)
)
        
for
part
in
self
.
snap
[
"
parts
"
]
:
            
if
"
after
"
in
self
.
snap
[
"
parts
"
]
[
part
]
.
keys
(
)
:
                
self
.
snap
[
"
parts
"
]
[
part
]
[
"
after
"
]
=
[
                    
key
                    
for
key
in
self
.
snap
[
"
parts
"
]
[
part
]
[
"
after
"
]
                    
if
key
not
in
removed_parts
                
]
        
return
removed
    
def
fix_distribution
(
self
)
:
        
self
.
snap
[
"
parts
"
]
[
"
distribution
"
]
.
setdefault
(
"
build
-
packages
"
[
]
)
.
append
(
            
"
git
"
        
)
    
def
add_firefox_repack
(
self
removed
)
:
        
repack_yaml
=
"
"
"
  
firefox
:
    
plugin
:
dump
    
source
:
source
    
override
-
build
:
|
      
craftctl
default
      
cp
CRAFT_PROJECT_DIR
/
default256
.
png
CRAFT_STAGE
/
      
cp
CRAFT_PROJECT_DIR
/
firefox
.
desktop
CRAFT_STAGE
/
"
"
"
        
original
=
removed
[
"
firefox
"
]
        
repack
=
yaml
.
safe_load
(
repack_yaml
)
        
for
original_step
in
original
:
            
if
original_step
in
(
                
"
build
-
packages
"
                
"
override
-
pull
"
                
"
override
-
build
"
                
"
plugin
"
            
)
:
                
continue
            
repack
[
"
firefox
"
]
[
original_step
]
=
original
[
original_step
]
        
current_parts
=
list
(
self
.
snap
[
"
parts
"
]
.
keys
(
)
)
        
repack
[
"
firefox
"
]
[
"
after
"
]
=
[
            
key
for
key
in
original
[
"
after
"
]
if
key
in
current_parts
        
]
        
self
.
snap
[
"
parts
"
]
.
update
(
repack
)
        
if
self
.
_appname
!
=
"
firefox
"
:
            
self
.
snap
[
"
apps
"
]
[
self
.
_appname
]
=
self
.
snap
[
"
apps
"
]
[
"
firefox
"
]
            
del
self
.
snap
[
"
apps
"
]
[
"
firefox
"
]
    
def
change_version
(
self
version
build
)
:
        
self
.
snap
[
"
version
"
]
=
f
"
{
version
}
-
{
build
}
"
    
def
change_name
(
self
name
)
:
        
self
.
snap
[
"
name
"
]
=
str
(
name
)
    
def
parse
(
self
inp
)
:
        
with
open
(
inp
)
as
src
:
            
snap
=
yaml
.
safe_load
(
src
.
read
(
)
)
        
self
.
assert_parts
(
snap
)
        
return
snap
class
SnapDesktopFile
:
    
def
__init__
(
self
log
appname
branchname
wmclass
=
None
)
:
        
if
wmclass
is
None
:
            
wmclass
=
f
"
{
appname
}
-
{
branchname
}
"
        
build_variables
=
{
            
"
PKG_NAME
"
:
appname
            
"
DBusActivatable
"
:
"
false
"
            
"
Icon
"
:
"
/
default256
.
png
"
            
"
REMOTING_NAME
"
:
wmclass
        
}
        
from
fluent
.
runtime
.
fallback
import
FluentLocalization
FluentResourceLoader
        
self
.
desktop
=
generate_browser_desktop_entry
(
            
log
            
build_variables
            
appname
            
branchname
            
FluentLocalization
            
FluentResourceLoader
        
)
    
def
repack
(
self
)
:
        
return
"
\
n
"
.
join
(
self
.
desktop
)
