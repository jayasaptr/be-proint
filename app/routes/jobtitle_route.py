from flask import Blueprint, jsonify, request
from app.services.jobtitle_service import JobTitleService

jobtitle_bp = Blueprint("jobtitle", __name__)

@jobtitle_bp.route("", methods=["GET"])
@jobtitle_bp.route("/", methods=["GET"])
def get_all_jobtitles():
    """
    Get all job titles with pagination (where InActDate is null and JobTtlLvlId is not null)
    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 100)
        - sort_by: Field to sort by (default: "JobTtlId")
        - sort_order: Sort order "asc" or "desc" (default: "asc")
        - search: Search by job title name (optional)
    """
    try:
        # Get query parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 100, type=int)
        sort_by = request.args.get("sort_by", "JobTtlId")
        sort_order = request.args.get("sort_order", "asc")
        search = request.args.get("search", "")

        # Validate per_page
        if per_page > 500:
            per_page = 500

        # Get data from service
        result = JobTitleService.get_all_jobtitles(
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

@jobtitle_bp.route("/<int:jobtitle_id>", methods=["GET"])
def get_jobtitle_by_id(jobtitle_id):
    """
    Get a specific job title by ID
    Path Parameters:
        - jobtitle_id: Job title ID
    """
    try:
        result = JobTitleService.get_jobtitle_by_id(jobtitle_id)

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500
