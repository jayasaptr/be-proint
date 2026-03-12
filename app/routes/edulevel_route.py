from flask import Blueprint, jsonify, request
from app.services.edulevel_service import EduLevelService

edulevel_bp = Blueprint("edulevel", __name__)

@edulevel_bp.route("", methods=["GET"])
@edulevel_bp.route("/", methods=["GET"])
def get_all_edulevels():
    """
    Get all education levels with pagination
    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 100)
        - sort_by: Field to sort by (default: "EduLevel")
        - sort_order: Sort order "asc" or "desc" (default: "asc")
        - active_only: Filter only active records (default: true)
        - search: Search by name (optional)
    """
    try:
        # Get query parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 100, type=int)
        sort_by = request.args.get("sort_by", "EduLevel")
        sort_order = request.args.get("sort_order", "asc")
        active_only = request.args.get("active_only", "true").lower() == "true"
        search = request.args.get("search", "")

        # Validate per_page
        if per_page > 500:
            per_page = 500

        # Get data from service
        result = EduLevelService.get_all_edulevels(
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

@edulevel_bp.route("/<edu_lvl_id>", methods=["GET"])
def get_edulevel_by_id(edu_lvl_id):
    """
    Get education level by ID
    """
    try:
        result = EduLevelService.get_edulevel_by_id(edu_lvl_id)

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@edulevel_bp.route("/active/all", methods=["GET"])
def get_all_active():
    """
    Get all active education levels (no pagination)
    """
    try:
        result = EduLevelService.get_all_active_edulevels()

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@edulevel_bp.route("/debug/raw", methods=["GET"])
def get_raw_data():
    """
    Debug endpoint - Get raw data tanpa filter (max 10 records)
    """
    try:
        from app.models.edulevel import PMEduLevel
        from app import db

        # Query tanpa filter
        edu_levels = PMEduLevel.query.limit(10).all()

        return jsonify({
            "success": True,
            "count": len(edu_levels),
            "data": [edu.to_dict() for edu in edu_levels],
            "info": "Raw data dari database (max 10 records)"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}",
            "type": str(type(e).__name__)
        }), 500

@edulevel_bp.route("/debug/count", methods=["GET"])
def get_count():
    """
    Debug endpoint - Get total count
    """
    try:
        from app.models.edulevel import PMEduLevel

        total = PMEduLevel.query.count()
        active_count = PMEduLevel.query.filter(PMEduLevel.FgActive == "1").count()

        return jsonify({
            "success": True,
            "total_records": total,
            "active_records": active_count,
            "info": "Total dan Active count"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}",
            "type": str(type(e).__name__)
        }), 500
