import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords.words("russian")
import re
import spacy
import ru_core_news_lg
nlp = ru_core_news_lg.load()
stop_words=stopwords.words("russian")
def preprocess(df):
    for i in range(len(df)):
        df['industries'][i] = re.sub(r'(?:[^\w\s]|_)+', ' ', df['industries'][i])
        df['about'][i] = re.sub(r'(?:[^\w\s]|_)+', ' ', df['about'][i])
        df['about'][i] =' '.join(df['about'][i].split()) 
        for item in range(len(df['refs'][i])):
            df['refs'][i][item] = re.sub(r'(?:[^\w\s]|_)+', ' ', df['refs'][i][item])
            df['refs'][i][item] =' '.join(df['refs'][i][item].split()) 
    for i in range(len(df)):

        filtered_industries=[]
        filtered_about = []
        

    
        tokenize_industries = nlp(df['industries'][i])
        for token in tokenize_industries:
            if token.lemma_ not in stop_words:
                filtered_industries.append(token.lemma_)
        df['industries'][i]=filtered_industries       
        tokenize_about = nlp(df['about'][i])
        for token in tokenize_about:
            if token.lemma_ not in stop_words:
                filtered_about.append(token.lemma_)
        df['about'][i] = filtered_about
        for item in range(len(df['refs'][i])):
            filtered_refs = []
            tokenize_refs = nlp(df['refs'][i][item])
            for token in tokenize_refs:
                if token.lemma_ not in stop_words:
                    filtered_refs.append(token.lemma_)
            df['refs'][i][item] = filtered_refs        
            
                    