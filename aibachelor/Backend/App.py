from typing import Any, Callable, Dict
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as torch
import Helper.Dataloader as dl, Helper.Embedding as emb, Helper.excelwriter as ew, Helper.ModelLoader as ml
from Helper.ModelAsker import ModelAsker
from Helper.ModelLoader import ModelLoader as myml
from milvus import default_server
from pymilvus import connections
from enum import Enum
from sentence_transformers import SentenceTransformer

class ModelType(Enum):
    AUTO = 'Auto'
    GPT2 = 'GPT2'
    BERT = 'BERT'

class embeddingModel(Enum):
    # 4096 dim
    E5Mistral7B = 'e5mistral7b'
    # i dont know the dim
    QAEmbeddings = 'qa_embeddings'
    # 1024 dim
    E5Large = 'e5Large'

class ModelName(Enum):
    MULTILINGUAL_E5_LARGE = 'intfloat/multilingual-e5-large'
    DFM_SENTENCE_ENCODER_LARGE = 'KennethEnevoldsen/dfm-sentence-encoder-large'
    GPT2 = 'gpt2'
    BERT_LARGE_UNCASED_WHOLE_WORD_MASKING_FINETUNED_SQUAD = 'bert-large-uncased-whole-word-masking-finetuned-squad'
    E5_MISTRAL_7B_INSTRUCT = 'intfloat/e5-mistral-7b-instruct'

connections.connect(host='localhost', port=default_server.listen_port)

loader = myml(ModelType.GPT2.value, ModelName.GPT2.value)
model, tokenizer = loader.load()

app = Flask(__name__)
CORS(app)

em: str = embeddingModel.E5Large.value

llama_asker = ModelAsker("llama3-8b-8192", em)
mixtral_asker = ModelAsker("mixtral-8x7b-32768", em)
google_asker = ModelAsker("gemma-7b-it", em)
gtp2_asker = ModelAsker("gpt2", em)


def ask_model(asker, question, model, tokenizer, with_context):
    return asker.ask(question, model, tokenizer, with_context)


@app.route('/answer', methods=['POST'])#
def get_answer():
    question: str = request.json['question']
    method: str = request.json['method']  # Assuming method is specified in the request
    # Call the appropriate method based on the dropdown selection

    methods: Dict[str, Callable[[str, Any, Any], Any]] = {
       #'GPT2': lambda question, model, tokenizer: ask_gpt2(question, model, tokenizer),
       #'GROG': grogmethod1,
       'LLAMA': lambda question, model, tokenizer: ask_model(llama_asker, question, model, tokenizer, True),
       'LLAMANOCONTEXT': lambda question, model, tokenizer: ask_model(llama_asker, question, model, tokenizer, False),
       'MIXTRAL': lambda question, model, tokenizer: ask_model(mixtral_asker, question, model, tokenizer, True),
       'MIXTRALNOCONTEXT': lambda question, model, tokenizer: ask_model(mixtral_asker, question, model, tokenizer, False),
       'GOOGLE': lambda question, model, tokenizer: ask_model(google_asker, question, model, tokenizer, True),
       'GOOGLENOCONTEXT': lambda question, model, tokenizer: ask_model(google_asker, question, model, tokenizer, False),
    }

    if method in methods:
        answer = methods[method](question, model, tokenizer)
        sender = "bot"
    else:
        answer = "Invalid method selected"
        sender = "bot"

    return jsonify({'answer': answer, 'sender': sender})

def create_embeddings(tokenizer, model, emodel: str) -> str:
    data = dl.loaddataQAPairs
    emb.insertEmbeddings(tokenizer, model, emodel, data)
    return "Embeddings created"


# def method2(question, context):
#     context = dl.loaddataQAstring()
#     max_score = -float('inf')
#     best_answer = None
#     # Iterate over each possible answer in the context
#     for context in context:
#         # Prepare the inputs for the BERT model
#         inputs = tokenizerBERT.encode_plus(question, context, max_length=512, truncation=True, padding='max_length', return_tensors="pt")
#         # Pass the inputs to the BERT model
#         outputs = modelBERT(**inputs)
#         answer_start_scores, answer_end_scores = outputs.start_logits, outputs.end_logits
#         # Get the most likely start and end of the answer
#         answer_start = torch.argmax(answer_start_scores)
#         answer_end = torch.argmax(answer_end_scores) + 1
#         if answer_start.item() == 0 or answer_end.item() == 0:
#             continue
#         if inputs["input_ids"][0][answer_start] == tokenizerBERT.sep_token_id or inputs["input_ids"][0][answer_end - 1] == tokenizerBERT.sep_token_id:
#             continue
        
#         # Calculate the total score for this answer
#         total_score = answer_start_scores[0, answer_start].item() + answer_end_scores[0, answer_end - 1].item()
#         # If this score is higher than the previous best, update the best answer
#         if total_score > max_score:
#             max_score = total_score
#             # Convert the answer from token IDs to a string
#             best_answer = tokenizerBERT.convert_tokens_to_string(tokenizerBERT.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end]))
#     return best_answer

# def grogmethod1(question):
#     chat_completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": question,
#             }
#         ],
#         model="mixtral-8x7b-32768",
#         temperature=0.5,
#         max_tokens=1024,
#         top_p=1,
#         stop=None,
#         stream=False,
#     )

#     return chat_completion.choices[0].message.content

# def ask_gpt2(question, model, tokenizer):
#     inputs = tokenizer.encode_plus(question, return_tensors="pt")
#     outputs = model.generate(
#         input_ids=inputs["input_ids"], 
#         attention_mask=inputs["attention_mask"],
#         max_length=100, 
#         num_return_sequences=1,  # Generate 5 different sequences
#         temperature=0.8,
#         pad_token_id=tokenizer.eos_token_id,
#         do_sample=True  # Use probabilistic decoding
#     )
#     answer = tokenizer.decode(outputs[0])
#     return answer

if __name__ == '__main__':
    app.run(debug=True)