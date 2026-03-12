from app.models.religion import PMReligion
from app import db
from sqlalchemy import asc, desc

class ReligionService:
    """Service layer untuk mengelola Religion"""

    @staticmethod
    def get_all_religions(page=1, per_page=100, sort_by="Religion", sort_order="asc", search=""):
        """
        Get all religions with pagination and sorting

        Args:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 100)
            sort_by (str): Field to sort by (default: "Religion")
            sort_order (str): Sort order "asc" or "desc" (default: "asc")
            search (str): Search by religion name (default: "")

        Returns:
            dict: Paginated religion data
        """
        try:
            # Build query
            query = PMReligion.query

            # Search filter
            if search:
                query = query.filter(
                    PMReligion.Religion.ilike(f"%{search}%")
                )

            # Apply sorting
            sort_column = getattr(PMReligion, sort_by, PMReligion.Religion)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

            # Paginate
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": [religion.to_dict() for religion in pagination.items],
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
                "message": f"Error retrieving religions: {str(e)}"
            }

    @staticmethod
    def get_religion_by_id(religion_id):
        """
        Get a religion by ID

        Args:
            religion_id (int): Religion ID

        Returns:
            dict: Religion data
        """
        try:
            religion = PMReligion.query.get(religion_id)

            if not religion:
                return {
                    "success": False,
                    "message": "Religion not found"
                }

            return {
                "success": True,
                "data": religion.to_dict()
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving religion: {str(e)}"
            }
