import fasttext as ft

model = ft.cbow('../data/fasttext_twitter_data.txt', 'word_vector_model', silent=False)
