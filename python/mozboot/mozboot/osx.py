from
__future__
import
absolute_import
print_function
unicode_literals
import
platform
import
subprocess
import
sys
import
tempfile
try
:
    
from
urllib2
import
urlopen
except
ImportError
:
    
from
urllib
.
request
import
urlopen
from
packaging
.
version
import
Version
from
mozboot
.
base
import
BaseBootstrapper
from
mozfile
import
which
from
mach
.
util
import
to_optional_path
to_optional_str
HOMEBREW_BOOTSTRAP
=
(
    
"
https
:
/
/
raw
.
githubusercontent
.
com
/
Homebrew
/
install
/
master
/
install
.
sh
"
)
BREW_INSTALL
=
"
"
"
We
will
install
the
Homebrew
package
manager
to
install
required
packages
.
You
will
be
prompted
to
install
Homebrew
with
its
default
settings
.
If
you
would
prefer
to
do
this
manually
hit
CTRL
+
c
install
Homebrew
yourself
ensure
"
brew
"
is
in
your
PATH
and
relaunch
bootstrap
.
"
"
"
BREW_PACKAGES
=
"
"
"
We
are
now
installing
all
required
packages
via
Homebrew
.
You
will
see
a
lot
of
output
as
packages
are
built
.
"
"
"
NO_BREW_INSTALLED
=
"
It
seems
you
don
'
t
have
Homebrew
installed
.
"
class
OSXAndroidBootstrapper
(
object
)
:
    
def
install_mobile_android_packages
(
self
mozconfig_builder
artifact_mode
=
False
)
:
        
os_arch
=
platform
.
machine
(
)
        
if
os_arch
!
=
"
x86_64
"
and
os_arch
!
=
"
arm64
"
:
            
raise
Exception
(
                
"
You
need
a
64
-
bit
version
of
Mac
OS
X
to
build
"
                
"
GeckoView
/
Firefox
for
Android
.
"
            
)
        
from
mozboot
import
android
        
android
.
ensure_android
(
            
"
macosx
"
            
os_arch
            
artifact_mode
=
artifact_mode
            
no_interactive
=
self
.
no_interactive
        
)
        
if
os_arch
=
=
"
x86_64
"
or
os_arch
=
=
"
x86
"
:
            
android
.
ensure_android
(
                
"
macosx
"
                
os_arch
                
system_images_only
=
True
                
artifact_mode
=
artifact_mode
                
no_interactive
=
self
.
no_interactive
                
avd_manifest_path
=
android
.
AVD_MANIFEST_X86_64
            
)
            
android
.
ensure_android
(
                
"
macosx
"
                
os_arch
                
system_images_only
=
True
                
artifact_mode
=
artifact_mode
                
no_interactive
=
self
.
no_interactive
                
avd_manifest_path
=
android
.
AVD_MANIFEST_ARM
            
)
        
else
:
            
android
.
ensure_android
(
                
"
macosx
"
                
os_arch
                
system_images_only
=
True
                
artifact_mode
=
artifact_mode
                
no_interactive
=
self
.
no_interactive
                
avd_manifest_path
=
android
.
AVD_MANIFEST_ARM64
            
)
    
def
ensure_mobile_android_packages
(
self
)
:
        
from
mozboot
import
android
        
arch
=
platform
.
machine
(
)
        
android
.
ensure_java
(
"
macosx
"
arch
)
        
if
arch
=
=
"
x86_64
"
or
arch
=
=
"
x86
"
:
            
self
.
install_toolchain_artifact
(
android
.
MACOS_X86_64_ANDROID_AVD
)
            
self
.
install_toolchain_artifact
(
android
.
MACOS_ARM_ANDROID_AVD
)
        
elif
arch
=
=
"
arm64
"
:
            
self
.
install_toolchain_artifact
(
android
.
MACOS_ARM64_ANDROID_AVD
)
    
def
install_mobile_android_artifact_mode_packages
(
self
mozconfig_builder
)
:
        
self
.
install_mobile_android_packages
(
mozconfig_builder
artifact_mode
=
True
)
    
def
generate_mobile_android_mozconfig
(
self
)
:
        
return
self
.
_generate_mobile_android_mozconfig
(
)
    
def
generate_mobile_android_artifact_mode_mozconfig
(
self
)
:
        
return
self
.
_generate_mobile_android_mozconfig
(
artifact_mode
=
True
)
    
def
_generate_mobile_android_mozconfig
(
self
artifact_mode
=
False
)
:
        
from
mozboot
import
android
        
return
android
.
generate_mozconfig
(
"
macosx
"
artifact_mode
=
artifact_mode
)
def
ensure_command_line_tools
(
)
:
    
