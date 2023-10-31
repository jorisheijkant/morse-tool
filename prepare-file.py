import numpy as np
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range

# Load the file
files_folder = 'files/test/test-6/'
file_name = 'test-6.mp3'
file_path = files_folder + file_name

sound = False

# Check if the file ends with .wav. If not, convert mp3 to wav with pydub
if file_name.endswith('.mp3'):
    print('This is a mp3 file. Converting to wav...')
    sound = AudioSegment.from_mp3(file_path)
    file_path = files_folder + file_name[:-4] + '.wav'
elif file_name.endswith('.wav'):
    print('This is a wav file. No conversion needed.')
    sound = AudioSegment.from_wav(file_path)

# Check how many channels the file has
channels = sound.channels
print('Channels:', channels)

if channels > 1:
    print('This file has more than 1 channel. Converting to mono...')
    sound = sound.set_channels(1)

# Denoise the file
print('Normalizing/denoising the file...')

# Normalize the audio
sound = normalize(sound)

# Apply a gate compressor to the audio
# sound = compress_dynamic_range(sound, threshold=-30.0, ratio=10.0, attack=0.1, release=50)

if(sound):
    new_file_path = files_folder + file_name[:-4] + '.wav'
    sound.export(new_file_path, format='wav')