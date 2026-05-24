from flask import Blueprint, jsonify
from models.resume_model import ResumeData

jobs = Blueprint("jobs", __name__)

@jobs.route("/jobs", methods=["GET"])
def get_jobs():

    latest = ResumeData.query.order_by(
        ResumeData.id.desc()
    ).first()

    if not latest:
        return jsonify([])

    skills = latest.resume_skills.lower()

    recommended_jobs = []

    if "react" in skills:
        recommended_jobs.append({
            "title": "React Developer",
            "skills": "React, JavaScript, Tailwind"
        })

    if "python" in skills:
        recommended_jobs.append({
            "title": "Python Backend Developer",
            "skills": "Python, Flask, APIs"
        })

    if "sql" in skills:
        recommended_jobs.append({
            "title": "Data Analyst",
            "skills": "SQL, Python, Excel"
        })

    return jsonify(recommended_jobs)