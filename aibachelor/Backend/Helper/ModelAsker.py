from groq import Groq
import time
import Helper.Embedding as emb, Helper.excelwriter as ew

class ModelAsker:
    def __init__(self, model_name, embeddingModel, with_context=True):
        self.model_name = model_name
        self.with_context = with_context
        self.embeddingModel = embeddingModel

    def ask(self, question, model, tokenizer, with_context):
        start = self.start_timer()

        if with_context:
            contextfromRAG, EmbeddingID = emb.retreivesimilarity(question, model, tokenizer, self.embeddingModel)
        else:
            contextfromRAG, EmbeddingID = "No context", "No context"

        messages = self.get_messages(question, contextfromRAG)

        client = Groq(api_key="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")
        
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=self.model_name,
        )

        end = self.stop_timer()
        time = end - start
        print(time)
        #self.send_to_excel_writer(question, chat_completion.choices[0].message.content, EmbeddingID, self.embeddingModel, chat_completion.model, contextfromRAG, time)

        return chat_completion.choices[0].message.content

    def ask_gpt2(self ,question, model, tokenizer):
        messages = [
            {
                "role": "system",
                "content": "Jens er en mand fra sjælland, bor i københavn og arbejder som fjollemand. han har et barn Magnus, og en kone Lena. Hans kammerat Flemse er en fjolletmand, som går ved navnet Krellovich, hvilket er lidt underligt..",
            },
            {
                "role": "user",
                "content": question,
            }
        ]
        client = Groq(api_key="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")

        chat_completion = client.chat.completions.create(
            messages=messages,
            model=self.model_name,
        )

        return chat_completion.choices[0].message.content

    def get_messages(self, question, contextfromRAG):
        return [
            {
                "role": "system",
                "content": contextfromRAG,
            },
            {
                "role": "user",
                "content": question,
            }
        ] if self.with_context else [
            {
                "role": "user",-
                "content": question,
            }
        ]

    def send_to_excel_writer(self, question, answer, embeddingID, embeddingModel, generativeModel, context, time):
        data = [
            (question, answer, embeddingID, embeddingModel, generativeModel, context, time)
        ]
        ew.export_to_excel(data, "data.xlsx")

    def start_timer(self):
        return time.time()

    def stop_timer(self):
        return time.time()
    



    
    