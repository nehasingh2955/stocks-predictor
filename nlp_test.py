from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier

import re, string, random

def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

if __name__ == "__main__":

    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')
    text = twitter_samples.strings('tweets.20150430-223406.json')
    #tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]

    stop_words = stopwords.words('english')

    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')
    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                         for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                         for tweet_dict in negative_tokens_for_model]

    import json

    with open('data/training.json') as f:
      data = json.load(f)


    positive = []
    negative = []


    for d in data:
        if (str(d['sentiment']).isnumeric()):
            if d['sentiment'] == 5:
                positive.append(d['text'].lower())
            elif d['sentiment'] == 1:
                negative.append(d['text'].lower())
            else:
                if d['sentiment'] * d['sentiment:confidence'] > 2:
                    positive.append(d['text'].lower())
                else:
                    negative.append(d['text'].lower())
    
    positive_tokens = []
    negative_tokens = []
    for p in positive:
        positive_tokens.append(word_tokenize(p))
    for n in negative:
        negative_tokens.append(word_tokenize(n))
    
    positive_clean = []
    negative_clean = []
    for p in positive_tokens:
        positive_clean.append(remove_noise(p, stop_words))
    for n in negative_tokens:
        negative_clean.append(remove_noise(n, stop_words))

    positive_model = get_tweets_for_model(positive_clean)
    negative_model = get_tweets_for_model(negative_clean)

    p_dataset = [(p, "Positive")
                         for p in positive_model]

    n_dataset = [(n, "Negative")
                         for n in negative_model]


    dataset = p_dataset + n_dataset
    #dataset += positive_dataset + negative_dataset

    random.shuffle(dataset)

    with open('data/negative.json') as f:
        negative_data = json.load(f)

    with open('data/positive.json') as f:
        positive_data = json.load(f)

    negative2 = []
    positive2 = []

    for d in negative_data:
        negative2.append(d['word'].lower())
    for d in positive_data:
        positive2.append(d['word'].lower())
    
    negative2_tokens = []
    positive2_tokens = []
    
    for p in negative2:
        negative2_tokens.append(word_tokenize(p))
    for p in positive2:
        positive2_tokens.append(word_tokenize(p))
    
    negative2_model = get_tweets_for_model(negative2_tokens)
    positive2_model = get_tweets_for_model(positive2_tokens)

    
    n2_dataset = [(n, "Negative")
                         for n in negative2_model]
    p2_dataset = [(p, "Positive")
                         for p in positive2_model]

    random.shuffle(n2_dataset)

    n3 = []
    p3 = []

    f = open("data/positive.txt", "r", encoding="latin-1")
    f1 = f.readlines()
    for x in f1:
        p3.append(remove_noise(word_tokenize(x.lower()), stop_words))
    
    f = open("data/negative.txt", "r", encoding="latin-1")
    f1 = f.readlines()
    for x in f1:
        n3.append(remove_noise(word_tokenize(x.lower()), stop_words))

    n3_model = get_tweets_for_model(n3)
    p3_model = get_tweets_for_model(p3)

    n3_1 = [(n, "Negative") for n in n3_model]
    p3_1 = [(p, "Positive") for p in p3_model]


    n4 = []
    p4 = []

    f = open("data/test-positive.txt", "r", encoding="latin-1")
    f1 = f.readlines()
    for x in f1:
        p4.append(remove_noise(word_tokenize(x.lower()), stop_words))
    
    f = open("data/test-negative.txt", "r", encoding="latin-1")
    f1 = f.readlines()
    for x in f1:
        n4.append(remove_noise(word_tokenize(x.lower()), stop_words))

    n4_model = get_tweets_for_model(n4)
    p4_model = get_tweets_for_model(p4)

    n4_1 = [(n, "Negative") for n in n4_model]
    p4_1 = [(p, "Positive") for p in p4_model]

    random.shuffle(n4_1)
    random.shuffle(p4_1)
    #splitpoint = len(dataset) * 8 // 10
    #train_data = n2_dataset[:354] + p2_dataset + n3_1 + p3_1 + p_dataset + n_dataset + positive_dataset + negative_dataset
    train_data = n3_1 + p3_1 + n4_1 + p4_1
    random.shuffle(train_data)
    #test_data = dataset[splitpoint:]

    classifier = NaiveBayesClassifier.train(train_data)


    company_ticker = "FB"
    company = "lyft"

    import requests
    url = ('https://newsapi.org/v2/everything?q=' + company + '&language=en&apiKey=4ce944e3975f4c30a8f3e7ecbd542800')
    response = requests.get(url)

    json_file = response.json()

    #saves a copy of raw json file for reference
    # f = open("data/text/" + company_ticker + "/data.txt", "w")
    # f.write(str(json_file))

    titles = []
    for a in json_file['articles']:
        if company in a['title'].lower():
            titles.append(a['title'])



    positive = 0
    negative = 0


    for t in titles:
        custom_tokens = remove_noise(word_tokenize(t.lower()))
        result = classifier.classify(dict([token, True] for token in custom_tokens))
        print(t, result)
        if result == "Negative":
            negative += 1
        else:
            positive += 1
    print("pos:neg", str(positive) + ":" + str(negative))












