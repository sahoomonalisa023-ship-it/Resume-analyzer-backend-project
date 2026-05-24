from flask import Blueprint, jsonify
from models.resume_model import ResumeData

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/dashboard", methods=["GET"])
def get_dashboard():

    latest = ResumeData.query.order_by(
        ResumeData.id.desc()
    ).first()

    if not latest:
        return jsonify({
            "message": "No data found"
        })

    return jsonify({
        "match_score": latest.match_score,
        "resume_skills": latest.resume_skills.split(","),
        "missing_skills": latest.missing_skills.split(",")
    })