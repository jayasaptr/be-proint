from flask import Blueprint, jsonify, request
from app.services.posadtgrphd_service import PosAdtGrpHdService

posadtgrphd_bp = Blueprint("posadtgrphd", __name__)

@posadtgrphd_bp.route("", methods=["GET"])
@posadtgrphd_bp.route("/", methods=["GET"])
def get_all_posadtgrphd():
    """
    Get all position audit group headers with pagination
    Filtered by FgShowOnSummary != 'N'

    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 100)
        - sort_by: Field to sort by (default: "PosAdtName")
        - sort_order: Sort order "asc" or "desc" (default: "asc")
        - search: Search by name or type (optional)
    """
    try:
        # Get query parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 100, type=int)
        sort_by = request.args.get("sort_by", "PosAdtName")
        sort_order = request.args.get("sort_order", "asc")
        search = request.args.get("search", "")

        # Validate per_page
        if per_page > 500:
            per_page = 500

        # Get data from service
        result = PosAdtGrpHdService.get_all_posadtgrphd(
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

@posadtgrphd_bp.route("/<int:posadt_type_id>", methods=["GET"])
def get_posadtgrphd_by_id(posadt_type_id):
    """
    Get position audit group header by ID

    Parameters:
        - posadt_type_id: Position Audit Type ID
    """
    try:
        result = PosAdtGrpHdService.get_posadtgrphd_by_id(posadt_type_id)

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500
