import matplotlib.pyplot as plt
from numba import jit, cuda 
import pandas as pd
from sklearn.manifold import TSNE
from transformers import AutoTokenizer, AutoModel
import torch

import Dataloader as dl

# Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask

# Loads data and returns a list of sentences as specfies in Dataloader
sentences = dl.loaddata()

# Load AutoModel from huggingface model repository
tokenizer = AutoTokenizer.from_pretrained("KennethEnevoldsen/dfm-sentence-encoder-large")
model = AutoModel.from_pretrained("KennethEnevoldsen/dfm-sentence-encoder-large")

# Tokenize sentences
encoded_input = tokenizer(
    sentences, padding=True, truncation=True, max_length=128, return_tensors="pt"
)

# Compute token embeddings
with torch.no_grad():
    model_output = model(**encoded_input)

# Perform pooling. In this case, mean pooling
sentence_embeddings = mean_pooling(model_output, encoded_input["attention_mask"])

sentence_embeddings = sentence_embeddings.detach().numpy()

# Perform t-SNE
tsne = TSNE(n_components=2, random_state=0)
tsne_results = tsne.fit_transform(sentence_embeddings)

# Create a DataFrame
df = pd.DataFrame({
    'Sentence': sentences,
    'Dimension 1': tsne_results[:,0],
    'Dimension 2': tsne_results[:,1]
})

# Display the DataFrame
print(df)

# Plot the results
plt.scatter(tsne_results[:,0], tsne_results[:,1])
plt.title('t-SNE of Sentence Embeddings')
plt.xlabel('Dimension 1')
plt.ylabel('Dimension 2')
plt.show()
