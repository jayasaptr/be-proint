from app.models.posadtgrpdt import RCEPosAdtGrpDt
from app.models.posadtgrphd import RCEPosAdtGrpHd
from app import db
from sqlalchemy import asc, desc

class PosAdtGrpDtService:
    """Service layer untuk mengelola Position Audit Group Detail"""

    @staticmethod
    def get_all_posadtgrpdt(page=1, per_page=100, sort_by="PosAdtGrpName", sort_order="asc", search="", include_header=False, posadt_type_id=None):
        """
        Get all position audit group details with pagination and sorting

        Args:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 100)
            sort_by (str): Field to sort by (default: "PosAdtGrpName")
            sort_order (str): Sort order "asc" or "desc" (default: "asc")
            search (str): Search by name or code (default: "")
            include_header (bool): Include related header data (default: False)
            posadt_type_id (list): Filter by PosAdtTypeId (optional, can be multiple)

        Returns:
            dict: Paginated position audit group detail data
        """
        try:
            # Build query with join to RCEPosAdtGrpHd
            query = RCEPosAdtGrpDt.query.join(
                RCEPosAdtGrpHd,
                RCEPosAdtGrpDt.PosAdtTypeId == RCEPosAdtGrpHd.PosAdtTypeId
            )

            # Filter by PosAdtTypeId if provided
            if posadt_type_id:
                query = query.filter(RCEPosAdtGrpDt.PosAdtTypeId.in_(posadt_type_id))

            # Search filter
            if search:
                query = query.filter(
                    db.or_(
                        RCEPosAdtGrpDt.PosAdtGrpName.ilike(f"%{search}%"),
                        RCEPosAdtGrpDt.PosAdtGrpCode.ilike(f"%{search}%"),
                        RCEPosAdtGrpHd.PosAdtName.ilike(f"%{search}%")
                    )
                )

            # Apply sorting
            sort_column = getattr(RCEPosAdtGrpDt, sort_by, RCEPosAdtGrpDt.PosAdtGrpName)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

            # Paginate
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": [item.to_dict(include_header=include_header) for item in pagination.items],
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
                "message": f"Error getting position audit group details: {str(e)}"
            }

    @staticmethod
    def get_posadtgrpdt_by_id(posadt_grp_id, include_header=False):
        """
        Get position audit group detail by ID

        Args:
            posadt_grp_id (int): Position Audit Group ID
            include_header (bool): Include related header data (default: False)

        Returns:
            dict: Position audit group detail data or error message
        """
        try:
            item = RCEPosAdtGrpDt.query.get(posadt_grp_id)
            if not item:
                return {
                    "success": False,
                    "message": "Position audit group detail not found"
                }

            return {
                "success": True,
                "data": item.to_dict(include_header=include_header)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error getting position audit group detail: {str(e)}"
            }

    @staticmethod
    def get_by_posadt_type_id(posadt_type_id, include_header=False):
        """
        Get all position audit group details by PosAdtTypeId

        Args:
            posadt_type_id (int): Position Audit Type ID
            include_header (bool): Include related header data (default: False)

        Returns:
            dict: List of position audit group details
        """
        try:
            items = RCEPosAdtGrpDt.query.filter_by(PosAdtTypeId=posadt_type_id).all()

            return {
                "success": True,
                "data": [item.to_dict(include_header=include_header) for item in items],
                "total": len(items)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error getting position audit group details by type: {str(e)}"
            }
