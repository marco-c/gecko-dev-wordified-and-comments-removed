"
"
"
Signs
and
aligns
an
APK
.
"
"
"
import
argparse
import
logging
import
shutil
import
subprocess
import
sys
import
tempfile
from
util
import
build_utils
def
FinalizeApk
(
apksigner_path
                
zipalign_path
                
unsigned_apk_path
                
final_apk_path
                
key_path
                
key_passwd
                
key_name
                
min_sdk_version
                
warnings_as_errors
=
False
)
:
  
with
tempfile
.
NamedTemporaryFile
(
)
as
staging_file
:
    
if
zipalign_path
:
      
logging
.
debug
(
'
Running
zipalign
'
)
      
zipalign_cmd
=
[
          
zipalign_path
'
-
p
'
'
-
f
'
'
4
'
unsigned_apk_path
staging_file
.
name
      
]
      
build_utils
.
CheckOutput
(
zipalign_cmd
                              
print_stdout
=
True
                              
fail_on_output
=
warnings_as_errors
)
      
signer_input_path
=
staging_file
.
name
    
else
:
      
signer_input_path
=
unsigned_apk_path
    
sign_cmd
=
build_utils
.
JavaCmd
(
)
+
[
        
'
-
jar
'
        
apksigner_path
        
'
sign
'
        
'
-
-
in
'
        
signer_input_path
        
'
-
-
out
'
        
staging_file
.
name
        
'
-
-
ks
'
        
key_path
        
'
-
-
ks
-
key
-
alias
'
        
key_name
        
'
-
-
ks
-
pass
'
        
'
pass
:
'
+
key_passwd
    
]
    
sign_cmd
+
=
[
'
-
-
v3
-
signing
-
enabled
'
'
false
'
]
    
if
min_sdk_version
>
=
24
:
      
sign_cmd
+
=
[
'
-
-
v1
-
signing
-
enabled
'
'
false
'
]
    
else
:
      
sign_cmd
+
=
[
'
-
-
min
-
sdk
-
version
'
'
1
'
]
    
logging
.
debug
(
'
Signing
apk
'
)
    
build_utils
.
CheckOutput
(
sign_cmd
                            
print_stdout
=
True
                            
fail_on_output
=
warnings_as_errors
)
    
shutil
.
move
(
staging_file
.
name
final_apk_path
)
    
if
sys
.
version_info
.
major
=
=
2
:
      
staging_file
.
delete
=
False
    
else
:
      
staging_file
.
_closer
.
delete
=
False
