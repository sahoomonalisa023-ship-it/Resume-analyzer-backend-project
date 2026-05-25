import re

def calculate_similarity(resume_text, job_description):

    if not resume_text or not job_description:
        return 0

    resume_words = set(resume_text.lower().split())
    job_words = set(job_description.lower().split())

    resume_words = {w for w in resume_words if len(w) > 2}
    job_words = {w for w in job_words if len(w) > 2}

    if not job_words:
        return 0

    matched = resume_words & job_words

    return round((len(matched) / len(job_words)) * 100, 2)