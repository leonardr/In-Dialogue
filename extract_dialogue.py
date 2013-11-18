import json
import re
import sys

class GutenbergDialogueExtractor(object):

    START = re.compile("START OF THIS PROJECT GUTENBERG EBOOK[^\r]*(\r\n)*")
    END = re.compile("End.*Project Gutenberg", re.I)


    def __init__(self, text, quote_char='"'):

        self.DIALOGUE_CHUNK = re.compile(r"(\W|^)(%s([^%s]|%s\w)*%s)(\W|$)" % (
            quote_char, quote_char, quote_char, quote_char))

        self.paragraph_templates = []
        self.dialogue_by_length = {}

        start, start2 = self.START.search(text).span()
        end, end2 = self.END.search(text, start2+2048).span()
        text = text[start2:end]

        paragraphs = text.split('\r\n\r\n')

        for para in paragraphs:
            chunks = []
            def replace(match):
                before, dialogue, ignore, after = match.groups()
                chunks.append(dialogue)
                return before + "%(dialogue)s" + after
                
            para = self.DIALOGUE_CHUNK.sub(replace, para)
            if len(chunks) > 0:
                self.dialogue_by_length.setdefault(
                    len(chunks), []).append(chunks)
            self.paragraph_templates.append(para)


for base_filename, quote in (("pg11.txt", "'"),
                             ("1727.txt", '"'),
                             ("46.txt", '"'),
                             ("pg2701.txt", '"'),
                             ):
    print base_filename
    text = open(base_filename).read()

    extractor = GutenbergDialogueExtractor(text, quote)

    dialogue_filename = base_filename + ".dialogue"
    skeleton_filename = base_filename + ".skeleton"

    json.dump(extractor.dialogue_by_length, open(dialogue_filename, "w"))
    json.dump(extractor.paragraph_templates, open(skeleton_filename, "w"))
