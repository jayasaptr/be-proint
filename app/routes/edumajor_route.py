from flask import Blueprint, jsonify, request
from app.services.edumajor_service import EduMajorService

edumajor_bp = Blueprint("edumajor", __name__)

@edumajor_bp.route("", methods=["GET"])
@edumajor_bp.route("/", methods=["GET"])
def get_all_edumajors():
    """
    Get all education majors with pagination
    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 100)
        - sort_by: Field to sort by (default: "EduMjrName")
        - sort_order: Sort order "asc" or "desc" (default: "asc")
        - active_only: Filter only active records (default: true)
        - search: Search by name (optional)
    """
    try:
        # Get query parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 100, type=int)
        sort_by = request.args.get("sort_by", "EduMjrName")
        sort_order = request.args.get("sort_order", "asc")
        active_only = request.args.get("active_only", "true").lower() == "true"
        search = request.args.get("search", "")

        # Validate per_page
        if per_page > 500:
            per_page = 500

        # Get data from service
        result = EduMajorService.get_all_edumajors(
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

@edumajor_bp.route("/<int:edu_mjr_id>", methods=["GET"])
def get_edumajor_by_id(edu_mjr_id):
    """
    Get education major by ID
    Path Parameters:
        - edu_mjr_id: Education major ID
    """
    try:
        result = EduMajorService.get_edumajor_by_id(edu_mjr_id)

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500
