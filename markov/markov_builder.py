from timeit import default_timer as timer
import json
import markovify
import math

with open('markov/sanitized_tweets.txt', 'r', encoding='utf-8') as f:
    text = f.read()

start = timer()
text_model = markovify.NewlineText(text)
text_model_test = markovify.NewlineText(text.split('\n')[0:10000])
end = timer()
print(f'Built markov chain in {math.floor(end - start)} seconds')

with open('markov/markov.json', 'w', encoding='utf-8') as f:
    model_dict = text_model.to_dict()
    json.dump(model_dict, f)
with open('markov/markov_mini.json', 'w', encoding='utf-8') as f:
    model_dict = text_model_test.to_dict()
    json.dump(model_dict, f)
