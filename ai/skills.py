import re

def extract_skills(text):

    text = text.lower()

    # remove special characters
    text = re.sub(r"[^a-zA-Z0-9+#.\s]", " ", text)

    words = text.split()

    # common stopwords remove
    stopwords = {

        "the", "and", "with", "for",
        "you", "your", "are", "have",
        "this", "that", "from", "will",
        "our", "job", "role", "team",
        "developer", "experience",
        "working", "skills", "knowledge"

    }

    filtered = [

        word.strip()

        for word in words

        if len(word) > 2
        and word not in stopwords

    ]

    # unique words
    unique_skills = list(set(filtered))

    return unique_skills[:80]