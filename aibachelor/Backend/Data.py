from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import numpy as np
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, RagTokenizer, RagSequenceForGeneration, RagRetriever, BertForQuestionAnswering, BertTokenizer, AutoTokenizer, AutoModel
import Dataloader as dl
import Embedding as emb
import excelwriter as ew
from milvus import default_server
from pymilvus import connections, utility, MilvusException
from sentence_transformers import SentenceTransformer

connections.connect(host='localhost', port=default_server.listen_port)
#4096 dim
#embeddingModel = "e5mistral7b"
#i dont know the dim
#embeddingModel = "qa_embeddings"
#1024 dim
embeddingModel = "e5Large"



try: 
    collection = utility.list_collections()
    print(collection)
except MilvusException as e:
    print(e)


client = Groq(
    api_key="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",
)

# tokenizer = AutoTokenizer.from_pretrained("KennethEnevoldsen/dfm-sentence-encoder-large")
# model = AutoModel.from_pretrained("KennethEnevoldsen/dfm-sentence-encoder-large")

# tokenizerGPT2 = GPT2Tokenizer.from_pretrained("gpt2")
# modelGPT2 = GPT2LMHeadModel.from_pretrained("gpt2")

# tokenizerBERT = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
# modelBERT = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

# tokenizer = AutoTokenizer.from_pretrained('intfloat/e5-mistral-7b-instruct')
# model = AutoModel.from_pretrained('intfloat/e5-mistral-7b-instruct')

tokenizer = AutoTokenizer.from_pretrained('intfloat/multilingual-e5-large')
model = AutoModel.from_pretrained('intfloat/multilingual-e5-large')

#context = dl.loaddata()

app = Flask(__name__)
CORS(app)
context = dl.loaddataQAPairs()


@app.route('/answer', methods=['POST'])#
def get_answer():
    question = request.json['question']
    method = request.json['method']  # Assuming method is specified in the request
    # Call the appropriate method based on the dropdown selection

    if method == 'GPT2':
        answer = ask_gpt2(question)
        sender = "bot"
    elif method == 'BERT':
        answer = method2(question, context)
        sender = "bot"
    elif method == 'GROG':
        answer = grogmethod1(question)
        sender = "bot"
    elif method == 'LLAMA':
        answer = askllama(question)
        sender = "bot"
    elif method == 'LLAMANOCONTEXT':
        answer = askllamaNoContext(question)
        sender = "bot"
    elif method == 'MIXTRAL':
        answer = askmixtral(question)
        sender = "bot"
    elif method == 'MIXTRALNOCONTEXT':
        answer = askmixtralNoContext(question)
        sender = "bot"
    elif method == 'GOOGLE':
        answer = askgoogle(question)
        sender = "bot"
    elif method == 'GOOGLENOCONTEXT':
        answer = askgoogleNoContext(question)
        sender = "bot"
    else:
        answer = "Invalid method selected"
        sender = "bot"
    
    return jsonify({'answer': answer, 'sender': sender})


def ask_gpt2(question):
    inputs = tokenizerGPT2.encode_plus(question, return_tensors="pt")
    outputs = modelGPT2.generate(
        input_ids=inputs["input_ids"], 
        attention_mask=inputs["attention_mask"],
        max_length=100, 
        num_return_sequences=1,  # Generate 5 different sequences
        temperature=0.8,
        pad_token_id=tokenizerGPT2.eos_token_id,
        do_sample=True  # Use probabilistic decoding
    )
    answer = tokenizerGPT2.decode(outputs[0])
    return answer


def method2(question, context):
    context = dl.loaddataQAstring()
    max_score = -float('inf')
    best_answer = None

    # Iterate over each possible answer in the context
    for context in context:
        # Prepare the inputs for the BERT model
        inputs = tokenizerBERT.encode_plus(question, context, max_length=512, truncation=True, padding='max_length', return_tensors="pt")

        # Pass the inputs to the BERT model
        outputs = modelBERT(**inputs)
        answer_start_scores, answer_end_scores = outputs.start_logits, outputs.end_logits

        # Get the most likely start and end of the answer
        answer_start = torch.argmax(answer_start_scores)
        answer_end = torch.argmax(answer_end_scores) + 1

        if answer_start.item() == 0 or answer_end.item() == 0:
            continue
        if inputs["input_ids"][0][answer_start] == tokenizerBERT.sep_token_id or inputs["input_ids"][0][answer_end - 1] == tokenizerBERT.sep_token_id:
            continue
    
        # Calculate the total score for this answer
        total_score = answer_start_scores[0, answer_start].item() + answer_end_scores[0, answer_end - 1].item()

        # If this score is higher than the previous best, update the best answer
        if total_score > max_score:
            max_score = total_score
            # Convert the answer from token IDs to a string
            best_answer = tokenizerBERT.convert_tokens_to_string(tokenizerBERT.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end]))

    return best_answer


