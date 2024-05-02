import pandas as pd

def loaddata():
    # Read the first Excel file
    df1 = pd.read_excel(r'labeled_036.xlsx')
    
    # Read the second Excel file
    df2 = pd.read_excel(r'labeled_020.xlsx')
    
    # Filter rows where finance_relevant is True and add identifier
    df1['question_id'] = '036_' + df1['question_id'].astype(str)
    df2['question_id'] = '020_' + df2['question_id'].astype(str)
    
    # Concatenate the two DataFrames
    df = pd.concat([df1, df2])

    # Filter rows where finance_relevant is True
    relevance_rows = df[df['finance_relevant'] == True]

    # Initialize a dictionary to store questions with the same ID
    QnA_dict = {}

    # Iterate over each row
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

    # Create a list to store question-answer pairs
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
        # Concatenate all the questions into a single string
        questions_text = ' '.join(question_texts)
        # Concatenate all the answers into a single string
        answers_text = ' '.join(answer_texts)
        # Add question-answer pair to the list with identifier
        if questions_text:
            question_answer_pairs.append((question_id, questions_text, answers_text))

    # Return question_answer_pairs without identifier
    return [(question, answers) for _, question, answers in question_answer_pairs]
    