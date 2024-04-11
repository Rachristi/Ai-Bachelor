import pandas as pd
from numba import jit, cuda 

def loaddata():
    df = pd.read_excel(r'..\labeled_036.xlsx')

    # Filter rows where finance_relevant is True
    relevance_rows = df[df['finance_relevant'] == True]

    QnA_dict = {}

    for index, row in relevance_rows.iterrows():
        question_id = row['question_id']
        data_type = row['data_type']
        text = row['text']
        
        # Check if the question_id already exists in the dictionary
        if question_id in QnA_dict:
            # Append the text to the existing list of texts for this question_id
            QnA_dict[question_id].append((text, data_type))
        else:
            # Create a new list with the text for this question_id
            QnA_dict[question_id] = [(text, data_type)]

    # Create lists to store questions and answers
    question_answer_pairs = []

    # Iterate over each question_id and its associated entries
    for question_id, entries in QnA_dict.items():
        # Initialize lists to store questions and answers for this question_id
        question_texts = []
        answer_texts = []
        # Iterate over each entry (text, data_type) tuple
        for entry in entries:
            text, data_type = entry
            # Check if the entry is a question or an answer
            if data_type == 'question':
                question_texts.append(text)
            else:
                answer_texts.append(text)
        # Concatenate all the answers into a single string
        answers_text = ' '.join(answer_texts)
        # Add question-answer pair to the list
        if question_texts:
            question_answer_pairs.append((question_texts[0], answers_text))

    return question_answer_pairs