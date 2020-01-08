config
=
{
    
"
mozilla
-
central
"
:
{
        
"
repo_path
"
:
'
mozilla
-
central
'
        
"
update_channel
"
:
"
nightly
"
    
}
    
'
mozilla
-
release
'
:
{
        
'
enable_release_promotion
'
:
True
        
'
repo_path
'
:
'
releases
/
mozilla
-
release
'
        
'
update_channel
'
:
'
release
'
        
'
branch_uses_per_checkin_strategy
'
:
True
        
'
platform_overrides
'
:
{
            
'
linux
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
            
}
            
'
linux64
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
            
}
            
'
macosx64
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
            
}
            
'
win32
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
            
}
            
'
win64
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
            
}
        
}
    
}
    
'
mozilla
-
esr60
'
:
{
        
'
enable_release_promotion
'
:
True
        
'
repo_path
'
:
'
releases
/
mozilla
-
esr60
'
        
'
update_channel
'
:
'
esr
'
        
'
branch_uses_per_checkin_strategy
'
:
True
        
'
platform_overrides
'
:
{
            
'
linux
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
            
}
            
'
linux64
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
            
}
            
'
macosx64
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
            
}
            
'
win32
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
            
}
            
'
win64
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
            
}
        
}
    
}
    
'
mozilla
-
beta
'
:
{
        
'
enable_release_promotion
'
:
1
        
'
repo_path
'
:
'
releases
/
mozilla
-
beta
'
        
'
update_channel
'
:
'
beta
'
        
'
branch_uses_per_checkin_strategy
'
:
True
        
'
platform_overrides
'
:
{
            
'
linux
'
:
{
                
'
mozconfig_variant
'
:
'
beta
'
            
}
            
'
linux64
'
:
{
                
'
mozconfig_variant
'
:
'
beta
'
            
}
            
'
macosx64
'
:
{
                
'
mozconfig_variant
'
:
'
beta
'
            
}
            
'
win32
'
:
{
                
'
mozconfig_variant
'
:
'
beta
'
            
}
            
'
win64
'
:
{
                
'
mozconfig_variant
'
:
'
beta
'
            
}
            
'
linux
-
devedition
'
:
{
                
"
update_channel
"
:
"
aurora
"
            
}
            
'
linux64
-
devedition
'
:
{
                
"
update_channel
"
:
"
aurora
"
            
}
            
'
macosx64
-
devedition
'
:
{
                
"
update_channel
"
:
"
aurora
"
            
}
            
'
win32
-
devedition
'
:
{
                
"
update_channel
"
:
"
aurora
"
            
}
            
'
win64
-
devedition
'
:
{
                
"
update_channel
"
:
"
aurora
"
            
}
        
}
    
}
    
'
mozilla
-
aurora
'
:
{
        
'
repo_path
'
:
'
releases
/
mozilla
-
aurora
'
        
'
update_channel
'
:
'
aurora
'
        
'
branch_uses_per_checkin_strategy
'
:
True
    
}
    
'
try
'
:
{
        
'
repo_path
'
:
'
try
'
        
'
branch_supports_uploadsymbols
'
:
False
    
}
    
'
gum
'
:
{
        
'
branch_uses_per_checkin_strategy
'
:
True
    
}
    
'
mozilla
-
inbound
'
:
{
        
'
repo_path
'
:
'
integration
/
mozilla
-
inbound
'
    
}
    
'
autoland
'
:
{
        
'
repo_path
'
:
'
integration
/
autoland
'
    
}
    
'
ux
'
:
{
}
    
'
cypress
'
:
{
        
'
branch_uses_per_checkin_strategy
'
:
True
    
}
    
'
alder
'
:
{
}
    
'
ash
'
:
{
}
    
'
birch
'
:
{
}
    
'
cedar
'
:
{
}
    
'
elm
'
:
{
}
    
'
fig
'
:
{
}
    
'
graphics
'
:
{
}
    
'
jamun
'
:
{
        
'
update_channel
'
:
'
beta
'
        
'
enable_release_promotion
'
:
1
        
'
platform_overrides
'
:
{
            
'
linux
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
            
}
            
'
linux64
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
            
}
            
'
macosx64
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
            
}
            
'
win32
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
            
}
            
'
win64
'
:
{
                
'
mozconfig_variant
'
:
'
release
'
            
}
            
'
linux
-
devedition
'
:
{
                
"
update_channel
"
:
"
aurora
"
            
}
            
'
linux64
-
devedition
'
:
{
                
"
update_channel
"
:
"
aurora
"
            
}
            
'
macosx64
-
devedition
'
:
{
                
"
update_channel
"
:
"
aurora
"
            
}
            
'
win32
-
devedition
'
:
{
                
"
update_channel
"
:
"
aurora
"
            
}
            
'
win64
-
devedition
'
:
{
                
"
update_channel
"
:
"
aurora
"
            
}
        
}
    
}
    
'
larch
'
:
{
}
    
'
oak
'
:
{
}
    
'
pine
'
:
{
}
}
