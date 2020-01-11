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
Devedition
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
devedition
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
Devedition
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
devedition
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
Devedition
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
devedition
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
Devedition
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
devedition
-
stub
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
Devedition
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
Devedition
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
