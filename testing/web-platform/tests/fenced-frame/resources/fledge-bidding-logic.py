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
X
-
Allow
-
FLEDGE
'
'
true
'
)
  
]
  
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
  
render_obj
=
'
ad
.
renderUrl
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
renderUrl
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
renderUrl
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
renderUrl
          
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
top_navigation
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
automatic
-
beacon
-
store
.
py
'
      
}
)
;
    
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
'
'
if
ad_with_size
is
not
None
else
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
