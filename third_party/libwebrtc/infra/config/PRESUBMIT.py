def
CheckChangeOnUpload
(
input_api
output_api
)
:
  
return
input_api
.
RunTests
(
      
input_api
.
canned_checks
.
CheckLucicfgGenOutput
(
          
input_api
output_api
          
'
config
.
star
'
)
)
+
input_api
.
canned_checks
.
CheckChangedLUCIConfigs
(
              
input_api
output_api
)
  
return
res
def
CheckChangeOnCommit
(
input_api
output_api
)
:
  
return
CheckChangeOnUpload
(
input_api
output_api
)
