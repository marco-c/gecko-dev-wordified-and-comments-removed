from
__future__
import
absolute_import
unicode_literals
import
mimetypes
import
os
import
boto3
import
requests
def
s3_upload
(
root
)
:
    
region
=
'
us
-
west
-
2
'
    
level
=
os
.
environ
.
get
(
'
MOZ_SCM_LEVEL
'
'
1
'
)
    
bucket
=
{
        
'
1
'
:
'
gecko
-
docs
.
mozilla
.
org
-
l1
'
        
'
2
'
:
'
gecko
-
docs
.
mozilla
.
org
-
l2
'
        
'
3
'
:
'
gecko
-
docs
.
mozilla
.
org
'
    
}
[
level
]
    
secrets_url
=
'
http
:
/
/
taskcluster
/
secrets
/
v1
/
secret
/
'
    
secrets_url
+
=
'
project
/
releng
/
gecko
/
build
/
level
-
{
}
/
gecko
-
docs
-
upload
'
.
format
(
        
level
)
    
if
'
TASK_ID
'
in
os
.
environ
:
        
print
(
"
Using
AWS
credentials
from
the
secrets
service
"
)
        
session
=
requests
.
Session
(
)
        
res
=
session
.
get
(
secrets_url
)
        
res
.
raise_for_status
(
)
        
secret
=
res
.
json
(
)
[
'
secret
'
]
        
session
=
boto3
.
session
.
Session
(
            
aws_access_key_id
=
secret
[
'
AWS_ACCESS_KEY_ID
'
]
            
aws_secret_access_key
=
secret
[
'
AWS_SECRET_ACCESS_KEY
'
]
            
region_name
=
region
)
    
else
:
        
print
(
"
Trying
to
use
your
AWS
credentials
.
.
"
)
        
session
=
boto3
.
session
.
Session
(
region_name
=
region
)
    
s3
=
session
.
client
(
'
s3
'
)
    
try
:
        
old_cwd
=
os
.
getcwd
(
)
        
os
.
chdir
(
root
)
        
for
dir
dirs
filenames
in
os
.
walk
(
'
.
'
)
:
            
if
dir
=
=
'
.
'
:
                
bad
=
[
d
for
d
in
dirs
if
                       
d
.
startswith
(
'
.
'
)
or
d
in
(
'
_venv
'
'
_staging
'
)
]
                
for
b
in
bad
:
                    
dirs
.
remove
(
b
)
            
for
filename
in
filenames
:
                
pathname
=
os
.
path
.
join
(
dir
filename
)
[
2
:
]
                
content_type
content_encoding
=
mimetypes
.
guess_type
(
pathname
)
                
extra_args
=
{
}
                
if
content_type
:
                    
extra_args
[
'
ContentType
'
]
=
content_type
                
if
content_encoding
:
                    
extra_args
[
'
ContentEncoding
'
]
=
content_encoding
                
print
(
'
uploading
'
pathname
)
                
s3
.
upload_file
(
pathname
bucket
pathname
ExtraArgs
=
extra_args
)
    
finally
:
        
os
.
chdir
(
old_cwd
)
