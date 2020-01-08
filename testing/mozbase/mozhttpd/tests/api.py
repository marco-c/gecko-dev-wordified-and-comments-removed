from
__future__
import
absolute_import
import
mozfile
import
mozhttpd
import
os
import
unittest
import
json
import
tempfile
import
mozunit
from
six
.
moves
.
urllib
.
request
import
(
    
HTTPHandler
    
ProxyHandler
    
Request
    
build_opener
    
install_opener
    
urlopen
)
from
six
.
moves
.
urllib
.
error
import
HTTPError
here
=
os
.
path
.
dirname
(
os
.
path
.
abspath
(
__file__
)
)
class
ApiTest
(
unittest
.
TestCase
)
:
    
resource_get_called
=
0
    
resource_post_called
=
0
    
resource_del_called
=
0
    
mozhttpd
.
handlers
.
json_response
    
def
resource_get
(
self
request
objid
)
:
        
self
.
resource_get_called
+
=
1
        
return
(
200
{
'
called
'
:
self
.
resource_get_called
                      
'
id
'
:
objid
                      
'
query
'
:
request
.
query
}
)
    
mozhttpd
.
handlers
.
json_response
    
def
resource_post
(
self
request
)
:
        
self
.
resource_post_called
+
=
1
        
return
(
201
{
'
called
'
:
self
.
resource_post_called
                      
'
data
'
:
json
.
loads
(
request
.
body
)
                      
'
query
'
:
request
.
query
}
)
    
mozhttpd
.
handlers
.
json_response
    
def
resource_del
(
self
request
objid
)
:
        
self
.
resource_del_called
+
=
1
        
return
(
200
{
'
called
'
:
self
.
resource_del_called
                      
'
id
'
:
objid
                      
'
query
'
:
request
.
query
}
)
    
def
get_url
(
self
path
server_port
querystr
)
:
        
url
=
"
http
:
/
/
127
.
0
.
0
.
1
:
%
s
%
s
"
%
(
server_port
path
)
        
if
querystr
:
            
url
+
=
"
?
%
s
"
%
querystr
        
return
url
    
def
try_get
(
self
server_port
querystr
)
:
        
self
.
resource_get_called
=
0
        
f
=
urlopen
(
self
.
get_url
(
'
/
api
/
resource
/
1
'
server_port
querystr
)
)
        
try
:
            
self
.
assertEqual
(
f
.
getcode
(
)
200
)
        
except
AttributeError
:
            
pass
        
self
.
assertEqual
(
json
.
loads
(
f
.
read
(
)
)
{
'
called
'
:
1
'
id
'
:
str
(
1
)
'
query
'
:
querystr
}
)
        
self
.
assertEqual
(
self
.
resource_get_called
1
)
    
def
try_post
(
self
server_port
querystr
)
:
        
self
.
resource_post_called
=
0
        
postdata
=
{
'
hamburgers
'
:
'
1234
'
}
        
try
:
            
f
=
urlopen
(
                
self
.
get_url
(
'
/
api
/
resource
/
'
server_port
querystr
)
                
data
=
json
.
dumps
(
postdata
)
            
)
        
except
HTTPError
as
e
:
            
self
.
assertEqual
(
e
.
code
201
)
            
body
=
e
.
fp
.
read
(
)
        
else
:
            
self
.
assertEqual
(
f
.
getcode
(
)
201
)
            
body
=
f
.
read
(
)
        
self
.
assertEqual
(
json
.
loads
(
body
)
{
'
called
'
:
1
                                            
'
data
'
:
postdata
                                            
'
query
'
:
querystr
}
)
        
self
.
assertEqual
(
self
.
resource_post_called
1
)
    
def
try_del
(
self
server_port
querystr
)
:
        
self
.
resource_del_called
=
0
        
opener
=
build_opener
(
HTTPHandler
)
        
request
=
Request
(
self
.
get_url
(
'
/
api
/
resource
/
1
'
server_port
querystr
)
)
        
