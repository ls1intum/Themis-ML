from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

input = "Instead of using a double, you should have used an int."

examples = ["You should use an int in this function.",
"An int should be used inside of this function for the implementation.",
"You didnt use an int here.",
"You could have used the ternary operator here."
]

examples.append(input)

vect = TfidfVectorizer(min_df=1, stop_words="english")
tfidf = vect.fit_transform(examples)
pairwise_similarity = tfidf * tfidf.T
arr = pairwise_similarity.toarray()
np.fill_diagonal(arr, np.nan)

input_id = examples.index(input)
id = np.nanargmax(arr[input_id])
print(examples[id])