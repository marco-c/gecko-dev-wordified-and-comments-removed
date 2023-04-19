"
"
"
Unit
tests
for
the
signal_processing
module
.
"
"
"
import
unittest
import
numpy
as
np
import
pydub
from
.
import
exceptions
from
.
import
signal_processing
class
TestSignalProcessing
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
signal_processing
module
.
  
"
"
"
    
def
testMixSignals
(
self
)
:
        
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
        
signal
=
signal_processing
.
SignalProcessingUtils
.
GenerateWhiteNoise
(
            
silence
)
        
noise
=
signal_processing
.
SignalProcessingUtils
.
GenerateWhiteNoise
(
            
silence
)
        
signal_samples
=
signal
.
get_array_of_samples
(
)
        
noise_samples
=
noise
.
get_array_of_samples
(
)
        
mix_neg_inf
=
signal_processing
.
SignalProcessingUtils
.
MixSignals
(
            
signal
noise
-
np
.
Inf
)
        
self
.
assertTrue
(
len
(
noise
)
len
(
mix_neg_inf
)
)
        
mix_neg_inf_samples
=
mix_neg_inf
.
get_array_of_samples
(
)
        
self
.
assertTrue
(
            
all
(
[
x
=
=
y
for
x
y
in
zip
(
noise_samples
mix_neg_inf_samples
)
]
)
)
        
mix_0
=
signal_processing
.
SignalProcessingUtils
.
MixSignals
(
            
signal
noise
0
.
0
)
        
self
.
assertTrue
(
len
(
signal
)
len
(
mix_0
)
)
        
self
.
assertTrue
(
len
(
noise
)
len
(
mix_0
)
)
        
mix_0_samples
=
mix_0
.
get_array_of_samples
(
)
        
self
.
assertTrue
(
            
any
(
[
x
!
=
y
for
x
y
in
zip
(
signal_samples
mix_0_samples
)
]
)
)
        
self
.
assertTrue
(
            
any
(
[
x
!
=
y
for
x
y
in
zip
(
noise_samples
mix_0_samples
)
]
)
)
        
mix_pos_inf
=
signal_processing
.
SignalProcessingUtils
.
MixSignals
(
            
signal
noise
np
.
Inf
)
        
self
.
assertTrue
(
len
(
signal
)
len
(
mix_pos_inf
)
)
        
mix_pos_inf_samples
=
mix_pos_inf
.
get_array_of_samples
(
)
        
self
.
assertTrue
(
            
all
(
[
x
=
=
y
for
x
y
in
zip
(
signal_samples
mix_pos_inf_samples
)
]
)
)
    
def
testMixSignalsMinInfPower
(
self
)
:
        
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
        
signal
=
signal_processing
.
SignalProcessingUtils
.
GenerateWhiteNoise
(
            
silence
)
        
with
self
.
assertRaises
(
exceptions
.
SignalProcessingException
)
:
            
_
=
signal_processing
.
SignalProcessingUtils
.
MixSignals
(
                
signal
silence
0
.
0
)
        
with
self
.
assertRaises
(
exceptions
.
SignalProcessingException
)
:
            
_
=
signal_processing
.
SignalProcessingUtils
.
MixSignals
(
                
silence
signal
0
.
0
)
    
def
testMixSignalNoiseDifferentLengths
(
self
)
:
        
shorter
=
signal_processing
.
SignalProcessingUtils
.
GenerateWhiteNoise
(
            
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
8000
)
)
        
longer
=
signal_processing
.
SignalProcessingUtils
.
GenerateWhiteNoise
(
            
pydub
.
AudioSegment
.
silent
(
duration
=
2000
frame_rate
=
8000
)
)
        
mix
=
signal_processing
.
SignalProcessingUtils
.
MixSignals
(
            
signal
=
shorter
            
noise
=
longer
            
pad_noise
=
signal_processing
.
SignalProcessingUtils
.
MixPadding
.
            
NO_PADDING
)
        
self
.
assertEqual
(
len
(
shorter
)
len
(
mix
)
)
        
mix
=
signal_processing
.
SignalProcessingUtils
.
MixSignals
(
            
signal
=
shorter
            
noise
=
longer
            
pad_noise
=
signal_processing
.
SignalProcessingUtils
.
MixPadding
.
            
ZERO_PADDING
)
        
self
.
assertEqual
(
len
(
shorter
)
len
(
mix
)
)
        
mix
=
signal_processing
.
SignalProcessingUtils
.
MixSignals
(
            
signal
=
longer
            
noise
=
shorter
            
pad_noise
=
signal_processing
.
SignalProcessingUtils
.
MixPadding
.
            
NO_PADDING
)
        
