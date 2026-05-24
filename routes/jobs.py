from flask import Blueprint, jsonify, request
from models.resume_model import ResumeData
import requests
from bs4 import BeautifulSoup

jobs = Blueprint("jobs", __name__)

@jobs.route("/jobs", methods=["GET", "POST"])
def get_jobs():
    latest = ResumeData.query.order_by(ResumeData.id.desc()).first()
    if not latest:
        return jsonify({"error": "No resume found in database"}), 404

    skills = latest.resume_skills.lower()
    
    # Agar frontend se POST request mein job link aa raha hai
    if request.method == "POST":
        data = request.get_json()
        job_url = data.get("url")
        
        if job_url:
            print("Scraping started for:", job_url)
            try:
                # 5 seconds ka timeout lagaya taaki zada load na le
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                response = requests.get(job_url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Page se saara text nikal kar lowercase kar diya
                    page_text = soup.get_text().lower()
                    
                    # ATS Matching Logic (Resume skills ko website ke text mein check karna)
                    matched_skills = []
                    resume_skills_list = [s.strip() for s in skills.split(',')] # e.g. ['react', 'javascript']
                    
                    for skill in resume_skills_list:
                        if skill in page_text:
                            matched_skills.append(skill)
                    
                    # Ek basic ATS Score calculate karna
                    if len(resume_skills_list) > 0:
                        ats_score = int((len(matched_skills) / len(resume_skills_list)) * 100)
                    else:
                        ats_score = 0
                        
                    return jsonify({
                        "status": "success",
                        "ats_score": ats_score,
                        "matched_skills": matched_skills,
                        "message": f"Scraped successfully with {ats_score}% match!"
                    })
                else:
                    return jsonify({"error": f"Website blocked access (Status: {response.status_code})"}), 400
                    
            except requests.exceptions.Timeout:
                return jsonify({"error": "Website took too long to respond. Please paste JD text manually."}), 408
            except Exception as e:
                return jsonify({"error": f"Scraping error: {str(e)}"}), 500

    # Baki normal GET request ke liye purana logic
    recommended_jobs = []
    if "react" in skills:
        recommended_jobs.append({"title": "React Developer", "skills": "React, JavaScript"})
    if "python" in skills:
        recommended_jobs.append({"title": "Python Developer", "skills": "Python, Flask"})
        
    return jsonify(recommended_jobs)