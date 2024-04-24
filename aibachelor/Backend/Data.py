from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import GPT2LMHeadModel, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

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
        answer = method2(question)
        sender = "bot"
    else:
        answer = "Invalid method selected"
        sender = "bot"
    return jsonify({'answer': answer, 'sender': sender})


def ask_gpt2(question):
    inputs = tokenizer.encode_plus(question, return_tensors="pt")
    outputs = model.generate(
        input_ids=inputs["input_ids"], 
        attention_mask=inputs["attention_mask"],
        max_length=100, 
        num_return_sequences=1,  # Generate 5 different sequences
        temperature=0.8,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True  # Use probabilistic decoding
    )
    answer = tokenizer.decode(outputs[0])
    return answer




def method2(question):
    # Implement method 2 logic here
    return "Answer from method 2"

if __name__ == '__main__':
    app.run(debug=True)