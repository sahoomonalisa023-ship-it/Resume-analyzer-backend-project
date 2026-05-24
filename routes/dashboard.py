from flask import Blueprint, jsonify
from models.resume_model import ResumeData

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/dashboard", methods=["GET"])
def get_dashboard():

    try:
        latest = ResumeData.query.order_by(
            ResumeData.id.desc()
        ).first()

        # ✅ SAFE EMPTY CASE
        if not latest:
            return jsonify({
                "match_score": 0,
                "resume_skills": [],
                "missing_skills": []
            }), 200

        # ✅ SAFE PARSER
        def safe_split(val):
            if val is None:
                return []
            return [x.strip() for x in str(val).split(",") if x.strip()]

        return jsonify({
            "match_score": float(latest.match_score or 0),
            "resume_skills": safe_split(latest.resume_skills),
            "missing_skills": safe_split(latest.missing_skills)
        }), 200

    except Exception as e:
        print("DASHBOARD ERROR:", str(e))
        return jsonify({
            "error": "Server crashed",
            "details": str(e)
        }), 500