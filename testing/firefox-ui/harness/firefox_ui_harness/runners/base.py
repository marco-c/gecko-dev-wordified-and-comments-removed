from
__future__
import
absolute_import
import
os
from
marionette_harness
import
BaseMarionetteTestRunner
MarionetteTestCase
class
FirefoxUITestRunner
(
BaseMarionetteTestRunner
)
:
    
def
__init__
(
self
*
*
kwargs
)
:
        
super
(
FirefoxUITestRunner
self
)
.
__init__
(
*
*
kwargs
)
        
self
.
app
=
"
fxdesktop
"
        
moz_log
=
"
"
        
if
"
MOZ_LOG
"
in
os
.
environ
:
            
moz_log
=
os
.
environ
[
"
MOZ_LOG
"
]
        
if
len
(
moz_log
)
>
0
:
            
moz_log
+
=
"
"
        
moz_log
+
=
"
UrlClassifierStreamUpdater
:
1
"
        
os
.
environ
[
"
MOZ_LOG
"
]
=
moz_log
        
self
.
test_handlers
=
[
MarionetteTestCase
]
