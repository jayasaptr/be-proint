from app.models.maritalstatus import PMMaritalSt
from app import db
from sqlalchemy import asc, desc

class MaritalStatusService:
    """Service layer untuk mengelola Marital Status"""

    @staticmethod
    def get_all_maritalstatuses(page=1, per_page=100, sort_by="MaritalSt", sort_order="asc", search=""):
        """
        Get all marital statuses with pagination and sorting

        Args:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 100)
            sort_by (str): Field to sort by (default: "MaritalSt")
            sort_order (str): Sort order "asc" or "desc" (default: "asc")
            search (str): Search by name (default: "")

        Returns:
            dict: Paginated marital status data
        """
        try:
            # Build query
            query = PMMaritalSt.query

            # Search filter
            if search:
                query = query.filter(PMMaritalSt.MaritalSt.ilike(f"%{search}%"))

            # Apply sorting
            sort_column = getattr(PMMaritalSt, sort_by, PMMaritalSt.MaritalSt)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

            # Paginate
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": [status.to_dict() for status in pagination.items],
                "pagination": {
                    "page": pagination.page,
                    "per_page": pagination.per_page,
                    "total_pages": pagination.pages,
                    "total_items": pagination.total,
                    "has_next": pagination.has_next,
                    "has_prev": pagination.has_prev
                }
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving marital statuses: {str(e)}"
            }
