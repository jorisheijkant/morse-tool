from morse_audio_decoder.morse import MorseCode
from pydub import AudioSegment


# Load the file
files_folder = 'files/'
file_name = 'test/cleaned-morse-mono.wav'
file_path = files_folder + file_name

# Check if the file ends with .wav. If not, convert mp3 to wav with pydub
if file_name.endswith('.mp3'):
    print('This is a mp3 file. Converting to wav...')
    sound = AudioSegment.from_mp3(file_path)
    file_path = files_folder + file_name[:-4] + '.wav'
    sound.export(file_path, format='wav')

    # Set the file_path to the new wav file
    file_path = files_folder + file_name[:-4] + '.wav'

# Check how many channels the file has
sound = AudioSegment.from_wav(file_path)
channels = sound.channels
print('Channels:', channels)

# If more than 1, convert to mono
if channels > 1:
    print('This file has more than 1 channel. Converting to mono...')
    sound = sound.set_channels(1)
    file_path = files_folder + file_name[:-4] + '-mono.wav'
    sound.export(file_path, format='wav')

    # Set the file_path to the new wav file
    file_path = files_folder + file_name[:-4] + '-mono.wav'

# Denoise the file
print('Denoising the file...')
sound = AudioSegment.from_wav(file_path)


# Decode the file
morse_code = MorseCode.from_wavfile(file_path)
print(morse_code)
out = morse_code.decode()
print(out)