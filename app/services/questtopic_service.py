from app.models.questtopic import RCQuestTopic
from app import db
from sqlalchemy import asc, desc

class QuestTopicService:
    """Service layer untuk mengelola Question Topic"""

    @staticmethod
    def get_all_topics(page=1, per_page=100, sort_by="QTopicName", sort_order="asc", search="", include_questions=False):
        """
        Get all question topics with pagination and sorting

        Args:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 100)
            sort_by (str): Field to sort by (default: "QTopicName")
            sort_order (str): Sort order "asc" or "desc" (default: "asc")
            search (str): Search by name (default: "")
            include_questions (bool): Include related questions (default: False)

        Returns:
            dict: Paginated question topics data
        """
        try:
            # Build query
            query = RCQuestTopic.query

            # Search filter
            if search:
                query = query.filter(RCQuestTopic.QTopicName.ilike(f"%{search}%"))

            # Apply sorting
            sort_column = getattr(RCQuestTopic, sort_by, RCQuestTopic.QTopicName)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

            # Paginate
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": [topic.to_dict(include_questions=include_questions) for topic in pagination.items],
                "pagination": {
                    "page": pagination.page,
                    "per_page": pagination.per_page,
                    "total": pagination.total,
                    "pages": pagination.pages,
                    "has_next": pagination.has_next,
                    "has_prev": pagination.has_prev,
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving question topics: {str(e)}"
            }

    @staticmethod
    def get_topic_by_id(topic_id, include_questions=False):
        """
        Get question topic by ID

        Args:
            topic_id (int): Topic ID
            include_questions (bool): Include related questions (default: False)

        Returns:
            dict: Topic data or error message
        """
        try:
            topic = RCQuestTopic.query.get(topic_id)

            if not topic:
                return {
                    "success": False,
                    "message": "Question topic not found"
                }

            return {
                "success": True,
                "data": topic.to_dict(include_questions=include_questions)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving question topic: {str(e)}"
            }
