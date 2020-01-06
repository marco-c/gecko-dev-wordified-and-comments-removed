"
"
"
Transform
the
signing
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
__future__
import
absolute_import
print_function
unicode_literals
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
treeherder
import
join_symbol
transforms
=
TransformSequence
(
)
transforms
.
add
def
make_signing_description
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
        
job
[
'
depname
'
]
=
'
unsigned
-
repack
'
        
dep_job
=
job
[
'
dependent
-
task
'
]
        
dep_platform
=
dep_job
.
attributes
.
get
(
'
build_platform
'
)
        
job
[
'
upstream
-
artifacts
'
]
=
[
]
        
if
'
android
'
in
dep_platform
:
            
job_specs
=
[
                
{
                    
'
artifacts
'
:
[
'
public
/
build
/
{
locale
}
/
target
.
apk
'
]
                    
'
format
'
:
'
jar
'
                
}
            
]
        
elif
'
macosx
'
in
dep_platform
:
            
job_specs
=
[
                
{
                    
'
artifacts
'
:
[
'
public
/
build
/
{
locale
}
/
target
.
dmg
'
]
                    
'
format
'
:
'
macapp
'
                
}
            
]
        
elif
'
win32
'
in
dep_platform
:
            
job_specs
=
[
                
{
                    
'
artifacts
'
:
[
                        
'
public
/
build
/
{
locale
}
/
target
.
zip
'
                        
'
public
/
build
/
{
locale
}
/
setup
.
exe
'
                        
'
public
/
build
/
{
locale
}
/
setup
-
stub
.
exe
'
                    
]
                    
'
format
'
:
'
sha2signcode
'
                
}
            
]
        
elif
'
win64
'
in
dep_platform
:
            
job_specs
=
[
                
{
                    
'
artifacts
'
:
[
                        
'
public
/
build
/
{
locale
}
/
target
.
zip
'
                        
'
public
/
build
/
{
locale
}
/
setup
.
exe
'
                    
]
                    
'
format
'
:
'
sha2signcode
'
                
}
            
]
        
elif
'
linux
'
in
dep_platform
:
            
job_specs
=
[
                
{
                    
'
artifacts
'
:
[
'
public
/
build
/
{
locale
}
/
target
.
tar
.
bz2
'
]
                    
'
format
'
:
'
gpg
'
                
}
{
                    
'
artifacts
'
:
[
'
public
/
build
/
{
locale
}
/
target
.
complete
.
mar
'
]
                    
'
format
'
:
'
mar
'
                
}
            
]
        
else
:
            
raise
Exception
(
"
Platform
not
implemented
for
signing
"
)
        
upstream_artifacts
=
[
]
        
for
spec
in
job_specs
:
            
fmt
=
spec
[
'
format
'
]
            
upstream_artifacts
.
append
(
{
                
"
taskId
"
:
{
"
task
-
reference
"
:
"
<
unsigned
-
repack
>
"
}
                
"
taskType
"
:
"
l10n
"
                
"
paths
"
:
[
f
.
format
(
locale
=
l
)
                          
for
l
in
dep_job
.
attributes
.
get
(
'
chunk_locales
'
[
]
)
                          
for
f
in
spec
[
'
artifacts
'
]
]
                
"
formats
"
:
[
fmt
]
            
}
)
        
job
[
'
upstream
-
artifacts
'
]
=
upstream_artifacts
        
label
=
dep_job
.
label
.
replace
(
"
nightly
-
l10n
-
"
"
signing
-
l10n
-
"
)
        
job
[
'
label
'
]
=
label
        
symbol
=
'
Ns
{
}
'
.
format
(
dep_job
.
attributes
.
get
(
'
l10n_chunk
'
)
)
        
group
=
'
tc
-
L10n
'
        
job
[
'
treeherder
'
]
=
{
            
'
symbol
'
:
join_symbol
(
group
symbol
)
        
}
        
yield
job
