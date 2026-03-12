from app.models.state import PMState
from app import db
from sqlalchemy import asc, desc

class StateService:
    """Service layer untuk mengelola State/Province"""

    @staticmethod
    def get_all_states(page=1, per_page=100, sort_by="StateName", sort_order="asc", search=""):
        """
        Get all states with pagination and sorting

        Args:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 100)
            sort_by (str): Field to sort by (default: "StateName")
            sort_order (str): Sort order "asc" or "desc" (default: "asc")
            search (str): Search by state name or code (default: "")

        Returns:
            dict: Paginated state data
        """
        try:
            # Build query
            query = PMState.query

            # Search filter
            if search:
                query = query.filter(
                    db.or_(
                        PMState.StateName.ilike(f"%{search}%"),
                        PMState.StateCode.ilike(f"%{search}%")
                    )
                )

            # Apply sorting
            sort_column = getattr(PMState, sort_by, PMState.StateName)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

            # Paginate
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": [state.to_dict() for state in pagination.items],
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
                "message": f"Error retrieving states: {str(e)}"
            }

    @staticmethod
    def get_state_by_id(state_id):
        """
        Get a state by ID

        Args:
            state_id (int): State ID

        Returns:
            dict: State data
        """
        try:
            state = PMState.query.get(state_id)

            if not state:
                return {
                    "success": False,
                    "message": "State not found"
                }

            return {
                "success": True,
                "data": state.to_dict()
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving state: {str(e)}"
            }
