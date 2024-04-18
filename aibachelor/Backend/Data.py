from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/answer', methods=['POST'])
def get_answer():
    question = request.json['question']
    method = request.json['method']  # Assuming method is specified in the request
    # Call the appropriate method based on the dropdown selection
    if method == 'method1':
        answer = method1(question)
    elif method == 'method2':
        answer = method2(question)
    else:
        answer = "Invalid method selected"
    return jsonify({'answer': answer})

def method1(question):
    # Implement method 1 logic here
    return "Answer from method 1"

def method2(question):
    # Implement method 2 logic here
    return "Answer from method 2"

if __name__ == '__main__':
    app.run(debug=True)