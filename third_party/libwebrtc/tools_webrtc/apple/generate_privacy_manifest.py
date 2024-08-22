__doc__
=
"
"
"
Generate
privacy
manifest
of
WebRTC
iOS
framework
.
"
"
"
import
argparse
import
plistlib
import
sys
def
generate_privacy_manifest
(
out_file
)
:
    
privacy_manifest
=
{
        
"
NSPrivacyTracking
"
:
        
False
        
"
NSPrivacyCollectedDataTypes
"
:
[
]
        
"
NSPrivacyTrackingDomains
"
:
[
]
        
"
NSPrivacyAccessedAPITypes
"
:
[
            
{
                
"
NSPrivacyAccessedAPIType
"
:
                
"
NSPrivacyAccessedAPICategorySystemBootTime
"
                
"
NSPrivacyAccessedAPITypeReasons
"
:
[
                    
"
35F9
.
1
"
                    
"
8FFB
.
1
"
                
]
            
}
            
{
                
"
NSPrivacyAccessedAPIType
"
:
                
"
NSPrivacyAccessedAPICategoryFileTimestamp
"
                
"
NSPrivacyAccessedAPITypeReasons
"
:
[
                    
"
C617
.
1
"
                
]
            
}
        
]
    
}
    
with
open
(
out_file
'
wb
'
)
as
file
:
        
plistlib
.
dump
(
privacy_manifest
file
fmt
=
plistlib
.
FMT_XML
)
def
main
(
)
:
    
parser
=
argparse
.
ArgumentParser
(
description
=
__doc__
)
    
parser
.
add_argument
(
"
-
o
"
"
-
-
output
"
type
=
str
help
=
"
Output
file
.
"
)
    
args
=
parser
.
parse_args
(
)
    
if
not
args
.
output
:
        
print
(
"
Output
file
is
required
"
)
        
return
1
    
generate_privacy_manifest
(
args
.
output
)
    
return
0
if
__name__
=
=
'
__main__
'
:
    
sys
.
exit
(
main
(
)
)
