from flask import Blueprint, jsonify, request
from app.services.cardtype_service import CardTypeService

cardtype_bp = Blueprint("cardtype", __name__)

@cardtype_bp.route("", methods=["GET"])
@cardtype_bp.route("/", methods=["GET"])
def get_all_cardtypes():
    """
    Get all card types with pagination
    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 100)
        - sort_by: Field to sort by (default: "CardType")
        - sort_order: Sort order "asc" or "desc" (default: "asc")
        - search: Search by card type name (optional)
    """
    try:
        # Get query parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 100, type=int)
        sort_by = request.args.get("sort_by", "CardType")
        sort_order = request.args.get("sort_order", "asc")
        search = request.args.get("search", "")

        # Validate per_page
        if per_page > 500:
            per_page = 500

        # Get data from service
        result = CardTypeService.get_all_cardtypes(
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

@cardtype_bp.route("/<int:cardtype_id>", methods=["GET"])
def get_cardtype_by_id(cardtype_id):
    """
    Get a card type by ID
    URL Parameters:
        - cardtype_id: Card Type ID
    """
    try:
        result = CardTypeService.get_cardtype_by_id(cardtype_id)

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500
