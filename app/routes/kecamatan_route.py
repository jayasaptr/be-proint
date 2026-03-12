from flask import Blueprint, jsonify, request
from app.services.kecamatan_service import KecamatanService

kecamatan_bp = Blueprint("kecamatan", __name__)

@kecamatan_bp.route("", methods=["GET"])
@kecamatan_bp.route("/", methods=["GET"])
def get_all_kecamatans():
    """
    Get all kecamatans with pagination
    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 100)
        - sort_by: Field to sort by (default: "KecamatanName")
        - sort_order: Sort order "asc" or "desc" (default: "asc")
        - search: Search by kecamatan name (optional)
        - city_id: Filter by CityId (optional)
    """
    try:
        # Get query parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 100, type=int)
        sort_by = request.args.get("sort_by", "KecamatanName")
        sort_order = request.args.get("sort_order", "asc")
        search = request.args.get("search", "")
        city_id = request.args.get("city_id", None, type=int)

        # Validate per_page
        if per_page > 500:
            per_page = 500

        # Get data from service
        result = KecamatanService.get_all_kecamatans(
            page=page,
            per_page=per_page,
            sort_by=sort_by,
            sort_order=sort_order,
            search=search,
            city_id=city_id
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

@kecamatan_bp.route("/<int:kecamatan_id>", methods=["GET"])
def get_kecamatan_by_id(kecamatan_id):
    """
    Get kecamatan by ID
    """
    try:
        result = KecamatanService.get_kecamatan_by_id(kecamatan_id)

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@kecamatan_bp.route("/by-city/<int:city_id>", methods=["GET"])
def get_kecamatans_by_city(city_id):
    """
    Get all kecamatans by city ID
    """
    try:
        result = KecamatanService.get_kecamatans_by_city(city_id)

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500
