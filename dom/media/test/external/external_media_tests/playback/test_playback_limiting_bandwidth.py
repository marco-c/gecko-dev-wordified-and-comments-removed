from
marionette
import
BrowserMobProxyTestCaseMixin
from
external_media_harness
.
testcase
import
NetworkBandwidthTestCase
class
TestPlaybackLimitingBandwidth
(
NetworkBandwidthTestCase
                                    
BrowserMobProxyTestCaseMixin
)
:
    
def
test_playback_limiting_bandwidth_250
(
self
)
:
        
self
.
proxy
.
limits
(
{
'
downstream_kbps
'
:
250
}
)
        
self
.
run_videos
(
)
    
def
test_playback_limiting_bandwidth_500
(
self
)
:
        
self
.
proxy
.
limits
(
{
'
downstream_kbps
'
:
500
}
)
        
self
.
run_videos
(
)
    
def
test_playback_limiting_bandwidth_1000
(
self
)
:
        
self
.
proxy
.
limits
(
{
'
downstream_kbps
'
:
1000
}
)
        
self
.
run_videos
(
)
