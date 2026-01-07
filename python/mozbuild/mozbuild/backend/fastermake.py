from
collections
import
defaultdict
from
operator
import
itemgetter
import
mozpack
.
path
as
mozpath
from
mozpack
.
manifests
import
InstallManifest
from
mozbuild
.
backend
.
base
import
PartialBackend
from
mozbuild
.
backend
.
make
import
MakeBackend
from
mozbuild
.
frontend
.
context
import
ObjDirPath
Path
from
mozbuild
.
frontend
.
data
import
(
    
ChromeManifestEntry
    
FinalTargetFiles
    
FinalTargetPreprocessedFiles
    
GeneratedFile
    
JARManifest
    
LocalizedFiles
    
LocalizedPreprocessedFiles
    
XPIDLModule
)
from
mozbuild
.
makeutil
import
Makefile
class
FasterMakeBackend
(
MakeBackend
PartialBackend
)
:
    
def
_init
(
self
)
:
        
super
(
)
.
_init
(
)
        
self
.
_manifest_entries
=
defaultdict
(
set
)
        
self
.
_install_manifests
=
defaultdict
(
InstallManifest
)
        
self
.
_dependencies
=
defaultdict
(
list
)
        
self
.
_l10n_dependencies
=
defaultdict
(
list
)
        
self
.
_has_xpidl
=
False
        
self
.
_generated_files_map
=
{
}
        
self
.
_generated_files
=
[
]
    
def
_add_preprocess
(
self
obj
src
dest
f
*
*
kwargs
)
:
        
basename
=
FinalTargetPreprocessedFiles
.
get_obj_basename
(
f
)
        
if
basename
.
endswith
(
"
.
css
"
)
:
            
kwargs
[
"
marker
"
]
=
"
%
"
        
depfile
=
mozpath
.
join
(
            
self
.
environment
.
topobjdir
            
"
faster
"
            
"
.
deps
"
            
mozpath
.
join
(
obj
.
install_target
dest
basename
)
.
replace
(
"
/
"
"
_
"
)
        
)
        
self
.
_install_manifests
[
obj
.
install_target
]
.
add_preprocess
(
            
mozpath
.
join
(
obj
.
srcdir
src
)
            
mozpath
.
join
(
dest
basename
)
            
depfile
            
*
*
kwargs
        
)
    
def
consume_object
(
self
obj
)
:
        
if
isinstance
(
obj
JARManifest
)
and
obj
.
install_target
.
startswith
(
"
dist
/
bin
"
)
:
            
self
.
_consume_jar_manifest
(
obj
)
        
elif
isinstance
(
            
obj
(
FinalTargetFiles
FinalTargetPreprocessedFiles
)
        
)
and
obj
.
install_target
.
startswith
(
"
dist
/
bin
"
)
:
            
ab_cd
=
self
.
environment
.
substs
[
"
MOZ_UI_LOCALE
"
]
            
localized
=
isinstance
(
obj
(
LocalizedFiles
LocalizedPreprocessedFiles
)
)
            
defines
=
obj
.
defines
or
{
}
            
if
defines
:
                
defines
=
defines
.
defines
            
for
path
files
in
obj
.
files
.
walk
(
)
:
                
for
f
in
files
:
                    
if
localized
and
not
isinstance
(
f
ObjDirPath
)
and
ab_cd
!
=
"
en
-
US
"
:
                        
src
=
self
.
localized_path
(
obj
.
relsrcdir
f
)
                        
dep_target
=
"
install
-
%
s
"
%
obj
.
install_target
                        
if
"
*
"
not
in
src
:
                            
merge
=
mozpath
.
abspath
(
                                
mozpath
.
join
(
                                    
self
.
environment
.
topobjdir
                                    
"
l10n_merge
"
                                    
obj
.
relsrcdir
                                    
f
                                
)
                            
)
                            
self
.
_l10n_dependencies
[
dep_target
]
.
append
(
(
                                
merge
                                
f
.
full_path
                                
src
                            
)
)
                            
src
=
merge
                    
else
:
                        
src
=
f
.
full_path
                    
if
isinstance
(
obj
FinalTargetPreprocessedFiles
)
:
                        
self
.
_add_preprocess
(
obj
src
path
f
defines
=
defines
)
                    
elif
"
*
"
in
f
:
                        
def
_prefix
(
s
)
:
                            
for
p
in
mozpath
.
split
(
s
)
:
                                
if
"
*
"
not
in
p
:
                                    
yield
p
+
"
/
"
                        
prefix
=
"
"
.
join
(
_prefix
(
src
)
)
                        
