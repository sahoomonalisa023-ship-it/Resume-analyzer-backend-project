from flask import Blueprint, request, jsonify
import PyPDF2
import traceback
import requests
from bs4 import BeautifulSoup

from ai.skills import extract_skills
from ai.matcher import calculate_similarity

from database import db
from models.resume_model import ResumeData

analyze = Blueprint("analyze", __name__)


def calculate_skill_score(resume_skills, job_skills):

    if not job_skills:
        return 0

    matched = len(set(resume_skills) & set(job_skills))

    return (matched / len(job_skills)) * 100


def extract_job_text_from_link(url):

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator=" ")

    except:
        return ""


@analyze.route('/analyze', methods=['POST'])
def analyze_resume():

    try:

        file = request.files.get('resume')
        job_desc = request.form.get('job_description', "")
        job_link = request.form.get('job_link', "")

        if job_link:
            job_desc = extract_job_text_from_link(job_link)

        if not file:
            return jsonify({"error": "No resume uploaded"}), 400

        text = ""

        try:
            pdf_reader = PyPDF2.PdfReader(file)

            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted

        except Exception as pdf_err:
            return jsonify({"error": str(pdf_err)}), 400

        resume_skills = [s.lower() for s in extract_skills(text)]
        job_skills = [s.lower() for s in extract_skills(job_desc)]

        text_score = float(calculate_similarity(text, job_desc))
        skill_score = float(calculate_skill_score(resume_skills, job_skills))

        final_score = (skill_score * 0.6) + (text_score * 0.4)

        missing_skills = list(set(job_skills) - set(resume_skills))

        try:
            new_data = ResumeData(
                match_score=round(final_score, 2),
                resume_skills=resume_skills,
                missing_skills=missing_skills
            )

            db.session.add(new_data)
            db.session.commit()

        except Exception as db_err:
            print(db_err)
            db.session.rollback()

        return jsonify({
            "match_score": round(final_score, 2),
            "skill_score": round(skill_score, 2),
            "text_score": round(text_score, 2),
            "resume_skills": resume_skills,
            "job_skills": job_skills,
            "missing_skills": missing_skills
        })

    except Exception as err:
        traceback.print_exc()
        return jsonify({"error": str(err)}), 500