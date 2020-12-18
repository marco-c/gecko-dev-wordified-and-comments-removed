from
__future__
import
absolute_import
division
import
os
import
mozunit
import
pytest
from
mozprofile
.
prefs
import
Preferences
from
mozprofile
import
(
    
BaseProfile
    
Profile
    
ChromeProfile
    
ChromiumProfile
    
FirefoxProfile
    
ThunderbirdProfile
    
create_profile
)
here
=
os
.
path
.
abspath
(
os
.
path
.
dirname
(
__file__
)
)
def
test_with_profile_should_cleanup
(
)
:
    
with
Profile
(
)
as
profile
:
        
assert
os
.
path
.
exists
(
profile
.
profile
)
    
assert
not
os
.
path
.
exists
(
profile
.
profile
)
def
test_with_profile_should_cleanup_even_on_exception
(
)
:
    
with
pytest
.
raises
(
ZeroDivisionError
)
:
        
with
Profile
(
)
as
profile
:
            
assert
os
.
path
.
exists
(
profile
.
profile
)
            
1
/
0
    
assert
not
os
.
path
.
exists
(
profile
.
profile
)
pytest
.
mark
.
parametrize
(
    
"
app
cls
"
    
[
        
(
"
chrome
"
ChromeProfile
)
        
(
"
chromium
"
ChromiumProfile
)
        
(
"
firefox
"
FirefoxProfile
)
        
(
"
thunderbird
"
ThunderbirdProfile
)
        
(
"
unknown
"
None
)
    
]
)
def
test_create_profile
(
tmpdir
app
cls
)
:
    
path
=
tmpdir
.
strpath
    
if
cls
is
None
:
        
with
pytest
.
raises
(
NotImplementedError
)
:
            
create_profile
(
app
)
        
return
    
profile
=
create_profile
(
app
profile
=
path
)
    
assert
isinstance
(
profile
BaseProfile
)
    
assert
profile
.
__class__
=
=
cls
    
assert
profile
.
profile
=
=
path
pytest
.
mark
.
parametrize
(
    
"
cls
"
    
[
        
Profile
        
ChromeProfile
        
ChromiumProfile
    
]
)
def
test_merge_profile
(
cls
)
:
    
profile
=
cls
(
preferences
=
{
"
foo
"
:
"
bar
"
}
)
    
assert
profile
.
_addons
=
=
[
]
    
assert
os
.
path
.
isfile
(
        
os
.
path
.
join
(
profile
.
profile
profile
.
preference_file_names
[
0
]
)
    
)
    
other_profile
=
os
.
path
.
join
(
here
"
files
"
"
dummy
-
profile
"
)
    
profile
.
merge
(
other_profile
)
    
prefs
=
{
}
    
for
name
in
profile
.
preference_file_names
:
        
path
=
os
.
path
.
join
(
profile
.
profile
name
)
        
assert
os
.
path
.
isfile
(
path
)
        
try
:
            
prefs
.
update
(
Preferences
.
read_json
(
path
)
)
        
except
ValueError
:
            
prefs
.
update
(
Preferences
.
read_prefs
(
path
)
)
    
assert
"
foo
"
in
prefs
    
assert
len
(
prefs
)
=
=
len
(
profile
.
preference_file_names
)
+
1
    
assert
all
(
name
in
prefs
for
name
in
profile
.
preference_file_names
)
    
if
cls
=
=
Profile
:
        
assert
len
(
profile
.
_addons
)
=
=
1
        
assert
profile
.
_addons
[
0
]
.
endswith
(
"
empty
.
xpi
"
)
        
assert
os
.
path
.
exists
(
profile
.
_addons
[
0
]
)
    
else
:
        
assert
len
(
profile
.
_addons
)
=
=
0
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