if
"
*
"
in
f
.
target_basename
:
                            
target
=
path
                        
else
:
                            
target
=
mozpath
.
join
(
path
f
.
target_basename
)
                        
self
.
_install_manifests
[
obj
.
install_target
]
.
add_pattern_link
(
                            
prefix
src
[
len
(
prefix
)
:
]
target
                        
)
                    
else
:
                        
self
.
_install_manifests
[
obj
.
install_target
]
.
add_link
(
                            
src
mozpath
.
join
(
path
f
.
target_basename
)
                        
)
                    
if
isinstance
(
f
ObjDirPath
)
:
                        
dep_target
=
"
install
-
%
s
"
%
obj
.
install_target
                        
dep
=
mozpath
.
relpath
(
f
.
full_path
self
.
environment
.
topobjdir
)
                        
if
dep
in
self
.
_generated_files_map
:
                            
dep
=
self
.
_generated_files_map
[
dep
]
                        
self
.
_dependencies
[
dep_target
]
.
append
(
dep
)
        
elif
isinstance
(
obj
ChromeManifestEntry
)
and
obj
.
install_target
.
startswith
(
            
"
dist
/
bin
"
        
)
:
            
top_level
=
mozpath
.
join
(
obj
.
install_target
"
chrome
.
manifest
"
)
            
if
obj
.
path
!
=
top_level
:
                
entry
=
"
manifest
%
s
"
%
mozpath
.
relpath
(
obj
.
path
obj
.
install_target
)
                
self
.
_manifest_entries
[
top_level
]
.
add
(
entry
)
            
self
.
_manifest_entries
[
obj
.
path
]
.
add
(
str
(
obj
.
entry
)
)
        
elif
isinstance
(
obj
GeneratedFile
)
:
            
if
obj
.
outputs
:
                
first_output
=
mozpath
.
relpath
(
                    
mozpath
.
join
(
obj
.
objdir
obj
.
outputs
[
0
]
)
self
.
environment
.
topobjdir
                
)
                
for
o
in
obj
.
outputs
[
1
:
]
:
                    
fullpath
=
mozpath
.
join
(
obj
.
objdir
o
)
                    
self
.
_generated_files_map
[
                        
mozpath
.
relpath
(
fullpath
self
.
environment
.
topobjdir
)
                    
]
=
first_output
            
self
.
_generated_files
.
append
(
obj
)
            
return
False
        
elif
isinstance
(
obj
XPIDLModule
)
:
            
self
.
_has_xpidl
=
True
            
return
False
        
else
:
            
return
False
        
return
True
    
def
consume_finished
(
self
)
:
        
mk
=
Makefile
(
)
        
mk
.
create_rule
(
[
"
default
"
]
)
        
mk
.
add_statement
(
"
TOPSRCDIR
=
%
s
"
%
self
.
environment
.
topsrcdir
)
        
mk
.
add_statement
(
"
TOPOBJDIR
=
%
s
"
%
self
.
environment
.
topobjdir
)
        
mk
.
add_statement
(
"
MDDEPDIR
=
.
deps
"
)
        
mk
.
add_statement
(
"
TOUCH
?
=
touch
"
)
        
mk
.
add_statement
(
"
include
(
TOPSRCDIR
)
/
config
/
makefiles
/
functions
.
mk
"
)
        
mk
.
add_statement
(
"
include
(
TOPSRCDIR
)
/
config
/
AB_rCD
.
mk
"
)
        
mk
.
add_statement
(
"
AB_CD
=
en
-
US
"
)
        
if
not
self
.
_has_xpidl
:
            
mk
.
add_statement
(
"
NO_XPIDL
=
1
"
)
        
for
var
in
(
            
"
PYTHON3
"
            
"
ACDEFINES
"
            
"
MOZ_BUILD_APP
"
            
"
MOZ_WIDGET_TOOLKIT
"
        
)
:
            
value
=
self
.
environment
.
substs
.
get
(
var
)
            
if
value
is
not
None
:
                
mk
.
add_statement
(
"
%
s
=
%
s
"
%
(
var
value
)
)
        
install_manifests_bases
=
self
.
_install_manifests
.
keys
(
)
        
manifest_targets
=
[
]
        
for
target
entries
in
self
.
_manifest_entries
.
items
(
)
:
            
manifest_targets
.
append
(
target
)
            
install_target
=
mozpath
.
basedir
(
target
install_manifests_bases
)
            
self
.
_install_manifests
[
install_target
]
.
add_content
(
                
"
"
.
join
(
"
%
s
\
n
"
%
e
for
e
in
sorted
(
entries
)
)
                
mozpath
.
relpath
(
target
install_target
)
            
)
        
