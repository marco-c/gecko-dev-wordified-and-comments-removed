import
os
config
=
{
    
"
virtualenv_modules
"
:
[
        
"
dbus
-
python
=
=
1
.
3
.
2
"
        
"
python
-
dbusmock
=
=
0
.
32
.
2
"
    
]
    
"
find_links
"
:
[
        
os
.
path
.
abspath
(
os
.
environ
.
get
(
"
MOZ_FETCHES_DIR
"
)
)
    
]
}
