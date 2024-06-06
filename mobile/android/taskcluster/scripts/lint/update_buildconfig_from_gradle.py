import
argparse
import
logging
import
os
import
subprocess
import
sys
from
collections
import
defaultdict
import
yaml
from
mergedeep
import
merge
logger
=
logging
.
getLogger
(
__name__
)
CONFIGURATIONS_WITH_DEPENDENCIES
=
(
    
"
api
"
    
"
compileOnly
"
    
"
implementation
"
    
"
testImplementation
"
)
def
_get_upstream_deps_per_gradle_project
(
gradle_root
existing_build_config
)
:
    
project_dependencies
=
defaultdict
(
set
)
    
gradle_projects
=
_get_gradle_projects
(
gradle_root
existing_build_config
)
    
for
configuration
in
CONFIGURATIONS_WITH_DEPENDENCIES
:
        
logger
.
info
(
            
f
"
Looking
for
dependencies
in
{
configuration
}
configuration
"
            
f
"
in
{
gradle_root
}
"
        
)
        
cmd
=
[
"
.
/
gradlew
"
"
-
-
console
=
plain
"
"
-
-
parallel
"
]
        
for
gradle_project
in
sorted
(
gradle_projects
)
:
            
cmd
.
extend
(
                
[
f
"
{
gradle_project
}
:
dependencies
"
"
-
-
configuration
"
configuration
]
            
)
        
current_project_name
=
None
        
for
line
in
subprocess
.
check_output
(
            
cmd
universal_newlines
=
True
cwd
=
gradle_root
        
)
.
splitlines
(
)
:
            
if
line
.
startswith
(
"
Project
"
)
:
                
current_project_name
=
line
.
split
(
"
:
"
)
[
1
]
.
strip
(
"
'
"
)
            
if
line
.
startswith
(
"
+
-
-
-
project
"
)
or
line
.
startswith
(
r
"
\
-
-
-
project
"
)
:
                
project_dependencies
[
current_project_name
]
.
add
(
line
.
split
(
"
"
)
[
2
]
)
    
return
{
        
project_name
:
sorted
(
project_dependencies
[
project_name
]
)
        
for
project_name
in
gradle_projects
    
}
def
_get_gradle_projects
(
gradle_root
existing_build_config
)
:
    
if
gradle_root
.
endswith
(
"
android
-
components
"
)
:
        
return
list
(
existing_build_config
[
"
projects
"
]
.
keys
(
)
)
    
elif
gradle_root
.
endswith
(
"
focus
-
android
"
)
:
        
return
[
"
app
"
]
    
raise
NotImplementedError
(
f
"
Cannot
find
gradle
projects
for
{
gradle_root
}
"
)
def
is_dir
(
string
)
:
    
if
os
.
path
.
isdir
(
string
)
:
        
return
string
    
else
:
        
raise
argparse
.
ArgumentTypeError
(
f
'
"
{
string
}
"
is
not
a
directory
'
)
def
_parse_args
(
cmdln_args
)
:
    
parser
=
argparse
.
ArgumentParser
(
        
description
=
"
Calls
gradle
and
generate
json
file
with
dependencies
"
    
)
    
parser
.
add_argument
(
        
"
gradle_root
"
        
metavar
=
"
GRADLE_ROOT
"
        
type
=
is_dir
        
help
=
"
The
directory
where
to
call
gradle
from
"
    
)
    
return
parser
.
parse_args
(
args
=
cmdln_args
)
def
_set_logging_config
(
)
:
    
logging
.
basicConfig
(
        
level
=
logging
.
DEBUG
format
=
"
%
(
asctime
)
s
-
%
(
levelname
)
s
-
%
(
message
)
s
"
    
)
def
_merge_build_config
(
existing_build_config
upstream_deps_per_project
)
:
    
updated_build_config
=
{
        
"
projects
"
:
{
            
project
:
{
"
upstream_dependencies
"
:
deps
}
            
for
project
deps
in
upstream_deps_per_project
.
items
(
)
        
}
    
}
    
return
merge
(
existing_build_config
updated_build_config
)
def
main
(
)
:
    
args
=
_parse_args
(
sys
.
argv
[
1
:
]
)
    
gradle_root
=
args
.
gradle_root
    
build_config_file
=
os
.
path
.
join
(
gradle_root
"
.
buildconfig
.
yml
"
)
    
_set_logging_config
(
)
    
with
open
(
build_config_file
)
as
f
:
        
existing_build_config
=
yaml
.
safe_load
(
f
)
    
upstream_deps_per_project
=
_get_upstream_deps_per_gradle_project
(
        
gradle_root
existing_build_config
    
)
    
merged_build_config
=
_merge_build_config
(
        
existing_build_config
upstream_deps_per_project
    
)
    
with
open
(
build_config_file
"
w
"
)
as
f
:
        
yaml
.
safe_dump
(
merged_build_config
f
)
    
logger
.
info
(
f
"
Updated
{
build_config_file
}
with
latest
gradle
config
!
"
)
__name__
=
=
"
__main__
"
and
main
(
)
