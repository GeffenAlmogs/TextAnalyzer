STRING_PUNCTUATION = "!”#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
READ_MODE = 'r'
CSV_ENCODING_MODE = 'utf-8'

class SentencesProcessor:
    def __init__(self, sentences_list: list[str], unwanted_words: set[str] = set()):
        self.sentences_list : list[str] = sentences_list
        self.processed_sentences : list[list[str]] = []
        self.unwanted_words = unwanted_words



    def convert_sentences_to_lowercase(self):
        """
        Converts all sentences in the 'sentences_list' to lowercase.
        """
        self.sentences_list = [sentence.lower() for sentence in self.sentences_list]



    def remove_unwanted_words_from_sentences(self):
        """
        Removes unwanted words from each sentence in 'sentences_list'.
        """
        sentences_without_unwanted_words = []
        for sentence in self.sentences_list:
            cleaned_sentence = self.remove_words_from_sentence(sentence)
            sentences_without_unwanted_words.append(cleaned_sentence)
        self.sentences_list = sentences_without_unwanted_words



    def clean_string_punctuation_from_sentences(self):
        """
        Removes punctuation from each sentence in 'sentences_list'.
        """
        clean_sentences = []
        for sentence in self.sentences_list:
            cleaned_sentence = self.remove_punctuation_from_sentence(sentence)
            clean_sentences.append(cleaned_sentence)
        self.sentences_list = clean_sentences



    def remove_repeating_whitespaces_from_sentences(self):
        """
        Removes repeating whitespaces from each sentence in 'sentences_list'.
        """
        self.sentences_list = [' '.join(sentence.split()) for sentence in self.sentences_list]



    def remove_empty_sentences(self):
        """
        Removes empty sentences from 'sentences_list'.
        """
        self.sentences_list = [line for line in self.sentences_list if line != '']



    def split_sentences_into_processed_sentences(self):
        """
        Splits each sentence in 'sentences_list' into a list of words.
        """
        self.processed_sentences = [sentence.split(' ') for sentence in self.sentences_list]



    def remove_words_from_sentence(self, sentence: str) -> str:
        """
        Removes unwanted words from a given sentence.
        """
        return ' '.join([word for word in sentence.split(' ') if not word in self.unwanted_words])



    def remove_punctuation_from_sentence(self, sentence: str) -> str:
        """
        Removes punctuation from a given sentence.

        Parameters:
        sentence (str): The sentence to be cleaned.

        Returns:
        str: The cleaned sentence with punctuation removed and replaced by spaces.
        """
        
        cleaned_sentence = ''
        for char in sentence:
            if char in STRING_PUNCTUATION:
                cleaned_sentence += ' '  # Replace punctuation with space
            elif char.isalnum() or char.isspace(): # Keep alphanumeric characters and spaces
                cleaned_sentence += char
        return cleaned_sentence



    def process_sentences(self) -> list[list[str]]:
        # Perform the processing steps
        self.convert_sentences_to_lowercase()
        self.clean_string_punctuation_from_sentences()
        self.remove_repeating_whitespaces_from_sentences()
        self.remove_unwanted_words_from_sentences()
        self.remove_empty_sentences()
        self.split_sentences_into_processed_sentences()
        return self.processed_sentences