config
=
{
    
'
stage_platform
'
:
'
android
-
geckoview
-
docs
'
    
'
src_mozconfig
'
:
'
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
api
-
16
-
frontend
/
nightly
'
    
'
multi_locale_config_platform
'
:
'
android
'
    
'
disable_package_metrics
'
:
True
    
'
postflight_build_mach_commands
'
:
[
        
[
'
android
'
         
'
geckoview
-
docs
'
         
'
-
-
archive
'
         
'
-
-
upload
'
'
mozilla
/
geckoview
'
         
'
-
-
upload
-
branch
'
'
gh
-
pages
/
javadoc
/
{
project
}
'
         
'
-
-
upload
-
message
'
'
Update
{
project
}
javadoc
to
rev
{
revision
}
'
         
'
-
-
variant
'
'
withGeckoBinariesRelease
'
        
]
    
]
    
'
artifact_flag_build_variant_in_try
'
:
None
    
'
max_build_output_timeout
'
:
0
}
