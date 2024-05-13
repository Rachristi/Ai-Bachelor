from pymilvus import DataType, CollectionSchema, FieldSchema, Collection, connections, utility, MilvusException
import Dataloader as dl
from transformers import AutoTokenizer, AutoModel
from milvus import default_server
import pickle
import psycopg2
from sentence_transformers import SentenceTransformer

#tokenizer = AutoTokenizer.from_pretrained("KennethEnevoldsen/dfm-sentence-encoder-large")
#model = AutoModel.from_pretrained("KennethEnevoldsen/dfm-sentence-encoder-large")

# tokenizer = AutoTokenizer.from_pretrained('intfloat/e5-mistral-7b-instruct')
# model = AutoModel.from_pretrained('intfloat/e5-mistral-7b-instruct')

connections.connect(host='localhost', port=default_server.listen_port)

def getembeddings():
    collection = utility.list_collections()
    print(collection)
    print(collection[1])

def insertEmbeddings(tokenizer, model, nameOfCollection, batch_size=8):
    try: 
        collection = utility.list_collections()
        print(collection)
    except MilvusException as e:
        print(e)

    data = dl.loaddataQAPairs()

    # Define a schema for the collection
    dim = 1024  # You should adjust this to match the dimensionality of your embeddings
    schema = CollectionSchema(fields=[
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim)
    ], description="Collection of question-answer pair embeddings")

    # Create a new collection
    collection = Collection(name=nameOfCollection, schema=schema)

    # Connect to the PostgreSQL database
    conn = dbconnction()

    # Create a cursor object
    cur = conn.cursor()

    # Process the data in batches
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]

        # Create embeddings for each question-answer pair in the batch
        inputs = tokenizer([f"{qa[0]} {qa[1]}" for qa in batch], max_length=512, padding=True, truncation=True, return_tensors='pt')
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()

        # Insert the embeddings into the collection
        mr = collection.insert([embeddings.tolist()])

        # Store the IDs, embeddings, and original text in a local list of tuples
        local_data = [(id, embedding, text) for id, embedding, text in zip(mr.primary_keys, embeddings, [f"{qa[0]} {qa[1]}" for qa in batch])]

        # Insert the local_data into the database
        for id, embedding, text in local_data:
            cur.execute(
                f"INSERT INTO {nameOfCollection} (id, embedding, text) VALUES (%s, %s, %s)",
                (id, embedding.tolist(), text)
            )

        print(f"Inserted {len(embeddings)} embeddings into the {nameOfCollection} collection.")

    # Commit the changes and close the connection
    conn.commit()
    cur.close()
    conn.close()

    return collection

def retreivesimilarity(question, model, tokenizer, nameOfCollection):
    #QA_EMBEDDINGS = "qa_embeddings"

    # Create a Collection object for the collection you want to search
    collection = Collection(name=nameOfCollection)

    # Create an index for the collection
    index_params = {"metric_type": "IP", "index_type": "IVF_FLAT", "params": {"nlist": 100}}
    collection.create_index("embedding", index_params)

    # Load the collection into memory
    collection.load()

    # Create a query vector
    inputs = tokenizer(question, padding=True, truncation=True, return_tensors="pt")
    outputs = model(**inputs)
    query_vector = outputs.last_hidden_state.mean(dim=1).detach().numpy()[0]

    # Perform a cosine similarity search
    search_params = {"metric_type": "IP", "params": {"nprobe": 10}}
    top_k = 5  # Number of results to return
    print(query_vector.shape)
    results = collection.search([query_vector.tolist()], "embedding", search_params, top_k)

    # Connect to the PostgreSQL database
    conn = dbconnction()

    # Create a cursor object
    cur = conn.cursor()

    # Fetch the text of the highest scored result
    highest_scored_result = results[0][0]
    cur.execute(f"SELECT text FROM {nameOfCollection} WHERE id = %s", (highest_scored_result.id,))
    text = cur.fetchone()[0]

    # Close the connection
    cur.close()
    conn.close()

    print(f"ID: {highest_scored_result.id}, score: {highest_scored_result.score}, text: {text}")

    return text, highest_scored_result.id

def dbconnction():
    conn = psycopg2.connect(
        host="localhost",
        database="bachelor",
        user="postgres",
        password="admin"
    )
    
    return conn

def drop(nameOfCollection):
    collection = Collection(name=nameOfCollection)
    collection.drop()


#DB emdeddings

#embeddinginsert = "qa_embeddings"
#embeddinginsert = "e5mistral7b"

#drop()
#retreivesimilarity("hvad er en pension?", model, tokenizer, embeddinginsert)
#insertEmbeddings(tokenizer, model, embeddinginsert)
#getembeddings()



#tablecreate 
    # CREATE TABLE your_table (
    #     id BIGINT PRIMARY KEY,
    #     embedding FLOAT[] NOT NULL,
    #     text TEXT NOT NULL
    # )



    