mk
.
add_statement
(
            
"
INSTALL_MANIFESTS
=
%
s
"
%
"
"
.
join
(
sorted
(
self
.
_install_manifests
.
keys
(
)
)
)
        
)
        
for
target
deps
in
sorted
(
self
.
_dependencies
.
items
(
)
)
:
            
mk
.
create_rule
(
[
target
]
)
.
add_dependencies
(
                
"
(
TOPOBJDIR
)
/
%
s
"
%
d
for
d
in
sorted
(
deps
)
            
)
        
python_deps
=
[
            
"
(
TOPSRCDIR
)
/
third_party
/
python
/
moz_l10n
/
moz
/
l10n
/
bin
/
build_file
.
py
"
        
]
        
for
target
deps
in
sorted
(
self
.
_l10n_dependencies
.
items
(
)
)
:
            
mk
.
create_rule
(
[
target
]
)
.
add_dependencies
(
                
"
%
s
"
%
d
[
0
]
for
d
in
sorted
(
deps
key
=
itemgetter
(
0
)
)
            
)
            
for
merge
ref_file
l10n_file
in
deps
:
                
rule
=
mk
.
create_rule
(
[
merge
]
)
.
add_dependencies
(
                    
[
ref_file
l10n_file
]
+
python_deps
                
)
                
rule
.
add_commands
(
[
                    
"
(
PYTHON3
)
-
m
moz
.
l10n
.
bin
.
build_file
"
                    
f
"
-
-
source
{
ref_file
}
-
-
l10n
{
l10n_file
}
-
-
target
{
merge
}
"
                
]
)
                
mk
.
create_rule
(
[
l10n_file
]
)
        
mk
.
add_statement
(
"
include
(
TOPSRCDIR
)
/
config
/
faster
/
rules
.
mk
"
)
        
for
base
install_manifest
in
self
.
_install_manifests
.
items
(
)
:
            
with
self
.
_write_file
(
                
mozpath
.
join
(
                    
self
.
environment
.
topobjdir
                    
"
faster
"
                    
"
install_
%
s
"
%
base
.
replace
(
"
/
"
"
_
"
)
                
)
            
)
as
fh
:
                
install_manifest
.
write
(
fileobj
=
fh
)
        
unified_manifest
=
InstallManifest
(
)
        
for
base
install_manifest
in
self
.
_install_manifests
.
items
(
)
:
            
assert
base
.
startswith
(
"
dist
/
bin
"
)
            
base
=
base
[
len
(
"
dist
/
bin
"
)
:
]
            
if
base
and
base
[
0
]
=
=
"
/
"
:
                
base
=
base
[
1
:
]
            
unified_manifest
.
add_entries_from
(
install_manifest
base
=
base
)
        
with
self
.
_write_file
(
            
mozpath
.
join
(
                
self
.
environment
.
topobjdir
"
faster
"
"
unified_install_dist_bin
"
            
)
        
)
as
fh
:
            
unified_manifest
.
write
(
fileobj
=
fh
)
        
for
obj
in
self
.
_generated_files
:
            
for
stmt
in
self
.
_format_statements_for_generated_file
(
obj
"
default
"
)
:
                
mk
.
add_statement
(
stmt
)
        
with
self
.
_write_file
(
            
mozpath
.
join
(
self
.
environment
.
topobjdir
"
faster
"
"
Makefile
"
)
        
)
as
fh
:
            
mk
.
dump
(
fh
removal_guard
=
False
)
    
def
_pretty_path
(
self
path
obj
)
:
        
if
path
.
startswith
(
self
.
environment
.
topobjdir
)
:
            
return
mozpath
.
join
(
                
"
(
TOPOBJDIR
)
"
mozpath
.
relpath
(
path
self
.
environment
.
topobjdir
)
            
)
        
elif
path
.
startswith
(
self
.
environment
.
topsrcdir
)
:
            
return
mozpath
.
join
(
                
"
(
TOPSRCDIR
)
"
mozpath
.
relpath
(
path
self
.
environment
.
topsrcdir
)
            
)
        
else
:
            
return
path
    
def
_format_generated_file_input_name
(
self
path
obj
)
:
        
return
self
.
_pretty_path
(
path
.
full_path
obj
)
    
def
_format_generated_file_output_name
(
self
path
obj
)
:
        
if
not
isinstance
(
path
Path
)
:
            
path
=
ObjDirPath
(
obj
.
_context
"
!
"
+
path
)
        
return
self
.
_pretty_path
(
path
.
full_path
obj
)
