import pandas as pd

def loaddata():
    df = pd.read_excel(r'C:\Users\RaChr\Desktop\Skole\Bachelor\labeled_020.xlsx')

    sentenses = get_sentencses(df)

    return sentenses


def get_sentencses(df):

    sentenses = df['text'].tolist()

    return sentenses
