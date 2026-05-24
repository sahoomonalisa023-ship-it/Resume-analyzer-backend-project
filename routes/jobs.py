from flask import Blueprint, jsonify, request
from models.resume_model import ResumeData
import requests
from bs4 import BeautifulSoup

jobs = Blueprint("jobs", __name__)

# =========================
# GET: Recommended Jobs
# =========================
@jobs.route("/jobs", methods=["GET"])
def get_jobs():

    latest = ResumeData.query.order_by(ResumeData.id.desc()).first()

    # fallback jobs (always show)
    fallback_jobs = [
        {"title": "Python Developer", "skills": "Python, Flask, SQL"},
        {"title": "Frontend Developer", "skills": "React, JavaScript, CSS"},
        {"title": "Data Analyst", "skills": "Python, Pandas, SQL"}
    ]

    if not latest or not latest.resume_skills:
        return jsonify(fallback_jobs)

    skills_text = latest.resume_skills.lower()

    recommended_jobs = []

    if "python" in skills_text:
        recommended_jobs.append({
            "title": "Python Developer",
            "skills": "Python, Flask"
        })

    if "react" in skills_text:
        recommended_jobs.append({
            "title": "React Developer",
            "skills": "React, JavaScript"
        })

    if "sql" in skills_text:
        recommended_jobs.append({
            "title": "Data Analyst",
            "skills": "SQL, Python"
        })

    # agar kuch match nahi hua to fallback
    if not recommended_jobs:
        recommended_jobs = fallback_jobs

    return jsonify(recommended_jobs)


# =========================
# POST: Job Link Scraping (ATS)
# =========================
@jobs.route("/jobs", methods=["POST"])
def scrape_job():

    data = request.get_json()
    job_url = data.get("url")

    if not job_url:
        return jsonify({"error": "No job URL provided"}), 400

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(job_url, headers=headers, timeout=8)

        if response.status_code != 200:
            return jsonify({
                "error": "Unable to access job page"
            }), 400

        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text().lower()

        latest = ResumeData.query.order_by(ResumeData.id.desc()).first()

        if not latest or not latest.resume_skills:
            return jsonify({"error": "No resume found"}), 404

        resume_skills = [
            skill.strip().lower()
            for skill in latest.resume_skills.split(",")
        ]

        matched_skills = [
            skill for skill in resume_skills
            if skill in page_text
        ]

        ats_score = int(
            (len(matched_skills) / len(resume_skills)) * 100
            if resume_skills else 0
        )

        return jsonify({
            "status": "success",
            "ats_score": ats_score,
            "matched_skills": matched_skills
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500