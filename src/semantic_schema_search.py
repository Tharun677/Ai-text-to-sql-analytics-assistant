from sentence_transformers import SentenceTransformer, util
from src.schema_retriever import get_database_schema


# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


def build_schema_documents():
    schema = get_database_schema()
    documents = []

    for table_name, table_info in schema.items():

        documents.append({
            "name": table_name,
            "type": "table",
            "description": table_info["description"],
            "table": table_name
        })

        for column in table_info["columns"]:
            documents.append({
                "name": column["column_name"],
                "type": "column",
                "description": column["description"],
                "table": table_name
            })

    return documents


def semantic_search_schema(question, limit=5):
    documents = build_schema_documents()

    if not documents:
        return []

    # Prepare searchable text
    schema_texts = [
        f"{item['name']}. {item['description']}. Table: {item['table']}"
        for item in documents
    ]

    # Convert schema descriptions into embeddings
    schema_embeddings = model.encode(
        schema_texts,
        convert_to_tensor=True
    )

    # Convert user's question into an embedding
    question_embedding = model.encode(
        question,
        convert_to_tensor=True
    )

    # Calculate semantic similarity
    similarities = util.cos_sim(
        question_embedding,
        schema_embeddings
    )[0]

    # Get the most relevant schema items
    top_results = similarities.argsort(descending=True)[:limit]

    results = []

    for index in top_results:
        item = documents[int(index)]
        item["similarity"] = round(
            float(similarities[index]), 4
        )
        results.append(item)

    return results


if __name__ == "__main__":
    question = "Which column stores the total money earned from product sales?"

    print("\nSEMANTIC SCHEMA SEARCH RESULTS")
    print("=" * 55)

    for result in semantic_search_schema(question):
        print(
            f"\nName: {result['name']}"
            f"\nType: {result['type']}"
            f"\nDescription: {result['description']}"
            f"\nSimilarity: {result['similarity']}"
        )
