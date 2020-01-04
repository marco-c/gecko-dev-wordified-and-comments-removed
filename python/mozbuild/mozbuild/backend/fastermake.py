from
__future__
import
absolute_import
unicode_literals
print_function
from
mozbuild
.
backend
.
common
import
CommonBackend
from
mozbuild
.
frontend
.
data
import
(
    
ContextDerived
    
Defines
    
DistFiles
    
FinalTargetFiles
    
JARManifest
    
JavaScriptModules
    
JsPreferenceFile
    
Resources
    
VariablePassthru
)
from
mozbuild
.
jar
import
JarManifestParser
from
mozbuild
.
makeutil
import
Makefile
from
mozbuild
.
preprocessor
import
Preprocessor
from
mozbuild
.
util
import
OrderedDefaultDict
from
mozpack
.
manifests
import
InstallManifest
import
mozpack
.
path
as
mozpath
from
collections
import
OrderedDict
from
itertools
import
chain
import
os
import
sys
class
OverwriteInstallManifest
(
InstallManifest
)
:
    
def
_add_entry
(
self
dest
entry
)
:
        
if
dest
in
self
.
_dests
:
            
print
(
'
Warning
:
Item
already
in
manifest
:
%
s
'
%
dest
                  
file
=
sys
.
stderr
)
        
self
.
_dests
[
dest
]
=
entry
class
FasterMakeBackend
(
CommonBackend
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
FasterMakeBackend
self
)
.
_init
(
)
        
self
.
_seen_directories
=
set
(
)
        
self
.
_defines
=
dict
(
)
        
self
.
_manifest_entries
=
OrderedDefaultDict
(
list
)
        
self
.
_install_manifests
=
OrderedDefaultDict
(
OverwriteInstallManifest
)
        
self
.
_dependencies
=
OrderedDefaultDict
(
list
)
    
def
_add_preprocess
(
self
obj
path
dest
target
=
None
*
*
kwargs
)
:
        
if
target
is
None
:
            
target
=
mozpath
.
basename
(
path
)
            
if
target
.
endswith
(
'
.
in
'
)
:
                
target
=
target
[
:
-
3
]
        
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
'
faster
'
'
.
deps
'
            
mozpath
.
join
(
obj
.
install_target
dest
target
)
.
replace
(
'
/
'
'
_
'
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
path
)
            
