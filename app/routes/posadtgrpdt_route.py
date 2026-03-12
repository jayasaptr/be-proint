from flask import Blueprint, jsonify, request
from app.services.posadtgrpdt_service import PosAdtGrpDtService

posadtgrpdt_bp = Blueprint("posadtgrpdt", __name__)

@posadtgrpdt_bp.route("", methods=["GET"])
@posadtgrpdt_bp.route("/", methods=["GET"])
def get_all_posadtgrpdt():
    """
    Get all position audit group details with pagination

    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 100)
        - sort_by: Field to sort by (default: "PosAdtGrpName")
        - sort_order: Sort order "asc" or "desc" (default: "asc")
        - search: Search by name or code (optional)
        - include_header: Include related header data "true" or "false" (default: "false")
        - posadt_type_id: Filter by PosAdtTypeId (optional)
    """
    try:
        # Get query parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 100, type=int)
        sort_by = request.args.get("sort_by", "PosAdtGrpName")
        sort_order = request.args.get("sort_order", "asc")
        search = request.args.get("search", "")
        include_header = request.args.get("include_header", "false").lower() == "true"
        posadt_type_id = request.args.get("posadt_type_id", type=int)

        # Validate per_page
        if per_page > 500:
            per_page = 500

        # Get data from service
        result = PosAdtGrpDtService.get_all_posadtgrpdt(
            page=page,
            per_page=per_page,
            sort_by=sort_by,
            sort_order=sort_order,
            search=search,
            include_header=include_header,
            posadt_type_id=posadt_type_id
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

@posadtgrpdt_bp.route("/<int:posadt_grp_id>", methods=["GET"])
def get_posadtgrpdt_by_id(posadt_grp_id):
    """
    Get position audit group detail by ID

    Parameters:
        - posadt_grp_id: Position Audit Group ID

    Query Parameters:
        - include_header: Include related header data "true" or "false" (default: "false")
    """
    try:
        include_header = request.args.get("include_header", "false").lower() == "true"
        result = PosAdtGrpDtService.get_posadtgrpdt_by_id(posadt_grp_id, include_header=include_header)

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@posadtgrpdt_bp.route("/by-type/<int:posadt_type_id>", methods=["GET"])
def get_by_type(posadt_type_id):
    """
    Get all position audit group details by PosAdtTypeId

    Parameters:
        - posadt_type_id: Position Audit Type ID

    Query Parameters:
        - include_header: Include related header data "true" or "false" (default: "false")
    """
    try:
        include_header = request.args.get("include_header", "false").lower() == "true"
        result = PosAdtGrpDtService.get_by_posadt_type_id(posadt_type_id, include_header=include_header)

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500
