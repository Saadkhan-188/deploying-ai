import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

documents = [
    "Freedom consists not in doing what we like, but in having the right to do what we ought.",
    "Those who deny freedom to others deserve it not for themselves.",
    "Liberty, when it begins to take root, is a plant of rapid growth.",
    "Freedom lies in being bold.",
    "Is freedom anything else than the right to live as we wish?",
    "I am no bird and no net ensnares me: I am a free human being with an independent will.",
    "The secret to happiness is freedom... And the secret to freedom is courage."
    "Freedom is the oxygen of the soul.", 
    "Life without liberty is like a body without spirit."
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(documents)

cosine_similarities = cosine_similarity(X)

simlarities_df = pd.DataFrame(cosine_similarities)


simlarities_df.loc[0,:].plot(kind='bar')

import matplotlib.pyplot as plt
simlarities_df.loc[0,:].plot(kind='bar')
plt.show()


# def semantic_search(query, top_k=3):
#     # Convert the query into the same TF-IDF space
#     query_vec = vectorizer.transform([query])
    
#     # Compute cosine similarity between query and all documents
#     similarities = cosine_similarity(query_vec, X).flatten()
    
#     # Get indices of top_k highest scores
#     top_indices = similarities.argsort()[::-1][:top_k]
    
#     # # Return results with scores
#     results = [(documents[i], similarities[i]) for i in top_indices]
#     return results

# results = semantic_search("What is the meaning of liberty?", top_k=3)

# for text, score in results:
#     print(f"\nScore: {score:.4f}")
#     print(text)
