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
pathlib
import
Path
from
typing
import
Optional
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
    
load_l10n_manifest
)
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
"
"
"
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
