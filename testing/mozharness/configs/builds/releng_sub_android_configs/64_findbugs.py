config
=
{
    
'
base_name
'
:
'
Android
findbugs
%
(
branch
)
s
'
    
'
stage_platform
'
:
'
android
-
findbugs
'
    
'
build_type
'
:
'
api
-
15
-
opt
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
15
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
gradle
'
         
'
app
:
findbugsOfficialAustralisDebug
'
         
'
app
:
findbugsOfficialPhotonDebug
'
        
]
    
]
    
'
artifact_flag_build_variant_in_try
'
:
None
}
