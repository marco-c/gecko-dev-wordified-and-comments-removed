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
TestUltraLowBandwidth
(
NetworkBandwidthTestCase
                                    
BrowserMobProxyTestCaseMixin
)
:
    
def
test_playback_limiting_bandwidth_160
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
160
}
)
        
self
.
run_videos
(
)
