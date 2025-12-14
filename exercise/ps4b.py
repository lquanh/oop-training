# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    '''
    print("Loading word list from file...")
    with open(file_name, 'r') as inFile:
        wordlist = []
        for line in inFile:
            # IMPORTANT: split() (không truyền đối số) sẽ tự xử lý whitespace + \n
            wordlist.extend([word.lower() for word in line.split()])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation
    '''
    word = word.lower()
    # strip thêm whitespace như \n \t \r để an toàn
    word = word.strip(" \t\n\r" + " !@#$%^&*()-_+={}[]|\\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    with open("story.txt", "r") as f:
        return str(f.read())

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        return self.message_text

    def get_valid_words(self):
        return self.valid_words[:]

    def build_shift_dict(self, shift):
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        sl = lower[shift:] + lower[:shift]
        su = upper[shift:] + upper[:shift]
        res = {}
        for i in range(26):
            res[lower[i]] = sl[i]
            res[upper[i]] = su[i]
        return res

    def apply_shift(self, shift):
        shift_dict = self.build_shift_dict(shift)
        encrypted = []
        for ch in self.message_text:
            encrypted.append(shift_dict.get(ch, ch))
        return ''.join(encrypted)

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        super().__init__(text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        return self.shift

    def get_encryption_dict(self):
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        return self.message_text_encrypted

    def change_shift(self, shift):
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

class CiphertextMessage(Message):
    def __init__(self, text):
        super().__init__(text)

    def decrypt_message(self):
        best_shift = 0
        best_count = -1
        best_decryption = self.message_text

        for shift in range(26):
            decrypted_text = self.apply_shift(shift)
            words = decrypted_text.split()
            count_valid = 0
            for w in words:
                if is_word(self.valid_words, w):
                    count_valid += 1

            if count_valid > best_count:
                best_count = count_valid
                best_shift = shift
                best_decryption = decrypted_text

        return (best_shift, best_decryption)

if __name__ == '__main__':
    # Example test case (PlaintextMessage)
    plaintext = PlaintextMessage('hello', 2)
    print('Plaintext test:')
    print('Expected Output: jgnnq')
    print('Actual Output:  ', plaintext.get_message_text_encrypted())
    print()

    # Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    print('Ciphertext test:')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output: ', ciphertext.decrypt_message())
    print()

    # Your own tests
    plaintext2 = PlaintextMessage('This is a test message!', 5)
    print('Plaintext2 encrypted:', plaintext2.get_message_text_encrypted())

    ciphertext2 = CiphertextMessage(plaintext2.get_message_text_encrypted())
    print('Ciphertext2 decrypted:', ciphertext2.decrypt_message())

    # Decrypt the story
    story_cipher = CiphertextMessage(get_story_string())
    best_shift, decrypted_story = story_cipher.decrypt_message()
    print('\nBest shift for story:', best_shift)
    print('Decrypted story:')
    print(decrypted_story)
