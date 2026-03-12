from app.models.posadtgrphd import RCEPosAdtGrpHd
from app import db
from sqlalchemy import asc, desc

class PosAdtGrpHdService:
    """Service layer untuk mengelola Position Audit Group Header"""

    @staticmethod
    def get_all_posadtgrphd(page=1, per_page=100, sort_by="PosAdtName", sort_order="asc", search=""):
        """
        Get all position audit group headers with pagination and sorting
        Filtered by FgShowOnSummary != 'N'

        Args:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 100)
            sort_by (str): Field to sort by (default: "PosAdtName")
            sort_order (str): Sort order "asc" or "desc" (default: "asc")
            search (str): Search by name or type (default: "")

        Returns:
            dict: Paginated position audit group header data
        """
        try:
            # Build query with filter for FgShowOnSummary
            query = RCEPosAdtGrpHd.query.filter(
                RCEPosAdtGrpHd.FgShowOnSummary != 'N'
            )

            # Search filter
            if search:
                query = query.filter(
                    db.or_(
                        RCEPosAdtGrpHd.PosAdtName.ilike(f"%{search}%"),
                        RCEPosAdtGrpHd.PosAdtType.ilike(f"%{search}%")
                    )
                )

            # Apply sorting
            sort_column = getattr(RCEPosAdtGrpHd, sort_by, RCEPosAdtGrpHd.PosAdtName)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

            # Paginate
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": [item.to_dict() for item in pagination.items],
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
                "message": f"Error getting position audit group headers: {str(e)}"
            }

    @staticmethod
    def get_posadtgrphd_by_id(posadt_type_id):
        """
        Get position audit group header by ID

        Args:
            posadt_type_id (int): Position Audit Type ID

        Returns:
            dict: Position audit group header data or error message
        """
        try:
            item = RCEPosAdtGrpHd.query.get(posadt_type_id)
            if not item:
                return {
                    "success": False,
                    "message": "Position audit group header not found"
                }

            return {
                "success": True,
                "data": item.to_dict()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error getting position audit group header: {str(e)}"
            }
