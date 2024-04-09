import openai
import os
from qdrant_client import QdrantClient, models
import json


# Load OpenAI key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")
client = QdrantClient(host="localhost", port=6333)  # Adjust host and port if needed

def encode_text(text):
    response = openai.Embedding.create(
        input=[text],
        model="text-embedding-3-large"  # Using the text-embedding-ada-002 model
    )
    embedding = response['data'][0]['embedding']
    return embedding

vector_size = 1536  # Dimension of the text-embedding-ada-002 model

client.recreate_collection(
    collection_name="qa_pairs",
    vectors_config=models.VectorParams(
        size=vector_size,
        distance=models.Distance.COSINE,  # Using cosine distance
    ),
)

def upload_to_qdrant(client, collection_name, qa_pairs):
    for i, qa_pair in enumerate(qa_pairs):
        question_embedding = encode_text(qa_pair['question'])
        answer_embedding = encode_text(qa_pair['answer'])
        
        client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=i * 2,
                    vector=question_embedding,
                    payload={
                        "text": qa_pair['question'],
                        "type": "question"
                    }
                ),
                models.PointStruct(
                    id=i * 2 + 1,
                    vector=answer_embedding,
                    payload={
                        "text": qa_pair['answer'],
                        "type": "answer"
                    }
                )
            ]
        )

# Load the JSON data from the file
with open("data/ori_pqau.json", "r") as file:
    data = json.load(file)

# Extract the QA pairs
qa_pairs = []
for item in data.values():
    qa_pair = {
        "question": item["QUESTION"],
        "contexts": item["CONTEXTS"],
        "meshes": item["MESHES"],
        "long_answer": item["LONG_ANSWER"],
        "labels": item["LABELS"]
    }
    qa_pairs.append(qa_pair)

# Call the `upload_to_qdrant` function with the extracted `qa_pairs`
upload_to_qdrant(client, "qa_pairs", qa_pairs)