from sentence_transformers import SentenceTransformer

from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer(
'all-MiniLM-L6-v2'
)

def calculate_similarity(
    resume_text,
    job_description
):

    embeddings = model.encode([

        resume_text,
        job_description
    ])

    similarity = cosine_similarity(

        [embeddings[0]],
        [embeddings[1]]

    )[0][0]

    return round(
        similarity * 100,
        2
    )