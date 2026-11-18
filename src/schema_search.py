from rapidfuzz import process, fuzz
from src.schema_retriever import get_database_schema


def search_schema(question, limit=5):
    schema = get_database_schema()

    searchable_items = []

    for table_name, table_info in schema.items():
        searchable_items.append({
            "name": table_name,
            "description": table_info["description"],
            "type": "table"
        })

        for column in table_info["columns"]:
            searchable_items.append({
                "name": column["column_name"],
                "description": column["description"],
                "type": "column",
                "table": table_name
            })

    search_terms = []

    for item in searchable_items:
        search_terms.append(item["name"])
        search_terms.append(item["description"])

    matches = process.extract(
        question,
        search_terms,
        scorer=fuzz.WRatio,
        limit=limit
    )

    results = []

    for matched_text, score, index in matches:
        if score >= 30:
            for item in searchable_items:
                if (
                    matched_text == item["name"]
                    or matched_text == item["description"]
                ):
                    if item not in results:
                        results.append(item)
                    break

    return results


if __name__ == "__main__":
    question = "Which column stores total revenue?"

    print("\nSCHEMA SEARCH RESULTS")
    print("=" * 40)

    for result in search_schema(question):
        print(result)
