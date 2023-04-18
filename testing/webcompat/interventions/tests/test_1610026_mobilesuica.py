import
pytest
from
helpers
import
Css
Text
find_element
def
load_site
(
session
)
:
    
session
.
get
(
"
https
:
/
/
www
.
mobilesuica
.
com
/
"
)
    
address
=
find_element
(
session
Css
(
"
input
[
name
=
MailAddress
]
"
)
default
=
None
)
    
password
=
find_element
(
session
Css
(
"
input
[
name
=
Password
]
"
)
default
=
None
)
    
error
=
find_element
(
session
Css
(
"
input
[
name
=
winclosebutton
]
"
)
default
=
None
)
    
site_is_down
=
None
is
not
find_element
(
        
session
Text
(
"
"
)
default
=
None
    
)
    
if
site_is_down
:
        
pytest
.
xfail
(
"
Site
is
currently
down
"
)
    
return
address
password
error
site_is_down
pytest
.
mark
.
with_interventions
def
test_enabled
(
session
)
:
    
address
password
error
site_is_down
=
load_site
(
session
)
    
if
site_is_down
:
        
return
    
assert
address
.
is_displayed
(
)
    
assert
password
.
is_displayed
(
)
    
assert
error
is
None
pytest
.
mark
.
without_interventions
def
test_disabled
(
session
)
:
    
address
password
error
site_is_down
=
load_site
(
session
)
    
if
site_is_down
:
        
return
    
assert
address
is
None
    
assert
password
is
None
    
assert
error
.
is_displayed
(
)
