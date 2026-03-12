from app.models.jobtitle import ODJobTitle
from app import db
from sqlalchemy import asc, desc

class JobTitleService:
    """Service layer untuk mengelola Job Title"""

    @staticmethod
    def get_all_jobtitles(page=1, per_page=100, sort_by="JobTtlId", sort_order="asc", search=""):
        """
        Get all job titles with pagination and sorting
        (where InActDate is null and JobTtlLvlId is not null)

        Args:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 100)
            sort_by (str): Field to sort by (default: "JobTtlId")
            sort_order (str): Sort order "asc" or "desc" (default: "asc")
            search (str): Search by job title name (default: "")

        Returns:
            dict: Paginated job title data
        """
        try:
            # Build query using raw SQL
            from sqlalchemy import text

            # Validate sort_by - only allow safe columns for sorting
            sortable_columns = ["JobTtlId", "JobTtlCode", "JobTtlName", "JobTtlOrgId",
                              "JobTtlLvlId", "UpdDate", "UpdUser", "UpdFlag",
                              "ActDate", "JobTtlReqId", "MaxEmpTypeLvl"]

            if sort_by not in sortable_columns:
                sort_by = "JobTtlId"

            # Validate sort_order
            if sort_order.lower() not in ["asc", "desc"]:
                sort_order = "asc"

            # Build WHERE clause
            where_clause = "WHERE InActDate IS NULL AND JobTtlLvlId IS NOT NULL"
            params = {"limit": per_page, "offset": (page - 1) * per_page}

            if search:
                where_clause += " AND JobTtlName LIKE :search"
                params["search"] = f"%{search}%"

            # Build SQL query
            sql = text(f"""
                SELECT
                    JobTtlId,
                    JobTtlCode,
                    JobTtlName,
                    JobTtlAlias,
                    JobTtlOrgId,
                    JobTtlLvlId,
                    JobTtlGrpId,
                    JobTtlParentId,
                    JobTtlValue,
                    JobLvlTopId,
                    StartLvlId,
                    JobTtlCompGrpId,
                    ActDate,
                    InActDate,
                    Initiator,
                    UpdDate,
                    UpdUser,
                    UpdFlag,
                    JobTtlReqId,
                    JobTtlDesc,
                    ExportDate,
                    FgJobTtlFPK,
                    MaxEmpTypeLvl
                FROM dbo.ODJobTitle
                {where_clause}
                ORDER BY {sort_by} {sort_order.upper()}
                OFFSET :offset ROWS
                FETCH NEXT :limit ROWS ONLY
            """)

            result = db.session.execute(sql, params)
            rows = result.fetchall()

            # Build count query
            count_where = where_clause
            count_params = {}
            if search:
                count_params["search"] = params["search"]

            count_sql = text(f"SELECT COUNT(*) FROM dbo.ODJobTitle {count_where}")
            total = db.session.execute(count_sql, count_params).scalar()

            # Convert to dict
            data = []
            for idx, row in enumerate(rows):
                try:
                    # Access by index
                    dict_data = {
                        "JobTtlId": row[0],
                        "JobTtlCode": row[1],
                        "JobTtlName": row[2],
                        "JobTtlAlias": row[3],
                        "JobTtlOrgId": row[4],
                        "JobTtlLvlId": row[5],
                        "JobTtlGrpId": row[6],
                        "JobTtlParentId": row[7],
                        "JobTtlValue": row[8],
                        "JobLvlTopId": row[9],
                        "StartLvlId": row[10],
                        "JobTtlCompGrpId": row[11],
                        "ActDate": row[12].isoformat() if row[12] is not None else None,
                        "InActDate": row[13].isoformat() if row[13] is not None else None,
                        "Initiator": row[14],
                        "UpdDate": row[15].isoformat() if row[15] is not None else None,
                        "UpdUser": row[16],
                        "UpdFlag": row[17],
                        "JobTtlReqId": row[18],
                        "JobTtlDesc": row[19],
                        "ExportDate": row[20].isoformat() if row[20] is not None else None,
                        "FgJobTtlFPK": row[21],
                        "MaxEmpTypeLvl": row[22]
                    }
                    data.append(dict_data)
                except Exception as e:
                    # Skip rows that fail to convert
                    continue

            # Calculate pagination info
            pages = (total + per_page - 1) // per_page

            return {
                "success": True,
                "data": data,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": total,
                    "pages": pages,
                    "has_next": page < pages,
                    "has_prev": page > 1
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error fetching job titles: {str(e)}"
            }

    @staticmethod
    def get_jobtitle_by_id(jobtitle_id):
        """
        Get a specific job title by ID

        Args:
            jobtitle_id (int): Job title ID

        Returns:
            dict: Job title data
        """
        try:
            jobtitle = ODJobTitle.query.filter(
                ODJobTitle.JobTtlId == jobtitle_id,
                ODJobTitle.InActDate == None,
                ODJobTitle.JobTtlLvlId != None
            ).first()

            if jobtitle:
                return {
                    "success": True,
                    "data": jobtitle.to_dict()
                }
            else:
                return {
                    "success": False,
                    "message": "Job title not found"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error fetching job title: {str(e)}"
            }
