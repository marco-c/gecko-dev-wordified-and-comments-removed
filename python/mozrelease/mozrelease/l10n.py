def
getPlatformLocales
(
shipped_locales
platform
)
:
    
platform_locales
=
[
]
    
for
line
in
shipped_locales
.
splitlines
(
)
:
        
locale
=
line
.
strip
(
)
.
split
(
)
[
0
]
        
if
locale
=
=
"
ja
-
JP
-
mac
"
and
not
platform
.
startswith
(
"
mac
"
)
:
            
continue
        
if
locale
=
=
"
ja
"
and
platform
.
startswith
(
"
mac
"
)
:
            
continue
        
platform_locales
.
append
(
locale
)
    
return
platform_locales
