import re

TECH_KEYWORDS = {

    "python",
    "java",
    "javascript",
    "typescript",
    "react",
    "nextjs",
    "nodejs",
    "express",
    "mongodb",
    "mysql",
    "postgresql",
    "sql",
    "html",
    "html5",
    "css",
    "css3",
    "tailwind",
    "bootstrap",
    "flask",
    "django",
    "api",
    "rest",
    "graphql",
    "docker",
    "kubernetes",
    "aws",
    "firebase",
    "git",
    "github",
    "linux",
    "pandas",
    "numpy",
    "tensorflow",
    "opencv",
    "machine",
    "learning",
    "ai",
    "ml",
    "data",
    "analytics",
    "powerbi",
    "excel",
    "c",
    "cpp",
    "c++",
    "php",
    "laravel",
    "redux",
    "vite",
    "figma",
    "ui",
    "ux"

}

def extract_skills(text):

    text = text.lower()

    words = re.findall(
        r"[a-zA-Z0-9+#.]+",
        text
    )

    found = set()

    for word in words:

        clean_word = word.strip()

        if clean_word in TECH_KEYWORDS:

            found.add(clean_word)

    return list(found)