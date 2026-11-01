import
locale
import
os
from
collections
import
defaultdict
from
contextlib
import
contextmanager
from
mozlint
import
result
from
mozlint
.
pathutils
import
get_ancestors_by_name
from
yamllint
import
linter
from
yamllint
.
cli
import
find_files_recursively
from
yamllint
.
config
import
YamlLintConfig
def
get_yamllint_version
(
)
:
    
from
yamllint
import
APP_VERSION
    
return
APP_VERSION
def
load_config
(
conf_file
)
:
    
if
conf_file
!
=
"
default
"
:
        
return
YamlLintConfig
(
file
=
conf_file
)
    
return
YamlLintConfig
(
"
extends
:
default
"
)
contextmanager
def
scoped_locale
(
name
)
:
    
if
name
is
None
:
        
yield
        
return
    
previous
=
locale
.
setlocale
(
locale
.
LC_ALL
)
    
locale
.
setlocale
(
locale
.
LC_ALL
name
)
    
try
:
        
yield
    
finally
:
        
locale
.
setlocale
(
locale
.
LC_ALL
previous
)
def
lint
(
files
config
*
*
lintargs
)
:
    
log
=
lintargs
[
"
log
"
]
    
root
=
lintargs
[
"
root
"
]
    
log
.
debug
(
f
"
Version
:
{
get_yamllint_version
(
)
}
"
)
    
paths_by_config
=
defaultdict
(
list
)
    
for
f
in
files
:
        
conf_files
=
get_ancestors_by_name
(
"
.
yamllint
"
f
root
)
        
paths_by_config
[
conf_files
[
0
]
if
conf_files
else
"
default
"
]
.
append
(
f
)
    
results
=
[
]
    
for
conf_file
paths
in
paths_by_config
.
items
(
)
:
        
conf
=
load_config
(
conf_file
)
        
with
scoped_locale
(
conf
.
locale
)
:
            
for
path
in
find_files_recursively
(
paths
conf
)
:
                
with
open
(
path
"
rb
"
)
as
fh
:
                    
problems
=
list
(
linter
.
run
(
fh
conf
path
.
removeprefix
(
"
.
/
"
)
)
)
                
for
problem
in
problems
:
                    
results
.
append
(
                        
result
.
from_config
(
                            
config
                            
path
=
os
.
path
.
relpath
(
path
root
)
                            
message
=
problem
.
desc
.
removesuffix
(
"
(
syntax
)
"
)
                            
level
=
"
error
"
                            
lineno
=
problem
.
line
                            
column
=
problem
.
column
                            
rule
=
problem
.
rule
or
"
syntax
"
                        
)
                    
)
    
return
results
