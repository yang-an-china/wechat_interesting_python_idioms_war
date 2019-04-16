# -- coding: utf-8 --

import codecs
import pickle

with codecs.open("names.txt", encoding="utf-8") as f, open("names.pickle", "wb") as pk:
    data = f.read().split(' ')
    #print(data)
    pickle.dump(data, pk)