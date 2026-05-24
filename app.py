from flask import Flask
from flask_cors import CORS

from database import db

from routes.analyze import analyze
from routes.dashboard import dashboard
from routes.jobs import jobs
from routes.auth import auth

import os

app = Flask(__name__)

# CORS
CORS(app)

# DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = \
'sqlite:///database.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# INIT DB
db.init_app(app)

# BLUEPRINTS
app.register_blueprint(analyze)

app.register_blueprint(dashboard)

app.register_blueprint(jobs)

app.register_blueprint(auth)

# HOME ROUTE
@app.route('/')
def home():

    return {
        "message": "Resume AI Backend Running"
    }

# MAIN
if __name__ == "__main__":

    with app.app_context():

        db.create_all()

    # RENDER / RAILWAY PORT
    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )