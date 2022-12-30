from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch

tokenizer = AutoTokenizer.from_pretrained("neulab/codebert-java")

model = AutoModelForMaskedLM.from_pretrained("neulab/codebert-java")

input_ids = tokenizer.batch_encode_plus(["asds"], return_tensors='pt')['input_ids']
  
with torch.no_grad():
  embeddings = model(input_ids)[0]
    
print(embeddings)