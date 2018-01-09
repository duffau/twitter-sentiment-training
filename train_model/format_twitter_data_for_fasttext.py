import csv

raw_file = open('../data/twitter_text.csv', 'r')
fastext_file = open('../data/fasttext_twitter_data.txt', 'w')
dict_reader = csv.DictReader(raw_file, ('created_at', 'user_name', 'followers_count', 'text'))
ft_writer = csv.writer(fastext_file)
dict_reader.__next__()

for row in dict_reader:
    text = [row['text'].replace('\n', ' ')]
    ft_writer.writerow(text)

raw_file.close()
fastext_file.close()
