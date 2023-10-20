from bs4 import BeautifulSoup
import requests
from lastfm import parse_genius
from tqdm import tqdm
import re
import pickle
from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    PER,
    NamesExtractor,

    Doc
)
def get_artist(name):
    url = f'https://genius.com/artists/{name}/songs'
    response = requests.get(url).content
    soup = BeautifulSoup(response, 'html.parser')
    soup = soup.find_all('h3')
    songs = map(lambda x: re.search('\([a-zA-Z0-9\s]+\)', x.text), soup)
    lyrics = []
    for i in songs:
        if not i:
            continue
        res = parse_genius(name, i.group()[1:-1])
        if not res:
            continue
        lyrics.append(res)
    with open('data.pickle', 'wb') as f:
        pickle.dump(lyrics, f, 'HIGHEST_PROTOCOL')
    print(lyrics)

def parse_text(txt):
    doc = Doc(txt)
    return doc.tokens

# get_artist('pornofilms')
if __name__ == "__main__":
    with open('data.pickle', 'rb') as f:
        data = pickle.load(f)
    print(parse_text(data[0]))