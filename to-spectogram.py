import wave
import numpy as np
import matplotlib.pyplot as plt

# Open the audio file
wr = wave.open('files/test/cleaned-morse.wav', 'r')

# Calculate the length of the audio file in seconds
num_frames = wr.getnframes()
frame_rate = wr.getframerate()
audio_length = num_frames / frame_rate

# Increase sz to analyze the entire audio file
sz = int(num_frames)

# Read the audio data
da = np.frombuffer(wr.readframes(sz), dtype=np.int16)
left, right = da[0::2], da[1::2]

lf = abs(np.fft.rfft(left))

plt.figure(1)
a = plt.subplot(111)  # Only one subplot for the first graph
r = 2**16/2
a.set_ylim([-r, r])
a.set_xlabel('time [s]')
a.set_ylabel('sample value [-]')
x = np.arange(sz) / frame_rate  # Use audio_length instead of 44100
plt.plot(x, left)
plt.savefig('sample-graph.png')
plt.show()  # Display the first graph

# Print the length of the audio file in seconds
print(f"Audio file length: {audio_length} seconds")
