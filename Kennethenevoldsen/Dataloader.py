import pandas as pd
from numba import jit, cuda 

def loaddata():
    df = pd.read_excel(r'C:\Users\RaChr\Desktop\Skole\Bachelor\Ai-Bachelor\labeled_020.xlsx')

    sentenses = get_sentencses(df)

    return sentenses


def get_sentencses(df):

    sentenses = df['text'].tolist()

    return sentenses
