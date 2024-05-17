from transformers import AutoTokenizer, AutoModel, GPT2Tokenizer, GPT2LMHeadModel, BertTokenizer, BertForQuestionAnswering

class ModelLoader:
    def __init__(self, model_type, model_name):
        self.model_type = model_type
        self.model_name = model_name
        self.tokenizer = None
        self.model = None

    def load(self):
        if self.model_type == 'Auto':
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModel.from_pretrained(self.model_name)
        elif self.model_type == 'GPT2':
            self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
            self.model = GPT2LMHeadModel.from_pretrained(self.model_name)
        elif self.model_type == 'BERT':
            self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
            self.model = BertForQuestionAnswering.from_pretrained(self.model_name)
        else:
            raise ValueError(f'Invalid model type: {self.model_type}')
        return self.model, self.tokenizer