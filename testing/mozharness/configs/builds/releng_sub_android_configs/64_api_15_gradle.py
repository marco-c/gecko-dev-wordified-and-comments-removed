config
=
{
    
'
base_name
'
:
'
Android
armv7
API
15
+
%
(
branch
)
s
Gradle
'
    
'
stage_platform
'
:
'
android
-
api
-
15
-
gradle
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
gradle
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
gradle
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
postflight_build_mach_commands
'
:
[
        
[
'
gradle
'
         
'
geckoview
:
assembleWithGeckoBinaries
'
         
'
geckoview_example
:
assembleWithGeckoBinaries
'
         
'
uploadArchives
'
        
]
    
]
    
'
artifact_flag_build_variant_in_try
'
:
'
api
-
15
-
gradle
-
artifact
'
}