def create_embeddings(tokenizer, model, emodel):
    emb.insertEmbeddings(tokenizer, model, emodel)
    return "Embeddings created"


def grogmethod1(question):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        model="mixtral-8x7b-32768",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )

    return chat_completion.choices[0].message.content


def askllama(question):
    start = startTimer()
    contextfromRAG, EmbeddingID = emb.retreivesimilarity(question, model, tokenizer, embeddingModel)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": contextfromRAG,
            },
            {
                "role": "user",
                "content": question,
            }
        ],
        model="llama3-8b-8192",
    )
    end = stopTimer()
    time = end - start
    sendToExcelWriter(question, chat_completion.choices[0].message.content, EmbeddingID, embeddingModel, chat_completion.model, contextfromRAG, time)

    return chat_completion.choices[0].message.content


def askllamaNoContext(question):
    start = startTimer()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        model="llama3-8b-8192",
    )
    end = stopTimer()
    time = end - start
    sendToExcelWriter(question, chat_completion.choices[0].message.content, "No context", "No context", chat_completion.model, "No context", time)

    return chat_completion.choices[0].message.content


def askmixtral(question):
    start = startTimer()
    contextfromRAG, EmbeddingID = emb.retreivesimilarity(question, model, tokenizer, embeddingModel)
    chat_completion = client.chat.completions.create(
        messages=[
                        {
                "role": "system",
                "content": contextfromRAG,
            },
            {
                "role": "user",
                "content": question,
            }
        ],
        model="mixtral-8x7b-32768",
    )
    end = stopTimer()
    time = end - start
    sendToExcelWriter(question, chat_completion.choices[0].message.content, EmbeddingID, embeddingModel, chat_completion.model, contextfromRAG, time)
    return chat_completion.choices[0].message.content


def askmixtralNoContext(question):
    start = startTimer()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        model="mixtral-8x7b-32768",
    )
    end = stopTimer()
    time = end - start
    sendToExcelWriter(question, chat_completion.choices[0].message.content, "No context", "No context", chat_completion.model, "No context", time)

    return chat_completion.choices[0].message.content


def askgoogle(question):
    start = startTimer()
    contextfromRAG, EmbeddingID = emb.retreivesimilarity(question, model, tokenizer, embeddingModel)
    chat_completion = client.chat.completions.create(
        messages=[
                        {
                "role": "system",
                "content": contextfromRAG,
            },
            {
                "role": "user",
                "content": question,
            }
        ],
        model="gemma-7b-it",
    )
    end = stopTimer()
    time = end - start
    sendToExcelWriter(question, chat_completion.choices[0].message.content, EmbeddingID, embeddingModel, chat_completion.model, contextfromRAG, time)
    return chat_completion.choices[0].message.content


def askgoogleNoContext(question):
    start = startTimer()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        model="gemma-7b-it",
    )
    end = stopTimer()
    time = end - start
    sendToExcelWriter(question, chat_completion.choices[0].message.content, "No context", "No context", chat_completion.model, "No context", time)
    return chat_completion.choices[0].message.content


def sendToExcelWriter(question, answer, embeddingID, embeddingModel, generativeModel, context, time):
    data = [
        (question, answer, embeddingID, embeddingModel, generativeModel, context, time)
    ]
    ew.export_to_excel(data, "data.xlsx")


def startTimer():
    import time
    start = time.time()
    return start


def stopTimer():
    import time
    end = time.time()
    return end

# create_embeddings(tokenizer, model,embeddingModel)

if __name__ == '__main__':
    app.run(debug=True)