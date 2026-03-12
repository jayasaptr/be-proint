from flask import Blueprint, jsonify, request
from app.services.state_service import StateService

state_bp = Blueprint("state", __name__)

@state_bp.route("", methods=["GET"])
@state_bp.route("/", methods=["GET"])
def get_all_states():
    """
    Get all states with pagination
    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 100)
        - sort_by: Field to sort by (default: "StateName")
        - sort_order: Sort order "asc" or "desc" (default: "asc")
        - search: Search by state name or code (optional)
    """
    try:
        # Get query parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 100, type=int)
        sort_by = request.args.get("sort_by", "StateName")
        sort_order = request.args.get("sort_order", "asc")
        search = request.args.get("search", "")

        # Validate per_page
        if per_page > 500:
            per_page = 500

        # Get data from service
        result = StateService.get_all_states(
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

@state_bp.route("/<int:state_id>", methods=["GET"])
def get_state_by_id(state_id):
    """
    Get a state by ID
    URL Parameters:
        - state_id: State ID
    """
    try:
        result = StateService.get_state_by_id(state_id)

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500
