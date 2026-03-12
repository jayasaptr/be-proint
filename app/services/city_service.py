from app.models.city import PMCity
from app import db
from sqlalchemy import asc, desc

class CityService:
    """Service layer untuk mengelola City"""

    @staticmethod
    def get_all_cities(page=1, per_page=100, sort_by="CityName", sort_order="asc", search="", state_id=None):
        """
        Get all cities with pagination and sorting

        Args:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 100)
            sort_by (str): Field to sort by (default: "CityName")
            sort_order (str): Sort order "asc" or "desc" (default: "asc")
            search (str): Search by city name or code (default: "")
            state_id (int): Filter by state ID (optional)

        Returns:
            dict: Paginated city data
        """
        try:
            # Build query
            query = PMCity.query

            # Filter by state ID if provided
            if state_id:
                query = query.filter(PMCity.CityStateId == state_id)

            # Search filter
            if search:
                query = query.filter(
                    db.or_(
                        PMCity.CityName.ilike(f"%{search}%"),
                        PMCity.CityCode.ilike(f"%{search}%")
                    )
                )

            # Apply sorting
            sort_column = getattr(PMCity, sort_by, PMCity.CityName)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

            # Paginate
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": [city.to_dict() for city in pagination.items],
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
                "message": f"Error retrieving cities: {str(e)}"
            }

    @staticmethod
    def get_city_by_id(city_id):
        """
        Get a city by ID

        Args:
            city_id (int): City ID

        Returns:
            dict: City data
        """
        try:
            city = PMCity.query.get(city_id)

            if not city:
                return {
                    "success": False,
                    "message": "City not found"
                }

            return {
                "success": True,
                "data": city.to_dict()
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error retrieving city: {str(e)}"
            }
