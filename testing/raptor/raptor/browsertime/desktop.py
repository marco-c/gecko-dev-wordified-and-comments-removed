from
logger
.
logger
import
RaptorLogger
from
perftest
import
PerftestDesktop
from
.
base
import
Browsertime
LOG
=
RaptorLogger
(
component
=
"
raptor
-
browsertime
-
desktop
"
)
class
BrowsertimeDesktop
(
PerftestDesktop
Browsertime
)
:
    
def
__init__
(
self
*
args
*
*
kwargs
)
:
        
super
(
BrowsertimeDesktop
self
)
.
__init__
(
*
args
*
*
kwargs
)
    
property
    
def
browsertime_args
(
self
)
:
        
binary_path
=
self
.
config
[
"
binary
"
]
        
LOG
.
info
(
"
binary_path
:
{
}
"
.
format
(
binary_path
)
)
        
args_list
=
[
"
-
-
viewPort
"
"
1280x1024
"
]
        
if
self
.
config
[
"
app
"
]
in
(
            
"
chrome
"
            
"
chromium
"
            
"
custom
-
car
"
        
)
:
            
return
args_list
+
[
                
"
-
-
browser
"
                
"
chrome
"
                
"
-
-
chrome
.
binaryPath
"
                
binary_path
            
]
        
return
args_list
+
[
            
"
-
-
browser
"
            
self
.
config
[
"
app
"
]
            
"
-
-
firefox
.
binaryPath
"
            
binary_path
        
]
    
def
setup_chrome_args
(
self
test
)
:
        
chrome_args
=
self
.
desktop_chrome_args
(
test
)
        
chrome_args
.
extend
(
            
[
"
-
-
no
-
first
-
run
"
"
-
-
no
-
experiments
"
"
-
-
disable
-
site
-
isolation
-
trials
"
]
        
)
        
btime_chrome_args
=
[
]
        
for
arg
in
chrome_args
:
            
btime_chrome_args
.
extend
(
[
"
-
-
chrome
.
args
=
"
+
str
(
arg
.
replace
(
"
'
"
'
"
'
)
)
]
)
        
return
btime_chrome_args
