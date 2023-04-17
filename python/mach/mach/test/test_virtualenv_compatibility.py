import
os
import
shutil
import
subprocess
import
sys
from
pathlib
import
Path
import
mozunit
from
buildconfig
import
topsrcdir
from
mach
.
requirements
import
MachEnvRequirements
def
_resolve_command_virtualenv_names
(
)
:
    
virtualenv_names
=
[
]
    
for
child
in
(
Path
(
topsrcdir
)
/
"
build
"
)
.
iterdir
(
)
:
        
if
not
child
.
name
.
endswith
(
"
_virtualenv_packages
.
txt
"
)
:
            
continue
        
if
child
.
name
=
=
"
mach_virtualenv_packages
.
txt
"
:
            
continue
        
virtualenv_names
.
append
(
child
.
name
[
:
-
len
(
"
_virtualenv_packages
.
txt
"
)
]
)
    
return
virtualenv_names
def
_requirement_definition_to_pip_format
(
virtualenv_name
cache
is_mach_or_build_env
)
:
    
"
"
"
Convert
from
parsed
requirements
object
to
pip
-
consumable
format
"
"
"
    
path
=
Path
(
topsrcdir
)
/
"
build
"
/
f
"
{
virtualenv_name
}
_virtualenv_packages
.
txt
"
    
requirements
=
MachEnvRequirements
.
from_requirements_definition
(
        
topsrcdir
False
is_mach_or_build_env
path
    
)
    
lines
=
[
]
    
for
pypi
in
(
        
requirements
.
pypi_requirements
+
requirements
.
pypi_optional_requirements
    
)
:
        
lines
.
append
(
str
(
pypi
.
requirement
)
)
    
for
vendored
in
requirements
.
vendored_requirements
:
        
lines
.
append
(
cache
.
package_for_vendor_dir
(
Path
(
vendored
.
path
)
)
)
    
return
"
\
n
"
.
join
(
lines
)
class
PackageCache
:
    
def
__init__
(
self
storage_dir
:
Path
)
:
        
self
.
_cache
=
{
}
        
self
.
_storage_dir
=
storage_dir
    
def
package_for_vendor_dir
(
self
vendor_path
:
Path
)
:
        
if
vendor_path
in
self
.
_cache
:
            
return
self
.
_cache
[
vendor_path
]
        
if
not
any
(
(
p
for
p
in
vendor_path
.
iterdir
(
)
if
p
.
name
.
endswith
(
"
.
dist
-
info
"
)
)
)
:
            
package_dir
=
vendor_path
            
while
True
:
                
if
(
package_dir
/
"
setup
.
py
"
)
.
exists
(
)
:
                    
break
                
elif
package_dir
.
parent
=
=
package_dir
:
                    
raise
Exception
(
                        
f
'
Package
"
{
vendor_path
}
"
is
not
a
wheel
and
does
not
have
a
'
                        
'
setup
.
py
file
.
Perhaps
it
should
be
"
pth
:
"
instead
of
'
                        
'
"
vendored
:
"
?
'
                    
)
                
package_dir
=
package_dir
.
parent
            
self
.
_cache
[
vendor_path
]
=
str
(
package_dir
)
            
return
str
(
package_dir
)
        
output_path
=
str
(
self
.
_storage_dir
/
f
"
{
vendor_path
.
name
}
-
0
-
py3
-
none
-
any
"
)
        
shutil
.
make_archive
(
output_path
"
zip
"
vendor_path
)
        
whl_path
=
output_path
+
"
.
whl
"
        
os
.
rename
(
output_path
+
"
.
zip
"
whl_path
)
        
self
.
_cache
[
vendor_path
]
=
whl_path
        
return
whl_path
def
test_virtualenvs_compatible
(
tmpdir
)
:
    
command_virtualenv_names
=
_resolve_command_virtualenv_names
(
)
    
work_dir
=
Path
(
tmpdir
)
    
cache
=
PackageCache
(
work_dir
)
    
mach_requirements
=
_requirement_definition_to_pip_format
(
"
mach
"
cache
True
)
    
subprocess
.
check_call
(
        
[
            
sys
.
executable
            
os
.
path
.
join
(
                
topsrcdir
                
"
third_party
"
                
"
python
"
                
"
virtualenv
"
                
"
virtualenv
.
py
"
            
)
            
"
-
-
no
-
download
"
            
str
(
work_dir
/
"
env
"
)
        
]
    
)
    
for
name
in
command_virtualenv_names
:
        
print
(
f
'
Checking
compatibility
of
"
{
name
}
"
virtualenv
'
)
        
command_requirements
=
_requirement_definition_to_pip_format
(
            
name
cache
name
=
=
"
build
"
        
)
        
with
open
(
work_dir
/
"
requirements
.
txt
"
"
w
"
)
as
requirements_txt
:
            
requirements_txt
.
write
(
mach_requirements
)
            
requirements_txt
.
write
(
"
\
n
"
)
            
requirements_txt
.
write
(
command_requirements
)
        
subprocess
.
check_call
(
            
[
                
str
(
work_dir
/
"
env
"
/
"
bin
"
/
"
pip
"
)
                
"
install
"
                
"
-
r
"
                
str
(
work_dir
/
"
requirements
.
txt
"
)
            
]
            
cwd
=
topsrcdir
        
)
if
__name__
=
=
"
__main__
"
:
    
mozunit
.
main
(
)
