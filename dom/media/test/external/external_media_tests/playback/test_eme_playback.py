from
external_media_harness
.
testcase
import
(
    
MediaTestCase
    
VideoPlaybackTestsMixin
    
EMESetupMixin
)
class
TestEMEPlayback
(
MediaTestCase
VideoPlaybackTestsMixin
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
TestEMEPlayback
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
