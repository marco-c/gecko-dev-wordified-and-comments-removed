from
wptserve
.
utils
import
isomorphic_decode
def
main
(
request
response
)
:
  
headers
=
[
    
(
'
Content
-
Type
'
'
Application
/
Javascript
'
)
    
(
'
Ad
-
Auction
-
Allowed
'
'
true
'
)
  
]
  
requested_size
=
request
.
GET
.
first
(
b
"
requested
-
size
"
None
)
  
requested_size_check
=
'
'
  
if
requested_size
is
not
None
:
    
width
height
=
isomorphic_decode
(
requested_size
)
.
split
(
'
-
'
)
    
requested_size_check
=
(
      
f
'
'
'
        
if
(
!
(
auctionConfig
.
requestedSize
.
width
=
=
=
'
{
width
}
'
)
&
&
             
(
auctionConfig
.
requestedSize
.
height
=
=
=
'
{
height
}
'
)
)
{
{
          
throw
new
Error
(
'
requestedSize
missing
/
incorrect
in
auctionConfig
'
)
;
        
}
}
      
'
'
'
    
)
  
score_ad
=
(
    
f
'
'
'
function
scoreAd
(
      
adMetadata
      
bid
      
auctionConfig
      
trustedScoringSignals
      
browserSignals
)
{
{
        
{
requested_size_check
}
        
return
2
*
bid
;
      
}
}
    
'
'
'
  
)
  
report_result
=
(
    
f
'
'
'
function
reportResult
(
      
auctionConfig
      
browserSignals
)
{
{
        
{
requested_size_check
}
        
return
;
      
}
}
    
'
'
'
  
)
  
content
=
f
'
{
score_ad
}
\
n
{
report_result
}
'
  
return
(
headers
content
)
