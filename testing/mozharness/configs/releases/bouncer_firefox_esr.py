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
check_uptake
"
:
True
            
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
esr
-
latest
"
            
"
check_uptake
"
:
True
            
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
next
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
esr
-
next
-
latest
"
            
"
check_uptake
"
:
True
            
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
check_uptake
"
:
True
            
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
esr
-
latest
-
SSL
"
            
"
check_uptake
"
:
True
            
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
next
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
esr
-
next
-
latest
-
SSL
"
            
"
check_uptake
"
:
True
            
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
check_uptake
"
:
True
            
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
esr
-
msi
-
latest
-
SSL
"
            
"
check_uptake
"
:
True
            
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
next
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
esr
-
next
-
msi
-
latest
-
SSL
"
            
"
check_uptake
"
:
True
            
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
check_uptake
"
:
True
            
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
esr
-
msix
-
latest
-
SSL
"
            
"
check_uptake
"
:
True
            
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
next
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
esr
-
next
-
msix
-
latest
-
SSL
"
            
"
check_uptake
"
:
True
            
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
check_uptake
"
:
True
            
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
check_uptake
"
:
True
            
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
