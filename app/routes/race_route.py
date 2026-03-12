from flask import Blueprint, jsonify, request
from app.services.race_service import RaceService

race_bp = Blueprint("race", __name__)

@race_bp.route("", methods=["GET"])
@race_bp.route("/", methods=["GET"])
def get_all_races():
    """
    Get all races with pagination
    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 100)
        - sort_by: Field to sort by (default: "Race")
        - sort_order: Sort order "asc" or "desc" (default: "asc")
        - search: Search by race name (optional)
    """
    try:
        # Get query parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 100, type=int)
        sort_by = request.args.get("sort_by", "Race")
        sort_order = request.args.get("sort_order", "asc")
        search = request.args.get("search", "")

        # Validate per_page
        if per_page > 500:
            per_page = 500

        # Get data from service
        result = RaceService.get_all_races(
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

@race_bp.route("/<int:race_id>", methods=["GET"])
def get_race_by_id(race_id):
    """
    Get a race by ID
    URL Parameters:
        - race_id: Race ID
    """
    try:
        result = RaceService.get_race_by_id(race_id)

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500
