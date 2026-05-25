from flask import Blueprint, jsonify
from models.resume_model import ResumeData

jobs = Blueprint("jobs", __name__)

ALL_JOBS = [

    {
        "title": "Python Developer",
        "skills": ["python", "flask", "sql", "api"]
    },

    {
        "title": "Frontend Developer",
        "skills": ["react", "javascript", "html", "css"]
    },

    {
        "title": "Full Stack Developer",
        "skills": ["react", "python", "mongodb", "flask"]
    },

    {
        "title": "Backend Developer",
        "skills": ["python", "django", "postgresql"]
    },

    {
        "title": "Data Analyst",
        "skills": ["python", "sql", "pandas"]
    },

    {
        "title": "MERN Stack Developer",
        "skills": ["mongodb", "express", "react", "nodejs"]
    },

    {
        "title": "AI Engineer",
        "skills": ["python", "api", "sql"]
    }

]


@jobs.route("/jobs", methods=["GET"])
def get_jobs():

    try:

        latest = ResumeData.query.order_by(
            ResumeData.id.desc()
        ).first()

        if not latest or not latest.resume_skills:

            return jsonify([])

        resume_skills = [

            skill.strip().lower()

            for skill in latest.resume_skills.split(",")

        ]

        matched_jobs = []

        for job in ALL_JOBS:

            job_skills = [
                skill.lower()
                for skill in job["skills"]
            ]

            matched = list(
                set(resume_skills) &
                set(job_skills)
            )

            if matched:

                score = int(
                    (
                        len(matched) /
                        len(job_skills)
                    ) * 100
                )

                matched_jobs.append({

                    "title": job["title"],

                    "skills": job["skills"],

                    "matched_skills": matched,

                    "match_score": score

                })

        matched_jobs.sort(
            key=lambda x: x["match_score"],
            reverse=True
        )

        return jsonify(matched_jobs)

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500