mozpath
.
join
(
dest
target
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
not
isinstance
(
obj
Defines
)
and
isinstance
(
obj
ContextDerived
)
:
            
defines
=
self
.
_defines
.
get
(
obj
.
objdir
{
}
)
            
if
defines
:
                
defines
=
defines
.
defines
        
if
isinstance
(
obj
Defines
)
:
            
self
.
_defines
[
obj
.
objdir
]
=
obj
            
assert
obj
.
objdir
not
in
self
.
_seen_directories
        
elif
isinstance
(
obj
JARManifest
)
and
\
                
obj
.
install_target
.
startswith
(
'
dist
/
bin
'
)
:
            
self
.
_consume_jar_manifest
(
obj
defines
)
        
elif
isinstance
(
obj
VariablePassthru
)
and
\
                
obj
.
install_target
.
startswith
(
'
dist
/
bin
'
)
:
            
for
f
in
obj
.
variables
.
get
(
'
EXTRA_COMPONENTS
'
{
}
)
:
                
path
=
mozpath
.
join
(
obj
.
install_target
'
components
'
                                    
mozpath
.
basename
(
f
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
add_symlink
(
                    
mozpath
.
join
(
obj
.
srcdir
f
)
                    
mozpath
.
join
(
'
components
'
mozpath
.
basename
(
f
)
)
                
)
                
if
f
.
endswith
(
'
.
manifest
'
)
:
                    
manifest
=
mozpath
.
join
(
obj
.
install_target
                                            
'
chrome
.
manifest
'
)
                    
self
.
_manifest_entries
[
manifest
]
.
append
(
                        
'
manifest
components
/
%
s
'
%
mozpath
.
basename
(
f
)
)
            
for
f
in
obj
.
variables
.
get
(
'
EXTRA_PP_COMPONENTS
'
{
}
)
:
                
self
.
_add_preprocess
(
obj
f
'
components
'
defines
=
defines
)
                
if
f
.
endswith
(
'
.
manifest
'
)
:
                    
manifest
=
mozpath
.
join
(
obj
.
install_target
                                            
'
chrome
.
manifest
'
)
                    
self
.
_manifest_entries
[
manifest
]
.
append
(
                        
'
manifest
components
/
%
s
'
%
mozpath
.
basename
(
f
)
)
        
elif
isinstance
(
obj
JavaScriptModules
)
and
\
                
obj
.
install_target
.
startswith
(
'
dist
/
bin
'
)
:
            
for
path
strings
in
obj
.
modules
.
walk
(
)
:
                
base
=
mozpath
.
join
(
'
modules
'
path
)
                
for
f
in
strings
:
                    
if
obj
.
flavor
=
=
'
extra
'
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
add_symlink
(
                            
mozpath
.
join
(
obj
.
srcdir
f
)
                            
mozpath
.
join
(
base
mozpath
.
basename
(
f
)
)
                        
)
                    
elif
obj
.
flavor
=
=
'
extra_pp
'
:
                        
self
.
_add_preprocess
(
obj
f
base
defines
=
defines
)
        
elif
isinstance
(
obj
JsPreferenceFile
)
and
\
                
obj
.
install_target
.
startswith
(
'
dist
/
bin
'
)
:
            
if
obj
.
install_target
=
=
'
dist
/
bin
'
:
                
pref_dir
=
'
defaults
/
pref
'
            
else
:
                
pref_dir
=
'
defaults
/
preferences
'
            
dest
=
mozpath
.
join
(
obj
.
install_target
pref_dir
                                
mozpath
.
basename
(
obj
.
path
)
)
            
self
.
_add_preprocess
(
obj
obj
.
path
pref_dir
defines
=
defines
                                 
silence_missing_directive_warnings
=
True
)
        
elif
isinstance
(
obj
Resources
)
and
\
                
obj
.
install_target
.
startswith
(
'
dist
/
bin
'
)
:
            
for
path
strings
in
obj
.
resources
.
walk
(
)
:
                
base
=
mozpath
.
join
(
'
res
'
path
)
                
for
f
in
strings
:
                    
flags
=
strings
.
flags_for
(
f
)
                    
if
flags
and
flags
.
preprocess
:
                        
self
.
_add_preprocess
(
obj
f
base
marker
=
'
%
'
                                             
defines
=
obj
.
defines
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
add_symlink
(
                            
mozpath
.
join
(
obj
.
srcdir
f
)
                            
mozpath
.
join
(
base
mozpath
.
basename
(
f
)
)
                        
)
        
elif
isinstance
(
obj
FinalTargetFiles
)
and
\
                
obj
.
install_target
.
startswith
(
'
dist
/
bin
'
)
:
            
for
path
strings
in
obj
.
files
.
walk
(
)
:
                
base
=
mozpath
.
join
(
obj
.
install_target
path
)
                
for
f
in
strings
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
add_symlink
(
                        
mozpath
.
join
(
obj
.
srcdir
f
)
                        
mozpath
.
join
(
path
mozpath
.
basename
(
f
)
)
                    
)
        
elif
isinstance
(
obj
DistFiles
)
and
\
                
obj
.
install_target
.
startswith
(
'
dist
/
bin
'
)
:
            
for
f
in
obj
.
files
:
                
self
.
_add_preprocess
(
obj
f
'
'
defines
=
defines
                                     
silence_missing_directive_warnings
=
True
)
        
else
:
            
return
True
        
self
.
_seen_directories
.
add
(
obj
.
objdir
)
        
return
True
    
def
_consume_jar_manifest
(
self
obj
defines
)
:
        
pp
=
Preprocessor
(
)
        
pp
.
context
.
update
(
defines
)
        
pp
.
context
.
update
(
self
.
environment
.
defines
)
        
pp
.
context
.
update
(
            
AB_CD
=
'
en
-
US
'
            
BUILD_FASTER
=
1
        
)
        
pp
.
out
=
JarManifestParser
(
)
        
pp
.
do_include
(
obj
.
path
)
        
self
.
backend_input_files
|
=
pp
.
includes
        
for
jarinfo
in
pp
.
out
:
            
install_target
=
obj
.
install_target
            
if
jarinfo
.
base
:
                
install_target
=
mozpath
.
join
(
install_target
jarinfo
.
base
)
            
for
e
in
jarinfo
.
entries
:
                
if
e
.
is_locale
:
                    
if
jarinfo
.
relativesrcdir
:
                        
path
=
mozpath
.
join
(
self
.
environment
.
topsrcdir
                                            
jarinfo
.
relativesrcdir
)
                    
else
:
                        
path
=
mozpath
.
dirname
(
obj
.
path
)
                    
src
=
mozpath
.
join
(
path
'
en
-
US
'
e
.
source
)
                
elif
e
.
source
.
startswith
(
'
/
'
)
:
                    
src
=
mozpath
.
join
(
self
.
environment
.
topsrcdir
                                       
e
.
source
[
1
:
]
)
                
else
:
                    
src
=
mozpath
.
join
(
mozpath
.
dirname
(
obj
.
path
)
e
.
source
)
                
if
'
*
'
in
e
.
source
:
                    
if
e
.
preprocess
:
                        
raise
Exception
(
'
%
s
:
Wildcards
are
not
supported
with
'
                                        
'
preprocessing
'
%
obj
.
path
)
                    
def
_prefix
(
s
)
:
                        
for
p
in
s
.
split
(
'
/
'
)
:
                            
if
'
*
'
not
in
p
:
                                
yield
p
+
'
/
'
                    
prefix
=
'
'
.
join
(
_prefix
(
src
)
)
                    
self
.
_install_manifests
[
install_target
]
\
                        
.
add_pattern_symlink
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
                        
mozpath
.
join
(
jarinfo
.
name
e
.
output
)
)
                    
continue
                
if
not
os
.
path
.
exists
(
src
)
:
                    
if
e
.
is_locale
:
                        
raise
Exception
(
                            
'
%
s
:
Cannot
find
%
s
'
%
(
obj
.
path
e
.
source
)
)
                    
if
e
.
source
.
startswith
(
'
/
'
)
:
                        
src
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
                                           
e
.
source
[
1
:
]
)
                    
else
:
                        
src
=
mozpath
.
join
(
obj
.
objdir
e
.
source
)
                    
self
.
_dependencies
[
'
install
-
%
s
'
%
install_target
]
\
                        
.
append
(
mozpath
.
relpath
(
                        
src
self
.
environment
.
topobjdir
)
)
                
if
e
.
preprocess
:
                    
kwargs
=
{
}
                    
if
src
.
endswith
(
'
.
css
'
)
:
                        
kwargs
[
'
marker
'
]
=
'
%
'
                    
self
.
_add_preprocess
(
                        
obj
                        
src
                        
mozpath
.
join
(
jarinfo
.
name
mozpath
.
dirname
(
e
.
output
)
)
                        
mozpath
.
basename
(
e
.
output
)
                        
defines
=
defines
                        
*
*
kwargs
)
                
else
:
                    
self
.
_install_manifests
[
install_target
]
.
add_symlink
(
                        
src
                        
mozpath
.
join
(
jarinfo
.
name
e
.
output
)
)
            
manifest
=
mozpath
.
normpath
(
mozpath
.
join
(
install_target
                                                     
jarinfo
.
name
)
)
            
manifest
+
=
'
.
manifest
'
            
for
m
in
jarinfo
.
chrome_manifests
:
                
self
.
_manifest_entries
[
manifest
]
.
append
(
                    
m
.
replace
(
'
%
'
mozpath
.
basename
(
jarinfo
.
name
)
+
'
/
'
)
)
            
if
jarinfo
.
name
!
=
'
chrome
'
:
                
manifest
=
mozpath
.
normpath
(
mozpath
.
join
(
install_target
                                                         
'
chrome
.
manifest
'
)
)
                
entry
=
'
manifest
%
s
.
manifest
'
%
jarinfo
.
name
                
if
entry
not
in
self
.
_manifest_entries
[
manifest
]
:
                    
self
.
_manifest_entries
[
manifest
]
.
append
(
entry
)
    
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
'
default
'
]
)
        
