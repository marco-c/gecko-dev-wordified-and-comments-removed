import
os
import
time
RESUME_WINDOW
=
5
RESUME_TIMEOUT
=
30
def
main
(
request
response
)
:
    
key
=
request
.
GET
.
first
(
b
"
key
"
)
    
stash
=
request
.
server
.
stash
    
if
request
.
method
=
=
"
POST
"
:
        
stash
.
put
(
key
True
)
        
time
.
sleep
(
RESUME_WINDOW
)
        
with
stash
.
lock
:
            
stash
.
take
(
key
)
        
return
f
"
put
{
key
}
into
stash
"
    
file_path
=
os
.
path
.
join
(
request
.
doc_root
"
media
"
"
movie_300
.
webm
"
)
    
with
open
(
file_path
"
rb
"
)
as
f
:
        
f
.
seek
(
0
os
.
SEEK_END
)
        
file_size
=
f
.
tell
(
)
        
f
.
seek
(
0
os
.
SEEK_SET
)
        
response
.
add_required_headers
=
False
        
response
.
writer
.
write_status
(
200
)
        
response
.
writer
.
write_header
(
"
Content
-
Type
"
"
video
/
webm
"
)
        
response
.
writer
.
write_header
(
"
Content
-
Length
"
str
(
file_size
)
)
        
response
.
writer
.
end_headers
(
)
        
first_size
=
4096
        
response
.
writer
.
write
(
f
.
read
(
first_size
)
)
        
deadline
=
time
.
monotonic
(
)
+
RESUME_TIMEOUT
        
while
True
:
            
with
stash
.
lock
:
                
if
stash
.
take
(
key
)
=
=
True
:
                    
stash
.
put
(
key
True
)
                    
break
            
if
time
.
monotonic
(
)
>
deadline
:
                
return
            
time
.
sleep
(
0
.
1
)
        
response
.
writer
.
write
(
f
.
read
(
file_size
-
first_size
)
)
