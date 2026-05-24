from database import db

class ResumeData(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    match_score = db.Column(
        db.Float
    )

    resume_skills = db.Column(
        db.Text
    )

    missing_skills = db.Column(
        db.Text
    )

    def __repr__(self):

        return f"<ResumeData {self.id}>"