from app.models.race import PMRace
from app import db
from sqlalchemy import asc, desc

class RaceService:
    """Service layer untuk mengelola Race"""

    @staticmethod
    def get_all_races(page=1, per_page=100, sort_by="Race", sort_order="asc", search=""):
        """
        Get all races with pagination and sorting

        Args:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 100)
            sort_by (str): Field to sort by (default: "Race")
            sort_order (str): Sort order "asc" or "desc" (default: "asc")
            search (str): Search by race name (default: "")

        Returns:
            dict: Paginated race data
        """
        try:
            # Build query
            query = PMRace.query

            # Search filter
            if search:
                query = query.filter(
                    PMRace.Race.ilike(f"%{search}%")
                )

            # Apply sorting
            sort_column = getattr(PMRace, sort_by, PMRace.Race)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

            # Paginate
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": [race.to_dict() for race in pagination.items],
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
                "message": f"Error retrieving races: {str(e)}"
            }

    @staticmethod
    def get_race_by_id(race_id):
        """
        Get a race by ID

        Args:
            race_id (int): Race ID

        Returns:
            dict: Race data
        """
        try:
            race = PMRace.query.get(race_id)

            if not race:
                return {
                    "success": False,
                    "message": "Race not found"
                }

            return {
                "success": True,
                "data": race.to_dict()
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving race: {str(e)}"
            }
