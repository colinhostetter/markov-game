import re

sentence_splitter = re.compile('[\?\.\!]')
remove_tokens = [re.compile(regex) for regex in [
    '\.?[#@]\w+',      # mentions and hashtags
    'https?:\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?',       # urls
    '\w+…',        # cut off by twitter api
    '\w+@\w+\.\w+', # emails
]]
remove_characters = [re.compile(regex) for regex in [
    # non-alphabetical characters (accents are allowed which is why all this unicode stuff)
    "[^A-Za-z\u00c0-\u00d6\u00d8-\u00f6\u00f8-\u02af\u1d00-\u1d25\u1d62-\u1d65\u1d6b-\u1d77\u1d79-\u1d9a\u1e00-\u1eff\u2090-\u2094\u2184-\u2184\u2488-\u2490\u271d-\u271d\u2c60-\u2c7c\u2c7e-\u2c7f\ua722-\ua76f\ua771-\ua787\ua78b-\ua78c\ua7fb-\ua7ff\ufb00-\ufb06'’-]",
    "(?:^[-'’]+|[-'’]+$)"       # allowed, but not at beginning or end of word
]]
disallow_alone = ("'", "’", "-", "amp")

with open('raw_tweets.txt', 'r', encoding='utf-8') as f, \
     open('sanitized_tweets.txt', 'w', encoding='utf-8') as dest:
    for tweet in f:
        tokens = tweet.split(' ')

        for regex in remove_tokens:
            tokens = [t for t in tokens if not regex.match(t)]

        sentences = sentence_splitter.split(' '.join(tokens))
        for sentence in sentences:
            tokens = sentence.split(' ')
            sanitized_tokens = []

            for token in tokens:
                for regex in remove_characters:
                    token = regex.sub('', token)
                if token and token not in disallow_alone:
                    token = token.lower()
                    sanitized_tokens.append(token)

            if sanitized_tokens:
                text = ' '.join(sanitized_tokens) + "\n"
                dest.write(text)
