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
  
ad_with_size
=
request
.
GET
.
first
(
b
"
ad
-
with
-
size
"
None
)
  
beacon
=
request
.
GET
.
first
(
b
"
beacon
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
browserSignals
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
browserSignals
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
browserSignals
'
)
;
        
}
}
      
'
'
'
    
)
  
render_obj
=
'
ad
.
renderURL
'
  
if
ad_with_size
is
not
None
:
    
render_obj
=
'
{
url
:
ad
.
renderURL
width
:
"
100px
"
height
:
"
50px
"
}
'
  
component_render_obj
=
'
component
.
renderURL
'
  
if
ad_with_size
is
not
None
:
    
component_render_obj
=
(
      
'
'
'
{
          
url
:
component
.
renderURL
          
width
:
"
100px
"
          
height
:
"
50px
"
         
}
      
'
'
'
    
)
  
register_ad_beacon
=
'
'
  
if
beacon
is
not
None
:
    
register_ad_beacon
=
(
    
'
'
'
registerAdBeacon
(
{
        
'
reserved
.
top_navigation_start
'
:
        
browserSignals
.
interestGroupOwner
+
        
'
/
fenced
-
frame
/
resources
/
beacon
-
store
.
py
?
type
=
reserved
.
top_navigation_start
'
        
'
reserved
.
top_navigation_commit
'
:
        
browserSignals
.
interestGroupOwner
+
        
'
/
fenced
-
frame
/
resources
/
beacon
-
store
.
py
?
type
=
reserved
.
top_navigation_commit
'
        
'
click
'
:
        
browserSignals
.
interestGroupOwner
+
        
'
/
fenced
-
frame
/
resources
/
beacon
-
store
.
py
?
type
=
click
'
      
}
)
;
    
'
'
'
  
)
  
generate_bid
=
(
    
f
'
'
'
function
generateBid
(
      
interestGroup
      
auctionSignals
      
perBuyerSignals
      
trustedBiddingSignals
      
browserSignals
)
{
{
        
{
requested_size_check
}
        
const
ad
=
interestGroup
.
ads
[
0
]
;
        
/
/
auctionSignals
controls
whether
or
not
component
auctions
are
        
/
/
allowed
.
        
let
allowComponentAuction
=
(
typeof
auctionSignals
=
=
=
'
string
'
&
&
          
auctionSignals
.
includes
(
'
bidderAllowsComponentAuction
'
)
)
;
        
let
result
=
{
{
          
'
ad
'
:
ad
          
'
bid
'
:
1
          
'
render
'
:
{
render_obj
}
          
'
allowComponentAuction
'
:
allowComponentAuction
        
}
}
;
        
if
(
interestGroup
.
adComponents
&
&
interestGroup
.
adComponents
.
length
>
0
)
          
result
.
adComponents
=
interestGroup
.
adComponents
.
map
(
(
component
)
=
>
{
{
            
return
{
component_render_obj
}
;
          
}
}
)
;
        
return
result
;
      
}
}
    
'
'
'
  
)
  
report_win
=
(
    
f
'
'
'
function
reportWin
(
      
auctionSignals
      
perBuyerSignals
      
sellerSignals
      
browserSignals
)
{
{
        
{
register_ad_beacon
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
generate_bid
}
\
n
{
report_win
}
'
  
return
(
headers
content
)
