from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import BertForQuestionAnswering, BertTokenizer
import Dataloader as dl



# tokenizerGPT2 = GPT2Tokenizer.from_pretrained("gpt2")
# modelGPT2 = GPT2LMHeadModel.from_pretrained("gpt2")

tokenizerBERT = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
modelBERT = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

context = dl.loaddata()


app = Flask(__name__)
CORS(app)

@app.route('/answer', methods=['POST'])
def get_answer():
    question = request.json['question']
    method = request.json['method']  # Assuming method is specified in the request
    # Call the appropriate method based on the dropdown selection
    if method == 'method1':
        answer = ask_gpt2(question)
        sender = "bot"
    elif method == 'method2':
        answer = method2(question, context)
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
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True  # Use probabilistic decoding
    )
    answer = tokenizerGPT2.decode(outputs[0])
    return answer


def method2(question, context):
    max_score = -float('inf')
    best_answer = None

    # Iterate over each possible answer in the context
    for possible_answer in context:
        # Prepare the inputs for the BERT model
        inputs = tokenizerBERT.encode_plus(question, possible_answer, max_length=512, truncation=True, padding='max_length', return_tensors="pt")

        # Pass the inputs to the BERT model
        outputs = modelBERT(**inputs)
        answer_start_scores, answer_end_scores = outputs.start_logits, outputs.end_logits

        # Get the most likely start and end of the answer
        answer_start = torch.argmax(answer_start_scores)
        answer_end = torch.argmax(answer_end_scores) + 1

        # Calculate the total score for this answer
        total_score = answer_start_scores[0, answer_start].item() + answer_end_scores[0, answer_end - 1].item()

        # If this score is higher than the previous best, update the best answer
        if total_score > max_score:
            max_score = total_score
            # Convert the answer from token IDs to a string
            best_answer = tokenizerBERT.convert_tokens_to_string(tokenizerBERT.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end]))

    return best_answer

if __name__ == '__main__':
    app.run(debug=True)