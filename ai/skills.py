import re

skills = [

    "python",
    "javascript",
    "react",
    "reactjs",
    "react.js",
    "nodejs",
    "node.js",
    "express",
    "expressjs",
    "mongodb",
    "mongoose",
    "sql",
    "mysql",
    "postgresql",
    "html",
    "css",
    "tailwind",
    "tailwind css",
    "bootstrap",
    "docker",
    "flask",
    "django",
    "git",
    "github",
    "rest api",
    "api",
]

def extract_skills(text):

    text = text.lower()

    found_skills = set()

    for skill in skills:

        pattern = r'\b' + re.escape(skill) + r'\b'

        if re.search(pattern, text):

            found_skills.add(skill)

    return list(found_skills)