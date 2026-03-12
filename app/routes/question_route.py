from flask import Blueprint, jsonify, request
from app.services.question_service import QuestionService

question_bp = Blueprint("question", __name__)

@question_bp.route("", methods=["GET"])
@question_bp.route("/", methods=["GET"])
def get_all_questions():
    """
    Get all questions with pagination
    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 100)
        - sort_by: Field to sort by (default: "QuestionId")
        - sort_order: Sort order "asc" or "desc" (default: "asc")
        - topic_id: Filter by topic ID (optional, can be comma-separated: 1,2,3 or multiple params: topic_id=1&topic_id=2)
        - search: Search by question name (optional)
    """
    try:
        # Get query parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 100, type=int)
        sort_by = request.args.get("sort_by", "QuestionId")
        sort_order = request.args.get("sort_order", "asc")
        search = request.args.get("search", "")

        # Parse topic_id - support both comma-separated and multiple params
        topic_ids = None
        topic_id_param = request.args.get("topic_id")
        if topic_id_param:
            # Check if comma-separated
            if "," in topic_id_param:
                topic_ids = [int(tid.strip()) for tid in topic_id_param.split(",") if tid.strip().isdigit()]
            else:
                # Single value or multiple params
                topic_ids_list = request.args.getlist("topic_id")
                if len(topic_ids_list) > 1:
                    topic_ids = [int(tid) for tid in topic_ids_list if tid.isdigit()]
                else:
                    topic_ids = int(topic_id_param) if topic_id_param.isdigit() else None

        # Validate per_page
        if per_page > 500:
            per_page = 500

        # Get data from service
        result = QuestionService.get_all_questions(
            page=page,
            per_page=per_page,
            sort_by=sort_by,
            sort_order=sort_order,
            topic_ids=topic_ids,
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

@question_bp.route("/grouped", methods=["GET"])
def get_questions_grouped_by_topic():
    """
    Get questions grouped by topic
    Query Parameters:
        - topic_id: Filter by topic ID (optional, can be comma-separated: 1,2,3 or multiple params: topic_id=1&topic_id=2)
        - search: Search by question name (optional)
    """
    try:
        search = request.args.get("search", "")

        # Parse topic_id - support both comma-separated and multiple params
        topic_ids = None
        topic_id_param = request.args.get("topic_id")
        if topic_id_param:
            # Check if comma-separated
            if "," in topic_id_param:
                topic_ids = [int(tid.strip()) for tid in topic_id_param.split(",") if tid.strip().isdigit()]
            else:
                # Single value or multiple params
                topic_ids_list = request.args.getlist("topic_id")
                if len(topic_ids_list) > 1:
                    topic_ids = [int(tid) for tid in topic_ids_list if tid.isdigit()]
                else:
                    topic_ids = int(topic_id_param) if topic_id_param.isdigit() else None

        # Get data from service
        result = QuestionService.get_questions_grouped_by_topic(
            topic_ids=topic_ids,
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

@question_bp.route("/<int:question_id>", methods=["GET"])
def get_question_by_id(question_id):
    """
    Get question by ID
    Path Parameters:
        - question_id: Question ID
    """
    try:
        result = QuestionService.get_question_by_id(question_id)

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500
