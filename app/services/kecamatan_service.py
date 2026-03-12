from app.models.kecamatan import PMKecamatan
from app import db
from sqlalchemy import asc, desc

class KecamatanService:
    """Service layer untuk mengelola Kecamatan"""

    @staticmethod
    def get_all_kecamatans(page=1, per_page=100, sort_by="KecamatanName", sort_order="asc", search="", city_id=None):
        """
        Get all kecamatans with pagination and sorting

        Args:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 100)
            sort_by (str): Field to sort by (default: "KecamatanName")
            sort_order (str): Sort order "asc" or "desc" (default: "asc")
            search (str): Search by kecamatan name (default: "")
            city_id (int): Filter by CityId (optional)

        Returns:
            dict: Paginated kecamatan data
        """
        try:
            # Build query
            query = PMKecamatan.query

            # Filter by CityId if provided
            if city_id:
                query = query.filter(PMKecamatan.CityId == city_id)

            # Search filter
            if search:
                query = query.filter(
                    PMKecamatan.KecamatanName.ilike(f"%{search}%")
                )

            # Apply sorting
            sort_column = getattr(PMKecamatan, sort_by, PMKecamatan.KecamatanName)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

            # Paginate
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": [kecamatan.to_dict() for kecamatan in pagination.items],
                "pagination": {
                    "page": pagination.page,
                    "per_page": pagination.per_page,
                    "total": pagination.total,
                    "pages": pagination.pages,
                    "has_next": pagination.has_next,
                    "has_prev": pagination.has_prev
                }
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error fetching kecamatans: {str(e)}"
            }

    @staticmethod
    def get_kecamatan_by_id(kecamatan_id):
        """
        Get kecamatan by ID

        Args:
            kecamatan_id (int): Kecamatan ID

        Returns:
            dict: Kecamatan data
        """
        try:
            kecamatan = PMKecamatan.query.get(kecamatan_id)

            if not kecamatan:
                return {
                    "success": False,
                    "message": "Kecamatan not found"
                }

            return {
                "success": True,
                "data": kecamatan.to_dict()
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error fetching kecamatan: {str(e)}"
            }

    @staticmethod
    def get_kecamatans_by_city(city_id):
        """
        Get all kecamatans by city ID

        Args:
            city_id (int): City ID

        Returns:
            dict: List of kecamatans for the city
        """
        try:
            kecamatans = PMKecamatan.query.filter_by(CityId=city_id).order_by(PMKecamatan.KecamatanName).all()

            return {
                "success": True,
                "data": [kecamatan.to_dict() for kecamatan in kecamatans]
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Error fetching kecamatans by city: {str(e)}"
            }
