# Create a visual representation of the audio file
# Use the time as the x axis and the amplitude as the y axis

# Import the libraries
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

audio_file = 'files/test/test.wav'

# Set up the plot
plt.figure(figsize=(20, 10))
plt.title('Audio file')
plt.xlabel('Time')
plt.ylabel('Amplitude')

# Read the audio file
sampling_freq, signal = wavfile.read(audio_file)

# Normalize the values
signal = signal / np.power(2, 15)

# Extract the length of the audio signal
len_signal = len(signal)

# Extract the half length
len_half = np.ceil((len_signal + 1) / 2.0).astype(int)

# Apply the Fourier transform
freq_signal = np.fft.fft(signal)

# Normalization
freq_signal = abs(freq_signal[0:len_half]) / len_signal

# Take the square
freq_signal **= 2

# Extract the length of the frequency transformed signal
len_fts = len(freq_signal)

# Adjust the signal for even and odd cases
if len_signal % 2:
    freq_signal[1:len_fts] *= 2
else:
    freq_signal[1:len_fts - 1] *= 2

# Extract the power in dB
signal_power = 10 * np.log10(freq_signal)

# Build the X axis
x_axis = np.arange(0, len_half, 1) * (sampling_freq / len_signal) / 1000.0

# Plot the figure
plt.plot(x_axis, signal_power, color='black')

# Set the limits
plt.xlim([0, np.max(x_axis)])

# Label the axes
plt.xlabel('Frequency (kHz)')

# Display the plot
# plt.show()

# Save the plot
plt.savefig('files/test/cleaned-morse-mono.png')