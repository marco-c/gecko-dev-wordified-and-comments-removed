from
.
charsetgroupprober
import
CharSetGroupProber
from
.
hebrewprober
import
HebrewProber
from
.
langbulgarianmodel
import
(
ISO_8859_5_BULGARIAN_MODEL
                                 
WINDOWS_1251_BULGARIAN_MODEL
)
from
.
langgreekmodel
import
ISO_8859_7_GREEK_MODEL
WINDOWS_1253_GREEK_MODEL
from
.
langhebrewmodel
import
WINDOWS_1255_HEBREW_MODEL
from
.
langrussianmodel
import
(
IBM855_RUSSIAN_MODEL
IBM866_RUSSIAN_MODEL
                               
ISO_8859_5_RUSSIAN_MODEL
KOI8_R_RUSSIAN_MODEL
                               
MACCYRILLIC_RUSSIAN_MODEL
                               
WINDOWS_1251_RUSSIAN_MODEL
)
from
.
langthaimodel
import
TIS_620_THAI_MODEL
from
.
langturkishmodel
import
ISO_8859_9_TURKISH_MODEL
from
.
sbcharsetprober
import
SingleByteCharSetProber
class
SBCSGroupProber
(
CharSetGroupProber
)
:
    
def
__init__
(
self
)
:
        
super
(
SBCSGroupProber
self
)
.
__init__
(
)
        
hebrew_prober
=
HebrewProber
(
)
        
logical_hebrew_prober
=
SingleByteCharSetProber
(
WINDOWS_1255_HEBREW_MODEL
                                                        
False
hebrew_prober
)
        
visual_hebrew_prober
=
SingleByteCharSetProber
(
WINDOWS_1255_HEBREW_MODEL
                                                       
True
hebrew_prober
)
        
hebrew_prober
.
set_model_probers
(
logical_hebrew_prober
                                        
visual_hebrew_prober
)
        
self
.
probers
=
[
            
SingleByteCharSetProber
(
WINDOWS_1251_RUSSIAN_MODEL
)
            
SingleByteCharSetProber
(
KOI8_R_RUSSIAN_MODEL
)
            
SingleByteCharSetProber
(
ISO_8859_5_RUSSIAN_MODEL
)
            
SingleByteCharSetProber
(
MACCYRILLIC_RUSSIAN_MODEL
)
            
SingleByteCharSetProber
(
IBM866_RUSSIAN_MODEL
)
            
SingleByteCharSetProber
(
IBM855_RUSSIAN_MODEL
)
            
SingleByteCharSetProber
(
ISO_8859_7_GREEK_MODEL
)
            
SingleByteCharSetProber
(
WINDOWS_1253_GREEK_MODEL
)
            
SingleByteCharSetProber
(
ISO_8859_5_BULGARIAN_MODEL
)
            
SingleByteCharSetProber
(
WINDOWS_1251_BULGARIAN_MODEL
)
            
SingleByteCharSetProber
(
TIS_620_THAI_MODEL
)
            
SingleByteCharSetProber
(
ISO_8859_9_TURKISH_MODEL
)
            
hebrew_prober
            
logical_hebrew_prober
            
visual_hebrew_prober
        
]
        
self
.
reset
(
)
