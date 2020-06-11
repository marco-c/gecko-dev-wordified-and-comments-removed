from
__future__
import
absolute_import
print_function
unicode_literals
from
mozboot
.
base
import
BaseBootstrapper
from
mozboot
.
linux_common
import
LinuxBootstrapper
MERCURIAL_INSTALL_PROMPT
=
'
'
'
Mercurial
releases
a
new
version
every
3
months
and
your
distro
'
s
package
may
become
out
of
date
.
This
may
cause
incompatibility
with
some
Mercurial
extensions
that
rely
on
new
Mercurial
features
.
As
a
result
you
may
not
have
an
optimal
version
control
experience
.
To
have
the
best
Mercurial
experience
possible
we
recommend
installing
Mercurial
via
the
"
pip
"
Python
packaging
utility
.
This
will
likely
result
in
files
being
placed
in
/
usr
/
local
/
bin
and
/
usr
/
local
/
lib
.
How
would
you
like
to
continue
?
  
1
.
Install
a
modern
Mercurial
via
pip
(
recommended
)
  
2
.
Install
a
legacy
Mercurial
via
apt
  
3
.
Do
not
install
Mercurial
Your
choice
:
'
'
'
class
DebianBootstrapper
(
        
LinuxBootstrapper
        
BaseBootstrapper
)
:
    
COMMON_PACKAGES
=
[
        
'
autoconf2
.
13
'
        
'
build
-
essential
'
        
'
nodejs
'
        
'
python
-
setuptools
'
        
'
unzip
'
        
'
uuid
'
        
'
zip
'
    
]
    
DISTRO_PACKAGES
=
[
]
    
DEBIAN_PACKAGES
=
[
    
]
    
BROWSER_COMMON_PACKAGES
=
[
        
'
libasound2
-
dev
'
        
'
libcurl4
-
openssl
-
dev
'
        
'
libdbus
-
1
-
dev
'
        
'
libdbus
-
glib
-
1
-
dev
'
        
'
libgtk
-
3
-
dev
'
        
'
libgtk2
.
0
-
dev
'
        
'
libpulse
-
dev
'
        
'
libx11
-
xcb
-
dev
'
        
'
libxt
-
dev
'
        
'
xvfb
'
        
'
yasm
'
    
]
    
BROWSER_DISTRO_PACKAGES
=
[
]
    
MOBILE_ANDROID_COMMON_PACKAGES
=
[
        
'
openjdk
-
8
-
jdk
-
headless
'
        
'
wget
'
    
]
    
MOBILE_ANDROID_DISTRO_PACKAGES
=
[
]
    
def
__init__
(
self
distro
version
dist_id
codename
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
distro
=
distro
        
self
.
version
=
version
        
self
.
dist_id
=
dist_id
        
self
.
codename
=
codename
        
self
.
packages
=
self
.
COMMON_PACKAGES
+
self
.
DISTRO_PACKAGES
        
if
self
.
distro
=
=
'
debian
'
:
            
self
.
packages
+
=
self
.
DEBIAN_PACKAGES
        
if
self
.
distro
=
=
'
ubuntu
'
and
int
(
self
.
version
.
split
(
'
.
'
)
[
0
]
)
>
=
20
:
            
self
.
packages
.
extend
(
[
'
python2
.
7
'
'
python2
.
7
-
dev
'
]
)
        
else
:
            
if
(
self
.
distro
=
=
'
ubuntu
'
                
or
(
self
.
distro
=
=
'
debian
'
and
self
.
codename
not
in
(
'
bullseye
'
'
sid
'
)
)
)
:
                
self
.
packages
.
append
(
'
python
-
pip
'
)
            
self
.
packages
.
append
(
'
python
-
dev
'
)
        
self
.
browser_packages
=
self
.
BROWSER_COMMON_PACKAGES
+
self
.
BROWSER_DISTRO_PACKAGES
        
self
.
mobile_android_packages
=
self
.
MOBILE_ANDROID_COMMON_PACKAGES
+
\
            
self
.
MOBILE_ANDROID_DISTRO_PACKAGES
    
def
install_system_packages
(
self
)
:
        
packages
=
list
(
self
.
packages
)
        
have_python3
=
any
(
[
self
.
which
(
'
python3
'
)
self
.
which
(
'
python3
.
8
'
)
                            
self
.
which
(
'
python3
.
7
'
)
self
.
which
(
'
python3
.
6
'
)
                            
self
.
which
(
'
python3
.
5
'
)
]
)
        
python3_packages
=
self
.
check_output
(
            
[
'
apt
-
cache
'
'
pkgnames
'
'
python3
'
]
universal_newlines
=
True
)
        
python3_packages
=
python3_packages
.
splitlines
(
)
        
if
not
have_python3
and
'
python3
'
in
python3_packages
:
            
packages
.
extend
(
[
'
python3
'
'
python3
-
dev
'
]
)
        
if
not
self
.
which
(
'
pip3
'
)
and
'
python3
-
pip
'
in
python3_packages
:
            
packages
.
append
(
'
python3
-
pip
'
)
        
self
.
apt_install
(
*
packages
)
    
def
install_browser_packages
(
self
)
:
        
self
.
ensure_browser_packages
(
)
    
def
install_browser_artifact_mode_packages
(
self
)
:
        
self
.
ensure_browser_packages
(
artifact_mode
=
True
)
    
def
install_mobile_android_packages
(
self
)
:
        
self
.
ensure_mobile_android_packages
(
)
    
def
install_mobile_android_artifact_mode_packages
(
self
)
:
        
self
.
ensure_mobile_android_packages
(
artifact_mode
=
True
)
    
def
ensure_browser_packages
(
self
artifact_mode
=
False
)
:
        
self
.
apt_install
(
*
self
.
browser_packages
)
        
modern
=
self
.
is_nasm_modern
(
)
        
if
not
modern
:
            
self
.
apt_install
(
'
nasm
'
)
    
def
ensure_mobile_android_packages
(
self
artifact_mode
=
False
)
:
        
self
.
apt_install
(
*
self
.
mobile_android_packages
)
        
self
.
ensure_java
(
)
        
from
mozboot
import
android
        
android
.
ensure_android
(
'
linux
'
artifact_mode
=
artifact_mode
                               
no_interactive
=
self
.
no_interactive
)
    
def
generate_mobile_android_mozconfig
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
'
linux
'
artifact_mode
=
artifact_mode
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
generate_mobile_android_mozconfig
(
artifact_mode
=
True
)
    
def
_update_package_manager
(
self
)
:
        
self
.
apt_update
(
)
    
def
upgrade_mercurial
(
self
current
)
:
        
"
"
"
Install
Mercurial
from
pip
because
Debian
packages
typically
lag
.
"
"
"
        
if
self
.
no_interactive
:
            
self
.
apt_install
(
'
mercurial
'
)
            
return
        
res
=
self
.
prompt_int
(
MERCURIAL_INSTALL_PROMPT
1
3
)
        
if
res
=
=
2
:
            
self
.
apt_install
(
'
mercurial
'
)
            
return
False
        
if
res
=
=
3
:
            
print
(
'
Not
installing
Mercurial
.
'
)
            
return
False
        
assert
res
=
=
1
        
self
.
run_as_root
(
[
'
pip3
'
'
install
'
'
-
-
upgrade
'
'
Mercurial
'
]
)
