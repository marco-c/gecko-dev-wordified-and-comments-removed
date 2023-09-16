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
  
score_ad_content
=
'
'
  
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
score_ad_content
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
        
return
;
      
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
