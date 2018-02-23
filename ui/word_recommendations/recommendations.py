from collections import deque, defaultdict


class RecommendationTree:
    def __init__(self, prefix='', number_of_recs=3):
        self.prefix = prefix
        self.words = deque(maxlen=number_of_recs)
        self.children = {}
        self.max_recs = number_of_recs

    def __str__(self):
        return '{prefix}: [{words}]'.format(prefix=self.prefix, words=', '.join(self.words))

    def insert_word(self, word):
        word = word.lower()
        if word != self.prefix:
            self.words.appendleft(word)

        if len(word) > len(self.prefix):
            # insert further if this word is not at full depth
            word_start = word[:len(self.prefix) + 1]
            next_tree = self.children.setdefault(word_start, RecommendationTree(word_start, self.max_recs))
            next_tree.insert_word(word)

    def build_tree(self, all_words):
        for word in all_words:
            self.insert_word(word)

    def lookup(self, phrase):
        phrase = phrase.lower()
        current_length = len(self.prefix)
        if len(phrase) > current_length:
            # select from a different node if necessary
            next_node = self.children.get(phrase[:current_length + 1], None)

            return next_node.lookup(phrase) if next_node is not None else []
        else:
            return list(self.words)


class RecommendationSystem:
    word_completion_file = 'ui/word_recommendations/google-10000-english-usa-no-swears.txt'
    preset_phrase_file = 'presets.txt'
    saved_words_file = 'saved_phrases.txt'
    word_mappings_file = 'word_mappings.txt'

    def __init__(self):
        self.completion_tree = RecommendationTree(number_of_recs=5)
        self.full_phrase_tree = RecommendationTree(number_of_recs=5)
        self.preset_phrases_used = defaultdict(int)
        self.saved_words_used = defaultdict(int)
        self.word_mappings = {}

        # read files into dictionaries for keeping
        self.load_preset_phrases()
        self.load_used_words()
        self.load_word_mappings()

        # build data structures for fast lookup of recommender 
        self.load_word_completion_tree()
        #self.load_full_phrase_tree()

    def get_recommendation(self, phrase, max_recommender=5):
        # get all word mappings for this exact phrase
        word_mappings = [] if phrase not in self.word_mappings else [self.word_mappings[phrase]]

        # lookup all saved phrases
        phrases = self.full_phrase_tree.lookup(phrase)

        # only look at last word for word completion
        start_loc = 0 if ' ' not in phrase else phrase.rindex(' ') + 1
        word_completions = self.completion_tree.lookup(phrase[start_loc:])

        final_list = word_mappings + phrases + word_completions
        return final_list[:max_recommender]

    def add_new_preset_phrase(self, phrase):
        self.preset_phrases_used[phrase] = 0
        self.save_preset_phrases_to_file()

    def add_new_word_mapping(self, short_form, long_form):
        self.word_mappings[short_form] = long_form
        self.save_word_mappings_to_file()

    def update_preset_phrase(self, phrase):
        self.preset_phrases_used[phrase] += 1

    def update_used_phrase(self, phrase):
        if phrase not in self.saved_words_used:
            self.full_phrase_tree.insert_word(phrase)
        self.saved_words_used[phrase] += 1

    def save_preset_phrases_to_file(self):
        self._save_dict_to_file(self.preset_phrases_used, self.preset_phrase_file)

    def save_used_words_to_file(self):
        self._save_dict_to_file(self.saved_words_used, self.saved_words_file)

    def save_word_mappings_to_file(self):
        self._save_dict_to_file(self.word_mappings, self.word_mappings_file)

    def save_all(self):
        self.save_preset_phrases_to_file()
        self.save_used_words_to_file()
        self.save_word_mappings_to_file()

    def load_word_completion_tree(self):
        # load list of most common words from file
        with open(self.word_completion_file, 'r') as f:
            word_lines = f.read()
        f.close()
        word_list = word_lines.split()

        # load reversed list in so that most common words appear first in lists
        self.completion_tree.build_tree(reversed(word_list))

    #def load_full_phrase_tree(self):
    #    all_items = self.preset_phrases_used.items() + self.saved_words_used.items()
    #    ordered_phrases = [pair[0] for pair in sorted(all_items, key=lambda p: p[1])]
    #    
    #    self.full_phrase_tree.build_tree(ordered_phrases)

    def load_preset_phrases(self):
        preset_dict = self._load_dict_from_file(self.preset_phrase_file, int)
        self.preset_phrases_used = defaultdict(int, preset_dict)

    def load_used_words(self):
        used_dict = self._load_dict_from_file(self.saved_words_file, int)
        self.saved_words_used = defaultdict(int, used_dict)

    def load_word_mappings(self):
        mapping_dict = self._load_dict_from_file(self.word_mappings_file)
        self.word_mappings = mapping_dict

    @staticmethod
    def _save_dict_to_file(lookup, filename):
        text = '\n'.join(['{key}:{val}'.format(key=k, val=v) for k, v in lookup.items()])
        with open(filename, 'w') as f:
            f.write(text)
        f.close()

    @staticmethod
    def _load_dict_from_file(filename, value_type=str):
        try:
            with open(filename, 'r') as f:
                loaded_data = f.read()
            f.close()
        except IOError:
            return {}

        return {k: value_type(v) for k, v in [line.split(':') for line in loaded_data.split('\n')]}
