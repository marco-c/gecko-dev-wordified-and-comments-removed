config
=
{
    
"
products
"
:
{
        
"
installer
"
:
{
            
"
product
-
name
"
:
"
Firefox
-
%
(
version
)
s
"
            
"
platforms
"
:
[
                
"
linux64
"
                
"
linux64
-
aarch64
"
                
"
osx
"
                
"
win
"
                
"
win64
"
                
"
win64
-
aarch64
"
            
]
        
}
        
"
installer
-
latest
"
:
{
            
"
product
-
name
"
:
"
Firefox
-
latest
"
            
"
platforms
"
:
[
                
"
linux64
"
                
"
linux64
-
aarch64
"
                
"
osx
"
                
"
win
"
                
"
win64
"
                
"
win64
-
aarch64
"
            
]
        
}
        
"
installer
-
ssl
"
:
{
            
"
product
-
name
"
:
"
Firefox
-
%
(
version
)
s
-
SSL
"
            
"
platforms
"
:
[
                
"
linux64
"
                
"
linux64
-
aarch64
"
                
"
osx
"
                
"
win
"
                
"
win64
"
                
"
win64
-
aarch64
"
            
]
        
}
        
"
installer
-
latest
-
ssl
"
:
{
            
"
product
-
name
"
:
"
Firefox
-
latest
-
SSL
"
            
"
platforms
"
:
[
                
"
linux64
"
                
"
linux64
-
aarch64
"
                
"
osx
"
                
"
win
"
                
"
win64
"
                
"
win64
-
aarch64
"
            
]
        
}
        
"
msi
"
:
{
            
"
product
-
name
"
:
"
Firefox
-
%
(
version
)
s
-
msi
-
SSL
"
            
"
platforms
"
:
[
                
"
win
"
                
"
win64
"
            
]
        
}
        
"
msi
-
latest
"
:
{
            
"
product
-
name
"
:
"
Firefox
-
msi
-
latest
-
SSL
"
            
"
platforms
"
:
[
                
"
win
"
                
"
win64
"
            
]
        
}
        
"
msix
"
:
{
            
"
product
-
name
"
:
"
Firefox
-
%
(
version
)
s
-
msix
-
SSL
"
            
"
platforms
"
:
[
                
"
win
"
                
"
win64
"
                
"
win64
-
aarch64
"
            
]
        
}
        
"
msix
-
latest
"
:
{
            
"
product
-
name
"
:
"
Firefox
-
msix
-
latest
-
SSL
"
            
"
platforms
"
:
[
                
"
win
"
                
"
win64
"
                
"
win64
-
aarch64
"
            
]
        
}
        
"
langpack
"
:
{
            
"
product
-
name
"
:
"
Firefox
-
%
(
version
)
s
-
langpack
-
SSL
"
            
"
platforms
"
:
[
                
"
linux64
"
                
"
linux64
-
aarch64
"
                
"
osx
"
                
"
win
"
                
"
win64
"
            
]
        
}
        
"
langpack
-
latest
"
:
{
            
"
product
-
name
"
:
"
Firefox
-
langpack
-
latest
-
SSL
"
            
"
platforms
"
:
[
                
"
linux64
"
                
"
linux64
-
aarch64
"
                
"
osx
"
                
"
win
"
                
"
win64
"
            
]
        
}
        
"
stub
-
installer
"
:
{
            
"
product
-
name
"
:
"
Firefox
-
%
(
version
)
s
-
stub
"
            
"
platforms
"
:
[
                
"
win
"
                
"
win64
"
                
"
win64
-
aarch64
"
            
]
        
}
        
"
stub
-
installer
-
latest
"
:
{
            
"
product
-
name
"
:
"
Firefox
-
stub
"
            
"
platforms
"
:
[
                
"
win
"
                
"
win64
"
                
"
win64
-
aarch64
"
            
]
        
}
        
"
pkg
"
:
{
            
"
product
-
name
"
:
"
Firefox
-
%
(
version
)
s
-
pkg
-
SSL
"
            
"
platforms
"
:
[
"
osx
"
]
        
}
        
"
pkg
-
latest
"
:
{
            
"
product
-
name
"
:
"
Firefox
-
pkg
-
latest
-
SSL
"
            
"
platforms
"
:
[
"
osx
"
]
        
}
        
"
complete
-
mar
"
:
{
            
"
product
-
name
"
:
"
Firefox
-
%
(
version
)
s
-
Complete
"
            
"
platforms
"
:
[
                
"
linux64
"
                
"
linux64
-
aarch64
"
                
"
osx
"
                
"
win
"
                
"
win64
"
                
"
win64
-
aarch64
"
            
]
        
}
    
}
    
"
partials
"
:
{
        
"
releases
-
dir
"
:
{
            
"
product
-
name
"
:
"
Firefox
-
%
(
version
)
s
-
Partial
-
%
(
prev_version
)
s
"
            
"
platforms
"
:
[
                
"
linux64
"
                
"
linux64
-
aarch64
"
                
"
osx
"
                
"
win
"
                
"
win64
"
                
"
win64
-
aarch64
"
            
]
        
}
    
}
}
