from flask import Blueprint, jsonify, request
from app.services.questtopic_service import QuestTopicService

questtopic_bp = Blueprint("questtopic", __name__)

@questtopic_bp.route("", methods=["GET"])
@questtopic_bp.route("/", methods=["GET"])
def get_all_topics():
    """
    Get all question topics with pagination
    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 100)
        - sort_by: Field to sort by (default: "QTopicName")
        - sort_order: Sort order "asc" or "desc" (default: "asc")
        - search: Search by name (optional)
        - include_questions: Include related questions (default: false)
    """
    try:
        # Get query parameters
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 100, type=int)
        sort_by = request.args.get("sort_by", "QTopicName")
        sort_order = request.args.get("sort_order", "asc")
        search = request.args.get("search", "")
        include_questions = request.args.get("include_questions", "false").lower() == "true"

        # Validate per_page
        if per_page > 500:
            per_page = 500

        # Get data from service
        result = QuestTopicService.get_all_topics(
            page=page,
            per_page=per_page,
            sort_by=sort_by,
            sort_order=sort_order,
            search=search,
            include_questions=include_questions
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

@questtopic_bp.route("/<int:topic_id>", methods=["GET"])
def get_topic_by_id(topic_id):
    """
    Get question topic by ID
    Path Parameters:
        - topic_id: Topic ID
    Query Parameters:
        - include_questions: Include related questions (default: false)
    """
    try:
        include_questions = request.args.get("include_questions", "false").lower() == "true"
        result = QuestTopicService.get_topic_by_id(topic_id, include_questions=include_questions)

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500
