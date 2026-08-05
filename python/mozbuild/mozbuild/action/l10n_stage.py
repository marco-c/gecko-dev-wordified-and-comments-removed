"
"
"
Per
-
locale
stage
action
.
Reads
<
topobjdir
>
/
l10n
-
manifest
.
json
plus
the
populated
merge
tree
at
<
merge
-
tree
>
/
to
materialize
<
topobjdir
>
/
dist
/
xpi
-
stage
/
locale
-
<
ab_cd
>
/
.
Invoked
in
make
via
(
call
py_action
l10n_stage
.
.
.
)
.
"
"
"
import
argparse
import
fnmatch
import
shutil
import
sys
from
glob
import
glob
from
pathlib
import
Path
from
typing
import
Iterator
Optional
import
mozpack
.
path
as
mozpath
from
mozbuild
.
frontend
.
l10n_manifest
import
(
    
L10nManifest
    
L10nManifestContextData
    
LocalizedFileGroup
    
load_l10n_manifest
)
from
mozbuild
.
preprocessor
import
Preprocessor
def
stage_locale
(
    
locale
:
str
    
manifest_path
:
Path
    
merge_tree
:
Path
    
dest_xpi_stage
:
Path
    
*
    
topsrcdir
:
Optional
[
Path
]
=
None
    
topobjdir
:
Optional
[
Path
]
=
None
    
mode
:
str
=
"
langpack
"
)
-
>
None
:
    
dest
=
dest_xpi_stage
    
manifest
=
load_l10n_manifest
(
manifest_path
)
    
state
=
StageState
(
        
locale
=
locale
        
manifest
=
manifest
        
merge_tree
=
merge_tree
        
dest
=
dest
        
topsrcdir
=
topsrcdir
        
topobjdir
=
topobjdir
        
mode
=
mode
    
)
    
if
mode
=
=
"
langpack
"
and
dest
.
exists
(
)
:
        
shutil
.
rmtree
(
dest
)
    
dest
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
    
for
context
in
manifest
.
contexts
:
        
_stage_context
(
state
context
)
class
StageState
:
    
def
__init__
(
        
self
        
*
        
locale
:
str
        
manifest
:
L10nManifest
        
merge_tree
:
Path
        
dest
:
Path
        
topsrcdir
:
Optional
[
Path
]
        
topobjdir
:
Optional
[
Path
]
        
mode
:
str
    
)
-
>
None
:
        
self
.
locale
=
locale
        
self
.
manifest
=
manifest
        
self
.
merge_tree
=
merge_tree
        
self
.
dest
=
dest
        
self
.
topsrcdir
=
topsrcdir
        
self
.
topobjdir
=
topobjdir
        
self
.
mode
=
mode
def
_stage_context
(
state
:
StageState
context
:
L10nManifestContextData
)
-
>
None
:
    
"
"
"
Stage
one
L10nManifestContextData
into
state
.
dest
.
    
LOCALIZED_FILES
and
LOCALIZED_PP_FILES
are
langpack
-
only
.
Chrome
    
mode
skips
them
so
multi
-
locale
builds
only
stage
chrome
content
.
    
"
"
"
    
if
state
.
mode
=
=
"
langpack
"
:
        
for
group
in
context
.
localized_files
:
            
_stage_file_group
(
state
context
group
preprocess
=
False
)
        
for
group
in
context
.
localized_pp_files
:
            
_stage_file_group
(
state
context
group
preprocess
=
True
)
def
_stage_file_group
(
    
state
:
StageState
    
context
:
L10nManifestContextData
    
group
:
LocalizedFileGroup
    
preprocess
:
bool
)
-
>
None
:
    
"
"
"
Stage
one
LOCALIZED_FILES
or
LOCALIZED_PP_FILES
group
.
    
Sources
may
be
en
-
US
/
.
.
.
(
resolves
via
the
merge
tree
)
    
/
path
/
locales
/
en
-
US
/
.
.
.
(
topsrcdir
-
rooted
merge
tree
)
or
a
glob
    
pattern
.
preprocess
=
True
runs
each
entry
through
the
preprocessor
    
with
LOCALE_PP_DEFINES
resolved
for
the
current
locale
.
    
"
"
"
    
install_target
=
mozpath
.
normpath
(
        
mozpath
.
join
(
context
.
install_subdir
group
.
subpath
)
    
)
    
if
install_target
=
=
"
.
"
:
        
install_target
=
"
"
    
defines
=
_resolve_locale_defines
(
state
context
)
if
preprocess
else
None
    
for
src_template
in
group
.
sources
:
        
for
src
dest_rel
in
_resolve_localized_sources
(
            
state
context
src_template
install_target
        
)
:
            
dest_path
=
mozpath
.
join
(
state
.
dest
dest_rel
)
            
