import json
import random

skeleton_file = "pg11.txt"
dialogue_file = "pg2701.txt"

#skeleton_file = "46.txt"
#dialogue_file = "1727.txt"

text = json.load(open(skeleton_file + ".skeleton"))
dialogue = json.load(open(dialogue_file + ".dialogue"))

class Dialogue(object):

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

        else:
            # Try a shorter one and add a single line of dialogue on
            # to the end. This may mean a recursive call.
            dialogue = self.get_dialogue(length-1) + self.get_dialogue(1)
        return dialogue

    def __getitem__(self, key):
        if self.counter is None:
            # Get a new list.
            self.dialogue = self.get_dialogue(self.key)
            self.counter = 0
        v = self.dialogue[self.counter]
        self.counter += 1
        return v


d = Dialogue(dialogue)

print "<html><head>"
print '<style>body { margin: 10px 300px 0 300px; }</style>'
print "</head>"
print "<body>"

for para in text:
    d.key = para.count("%(dialogue)s")
    para = para % d
    para  = para.replace("\n ", "<br/>\b ")
    print "<p>" + para.encode("utf8")
    print
    d.counter = None
    d.dialogue = None

print '</body>'
print "</html>"
