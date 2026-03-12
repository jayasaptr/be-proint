from flask import Blueprint, jsonify, request
from app.services.eduinstitution_service import EduInstitutionService

eduinstitution_bp = Blueprint("eduinstitution", __name__)

@eduinstitution_bp.route("", methods=["GET"])
@eduinstitution_bp.route("/", methods=["GET"])
def get_all_eduinstitutions():
    """
    Get all education institutions with pagination
    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 100)
        - sort_by: Field to sort by (default: "EduInsName")
        - sort_order: Sort order "asc" or "desc" (default: "asc")
        - active_only: Filter only active records (default: true)
        - search: Search by name (optional)
    """
    try:
        # Get query parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 100, type=int)
        sort_by = request.args.get("sort_by", "EduInsName")
        sort_order = request.args.get("sort_order", "asc")
        active_only = request.args.get("active_only", "true").lower() == "true"
        search = request.args.get("search", "")

        # Validate per_page
        if per_page > 500:
            per_page = 500

        # Get data from service
        result = EduInstitutionService.get_all_eduinstitutions(
            page=page,
            per_page=per_page,
            sort_by=sort_by,
            sort_order=sort_order,
            active_only=active_only,
            search=search
        )

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@eduinstitution_bp.route("/<int:edu_ins_id>", methods=["GET"])
def get_eduinstitution_by_id(edu_ins_id):
    """
    Get education institution by ID
    Path Parameters:
        - edu_ins_id: Education institution ID
    """
    try:
        result = EduInstitutionService.get_eduinstitution_by_id(edu_ins_id)

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500
