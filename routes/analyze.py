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


def calculate_skill_score(
    resume_skills,
    job_skills
):

    if not job_skills:
        return 0

    matched = list(

        set(resume_skills) &
        set(job_skills)

    )

    score = (
        len(matched) /
        len(job_skills)
    ) * 100

    return round(score, 2)


def extract_job_text_from_link(url):

    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        text = soup.get_text(
            separator=" "
        )

        return text

    except:
        return ""


@analyze.route(
    '/analyze',
    methods=['POST']
)

def analyze_resume():

    try:

        file = request.files.get(
            'resume'
        )

        job_desc = request.form.get(
            'job_description',
            ""
        )

        job_link = request.form.get(
            'job_link',
            ""
        )

        # =========================
        # COMBINE LINK + TEXT
        # =========================

        if job_link:

            scraped_text = extract_job_text_from_link(
                job_link
            )

            job_desc = (
                job_desc + " " + scraped_text
            )

        # =========================
        # CHECK PDF
        # =========================

        if not file:

            return jsonify({
                "error": "No resume uploaded"
            }), 400

        text = ""

        # =========================
        # PDF TEXT EXTRACTION
        # =========================

        try:

            pdf_reader = PyPDF2.PdfReader(file)

            for page in pdf_reader.pages:

                extracted = page.extract_text()

                if extracted:

                    text += extracted

        except Exception as pdf_err:

            return jsonify({
                "error": str(pdf_err)
            }), 400

        # =========================
        # SKILL EXTRACTION
        # =========================

        raw_resume_skills = extract_skills(
            text
        )

        raw_job_skills = extract_skills(
            job_desc
        )

        resume_skills = [

            skill.lower()

            for skill in raw_resume_skills

        ]

        job_skills = [

            skill.lower()

            for skill in raw_job_skills

        ]

        # =========================
        # AI TEXT SIMILARITY
        # =========================

        text_score = float(

            calculate_similarity(
                text,
                job_desc
            )

        )

        # =========================
        # SKILL SCORE
        # =========================

        skill_score = float(

            calculate_skill_score(
                resume_skills,
                job_skills
            )

        )

        # =========================
        # FINAL ATS SCORE
        # =========================

        final_score = (

            text_score * 0.7

        ) + (

            skill_score * 0.3

        )

        # =========================
        # MISSING SKILLS
        # =========================

        missing_skills = list(

            set(job_skills) -
            set(resume_skills)

        )

        # =========================
        # SAVE DATABASE
        # =========================

        try:

            new_data = ResumeData(

                match_score=round(
                    final_score,
                    2
                ),

                resume_skills=",".join(
                    resume_skills
                ),

                missing_skills=",".join(
                    missing_skills
                )

            )

            db.session.add(new_data)

            db.session.commit()

        except Exception as db_err:

            print(db_err)

            db.session.rollback()

        # =========================
        # RESPONSE
        # =========================

        return jsonify({

            "match_score": round(
                final_score,
                2
            ),

            "skill_score": round(
                skill_score,
                2
            ),

            "text_score": round(
                text_score,
                2
            ),

            "resume_skills": resume_skills,

            "job_skills": job_skills,

            "missing_skills": missing_skills

        })

    except Exception as err:

        traceback.print_exc()

        return jsonify({
            "error": str(err)
        }), 500