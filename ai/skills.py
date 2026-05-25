import re
from collections import Counter

STOPWORDS = {

    "the", "and", "with", "for", "you",
    "your", "are", "have", "this",
    "that", "from", "will", "our",
    "job", "role", "team", "skills",
    "experience", "working", "good",
    "ability", "knowledge", "using",
    "worked", "project", "projects",
    "developer", "application",
    "applications", "responsible",
    "developed", "build", "building",
    "resume", "cv", "name",
    "email", "phone", "address"

}

def extract_skills(text):

    text = text.lower()

    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z0-9+#.-]{2,}\b",
        text
    )

    filtered = [

        word.strip()

        for word in words

        if word not in STOPWORDS
        and not word.isdigit()

    ]

    freq = Counter(filtered)

    common_words = [

        word

        for word, count in freq.most_common(50)

    ]

    return common_words