proc
=
subprocess
.
run
(
        
[
"
xcode
-
select
"
"
-
-
print
-
path
"
]
        
stdout
=
subprocess
.
PIPE
        
stderr
=
subprocess
.
DEVNULL
    
)
    
if
not
proc
.
stdout
:
        
subprocess
.
run
(
[
"
xcode
-
select
"
"
-
-
install
"
]
check
=
True
)
        
print
(
"
Please
follow
the
command
line
tools
installer
instructions
"
)
        
print
(
"
and
rerun
.
/
mach
bootstrap
when
it
'
s
finished
.
"
)
        
sys
.
exit
(
1
)
class
OSXBootstrapperLight
(
OSXAndroidBootstrapper
BaseBootstrapper
)
:
    
def
__init__
(
self
version
*
*
kwargs
)
:
        
BaseBootstrapper
.
__init__
(
self
*
*
kwargs
)
    
def
install_system_packages
(
self
)
:
        
ensure_command_line_tools
(
)
    
def
install_browser_packages
(
self
mozconfig_builder
)
:
        
pass
    
def
install_browser_artifact_mode_packages
(
self
mozconfig_builder
)
:
        
pass
    
def
ensure_node_packages
(
self
)
:
        
pass
    
def
ensure_stylo_packages
(
self
)
:
        
pass
    
def
ensure_clang_static_analysis_package
(
self
)
:
        
pass
    
def
ensure_nasm_packages
(
self
)
:
        
pass
    
def
ensure_minidump_stackwalk_packages
(
self
)
:
        
self
.
install_toolchain_artifact
(
"
minidump
-
stackwalk
"
)
class
OSXBootstrapper
(
OSXAndroidBootstrapper
BaseBootstrapper
)
:
    
def
__init__
(
self
version
*
*
kwargs
)
:
        
BaseBootstrapper
.
__init__
(
self
*
*
kwargs
)
        
self
.
os_version
=
Version
(
version
)
        
if
self
.
os_version
<
Version
(
"
10
.
6
"
)
:
            
raise
Exception
(
"
OS
X
10
.
6
or
above
is
required
.
"
)
        
self
.
minor_version
=
version
.
split
(
"
.
"
)
[
1
]
    
def
install_system_packages
(
self
)
:
        
ensure_command_line_tools
(
)
        
self
.
ensure_homebrew_installed
(
)
        
_
hg_modern
_
=
self
.
is_mercurial_modern
(
)
        
if
not
hg_modern
:
            
print
(
                
"
Mercurial
wasn
'
t
found
or
is
not
sufficiently
modern
.
"
                
"
It
will
be
installed
with
brew
"
            
)
        
packages
=
[
"
git
"
"
gnu
-
tar
"
"
terminal
-
notifier
"
"
watchman
"
]
        
if
not
hg_modern
:
            
packages
.
append
(
"
mercurial
"
)
        
self
.
_ensure_homebrew_packages
(
packages
)
    
def
install_browser_packages
(
self
mozconfig_builder
)
:
        
pass
    
def
install_browser_artifact_mode_packages
(
self
mozconfig_builder
)
:
        
pass
    
def
_ensure_homebrew_found
(
self
)
:
        
self
.
brew
=
to_optional_path
(
which
(
"
brew
"
)
)
        
return
self
.
brew
is
not
None
    
def
_ensure_homebrew_packages
(
self
packages
is_for_cask
=
False
)
:
        
package_type_flag
=
"
-
-
cask
"
if
is_for_cask
else
"
-
-
formula
"
        
self
.
ensure_homebrew_installed
(
)
        
def
create_homebrew_cmd
(
*
parameters
)
:
            
base_cmd
=
[
to_optional_str
(
self
.
brew
)
]
            
base_cmd
.
extend
(
parameters
)
            
return
base_cmd
+
[
package_type_flag
]
        
installed
=
set
(
            
subprocess
.
check_output
(
                
create_homebrew_cmd
(
"
list
"
)
universal_newlines
=
True
            
)
.
split
(
)
        
)
        
outdated
=
set
(
            
subprocess
.
check_output
(
                
create_homebrew_cmd
(
"
outdated
"
"
-
-
quiet
"
)
universal_newlines
=
True
            
)
.
split
(
)
        
)
        
to_install
=
set
(
package
for
package
in
packages
if
package
not
in
installed
)
        
to_upgrade
=
set
(
package
for
package
in
packages
if
package
in
outdated
)
        
if
to_install
or
to_upgrade
:
            
print
(
BREW_PACKAGES
)
        
if
to_install
:
            
subprocess
.
check_call
(
create_homebrew_cmd
(
"
install
"
)
+
list
(
to_install
)
)
        
