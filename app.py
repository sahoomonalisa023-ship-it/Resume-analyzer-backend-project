from flask import Flask
from flask_cors import CORS

from database import db

from routes.analyze import analyze
from routes.dashboard import dashboard
from routes.jobs import jobs
from routes.auth import auth

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = \
'sqlite:///database.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(analyze)
app.register_blueprint(dashboard)
app.register_blueprint(jobs)
app.register_blueprint(auth)

@app.route('/')
def home():
    return "Backend Running"

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)