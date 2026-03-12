from app.models.edumajor import PMEduMajor
from app import db
from sqlalchemy import asc, desc

class EduMajorService:
    """Service layer untuk mengelola Education Major"""

    @staticmethod
    def get_all_edumajors(page=1, per_page=100, sort_by="EduMjrName", sort_order="asc", active_only=True, search=""):
        """
        Get all education majors with pagination and sorting

        Args:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 100)
            sort_by (str): Field to sort by (default: "EduMjrName")
            sort_order (str): Sort order "asc" or "desc" (default: "asc")
            active_only (bool): Filter only active records (default: True)
            search (str): Search by name (default: "")

        Returns:
            dict: Paginated education majors data
        """
        try:
            # Build query
            query = PMEduMajor.query

            # Filter active only if requested
            if active_only:
                query = query.filter(PMEduMajor.FgActive == "Y")

            # Search filter
            if search:
                query = query.filter(PMEduMajor.EduMjrName.ilike(f"%{search}%"))

            # Apply sorting
            sort_column = getattr(PMEduMajor, sort_by, PMEduMajor.EduMjrName)
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
                "message": f"Error retrieving education majors: {str(e)}"
            }

    @staticmethod
    def get_edumajor_by_id(edu_mjr_id):
        """
        Get education major by ID

        Args:
            edu_mjr_id (int): Education major ID

        Returns:
            dict: Education major data or error message
        """
        try:
            edu_major = PMEduMajor.query.get(edu_mjr_id)

            if not edu_major:
                return {
                    "success": False,
                    "message": "Education major not found"
                }

            return {
                "success": True,
                "data": edu_major.to_dict()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving education major: {str(e)}"
            }
