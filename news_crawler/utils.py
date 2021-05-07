import nltk


def if_tokenizer_exists():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')


def if_tagger_exists():
    try:
        nltk.data.find('tagger/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('averaged_perceptron_tagger')


def if_chunker_exists():
    try:
        nltk.data.find('chunkers/maxent_ne_chunker')
    except LookupError:
        nltk.download('maxent_ne_chunker')


def if_corpora_exists():
    try:
        nltk.data.find('corpora/words')
    except LookupError:
        nltk.download('words')
