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
linux
"
                
"
linux64
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
linux
"
                
"
linux64
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
linux
"
                
"
linux64
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
linux
"
                
"
linux64
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
linux
"
                
"
linux64
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
linux
"
                
"
linux64
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
