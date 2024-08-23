def
main
(
request
response
)
:
  
script
=
request
.
GET
.
first
(
b
"
script
"
)
  
should_ack_load
=
b
"
false
"
  
try
:
    
if
request
.
GET
.
first
(
b
"
should_ack_load
"
)
=
=
b
"
true
"
:
      
should_ack_load
=
b
"
true
"
  
except
:
    
pass
  
cookie_header
=
request
.
headers
.
get
(
b
"
Cookie
"
b
"
"
)
  
body
=
b
"
"
"
  
<
!
DOCTYPE
html
>
  
<
meta
charset
=
"
utf
-
8
"
>
  
<
title
>
Subframe
with
HTTP
Cookies
<
/
title
>
  
<
script
src
=
"
/
resources
/
testharness
.
js
"
>
<
/
script
>
  
<
script
src
=
"
/
resources
/
testdriver
.
js
"
>
<
/
script
>
  
<
script
src
=
"
/
resources
/
testdriver
-
vendor
.
js
"
>
<
/
script
>
  
<
script
>
    
var
httpCookies
=
"
%
s
"
;
    
var
should_ack_load
=
%
s
;
  
<
/
script
>
  
<
body
>
  
<
script
src
=
"
%
s
"
>
<
/
script
>
  
<
/
body
>
  
"
"
"
%
(
cookie_header
should_ack_load
script
)
  
return
(
200
[
]
body
)
