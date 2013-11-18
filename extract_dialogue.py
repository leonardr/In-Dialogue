import re
from text.blob import TextBlob, Sentence
import sys

base_filename = sys.argv[1]
dialogue_filename = base_filename + ".dialogue"
skeleton_filename = base_filename + ".skeleton"

class GutenbergDialogueExtractor(object):

    START = re.compile("START OF THIS PROJECT GUTENBERG EBOOK[^\r]*(\r\n)*")
    END = re.compile("End of Project Gutenberg's")

    


    # SENTENCE_WITH_BEGINNING_OF_DIALOGUE = re.compile("\b'([^']|'\w)*$")
    SENTENCE_WITH_BEGINNING_OF_DIALOGUE = re.compile(r"(\b')")
    # SENTENCE_WITH_END_OF_DIALOGUE = re.compile("^([^']|'\w)*'\b")
    SENTENCE_WITH_END_OF_DIALOGUE = re.compile(r"('\b)")
    DIALOGUE_CHUNK = re.compile(r"(\W|^)('([^']|'\w)*')(\W|$)")
    NEWLINES = re.compile("(\r\n)+")

    @property
    def last_sentence(self):
        last_paragraph = self.paragraphs[-1]
        if len(last_paragraph) == 0:
            return None, None
        else:
            return last_paragraph, last_paragraph[-1]

    def __init__(self, text):

        self.dialogue_chunks = []

        start, start2 = self.START.search(text).span()
        end, end2 = self.END.search(text).span()
        text = text[start2:end]

        blob = TextBlob(text)
        self.paragraphs = [[]]
        this_paragraph = self.paragraphs[-1]
        for sentence in blob.sentences:
            sentence = str(sentence)
            paragraph_break = sentence.find('\r\n\r\n')
            if paragraph_break != -1:
                # Anything before the newlines belongs to the previous sentence.
                earlier = sentence[:paragraph_break]
                later = sentence[paragraph_break+1:]
                last_paragraph, last_sentence = self.last_sentence
                if last_sentence is None:
                    # There is no previous sentence, so this is a standalone paragraph.
                    this_paragraph.append(earlier)
                    this_paragraph = []
                    self.paragraphs.append(this_paragraph)
                else:
                    # This is part of the previous sentence.
                    last_paragraph[-1] = last_sentence + earlier
                sentence = sentence[paragraph_break:]

                # Add a new paragraph.
                self.paragraphs.append([])
                this_paragraph = self.paragraphs[-1]
            this_paragraph.append(sentence)
        self.extract()

    def extract(self):
        import pdb; pdb.set_trace()
        for paragraph in self.paragraphs:
            multi_part_dialogue = None
            for i, sentence in enumerate(paragraph):

                sentence = self.NEWLINES.sub(" ", sentence)

                if " '" in sentence:
                    import pdb; pdb.set_trace()
                if self.SENTENCE_WITH_BEGINNING_OF_DIALOGUE.match(sentence):
                    print "FIRST: %s" % sentence
                    multi_part_dialogue == [sentence]
                elif multi_part_dialogue is not None:
                    multi_part_dialogue.append(sentence)
                    if self.SENTENCE_WITH_END_OF_DIALOGUE.match(sentence):
                        print "LAST: %s" % sentence
                        self.dialogue_chunks.append(multi_part_dialogue)
                        multi_part_dialogue = None

                current_chunk = []
                def do_substitution(match):
                    a, b, c, d = match.groups()
                    current_chunk.append(b)
                    return a + "%(dialogue)s" + c + d
                paragraph[i] = self.DIALOGUE_CHUNK.sub(do_substitution, sentence)
                if len(current_chunk) > 0:
                    self.dialogue_chunks.append(current_chunk)

text = open(base_filename).read()
extractor = GutenbergDialogueExtractor(text)
extractor.extract()

import pdb; pdb.set_trace()
