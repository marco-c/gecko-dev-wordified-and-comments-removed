import
subprocess
import
sys
import
threading
import
urllib
.
request
from
urllib
.
parse
import
urlparse
urlunparse
URI_HEADER
=
"
URI
:
"
def
url_exists
(
url
)
:
    
try
:
        
req
=
urllib
.
request
.
Request
(
url
method
=
"
HEAD
"
)
        
response
=
urllib
.
request
.
urlopen
(
req
)
        
return
response
.
getcode
(
)
=
=
200
    
except
Exception
:
        
return
False
def
write_and_flush
(
fh
data
)
:
    
fh
.
write
(
data
)
    
fh
.
flush
(
)
def
output_handler
(
proc
url_mapping
lock
)
:
    
for
line
in
proc
.
stdout
:
        
if
line
.
startswith
(
URI_HEADER
)
:
            
url
=
line
[
len
(
URI_HEADER
)
:
]
.
rstrip
(
)
            
with
lock
:
                
original_url
=
url_mapping
.
get
(
url
None
)
            
if
original_url
:
                
write_and_flush
(
sys
.
stdout
line
.
replace
(
url
original_url
)
)
                
continue
        
write_and_flush
(
sys
.
stdout
line
)
def
main
(
)
:
    
proc
=
subprocess
.
Popen
(
        
[
"
/
usr
/
lib
/
apt
/
methods
/
http
"
]
        
stdin
=
subprocess
.
PIPE
        
stdout
=
subprocess
.
PIPE
        
text
=
True
    
)
    
url_mapping
=
{
}
    
lock
=
threading
.
Lock
(
)
    
output_thread
=
threading
.
Thread
(
        
target
=
output_handler
args
=
(
proc
url_mapping
lock
)
daemon
=
True
    
)
    
output_thread
.
start
(
)
    
while
True
:
        
try
:
            
line
=
sys
.
stdin
.
readline
(
)
        
except
KeyboardInterrupt
:
            
break
        
if
not
line
:
            
break
        
if
line
.
startswith
(
URI_HEADER
)
:
            
url
=
line
[
len
(
URI_HEADER
)
:
]
.
rstrip
(
)
            
url_parts
=
urlparse
(
url
)
            
if
url_parts
.
hostname
=
=
"
snapshot
.
debian
.
org
"
and
url_parts
.
path
.
endswith
(
                
"
.
deb
"
            
)
:
                
path_parts
=
url_parts
.
path
.
split
(
"
/
"
)
                
path_parts
.
pop
(
3
)
                
path_parts
.
pop
(
1
)
                
modified_url
=
urlunparse
(
                    
url_parts
.
_replace
(
                        
netloc
=
"
deb
.
debian
.
org
"
path
=
"
/
"
.
join
(
path_parts
)
                    
)
                
)
                
if
url_exists
(
modified_url
)
:
                    
with
lock
:
                        
url_mapping
[
modified_url
]
=
url
                    
write_and_flush
(
proc
.
stdin
line
.
replace
(
url
modified_url
)
)
                    
continue
        
write_and_flush
(
proc
.
stdin
line
)
    
proc
.
stdin
.
close
(
)
    
output_thread
.
join
(
)
if
__name__
=
=
"
__main__
"
:
    
main
(
)
