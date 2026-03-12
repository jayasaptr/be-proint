from flask import Blueprint, jsonify, request
from app.services.site_service import SiteService

site_bp = Blueprint("site", __name__)

@site_bp.route("", methods=["GET"])
@site_bp.route("/", methods=["GET"])
def get_all_sites():
    """
    Get all sites with pagination
    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 100)
        - sort_by: Field to sort by (default: "OrgRecName")
        - sort_order: Sort order "asc" or "desc" (default: "asc")
        - search: Search by site name or code (optional)
    """
    try:
        # Get query parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 100, type=int)
        sort_by = request.args.get("sort_by", "OrgRecName")
        sort_order = request.args.get("sort_order", "asc")
        search = request.args.get("search", "")

        # Validate per_page
        if per_page > 500:
            per_page = 500

        # Get data from service
        result = SiteService.get_all_sites(
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

@site_bp.route("/<int:site_id>", methods=["GET"])
def get_site_by_id(site_id):
    """
    Get site by ID
    """
    try:
        result = SiteService.get_site_by_id(site_id)

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500
