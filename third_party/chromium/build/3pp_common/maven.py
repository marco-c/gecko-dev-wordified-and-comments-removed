"
"
"
The
fetch
.
py
and
install
.
py
helpers
for
a
3pp
Maven
module
.
"
"
"
import
os
import
pathlib
import
re
import
shutil
import
subprocess
import
urllib
.
request
import
common
APACHE_MAVEN_URL
=
'
https
:
/
/
repo
.
maven
.
apache
.
org
/
maven2
'
_POM_TEMPLATE
=
"
"
"
\
<
project
>
  
<
modelVersion
>
4
.
0
.
0
<
/
modelVersion
>
  
<
groupId
>
group
<
/
groupId
>
  
<
artifactId
>
artifact
<
/
artifactId
>
  
<
version
>
1
<
/
version
>
  
<
dependencies
>
    
<
dependency
>
      
<
groupId
>
{
group_id
}
<
/
groupId
>
      
<
artifactId
>
{
artifact_id
}
<
/
artifactId
>
      
<
version
>
{
version
}
<
/
version
>
      
<
scope
>
runtime
<
/
scope
>
    
<
/
dependency
>
  
<
/
dependencies
>
  
<
build
>
    
<
plugins
>
      
<
plugin
>
        
<
artifactId
>
maven
-
assembly
-
plugin
<
/
artifactId
>
        
<
version
>
3
.
3
.
0
<
/
version
>
        
<
configuration
>
          
<
descriptorRefs
>
            
<
descriptorRef
>
jar
-
with
-
dependencies
<
/
descriptorRef
>
          
<
/
descriptorRefs
>
        
<
/
configuration
>
        
<
executions
>
          
<
execution
>
            
<
phase
>
package
<
/
phase
>
            
<
goals
>
              
<
goal
>
single
<
/
goal
>
            
<
/
goals
>
          
<
/
execution
>
        
<
/
executions
>
      
<
/
plugin
>
    
<
/
plugins
>
  
<
/
build
>
  
<
repositories
>
    
<
repository
>
      
<
id
>
placeholder_id
<
/
id
>
      
<
name
>
placeholder_name
<
/
name
>
      
<
url
>
{
maven_url
}
<
/
url
>
    
<
/
repository
>
  
<
/
repositories
>
<
/
project
>
"
"
"
def
_detect_latest
(
maven_url
package
)
:
    
metadata_url
=
'
{
}
/
{
}
/
maven
-
metadata
.
xml
'
.
format
(
        
maven_url
        
package
.
replace
(
'
.
'
'
/
'
)
.
replace
(
'
:
'
'
/
'
)
)
    
metadata
=
urllib
.
request
.
urlopen
(
metadata_url
)
.
read
(
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
    
m
=
re
.
search
(
'
<
latest
>
(
[
^
<
]
+
)
<
/
latest
>
'
metadata
)
    
if
m
:
        
latest
=
m
.
group
(
1
)
    
else
:
        
latest
=
re
.
findall
(
'
<
version
>
(
[
^
<
]
+
)
<
/
version
>
'
metadata
)
[
-
1
]
    
return
latest
def
_install
(
output_prefix
             
deps_prefix
             
maven_url
             
package
             
version
             
jar_name
=
None
             
post_process_func
=
None
)
:
    
group_id
artifact_id
=
package
.
split
(
'
:
'
)
    
if
not
jar_name
:
        
jar_name
=
f
'
{
artifact_id
}
.
jar
'
    
pathlib
.
Path
(
'
pom
.
xml
'
)
.
write_text
(
        
_POM_TEMPLATE
.
format
(
version
=
version
                             
group_id
=
group_id
                             
artifact_id
=
artifact_id
                             
maven_url
=
maven_url
)
)
    
env
=
os
.
environ
.
copy
(
)
    
env
[
'
JAVA_HOME
'
]
=
common
.
path_within_checkout
(
'
third_party
/
jdk
/
current
'
)
    
subprocess
.
run
(
[
'
mvn
'
'
-
v
'
]
check
=
True
env
=
env
)
    
subprocess
.
run
(
[
'
mvn
'
'
clean
'
'
assembly
:
single
'
'
-
f
'
'
pom
.
xml
'
]
                   
check
=
True
                   
env
=
env
)
    
src_jar_path
=
'
target
/
artifact
-
1
-
jar
-
with
-
dependencies
.
jar
'
    
dst_jar_path
=
os
.
path
.
join
(
output_prefix
jar_name
)
    
if
post_process_func
:
        
post_process_func
(
src_jar_path
dst_jar_path
)
    
else
:
        
shutil
.
move
(
src_jar_path
dst_jar_path
)
def
main
(
*
         
package
         
jar_name
=
None
         
maven_url
=
'
https
:
/
/
dl
.
google
.
com
/
android
/
maven2
'
         
post_process_func
=
None
         
version_override
=
None
)
:
    
"
"
"
3pp
entry
point
for
fetch
.
py
.
    
Args
:
      
package
:
E
.
g
.
:
some
.
package
:
some
-
thing
      
jar_name
:
Name
of
.
jar
.
Defaults
to
|
some
-
thing
|
.
jar
      
maven_url
:
URL
of
Maven
repository
.
      
post_process_func
:
Called
to
finish
.
Args
:
src_jar_path
dst_jar_path
      
version_override
:
Use
this
version
instead
of
the
latest
one
.
    
"
"
"
    
def
do_latest
(
)
:
        
return
version_override
or
_detect_latest
(
maven_url
package
)
    
def
do_install
(
args
)
:
        
_install
(
args
.
output_prefix
args
.
deps_prefix
maven_url
package
                 
args
.
version
jar_name
post_process_func
)
    
common
.
main
(
do_latest
=
do_latest
                
do_install
=
do_install
                
runtime_deps
=
[
'
/
/
third_party
/
jdk
/
current
'
]
)
