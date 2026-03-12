from app.models.edulevel import PMEduLevel
from app import db
from sqlalchemy import asc, desc

class EduLevelService:
    """Service layer untuk mengelola Education Level"""

    @staticmethod
    def get_all_edulevels(page=1, per_page=100, sort_by="EduLevel", sort_order="asc", active_only=True, search=""):
        """
        Get all education levels with pagination and sorting

        Args:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 100)
            sort_by (str): Field to sort by (default: "EduLevel")
            sort_order (str): Sort order "asc" or "desc" (default: "asc")
            active_only (bool): Filter only active records (default: True)
            search (str): Search by name (default: "")

        Returns:
            dict: Paginated education levels data
        """
        try:
            # Build query
            query = PMEduLevel.query

            # Filter active only if requested
            if active_only:
                query = query.filter(PMEduLevel.FgActive == "Y")

            # Search filter
            if search:
                query = query.filter(PMEduLevel.EduLvlName.ilike(f"%{search}%"))

            # Apply sorting
            sort_column = getattr(PMEduLevel, sort_by, PMEduLevel.EduLevel)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

            # Paginate
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": [edu.to_dict() for edu in pagination.items],
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
                "message": f"Error fetching education levels: {str(e)}"
            }

    @staticmethod
    def get_edulevel_by_id(edu_lvl_id):
        """
        Get education level by ID

        Args:
            edu_lvl_id (str): Education level ID

        Returns:
            dict: Education level data or error message
        """
        try:
            edu_level = PMEduLevel.query.filter_by(EduLvlId=edu_lvl_id).first()

            if not edu_level:
                return {
                    "success": False,
                    "message": "Education level not found"
                }

            return {
                "success": True,
                "data": edu_level.to_dict()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error fetching education level: {str(e)}"
            }

    @staticmethod
    def get_all_active_edulevels():
        """
        Get all active education levels (simplified, no pagination)

        Returns:
            dict: All active education levels
        """
        try:
            edu_levels = PMEduLevel.query.filter_by(FgActive="Y").order_by(asc(PMEduLevel.EduLevel)).all()

            return {
                "success": True,
                "data": [edu.to_dict() for edu in edu_levels]
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error fetching education levels: {str(e)}"
            }
