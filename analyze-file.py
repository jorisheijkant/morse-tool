# Import the libraries
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy import stats
from scipy.signal import butter, lfilter, sosfilt
from utils.frequency_analysis import frequency_analysis
from utils.morse_from_sound_profile import morse_from_sound_profile
from utils.decode_morse import decode_morse
from utils.weather_report_decoder import decode_report

audio_file = 'files/test/alphabet/alphabet.wav'
file_no_ext_with_folder = audio_file.split('.')[0]
file_no_ext = file_no_ext_with_folder.split('/')[-1]
print(f"Now analyzing {file_no_ext}...")

# Set up analysis object
analysis = {}

# Read the audio file
sampling_freq, signal = wavfile.read(audio_file)

# Check if file is mono, otherwise break
if len(signal.shape) > 1:
    print(f"File {file_no_ext} is not mono, exiting... This tool only works with mono files.")
    sys.exit()

# Normalize the values
signal = signal / np.power(2, 15)

# Extract the length of the audio signal
len_signal = len(signal)

# Convert the length to a min:sec format using the modulo operator
seconds = len_signal / sampling_freq
minutes = int(round(seconds // 60))
seconds = int(round(seconds % 60))
analysis['length (m:s)'] = f"{minutes}:{seconds}"

print(f"Doing frequency analysis wth sampling freq {sampling_freq} and signal length {len_signal}...")
frequency_information = frequency_analysis(signal, sampling_freq, file_no_ext_with_folder, True, True)
print(frequency_information)
range_to_use = frequency_information['freq_range']

# Write out the 
if(len(frequency_information['denoised_signal']) > 0):
    print(f"Has denoised signal, writing to file...")
    denoised_signal = frequency_information['denoised_signal']
    wavfile.write(f"{file_no_ext_with_folder}-denoised.wav", sampling_freq, denoised_signal.astype(np.int16))

# Cut out only the part of the signal that is in the frequency range, using a scipy butterworth filter (bandpass)
nyquist_freq = 0.5 * sampling_freq
normalized_low_freq = range_to_use[0] / nyquist_freq
normalized_high_freq = range_to_use[1] / nyquist_freq
sos = butter(10, [normalized_low_freq, normalized_high_freq], 'bandpass', output='sos')
filtered = sosfilt(sos, signal)

# Store an array of all the samples, with their time and their amplitude
samples = []
for i in range(len_signal):
    samples.append({
        'time': round(i / float(sampling_freq), 4),
        'amplitude': abs(filtered[i]),
        'db': 20 * np.log10(abs(filtered[i]) + 1e-10) if i > 0 else 0
    })

# Get the lowest and highest amplitude values
amplitude_values = [sample['amplitude'] for sample in samples]
min_amplitude = min(amplitude_values)
max_amplitude = max(amplitude_values)
most_common_amplitude = stats.mode(amplitude_values)
most_common_amplitude = most_common_amplitude[0]

print(f"Min amplitude: {min_amplitude}, max amplitude: {max_amplitude}, most common amplitude: {most_common_amplitude}")

# Calculate the noise floor
amplitude_values = [sample['amplitude'] for sample in samples]
noise_floor = np.median(amplitude_values)
std_dev = np.std(amplitude_values)

# Set the threshold to be a multiple of the standard deviation above the median
threshold_multiplier = 1.75
threshold = noise_floor + threshold_multiplier * std_dev
print(f"Noise floor: {noise_floor}, standard deviation: {std_dev}, threshold: {threshold}")
# threshold = 0.35

# Now use this list of amplitudes to measure when there is a sound and when there is silence
# A sound is defined as a period of time where the amplitude is above the threshold
# A silence is defined as a period of time where the amplitude is below the threshold

# Total samples 
total_samples = len(samples)
print(f"Total samples: {total_samples}")

# How many samples per ms are there? 
print(f"Samples per second: {sampling_freq}")

# How big groups of samples do we want to look at, making sure that each group contains the max amplitude?
# Make this dynamic, based on the frequency of the sound and the sampling frequency
group_size = int(round((sampling_freq / frequency_information['max_signal_freq']) * 4))
print(f"Group size: {group_size}")

# Chunk the array of samples into groups of the right size
sample_groups = [samples[i:i + group_size] for i in range(0, len(samples), group_size)]
print(f"Nr of sample groups: {len(sample_groups)}")

# Convert the sample groups to a single value, where we take the max amplitude of the group and the beginning time
sample_groups = [{
    'time': sample_group[0]['time'],
    'amplitude': max([sample['amplitude'] for sample in sample_group])
} for sample_group in sample_groups]

print(f"Nr of sample groups: {len(sample_groups)}")
print(f"First sample group: {sample_groups[0]}")

# Set up the sound and silence arrays
sounds = []
silences = []
# Set up the current sound and silence objects
current_sound = None
current_silence = None

# Make a rather high res plot 
plt.figure(figsize=(20, 10))
plt.plot([sample_group['time'] for sample_group in sample_groups[:800]], [sample_group['amplitude'] for sample_group in sample_groups[:800]], color='black')
# Add the threshold line as a red line
plt.axhline(y=threshold, color='red', linestyle='-')
plt.savefig(f"{file_no_ext_with_folder}-groups.png")

# Loop through all the samples
for sample in sample_groups:
    signal_here = sample['amplitude']
    time_here = sample['time']

    # If the signal is above the threshold, we are in a sound
    if signal_here > threshold:
        # If we were in a silence, we add it to the silences array
        if current_silence is not None:
            silences.append(current_silence)
            current_silence = None
        # If we are not in a sound, we are now
        if current_sound is None:
            current_sound = {
                'start': time_here,
                'end': time_here,
                'amplitude': round(signal_here, 4),
                'length': 0
            }
        # If we are already in a sound, we update the end time
        else:
            current_sound['end'] = time_here
            current_sound['length'] = round(current_sound['end'] - current_sound['start'], 4)
            current_sound['amplitude'] = max(current_sound['amplitude'], signal_here)
    # If the signal is below the threshold, we are in a silence
    else:
        # If we were in a sound, we add it to the sounds array
        if current_sound is not None:
            sounds.append(current_sound)
            current_sound = None
        # If we are not in a silence, we are now
        if current_silence is None:
            current_silence = {
                'start': time_here,
                'end': time_here,
                'amplitude': round(signal_here, 4),
                'length': 0
            }
        # If we are already in a silence, we update the end time
        else:
            current_silence['end'] = time_here
            current_silence['length'] = round(current_silence['end'] - current_silence['start'], 4)
            current_silence['amplitude'] = max(current_silence['amplitude'], signal_here)

# If we are still in a sound, we add it to the sounds array
if current_sound is not None:
    sounds.append(current_sound)
    current_sound = None

# If we are still in a silence, we add it to the silences array
if current_silence is not None:
    silences.append(current_silence)
    current_silence = None

# Add the sounds and silences to the analysis object
analysis['nr_of_sounds'] = len(sounds)
analysis['nr_of_silences'] = len(silences)

# Average length of the sounds
sound_lengths = [sound['length'] for sound in sounds]
avg_sound_length = sum(sound_lengths) / len(sound_lengths)
analysis['avg_sound_length'] = f"{avg_sound_length} seconds"

# Get the lowest and highest db values
db_values = [sample['db'] for sample in samples]
min_db = min(db_values)
max_db = max(db_values)
analysis['min_db'] = f"{min_db} db"
analysis['max_db'] = f"{max_db} db"
analysis['frequency'] = f"{frequency_information['max_signal_freq']} Hz"

morse_array = morse_from_sound_profile(sounds, silences)
analysis['morse_array'] = morse_array

print(f"Now decoding morse...")
print(f"Morse array: {morse_array}")
text = decode_morse(morse_array)
analysis['text'] = text
report = decode_report(text)
analysis['full_report'] = report
analysis['station'] = report['station']
analysis['callsign'] = report['callsign']
analysis['position'] = report['position']

# Write the analysis to a file
with open(f"{file_no_ext_with_folder}.txt", 'w') as f:
    for key, value in analysis.items():
        f.write(f"{key}: {value}\n")

print(f"Analysis of {file_no_ext} complete.")
