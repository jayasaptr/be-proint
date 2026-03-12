from app.models.question import RCQuestion
from app.models.questtopic import RCQuestTopic
from app import db
from sqlalchemy import asc, desc

class QuestionService:
    """Service layer untuk mengelola Question"""

    @staticmethod
    def get_all_questions(page=1, per_page=100, sort_by="QuestionId", sort_order="asc", topic_ids=None, search=""):
        """
        Get all questions with pagination and sorting

        Args:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 100)
            sort_by (str): Field to sort by (default: "QuestionId")
            sort_order (str): Sort order "asc" or "desc" (default: "asc")
            topic_ids (list): Filter by topic IDs (optional, can be single or multiple)
            search (str): Search by question name (default: "")

        Returns:
            dict: Paginated questions data
        """
        try:
            # Build query
            query = RCQuestion.query

            # Filter by topic if provided
            if topic_ids:
                if isinstance(topic_ids, list) and len(topic_ids) > 0:
                    query = query.filter(RCQuestion.QTopicId.in_(topic_ids))
                else:
                    query = query.filter(RCQuestion.QTopicId == topic_ids)

            # Search filter
            if search:
                query = query.filter(RCQuestion.QuestName.ilike(f"%{search}%"))

            # Apply sorting
            sort_column = getattr(RCQuestion, sort_by, RCQuestion.QuestionId)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

            # Paginate
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": [question.to_dict(include_topic=True) for question in pagination.items],
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
                "message": f"Error retrieving questions: {str(e)}"
            }

    @staticmethod
    def get_question_by_id(question_id):
        """
        Get question by ID

        Args:
            question_id (int): Question ID

        Returns:
            dict: Question data or error message
        """
        try:
            question = RCQuestion.query.get(question_id)

            if not question:
                return {
                    "success": False,
                    "message": "Question not found"
                }

            return {
                "success": True,
                "data": question.to_dict(include_topic=True)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving question: {str(e)}"
            }

    @staticmethod
    def get_questions_grouped_by_topic(topic_ids=None, search=""):
        """
        Get questions grouped by topic

        Args:
            topic_ids (list): Filter by topic IDs (optional, can be single or multiple)
            search (str): Search by question name (default: "")

        Returns:
            dict: Questions grouped by topic
        """
        try:
            from app.models.questtopic import RCQuestTopic

            # Build query for topics
            topic_query = RCQuestTopic.query

            # Filter by topic IDs if provided
            if topic_ids:
                if isinstance(topic_ids, list) and len(topic_ids) > 0:
                    topic_query = topic_query.filter(RCQuestTopic.QTopicId.in_(topic_ids))
                else:
                    topic_query = topic_query.filter(RCQuestTopic.QTopicId == topic_ids)

            # Get all matching topics
            topics = topic_query.order_by(RCQuestTopic.QTopicName).all()

            result_data = []

            for topic in topics:
                # Build query for questions
                question_query = RCQuestion.query.filter(RCQuestion.QTopicId == topic.QTopicId)

                # Search filter
                if search:
                    question_query = question_query.filter(RCQuestion.QuestName.ilike(f"%{search}%"))

                # Order by QuestRow
                question_query = question_query.order_by(RCQuestion.QuestRow)

                questions = question_query.all()

                # Only include topics that have questions (or all if no search)
                if questions or not search:
                    result_data.append({
                        "topic": {
                            "QTopicId": topic.QTopicId,
                            "QTopicCode": topic.QTopicCode,
                            "QTopicName": topic.QTopicName,
                            "UpdDate": topic.UpdDate.isoformat() if topic.UpdDate else None,
                            "UpdUser": topic.UpdUser,
                            "UpdFlag": topic.UpdFlag,
                        },
                        "questions": [{
                            "QuestionId": q.QuestionId,
                            "QTopicId": q.QTopicId,
                            "QuestCode": q.QuestCode,
                            "QuestName": q.QuestName,
                            "FgAnsMode": q.FgAnsMode,
                            "UpdDate": q.UpdDate.isoformat() if q.UpdDate else None,
                            "UpdUser": q.UpdUser,
                            "UpdFlag": q.UpdFlag,
                            "QuestRow": q.QuestRow,
                        } for q in questions]
                    })

            return {
                "success": True,
                "data": result_data
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving questions by topic: {str(e)}"
            }
