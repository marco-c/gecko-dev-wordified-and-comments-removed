from
__future__
import
absolute_import
def
test
(
mod
path
entity
=
None
)
:
    
if
mod
not
in
(
        
"
netwerk
"
        
"
dom
"
        
"
toolkit
"
        
"
security
/
manager
"
        
"
devtools
/
client
"
        
"
devtools
/
shared
"
        
"
devtools
/
startup
"
        
"
browser
"
        
"
browser
/
extensions
/
formautofill
"
        
"
browser
/
extensions
/
report
-
site
-
issue
"
        
"
extensions
/
spellcheck
"
        
"
other
-
licenses
/
branding
/
firefox
"
        
"
browser
/
branding
/
official
"
        
"
services
/
sync
"
    
)
:
        
return
"
ignore
"
    
if
mod
not
in
(
"
browser
"
"
extensions
/
spellcheck
"
)
:
        
return
"
error
"
    
if
entity
is
None
:
        
if
mod
=
=
"
extensions
/
spellcheck
"
:
            
return
"
ignore
"
        
return
"
error
"
    
if
mod
=
=
"
extensions
/
spellcheck
"
:
        
return
"
error
"
    
if
path
=
=
"
defines
.
inc
"
:
        
return
"
ignore
"
if
entity
=
=
"
MOZ_LANGPACK_CONTRIBUTORS
"
else
"
error
"
    
return
"
error
"
