from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import BertForQuestionAnswering, BertTokenizer
import Dataloader as dl

tokenizerGPT2 = GPT2Tokenizer.from_pretrained("gpt2")
modelGPT2 = GPT2LMHeadModel.from_pretrained("gpt2")

tokenizerBERT = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
modelBERT = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

client = Groq(
    api_key="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",
)

app = Flask(__name__)
CORS(app)

@app.route('/answer', methods=['POST'])
def get_answer():
    context = dl.loaddataQAPairs()
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
        answer = grogmethod2(question)
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

def grogmethod2(question):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        model="llama3-8b-8192",
        temperature=0.2,
        max_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )

    return chat_completion.choices[0].message.content

if __name__ == '__main__':
    app.run(debug=True)