from app.models.vacantpos import RCEVacantPos
from app.models.posadtgrpmbr import RCEPosAdtGrpMbr
from app.models.posadtgrpdt import RCEPosAdtGrpDt
from app.models.posadtgrphd import RCEPosAdtGrpHd
from app import db
from sqlalchemy import asc, desc, and_, or_
from sqlalchemy.orm import joinedload
from datetime import datetime

class VacantPosService:
    """Service layer untuk mengelola Vacant Position"""

    @staticmethod
    def get_all_vacancies(page=1, per_page=100, sort_by="VacantPositionName", sort_order="asc", search="", posadt_grp_id=None, posadt_type_id=None, include_relations=False, exclude_expired=True):
        """
        Get all vacancies with pagination and sorting
        Filtered by FgActive and FgShowVacant != 'N'

        Args:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 100)
            sort_by (str): Field to sort by (default: "VacantPositionName")
            sort_order (str): Sort order "asc" or "desc" (default: "asc")
            search (str): Search by position name or code (default: "")
            posadt_grp_id (list): Filter by PosAdtGrpId (optional, can be multiple, uses AND logic - all must match)
            posadt_type_id (list): Filter by PosAdtTypeId (optional, can be multiple, uses AND logic - all must match)
            include_relations (bool): Include related position audit group data (default: False)
            exclude_expired (bool): Exclude vacancies with VacantExpDate < current date (default: True)

        Returns:
            dict: Paginated vacancy data
        """
        try:
            # Build query with filters for active and show vacant
            query = RCEVacantPos.query.filter(
                and_(
                    RCEVacantPos.FgActive == 'Y',
                    RCEVacantPos.FgShowVacant != 'N'
                )
            )

            # Filter out expired vacancies if requested
            if exclude_expired:
                current_date = datetime.now()
                query = query.filter(
                    or_(
                        RCEVacantPos.VacantExpDate >= current_date,
                        RCEVacantPos.VacantExpDate.is_(None)
                    )
                )

            # Eager load relationships if requested
            if include_relations:
                query = query.options(
                    joinedload(RCEVacantPos.posadt_members)
                    .joinedload(RCEPosAdtGrpMbr.posadt_grp_dt)
                ).options(
                    joinedload(RCEVacantPos.posadt_members)
                    .joinedload(RCEPosAdtGrpMbr.posadt_grp_hd)
                )

            # Filter by PosAdtGrpId or PosAdtTypeId if provided
            # Using subquery to ensure ALL conditions are met (AND logic)
            if posadt_grp_id or posadt_type_id:
                subquery_filters = []

                # For each posadt_grp_id, create a subquery to check if vacancy has that group
                if posadt_grp_id:
                    for grp_id in posadt_grp_id:
                        subq = db.session.query(RCEPosAdtGrpMbr.VacantPosId).filter(
                            RCEPosAdtGrpMbr.PosAdtGrpId == grp_id
                        )
                        query = query.filter(RCEVacantPos.VacantPosId.in_(subq))

                # For each posadt_type_id, create a subquery to check if vacancy has that type
                if posadt_type_id:
                    for type_id in posadt_type_id:
                        subq = db.session.query(RCEPosAdtGrpMbr.VacantPosId).filter(
                            RCEPosAdtGrpMbr.PosAdtTypeId == type_id
                        )
                        query = query.filter(RCEVacantPos.VacantPosId.in_(subq))

            # Search filter
            if search:
                query = query.filter(
                    db.or_(
                        RCEVacantPos.VacantPositionName.ilike(f"%{search}%"),
                        RCEVacantPos.VacantPosCode.ilike(f"%{search}%")
                    )
                )

            # Apply sorting
            sort_column = getattr(RCEVacantPos, sort_by, RCEVacantPos.VacantPositionName)
            if sort_order.lower() == "desc":
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))

            # Paginate
            pagination = query.paginate(page=page, per_page=per_page, error_out=False)

            return {
                "success": True,
                "data": [vacancy.to_dict(include_relations=include_relations) for vacancy in pagination.items],
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
                "message": f"Error getting vacancies: {str(e)}"
            }

    @staticmethod
    def get_vacancy_by_id(vacancy_id, include_relations=False):
        """
        Get vacancy by ID

        Args:
            vacancy_id (int): Vacancy ID
            include_relations (bool): Include related position audit group data (default: False)

        Returns:
            dict: Vacancy data or error message
        """
        try:
            query = RCEVacantPos.query

            # Eager load relationships if requested
            if include_relations:
                query = query.options(
                    joinedload(RCEVacantPos.posadt_members)
                    .joinedload(RCEPosAdtGrpMbr.posadt_grp_dt)
                ).options(
                    joinedload(RCEVacantPos.posadt_members)
                    .joinedload(RCEPosAdtGrpMbr.posadt_grp_hd)
                )

            vacancy = query.get(vacancy_id)
            if not vacancy:
                return {
                    "success": False,
                    "message": "Vacancy not found"
                }

            return {
                "success": True,
                "data": vacancy.to_dict(include_relations=include_relations)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error getting vacancy: {str(e)}"
            }
