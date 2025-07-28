"
"
"
Implementation
of
skia_gold_session
.
py
without
output
managers
.
Diff
output
is
instead
stored
in
a
directory
and
pointed
to
with
file
:
/
/
URLs
.
"
"
"
import
os
import
subprocess
import
time
import
six
from
skia_gold_common
import
skia_gold_session
class
OutputManagerlessSkiaGoldSession
(
skia_gold_session
.
SkiaGoldSession
)
:
  
def
RunComparison
(
      
self
      
name
      
png_file
      
output_manager
=
True
      
inexact_matching_args
=
None
      
use_luci
=
True
      
optional_keys
=
None
      
force_dryrun
=
False
)
:
    
return
super
(
OutputManagerlessSkiaGoldSession
self
)
.
RunComparison
(
        
name
=
name
        
png_file
=
png_file
        
output_manager
=
output_manager
        
inexact_matching_args
=
inexact_matching_args
        
use_luci
=
use_luci
        
optional_keys
=
optional_keys
        
force_dryrun
=
force_dryrun
)
  
def
_CreateDiffOutputDir
(
self
name
)
:
    
timestamp
=
int
(
time
.
time
(
)
)
    
name
=
'
%
s_
%
d
'
%
(
name
timestamp
)
    
filepath
=
os
.
path
.
join
(
self
.
_local_png_directory
name
)
    
os
.
makedirs
(
filepath
)
    
return
filepath
  
def
_StoreDiffLinks
(
self
image_name
_
output_dir
)
:
    
results
=
self
.
_comparison_results
.
setdefault
(
image_name
                                                  
self
.
ComparisonResults
(
)
)
    
for
f
in
os
.
listdir
(
output_dir
)
:
      
file_url
=
'
file
:
/
/
%
s
'
%
os
.
path
.
join
(
output_dir
f
)
      
if
f
.
startswith
(
'
input
-
'
)
:
        
results
.
local_diff_given_image
=
file_url
      
elif
f
.
startswith
(
'
closest
-
'
)
:
        
results
.
local_diff_closest_image
=
file_url
      
elif
f
=
=
'
diff
.
png
'
:
        
results
.
local_diff_diff_image
=
file_url
  
staticmethod
  
def
_RunCmdForRcAndOutput
(
cmd
)
:
    
try
:
      
output
=
subprocess
.
check_output
(
cmd
                                       
stderr
=
subprocess
.
STDOUT
)
.
decode
(
'
utf
-
8
'
)
      
return
0
output
    
except
subprocess
.
CalledProcessError
as
e
:
      
output
=
e
.
output
      
if
not
isinstance
(
output
six
.
string_types
)
:
        
output
=
output
.
decode
(
'
utf
-
8
'
)
      
return
e
.
returncode
output
