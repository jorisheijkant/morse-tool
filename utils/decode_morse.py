# Write the code to decode the morse to text
from utils.dictionary import morse_to_text

def decode_morse(morse):
    # Parse the string, every space means a new character, every slash means a new word
    # Make an array of words, which consist of characters
    words = morse.split('/')
    print(f"Morse string consists of {len(words)} words")
    # Decode every word
    decoded_words = []
    for word in words:
        # Decode every character
        characters = word.split(' ')
        decoded_characters = []
        for character in characters:
            # Check if the character exists
            if character.strip() == '':
                continue
            if character not in morse_to_text:
                print(f"Character {character} not found in morse_to_text dictionary")
                continue
            # Decode the character
            decoded_characters.append(morse_to_text[character])
        # Decode the word
        decoded_words.append(''.join(decoded_characters))
    
    # Return the decoded string
    return ' '.join(decoded_words)
