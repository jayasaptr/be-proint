from flask import Blueprint, jsonify, request
from app.services.religion_service import ReligionService

religion_bp = Blueprint("religion", __name__)

@religion_bp.route("", methods=["GET"])
@religion_bp.route("/", methods=["GET"])
def get_all_religions():
    """
    Get all religions with pagination
    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 100)
        - sort_by: Field to sort by (default: "Religion")
        - sort_order: Sort order "asc" or "desc" (default: "asc")
        - search: Search by religion name (optional)
    """
    try:
        # Get query parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 100, type=int)
        sort_by = request.args.get("sort_by", "Religion")
        sort_order = request.args.get("sort_order", "asc")
        search = request.args.get("search", "")

        # Validate per_page
        if per_page > 500:
            per_page = 500

        # Get data from service
        result = ReligionService.get_all_religions(
            page=page,
            per_page=per_page,
            sort_by=sort_by,
            sort_order=sort_order,
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

@religion_bp.route("/<int:religion_id>", methods=["GET"])
def get_religion_by_id(religion_id):
    """
    Get a religion by ID
    URL Parameters:
        - religion_id: Religion ID
    """
    try:
        result = ReligionService.get_religion_by_id(religion_id)

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500
