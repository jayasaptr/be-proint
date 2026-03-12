from flask import Blueprint, jsonify, request
from app.services.candidate_service import CandidateService
import os

candidate_bp = Blueprint("candidate", __name__)

@candidate_bp.route("/apply", methods=["POST"])
def submit_candidate():
    """
    Submit candidate application (Apply Job)

    Content-Type: multipart/form-data

    Required Fields:
        - job_id: ID posisi yang dilamar (integer)
        - full_name: Nama lengkap kandidat
        - email: Email kandidat
        - gender: Jenis kelamin (M/F)
        - birth_city_id: ID kota tempat lahir (integer, dari API /cities)
        - date_of_birth: Tanggal lahir (YYYY-MM-DD)
        - marital_status_id: ID status pernikahan (integer, dari API /maritalstatuses)
        - mobile_phone: Nomor HP
        - id_card_address: Alamat sesuai KTP
        - province_id: ID provinsi (integer, dari API /states)
        - city_id: ID kota (integer, dari API /cities)
        - zip_code: Kode pos
        - captcha_token: Token Cloudflare Turnstile
        - is_declared_true: Pernyataan kebenaran data

    Optional Fields:
        - blood_type: Golongan darah (A, B, AB, O, A+, A-, B+, B-, AB+, AB-, O+, O-)
        - race_id: ID suku/etnis (integer, dari API /races)

    Nested JSON Fields (as JSON string):
        - identities: Array of identity cards
          [{"card_type_id": 1, "number": "3201234567890001"}]
        - educations: Array of education history
          [{"edu_level_id": 5, "edu_institution_id": 12, "major": "Teknik Informatika", "gpa": 3.50, "is_last_education": true}]
        - experiences: Array of work experiences (optional)
          [{"company_name": "PT. ABC", "position": "Staff IT", "job_period_year": "2020 - 2022", "salary": 5000000}]
        - answers: Array of question answers
          [{"qtempid": 1, "question_id": 5, "answer": "Ya"}]

    Files:
        - photo: Pas foto (optional, JPEG/PNG, max 2MB)
        - documents[]: Array of document files (min 1, PDF/Word, max 10MB per file)
        - document_descriptions[]: Array of document descriptions

    Returns:
        200: Success with candidate_id and candidate_code
        400: Bad request (captcha failed)
        422: Validation error
        500: Server error
    """
    try:
        # Get form data
        form_data = request.form.to_dict()

        # Get files
        files = {}

        # Handle single photo file
        if 'photo' in request.files:
            files['photo'] = request.files['photo']

        # Handle multiple document files
        if 'documents[]' in request.files:
            files['documents[]'] = request.files.getlist('documents[]')

        # Validate is_declared_true
        if form_data.get('is_declared_true', '').lower() not in ['true', '1', 'yes']:
            return jsonify({
                "success": False,
                "message": "Pernyataan kebenaran data harus disetujui",
                "errors": {
                    "is_declared_true": ["Anda harus menyetujui pernyataan kebenaran data"]
                }
            }), 422

        # Call service to process submission
        success, message, data, status_code = CandidateService.submit_candidate(
            form_data=form_data,
            files=files
        )

        # Prepare response
        response = {
            "success": success,
            "message": message
        }

        if data:
            if "errors" in data:
                response["errors"] = data["errors"]
            else:
                response["data"] = data

        return jsonify(response), status_code

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500


@candidate_bp.route("/check-email", methods=["POST"])
def check_email():
    """
    Check if email already exists (for any job application)

    Note: Kandidat yang sama bisa melamar beberapa posisi berbeda.
    Untuk cek apakah sudah pernah melamar job tertentu, gunakan /check-application

    Body:
        {
            "email": "example@email.com"
        }

    Returns:
        200: Email check result
    """
    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({
                "success": False,
                "message": "Email is required"
            }), 422

        exists = CandidateService.check_duplicate_email(email)

        return jsonify({
            "success": True,
            "exists": exists,
            "message": "Email sudah pernah digunakan untuk melamar" if exists else "Email belum pernah digunakan"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500


@candidate_bp.route("/check-identity", methods=["POST"])
def check_identity():
    """
    Check if identity number already exists (for any job application)

    Note: Kandidat yang sama bisa melamar beberapa posisi berbeda.
    Untuk cek apakah sudah pernah melamar job tertentu, gunakan /check-application

    Body:
        {
            "identity_number": "1234567890123456"
        }

    Returns:
        200: Identity check result
    """
    try:
        data = request.get_json()
        identity_number = data.get('identity_number')

        if not identity_number:
            return jsonify({
                "success": False,
                "message": "Identity number is required"
            }), 422

        exists = CandidateService.check_duplicate_identity(identity_number)

        return jsonify({
            "success": True,
            "exists": exists,
            "message": "Nomor identitas sudah pernah digunakan untuk melamar" if exists else "Nomor identitas belum pernah digunakan"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500


@candidate_bp.route("/check-application", methods=["POST"])
def check_application():
    """
    Check if candidate has already applied to a specific job

    Body:
        {
            "email": "example@email.com",
            "job_id": 12
        }

    Returns:
        200: Application check result
    """
    try:
        data = request.get_json()
        email = data.get('email')
        job_id = data.get('job_id')

        if not email or not job_id:
            return jsonify({
                "success": False,
                "message": "Email and job_id are required"
            }), 422

        exists = CandidateService.check_duplicate_application(email, job_id)

        return jsonify({
            "success": True,
            "exists": exists,
            "message": "Anda sudah pernah melamar posisi ini" if exists else "Anda belum pernah melamar posisi ini"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500


@candidate_bp.route("/captcha-config", methods=["GET"])
def get_captcha_config():
    """
    Get Cloudflare Turnstile captcha configuration

    Returns:
        200: Captcha configuration with site key
    """
    try:
        site_key = os.getenv('TURNSTILE_SITE_KEY', '')

        if not site_key:
            return jsonify({
                "success": False,
                "message": "Captcha not configured"
            }), 500

        return jsonify({
            "success": True,
            "data": {
                "site_key": site_key,
                "provider": "cloudflare_turnstile"
            }
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500