self
.
assertEqual
(
len
(
shorter
)
len
(
mix
)
)
        
mix
=
signal_processing
.
SignalProcessingUtils
.
MixSignals
(
            
signal
=
longer
            
noise
=
shorter
            
pad_noise
=
signal_processing
.
SignalProcessingUtils
.
MixPadding
.
            
ZERO_PADDING
)
        
self
.
assertEqual
(
len
(
longer
)
len
(
mix
)
)
    
def
testMixSignalNoisePaddingTypes
(
self
)
:
        
shorter
=
signal_processing
.
SignalProcessingUtils
.
GenerateWhiteNoise
(
            
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
8000
)
)
        
longer
=
signal_processing
.
SignalProcessingUtils
.
GeneratePureTone
(
            
pydub
.
AudioSegment
.
silent
(
duration
=
2000
frame_rate
=
8000
)
440
.
0
)
        
mix_zero_pad
=
signal_processing
.
SignalProcessingUtils
.
MixSignals
(
            
signal
=
longer
            
noise
=
shorter
            
target_snr
=
-
6
            
pad_noise
=
signal_processing
.
SignalProcessingUtils
.
MixPadding
.
            
ZERO_PADDING
)
        
mix_loop
=
signal_processing
.
SignalProcessingUtils
.
MixSignals
(
            
signal
=
longer
            
noise
=
shorter
            
target_snr
=
-
6
            
pad_noise
=
signal_processing
.
SignalProcessingUtils
.
MixPadding
.
LOOP
)
        
def
Energy
(
signal
)
:
            
samples
=
signal_processing
.
SignalProcessingUtils
.
AudioSegmentToRawData
(
                
signal
)
.
astype
(
np
.
float32
)
            
return
np
.
sum
(
samples
*
samples
)
        
e_mix_zero_pad
=
Energy
(
mix_zero_pad
[
-
1000
:
]
)
        
e_mix_loop
=
Energy
(
mix_loop
[
-
1000
:
]
)
        
self
.
assertLess
(
0
e_mix_zero_pad
)
        
self
.
assertLess
(
e_mix_zero_pad
e_mix_loop
)
    
def
testMixSignalSnr
(
self
)
:
        
tone_low
=
signal_processing
.
SignalProcessingUtils
.
GeneratePureTone
(
            
pydub
.
AudioSegment
.
silent
(
duration
=
64
frame_rate
=
8000
)
250
.
0
)
        
tone_high
=
signal_processing
.
SignalProcessingUtils
.
GeneratePureTone
(
            
pydub
.
AudioSegment
.
silent
(
duration
=
64
frame_rate
=
8000
)
3000
.
0
)
        
def
ToneAmplitudes
(
mix
)
:
            
"
"
"
Returns
the
amplitude
of
the
coefficients
#
16
and
#
192
which
         
correspond
to
the
tones
at
250
and
3k
Hz
respectively
.
"
"
"
            
mix_fft
=
np
.
absolute
(
                
signal_processing
.
SignalProcessingUtils
.
Fft
(
mix
)
)
            
return
mix_fft
[
16
]
mix_fft
[
192
]
        
mix
=
signal_processing
.
SignalProcessingUtils
.
MixSignals
(
            
signal
=
tone_low
noise
=
tone_high
target_snr
=
-
6
)
        
ampl_low
ampl_high
=
ToneAmplitudes
(
mix
)
        
self
.
assertLess
(
ampl_low
ampl_high
)
        
mix
=
signal_processing
.
SignalProcessingUtils
.
MixSignals
(
            
signal
=
tone_high
noise
=
tone_low
target_snr
=
-
6
)
        
ampl_low
ampl_high
=
ToneAmplitudes
(
mix
)
        
self
.
assertLess
(
ampl_high
ampl_low
)
        
mix
=
signal_processing
.
SignalProcessingUtils
.
MixSignals
(
            
signal
=
tone_low
noise
=
tone_high
target_snr
=
6
)
        
ampl_low
ampl_high
=
ToneAmplitudes
(
mix
)
        
self
.
assertLess
(
ampl_high
ampl_low
)
        
mix
=
signal_processing
.
SignalProcessingUtils
.
MixSignals
(
            
signal
=
tone_high
noise
=
tone_low
target_snr
=
6
)
        
ampl_low
ampl_high
=
ToneAmplitudes
(
mix
)
        
self
.
assertLess
(
ampl_low
ampl_high
)
