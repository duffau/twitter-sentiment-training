import pickle
import numpy as np
import matplotlib.pyplot as plt

with open('word_to_index.pickle', 'rb') as file:
    words = pickle.load(file)

tsne_word_vectors = np.load('tsne_word_vectors.npy')

plot_words = ['man', 'woman', 'king', 'queen']
# plot_words = ['good', 'bad', 'love', 'hate', 'strong', 'weak']
# plot_words = ['btc', 'eth', 'usd', 'eur']
plot_words = [(words.get(word, None), word) for word in plot_words if words.get(word, None)]
plot_indices = [i for i, w in plot_words]
print(plot_indices)
print(tsne_word_vectors[plot_indices, :])
plt.plot(tsne_word_vectors[plot_indices, 0], tsne_word_vectors[plot_indices, 1], '.')

for i, w in plot_words:
    x = tsne_word_vectors[i, 0]
    y = tsne_word_vectors[i, 1]
    plt.text(x, y, w)

plt.savefig('words_vectors.png')