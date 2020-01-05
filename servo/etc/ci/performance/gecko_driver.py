from
contextlib
import
contextmanager
import
json
import
os
from
selenium
import
webdriver
from
selenium
.
common
.
exceptions
import
TimeoutException
import
sys
contextmanager
def
create_gecko_session
(
)
:
    
try
:
        
firefox_binary
=
os
.
environ
[
'
FIREFOX_BIN
'
]
    
except
KeyError
:
        
print
(
"
+
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
+
"
)
        
print
(
"
|
You
must
set
the
path
to
your
firefox
binary
to
FIREFOX_BIN
|
"
)
        
print
(
"
+
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
+
"
)
        
sys
.
exit
(
)
    
driver
=
webdriver
.
Firefox
(
firefox_binary
=
firefox_binary
)
    
yield
driver
    
driver
.
quit
(
)
def
generate_placeholder
(
testcase
)
:
        
timings
=
{
            
"
testcase
"
:
testcase
            
"
title
"
:
"
"
        
}
        
timing_names
=
[
            
"
navigationStart
"
            
"
unloadEventStart
"
            
"
domLoading
"
            
"
fetchStart
"
            
"
responseStart
"
            
"
loadEventEnd
"
            
"
connectStart
"
            
"
domainLookupStart
"
            
"
redirectStart
"
            
"
domContentLoadedEventEnd
"
            
"
requestStart
"
            
"
secureConnectionStart
"
            
"
connectEnd
"
            
"
loadEventStart
"
            
"
domInteractive
"
            
"
domContentLoadedEventStart
"
            
"
redirectEnd
"
            
"
domainLookupEnd
"
            
"
unloadEventEnd
"
            
"
responseEnd
"
            
"
domComplete
"
        
]
        
for
name
in
timing_names
:
            
timings
[
name
]
=
0
if
name
=
=
"
navigationStart
"
else
-
1
        
return
[
timings
]
def
run_gecko_test
(
testcase
timeout
is_async
)
:
    
with
create_gecko_session
(
)
as
driver
:
        
driver
.
set_page_load_timeout
(
timeout
)
        
try
:
            
driver
.
get
(
testcase
)
        
except
TimeoutException
:
            
print
(
"
Timeout
!
"
)
            
return
generate_placeholder
(
testcase
)
        
try
:
            
timings
=
{
                
"
testcase
"
:
testcase
                
"
title
"
:
driver
.
title
.
replace
(
"
"
"
&
#
44
;
"
)
            
}
            
timings
.
update
(
json
.
loads
(
                
driver
.
execute_script
(
                    
"
return
JSON
.
stringify
(
performance
.
timing
)
"
                
)
            
)
)
        
except
:
            
print
(
"
Failed
to
get
a
valid
timing
measurement
.
"
)
            
return
generate_placeholder
(
testcase
)
        
if
is_async
:
            
driver
.
implicitly_wait
(
5
)
            
driver
.
find_element_by_id
(
"
GECKO_TEST_DONE
"
)
            
timings
.
update
(
json
.
loads
(
                
driver
.
execute_script
(
                    
"
return
JSON
.
stringify
(
window
.
customTimers
)
"
                
)
            
)
)
    
return
[
timings
]
if
__name__
=
=
'
__main__
'
:
    
from
pprint
import
pprint
    
url
=
"
http
:
/
/
localhost
:
8000
/
page_load_test
/
tp5n
/
dailymail
.
co
.
uk
/
www
.
dailymail
.
co
.
uk
/
ushome
/
index
.
html
"
    
pprint
(
run_gecko_test
(
url
15
)
)