if
to_upgrade
:
            
subprocess
.
check_call
(
create_homebrew_cmd
(
"
upgrade
"
)
+
list
(
to_upgrade
)
)
    
def
_ensure_homebrew_casks
(
self
casks
)
:
        
self
.
_ensure_homebrew_found
(
)
        
known_taps
=
subprocess
.
check_output
(
[
to_optional_str
(
self
.
brew
)
"
tap
"
]
)
        
if
b
"
homebrew
/
cask
-
versions
"
not
in
known_taps
:
            
subprocess
.
check_output
(
                
[
to_optional_str
(
self
.
brew
)
"
tap
"
"
homebrew
/
cask
-
versions
"
]
            
)
        
if
b
"
caskroom
/
versions
"
in
known_taps
:
            
subprocess
.
check_output
(
                
[
to_optional_str
(
self
.
brew
)
"
untap
"
"
caskroom
/
versions
"
]
            
)
        
self
.
_ensure_homebrew_packages
(
casks
is_for_cask
=
True
)
    
def
ensure_homebrew_browser_packages
(
self
)
:
        
packages
=
[
"
yasm
"
]
        
self
.
_ensure_homebrew_packages
(
packages
)
    
def
ensure_homebrew_installed
(
self
)
:
        
"
"
"
        
Search
for
Homebrew
in
sys
.
path
if
not
found
prompt
the
user
to
install
it
.
        
Then
assert
our
PATH
ordering
is
correct
.
        
"
"
"
        
homebrew_found
=
self
.
_ensure_homebrew_found
(
)
        
if
not
homebrew_found
:
            
self
.
install_homebrew
(
)
    
def
ensure_clang_static_analysis_package
(
self
)
:
        
from
mozboot
import
static_analysis
        
self
.
install_toolchain_static_analysis
(
static_analysis
.
MACOS_CLANG_TIDY
)
    
def
ensure_sccache_packages
(
self
)
:
        
from
mozboot
import
sccache
        
self
.
install_toolchain_artifact
(
"
sccache
"
)
        
self
.
install_toolchain_artifact
(
sccache
.
RUSTC_DIST_TOOLCHAIN
no_unpack
=
True
)
        
self
.
install_toolchain_artifact
(
sccache
.
CLANG_DIST_TOOLCHAIN
no_unpack
=
True
)
    
def
ensure_fix_stacks_packages
(
self
)
:
        
self
.
install_toolchain_artifact
(
"
fix
-
stacks
"
)
    
def
ensure_stylo_packages
(
self
)
:
        
self
.
install_toolchain_artifact
(
"
clang
"
)
        
self
.
install_toolchain_artifact
(
"
cbindgen
"
)
    
def
ensure_nasm_packages
(
self
)
:
        
self
.
install_toolchain_artifact
(
"
nasm
"
)
    
def
ensure_node_packages
(
self
)
:
        
self
.
install_toolchain_artifact
(
"
node
"
)
    
def
ensure_minidump_stackwalk_packages
(
self
)
:
        
self
.
install_toolchain_artifact
(
"
minidump
-
stackwalk
"
)
    
def
install_homebrew
(
self
)
:
        
print
(
BREW_INSTALL
)
        
bootstrap
=
urlopen
(
url
=
HOMEBREW_BOOTSTRAP
timeout
=
20
)
.
read
(
)
        
with
tempfile
.
NamedTemporaryFile
(
)
as
tf
:
            
tf
.
write
(
bootstrap
)
            
tf
.
flush
(
)
            
subprocess
.
check_call
(
[
"
bash
"
tf
.
name
]
)
        
homebrew_found
=
self
.
_ensure_homebrew_found
(
)
        
if
not
homebrew_found
:
            
print
(
                
"
Homebrew
was
just
installed
but
can
'
t
be
found
on
PATH
.
"
                
"
Please
file
a
bug
.
"
            
)
            
sys
.
exit
(
1
)
    
def
_update_package_manager
(
self
)
:
        
subprocess
.
check_call
(
[
to_optional_str
(
self
.
brew
)
"
-
v
"
"
update
"
]
)
    
def
_upgrade_package
(
self
package
)
:
        
self
.
_ensure_homebrew_installed
(
)
        
try
:
            
subprocess
.
check_output
(
                
[
to_optional_str
(
self
.
brew
)
"
-
v
"
"
upgrade
"
package
]
                
stderr
=
subprocess
.
STDOUT
            
)
        
except
subprocess
.
CalledProcessError
as
e
:
            
if
b
"
already
installed
"
not
in
e
.
output
:
                
raise
    
def
upgrade_mercurial
(
self
current
)
:
        
self
.
_upgrade_package
(
"
mercurial
"
)