mk
.
add_statement
(
'
TOPSRCDIR
=
%
s
'
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
'
TOPOBJDIR
=
%
s
'
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
'
BACKEND
=
%
s
'
%
self
.
_backend_output_list_file
)
        
for
var
in
(
            
'
PYTHON
'
            
'
ACDEFINES
'
            
'
MOZ_BUILD_APP
'
            
'
MOZ_WIDGET_TOOLKIT
'
        
)
:
            
mk
.
add_statement
(
'
%
s
=
%
s
'
%
(
var
self
.
environment
.
substs
[
var
]
)
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
iteritems
(
)
:
            
manifest_targets
.
append
(
target
)
            
target
=
'
(
TOPOBJDIR
)
/
%
s
'
%
target
            
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
                
[
'
content
=
%
s
'
%
'
'
.
join
(
'
"
%
s
"
'
%
e
for
e
in
entries
)
]
)
        
mk
.
add_statement
(
'
MANIFEST_TARGETS
=
%
s
'
%
'
'
.
join
(
manifest_targets
)
)
        
mk
.
add_statement
(
'
INSTALL_MANIFESTS
=
%
s
'
                         
%
'
'
.
join
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
        
for
target
deps
in
self
.
_dependencies
.
iteritems
(
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
                
'
(
TOPOBJDIR
)
/
%
s
'
%
d
for
d
in
deps
)
        
mk
.
create_rule
(
[
self
.
_backend_output_list_file
]
)
.
add_dependencies
(
            
self
.
backend_input_files
)
        
mk
.
add_statement
(
'
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
'
)
        
for
base
install_manifest
in
self
.
_install_manifests
.
iteritems
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
'
faster
'
                                 
'
install_
%
s
'
%
base
.
replace
(
'
/
'
'
_
'
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
'
faster
'
                             
'
Makefile
'
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
