 
from nltk.text import Text  


from nltk import CFG
from nltk.parse.generate import generate, demo_grammar
#grammar = CFG.fromstring(demo_grammar)

test_grammar = """
  S -> NP VP
    NP -> Det N
    PP -> P NP
    VP -> 'slept'
    VP -> 'saw' NP
    VP -> 'walked' PP
    Det -> 'the'
    Det -> 'a'
    N -> 'man'
    N -> 'park'
    N -> 'dog'
    P -> 'in'
    P -> 'with'

""" #% ("with")

test_gram = ["S -> NP VP",
    "NP -> Det N",
    "PP -> P NP",
    "VP -> 'slept'",
    "VP -> 'saw' NP",
    "VP -> 'walked' PP",
    "Det -> 'the'",
    "Det -> 'a'",
    "N -> 'man'",
    "N -> 'park'",
    "N -> 'dog'",
    "P -> 'in'",
    "P -> 'with'"]
grammar = CFG.fromstring(test_gram)
# all of max depth 4
for sentence in generate(grammar, depth=4):
    print ( ' '.join(sentence))


