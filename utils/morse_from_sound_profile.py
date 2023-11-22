import numpy as np

def morse_from_sound_profile(sounds, silences, correct_human_timing_errors=False):
    print(f"Reconstructing morse profile from {len(sounds)} sounds and {len(silences)} silences")
    morse_array = []
    average_sound_length = np.mean([sound['length'] for sound in sounds])

    # Combine the sounds and silences into one array, based on the start time, also add a type
    for sound in sounds:
        sound['type'] = 'sound'
    for silence in silences:
        silence['type'] = 'silence'
    sounds_and_silences = sounds + silences
    sounds_and_silences.sort(key=lambda x: x['start'])
    # Print the first 10 sounds and silences to check
    print(f"First 10 sounds and silences: {sounds_and_silences[:10]}")
    
    # Group the sounds in groups based on if they're above or below the average length
    below_average = []
    above_average = []
    for sound in sounds:
        if(sound['length'] < average_sound_length):
            below_average.append(sound)
        else:
            above_average.append(sound)

    # Reduce the groups to just the length
    below_average = [sound['length'] for sound in below_average]
    above_average = [sound['length'] for sound in above_average]

    short_sound_length = round(np.mean(below_average), 2)
    long_sound_length = round(np.mean(above_average), 2)
    print(f"Short sound length: {short_sound_length}")
    print(f"Long sound length: {long_sound_length}") 

    # Set the sound lengths
    # N.B. These are adaptive, as in that they will be recalculated after each sound
    # In this way, human timing errors should mostly be corrected for
    short_sound_minimum = round(short_sound_length / 1.5, 2)
    short_sound_maximum = round((short_sound_length + long_sound_length) / 2, 2)
    long_sound_minimum = round((long_sound_length / 1.5), 2)
    long_sound_maximum = round(long_sound_length * 1.5, 2)
    word_break_minimum = round(long_sound_length * 1.5, 2)

    print(f"Short sound minimum: {short_sound_minimum}, short sound maximum {short_sound_maximum}. Long sound length: {long_sound_length}, long sound minimum: {long_sound_minimum}, long sound maximum: {long_sound_maximum}. Word break minimum: {word_break_minimum}")

    for item in sounds_and_silences:
        if(item['type'] == 'sound'):
            if(item['length'] > short_sound_minimum and item['length'] < short_sound_maximum):
                morse_array.append(".")
                if(correct_human_timing_errors):
                    short_sound_length = round((5 * short_sound_length + item['length']) / 6, 2)
            elif item['length'] > long_sound_minimum and item['length'] < long_sound_maximum:
                morse_array.append("_")
                if(correct_human_timing_errors):
                    long_sound_length = round((5 * long_sound_length + item['length']) / 6, 2)
        elif(item['type'] == 'silence'):
            if(item['length'] < short_sound_maximum):
                morse_array.append("")
            elif(item['length'] > short_sound_maximum and item['length'] < word_break_minimum):
                morse_array.append(" ")
            elif(item['length'] > word_break_minimum):
                morse_array.append(" / ")

        # Recalculate the sound lengths
        short_sound_minimum = round(short_sound_length / 1.5, 2)
        short_sound_maximum = round((short_sound_length + long_sound_length) / 2, 2)
        long_sound_minimum = round((long_sound_length / 1.5), 2)
        long_sound_maximum = round(long_sound_length * 1.5, 2)
        word_break_minimum = round(long_sound_length * 1.5, 2)

    # Convert the array into a string
    morse_string = "".join(morse_array)

    # TODO: decode this into regular text
    return morse_string
