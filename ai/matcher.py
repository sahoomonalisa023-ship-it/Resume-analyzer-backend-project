import re

def calculate_similarity(
    resume_text,
    job_description
):

    resume_words = set(
        re.findall(r'\w+', resume_text.lower())
    )

    job_words = set(
        re.findall(r'\w+', job_description.lower())
    )

    if not job_words:
        return 0

    matched = len(
        resume_words & job_words
    )

    similarity = (
        matched / len(job_words)
    ) * 100

    return round(similarity, 2)