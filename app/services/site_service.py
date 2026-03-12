from app.models.site import RCOrgRecMs
from app import db
from sqlalchemy import asc, desc

class SiteService:
    """Service layer untuk mengelola Site"""

    @staticmethod
    def get_all_sites(page=1, per_page=100, sort_by="OrgRecName", sort_order="asc", search=""):
        """
        Get all sites with pagination and sorting

        Args:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 100)
            sort_by (str): Field to sort by (default: "OrgRecName")
            sort_order (str): Sort order "asc" or "desc" (default: "asc")
            search (str): Search by site name or code (default: "")

        Returns:
            dict: Paginated site data
        """
        try:
            # Build query
            query = RCOrgRecMs.query

            # Search filter
            if search:
                query = query.filter(
                    db.or_(
                        RCOrgRecMs.OrgRecName.ilike(f"%{search}%"),
                        RCOrgRecMs.OrgRecCode.ilike(f"%{search}%")
                    )
                )

            # Apply sorting
            sort_column = getattr(RCOrgRecMs, sort_by, RCOrgRecMs.OrgRecName)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

            # Paginate
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": [site.to_dict() for site in pagination.items],
                "pagination": {
                    "page": pagination.page,
                    "per_page": pagination.per_page,
                    "total": pagination.total,
                    "pages": pagination.pages,
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error getting sites: {str(e)}"
            }

    @staticmethod
    def get_site_by_id(site_id):
        """
        Get site by ID

        Args:
            site_id (int): Site ID

        Returns:
            dict: Site data or error message
        """
        try:
            site = RCOrgRecMs.query.get(site_id)
            if not site:
                return {
                    "success": False,
                    "message": "Site not found"
                }

            return {
                "success": True,
                "data": site.to_dict()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error getting site: {str(e)}"
            }
