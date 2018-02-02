import sqlite3
import array
import sys
import numpy as np
from MulticoreTSNE import MulticoreTSNE as TSNE
# from sklearn.manifold import TSNE
import pickle


def bytes2array(b, byteformat='d', input_endianness='big'):
    system_endianness = sys.byteorder
    ar = array.array(byteformat, b)
    # If the order of bytes (endianness) assumed in the input does not match the byteorder of
    # of the current processor then reverse the byteorder of the output.
    if system_endianness == input_endianness:
        return np.array(ar)
    else:
        ar.byteswap()
        return np.array(ar)

conn = sqlite3.connect('/home/christian/go/src/bitbucket.com/chrduffau/twitter-sentiment-server/database/glove25.db')
cursor = conn.cursor()


cursor.execute("SELECT * from fasttext")
table = cursor.fetchall()
print('All words fetched.')
word_vectors = []
words = {}

for i, row in enumerate(table):
    words[row[0]] = i
    word_vectors.append(bytes2array(row[1]))
    if i % 10000 == 0:
        print('{} word vectors converted to np array.'.format(i))


word_vectors = np.array(word_vectors)

tsne_word_vectors = TSNE(n_components=2, perplexity=40, verbose=3, n_jobs=4).fit_transform(word_vectors)

np.save('tsne_word_vectors', tsne_word_vectors)

with open('word_to_index.pickle', 'wb') as file:
    pickle.dump(words, file)
