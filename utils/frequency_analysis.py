import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy import stats

def frequency_analysis(signal, sampling_freq, file, plot=False, inverse=False):
    len_signal = len(signal)
    # Extract the half length
    len_half = np.ceil((len_signal + 1) / 2.0).astype(int)

    # Apply the Fourier transform
    freq_signal = np.fft.fft(signal)

    # Normalization
    freq_signal = abs(freq_signal[0:len_half]) / len_signal

    # Take the square
    freq_signal **= 2

    original_freq_signal = freq_signal

    # Extract the length of the frequency transformed signal
    len_fts = len(freq_signal)

    # Adjust the signal for even and odd cases
    if len_signal % 2:
        freq_signal[1:len_fts] *= 2
    else:
        freq_signal[1:len_fts - 1] *= 2

    # Extract the power in dB, watch out for zero division
    signal_power = 10 * np.log10(freq_signal + 1e-10)

    # Check at which frequency maximum power is present
    raw_max_power = np.max(signal_power[1:])
    max_power = int(round(np.max(signal_power[1:])))
    max_signal_index = np.where(signal_power == raw_max_power)[0][0]

    max_signal_freq = max_signal_index * sampling_freq / len_signal
    freq_range = [int(round(max_signal_freq - 10)), int(round(max_signal_freq + 10))]
    print(f"Max signal index: {max_signal_index}, max signal freq: {max_signal_freq}, signal power length {len(signal_power)}")

    # Calculate the noise floor in dB
    # Round all values in the signal power array
    signal_rounded = np.round(signal_power)
    noise_floor = stats.mode(signal_rounded)
    noise_floor = int(noise_floor[0])

    if(plot):    
        x_axis_label_divisor = len_signal / sampling_freq
        # Plot the frequency spectrum of the audio signal using matplotlib
        plt.figure(figsize=(8, 4))
        plt.plot(signal_power, color='black')
        plt.xlabel('Frequency (Hz)')
        plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{x/42:g}'))

        plt.ylabel('Amplitude')
        plt.title(f"Frequency spectrum of {file}")
        plt.grid(True)

        plt.savefig(f"{file}_frequency_spectrum.png", dpi=300, bbox_inches='tight')

    reconstructed_signal = []
    if(inverse):
        # Cut everything below the noise floor
        # TODO: Do this like here: https://www.youtube.com/watch?v=s2K1JfNR7Sc
        freq_signal = original_freq_signal
        freq_signal[signal_power < noise_floor] = 0

        reconstructed_signal = np.fft.ifft(freq_signal)

        # Normalize reconstructed signal
        reconstructed_signal = reconstructed_signal / np.power(2, 15)
        



    return {
        'max_power': max_power,
        'max_signal_freq': max_signal_freq,
        'freq_range': freq_range,
        'noise_floor': noise_floor,
        'denoised_signal': reconstructed_signal
    }