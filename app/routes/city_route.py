from flask import Blueprint, jsonify, request
from app.services.city_service import CityService

city_bp = Blueprint("city", __name__)

@city_bp.route("", methods=["GET"])
@city_bp.route("/", methods=["GET"])
def get_all_cities():
    """
    Get all cities with pagination
    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 100)
        - sort_by: Field to sort by (default: "CityName")
        - sort_order: Sort order "asc" or "desc" (default: "asc")
        - search: Search by city name or code (optional)
        - state_id: Filter by state ID (optional)
    """
    try:
        # Get query parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 100, type=int)
        sort_by = request.args.get("sort_by", "CityName")
        sort_order = request.args.get("sort_order", "asc")
        search = request.args.get("search", "")
        state_id = request.args.get("state_id", type=int)

        # Validate per_page
        if per_page > 500:
            per_page = 500

        # Get data from service
        result = CityService.get_all_cities(
            page=page,
            per_page=per_page,
            sort_by=sort_by,
            sort_order=sort_order,
            search=search,
            state_id=state_id
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

@city_bp.route("/<int:city_id>", methods=["GET"])
def get_city_by_id(city_id):
    """
    Get a city by ID
    URL Parameters:
        - city_id: City ID
    """
    try:
        result = CityService.get_city_by_id(city_id)

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500