request
.
get_method
=
lambda
:
'
DEL
'
        
f
=
opener
.
open
(
request
)
        
try
:
            
self
.
assertEqual
(
f
.
getcode
(
)
200
)
        
except
AttributeError
:
            
pass
        
self
.
assertEqual
(
json
.
loads
(
f
.
read
(
)
)
{
'
called
'
:
1
'
id
'
:
str
(
1
)
'
query
'
:
querystr
}
)
        
self
.
assertEqual
(
self
.
resource_del_called
1
)
    
def
test_api
(
self
)
:
        
httpd
=
mozhttpd
.
MozHttpd
(
port
=
0
                                  
urlhandlers
=
[
{
'
method
'
:
'
GET
'
                                                
'
path
'
:
'
/
api
/
resource
/
(
[
^
/
]
+
)
/
?
'
                                                
'
function
'
:
self
.
resource_get
}
                                               
{
'
method
'
:
'
POST
'
                                                
'
path
'
:
'
/
api
/
resource
/
?
'
                                                
'
function
'
:
self
.
resource_post
}
                                               
{
'
method
'
:
'
DEL
'
                                                
'
path
'
:
'
/
api
/
resource
/
(
[
^
/
]
+
)
/
?
'
                                                
'
function
'
:
self
.
resource_del
}
                                               
]
)
        
httpd
.
start
(
block
=
False
)
        
server_port
=
httpd
.
httpd
.
server_port
        
self
.
try_get
(
server_port
'
'
)
        
self
.
try_get
(
server_port
'
?
foo
=
bar
'
)
        
self
.
try_post
(
server_port
'
'
)
        
self
.
try_post
(
server_port
'
?
foo
=
bar
'
)
        
self
.
try_del
(
server_port
'
'
)
        
self
.
try_del
(
server_port
'
?
foo
=
bar
'
)
        
exception_thrown
=
False
        
try
:
            
urlopen
(
self
.
get_url
(
'
/
'
server_port
None
)
)
        
except
HTTPError
as
e
:
            
self
.
assertEqual
(
e
.
code
404
)
            
exception_thrown
=
True
        
self
.
assertTrue
(
exception_thrown
)
    
def
test_nonexistent_resources
(
self
)
:
        
httpd
=
mozhttpd
.
MozHttpd
(
port
=
0
)
        
httpd
.
start
(
block
=
False
)
        
server_port
=
httpd
.
httpd
.
server_port
        
exception_thrown
=
False
        
try
:
            
urlopen
(
self
.
get_url
(
'
/
api
/
resource
/
'
server_port
None
)
)
        
except
HTTPError
as
e
:
            
self
.
assertEqual
(
e
.
code
404
)
            
exception_thrown
=
True
        
self
.
assertTrue
(
exception_thrown
)
        
exception_thrown
=
False
        
try
:
            
urlopen
(
                
self
.
get_url
(
'
/
api
/
resource
/
'
server_port
None
)
                
data
=
json
.
dumps
(
{
}
)
            
)
        
except
HTTPError
as
e
:
            
self
.
assertEqual
(
e
.
code
404
)
            
exception_thrown
=
True
        
self
.
assertTrue
(
exception_thrown
)
        
exception_thrown
=
False
        
try
:
            
opener
=
build_opener
(
HTTPHandler
)
            
request
=
Request
(
self
.
get_url
(
'
/
api
/
resource
/
'
server_port
None
)
)
            
request
.
get_method
=
lambda
:
'
DEL
'
            
opener
.
open
(
request
)
        
except
HTTPError
:
            
self
.
assertEqual
(
e
.
code
404
)
            
exception_thrown
=
True
        
self
.
assertTrue
(
exception_thrown
)
    
def
test_api_with_docroot
(
self
)
:
        
httpd
=
mozhttpd
.
MozHttpd
(
port
=
0
docroot
=
here
                                  
urlhandlers
=
[
{
'
method
'
:
'
GET
'
                                                
'
path
'
:
'
/
api
/
resource
/
(
[
^
/
]
+
)
/
?
'
                                                
'
function
'
:
self
.
resource_get
}
]
)
        
