from __future__ import print_function
import sys
sys.path.append("../src")
import sentiment as s

print(s.sentiment("This movie was awesome! The acting was great, plot was wonderful, and there were pythons...so yea!"))
print(s.sentiment("This movie was utter junk. There were absolutely 0 pythons. I don't see what the point was at all. Horrible movie, 0/10"))
print(s.sentiment("I crapped myself today on the bus"))
print(s.sentiment("Does Vani Like Palash"))
print(s.sentiment("AMAZING"))
