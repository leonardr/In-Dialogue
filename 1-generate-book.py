#!/usr/bin/env python
import json
import os
import random
import sys

COOKED_DIR = 'cooked'

class Mashup(object):

    HTML_HEADER = '''<html><head>
 <style>body { max-width: 900px; margin: 0 auto; }</style>
 <title>%(title)s</title>
 </head>
 <body>
  <h1>%(title)s</h1>'''

    HTML_FOOTER = '</body></head>'

    def __init__(self, template_file, dialogue_file, title):
        self.title = title
        template_file = os.path.join(COOKED_DIR, template_file + ".template")
        dialogue_file = os.path.join(COOKED_DIR, dialogue_file + ".dialogue")
        self.template = json.load(open(template_file))
        self.dialogue = RandomDialogue(json.load(open(dialogue_file)))
        self.paragraphs = []

        for para in self.template:
            # How many snippets do we need for this paragraph?
            size = para.count("%(dialogue)s")
            if size > 0:
                snippets = self.dialogue.get_dialogue(size)
                para = para % snippets
            self.paragraphs.append(para)

    def as_html(self):
        h = [self.HTML_HEADER % dict(title=self.title)]

        for para in self.paragraphs:
            # Maintain lines of poetry/decorations as best we can.
            para  = para.replace("\n ", "<br/>\n ")

            # Wrap in <p> tags.
            h.append("<p>%s</p>" % para)

        h.append(self.HTML_FOOTER)
        return "\n".join(h)

class RandomDialogue(object):
    """A way of getting random snippets of dialogue."""

    def __init__(self, values):
        self.all_values = values
        self.key = None
        self.counter = None

    def get_dialogue(self, length):
        k = str(length)
        if k in self.all_values and len(self.all_values[k]):
            dialogue = random.choice(self.all_values[k])
            try:
                self.all_values[k].remove(dialogue)
            except Exception, e:
                import pdb; pdb.set_trace()
            return DialogueSnippets(dialogue)
        else:
            if length == 1:
                raise Exception("No remaining dialogue choices of size 1.")
            # Try a shorter one and add a single line of dialogue on
            # to the end. This may mean a recursive call.
            dialogue = self.get_dialogue(length-1)
            dialogue.snippets += self.get_dialogue(1).snippets
            return dialogue

class DialogueSnippets(object):
    """A single paragraph's worth of dialogue, with speech breaks preserved."""

    def __init__(self, snippets):
        self.snippets = snippets
        self.counter = 0

    def __getitem__(self, key):
        v = self.snippets[self.counter]
        self.counter += 1
        return v

def usage():
    print("Usage: %s [title of work] [text source] [dialogue source]" % sys.argv[0])
    print("Available sources:")

    for fn in sorted(os.listdir(COOKED_DIR)):
        if fn.endswith(".txt.template"):
            base = fn.replace(".txt.template", "")
            if os.path.exists(os.path.join(COOKED_DIR, base + ".txt.dialogue")):
                path = os.path.join(COOKED_DIR, fn)
                data = json.load(open(path))
                sample = data[0].replace("\r\n", " ").replace("\n", " ").strip()
                print(" %s (%s)" % (base, sample))
    sys.exit()

if len(sys.argv) != 4:
    usage()
else:
    title, text, dialogue = sys.argv[1:]
    text_file = text + ".txt.template"
    dialogue_file = dialogue + ".txt.dialogue"
    if not os.path.exists(os.path.join(COOKED_DIR, text_file)):
        print("Couldn't find text for '%s'" % text)
        usage()

    if not os.path.exists(os.path.join(COOKED_DIR, dialogue_file)):
        print("Couldn't find dialogue for '%s'" % text)
        usage()

    print(Mashup(text + ".txt", dialogue + ".txt", title).as_html().encode("utf8"))