_stage_entry
(
src
dest_path
preprocess
defines
)
def
_resolve_localized_sources
(
    
state
:
StageState
    
context
:
L10nManifestContextData
    
src_template
:
str
    
install_target
:
str
)
-
>
Iterator
[
tuple
[
str
str
]
]
:
    
"
"
"
Yield
(
src_abs
dest_rel
)
pairs
for
one
source
template
.
    
en
-
US
/
and
/
locales
/
en
-
US
/
markers
resolve
against
the
merge
tree
.
    
Bare
patterns
resolve
against
the
merge
tree
'
s
directory
for
the
    
context
(
mirroring
EXPAND_LOCALE_SRCDIR
)
.
Glob
patterns
expand
    
against
whichever
resolved
location
.
    
"
"
"
    
if
src_template
.
startswith
(
"
en
-
US
/
"
)
:
        
rest
=
src_template
[
len
(
"
en
-
US
/
"
)
:
]
        
src_abs
=
mozpath
.
join
(
_locale_source_root
(
state
context
.
relsrcdir
)
rest
)
    
elif
"
/
locales
/
en
-
US
/
"
in
src_template
:
        
if
src_template
.
startswith
(
"
/
"
)
:
            
rel
=
src_template
.
lstrip
(
"
/
"
)
        
else
:
            
rel
=
mozpath
.
join
(
context
.
relsrcdir
src_template
)
        
if
state
.
locale
=
=
"
en
-
US
"
:
            
src_abs
=
mozpath
.
join
(
state
.
topsrcdir
or
"
"
rel
)
        
else
:
            
before
rest
=
rel
.
split
(
"
/
locales
/
en
-
US
/
"
1
)
            
src_abs
=
mozpath
.
join
(
state
.
merge_tree
before
rest
)
    
else
:
        
src_abs
=
mozpath
.
join
(
            
_locale_source_root
(
state
context
.
relsrcdir
)
src_template
        
)
    
if
_has_wildcard
(
src_abs
)
:
        
for
match
in
sorted
(
glob
(
src_abs
)
)
:
            
if
Path
(
match
)
.
is_file
(
)
:
                
dest_rel
=
mozpath
.
join
(
install_target
mozpath
.
basename
(
match
)
)
                
yield
match
dest_rel
        
return
    
if
Path
(
src_abs
)
.
exists
(
)
:
        
dest_basename
=
mozpath
.
basename
(
src_template
)
        
dest_rel
=
mozpath
.
join
(
install_target
dest_basename
)
        
yield
src_abs
dest_rel
def
_merge_subdir_for
(
relsrcdir
:
str
)
-
>
str
:
    
"
"
"
Mirror
EXPAND_LOCALE_SRCDIR
.
Strips
a
trailing
/
locales
so
the
    
merge
subdir
matches
the
L10NBASEDIR
layout
.
    
"
"
"
    
if
relsrcdir
.
endswith
(
"
/
locales
"
)
:
        
return
relsrcdir
[
:
-
len
(
"
/
locales
"
)
]
    
if
relsrcdir
=
=
"
locales
"
:
        
return
"
"
    
return
relsrcdir
def
_locale_source_root
(
state
:
StageState
relsrcdir
:
str
)
-
>
str
:
    
"
"
"
Root
directory
that
locale
-
marked
sources
resolve
under
for
    
state
.
locale
.
en
-
US
reads
directly
from
the
source
tree
(
the
merge
    
step
is
skipped
for
en
-
US
so
the
merge
tree
is
empty
)
.
Other
    
locales
read
from
the
merge
tree
populated
by
the
merge
step
from
    
the
l10n
source
repo
.
    
"
"
"
    
if
state
.
locale
=
=
"
en
-
US
"
:
        
return
mozpath
.
join
(
state
.
topsrcdir
or
"
"
relsrcdir
"
en
-
US
"
)
    
return
mozpath
.
join
(
state
.
merge_tree
_merge_subdir_for
(
relsrcdir
)
)
def
_resolve_locale_defines
(
    
state
:
StageState
context
:
L10nManifestContextData
)
-
>
dict
[
str
object
]
:
    
"
"
"
Compose
the
preprocessor
define
dict
for
context
and
the
current
    
locale
:
DEFINES
+
LOCALE_PP_DEFINES
-
resolved
+
AB_CD
.
    
"
"
"
    
out
=
dict
(
context
.
defines
or
{
}
)
    
out
.
update
(
_locale_resolved_defines
(
context
.
locale_pp_defines
or
{
}
state
.
locale
)
)
    
out
[
"
AB_CD
"
]
=
state
.
locale
    
return
out
def
_stage_entry
(
    
src
:
str
dest
:
str
preprocess
:
bool
defines
:
Optional
[
dict
[
str
object
]
]
)
-
>
None
:
    
