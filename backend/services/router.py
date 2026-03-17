import re

def is_dataset_question(question: str) -> bool:
    question = question.lower()

    # Pattern 1: specific order id
    if re.search(r"\b\d{3,5}\b", question):
        return True

    # Pattern 2: asking for record details
    dataset_keywords = [
        "order id", "details of", "show record", "which order",
        "picking time", "distance", "transport mode",
        "warehouse name", "delay yes or no"
    ]

    if any(word in question for word in dataset_keywords):
        return True

    # Otherwise → research question
    return False
