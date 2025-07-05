from flask import Flask
from config import Config
from database import db
from models import Complaint
from routes.complaints import complaints_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(complaints_bp)

@app.route("/")
def index():
    return "RAG Chatbot Backend is Running"

if __name__ == "__main__":
    app.run(debug=True)
