from
marionette_harness
import
BrowserMobProxyTestCaseMixin
from
external_media_harness
.
testcase
import
(
    
EMESetupMixin
    
NetworkBandwidthTestCase
    
NetworkBandwidthTestsMixin
)
class
TestEMEPlaybackLimitingBandwidth
(
NetworkBandwidthTestCase
                                       
BrowserMobProxyTestCaseMixin
                                       
NetworkBandwidthTestsMixin
                                       
EMESetupMixin
)
:
    
def
setUp
(
self
)
:
        
super
(
TestEMEPlaybackLimitingBandwidth
self
)
.
setUp
(
)
        
self
.
check_eme_system
(
)
