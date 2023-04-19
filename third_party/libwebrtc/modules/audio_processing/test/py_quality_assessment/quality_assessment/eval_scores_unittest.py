"
"
"
Unit
tests
for
the
eval_scores
module
.
"
"
"
import
os
import
shutil
import
tempfile
import
unittest
import
pydub
from
.
import
data_access
from
.
import
eval_scores
from
.
import
eval_scores_factory
from
.
import
signal_processing
class
TestEvalScores
(
unittest
.
TestCase
)
:
    
"
"
"
Unit
tests
for
the
eval_scores
module
.
  
"
"
"
    
def
setUp
(
self
)
:
        
"
"
"
Create
temporary
output
folder
and
two
audio
track
files
.
"
"
"
        
self
.
_output_path
=
tempfile
.
mkdtemp
(
)
        
silence
=
pydub
.
AudioSegment
.
silent
(
duration
=
1000
frame_rate
=
48000
)
        
fake_reference_signal
=
(
signal_processing
.
SignalProcessingUtils
.
                                 
GenerateWhiteNoise
(
silence
)
)
        
fake_tested_signal
=
(
signal_processing
.
SignalProcessingUtils
.
                              
GenerateWhiteNoise
(
silence
)
)
        
self
.
_fake_reference_signal_filepath
=
os
.
path
.
join
(
            
self
.
_output_path
'
fake_ref
.
wav
'
)
        
signal_processing
.
SignalProcessingUtils
.
SaveWav
(
            
self
.
_fake_reference_signal_filepath
fake_reference_signal
)
        
self
.
_fake_tested_signal_filepath
=
os
.
path
.
join
(
            
self
.
_output_path
'
fake_test
.
wav
'
)
        
signal_processing
.
SignalProcessingUtils
.
SaveWav
(
            
self
.
_fake_tested_signal_filepath
fake_tested_signal
)
    
def
tearDown
(
self
)
:
        
"
"
"
Recursively
delete
temporary
folder
.
"
"
"
        
shutil
.
rmtree
(
self
.
_output_path
)
    
def
testRegisteredClasses
(
self
)
:
        
exceptions
=
[
'
thd
'
'
echo_metric
'
]
        
self
.
assertTrue
(
os
.
path
.
exists
(
self
.
_output_path
)
)
        
registered_classes
=
eval_scores
.
EvaluationScore
.
REGISTERED_CLASSES
        
self
.
assertIsInstance
(
registered_classes
dict
)
        
self
.
assertGreater
(
len
(
registered_classes
)
0
)
        
eval_score_workers_factory
=
(
            
eval_scores_factory
.
EvaluationScoreWorkerFactory
(
                
polqa_tool_bin_path
=
os
.
path
.
join
(
                    
os
.
path
.
dirname
(
os
.
path
.
abspath
(
__file__
)
)
'
fake_polqa
'
)
                
echo_metric_tool_bin_path
=
None
)
)
        
eval_score_workers_factory
.
SetScoreFilenamePrefix
(
'
scores
-
'
)
        
for
eval_score_name
in
registered_classes
:
            
if
eval_score_name
in
exceptions
:
                
continue
            
eval_score_worker
=
eval_score_workers_factory
.
GetInstance
(
                
registered_classes
[
eval_score_name
]
)
            
eval_score_worker
.
SetReferenceSignalFilepath
(
                
self
.
_fake_reference_signal_filepath
)
            
eval_score_worker
.
SetTestedSignalFilepath
(
                
self
.
_fake_tested_signal_filepath
)
            
eval_score_worker
.
Run
(
self
.
_output_path
)
            
score
=
data_access
.
ScoreFile
.
Load
(
                
eval_score_worker
.
output_filepath
)
            
self
.
assertTrue
(
isinstance
(
score
float
)
)
    
def
testTotalHarmonicDistorsionScore
(
self
)
:
        
pure_tone_freq
=
5000
.
0
        
eval_score_worker
=
eval_scores
.
TotalHarmonicDistorsionScore
(
'
scores
-
'
)
        
eval_score_worker
.
SetInputSignalMetadata
(
{
            
'
signal
'
:
            
'
pure_tone
'
            
'
frequency
'
:
            
pure_tone_freq
            
'
test_data_gen_name
'
:
            
'
identity
'
            
'
test_data_gen_config
'
:
            
'
default
'
        
}
)
        
template
=
pydub
.
AudioSegment
.
silent
(
duration
=
1000
frame_rate
=
48000
)
        
pure_tone
=
signal_processing
.
SignalProcessingUtils
.
GeneratePureTone
(
            
template
pure_tone_freq
)
        
white_noise
=
signal_processing
.
SignalProcessingUtils
.
GenerateWhiteNoise
(
            
template
)
        
noisy_tone
=
signal_processing
.
SignalProcessingUtils
.
MixSignals
(
            
pure_tone
white_noise
)
        
scores
=
[
None
None
None
]
        
for
index
tested_signal
in
enumerate
(
            
[
pure_tone
noisy_tone
white_noise
]
)
:
            
tmp_filepath
=
os
.
path
.
join
(
self
.
_output_path
'
tmp_thd
.
wav
'
)
            
signal_processing
.
SignalProcessingUtils
.
SaveWav
(
                
tmp_filepath
tested_signal
)
            
eval_score_worker
.
SetTestedSignalFilepath
(
tmp_filepath
)
            
eval_score_worker
.
Run
(
self
.
_output_path
)
            
scores
[
index
]
=
eval_score_worker
.
score
            
os
.
remove
(
eval_score_worker
.
output_filepath
)
        
self
.
assertTrue
(
all
(
[
scores
[
i
+
1
]
>
scores
[
i
]
for
i
in
range
(
2
)
]
)
)
