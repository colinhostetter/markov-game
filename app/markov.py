import markovify
import os

# If not running in production, use a much smaller Markov chain that loads much faster
is_production = os.getenv('ENV') == 'production'
filename = 'markov/markov.json' if is_production else 'markov/markov_mini.json'

with open(filename, 'r') as f:
    json = f.read()
model = markovify.NewlineText.from_json(json)

__all__ = ['init_markov', 'model']
