from app.models.vacantpos import RCEVacantPos
from app.models.posadtgrpmbr import RCEPosAdtGrpMbr
from app.models.posadtgrpdt import RCEPosAdtGrpDt
from app.models.posadtgrphd import RCEPosAdtGrpHd
from app import db
from sqlalchemy import asc, desc, and_, or_, case
from sqlalchemy.orm import joinedload
from datetime import datetime

# Aturan identifikasi lowongan FTAP (Future Talent Acceleration Program).
# Disamakan dengan App\Support\FtapProgram di api-erecruitment-dh:
#   - nama lowongan mengandung "FTAP", atau
#   - punya grup atribut yang namanya diawali "FTAP", atau
#   - tipe grup atributnya bernama "Future Talent ...".
FTAP_VACANCY_NAME_PATTERN = "%FTAP%"
FTAP_GROUP_NAME_PATTERN = "FTAP%"
FTAP_GROUP_TYPE_PATTERN = "Future Talent%"


class VacantPosService:
    """Service layer untuk mengelola Vacant Position"""

    @staticmethod
    def _ftap_vacancy_ids():
        """
        Kumpulan VacantPosId yang termasuk FTAP berdasarkan grup atributnya.
        Dipakai sebagai daftar literal di ORDER BY agar tidak perlu subquery di
        klausa ORDER BY (SQL Server menolaknya pada query tertentu).
        """
        rows = (
            db.session.query(RCEPosAdtGrpMbr.VacantPosId)
            .join(RCEPosAdtGrpDt, RCEPosAdtGrpDt.PosAdtGrpId == RCEPosAdtGrpMbr.PosAdtGrpId)
            .outerjoin(RCEPosAdtGrpHd, RCEPosAdtGrpHd.PosAdtTypeId == RCEPosAdtGrpDt.PosAdtTypeId)
            .filter(
                or_(
                    RCEPosAdtGrpDt.PosAdtGrpName.like(FTAP_GROUP_NAME_PATTERN),
                    RCEPosAdtGrpHd.PosAdtName.like(FTAP_GROUP_TYPE_PATTERN),
                )
            )
            .distinct()
            .all()
        )
        return [row[0] for row in rows if row[0] is not None]

    @staticmethod
    def _ftap_priority_expression():
        """
        Ekspresi CASE untuk ORDER BY: 0 untuk lowongan FTAP, 1 untuk lainnya,
        sehingga FTAP selalu muncul paling depan sebelum sort utama.
        """
        conditions = [RCEVacantPos.VacantPositionName.like(FTAP_VACANCY_NAME_PATTERN)]
        ftap_ids = VacantPosService._ftap_vacancy_ids()
        if ftap_ids:
            conditions.append(RCEVacantPos.VacantPosId.in_(ftap_ids))
        return case((or_(*conditions), 0), else_=1)

    @staticmethod
    def _apply_group_filters(query, posadt_grp_id):
        """
        Filter lowongan berdasarkan opsi grup atribut (PosAdtGrpId).

        Semantik: OR di dalam satu kategori (PosAdtTypeId), AND antar kategori.
        Contoh: Level = Mechanic|Non Staff dan Location = Jakarta|Kalsel berarti
        (Mechanic OR Non Staff) AND (Jakarta OR Kalsel). Sebelumnya semua ID
        di-AND sehingga memilih >1 opsi pada kategori yang sama selalu kosong,
        karena satu lowongan hanya punya satu nilai per kategori.
        """
        requested_ids = list(dict.fromkeys(posadt_grp_id))  # unik, urutan terjaga
        if not requested_ids:
            return query

        rows = (
            db.session.query(RCEPosAdtGrpDt.PosAdtGrpId, RCEPosAdtGrpDt.PosAdtTypeId)
            .filter(RCEPosAdtGrpDt.PosAdtGrpId.in_(requested_ids))
            .all()
        )

        ids_by_type = {}
        known_ids = set()
        for grp_id, type_id in rows:
            ids_by_type.setdefault(type_id, []).append(grp_id)
            known_ids.add(grp_id)

        # ID yang tidak ditemukan di master tetap dipakai sebagai satu kelompok
        # OR agar tidak diam-diam diabaikan.
        unknown_ids = [grp_id for grp_id in requested_ids if grp_id not in known_ids]
        if unknown_ids:
            ids_by_type.setdefault(None, []).extend(unknown_ids)

        for group_ids in ids_by_type.values():
            subq = db.session.query(RCEPosAdtGrpMbr.VacantPosId).filter(
                RCEPosAdtGrpMbr.PosAdtGrpId.in_(group_ids)
            )
            query = query.filter(RCEVacantPos.VacantPosId.in_(subq))

        return query

    @staticmethod
    def get_all_vacancies(page=1, per_page=100, sort_by="VacantPositionName", sort_order="asc", search="", posadt_grp_id=None, posadt_type_id=None, include_relations=False, exclude_expired=True, ftap_first=True):
        """
        Get all vacancies with pagination and sorting
        Filtered by FgActive and FgShowVacant != 'N'

        Args:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 100)
            sort_by (str): Field to sort by (default: "VacantPositionName")
            sort_order (str): Sort order "asc" or "desc" (default: "asc")
            search (str): Search by position name or code (default: "")
            posadt_grp_id (list): Filter by PosAdtGrpId. OR within the same
                PosAdtTypeId, AND across different PosAdtTypeId.
            posadt_type_id (list): Filter by PosAdtTypeId. Vacancy must have at
                least one attribute of any selected type (OR).
            include_relations (bool): Include related position audit group data (default: False)
            exclude_expired (bool): Exclude vacancies with VacantExpDate < current date (default: True)
            ftap_first (bool): Put FTAP vacancies at the top before applying sort_by (default: True)

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

            # Filter by attribute option: OR within a category, AND across categories
            if posadt_grp_id:
                query = VacantPosService._apply_group_filters(query, posadt_grp_id)

            # Filter by attribute category: vacancy has any attribute of the selected types
            if posadt_type_id:
                type_subq = db.session.query(RCEPosAdtGrpMbr.VacantPosId).filter(
                    RCEPosAdtGrpMbr.PosAdtTypeId.in_(list(set(posadt_type_id)))
                )
                query = query.filter(RCEVacantPos.VacantPosId.in_(type_subq))

            # Search filter
            if search:
                query = query.filter(
                    db.or_(
                        RCEVacantPos.VacantPositionName.ilike(f"%{search}%"),
                        RCEVacantPos.VacantPosCode.ilike(f"%{search}%")
                    )
                )

            # Apply sorting: FTAP first (optional), then requested column
            order_clauses = []
            if ftap_first:
                order_clauses.append(asc(VacantPosService._ftap_priority_expression()))

            sort_column = getattr(RCEVacantPos, sort_by, RCEVacantPos.VacantPositionName)
            if sort_order.lower() == "desc":
                order_clauses.append(desc(sort_column))
            else:
                order_clauses.append(asc(sort_column))

            # Tie-breaker supaya urutan stabil antar halaman (OFFSET/FETCH)
            order_clauses.append(asc(RCEVacantPos.VacantPosId))
            query = query.order_by(*order_clauses)

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
