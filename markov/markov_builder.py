from timeit import default_timer as timer
import markovify
import math

with open('sanitized_tweets.txt', 'r', encoding='utf-8') as f:
    text = f.read()

start = timer()
text_model = markovify.NewlineText(text)
text_model_test = markovify.NewlineText(text.split('\n')[0:10000])
end = timer()
print(f'Built markov chain in {math.floor(end - start)} seconds')

with open('markov.json', 'w', encoding='utf-8') as f:
    f.write(text_model.to_json())
with open('markov_mini.json', 'w', encoding='utf-8') as f:
    f.write(text_model_test.to_json())
