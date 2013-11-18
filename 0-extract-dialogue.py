#!/usr/bin/env python
import json
import os
import re
import sys

RAW_DIR = 'raw'
COOKED_DIR = 'cooked'

class GutenbergDialogueExtractor(object):

    START = re.compile("Start[^\n]*Project Gutenberg", re.I)
    END = re.compile("End[^\n]*Project Gutenberg", re.I)

    SINGLE_QUOTE_DIALOGUE = re.compile("^'[A-Z]", re.M)
    DOUBLE_QUOTE_DIALOGUE = re.compile('^"[A-Z]', re.M)

    def __init__(self, text):

        self.paragraph_templates = []
        self.dialogue_by_length = {}

        start, start2 = self.START.search(text).span()
        end, end2 = self.END.search(text, start2+2048).span()
        text = text[start2:end]

        print (text[:80].replace("\r\n", " ").replace("\n", " "))

        # Does this text use single or double quotes to identify dialogue?
        single_count = len(self.SINGLE_QUOTE_DIALOGUE.findall(text))
        double_count = len(self.DOUBLE_QUOTE_DIALOGUE.findall(text))
        if single_count > double_count:
            print " Single quotes. (%d single, %d double)" % (single_count, double_count)
            quote_char = "'"
        else:
            print " Double quotes. (%d single, %d double)" % (single_count, double_count)
            quote_char = '"' 

        dialogue_chunk = re.compile(
            r"(\W|^)(%(q)s([^%(q)s]|%(q)s\w)*(%(q)s|$))(\W|$)" % (
                dict(q=quote_char)))

        paragraphs = text.split('\r\n\r\n')

        for para in paragraphs:
            chunks = []
            def replace(match):
                before, dialogue, ignore, ignore, after = match.groups()
                chunks.append(dialogue)
                return before + "%(dialogue)s" + after
                
            para = dialogue_chunk.sub(replace, para)
            if len(chunks) > 0:
                self.dialogue_by_length.setdefault(
                    len(chunks), []).append(chunks)
            self.paragraph_templates.append(para)

for f in sorted(os.listdir(RAW_DIR)):
    p = os.path.join(RAW_DIR, f)
    print "Processing %s" % f
    extractor = GutenbergDialogueExtractor(open(p).read())

    base_filename = os.path.split(f)[1].replace(".utf-8", '')
    dialogue_destination = os.path.join(COOKED_DIR, base_filename + ".dialogue")
    template_destination = os.path.join(COOKED_DIR, base_filename + ".template")

    json.dump(extractor.dialogue_by_length, open(dialogue_destination, "w"))
    json.dump(extractor.paragraph_templates, open(template_destination, "w"))
