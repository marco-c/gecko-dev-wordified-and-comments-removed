config
=
{
    
"
stage_platform
"
:
"
android
-
geckoview
-
docs
"
    
"
src_mozconfig
"
:
"
mobile
/
android
/
config
/
mozconfigs
/
android
-
arm
/
nightly
-
android
-
lints
"
    
"
disable_package_metrics
"
:
True
    
"
postflight_build_mach_commands
"
:
[
        
[
            
"
android
"
            
"
geckoview
-
docs
"
            
"
-
-
archive
"
            
"
-
-
upload
"
            
"
mozilla
/
geckoview
"
            
"
-
-
upload
-
branch
"
            
"
gh
-
pages
"
            
"
-
-
javadoc
-
path
"
            
"
javadoc
/
{
project
}
"
            
"
-
-
upload
-
message
"
            
"
Update
{
project
}
documentation
to
rev
{
revision
}
"
        
]
    
]
}
