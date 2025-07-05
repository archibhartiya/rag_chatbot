from flask import Blueprint, request, jsonify
from models import Complaint
from database import db
import re

complaints_bp = Blueprint("complaints", __name__)

@complaints_bp.route("/complaints", methods=["POST"])
def create_complaint():
    data = request.json
    if not all(k in data for k in ("name", "phone_number", "email", "complaint_details")):
        return jsonify({"error": "Missing fields"}), 400

    if not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"]):
        return jsonify({"error": "Invalid email"}), 400

    complaint = Complaint(**data)
    db.session.add(complaint)
    db.session.commit()

    return jsonify({
        "complaint_id": complaint.id,
        "message": "Complaint created successfully"
    })

@complaints_bp.route("/complaints/<complaint_id>", methods=["GET"])
def get_complaint(complaint_id):
    complaint = Complaint.query.get(complaint_id)
    if not complaint:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "complaint_id": complaint.id,
        "name": complaint.name,
        "phone_number": complaint.phone_number,
        "email": complaint.email,
        "complaint_details": complaint.complaint_details,
        "created_at": complaint.created_at
    })
