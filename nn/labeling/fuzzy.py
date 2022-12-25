from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from thefuzz import fuzz
from thefuzz import process
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

stop_words = stopwords.words("english")
stop_words.append(",")
stop_words.append(".")

examples = ["You should use an int in this function.",
"An int should be used inside of this function for the implementation.",
"You didnt use an int here."]

sentences = [word_tokenize(words) for words in examples]

filtered = [
    [word for word in sentence if word.casefold() not in stop_words] for sentence in sentences 
]

sentences = [[lemmatizer.lemmatize(word) for word in sentence] for sentence in filtered]

sentences = [' '.join(sentence) for sentence in filtered]


arg = "The exercise requires you to use an int in this function"
arg_words = word_tokenize(arg)
lem_arg = [lemmatizer.lemmatize(word) for word in arg_words]
print(lem_arg)
filtered_arg = [
   word for word in lem_arg if word.casefold() not in stop_words
]
processed_arg = ' '.join(filtered_arg)

print(processed_arg)
print(sentences)
res = process.extract(processed_arg, sentences)

print(res)