# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''

    print("Loading word list from file...")
    inFile = open(file_name, 'r')
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\\:;'<>?,./\"")
    return word in word_list

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object

        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.

        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]

    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)

        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled
        according to vowels_permutation. The first letter in vowels_permutation
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52
        keys of all the uppercase letters and all the lowercase letters.
        '''
        transpose = {}

        # Map lowercase vowels
        for i in range(len(VOWELS_LOWER)):
            transpose[VOWELS_LOWER[i]] = vowels_permutation[i]

        # Map uppercase vowels (keep same permutation but uppercase)
        for i in range(len(VOWELS_UPPER)):
            transpose[VOWELS_UPPER[i]] = vowels_permutation[i].upper()

        # Consonants map to themselves
        for c in CONSONANTS_LOWER:
            transpose[c] = c
        for c in CONSONANTS_UPPER:
            transpose[c] = c

        return transpose

    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary

        Returns: an encrypted version of the message text, based
        on the dictionary
        '''
        out = []
        for ch in self.message_text:
            if ch in transpose_dict:
                out.append(transpose_dict[ch])
            else:
                out.append(ch)
        return ''.join(out)

class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self, text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message.

        Returns: the best decrypted message
        '''
        best_msg = self.message_text
        best_count = 0

        for perm in get_permutations(VOWELS_LOWER):
            # To decrypt: build encryption dict for perm, then invert it
            enc_dict = self.build_transpose_dict(perm)
            dec_dict = {v: k for k, v in enc_dict.items()}

            candidate = self.apply_transpose(dec_dict)

            # Count valid words
            words = candidate.split()
            count = 0
            for w in words:
                if is_word(self.valid_words, w):
                    count += 1

            if count > best_count:
                best_count = count
                best_msg = candidate

        # If no permutation yields at least 1 valid word, return original
        if best_count == 0:
            return self.message_text
        return best_msg


if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

    # TODO: WRITE YOUR TEST CASES HERE
    # A couple quick extra tests:
    m2 = SubMessage("AEIOU aeiou")
    p2 = "uoiea"
    d2 = m2.build_transpose_dict(p2)
    e2 = m2.apply_transpose(d2)
    print("Extra test encrypt:", e2)
    print("Extra test decrypt:", EncryptedSubMessage(e2).decrypt_message())
