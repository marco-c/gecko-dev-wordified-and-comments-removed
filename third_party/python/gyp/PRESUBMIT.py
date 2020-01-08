"
"
"
Top
-
level
presubmit
script
for
GYP
.
See
http
:
/
/
dev
.
chromium
.
org
/
developers
/
how
-
tos
/
depottools
/
presubmit
-
scripts
for
more
details
about
the
presubmit
API
built
into
gcl
.
"
"
"
PYLINT_BLACKLIST
=
[
    
'
test
/
lib
/
TestCmd
.
py
'
    
'
test
/
lib
/
TestCommon
.
py
'
    
'
test
/
lib
/
TestGyp
.
py
'
]
PYLINT_DISABLED_WARNINGS
=
[
    
'
W0611
'
    
'
W0632
'
    
'
W0633
'
    
'
F0401
'
    
'
W0622
'
    
'
W0612
'
    
'
C0323
'
    
'
C0322
'
    
'
W0301
'
    
'
W0613
'
    
'
W0105
'
    
'
W0110
'
    
'
W0123
'
    
'
C0324
'
    
'
W0212
'
    
'
W0311
'
    
'
C0301
'
    
'
E0602
'
    
'
W0702
'
    
'
E1101
'
    
'
W0102
'
    
'
R0401
'
    
'
W0201
'
'
W0232
'
'
E1103
'
'
W0621
'
'
W0108
'
'
W0223
'
'
W0231
'
    
'
R0201
'
'
E0101
'
'
C0321
'
    
'
W0104
'
]
def
_LicenseHeader
(
input_api
)
:
  
current_year
=
int
(
input_api
.
time
.
strftime
(
'
%
Y
'
)
)
  
allowed_years
=
(
str
(
s
)
for
s
in
reversed
(
xrange
(
2009
current_year
+
1
)
)
)
  
years_re
=
'
(
'
+
'
|
'
.
join
(
allowed_years
)
+
'
)
'
  
return
(
      
r
'
.
*
?
Copyright
(
\
(
c
\
)
)
?
%
(
year
)
s
Google
Inc
\
.
All
rights
reserved
\
.
\
n
'
      
r
'
.
*
?
Use
of
this
source
code
is
governed
by
a
BSD
-
style
license
that
'
        
r
'
can
be
\
n
'
      
r
'
.
*
?
found
in
the
LICENSE
file
\
.
\
n
'
  
)
%
{
      
'
year
'
:
years_re
  
}
def
CheckChangeOnUpload
(
input_api
output_api
)
:
  
report
=
[
]
  
report
.
extend
(
input_api
.
canned_checks
.
PanProjectChecks
(
      
input_api
output_api
license_header
=
_LicenseHeader
(
input_api
)
)
)
  
return
report
def
CheckChangeOnCommit
(
input_api
output_api
)
:
  
report
=
[
]
  
report
.
extend
(
input_api
.
canned_checks
.
PanProjectChecks
(
      
input_api
output_api
license_header
=
_LicenseHeader
(
input_api
)
)
)
  
report
.
extend
(
input_api
.
canned_checks
.
CheckTreeIsOpen
(
      
input_api
output_api
      
'
http
:
/
/
gyp
-
status
.
appspot
.
com
/
status
'
      
'
http
:
/
/
gyp
-
status
.
appspot
.
com
/
current
'
)
)
  
import
os
  
import
sys
  
old_sys_path
=
sys
.
path
  
try
:
    
sys
.
path
=
[
'
pylib
'
'
test
/
lib
'
]
+
sys
.
path
    
blacklist
=
PYLINT_BLACKLIST
    
if
sys
.
platform
=
=
'
win32
'
:
      
blacklist
=
[
os
.
path
.
normpath
(
x
)
.
replace
(
'
\
\
'
'
\
\
\
\
'
)
                   
for
x
in
PYLINT_BLACKLIST
]
    
report
.
extend
(
input_api
.
canned_checks
.
RunPylint
(
        
input_api
        
output_api
        
black_list
=
blacklist
        
disabled_warnings
=
PYLINT_DISABLED_WARNINGS
)
)
  
finally
:
    
sys
.
path
=
old_sys_path
  
return
report
