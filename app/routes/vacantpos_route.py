from flask import Blueprint, jsonify, request
from app.services.vacantpos_service import VacantPosService

vacantpos_bp = Blueprint("vacantpos", __name__)

@vacantpos_bp.route("", methods=["GET"])
@vacantpos_bp.route("/", methods=["GET"])
def get_all_vacancies():
    """
    Get all vacancies with pagination
    Filtered by FgActive = 'Y' and FgShowVacant != 'N'

    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 100)
        - sort_by: Field to sort by (default: "VacantPositionName")
        - sort_order: Sort order "asc" or "desc" (default: "asc")
        - search: Search by position name or code (optional)
        - posadt_grp_id: Filter by PosAdtGrpId (optional, can be multiple: ?posadt_grp_id=1&posadt_grp_id=2).
          OR within the same category (PosAdtTypeId), AND across categories.
        - posadt_type_id: Filter by PosAdtTypeId (optional, can be multiple: ?posadt_type_id=1&posadt_type_id=2).
          Vacancy must have at least one attribute of any selected type (OR).
        - include_relations: Include related position audit group data "true" or "false" (default: "false")
        - exclude_expired: Exclude vacancies with VacantExpDate < current date "true" or "false" (default: "true")
        - ftap_first: Put FTAP vacancies at the top before sort_by "true" or "false" (default: "true")
    """
    try:
        # Get query parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 100, type=int)
        sort_by = request.args.get("sort_by", "VacantPositionName")
        sort_order = request.args.get("sort_order", "asc")
        search = request.args.get("search", "")
        posadt_grp_id = request.args.getlist("posadt_grp_id", type=int)
        posadt_type_id = request.args.getlist("posadt_type_id", type=int)
        include_relations = request.args.get("include_relations", "false").lower() == "true"
        exclude_expired = request.args.get("exclude_expired", "true").lower() == "true"
        ftap_first = request.args.get("ftap_first", "true").lower() == "true"

        # Validate per_page
        if per_page > 500:
            per_page = 500

        # Get data from service
        result = VacantPosService.get_all_vacancies(
            page=page,
            per_page=per_page,
            sort_by=sort_by,
            sort_order=sort_order,
            search=search,
            posadt_grp_id=posadt_grp_id,
            posadt_type_id=posadt_type_id,
            include_relations=include_relations,
            exclude_expired=exclude_expired,
            ftap_first=ftap_first
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

@vacantpos_bp.route("/<int:vacancy_id>", methods=["GET"])
def get_vacancy_by_id(vacancy_id):
    """
    Get vacancy by ID

    Parameters:
        - vacancy_id: Vacancy ID

    Query Parameters:
        - include_relations: Include related position audit group data "true" or "false" (default: "false")
    """
    try:
        include_relations = request.args.get("include_relations", "false").lower() == "true"
        result = VacantPosService.get_vacancy_by_id(vacancy_id, include_relations=include_relations)

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500
