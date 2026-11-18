
import re
from rapidfuzz import process, fuzz

KEYWORDS = [
    "revenue", "sales", "quantity", "product",
    "category", "electronics", "furniture",
    "accessories", "highest", "lowest",
    "average", "total", "profit", "date",
    "monthly", "daily"
]


def clean_question(question):
    question = question.lower()
    question = re.sub(r"[^a-z0-9\s]", " ", question)
    question = re.sub(r"\s+", " ", question).strip()
    return question


def detect_keywords(question):
    cleaned_question = clean_question(question)
    words = cleaned_question.split()
    detected_keywords = []

    for word in words:
        match = process.extractOne(
            word,
            KEYWORDS,
            scorer=fuzz.ratio,
            score_cutoff=75
        )

        if match:
            detected_keywords.append(match[0])

    return list(dict.fromkeys(detected_keywords))


if __name__ == "__main__":
    test_question = "Show me total reveneu by categroy"

    print("Original question:", test_question)
    print("Detected keywords:", detect_keywords(test_question))