httpd
.
start
(
block
=
False
)
        
server_port
=
httpd
.
httpd
.
server_port
        
f
=
urlopen
(
self
.
get_url
(
'
/
'
server_port
None
)
)
        
try
:
            
self
.
assertEqual
(
f
.
getcode
(
)
200
)
        
except
AttributeError
:
            
pass
        
self
.
assertTrue
(
'
Directory
listing
for
'
in
f
.
read
(
)
)
        
self
.
try_get
(
server_port
'
'
)
        
self
.
try_get
(
server_port
'
?
foo
=
bar
'
)
class
ProxyTest
(
unittest
.
TestCase
)
:
    
def
tearDown
(
self
)
:
        
install_opener
(
None
)
    
def
test_proxy
(
self
)
:
        
docroot
=
tempfile
.
mkdtemp
(
)
        
self
.
addCleanup
(
mozfile
.
remove
docroot
)
        
hosts
=
(
'
mozilla
.
com
'
'
mozilla
.
org
'
)
        
unproxied_host
=
'
notmozilla
.
org
'
        
def
url
(
host
)
:
return
'
http
:
/
/
%
s
/
'
%
host
        
index_filename
=
'
index
.
html
'
        
def
index_contents
(
host
)
:
return
'
%
s
index
'
%
host
        
index
=
open
(
os
.
path
.
join
(
docroot
index_filename
)
'
w
'
)
        
index
.
write
(
index_contents
(
'
*
'
)
)
        
index
.
close
(
)
        
httpd
=
mozhttpd
.
MozHttpd
(
port
=
0
docroot
=
docroot
)
        
httpd
.
start
(
block
=
False
)
        
server_port
=
httpd
.
httpd
.
server_port
        
proxy_support
=
ProxyHandler
(
{
            
'
http
'
:
'
http
:
/
/
127
.
0
.
0
.
1
:
%
d
'
%
server_port
        
}
)
        
install_opener
(
build_opener
(
proxy_support
)
)
        
for
host
in
hosts
:
            
f
=
urlopen
(
url
(
host
)
)
            
try
:
                
self
.
assertEqual
(
f
.
getcode
(
)
200
)
            
except
AttributeError
:
                
pass
            
self
.
assertEqual
(
f
.
read
(
)
index_contents
(
'
*
'
)
)
        
httpd
.
stop
(
)
        
httpd
=
mozhttpd
.
MozHttpd
(
port
=
0
docroot
=
docroot
proxy_host_dirs
=
True
)
        
httpd
.
start
(
block
=
False
)
        
server_port
=
httpd
.
httpd
.
server_port
        
proxy_support
=
ProxyHandler
(
{
            
'
http
'
:
'
http
:
/
/
127
.
0
.
0
.
1
:
%
d
'
%
server_port
        
}
)
        
install_opener
(
build_opener
(
proxy_support
)
)
        
for
host
in
hosts
:
            
os
.
mkdir
(
os
.
path
.
join
(
docroot
host
)
)
            
open
(
os
.
path
.
join
(
docroot
host
index_filename
)
'
w
'
)
\
                
.
write
(
index_contents
(
host
)
)
        
for
host
in
hosts
:
            
f
=
urlopen
(
url
(
host
)
)
            
try
:
                
self
.
assertEqual
(
f
.
getcode
(
)
200
)
            
except
AttributeError
:
                
pass
            
self
.
assertEqual
(
f
.
read
(
)
index_contents
(
host
)
)
        
exc
=
None
        
try
:
            
urlopen
(
url
(
unproxied_host
)
)
        
except
HTTPError
as
e
:
            
exc
=
e
        
self
.
assertNotEqual
(
exc
None
)
        
self
.
assertEqual
(
exc
.
code
404
)
if
__name__
=
=
'
__main__
'
:
    
mozunit
.
main
(
)