Path
(
dest
)
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
    
if
preprocess
:
        
_preprocess_to
(
src
dest
defines
)
    
else
:
        
_copy_to
(
src
dest
)
def
_preprocess_to
(
src
:
str
dest
:
str
defines
:
dict
[
str
object
]
)
-
>
None
:
    
pp
=
Preprocessor
(
defines
=
defines
)
    
pp
.
do_filter
(
"
substitution
"
)
    
with
open
(
dest
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
out
:
        
pp
.
out
=
out
        
pp
.
do_include
(
src
)
def
_copy_to
(
src
:
str
dest
:
str
)
-
>
None
:
    
shutil
.
copyfile
(
src
dest
)
def
_has_wildcard
(
path
:
str
)
-
>
bool
:
    
return
any
(
c
in
path
for
c
in
"
*
?
[
"
)
def
_resolve_locale_pp_define
(
table
:
dict
[
str
str
]
locale
:
str
)
-
>
Optional
[
str
]
:
    
"
"
"
Resolve
a
single
LOCALE_PP_DEFINES
inner
dict
for
locale
.
    
Exact
ab_cd
keys
take
precedence
over
fnmatch
-
style
patterns
.
    
Returns
the
resolved
value
or
None
if
neither
matches
.
    
"
"
"
    
if
locale
in
table
:
        
return
table
[
locale
]
    
for
pattern
value
in
table
.
items
(
)
:
        
if
_has_wildcard
(
pattern
)
:
            
if
fnmatch
.
fnmatchcase
(
locale
pattern
)
:
                
return
value
    
return
None
def
_locale_resolved_defines
(
    
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
    
locale
:
str
)
-
>
dict
[
str
str
]
:
    
"
"
"
Resolve
every
LOCALE_PP_DEFINES
entry
for
locale
dropping
    
defines
whose
inner
table
has
no
match
.
    
"
"
"
    
out
=
{
}
    
for
name
table
in
locale_pp_defines
.
items
(
)
:
        
value
=
_resolve_locale_pp_define
(
table
locale
)
        
if
value
is
not
None
:
            
out
[
name
]
=
value
    
return
out
def
main
(
argv
:
list
[
str
]
)
-
>
int
:
    
parser
=
argparse
.
ArgumentParser
(
        
description
=
(
            
"
Stage
a
locale
into
dist
/
xpi
-
stage
/
locale
-
<
ab_cd
>
/
from
"
            
"
l10n
-
manifest
.
json
plus
a
populated
merge
tree
.
"
        
)
    
)
    
parser
.
add_argument
(
"
-
-
locale
"
required
=
True
help
=
"
The
ab_cd
locale
code
"
)
    
parser
.
add_argument
(
"
-
-
manifest
"
required
=
True
help
=
"
Path
to
l10n
-
manifest
.
json
"
)
    
parser
.
add_argument
(
        
"
-
-
merge
-
tree
"
        
required
=
True
        
help
=
"
Populated
merge
tree
(
e
.
g
.
<
topobjdir
>
/
<
reldir
>
/
merge
-
dir
/
<
ab_cd
>
/
)
"
    
)
    
parser
.
add_argument
(
"
-
-
dest
"
required
=
True
help
=
"
Destination
xpi
-
stage
directory
"
)
    
parser
.
add_argument
(
"
-
-
topsrcdir
"
default
=
None
)
    
parser
.
add_argument
(
"
-
-
topobjdir
"
default
=
None
)
    
parser
.
add_argument
(
        
"
-
-
mode
"
        
choices
=
(
"
langpack
"
"
chrome
"
)
        
default
=
"
langpack
"
        
help
=
"
Staging
mode
.
langpack
(
default
)
wipes
dest
and
processes
"
        
"
all
subsystems
.
chrome
leaves
dest
intact
and
only
stages
"
        
"
jar
.
mn
locale
entries
(
used
by
mach
package
-
multi
-
locale
to
"
        
"
accumulate
per
-
locale
chrome
into
the
same
dist
tree
)
.
"
    
)
    
args
=
parser
.
parse_args
(
argv
)
    
stage_locale
(
        
locale
=
args
.
locale
        
manifest_path
=
Path
(
args
.
manifest
)
        
merge_tree
=
Path
(
args
.
merge_tree
)
        
dest_xpi_stage
=
Path
(
args
.
dest
)
        
topsrcdir
=
Path
(
args
.
topsrcdir
)
if
args
.
topsrcdir
else
None
        
topobjdir
=
Path
(
args
.
topobjdir
)
if
args
.
topobjdir
else
None
        
mode
=
args
.
mode
    
)
    
return
0
if
__name__
=
=
"
__main__
"
:
    
sys
.
exit
(
main
(
sys
.
argv
[
1
:
]
)
)
